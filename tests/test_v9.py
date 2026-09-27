"""Animation checks against the real supplied art, not fabricated ASR scores."""
import sys,json,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import rigging
from rigging import CharacterRig,Pose,pose_at,blink_envelope,blink_schedule,locate_rig

class V9AnimationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rigs=json.loads((ROOT/'assets/animation/rigs.json').read_text())['rigs']
    def path(self,name='sakura'):
        return str(ROOT/('assets/mascot/kiko_idle.png' if name=='kiko_idle' else f'assets/teachers/{name}/full.png'))
    def rig(self,name='sakura',size=(256,390)):return CharacterRig(self.path(name),*size)
    def test_eight_teachers_and_one_mascot_have_individual_rigs(self):
        self.assertEqual(set(self.rigs),{'sakura','aiko','haruto','ren','miyako','emiri','satoshi','yuki','kiko_idle'})
        self.assertEqual(len({r['seed'] for r in self.rigs.values()}),9)
    def test_every_eye_frame_exists_matches_bbox_and_is_local(self):
        for name,config in self.rigs.items():
            blink=config.get('blink')
            if not blink:continue
            x0,y0,x1,y1=blink['bbox'];self.assertLess((x1-x0)*(y1-y0),np.prod(config['source_size'])*.13)
            for file in blink['frames']:
                with Image.open(ROOT/'assets/animation'/name/file) as im:
                    self.assertEqual(im.mode,'RGBA');self.assertEqual(im.size,(x1-x0,y1-y0))
    def test_closed_smile_ren_does_not_receive_fabricated_open_eyes(self):
        self.assertFalse(self.rig('ren').capabilities['blink'])
        self.assertTrue(self.rig('ren').capabilities['rig'])
    def test_blink_closes_holds_and_reopens(self):
        self.assertEqual(blink_envelope(-1),0);self.assertEqual(blink_envelope(.09),1)
        self.assertGreater(blink_envelope(.03),0);self.assertGreater(blink_envelope(.18),0)
        self.assertEqual(blink_envelope(.3),0)
    def test_blink_intervals_are_not_a_synchronized_sine_loop(self):
        a=blink_schedule(49);b=blink_schedule(66)
        self.assertNotEqual(a,b);self.assertGreater(len(set(np.round(np.diff(a),2))),5)
    def test_blink_changes_only_eye_area(self):
        rig=self.rig();a=np.asarray(rig.render(0,pose=Pose()));b=np.asarray(rig.render(0,pose=Pose(blink=1)))
        yy,xx=np.where(np.any(a!=b,axis=2));self.assertGreater(len(xx),0)
        x,y=rig.eye_pos;w,h=rig.eye_frames[0].size
        self.assertGreaterEqual(xx.min(),x-2);self.assertLessEqual(xx.max(),x+w+2)
        self.assertGreaterEqual(yy.min(),y-2);self.assertLessEqual(yy.max(),y+h+2)
    def test_teacher_lower_body_is_anchored_not_globally_zoomed(self):
        for name in self.rigs:
            if name=='kiko_idle':continue
            rig=self.rig(name);a=np.asarray(rig.render(0));b=np.asarray(rig.render(2))
            np.testing.assert_array_equal(a[-55:],b[-55:],err_msg=name)
            self.assertTrue(np.any(a!=b),name)
    def test_no_global_rotation_scale_or_translation_field(self):
        for config in self.rigs.values():
            for spec in config['fields']:
                self.assertIn('center',spec);self.assertIn('radii',spec)
                self.assertNotIn(spec['channel'],['scale','whole','bounce','zoom'])
    def test_kiko_paws_fixed_while_tail_moves(self):
        rig=self.rig('kiko_idle',(260,340));sx,sy=rig.scale;ox,oy=rig.offset
        box=(int(ox+145*sx),int(oy+402*sy),int(ox+295*sx),int(oy+434*sy))
        a=rig.render(0,pose=Pose(tail=1,ear_left=1));b=rig.render(0,pose=Pose(tail=-1,ear_right=-1))
        self.assertIsNone(ImageChops.difference(a.crop(box),b.crop(box)).getbbox())
        self.assertTrue(np.any(np.array(a)!=np.array(b)))
    def test_character_stays_inside_transparent_gutter(self):
        for name in self.rigs:
            rig=self.rig(name,(190,310))
            for t in [0,2.1,4.4,7.8]:
                x0,y0,x1,y1=rig.render(t,'praise').getchannel('A').getbbox()
                self.assertGreaterEqual(x0,1);self.assertGreaterEqual(y0,1)
                self.assertLess(x1,190);self.assertLess(y1,310)
    def test_reduced_motion_is_exactly_static(self):
        rig=self.rig();a=rig.render(0,enabled=False);b=rig.render(30,'praise',enabled=False)
        np.testing.assert_array_equal(np.asarray(a),np.asarray(b))
    def test_listening_and_praise_change_local_pose(self):
        self.assertNotEqual(pose_at(2,49,'idle'),pose_at(2,49,'listening'))
        self.assertNotEqual(pose_at(2,251,'idle'),pose_at(2,251,'praise'))
    def test_fallback_without_opencv(self):
        with patch.object(rigging,'cv2',None):
            rig=self.rig();im=rig.render(3)
            self.assertEqual(im.mode,'RGBA');self.assertEqual(im.size,(256,390))
    def test_original_source_files_are_not_modified_by_rendering(self):
        import hashlib
        path=Path(self.path());before=hashlib.sha256(path.read_bytes()).hexdigest()
        self.rig().render(2)
        self.assertEqual(before,hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':unittest.main(verbosity=2)
