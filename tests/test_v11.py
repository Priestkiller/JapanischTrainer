"""Curriculum and progress regression tests. No live audio/model claim."""
from __future__ import annotations
import json, os, re, sys, tempfile, unittest
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from learning import Learning
from storage import ProgressStore
from study import PracticeBook, StudySession, PHASES, matches_romaji
from lesson_ui import LessonMixin
from ui_renderer import Surface

class CourseV11Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.tmp.name});self.env.start()
        self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.book=PracticeBook(ROOT,self.learning)
        self.new=[l for l in self.learning.lessons if l.get('origin')=='v11']
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def flow(self,key='v11:long-vowels',index=0):return StudySession(self.learning.by_key[key],self.store,self.book,index)
    def test_exact_expansion(self):
        self.assertEqual(len(self.learning.lessons),150);self.assertEqual(len(self.learning.cards),680)
        self.assertEqual(len(self.new),100);self.assertEqual(sum(len(l['cards']) for l in self.new),502)
    def test_all_old_content_keys_order_and_speech_are_unchanged(self):
        old=json.loads((ROOT/'docs/LEGACY_COURSE_V101.json').read_text(encoding='utf8'))
        self.assertEqual(len(old['lessons']),50)
        for l in old['lessons']:
            now=self.learning.by_key[l['key']]
            for field in ('title','xp'):self.assertEqual(now[field],l[field],(l['key'],field))
            # Package 02 adds one explicitly accepted alternative-reading target;
            # every original speech target remains byte-for-byte equivalent.
            self.assertEqual(now['speech'][:len(l['speech'])],l['speech'],l['key'])
            self.assertEqual(len(now['cards']),len(l['cards']))
            for actual,prior in zip(now['cards'],l['cards']):
                # 11.0.2 adds explanations; every original card field and index stays intact.
                for field,value in prior.items():
                    if field in ('example_romaji','example_de') and l['key']=='14:0' and actual['jp'] in ['が','を','の']:
                        self.assertEqual(actual[field],actual['example'][field.removeprefix('example_')]);continue
                    if field=='example' and now.get('study_guide',{}).get('package')==2:
                        if l['key']=='14:0' and actual['jp'] in ['が','を','の']:continue
                        self.assertEqual(actual['example']['jp'],value);continue
                    self.assertEqual(actual[field],value,(l['key'],field))
    def test_learning_order_is_a_permutation(self):
        keys=[l['key'] for l in self.learning.lessons]
        self.assertEqual(len(keys),len(set(keys)))
        self.assertEqual(keys,self.learning.course['learning_order'])
    def test_early_basics_remain_first(self):
        self.assertEqual([l['key'] for l in self.learning.lessons[:2]],['0:0','0:1'])
        self.assertTrue(all(l['level']=='Einstieg' for l in self.learning.lessons[:8]))
    def test_eight_descriptive_sections_not_test_certificates(self):
        self.assertEqual(self.learning.stages,['Einstieg','Schrift','Erste Sätze','Zahlen & Zeit','Alltag','Aufbau','Praxis','Ausblick'])
        self.assertIn('kein vollständiger',self.learning.course['scope_note'])
    def test_all_new_lessons_have_teaching_goal_and_intro(self):
        for l in self.new:
            self.assertGreater(len(l['goal']),20,l['key']);self.assertGreater(len(l['intro']),100,l['key'])
            self.assertEqual(self.book.intro(l),l['intro'])
    def test_every_new_card_has_complete_explanation(self):
        for l in self.new:
            for c in l['cards']:
                p=self.book.profile(c,l)
                for field in ('usage','explain','register','pitfall','parts','extra','scenario'):self.assertTrue(p.get(field),(l['key'],c['jp'],field))
                self.assertGreater(len(p['explain']),80)
    def test_same_word_in_new_context_uses_card_profile(self):
        l=self.learning.by_key['v11:kana-s'];c=next(c for c in l['cards'] if c['jp']=='すし')
        self.assertEqual(self.book.profile(c,l),c['detail'])
        self.assertIn('Su-shi',self.book.profile(c,l)['explain'])
    def test_card_specific_example_overrides_legacy_dictionary(self):
        l=self.learning.by_key['v11:languages'];c=l['cards'][-1]
        self.assertEqual(self.learning.examples(c),c['example'])
        for key in ('jp','romaji','de'):self.assertTrue(self.learning.examples(c)[key])
    def test_new_speech_targets_count_and_link(self):
        self.assertEqual(sum(len(l.get('speech',[])) for l in self.learning.lessons),565)
        for l in self.new:
            self.assertEqual(len(l['speech']),len(l['cards']))
            for c in l['cards']:
                target=self.learning.speech_target(c,l)
                self.assertEqual(target['romaji'],c['romaji']);self.assertIn(target['target'],target['accept'])
    def test_phonetic_help_is_not_missing_j_or_long_vowels(self):
        cards={c['jp']:c for l in self.new for c in l['cards']}
        self.assertTrue(cards['じえいぎょう']['approx'].startswith('dschi'))
        self.assertEqual(cards['きゅう']['approx'],'kjuu')
        self.assertEqual(cards['おじいさん']['approx'],'o-dschii-sa-n')
    def test_pronunciation_note_is_qualified(self):
        self.assertIn('Annäherung',self.learning.course['pronunciation_note'])
        self.assertIn('Hören',self.learning.course['pronunciation_note'])
    def test_new_material_not_100_copies(self):
        cards=[c for l in self.new for c in l['cards']]
        self.assertGreaterEqual(len({c['jp'] for c in cards}),490)
        self.assertEqual(len({l['title'] for l in self.new}),100)
        self.assertEqual(len({c['detail']['explain'] for c in cards}),502)
    def test_all_scenarios_have_unambiguous_distinct_options(self):
        for l in self.new:
            for c in l['cards']:
                q=c['detail']['scenario'];self.assertNotIn(q['correct'],q['wrong'])
                self.assertGreaterEqual(len(set(q['wrong'])),2)
    def test_roman_build_fallback_does_not_use_future_targets(self):
        for l in self.new:
            for i in range(len(l['cards'])):
                f=StudySession(l,self.store,self.book,i);f.phase='build'
                if not self.book.blocks(f.card,l)[0]:
                    self.assertTrue(set(f.answers()[0]) <= {c['romaji'] for c in l['cards'][:i+1]})
    def test_meaning_choices_are_native_language_same_topic(self):
        for l in self.new:
            f=StudySession(l,self.store,self.book);f.phase='meaning'
            self.assertTrue(set(f.answers()[0]) <= {c['de'] for c in l['cards']})
            self.assertGreaterEqual(len(f.answers()[0]),3)
    def test_every_card_starts_by_teaching_not_testing(self):
        for l in self.new:
            f=StudySession(l,self.store,self.book);self.assertEqual(f.phase,'understand')
            self.assertEqual(f.advance(),'blocked')
    def test_listening_never_picks_future_japanese(self):
        for l in self.new:
            for i in range(len(l['cards'])):
                f=StudySession(l,self.store,self.book,i);f.phase='listen';f.reset_task()
                self.assertLessEqual(f.listen_index,i)
                self.assertTrue(set(f.answers()[0]) <= {c['de'] for c in l['cards'][:i+1]})
    def test_only_explicit_equivalent_readings_are_accepted(self):
        f=self.flow('v11:clock-minutes',2);self.assertEqual(f.card['jp'],'じゅっぷん')
        f.phase='write';f.check_write('jippun');self.assertTrue(f.success)
        g=self.flow('v11:long-vowels',1);g.phase='write';g.check_write('obasan');self.assertFalse(g.success)
    def test_search_german(self):self.assertTrue(any(l['key']=='v11:jobs' for l in self.learning.filtered_lessons('selbstständig')))
    def test_search_japanese(self):self.assertTrue(any(l['key']=='v11:long-vowels' for l in self.learning.filtered_lessons('おばあさん')))
    def test_search_romaji(self):self.assertTrue(any(l['key']=='v11:jobs' for l in self.learning.filtered_lessons('jieigyō')))
    def test_stage_filter_and_new_only(self):
        rows=self.learning.filtered_lessons(stage='Praxis',new_only=True)
        self.assertEqual(len(rows),15);self.assertTrue(all(l['level']=='Praxis' for l in rows))
        self.assertEqual(len(self.learning.filtered_lessons(new_only=True)),100)
    def test_zero_search_results_is_valid(self):self.assertEqual(self.learning.filtered_lessons('zzzzzz-not-a-lesson'),[])
    def test_first_lesson_available_new_ones_not_premarked_complete(self):
        self.assertTrue(self.learning.unlocked('0:0'));self.assertFalse(self.learning.unlocked('v11:long-vowels'))
        self.assertEqual(self.store.data['completed'],[])
    def test_stable_card_key_despite_new_display_position(self):
        c=next(c for c in self.learning.cards if c['lesson_key']=='1:0' and c['card_index']==1)
        self.assertEqual(c['key'],'1:0:1');self.assertEqual(c['jp'],'ありがとう')
    def test_migration_keeps_old_progress_and_cursor_and_preferences(self):
        old={'completed':['0:0','0:1','1:0'],'xp':175,'teacher_id':'haruto',
             'last_lesson':{'key':'1:1','card':1},'motion_enabled':True,'motion_preset':'lively',
             'tts_speed':.9,'lesson_sessions':{'1:1':{'index':1,'phase':'write','mode':'learn'}},
             'study_cards':{'1:1:1':{'mistakes':2}},'review':{'1:1:1':{'box':0,'due':0}},
             'speech_scores':{'ありがとう':{'best':85}},'custom_extension':'keep'}
        self.store.path.write_text(json.dumps(old),encoding='utf8');store=ProgressStore();model=Learning(ROOT,store)
        for k,v in old.items():self.assertEqual(store.data[k],v,k)
        backup=store.path.with_name('progress.before-course-v11.json');self.assertTrue(backup.exists())
        self.assertEqual(json.loads(backup.read_text()),old)
        self.assertTrue(model.unlocked('1:1'));self.assertEqual(model.next_lesson()['key'],'1:1')
        f=StudySession(model.by_key['1:1'],store,PracticeBook(ROOT,model),restore=True)
        self.assertEqual((f.index,f.phase),(1,'write'))
    def test_migration_does_not_overwrite_first_backup(self):
        self.store.data.pop('course_revision',None);self.store.data['xp']=123;self.store.save()
        Learning(ROOT,self.store);backup=self.store.path.with_name('progress.before-course-v11.json');first=backup.read_bytes()
        self.store.data['xp']=999;self.store.save();Learning(ROOT,self.store)
        self.assertEqual(backup.read_bytes(),first)
    def test_inserted_basics_do_not_relock_advanced_existing_completion(self):
        self.store.data['completed']=['25:0'];self.assertTrue(self.learning.unlocked('v11:long-vowels'))
        self.assertTrue(self.learning.unlocked('25:0'));self.assertFalse(self.learning.unlocked('43:0'))
    def test_unlocked_is_not_the_same_as_studied_vocabulary(self):
        self.store.data['completed']=['25:0']
        self.assertNotIn('おばあさん',[c['jp'] for c in self.learning.available_cards()])
        self.assertEqual(self.learning.available_cards(all_=True),self.learning.cards)
    def test_new_long_sentences_fit_without_hidden_pronunciation(self):
        ui=LessonMixin();surface=Surface(1440,1040,1)
        for width in (616,660,682):
            for c in self.learning.cards:
                layout=ui.pinned_text_layout(surface,width,c)
                self.assertLess(layout['white_h']+108,365,(c['jp'],width,layout))
                self.assertGreaterEqual(layout['romaji'][0],15)
                self.assertGreaterEqual(layout['approx'][0],12)
    def test_invalid_lesson_key_cannot_be_opened(self):self.assertFalse(self.learning.unlocked('not-a-lesson'))
    def test_source_reference_and_scope_are_packaged(self):
        self.assertGreaterEqual(len(self.learning.course['references']),4)
        self.assertIn('eigenständig',self.learning.course['authorship_note'])
    def test_each_new_lesson_recap_includes_every_card(self):
        # Memory-only saves: this tests session logic, not persistence (tested above).
        self.store.save=lambda:None
        for l in self.new:
            f=StudySession(l,self.store,self.book)
            while f.mode!='recap':f.mark(True,'unit-test');self.assertEqual(f.advance(),'next')
            self.assertEqual(set(f.recap),set(range(len(l['cards']))))

if __name__=='__main__':unittest.main(verbosity=2)
