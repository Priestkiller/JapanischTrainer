"""Package 04 contracts, exhaustive practice and real saved-profile boundaries.

These are software/content-structure tests, not human language acceptance.
"""
import copy, hashlib, json, os, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from learning import Learning
from storage import ProgressStore
from study import PracticeBook, StudySession, PHASES
from tools import upgrade_package4 as authored

ROOT=Path(__file__).resolve().parents[1]
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class Package4Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=PracticeBook(ROOT,self.learning)
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def flow(self,key,index=0):return StudySession(self.learning.by_key[key],self.store,self.book,index)
    def test_previous_80_identity_and_only_explicit_numbers_correction(self):
        base=json.loads((ROOT/'tests/fixtures/package03-contract.json').read_text('utf-8'))
        data=json.loads((ROOT/'data/course.json').read_text('utf-8'))
        raw={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
        self.assertEqual(len(base['reviewed']),80);self.assertTrue(set(base['reviewed']).isdisjoint(authored.GUIDES))
        self.assertEqual(data['learning_order'],base['order']);self.assertEqual(data['revision'],base['revision'])
        for k,expected in base['lessons'].items():
            if k not in authored.GUIDES and k!='12:0':self.assertEqual(digest(raw[k]),expected,k)
        expected=copy.deepcopy(base['numbers_lesson']);authored.improve_numbers({'12:0':expected})
        self.assertEqual(raw['12:0'],expected)
        # No other old card, lesson metadata or speech target in that lesson may change.
        old=copy.deepcopy(base['numbers_lesson']);changed=copy.deepcopy(raw['12:0'])
        changed['cards'][4]['detail']=old['cards'][4]['detail'];self.assertEqual(changed,old)
        for k,l in raw.items():self.assertEqual(digest({'xp':l['xp'],'cards':[[c['jp'],c['romaji'],c['de']] for c in l['cards']]}),base['identities'][k],k)
        for path,sha in base['protected_files'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha,path)
    def test_inventory_explicit_prerequisites_and_no_duplicate_review_count(self):
        selected=[l for l in self.learning.lessons if l.get('study_guide',{}).get('package')==4]
        self.assertEqual({l['key'] for l in selected},set(authored.GUIDES));self.assertEqual(len(selected),25)
        self.assertEqual(sum(len(l['cards']) for l in selected),123)
        guided=[l for l in self.learning.lessons if l.get('study_guide')]
        self.assertEqual((len(guided),sum(len(l['cards']) for l in guided)),(105,501))
        order=self.learning.course['learning_order']
        self.assertNotEqual([l['key'] for l in selected],order[80:105])
        for l in selected:
            g=l['study_guide'];self.assertEqual(len(g['points']),3);self.assertTrue(g['recall']);self.assertTrue(l['goal'])
            for k in g['prerequisites']+g['retrieves']:self.assertLess(order.index(k),order.index(l['key']),(l['key'],k))
            for c in l['cards']:
                q=c['detail']['scenario'];self.assertNotIn(q['correct'],q['wrong']);self.assertEqual(len(q['wrong']),len(set(q['wrong'])))
                self.assertEqual(set(q['wrong']),set(q['feedback']));self.assertTrue(all(len(x)>25 for x in q['feedback'].values()))
                self.assertNotIn('dieser Karte',q['question']);self.assertTrue(all(c['example'][x] for x in ['jp','romaji','de']))
                if 'example_romaji' in c:self.assertEqual(c['example']['romaji'],c['example_romaji']);self.assertEqual(c['example']['de'],c['example_de'])
    def test_every_new_card_all_phases_wrong_empty_hint_and_correct(self):
        for key in authored.GUIDES:
            for i,c in enumerate(self.learning.by_key[key]['cards']):
                for phase in PHASES[1:]:
                    f=self.flow(key,i);f.phase=phase;f.reset_task()
                    self.assertEqual(f.advance(),'blocked');f.hint_used=True;self.assertEqual(f.advance(),'blocked')
                    if phase=='write':
                        f.check_write('');self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked')
                        f.check_write('unrelated');self.assertFalse(f.success);f.check_write(c['romaji'])
                    elif phase=='build':
                        parts,_=self.book.blocks(c,f.lesson)
                        if parts:
                            f.tokens=[];f.check_build();self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked')
                            f.tokens=list(range(len(parts)));f.check_build()
                        else:
                            options,correct=f.answers();f.choose(correct)
                    else:
                        f.audio_seen=True;options,correct=f.answers()
                        for wrong in [x for x in options if x!=correct]:
                            f.choose(wrong);self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked');self.assertGreater(len(f.feedback),30)
                            if phase=='apply':self.assertIn(c['detail']['scenario']['feedback'][wrong],f.feedback)
                        f.choose(correct)
                    self.assertTrue(f.success,(key,i,phase))
        self.assertEqual(self.store.data['xp'],0);self.assertEqual(self.store.data['completed'],[])
    def test_all_old_sessions_resume_and_do_not_gain_credit(self):
        for key in [*authored.GUIDES,'12:0']:
            index=4 if key=='12:0' else 1
            self.store.data.update(course_revision=11,xp=456,teacher_id='ren',tts_speed=.85,completed=['0:0','14:0'],legacy_unlocked=[key],
                review={'14:0:2':{'box':3,'due':9999999999}},last_lesson={'key':key,'card':index},
                lesson_sessions={key:{'index':index,'phase':'write','mode':'learn','recap':[],'recap_total':0,'recap_passed':0}})
            self.store.save();before=copy.deepcopy(self.store.data)
            store=ProgressStore();learning=Learning(ROOT,store);f=StudySession(learning.by_key[key],store,PracticeBook(ROOT,learning),restore=True)
            for field in ['xp','teacher_id','tts_speed','completed','legacy_unlocked','review','last_lesson','lesson_sessions']:self.assertEqual(store.data[field],before[field],(key,field))
            self.assertEqual((f.phase,f.index),('write',index));self.assertEqual(f.advance(),'blocked')
    def test_numbers_preparation_is_not_an_assessment_bypass(self):
        f=self.flow('12:0',4);p=f.card['detail'];self.assertEqual(len(p['parts']),3);self.assertEqual(len(p['extra']),3)
        f.phase='write';f.reset_task();f.hint_used=True;f.check_write('go roku');self.assertFalse(f.success)
        self.assertEqual(f.advance(),'blocked');f.check_write(f.card['romaji']);self.assertTrue(f.success)
        f.phase='apply';f.reset_task();f.choose('ろく');self.assertFalse(f.success);f.choose('はち');self.assertTrue(f.success)
        self.assertEqual(self.store.data['xp'],0)
    def test_authoring_is_idempotent(self):
        temp=Path(self.tmp.name);(temp/'data').mkdir()
        for name in ['course.json','deep_lessons.json']:(temp/'data'/name).write_bytes((ROOT/'data'/name).read_bytes())
        before=(temp/'data/course.json').read_bytes()
        with patch.object(authored,'ROOT',temp):authored.upgrade()
        self.assertEqual((temp/'data/course.json').read_bytes(),before)

if __name__=='__main__':unittest.main()
