"""Package 03 contracts and behavior; no claim of human language/audio testing."""
from vowel_clarity_contract import before_vowel_clarity
import copy, hashlib, json, os, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from learning import Learning
from storage import ProgressStore
from study import PracticeBook, StudySession
from tools import upgrade_package3 as authored
from tools import upgrade_package4 as following

ROOT=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class Package3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=PracticeBook(ROOT,self.learning)
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def flow(self,key,index=0):return StudySession(self.learning.by_key[key],self.store,self.book,index)
    def test_previous_55_and_all_other_unselected_lessons_unchanged(self):
        base=json.loads((ROOT/'tests/fixtures/package02-contract.json').read_text())
        data=json.loads((ROOT/'data/course.json').read_text('utf-8'))
        raw={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
        self.assertEqual(data['learning_order'],base['order']);self.assertEqual(data['revision'],base['revision'])
        self.assertEqual(len(base['reviewed']),55)
        for k,expected in base['lessons'].items():
            # Package 04 is checked against its newer full 11.0.5 contract.
            # All other original 11.0.4 hashes remain enforced here.
            if k not in authored.GUIDES and k not in following.GUIDES:self.assertEqual(digest(before_vowel_clarity(k,raw[k])),expected,k)
        for k,l in raw.items():self.assertEqual(digest({'xp':l['xp'],'cards':[[c['jp'],c['romaji'],c['de']] for c in l['cards']]}),base['identities'][k],k)
    def test_inventory_prerequisites_solutions_and_feedback(self):
        lessons=[l for l in self.learning.lessons if l.get('study_guide',{}).get('package')==3]
        self.assertEqual({l['key'] for l in lessons},set(authored.GUIDES));self.assertEqual(len(lessons),25)
        self.assertEqual(sum(len(l['cards']) for l in lessons),119)
        order=self.learning.course['learning_order']
        for l in lessons:
            self.assertEqual(len(l['study_guide']['points']),3)
            for k in l['study_guide']['prerequisites']+l['study_guide']['retrieves']:self.assertLess(order.index(k),order.index(l['key']))
            for c in l['cards']:
                q=c['detail']['scenario'];self.assertNotIn(q['correct'],q['wrong']);self.assertEqual(len(q['wrong']),len(set(q['wrong'])))
                self.assertEqual(set(q['wrong']),set(q['feedback']));self.assertTrue(all(q['feedback'].values()))
                self.assertTrue(all(c['example'][f] for f in ['jp','romaji','de']))
    def test_all_application_answers_and_failures(self):
        for key in authored.GUIDES:
            for i,c in enumerate(self.learning.by_key[key]['cards']):
                q=c['detail']['scenario']
                for wrong in q['wrong']:
                    f=self.flow(key,i);f.phase='apply';f.reset_task();f.choose(wrong)
                    if wrong in f.answers()[0]:
                        self.assertFalse(f.success);self.assertIn(q['feedback'][wrong],f.feedback);self.assertEqual(f.advance(),'blocked')
                f=self.flow(key,i);f.phase='apply';f.reset_task();f.choose(q['correct']);self.assertTrue(f.success,(key,i))
        self.assertEqual(self.store.data['xp'],0);self.assertEqual(self.store.data['completed'],[])
    def test_all_selected_old_sessions_resume_without_new_credit(self):
        for key in authored.GUIDES:
            self.store.data.update(course_revision=11,xp=456,teacher_id='ren',completed=['0:0','14:0'],legacy_unlocked=[key],
                review={'14:0:2':{'box':3,'due':9999999999}},last_lesson={'key':key,'card':1},
                lesson_sessions={key:{'index':1,'phase':'write','mode':'learn','recap':[],'recap_total':0,'recap_passed':0}})
            self.store.save();before=copy.deepcopy(self.store.data)
            store=ProgressStore();learning=Learning(ROOT,store);f=StudySession(learning.by_key[key],store,PracticeBook(ROOT,learning),restore=True)
            for field in ['xp','teacher_id','completed','legacy_unlocked','review','last_lesson','lesson_sessions']:self.assertEqual(store.data[field],before[field],(key,field))
            self.assertEqual((f.phase,f.index),('write',1));self.assertEqual(f.advance(),'blocked')
    def test_authoring_composition_is_idempotent_without_touching_previous_packages(self):
        temp=Path(self.tmp.name);(temp/'data').mkdir()
        for name in ['course.json','deep_lessons.json']:(temp/'data'/name).write_bytes((ROOT/'data'/name).read_bytes())
        before=(temp/'data/course.json').read_bytes()
        with patch.object(authored,'ROOT',temp):authored.upgrade()
        # Reapply the one explicit later correction (12:0:4), never bless new
        # hashes wholesale or let an older authoring script downgrade content.
        with patch.object(following,'ROOT',temp):following.upgrade()
        self.assertEqual((temp/'data/course.json').read_bytes().replace(b'\r\n',b'\n'),before.replace(b'\r\n',b'\n'))

if __name__=='__main__':unittest.main()
