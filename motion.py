"""Independent, bounded idle clock and user-controlled motion presets.

Expression/reaction timers deliberately do not own this clock. Restoring a
window or finishing a success reaction cannot restart the breathing cycle.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

PRESETS = {
    'subtle': ('Dezent', .60),
    'natural': ('Natürlich', 1.00),
    'lively': ('Lebendig', 1.40),
}

def preset_name(value: object) -> str:
    return value if isinstance(value, str) and value in PRESETS else 'natural'

def preset_strength(value: object) -> float:
    return PRESETS[preset_name(value)][1]

@dataclass
class MotionClock:
    """Animation time advances only while visible and enabled.

    A late GUI frame never causes a large jump through an animation. Audio and
    recognition still use their own real-time clocks; only visual time is capped.
    """
    time: float = 0.0
    last: float | None = None
    active: bool = False
    max_step: float = .10

    def step(self, now: float, active: bool) -> float:
        now = float(now)
        if not math.isfinite(now):
            return self.time
        if self.last is not None and active and self.active:
            self.time += min(self.max_step, max(0.0, now - self.last))
        self.last, self.active = now, bool(active)
        return self.time
