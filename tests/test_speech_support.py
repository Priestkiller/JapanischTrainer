import copy,json,unittest
from pathlib import Path
from types import SimpleNamespace
from speech_support import SpeechSupport,speech_deck
from learning import Learning
ROOT=Path(__file__).resolve().parents[1]
class SpeechSupportTests(unittest.TestCase):
 def store(self):return SimpleNamespace(data={'course_revision':11,'xp':123,'completed':['0:0'],'speech_scores':{'あ':{'best':91}},'lesson_sessions':{}},save=lambda:None)
 def test_exact_threshold_terminal_events_cancel_and_restore(self):
  store=self.store();s=SpeechSupport(store,'task',{'card':'0:0:0'})
  self.assertFalse(s.open());self.assertTrue(s.begin('cancel'));self.assertFalse(s.begin('double'));s.cancel();self.assertFalse(s.finish('cancel','mismatch'))
  for i,reason in enumerate(['mismatch','unreliable','technical'],1):
   s=SpeechSupport(store,'task');self.assertFalse(s.finish('old','mismatch'));self.assertTrue(s.begin(str(i)));self.assertTrue(s.finish(str(i),reason));self.assertFalse(s.finish(str(i),reason));self.assertEqual(s.data['failures'],i);self.assertEqual(s.open(),i==3)
  self.assertIn('kein Aussprachefehler',s.data['feedback']);self.assertEqual(store.data['xp'],123)
 def test_choice_requires_confirmation_then_defers_without_score(self):
  store=self.store();s=SpeechSupport(store,'task',{'card':'0:0:0'});cards=[{'key':str(i),'jp':jp,'de':de,'romaji':ro} for i,jp,de,ro in [(1,'あ','Laut a','a'),(2,'い','Laut i','i')]];d=speech_deck(cards[0],[],cards)
  old=copy.deepcopy({k:store.data[k] for k in ['xp','completed','speech_scores']})
  for i in range(3):s.begin(str(i));s.finish(str(i),'technical')
  self.assertTrue(s.open());s.select(d['correct']);self.assertFalse(s.confirm(d));s.prepare();s.select('2');self.assertFalse(s.confirm(d));self.assertIn('い',s.data['feedback']);s.select(d['correct']);self.assertTrue(s.confirm(d));self.assertFalse(s.confirm(d));self.assertEqual({k:store.data[k] for k in old},old)
  resumed=SpeechSupport(store,'task');self.assertTrue(resumed.data['assisted']);self.assertFalse(resumed.begin('more'));self.assertEqual(store.data['speech_reviews']['task']['card'],'0:0:0')
  resumed.new_round();self.assertEqual(resumed.data['failures'],0);resumed.begin('later');resumed.finish('later','accepted');self.assertNotIn('task',store.data['speech_reviews'])
 def test_all_course_cards_have_unique_decks_and_explicit_first_introduction(self):
  learning=Learning(ROOT,self.store())
  for i,c in enumerate(learning.cards):
   d=speech_deck(c,learning.cards[:i+1],learning.cards)
   self.assertGreaterEqual(len(d['options']),2,c['key']);self.assertEqual(sum(v['id']==d['correct'] for v in d['options']),1)
   self.assertEqual(len({v['de'] for v in d['options']}),len(d['options']))
   if not d['needsPreparation']:self.assertTrue({v['id'] for v in d['options']}.issubset({v['key'] for v in learning.cards[:i+1]}))
  self.assertTrue(speech_deck(learning.cards[0],learning.cards[:1],learning.cards)['needsPreparation'])
