"""V10 local animation and reaction state tests. No Windows/audio inference."""
import sys, json, hashlib, unittest, tempfile, os
from pathlib import Path
from unittest.mock import patch
from dataclasses import replace
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rigging import CharacterRig, Pose, expression_document
from reactions import ReactionController, ReactionSample, PROFILES, reaction_envelope, nod_envelope
from lesson_ui import LessonMixin
from storage import ProgressStore
from learning import Learning
from study import StudySession, PracticeBook

class ReactionTests(unittest.TestCase):
    def setUp(self):
        self.now=100.;self.c=ReactionController(lambda:self.now)
    def test_all_eight_teacher_profiles_are_present(self):
        self.assertEqual(set(PROFILES),{'sakura','aiko','haruto','ren','miyako','emiri','satoshi','yuki'})
    def test_one_shot_event_has_smooth_entrance_and_exact_expiry(self):
        self.c.trigger('praise','sakura');self.assertEqual(self.c.sample('sakura').amount,0)
        self.now+=.18;self.assertEqual(self.c.sample('sakura').amount,1)
        self.now+=2.3;self.assertGreater(self.c.sample('sakura').amount,0)
        self.now+=.3;self.assertEqual(self.c.sample('sakura').mood,'idle')
    def test_closed_idle_and_no_reaction_without_evidence(self):
        for name in PROFILES:self.assertEqual(self.c.sample(name).mood,'idle')
    def test_no_reaction_bleeds_into_another_teacher(self):
        self.c.trigger('praise','aiko');self.now+=.5
        self.assertEqual(self.c.sample('aiko').mood,'praise');self.assertEqual(self.c.sample('sakura').mood,'idle')
    def test_new_outcome_supersedes_previous_one(self):
        self.c.trigger('praise','ren');first=self.c.sequence;self.c.trigger('encourage','ren')
        self.assertEqual(self.c.sequence,first+1);self.assertEqual(self.c.sample('ren').mood,'encourage')
    def test_recording_takes_precedence(self):
        self.c.trigger('praise','sakura');self.now+=.3
        self.assertEqual(self.c.sample('sakura',recording=True).mood,'listening')
        self.assertEqual(self.c.sample('sakura',recording=True).amount,0)
    def test_playback_does_not_become_a_fake_talking_mouth(self):
        for job in ('Vorlesen','Hörbeispiel'):
            a=self.c.sample('sakura',job=job);self.assertEqual(a.mood,'speaking');self.assertEqual(a.amount,0)
    def test_asr_pending_is_thinking_not_success(self):
        self.assertEqual(self.c.sample('ren',job='Spracherkennung').mood,'thinking')
    def test_no_fake_pronunciation_claim_in_speech_praise(self):
        self.c.trigger('praise','emiri','speech-match');m=self.c.sample('emiri').message
        self.assertIn('erkannt',m);self.assertNotIn('perfekt',m.lower());self.assertNotIn('Akzent',m)
    def test_uncertain_recording_is_not_learner_failure(self):
        self.c.trigger('encourage','miyako','speech-uncertain')
        self.assertIn('keine falsche Antwort',self.c.sample('miyako').message)
    def test_unknown_ids_or_moods_are_rejected(self):
        self.assertFalse(self.c.trigger('praise','nobody'));self.assertFalse(self.c.trigger('angry','sakura'))
        self.assertEqual(self.c.sequence,0)
    def test_clear_removes_mood_and_dialog(self):
        self.c.trigger('praise','yuki');self.c.clear();self.assertEqual(self.c.sample('yuki').message,'')
    def test_nod_is_bounded_and_nonperiodic(self):
        a=[nod_envelope(t) for t in np.linspace(0,5,200)]
        self.assertLessEqual(max(a),1);self.assertGreaterEqual(min(a),-.16);self.assertEqual(nod_envelope(3),0)
    def test_envelope_is_bounded_at_all_times(self):
        for t in np.linspace(-2,10,1000):self.assertTrue(0<=reaction_envelope(t)<=1)

class FaceTests(unittest.TestCase):
    def path(self,n):return str(ROOT/('assets/mascot/kiko_idle.png' if n=='kiko_idle' else f'assets/teachers/{n}/full.png'))
    def rig(self,n='sakura'):return CharacterRig(self.path(n),260,390)
    def test_all_nine_have_authored_expression_assets(self):
        data=expression_document(str(ROOT/'assets/animation'))
        self.assertEqual(set(data),set(PROFILES)|{'kiko_idle'})
        for n in data:self.assertTrue(data[n]['closed_idle'])
    def test_local_patch_files_and_bbox_are_valid(self):
        for n,c in expression_document(str(ROOT/'assets/animation')).items():
            for k in ('idle','praise','encourage','cheeks','praise_face'):
                if k not in c:continue
                spec=c[k];x0,y0,x1,y1=spec['bbox']
                with Image.open(ROOT/'assets/animation'/n/spec['file']) as im:
                    self.assertEqual(im.mode,'RGBA');self.assertEqual(im.size,(x1-x0,y1-y0))
                    self.assertGreaterEqual(x0,0);self.assertGreaterEqual(y0,0)
    def test_all_teacher_neutral_bases_report_closed_mouth(self):
        for n in PROFILES:
            r=self.rig(n);self.assertTrue(r.capabilities['closed_idle'])
            self.assertIn('idle',r.capabilities['expressions']);self.assertIn('praise',r.capabilities['expressions'])
    def test_all_teachers_have_visibly_different_correct_expression(self):
        for n in PROFILES:
            r=self.rig(n);a=np.asarray(r.render(0,enabled=False));b=np.asarray(r.render(0,'praise',enabled=False,reaction_strength=1))
            self.assertGreater(np.count_nonzero(a!=b),20,n)
    def test_all_teachers_keep_closed_mouth_during_listening_thinking_and_playback(self):
        for n in PROFILES:
            r=self.rig(n);idle=np.asarray(r.render(0,enabled=False))
            for m in ('idle','listening','thinking','speaking'):
                np.testing.assert_array_equal(idle,np.asarray(r.render(0,m,enabled=False,reaction_strength=0)))
    def test_reaction_does_not_change_lower_body_or_sprite_alpha(self):
        for n in PROFILES:
            r=self.rig(n);a=np.asarray(r.render(0,enabled=False));b=np.asarray(r.render(0,'praise',enabled=False,reaction_strength=1))
            np.testing.assert_array_equal(a[170:],b[170:],err_msg=n)
            np.testing.assert_array_equal(a[:,:,3],b[:,:,3],err_msg=n)
    def test_fractional_expression_reverts_exactly_to_neutral(self):
        for n in PROFILES:
            r=self.rig(n);a=r.render(0,enabled=False)
            r.render(0,'praise',enabled=False,reaction_strength=.5)
            np.testing.assert_array_equal(np.asarray(a),np.asarray(r.render(0,'idle',enabled=False,reaction_strength=0)))
    def test_disabled_motion_allows_static_feedback_without_wobble(self):
        r=self.rig();a=r.render(0,'praise',enabled=False,reaction_strength=1);b=r.render(50,'praise',enabled=False,reaction_strength=1)
        np.testing.assert_array_equal(np.asarray(a),np.asarray(b))
    def test_kiko_cheers_with_same_seated_body(self):
        r=self.rig('kiko_idle');a=np.asarray(r.render(0,enabled=False));b=np.asarray(r.render(0,'praise',enabled=False,reaction_strength=1))
        self.assertTrue(np.any(a!=b));cut=round(r.offset[1]+300*r.scale[1]);np.testing.assert_array_equal(a[cut:],b[cut:])
    def test_original_full_art_is_not_modified_by_renderer(self):
        for n in PROFILES:
            p=Path(self.path(n));before=hashlib.sha256(p.read_bytes()).hexdigest()
            self.rig(n).render(1,'praise',reaction_strength=1,reaction_age=.5)
            self.assertEqual(before,hashlib.sha256(p.read_bytes()).hexdigest())
    def test_praise_renderer_is_bounded_for_all_teachers_and_fox(self):
        for n in list(PROFILES)+['kiko_idle']:
            r=self.rig(n)
            for age in (0,.18,.65,1.4,2.4):
                im=r.render(0,'praise',reaction_strength=reaction_envelope(age),reaction_age=age,pose=Pose(nod=1))
                self.assertEqual(im.size,(260,390));self.assertEqual(im.mode,'RGBA')
    def test_static_cards_and_avatars_are_real_individual_pngs(self):
        for n in PROFILES:
            for k,size in [('card',(480,672)),('avatar',(320,320))]:
                with Image.open(ROOT/f'assets/teachers/{n}/{k}.png') as im:self.assertEqual(im.size,size)

class MinimalApp(LessonMixin):
    def request_draw(self):pass
    def teacher(self):return self.learning.teacher()
    def __init__(self,store):
        self.store=store;self.learning=Learning(ROOT,store);self.book=PracticeBook(ROOT,self.learning)
        self.lesson=self.learning.by_key['1:0'];self.flow=StudySession(self.lesson,store,self.book,1)
        self.flow.phase='meaning';self.flow.reset_task();self.recording=False;self.job='';self.reactions=ReactionController()
        self.reaction='idle';self.reaction_until=0

class StepDispatchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':self.temp.name});self.env.start()
        self.app=MinimalApp(ProgressStore())
    def tearDown(self):self.env.stop();self.temp.cleanup()
    def test_correct_answer_triggers_praise_for_every_teacher(self):
        for n in PROFILES:
            a=self.app;a.store.data['teacher_id']=n;a.flow.reset_task();a.clear_reaction();_,c=a.flow.answers();a.check_answer(c)
            self.assertEqual(a.actor_feedback().mood,'praise');self.assertEqual(a.actor_feedback().teacher_id,n)
    def test_mistake_is_encouraging_for_every_teacher(self):
        for n in PROFILES:
            a=self.app;a.store.data['teacher_id']=n;a.flow.reset_task();o,c=a.flow.answers();a.check_answer(next(v for v in o if v!=c))
            self.assertEqual(a.actor_feedback().mood,'encourage')
    def test_same_solved_answer_does_not_restart_reaction(self):
        a=self.app;_,c=a.flow.answers();a.check_answer(c);seq=a.reactions.sequence;a.check_answer(c)
        self.assertEqual(seq,a.reactions.sequence)
    def test_unknown_answer_and_unheard_audio_do_not_trigger_reaction(self):
        a=self.app;a.check_answer('not an option');self.assertEqual(a.actor_mood(),'idle')
        a.flow.phase='listen';a.flow.reset_task();_,c=a.flow.answers();a.check_answer(c);self.assertEqual(a.actor_mood(),'idle')
    def test_skipped_hearing_does_not_celebrate(self):
        a=self.app;a.flow.phase='listen';a.flow.reset_task();a.flow.audio_skipped=True;_,c=a.flow.answers();a.check_answer(c)
        self.assertTrue(a.flow.success);self.assertEqual(a.actor_mood(),'idle')
    def test_build_task_triggers_joy_only_after_correct_build(self):
        a=self.app;a.flow.phase='build';a.flow.reset_task();a.check_blocks();self.assertEqual(a.actor_mood(),'encourage')
        parts,_=a.book.blocks(a.flow.card,a.lesson);a.flow.tokens=list(range(len(parts)));a.check_blocks();self.assertEqual(a.actor_mood(),'praise')
    def test_praise_does_not_itself_award_xp(self):
        a=self.app;before=a.store.data.copy();a.react('praise');self.assertEqual(a.store.data,before)

if __name__=='__main__':unittest.main(verbosity=2)
