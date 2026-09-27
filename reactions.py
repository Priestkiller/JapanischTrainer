"""Short, evidence-driven character reactions. No scores, rewards or audio invented."""
from __future__ import annotations
from dataclasses import dataclass
import math
import time
from typing import Callable

PROFILES = {
 'sakura': {'joy': .9, 'nod': .85, 'praise': 'Richtig! Das hast du gut gemacht.', 'encourage': 'Kein Problem. Wir schauen es uns gemeinsam noch einmal an.'},
 'aiko': {'joy': .65, 'nod': .60, 'praise': 'Sehr schön. Genau so ist es.', 'encourage': 'Lass dir Zeit. Die Erklärung bleibt für dich sichtbar.'},
 'haruto': {'joy': .48, 'nod': .80, 'praise': 'Genau richtig. Gut aufgepasst!', 'encourage': 'Noch nicht. Vergleiche die Erklärung noch einmal in Ruhe.'},
 'ren': {'joy': 1.2, 'nod': 1.12, 'praise': 'Jawoll, richtig! Gut gemacht!', 'encourage': 'Alles gut! Noch ein Versuch, ganz ohne Stress.'},
 'miyako': {'joy': .62, 'nod': .66, 'praise': 'Wunderbar. Ein weiterer kleiner Schritt.', 'encourage': 'Wiederholung gehört dazu. Wir nehmen uns die Zeit.'},
 'emiri': {'joy': 1.28, 'nod': 1.14, 'praise': 'Juhu, das stimmt! Weiter so!', 'encourage': 'Du bleibst dran! Lass uns noch einmal zusammen üben.'},
 'satoshi': {'joy': .44, 'nod': .70, 'praise': 'Richtig zugeordnet. Gut verstanden.', 'encourage': 'Schau dir den Unterschied noch einmal an. Du darfst nachlesen.'},
 'yuki': {'joy': .66, 'nod': .67, 'praise': 'Passt. Gut gemacht!', 'encourage': 'Noch nicht ganz. Die Lernkarte hilft dir beim nächsten Versuch.'},
}


def ease(value: float) -> float:
    x = min(1.0, max(0.0, value))
    return x*x*(3-2*x)


def reaction_envelope(age: float, duration: float=2.65) -> float:
    """Fast but smooth entrance, enough reading time, then a gentle return to idle."""
    if age < 0 or age >= duration:
        return 0.0
    return ease(age/.16) * ease((duration-age)/.46)


@dataclass(frozen=True)
class ReactionSample:
    mood: str = 'idle'
    age: float = 0.0
    amount: float = 0.0
    sequence: int = 0
    teacher_id: str = ''
    source: str = ''
    message: str = ''


class ReactionController:
    """Transient UI state only; never writes XP, correctness or learner progress."""
    DURATION = 2.65
    def __init__(self, clock: Callable[[], float] = time.monotonic):
        self.clock = clock
        self.sequence = 0
        self.teacher_id = ''
        self.source = ''
        self.mood = 'idle'
        self.started = 0.0

    def trigger(self, mood: str, teacher_id: str, source: str='answer') -> bool:
        if mood not in ('praise', 'encourage') or teacher_id not in PROFILES:
            return False
        self.sequence += 1
        self.mood, self.teacher_id, self.source = mood, teacher_id, source
        self.started = self.clock()
        return True

    def clear(self):
        self.mood = 'idle'
        self.teacher_id = ''
        self.source = ''

    def sample(self, teacher_id: str, recording: bool=False, job: str='') -> ReactionSample:
        # Recording and actual processing always take precedence. No talk-loop is
        # inferred from button clicks; mouths remain closed for these activities.
        if recording:
            return ReactionSample('listening', teacher_id=teacher_id)
        if job in ('Vorlesen', 'Hörbeispiel'):
            return ReactionSample('speaking', teacher_id=teacher_id)
        if job == 'Spracherkennung':
            return ReactionSample('thinking', teacher_id=teacher_id)
        age = self.clock() - self.started
        if self.mood == 'idle' or self.teacher_id != teacher_id or age >= self.DURATION:
            return ReactionSample(teacher_id=teacher_id)
        profile = PROFILES[teacher_id]
        message = profile[self.mood]
        if self.source == 'speech-match':
            message = ('Das Zielwort wurde erkannt. Gut gemacht!' if self.mood == 'praise'
                       else 'Die Erkennung war noch nicht eindeutig. Probiere es in Ruhe noch einmal.')
        elif self.source == 'speech-uncertain':
            message = 'Die Aufnahme ist nicht sicher auswertbar. Das ist keine falsche Antwort.'
        elif self.source == 'review-known':
            message = 'Schön, dass du dich erinnerst. Weiter so!'
        elif self.source == 'lesson-complete':
            message = 'Lektion geschafft! Du bist drangeblieben. Gut gemacht!'
        return ReactionSample(self.mood, max(0., age), reaction_envelope(age, self.DURATION),
                              self.sequence, teacher_id, self.source, message)


def nod_envelope(age: float) -> float:
    """A single nod and a much smaller settling motion, never a repeating bounce."""
    if 0 <= age < .88:
        return math.sin(math.pi*age/.88)**2
    if .88 <= age < 1.35:
        return -.16*math.sin(math.pi*(age-.88)/.47)**2
    return 0.
