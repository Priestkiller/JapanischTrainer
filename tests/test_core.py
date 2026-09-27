import os,sys,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from storage import ProgressStore
from learning import Learning
from speech_engine import _audio_quality

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.model=Learning(ROOT,self.store)
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def test_v6_progress_and_backup(self):
        old={'completed':['0:0','0:1','1:0'],'xp':75,'teacher_id':'aiko','speech_scores':{'ありがとう':{'best':88}},'legacy_extension':17}
        self.store.path.write_text(json.dumps(old),encoding='utf8');new=ProgressStore()
        for key in old:self.assertEqual(new.data[key],old[key])
        self.assertTrue(new.path.with_name('progress.before-v8.json').exists())
    def test_xp_awarded_once(self):
        self.store.mark_complete('0:0',20);self.store.mark_complete('0:0',20)
        self.assertEqual(self.store.data['xp'],20);self.assertEqual(self.store.data['completed'],['0:0'])
    def test_course_integrity(self):
        self.assertEqual(len(self.model.lessons),150);self.assertEqual(len(self.model.cards),680)
        for lesson in self.model.lessons:
            self.assertTrue(lesson['cards'])
            for card in lesson['cards']:
                for key in ('jp','de','romaji'):self.assertTrue(card.get(key),(lesson['key'],key))
                self.assertIn(card['de'],self.model.answers(card,lesson))
    def test_no_advanced_grammar_distractors(self):
        for lesson in self.model.lessons:
            allowed={c['de'] for c in lesson['cards']}
            for card in lesson['cards']:self.assertTrue(set(self.model.answers(card,lesson))<=allowed)
    def test_all_teacher_assets_have_alpha(self):
        self.assertEqual(len(self.model.teachers),8)
        for teacher in self.model.teachers:
            for kind in ('full','card','avatar'):
                with Image.open(self.model.asset(teacher,kind)) as im:
                    self.assertEqual(im.mode,'RGBA');self.assertLess(im.getchannel('A').getextrema()[0],10)
    def test_unique_voice_ids(self):
        ids={t['speaker_id'] for t in self.model.teachers}
        self.assertEqual(len(ids),8);self.assertTrue(all(0<=i<10 for i in ids))
    def test_lesson_unlocking(self):
        self.assertTrue(self.model.unlocked('0:0'));self.assertFalse(self.model.unlocked('0:1'))
        self.store.mark_complete('0:0',20);self.assertTrue(self.model.unlocked('0:1'))
    def test_silent_audio_is_not_a_bad_pronunciation_mark(self):
        _,quality=_audio_quality(np.zeros(48000,dtype=np.float32),48000)
        self.assertEqual(quality.status,'bad')
    def test_invalid_file_is_backed_up(self):
        self.store.path.write_text('{broken',encoding='utf8');new=ProgressStore()
        self.assertTrue(new.warning);self.assertTrue(list(new.path.parent.glob('progress.invalid-*.json')))
    def test_current_word_available_for_practice(self):
        self.store.data['last_lesson']={'key':'1:0','card':1}
        self.assertIn('ありがとう',[c['jp'] for c in self.model.available_cards()])
    def test_existing_speech_targets_retained(self):
        self.assertEqual(sum(len(l.get('speech',[])) for l in self.model.lessons if l.get('origin')=='legacy'),62)
if __name__=='__main__':unittest.main(verbosity=2)
