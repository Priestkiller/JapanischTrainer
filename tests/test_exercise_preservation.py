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
  # 11.0.11 records an additional per-skill metric; remove exactly that hook.
  study=(ROOT/'study.py').read_text('utf8').replace("        skill=PHASE_SKILL.get(self.phase)\n        if skill:\n            index=self.listen_index if self.phase=='listen' and self.mode!='recap' else self.index\n            record_attempt(self.store.data, self.lesson['key']+':'+str(index), skill, ok, skipped or self.hint_used)\n",'')
  for node in ast.parse(study).body:
   if isinstance(node,ast.ClassDef):
    for f in node.body:
     if isinstance(f,ast.FunctionDef):current[node.name+'.'+f.name]=sha(ast.dump(f))
  for name,digest in base['unchanged_python'].items():self.assertEqual(current[name],digest,name)
  core=(ROOT/'mobile/web/core.mjs').read_text('utf8')
  core=core.replace("import {cleanAdaptive,recordAttempt,PHASE_SKILL} from './adaptive.mjs';\n",'').replace("  out.adaptive=cleanAdaptive(input.adaptive);\n",'')
  core=core.replace("    const metricKey=this.phase==='listen'&&this.mode!=='recap'?`${this.lesson.key}:${this.lesson.cards.indexOf(this.listenCard)}`:this.key;\n    recordAttempt(this.store.data,metricKey,PHASE_SKILL[this.phase],ok,skipped||this.hintOpen||(this.phase==='speak'&&(this.support.data.assisted||m.last_speech_outcome==='self_check')));\n",'').replace("    this.metrics().last_speech_outcome=matched?'automatic':'mismatch';\n",'')
  # The 11.0.10 task explicitly adds speech-help persistence and an outcome label.
  # Remove only those additions when comparing the historical assessment contract.
  core=core.replace("import {SpeechSupport,speechDeck} from './speech-support.mjs';\n",'').replace(",'speech_support','speech_reviews'",'').replace("    m.last_speech_outcome='self_check';\n",'')
  self.assertEqual(sha(core.split('export class Session')[0]),base['core_before_session'])
  self.assertEqual(sha(core.split('  metrics()')[1]),base['core_from_metrics'])
  css=(ROOT/'mobile/web/styles.css').read_text('utf8')
  self.assertEqual(sha(css[:base['styles_prefix_length']]),base['styles_prefix'])
  native=(ROOT/'mobile/app/src/main/java/de/priestkiller/japanischtrainer/SpeechEngine.kt').read_text('utf8')
  # 11.0.8 intentionally changes Android ASR; the historical whole-block hash remains in the fixture.
  self.assertEqual(sha(native[native.index('    private fun tts()'):native.index('    @JvmOverloads private fun asr(')]),base['native_tts_function'])
  self.assertEqual(sha(native[native.index('    // Instrumented test'):]),base['native_diagnostic'])
