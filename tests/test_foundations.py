"""11.0.2 curriculum contracts; no claim of human language validation."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class FoundationTests(unittest.TestCase):
    def test_guides_use_existing_earlier_lessons_and_leave_no_foundation_fallback(self):
        data=json.loads((ROOT/'data/course.json').read_text('utf-8'))
        lessons={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
        order=data['learning_order'];guided=[k for k in order if 'study_guide' in lessons[k] and lessons[k]['study_guide'].get('package',1)==1]
        self.assertEqual(guided,order[:30])
        for key in guided:
            lesson=lessons[key];g=lesson['study_guide']
            self.assertTrue(lesson['goal']);self.assertEqual(len(g['points']),3);self.assertTrue(g['recall'])
            for prior in g['prerequisites']:
                self.assertIn(prior,lessons);self.assertLess(order.index(prior),order.index(key))
            for card in lesson['cards']:
                scenario=card['detail']['scenario']
                self.assertNotIn('dieser Karte',scenario['question'])
                self.assertNotIn(scenario['correct'],scenario['wrong'])
                self.assertGreaterEqual(len(set(scenario['wrong'])),2)

    def test_runtime_versions_match_course_and_android_code_increases(self):
        course=json.loads((ROOT/'data/course.json').read_text('utf-8'))
        release=json.loads((ROOT/'release.json').read_text('utf-8'))
        android=json.loads((ROOT/'mobile/android-version.json').read_text('utf-8'))
        self.assertEqual(course['content_version'],release['version'])
        import ast
        tree=ast.parse((ROOT/'app.py').read_text('utf-8'))
        installed=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='VERSION' for t in n.targets))
        self.assertEqual(installed,release['version'])
        self.assertEqual(android['course'],release['version'])
        gradle=(ROOT/'mobile/app/build.gradle.kts').read_text('utf-8')
        self.assertIn(f'versionCode = {android["code"]}',gradle)
        self.assertIn(f'versionName = "{android["name"]}"',gradle)
        self.assertGreater(android['code'],11000103)

if __name__=='__main__':unittest.main()
