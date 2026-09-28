"""Independent baseline protection: no blessing of changed course/assessment rules."""
import ast,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(s):return hashlib.sha256(s.encode('utf8')).hexdigest()
class PreservationTests(unittest.TestCase):
 def test_original_course_assessment_and_native_models(self):
  base=json.loads((ROOT/'tests/fixtures/exercise-expansion-contract.json').read_text('utf8'))
  course=json.loads((ROOT/'data/course.json').read_text('utf8'));self.assertEqual(course.pop('content_version'), '11.0.7')
  self.assertEqual(sha(json.dumps(course,ensure_ascii=False,sort_keys=True)),base['course_without_version_sha256'])
  current={}
  for node in ast.parse((ROOT/'study.py').read_text('utf8')).body:
   if isinstance(node,ast.ClassDef):
    for f in node.body:
     if isinstance(f,ast.FunctionDef):current[node.name+'.'+f.name]=sha(ast.dump(f))
  for name,digest in base['unchanged_python'].items():self.assertEqual(current[name],digest,name)
  core=(ROOT/'mobile/web/core.mjs').read_text('utf8')
  self.assertEqual(sha(core.split('export class Session')[0]),base['core_before_session'])
  self.assertEqual(sha(core.split('  metrics()')[1]),base['core_from_metrics'])
  css=(ROOT/'mobile/web/styles.css').read_text('utf8')
  self.assertEqual(sha(css[:base['styles_prefix_length']]),base['styles_prefix'])
  native=(ROOT/'mobile/app/src/main/java/de/priestkiller/japanischtrainer/SpeechEngine.kt').read_text('utf8')
  self.assertEqual(sha(native[native.index('    private fun tts()'):native.index('    fun stopPlayback()')]),base['native_model_functions'])
  self.assertEqual(sha(native[native.index('    // Instrumented test'):]),base['native_diagnostic'])
