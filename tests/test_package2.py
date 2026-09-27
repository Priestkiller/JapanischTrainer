"""Package 02: content identity, old profiles and explanatory failure behavior.

These tests validate contracts, not natural Japanese or microphone recognition.
"""
import copy,hashlib,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from learning import Learning
from storage import ProgressStore
from study import PracticeBook,StudySession
from tools.upgrade_package2 import GUIDES

ROOT=Path(__file__).resolve().parents[1]
def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class Package2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=PracticeBook(ROOT,self.learning)
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def flow(self,key,index=0):return StudySession(self.learning.by_key[key],self.store,self.book,index)
    def test_first_package_and_all_card_identities_preserved(self):
        baseline=json.loads((ROOT/'tests/fixtures/package01-contract.json').read_text('utf8'))
        data=json.loads((ROOT/'data/course.json').read_text('utf8'))
        raw={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
        self.assertEqual(data['revision'],baseline['revision']);self.assertEqual(data['learning_order'],baseline['order'])
        for key,expected in baseline['foundation_hashes'].items():self.assertEqual(digest(raw[key]),expected,key)
        for key,expected in baseline['identity_hashes'].items():
            l=raw[key];self.assertEqual(digest({'xp':l['xp'],'cards':[[c['jp'],c['romaji'],c['de']] for c in l['cards']]}),expected,key)
    def test_selected_package_is_noncontiguous_and_all_wrong_options_are_explained(self):
        selected=[l for l in self.learning.lessons if l.get('study_guide',{}).get('package')==2]
        self.assertEqual({l['key'] for l in selected},set(GUIDES));self.assertEqual(len(selected),25)
        self.assertEqual(sum(len(l['cards']) for l in selected),121)
        order=[l['key'] for l in self.learning.lessons];self.assertNotEqual([l['key'] for l in selected],order[30:55])
        for l in selected:
            g=l['study_guide'];self.assertEqual(len(g['points']),3)
            for p in g['prerequisites']+g.get('retrieves',[]):self.assertLess(order.index(p),order.index(l['key']))
            for c in l['cards']:
                s=c['detail']['scenario'];self.assertNotIn(s['correct'],s['wrong']);self.assertGreaterEqual(len(set(s['wrong'])),2)
                self.assertEqual(set(s['wrong']),set(s['feedback']));self.assertTrue(all(t.strip() and t!=w for w,t in s['feedback'].items()))
                self.assertIsInstance(c.get('example',{}),dict)
                if c.get('example') and 'example_romaji' in c:
                    self.assertEqual(c['example_romaji'],c['example']['romaji']);self.assertEqual(c['example_de'],c['example']['de'])
    def test_every_wrong_application_stays_open_and_schedules_review(self):
        for key in GUIDES:
            for i,c in enumerate(self.learning.by_key[key]['cards']):
                for value,why in c['detail']['scenario']['feedback'].items():
                    f=self.flow(key,i);f.phase='apply';f.reset_task();f.choose(value)
                    if value not in f.answers()[0]:continue
                    self.assertIn(why,f.feedback);self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked')
                    self.assertEqual(self.store.data['review'][f.card_key]['box'],0)
        self.assertEqual(self.store.data['xp'],0);self.assertEqual(self.store.data['completed'],[])
    def test_failure_is_about_the_heard_card_not_the_current_card(self):
        f=self.flow('v11:polite-past',4);f.phase='listen';f.reset_task();f.listen_card=f.lesson['cards'][2];f.audio_seen=True
        f.choose(f.lesson['cards'][1]['de'])
        self.assertIn('Vergangenheit',f.feedback);self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked')
    def test_written_aliases_do_not_accept_unrelated_answers(self):
        for answer in ['nani','nan','nani / nan']:
            f=self.flow('13:0');f.phase='write';f.check_write(answer);self.assertTrue(f.success,answer)
        f=self.flow('13:0');f.phase='write';f.check_write('doko');self.assertFalse(f.success)
    def test_old_profile_retains_completed_xp_teacher_review_and_resume(self):
        self.store.data.update(course_revision=11,completed=['0:0','1:0','14:0'],xp=321,teacher_id='ren',
          review={'14:0:2':{'box':3,'due':9999999999}},legacy_unlocked=['v11:positions'],
          last_lesson={'key':'v11:positions','card':2},
          lesson_sessions={'v11:positions':{'index':2,'phase':'write','mode':'learn','recap':[],'recap_total':0,'recap_passed':0}})
        self.store.save();before=copy.deepcopy(self.store.data)
        restarted=ProgressStore();learning=Learning(ROOT,restarted);book=PracticeBook(ROOT,learning)
        f=StudySession(learning.by_key['v11:positions'],restarted,book,restore=True)
        for field in ['completed','xp','teacher_id','review','legacy_unlocked','last_lesson','lesson_sessions']:
            self.assertEqual(restarted.data[field],before[field],field)
        self.assertEqual((f.phase,f.index),('write',2));self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked')
        self.assertTrue(learning.unlocked('v11:positions'))
    def test_build_and_write_errors_explain_without_unlocking(self):
        f=self.flow('v11:location-action');f.phase='build';f.tokens=[];f.check_build()
        self.assertIn('Partikel',f.feedback);self.assertFalse(f.success)
        f.phase='write';f.reset_task();f.check_write('wrong');self.assertIn('Bewegungsziel',f.feedback)
        self.assertEqual(f.advance(),'blocked');self.assertEqual(self.store.data['xp'],0)

if __name__=='__main__':unittest.main()
