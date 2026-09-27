import os,sys,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import ImageChops
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from storage import ProgressStore
from learning import Learning
from study import StudySession,PracticeBook,PHASES,matches_romaji,compact
from actors import sprite

class V8Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=PracticeBook(ROOT,self.learning)
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def flow(self,key='1:0',index=0):return StudySession(self.learning.by_key[key],self.store,self.book,index)
    def test_six_steps_not_one_question(self):
        f=self.flow();self.assertEqual(len(PHASES),6);self.assertEqual(f.advance(),'blocked')
        f.mark(True,'read');self.assertEqual(f.advance(),'next');self.assertEqual(f.phase,'meaning');self.assertEqual(f.index,0)
    def test_35_authored_profiles_and_all_cards_supported(self):
        self.assertEqual(len(self.book.data['profiles']),35)
        for lesson in self.learning.lessons:
            for c in lesson['cards']:
                p=self.book.profile(c,lesson)
                for key in ['explain','usage','pitfall','kind']:self.assertTrue(p[key])
                self.assertTrue(p['scenario']['correct'])
    def test_writing_preserves_vowel_length(self):
        for text in ['arigatō','arigatou','arigatoo',' A-RI-GA-TOO! ']:self.assertTrue(matches_romaji(text,'arigatō'),text)
        self.assertFalse(matches_romaji('arigato','arigatō'))
        self.assertFalse(matches_romaji('ie','iie'))
        self.assertTrue(matches_romaji('kohii','kōhī') is False)
        self.assertTrue(matches_romaji('koohii','kōhī'))
    def test_listening_only_previously_introduced_words(self):
        for lesson in self.learning.lessons:
            for i,c in enumerate(lesson['cards']):
                f=StudySession(lesson,self.store,self.book,i);f.phase='listen';f.reset_task()
                self.assertLessEqual(f.listen_index,i)
                self.assertTrue(set(f.answers()[0]) <= {x['de'] for x in lesson['cards'][:i+1]})
    def test_mistakes_recorded_without_penalty(self):
        f=self.flow();f.phase='meaning';opts,correct=f.answers();wrong=next(x for x in opts if x!=correct);f.choose(wrong)
        self.assertFalse(f.success);self.assertEqual(f.advance(),'blocked');self.assertEqual(f.metrics()['mistakes'],1)
        self.assertEqual(self.store.data['xp'],0);self.assertIn(f.card_key,self.store.data['review'])
    def test_listening_needs_audio_or_explicit_skip(self):
        f=self.flow(index=1);f.phase='listen';f.reset_task();_,correct=f.answers();f.choose(correct)
        self.assertFalse(f.success);f.audio_skipped=True;f.choose(correct);self.assertTrue(f.success)
        self.assertNotIn('listen',f.metrics()['phases']);self.assertIn('listen',f.metrics()['skipped_phases'])
    def test_resume_keeps_phase_and_old_progress(self):
        self.store.data.update({'xp':75,'completed':['0:0','0:1'],'teacher_id':'aiko'})
        f=self.flow(index=1);f.phase='write';f.snapshot();store=ProgressStore()
        resumed=StudySession(f.lesson,store,self.book,restore=True)
        self.assertEqual((resumed.index,resumed.phase),(1,'write'));self.assertEqual(store.data['xp'],75);self.assertEqual(store.data['teacher_id'],'aiko')
        self.assertTrue(store.path.with_name('progress.before-v8.json').exists())
    def test_recap_contains_only_current_lesson_and_extra_weak_card(self):
        f=self.flow('0:1');f.metrics()['mistakes']=2
        while f.mode!='recap':f.mark(True,'test');self.assertEqual(f.advance(),'next')
        self.assertEqual(set(f.recap),{0,1,2});self.assertGreater(len(f.recap),3)
        f.snapshot();restored=StudySession(f.lesson,self.store,self.book,restore=True)
        self.assertEqual(restored.mode,'recap');self.assertEqual(restored.recap,f.recap)
    def test_all_lessons_can_finish_through_each_phase(self):
        count=0
        for lesson in self.learning.lessons:
            f=StudySession(lesson,self.store,self.book)
            for turn in range(100):
                if f.phase=='understand' and f.mode!='recap':f.mark(True,'read')
                elif f.phase=='write' and f.mode!='recap':f.check_write(f.card['romaji'])
                elif f.phase=='build' and f.mode!='recap' and self.book.blocks(f.card,lesson)[0]:
                    parts,_=self.book.blocks(f.card,lesson);f.tokens=list(range(len(parts)));f.check_build()
                else:
                    f.audio_seen=True;_,correct=f.answers();f.choose(correct)
                self.assertTrue(f.success,(lesson['key'],f.phase));count+=1
                result=f.advance()
                if result=='complete':break
            else:self.fail('No completion: '+lesson['key'])
        self.assertEqual(count,len(self.learning.cards)*7) # 6 guided steps + one recap per card; no test mistakes
    def test_all_assets_animate_and_stay_bounded(self):
        for t in self.learning.teachers:
            a=sprite(str(self.learning.asset(t)),160,250,0,'teacher','idle')
            b=sprite(str(self.learning.asset(t)),160,250,18,'teacher','idle')
            self.assertEqual(a.size,(160,250));self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
            bbox=a.getchannel('A').getbbox();self.assertTrue(bbox and bbox[0]>0 and bbox[1]>0)
    def test_reduced_motion_is_identical(self):
        path=str(self.learning.asset());a=sprite(path,180,280,-1,'teacher','idle');b=sprite(path,180,280,-1,'teacher','speaking')
        self.assertIsNone(ImageChops.difference(a,b).getbbox())
    def test_audio_is_not_a_required_phase(self):self.assertNotIn('speech',PHASES)

if __name__=='__main__':unittest.main(verbosity=2)
