"""Behavior and source contracts for real additional exercises, with isolated profiles."""
import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from exercises import ExerciseBook,ExerciseRound,matches,order
from learning import Learning
from storage import ProgressStore

ROOT=Path(__file__).resolve().parents[1]

def solve(r):
    t=r.task;d=r.answer;k=t['family']
    if k in ('echo','recall'):r.heard();return r.check(t['accepted_speech'][0])
    if k=='pairs':
        for p in t['pairs']:r.heard(p['id'])
        r.set('pairs',{p['id']:p['id'] for p in t['pairs']})
    elif k in ('choice_gap','read'):r.set('choice',t['answers'][0])
    elif k=='hear_gap':r.heard();r.set('text',t['answers'][0])
    else:
        remaining=list(t['tokens']);ids=[]
        for word in t['solutions'][0]:
            token=next(x for x in remaining if x['text']==word);ids.append(token['id']);remaining.remove(token)
        r.set('tokens' if k=='translate' else 'slots',ids if k=='translate' else {str(i):v for i,v in enumerate(ids)})
    return r.check()

class ExerciseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=ExerciseBook(ROOT)
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def new(self,key):return ExerciseRound(self.book,self.learning.by_key[key],self.store)
    def test_curated_sources_and_all_eight_families(self):
        self.assertEqual(len(self.book.packs),25);self.assertEqual(len(self.book.tasks),156)
        self.assertEqual(len({t['id'] for t in self.book.tasks.values()}),156)
        self.assertEqual(set(t['family'] for t in self.book.tasks.values()),{'pairs','echo','recall','hear_gap','choice_gap','multi_gap','translate','read'})
        for p in self.book.packs.values():
            lesson=self.learning.by_key[p['lesson']];self.assertTrue(lesson.get('study_guide'))
            reviewed=set(self.learning.course['learning_order'][:30])|{l['key'] for l in self.learning.lessons if l.get('study_guide',{}).get('package') in (2,3,4)}
            self.assertIn(p['lesson'],reviewed)
            for key in p['introduced']:
                lessonkey,i=key.rsplit(':',1);self.assertEqual(lessonkey,p['lesson']);self.assertTrue(lesson['cards'][int(i)]['detail']['explain'])
            for tid in p['tasks']:
                t=self.book.tasks[tid];self.assertIn(t['card'],p['introduced']);self.assertTrue(set(t['prerequisites'])<=set(p['introduced']))
                if t['repeat']:self.assertIn(t['repeat'],p['tasks'])
                self.assertTrue(t['why']);self.assertTrue(t['hint'])
                if t['family']=='pairs':
                    for field in ['id','reading','de']:self.assertEqual(len(t['pairs']),len({v[field] for v in t['pairs']}))
                for c in t.get('choices',[]):self.assertTrue(c['feedback'])
                if t['family']=='choice_gap':
                    introduced=' '.join(lesson['cards'][int(k.rsplit(':',1)[1])]['jp'] for k in p['introduced'])
                    for c in t['choices']:self.assertIn(c['text'],introduced)
                for solution in t.get('solutions',[]):
                    pool=[v['text'] for v in t['tokens']]
                    for word in solution:self.assertIn(word,pool);pool.remove(word)
    def test_all_rounds_wrong_help_solutions_and_no_fake_progress(self):
        self.store.data['xp']=432;self.store.data['completed']=['0:0'];self.store.data['teacher_id']='ren'
        self.store.data['lesson_sessions']['5:0']={'index':2,'phase':'write','mode':'learn'}
        old=copy.deepcopy(self.store.data['lesson_sessions']['5:0']);seen=[]
        for key in self.book.packs:
            r=self.new(key);self.assertEqual(r.state['stage'],'intro');self.assertFalse(r.check('anything'));r.start()
            for _ in range(40):
                if r.state['stage']=='complete':break
                t=r.task;seen.append(t['id']);self.assertFalse(r.advance());r.help(1);self.assertFalse(r.answer['success'])
                if t['family'] in ('echo','recall'):
                    r.heard();self.assertFalse(r.check(''));self.assertFalse(r.check('これは別の答え'))
                else:
                    for p in t.get('pairs',[]):r.heard(p['id'])
                    r.heard();self.assertFalse(r.check());self.assertTrue(r.answer['feedback'])
                r.help(2);self.assertFalse(r.answer['success']);self.assertTrue(solve(r),t['id']);n=len(r.state['outcomes']);solve(r);self.assertEqual(n,len(r.state['outcomes']))
                self.assertEqual(r.state['outcomes'][-1]['result'],'solution');self.assertTrue(r.advance())
            self.assertEqual(r.state['stage'],'complete');self.assertLessEqual(len(r.state['review']),6)
        self.assertEqual(set(seen),set(self.book.tasks));self.assertEqual(self.store.data['xp'],432);self.assertEqual(self.store.data['completed'],['0:0']);self.assertEqual(self.store.data['teacher_id'],'ren');self.assertEqual(self.store.data['lesson_sessions']['5:0'],old)
    def test_restore_preserves_identity_inputs_help_and_results(self):
        r=self.new('5:0');r.start();r.state['index']=5;r.set('text','mi');r.help(1)
        state=copy.deepcopy(r.state);loaded=self.new('5:0');self.assertEqual(loaded.state,state)
        # Use the actual Windows export/import handlers and a fresh disk load.
        from app import TrainerApp
        from types import SimpleNamespace
        file=Path(self.tmp.name)/'export.json'
        app=SimpleNamespace(root=None,store=self.store,notify=lambda *_:None,request_draw=lambda:None)
        with patch('app.filedialog.asksaveasfilename',return_value=str(file)):TrainerApp.export_progress(app)
        self.store.data['lesson_sessions']={};self.store.save()
        with patch('app.filedialog.askopenfilename',return_value=str(file)),patch('app.messagebox.askyesno',return_value=True),patch('app.messagebox.showerror',side_effect=AssertionError('Import failed')):TrainerApp.import_progress(app)
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store)
        self.assertEqual(self.new('5:0').state,state);self.assertTrue((Path(self.tmp.name)/'progress.before-import.json').exists())
        self.assertEqual(self.store.data['xp'],0)
    def test_audio_gate_and_technical_failures_never_pass(self):
        r=self.new('5:0');r.start();self.assertFalse(r.check(r.task['audio']));r.technical('Permission denied');self.assertFalse(r.advance());self.assertNotIn(r.task['card'],self.store.data['review'])
        r.heard();self.assertTrue(solve(r));r.advance();r.advance();self.assertFalse(r.answer['success'])
    def test_meaningful_normalization_keeps_negation_length_and_small_kana(self):
        self.assertTrue(matches('コーヒー',['こーひー'],'speech'));self.assertTrue(matches('学生です',['がくせいです','学生です'],'speech'))
        for a,b in [('のみません','のみます'),('きて','きって'),('おばさん','おばあさん'),('こんにちわ','こんにちは'),('しや','しゃ'),('nani','nan')]:self.assertFalse(matches(a,[b],'speech'))
        self.assertTrue(matches('koohii',['kōhī'],'romaji'));self.assertFalse(matches('kohi',['kōhī'],'romaji'));self.assertFalse(matches("kani",["kan'i"],'romaji'))
    def test_partial_multigap_and_combined_solution(self):
        r=self.new('5:0');r.start();r.state['index']=next(i for i,k in enumerate(r.state['queue']) if self.book.tasks[k]['family']=='multi_gap')
        t=r.task;first=next(x['id'] for x in t['tokens'] if x['text']==t['solutions'][0][0]);r.set('slots',{'0':first});self.assertFalse(r.check());self.assertEqual(r.answer['per_slot'],[True,False]);self.assertFalse(r.advance());self.assertTrue(solve(r))
    def test_duplicate_token_id_is_not_reused_and_permutation_is_stable(self):
        r=self.new('5:0');r.start();r.state['index']=4;t=r.task
        old=copy.deepcopy(t);t['tokens']=[{'id':'a','text':'も'},{'id':'b','text':'も'}];t['solutions']=[['も','も']]
        try:r.set('tokens',['a','a']);self.assertFalse(r.check());r.set('tokens',['a','b']);self.assertTrue(r.check())
        finally:t.clear();t.update(old)
        self.assertEqual(order([0,1,2],'left'),order([0,1,2],'left'));self.assertNotEqual(order(list(range(9)),'left'),order(list(range(9)),'right'))
    def test_unknown_content_revision_reintroduces_without_resetting_old_profile(self):
        r=self.new('5:0');r.start();r.state['revision']=0;r.save();self.store.data['completed']=['0:0'];self.store.data['xp']=20
        r=self.new('5:0');self.assertEqual(r.state['stage'],'intro');self.assertEqual(self.store.data['xp'],20);self.assertEqual(self.store.data['completed'],['0:0'])

    def test_all_explicit_alternatives_and_every_wrong_choice(self):
        for t in self.book.tasks.values():
            r=self.new(t['lesson']);r.restart();r.start();r.state['index']=r.state['queue'].index(t['id']);r.heard()
            if t['family'] in ('echo','recall'):
                for variant in t['accepted_speech']:
                    r.answer['success']=False;self.assertTrue(r.check(variant),(t['id'],variant))
            for variant in t.get('solutions',[]):
                pool=list(t['tokens']);ids=[]
                for word in variant:
                    token=next(x for x in pool if x['text']==word);pool.remove(token);ids.append(token['id'])
                r.answer['success']=False;r.set('tokens' if t['family']=='translate' else 'slots',ids if t['family']=='translate' else {str(i):v for i,v in enumerate(ids)})
                self.assertTrue(r.check(),(t['id'],variant))
            for choice in t.get('choices',[]):
                r.answer['success']=False;r.set('choice',choice['id']);self.assertEqual(r.check(),choice['id'] in t['answers']);self.assertIn(choice['feedback'],r.answer['feedback'])

    def test_base_task_drafts_restore_without_completing_a_phase(self):
        from study import StudySession,PracticeBook
        book=PracticeBook(ROOT,self.learning);l=self.learning.by_key['5:0']
        for phase in ['write','build']:
            f=StudySession(l,self.store,book,3);f.phase=phase;f.reset_task();f.input_text='mizu o';f.tokens=[1,0];f.hint_used=True;f.snapshot()
            restored=StudySession(l,self.store,book,restore=True)
            self.assertEqual((restored.input_text,restored.tokens,restored.hint_used),('mizu o',[1,0],True));self.assertEqual(restored.advance(),'blocked')
        self.assertEqual(self.store.data['xp'],0)

    def test_cancelled_tts_never_plays_after_generation(self):
        from speech_engine import LocalSpeechEngine
        from unittest.mock import MagicMock
        engine=LocalSpeechEngine();cancelled=[False];tts=MagicMock()
        def generated(*args):cancelled[0]=True;return type('Audio',(),{'samples':[.1]*100,'sample_rate':24000})()
        tts.generate.side_effect=generated
        with patch.object(engine,'_ensure_tts',return_value=tts),patch('speech_engine.sd') as output:
            engine.speak('みず',cancelled=lambda:cancelled[0]);output.play.assert_not_called()

    def test_malformed_import_is_bounded_and_cannot_gain_xp(self):
        r=self.new('5:0');r.state.update(index='bad',review=[None,'foreign'],stage='review',outcomes=[{}]*999,task={'text':None,'help':999,'tokens':{},'slots':[]});r.save()
        restored=self.new('5:0');self.assertEqual(restored.state['stage'],'complete');self.assertEqual(restored.answer['text'],'');self.assertLessEqual(len(restored.state['outcomes']),200);self.assertEqual(self.store.data['xp'],0)

if __name__=='__main__':unittest.main()
