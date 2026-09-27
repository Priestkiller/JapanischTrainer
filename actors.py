"""V10.1 continuous idle layer with short additive reactions.

Actor-only canvases update. Lessons, text, caret and speech controls are untouched.
Idle time is independent from expression time, redraws and lesson transitions.
"""
from __future__ import annotations
from dataclasses import dataclass, fields, replace
from functools import lru_cache
import logging
import math
import time
from PIL import ImageTk
from rigging import CharacterRig, Pose, blink_envelope
from reactions import ReactionSample, PROFILES, nod_envelope
from motion import MotionClock


@dataclass(frozen=True)
class ActorSpec:
    id: str
    path: str
    box: tuple[int, int, int, int]
    role: str = 'teacher'
    mood: str = 'idle'


@lru_cache(maxsize=3)
def _prepared(path, w, h):
    return CharacterRig(path, w, h)


def sprite(path, w, h, phase, role='teacher', mood='idle'):
    """Compatibility hook; the live animator uses continuous independent time."""
    return _prepared(path, max(10, w), max(10, h)).render(
        max(0, phase) / 72 * 6.4, mood, enabled=phase >= 0)


sprite.cache_clear = _prepared.cache_clear


def reaction_pose(base: Pose, sample: ReactionSample, identity: str) -> Pose:
    """Overlay a one-shot gesture; never replace/reset the underlying idle."""
    amount = min(1., max(0., sample.amount))
    if sample.mood not in ('praise', 'encourage') or amount <= 0:
        return base
    joyful = sample.mood == 'praise'
    profile = PROFILES.get(identity, {'joy': 1.2, 'nod': .85})
    power = profile['nod'] * (1. if joyful else .3)
    # Extra tail energy is event-relative. Changing mood never changes the
    # frequency/phase of the baseline tail channel as it did in the older path.
    tail_extra = .33 * amount * math.sin(sample.age * math.tau / .95) if joyful else 0.
    return replace(base,
        nod=base.nod + nod_envelope(sample.age) * power,
        head=base.head + amount * (.22 if joyful else .13),
        tail=base.tail + tail_extra,
        ear_left=base.ear_left + (.24 * amount if joyful else 0.),
        ear_right=base.ear_right + (.19 * amount if joyful else 0.),
        blink=max(base.blink, blink_envelope(sample.age - .42)))


class ActorLayer:
    TARGET_FPS = 30

    def __init__(self, root, canvas, enabled, mood_provider=None,
                 reaction_provider=None, strength_provider=None):
        self.root, self.canvas, self.is_enabled = root, canvas, enabled
        self.mood_provider, self.reaction_provider = mood_provider, reaction_provider
        self.strength_provider = strength_provider
        self.specs, self.items, self.photos, self.images, self.rigs = {}, {}, {}, {}, {}
        self.keys, self.poses, self.pose_times, self.last_phases = {}, {}, {}, {}
        self.started = time.monotonic()  # Diagnostic only; no reaction resets this.
        self.clock = MotionClock()
        self.closed, self.frame_count, self.render_errors = False, 0, []
        self.render_ms = []
        self.timer = root.after(33, self.tick)

    def phase(self, spec):
        return self.clock.time if self.is_enabled() else -1

    def sync(self, specs):
        new = {s.id: s for s in specs}
        for key in list(self.items):
            if key not in new:
                self.canvas.delete(self.items.pop(key))
                for table in (self.photos, self.images, self.rigs, self.keys,
                              self.poses, self.pose_times, self.last_phases):
                    table.pop(key, None)
        for key, spec in new.items():
            signature = (spec.path, spec.box[2], spec.box[3])
            if self.keys.get(key) != signature:
                self.rigs[key] = CharacterRig(*signature)
                self.keys[key] = signature
                self.poses.pop(key, None)
                self.pose_times.pop(key, None)
                self.last_phases.pop(key, None)
            if key not in self.items:
                self.items[key] = self.canvas.create_image(
                    spec.box[0], spec.box[1], anchor='nw', tags=('actor',))
            self.canvas.coords(self.items[key], spec.box[0], spec.box[1])
        self.specs = new
        self.paint(force=True)

    def _pose(self, key, target, visual_time):
        old = self.poses.get(key, target)
        dt = max(0., min(.15, visual_time - self.pose_times.get(key, visual_time)))
        # Smooth attitude/strength changes; the breathing clock keeps running.
        k = 1 - math.exp(-dt / .15) if dt else (1. if key not in self.poses else 0.)
        result = Pose(**{
            f.name: getattr(target, f.name) if f.name == 'blink' else
            getattr(old, f.name) + (getattr(target, f.name) - getattr(old, f.name)) * k
            for f in fields(Pose)})
        self.poses[key], self.pose_times[key] = result, visual_time
        return result

    def paint(self, force=False):
        now = time.monotonic()
        enabled = bool(self.is_enabled())
        visible = self.root.state() != 'iconic' and self.root.winfo_viewable()
        visual_time = self.clock.step(now, enabled and bool(visible) and bool(self.specs))
        frame_no = int(visual_time * self.TARGET_FPS) if enabled else -1
        sample = self.reaction_provider() if self.reaction_provider else ReactionSample()
        strength = float(self.strength_provider()) if self.strength_provider else 1.
        strength = min(1.5, max(0., strength)) if math.isfinite(strength) else 1.
        for key, spec in self.specs.items():
            mood = sample.mood if self.reaction_provider else (
                self.mood_provider() if self.mood_provider else spec.mood)
            amount = sample.amount if enabled else float(mood in ('praise', 'encourage'))
            phase_key = (frame_no, mood, sample.sequence, round(strength, 3))
            if not force and self.last_phases.get(key) == phase_key:
                continue
            rig = self.rigs[key]
            start = time.perf_counter()
            try:
                base = rig.idle_pose(visual_time, mood, strength)
                target = reaction_pose(base, sample, rig.identity)
                pose = self._pose(key, target, visual_time)
                image = rig.render(visual_time, mood, enabled=enabled, pose=pose,
                                   reaction_strength=amount, reaction_age=sample.age)
            except Exception as exc:
                logging.exception('Actor render failed: %s', spec.path)
                self.render_errors.append(str(exc))
                self.render_errors = self.render_errors[-10:]
                image = rig.base.copy()
            photo = ImageTk.PhotoImage(image, master=self.root)
            self.canvas.itemconfigure(self.items[key], image=photo)
            self.photos[key], self.images[key] = photo, image
            self.last_phases[key] = phase_key
            self.frame_count += 1
            self.canvas.tag_raise(self.items[key])
            self.render_ms.append((time.perf_counter() - start) * 1000)
            self.render_ms = self.render_ms[-180:]

    def tick(self):
        if self.closed:
            return
        begin = time.monotonic()
        try:
            visible = self.root.state() != 'iconic' and self.root.winfo_viewable()
            if visible:
                self.paint()
            else:
                self.clock.step(begin, False)
            period = 1 / self.TARGET_FPS if self.is_enabled() and visible and self.specs else .3
            self.timer = self.root.after(
                max(16, round((period - (time.monotonic() - begin)) * 1000)), self.tick)
        except Exception:
            logging.exception('Animation scheduling error')
            if not self.closed:
                self.timer = self.root.after(300, self.tick)

    def composite(self, base):
        image = base.copy()
        for key, spec in self.specs.items():
            if key in self.images:
                image.alpha_composite(self.images[key], spec.box[:2])
        return image

    def close(self):
        self.closed = True
        try:
            self.root.after_cancel(self.timer)
        except Exception:
            pass
        for table in (self.photos, self.images, self.rigs, self.poses):
            table.clear()
        _prepared.cache_clear()
