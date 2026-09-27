"""Idle regression checks: ongoing baseline plus closed-mouth feedback, all actors."""
from __future__ import annotations
import json
import os
import tempfile
import unittest
from dataclasses import fields
from pathlib import Path
from unittest.mock import patch
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from actors import reaction_pose
from motion import MotionClock, PRESETS, preset_name, preset_strength
from rigging import CharacterRig, Pose
from reactions import ReactionSample, PROFILES, reaction_envelope
from storage import ProgressStore

NAMES=tuple(PROFILES)+('kiko_idle',)
def make_rig(name, size=(390,630)):
    rel='assets/mascot/kiko_idle.png' if name=='kiko_idle' else f'assets/teachers/{name}/full.png'
    return CharacterRig(str(ROOT/rel),*size)

class ClockTests(unittest.TestCase):
    def test_clock_advances_without_reactions(self):
        c=MotionClock();c.step(1,True);c.step(1.04,True)
        self.assertAlmostEqual(c.time,.04)
    def test_hidden_window_does_not_accumulate_a_jump(self):
        c=MotionClock();c.step(1,True);c.step(1.04,True);c.step(2,False)
        c.step(102,False);old=c.time;c.step(102.01,True)
        self.assertEqual(c.time,old);c.step(102.05,True);self.assertAlmostEqual(c.time,old+.04)
    def test_motion_off_does_not_accumulate_time(self):
        c=MotionClock();c.step(1,False);c.step(60,False);self.assertEqual(c.time,0)
    def test_long_render_cannot_skip_a_large_pose_change(self):
        c=MotionClock();c.step(1,True);c.step(12,True);self.assertAlmostEqual(c.time,.1)
    def test_clock_rejects_nonfinite_and_negative_deltas(self):
        c=MotionClock();c.step(1,True);c.step(1.03,True);old=c.time
        c.step(float('nan'),True);self.assertEqual(c.time,old)
        c.step(.8,True);self.assertEqual(c.time,old)

class IdleCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rigs={name:make_rig(name) for name in NAMES}
    def test_idle_never_changes_its_phase_or_frequency_during_feedback(self):
        for name,r in self.rigs.items():
            for t in (0,2.1,7.4,17.6):
                base=r.idle_pose(t)
                self.assertEqual(base,r.idle_pose(t,'praise'),name)
                self.assertEqual(base,r.idle_pose(t,'encourage'),name)
    def test_praise_keeps_breath_hair_cloth_and_posture_channels(self):
        for name,r in self.rigs.items():
            base=r.idle_pose(6.12)
            after=reaction_pose(base,ReactionSample('praise',.6,1.),name)
            for channel in ('breath','head_lift','hair_left','hair_right','cloth','pendant','posture'):
                self.assertEqual(getattr(after,channel),getattr(base,channel),(name,channel))
            self.assertGreater(after.nod,base.nod,name)
    def test_expired_reaction_is_exactly_the_same_running_idle(self):
        for name,r in self.rigs.items():
            base=r.idle_pose(8.5)
            self.assertEqual(base,reaction_pose(base,ReactionSample('idle'),name))
            self.assertEqual(base,reaction_pose(base,ReactionSample('praise',2.65,0.),name))
    def test_every_teacher_has_an_individually_tuned_idle(self):
        profiles=[json.dumps(r.config['idle_profile'],sort_keys=True) for r in self.rigs.values()]
        self.assertEqual(len(set(profiles)),len(NAMES))
    def test_heads_move_visibly_at_actual_ui_size_without_blinking(self):
        for name in PROFILES:
            r=self.rigs[name];field=next(f for f in r.config['fields'] if f['channel']=='head')
            x,y=field['center'];sx,sy=r.scale;ox,oy=r.offset
            distance=((r.grid[:,:,0]-(x*sx+ox))**2+(r.grid[:,:,1]-(y*sy+oy))**2)
            row,col=np.unravel_index(distance.argmin(),distance.shape)
            samples=np.stack([r.displacement(r.idle_pose(float(t)))[row,col] for t in np.linspace(0,12,70)])
            peak_to_peak=float(np.linalg.norm(np.ptp(samples,axis=0)))
            self.assertGreater(peak_to_peak,1.1,(name,peak_to_peak))
            self.assertLess(peak_to_peak,14.,(name,peak_to_peak))
    def test_reduced_motion_keeps_all_characters_still_and_mouths_closed(self):
        for name,r in self.rigs.items():
            self.assertTrue(r.capabilities['closed_idle'],name)
            a=r.render(0,enabled=False);b=r.render(80,enabled=False)
            np.testing.assert_array_equal(np.asarray(a),np.asarray(b),err_msg=name)
    def test_preset_changes_motion_but_never_blink_or_expression_strength(self):
        for name,r in self.rigs.items():
            weak=r.idle_pose(4,strength=.6);strong=r.idle_pose(4,strength=1.4)
            self.assertEqual(weak.blink,strong.blink,name)
            self.assertGreater(abs(strong.breath),abs(weak.breath),name)
            sample=ReactionSample('praise',.5,1.)
            self.assertAlmostEqual(reaction_pose(weak,sample,name).nod,
                                   reaction_pose(strong,sample,name).nod,msg=name)
    def test_lively_mode_stays_inside_sprite_and_anchors_lower_body(self):
        for name in PROFILES:
            r=self.rigs[name];a=r.render(1,strength=1.4);b=r.render(4.4,strength=1.4)
            np.testing.assert_array_equal(np.asarray(a)[-80:],np.asarray(b)[-80:],err_msg=name)
            for im in (a,b):
                x0,y0,x1,y1=im.getchannel('A').getbbox()
                self.assertGreaterEqual(x0,1);self.assertGreaterEqual(y0,1)
                self.assertLess(x1,im.width);self.assertLess(y1,im.height)
    def test_motion_mesh_does_not_fold_on_itself(self):
        for name,r in self.rigs.items():
            gx=r.grid[0,:,0];gy=r.grid[:,0,1]
            for t in (0.,2.15,4.6,7.3):
                sample=ReactionSample('praise',.55,reaction_envelope(.55))
                delta=r.displacement(reaction_pose(r.idle_pose(t,strength=1.4),sample,name))
                dxdy,dxdx=np.gradient(delta[:,:,0],gy,gx)
                dydy,dydx=np.gradient(delta[:,:,1],gy,gx)
                jac=(1+dxdx)*(1+dydy)-dxdy*dydx
                self.assertGreater(jac.min(),.50,(name,float(jac.min())))
    def test_source_expression_patches_are_unchanged_across_idle_states(self):
        for name,r in self.rigs.items():
            expected=np.asarray(r._face('idle',0))
            for mood in ('idle','listening','thinking','speaking'):
                np.testing.assert_array_equal(expected,np.asarray(r._face(mood,0)),err_msg=name)

class PreferenceTests(unittest.TestCase):
    def test_three_explicit_presets_and_natural_default(self):
        self.assertEqual(set(PRESETS),{'subtle','natural','lively'})
        self.assertEqual(preset_name(None),'natural')
        self.assertEqual(preset_strength('natural'),1.)
        self.assertLess(preset_strength('subtle'),preset_strength('natural'))
        self.assertGreater(preset_strength('lively'),preset_strength('natural'))
    def test_unknown_or_unhashable_preference_is_safe(self):
        for v in (None,[],{},float('nan'),4,'missing'):
            self.assertEqual(preset_name(v),'natural')
    def test_old_progress_and_explicit_motion_off_are_preserved(self):
        with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':td}):
            old={'completed':['0:0'],'xp':75,'teacher_id':'aiko','motion_enabled':False}
            (Path(td)/'progress.json').write_text(json.dumps(old),encoding='utf8')
            store=ProgressStore()
            for k,v in old.items():self.assertEqual(store.data[k],v)
            self.assertEqual(store.data['motion_preset'],'natural')
    def test_new_preference_is_persisted(self):
        with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':td}):
            s=ProgressStore();s.data['motion_preset']='lively';s.save()
            self.assertEqual(ProgressStore().data['motion_preset'],'lively')

if __name__=='__main__':unittest.main(verbosity=2)
