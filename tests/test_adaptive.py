import json,os,tempfile,unittest,zipfile,hashlib
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
from adaptive import clean_adaptive,record_attempt,daily_plan,finish_daily
from storage import ProgressStore
from learning import Learning
from study import PracticeBook,StudySession
from modelpacks import unpack,check_url
from speech_trial import prepare,NoVoice
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

class AdaptiveTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
  self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=PracticeBook(ROOT,self.learning)
 def tearDown(self):self.env.stop();self.tmp.cleanup()
 def test_fresh_plan_explains_before_testing_and_preserves_progress(self):
  d=self.store.data;before=deepcopy(d);upcoming=self.learning.cards[:2]
  p=daily_plan(d,self.learning.cards,self.learning.available_cards(),upcoming,'2026-09-30',100)
  self.assertEqual([t['skill'] for t in p['tasks']],['intro','intro'])
  for t in p['tasks']:
   self.assertTrue(finish_daily(d,t,True,now=100));self.assertFalse(finish_daily(d,t,True,now=100))
  self.store.save();loaded=ProgressStore();self.assertEqual(loaded.data['adaptive'],d['adaptive'])
  self.assertEqual(d['xp'],before['xp']);self.assertEqual(d['completed'],before['completed']);self.assertEqual(d['last_lesson'],before['last_lesson'])
  again=daily_plan(d,self.learning.cards,[],upcoming,'2026-09-30',200);self.assertEqual(len(again['done']),2)
 def test_weak_skill_is_independent_and_assistance_is_not_mastery(self):
  d=self.store.data;c=self.learning.cards[0];d['adaptive']['introduced']=[c['key']]
  record_attempt(d,c['key'],'read',True,now=100);record_attempt(d,c['key'],'speak',False,now=101)
  p=daily_plan(d,self.learning.cards,[],[],'2026-09-30',200);self.assertEqual(p['tasks'][0]['skill'],'speak')
  self.assertTrue(finish_daily(d,p['tasks'][0],True,True,now=200));m=d['adaptive']['skills'][c['key']]['speak'];self.assertEqual(m['right'],0);self.assertEqual(m['due'],86600)
  self.assertEqual(d['adaptive']['skills'][c['key']]['read']['right'],1)
 def test_old_session_retains_xp_ids_and_phase(self):
  d=self.store.data;l=self.learning.lessons[0];flow=StudySession(l,self.store,self.book,0);flow.mark(True,'ok');flow.advance()
  d['xp']=777;self.store.save();old=deepcopy(d['lesson_sessions']);restored=ProgressStore()
  self.assertEqual(restored.data['xp'],777);self.assertEqual(restored.data['lesson_sessions'],old)
  again=StudySession(l,restored,PracticeBook(ROOT,Learning(ROOT,restored)),0,restore=True);self.assertEqual(again.phase,flow.phase)
 def test_course_listening_metric_uses_heard_card(self):
  l=self.learning.lessons[0];s=StudySession(l,self.store,self.book,2);s.phase='listen';s.listen_index=0;s.mark(False,'retry')
  self.assertEqual(self.store.data['adaptive']['skills'][l['key']+':0']['listen']['attempts'],1)
 def test_malformed_import_safe(self):
  a=clean_adaptive({'skills':{'x':{'read':{'attempts':float('nan'),'due':-9}}},'daily':{'date':'2026-09-30','tasks':[None,{'id':'x','card':'x','skill':'nonsense'}],'done':['no']}})
  self.assertEqual(a['skills']['x']['read']['due'],0);self.assertEqual(a['daily']['tasks'],[])
 def test_practice_evidence_is_real_known_course_content(self):
  data=json.loads((ROOT/'data/practice_content.json').read_text('utf8'))
  for story in data['stories']:
   lesson=self.learning.by_key[story['lesson']]
   for q in story['questions']:
    self.assertIn(q['correct'],q['options']);self.assertEqual(len(q['options']),len(set(q['options'])));self.assertTrue(lesson['cards'][q['evidence']]['jp'])
 def test_signal_gate_rejects_silence_click_clipping(self):
  for x in [np.zeros(32000),np.r_[np.zeros(8000),.5,np.zeros(8000)],np.tile([1.,-1.],16000)]:
   with self.assertRaises(ValueError):prepare(x,16000,True)
 def test_model_archive_rejects_tamper_extra_paths_and_http(self):
  root=Path(self.tmp.name);z=root/'pack.zip'
  def pack(name='weights.onnx',data=b'weights'):
   with zipfile.ZipFile(z,'w') as out:out.writestr(name,data)
   return dict(bytes=z.stat().st_size,sha256=hashlib.sha256(z.read_bytes()).hexdigest(),files=[dict(path=name,size=len(data),sha256=hashlib.sha256(data).hexdigest())])
  m=pack();unpack(z,root/'good',m);self.assertEqual((root/'good/weights.onnx').read_bytes(),b'weights')
  m['sha256']='0'*64
  with self.assertRaises(ValueError):unpack(z,root/'bad',m)
  m=pack('../escape')
  with self.assertRaises(ValueError):unpack(z,root/'traversal',m)
  self.assertFalse((root/'escape').exists())
  m=pack();m['files'].append(dict(path='missing',size=1,sha256='0'*64))
  with self.assertRaises(ValueError):unpack(z,root/'extra',m)
  with self.assertRaises(RuntimeError):unpack(z,root/'cancel',pack(),lambda:True)
  for url in ['http://example.com','https://user:pass@example.com','file:///c:/x']:
   with self.assertRaises(ValueError):check_url(url)
