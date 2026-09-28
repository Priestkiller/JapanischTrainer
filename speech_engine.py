from __future__ import annotations

import json
import math
import os
import re
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np

try:
    import sounddevice as sd
except Exception:
    sd = None

try:
    import sherpa_onnx
except Exception:
    sherpa_onnx = None

try:
    from pykakasi import kakasi as _kakasi_factory
except Exception:
    _kakasi_factory = None


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


ROOT = app_root()
MODELS = ROOT / "models"
PARAKEET_DIR = MODELS / "parakeet-ja"
SENSEVOICE_DIR = MODELS / "sensevoice"
TTS_DIR = MODELS / "supertonic"


@dataclass
class AudioQuality:
    status: str
    message: str
    duration: float
    speech_duration: float
    peak: float
    rms: float
    clipping_percent: float
    gain_applied: float


@dataclass
class SpeechScore:
    score: int
    heard: str
    matched_target: str
    reading_heard: str
    reading_target: str


@dataclass
class PronunciationResult:
    score: int
    heard: str
    matched_target: str
    reading_heard: str
    reading_target: str
    engine: str
    alternatives: list[tuple[str, str, int]] = field(default_factory=list)
    quality: AudioQuality | None = None
    reliable: bool = True


def _kata_to_hira(text: str) -> str:
    out = []
    for ch in text:
        code = ord(ch)
        if 0x30A1 <= code <= 0x30F6:
            out.append(chr(code - 0x60))
        else:
            out.append(ch)
    return "".join(out)


def _strip(text: str) -> str:
    text = str(text or "").lower()
    text = re.sub(r"[\s\u3000、。！？!?.,・:;\-—―…\"'（）()「」『』【】\[\]]+", "", text)
    return _kata_to_hira(text)


_kakasi = None
if _kakasi_factory is not None:
    try:
        _kakasi = _kakasi_factory()
    except Exception:
        _kakasi = None


def reading(text: str) -> str:
    """Convert Japanese text to a hiragana-like reading where possible."""
    base = _strip(text)
    if _kakasi is None:
        return base
    try:
        converted = _kakasi.convert(str(text or ""))
        hira = "".join(part.get("hira", part.get("orig", "")) for part in converted)
        return _strip(hira)
    except Exception:
        return base


def _morae(text: str) -> list[str]:
    s = reading(text)
    small = set("ゃゅょぁぃぅぇぉゎゕゖ")
    out: list[str] = []
    for ch in s:
        if ch in small and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def _romaji(text: str) -> str:
    if _kakasi is None:
        return text
    try:
        parts = _kakasi.convert(text)
        return "".join(p.get("hepburn", p.get("orig", "")) for p in parts).lower()
    except Exception:
        return text.lower()


def _vowel(roma: str) -> str:
    for c in reversed(roma):
        if c in "aeiou":
            return c
    return ""


def _initial(roma: str) -> str:
    m = re.match(r"([^aeiou]*)([aeiou].*)?$", roma)
    return (m.group(1) if m else roma).replace("y", "j")


def _sub_cost(a: str, b: str) -> float:
    if a == b:
        return 0.0
    ra, rb = _romaji(a), _romaji(b)
    if ra == rb:
        return 0.0
    va, vb = _vowel(ra), _vowel(rb)
    ia, ib = _initial(ra), _initial(rb)
    voiced_pairs = [
        {"k", "g"}, {"s", "z"}, {"sh", "j"}, {"t", "d"},
        {"ch", "j"}, {"h", "b"}, {"h", "p"}, {"b", "p"},
    ]
    if va and va == vb and any({ia, ib} <= pair for pair in voiced_pairs):
        return 0.42
    if va and va == vb:
        return 0.72
    # し/ち, す/つ and similar nearby learner confusions should be penalized,
    # but not as harshly as a completely unrelated mora.
    if {ra, rb} in ({"shi", "chi"}, {"su", "tsu"}, {"ji", "chi"}):
        return 0.62
    return 1.0


def _del_cost(token: str) -> float:
    if token in {"っ", "ー"}:
        return 0.55
    return 1.0


def _weighted_distance(a: list[str], b: list[str]) -> float:
    if not a:
        return sum(_del_cost(x) for x in b)
    if not b:
        return sum(_del_cost(x) for x in a)
    prev = [0.0]
    for tok in b:
        prev.append(prev[-1] + _del_cost(tok))
    for aa in a:
        cur = [prev[0] + _del_cost(aa)]
        for j, bb in enumerate(b, start=1):
            cur.append(min(
                cur[-1] + _del_cost(bb),
                prev[j] + _del_cost(aa),
                prev[j - 1] + _sub_cost(aa, bb),
            ))
        prev = cur
    return prev[-1]


def similarity(a: str, b: str) -> float:
    # Exact surface match first. This also handles ASR orthography variants that
    # are explicitly accepted in a lesson, e.g. 今日は for the greeting.
    if _strip(a) and _strip(a) == _strip(b):
        return 1.0
    aa, bb = _morae(a), _morae(b)
    m = max(len(aa), len(bb))
    if m == 0:
        return 1.0
    d = _weighted_distance(aa, bb)
    return max(0.0, 1.0 - d / m)


def grade_pronunciation(heard: str, accepted: Iterable[str]) -> SpeechScore:
    candidates = [x for x in accepted if str(x).strip()] or [""]
    best = max(candidates, key=lambda x: similarity(heard, x))
    raw = similarity(heard, best)
    # Mild beginner curve only. The main accuracy improvement now comes from
    # Japanese-specific ASR + mora-aware comparison rather than inflating scores.
    adjusted = raw
    if 0.58 <= raw < 0.90:
        adjusted = min(0.92, raw + 0.035)
    return SpeechScore(
        score=round(adjusted * 100),
        heard=str(heard or "").strip(),
        matched_target=best,
        reading_heard=reading(heard),
        reading_target=reading(best),
    )


def _audio_quality(audio: np.ndarray, sample_rate: int) -> tuple[np.ndarray, AudioQuality]:
    x = np.asarray(audio, dtype=np.float32).reshape(-1)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    if len(x) == 0:
        q = AudioQuality("bad", "Keine Audiodaten.", 0, 0, 0, 0, 0, 1)
        return x, q

    duration = len(x) / max(1, sample_rate)
    x = x - float(np.mean(x))
    raw_peak = float(np.max(np.abs(x))) if len(x) else 0.0
    raw_rms = float(np.sqrt(np.mean(x * x) + 1e-12))
    clipping = float(np.mean(np.abs(x) >= 0.985) * 100.0)

    frame = max(64, int(sample_rate * 0.025))
    hop = max(32, int(sample_rate * 0.010))
    vals = []
    starts = []
    for start in range(0, max(1, len(x) - frame + 1), hop):
        seg = x[start:start + frame]
        if len(seg) < frame // 2:
            break
        vals.append(float(np.sqrt(np.mean(seg * seg) + 1e-12)))
        starts.append(start)
    if not vals:
        vals = [raw_rms]
        starts = [0]
    rv = np.asarray(vals, dtype=np.float32)
    noise = float(np.percentile(rv, 20))
    upper = float(np.percentile(rv, 80))
    threshold = max(0.0045, noise * 2.6, upper * 0.20)
    voiced = np.where(rv >= threshold)[0]

    if len(voiced):
        first = max(0, starts[int(voiced[0])] - int(sample_rate * 0.18))
        last = min(len(x), starts[int(voiced[-1])] + frame + int(sample_rate * 0.22))
        trimmed = x[first:last]
        speech_duration = max(0.0, (last - first) / sample_rate)
    else:
        trimmed = x
        speech_duration = 0.0

    speech_rms = float(np.sqrt(np.mean(trimmed * trimmed) + 1e-12)) if len(trimmed) else 0.0
    target_rms = 0.085
    gain = 1.0 if speech_rms <= 1e-6 else min(8.0, max(0.65, target_rms / speech_rms))
    processed = np.clip(trimmed * gain, -0.98, 0.98).astype(np.float32, copy=False)

    if duration < 0.22 or speech_duration < 0.16:
        status, msg = "bad", "Zu wenig Sprache erkannt. Bitte etwas länger sprechen."
    elif raw_peak < 0.012 or raw_rms < 0.0025:
        status, msg = "bad", "Das Mikrofon ist sehr leise. Näher ans Mikrofon gehen oder Eingangspegel erhöhen."
    elif clipping > 1.5:
        status, msg = "bad", "Die Aufnahme übersteuert. Mikrofonpegel etwas reduzieren oder weiter weg sprechen."
    elif noise > 0.020 and upper < noise * 2.0:
        status, msg = "warn", "Relativ viel Hintergrundgeräusch erkannt. Ein ruhigerer Raum verbessert die Auswertung."
    else:
        status, msg = "good", "Aufnahmepegel ist brauchbar."

    q = AudioQuality(
        status=status,
        message=msg,
        duration=duration,
        speech_duration=speech_duration,
        peak=raw_peak,
        rms=raw_rms,
        clipping_percent=clipping,
        gain_applied=gain,
    )
    return processed, q


class LocalSpeechEngine:
    def __init__(self) -> None:
        self._tts = None
        self._parakeet = None
        self._sense = None
        self._tts_lock = threading.Lock()
        self._asr_lock = threading.Lock()
        self._stream = None
        self._chunks: list[np.ndarray] = []
        self._recording = False
        self.sample_rate = 48000
        self.input_device = None
        self.last_quality: AudioQuality | None = None

    @property
    def tts_ready(self) -> bool:
        required = [
            "duration_predictor.int8.onnx", "text_encoder.int8.onnx",
            "vector_estimator.int8.onnx", "vocoder.int8.onnx", "tts.json",
            "unicode_indexer.bin", "voice.bin",
        ]
        return all((TTS_DIR / f).is_file() for f in required)

    @property
    def parakeet_ready(self) -> bool:
        return (PARAKEET_DIR / "model.int8.onnx").is_file() and (PARAKEET_DIR / "tokens.txt").is_file()

    @property
    def sensevoice_ready(self) -> bool:
        return (SENSEVOICE_DIR / "model.int8.onnx").is_file() and (SENSEVOICE_DIR / "tokens.txt").is_file()

    @property
    def asr_ready(self) -> bool:
        return self.parakeet_ready or self.sensevoice_ready

    def model_status(self) -> dict:
        names = []
        if self.parakeet_ready:
            names.append("Parakeet JA 35k")
        if self.sensevoice_ready:
            names.append("SenseVoice Reserve")
        return {
            "tts": self.tts_ready,
            "asr": self.asr_ready,
            "runtime": sherpa_onnx is not None,
            "parakeet": self.parakeet_ready,
            "sensevoice": self.sensevoice_ready,
            "asr_name": " + ".join(names) if names else "fehlt",
        }

    def list_input_devices(self) -> list[tuple[int, str]]:
        if sd is None:
            return []
        out = []
        try:
            for i, d in enumerate(sd.query_devices()):
                if int(d.get("max_input_channels", 0)) > 0:
                    sr = int(float(d.get("default_samplerate", 0) or 0))
                    suffix = f" · {sr//1000} kHz" if sr else ""
                    out.append((i, str(d.get("name", f"Device {i}")) + suffix))
        except Exception:
            pass
        return out

    def _ensure_tts(self):
        if sherpa_onnx is None:
            raise RuntimeError("sherpa-onnx ist nicht installiert.")
        if not self.tts_ready:
            raise RuntimeError("Das lokale japanische TTS-Modell fehlt.")
        if self._tts is not None:
            return self._tts
        with self._tts_lock:
            if self._tts is None:
                cfg = sherpa_onnx.OfflineTtsConfig(
                    model=sherpa_onnx.OfflineTtsModelConfig(
                        supertonic=sherpa_onnx.OfflineTtsSupertonicModelConfig(
                            duration_predictor=str(TTS_DIR / "duration_predictor.int8.onnx"),
                            text_encoder=str(TTS_DIR / "text_encoder.int8.onnx"),
                            vector_estimator=str(TTS_DIR / "vector_estimator.int8.onnx"),
                            vocoder=str(TTS_DIR / "vocoder.int8.onnx"),
                            tts_json=str(TTS_DIR / "tts.json"),
                            unicode_indexer=str(TTS_DIR / "unicode_indexer.bin"),
                            voice_style=str(TTS_DIR / "voice.bin"),
                        ),
                        debug=False,
                        num_threads=max(2, min(6, os.cpu_count() or 2)),
                        provider="cpu",
                    )
                )
                if not cfg.validate():
                    raise RuntimeError("Supertonic-Konfiguration konnte nicht validiert werden.")
                self._tts = sherpa_onnx.OfflineTts(cfg)
        return self._tts

    def _ensure_parakeet(self):
        if sherpa_onnx is None or not self.parakeet_ready:
            return None
        if self._parakeet is not None:
            return self._parakeet
        with self._asr_lock:
            if self._parakeet is None:
                self._parakeet = sherpa_onnx.OfflineRecognizer.from_nemo_ctc(
                    model=str(PARAKEET_DIR / "model.int8.onnx"),
                    tokens=str(PARAKEET_DIR / "tokens.txt"),
                    num_threads=max(2, min(6, os.cpu_count() or 2)),
                    sample_rate=16000,
                    feature_dim=80,
                    decoding_method="greedy_search",
                    debug=False,
                    provider="cpu",
                )
        return self._parakeet

    def _ensure_sensevoice(self):
        if sherpa_onnx is None or not self.sensevoice_ready:
            return None
        if self._sense is not None:
            return self._sense
        with self._asr_lock:
            if self._sense is None:
                self._sense = sherpa_onnx.OfflineRecognizer.from_sense_voice(
                    model=str(SENSEVOICE_DIR / "model.int8.onnx"),
                    tokens=str(SENSEVOICE_DIR / "tokens.txt"),
                    num_threads=max(2, min(4, os.cpu_count() or 2)),
                    sample_rate=16000,
                    feature_dim=80,
                    language="ja",
                    use_itn=True,
                    debug=False,
                    provider="cpu",
                )
        return self._sense

    @staticmethod
    def _decode(recognizer, audio: np.ndarray, sample_rate: int) -> str:
        stream = recognizer.create_stream()
        stream.accept_waveform(int(sample_rate), np.asarray(audio, dtype=np.float32))
        recognizer.decode_stream(stream)
        result = stream.result
        text = getattr(result, "text", None)
        if text is None:
            try:
                if isinstance(result, str):
                    parsed = json.loads(result)
                    text = parsed.get("text", result)
                else:
                    text = str(result)
            except Exception:
                text = str(result)
        return str(text or "").strip()

    def speak(self, text: str, speed: float = 1.0, speaker_id: int = 0, cancelled=None) -> None:
        if cancelled and cancelled():return
        if sd is None:
            raise RuntimeError("sounddevice ist nicht verfügbar.")
        tts = self._ensure_tts()
        gen = sherpa_onnx.GenerationConfig()
        gen.sid = int(max(0, min(9, speaker_id)))
        gen.num_steps = 8
        gen.speed = float(speed)
        try:
            gen.extra["lang"] = "ja"
        except Exception:
            gen.extra = {"lang": "ja"}
        audio = tts.generate(text, gen)
        if cancelled and cancelled():return
        if audio is None or len(audio.samples) == 0:
            raise RuntimeError("Die Sprachsynthese hat kein Audio erzeugt.")
        sd.stop()
        sd.play(np.asarray(audio.samples, dtype=np.float32), int(audio.sample_rate), blocking=True)

    def start_recording(self, device: int | None = None) -> None:
        if sd is None:
            raise RuntimeError("sounddevice ist nicht verfügbar.")
        if self._recording:
            return
        self._chunks = []
        self.input_device = device
        try:
            info = sd.query_devices(device, "input") if device is not None else sd.query_devices(kind="input")
            native_sr = int(round(float(info.get("default_samplerate", 48000) or 48000)))
        except Exception:
            native_sr = 48000
        # Record at the microphone's native rate. Forcing cheap devices to 16 kHz
        # can make Windows resample badly before the ASR even sees the signal.
        self.sample_rate = max(16000, min(96000, native_sr))

        def callback(indata, frames, time_info, status):
            if self._recording:
                self._chunks.append(np.asarray(indata[:, 0], dtype=np.float32).copy())

        self._recording = True
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            device=device,
            callback=callback,
            blocksize=0,
        )
        self._stream.start()

    def stop_recording(self) -> np.ndarray:
        if not self._recording:
            return np.zeros(0, dtype=np.float32)
        self._recording = False
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            finally:
                self._stream = None
        if not self._chunks:
            return np.zeros(0, dtype=np.float32)
        audio = np.concatenate(self._chunks).astype(np.float32, copy=False)
        self._chunks = []
        return audio

    def recognize_for_target(self, audio: np.ndarray, accepted: Iterable[str], sample_rate: int | None = None) -> PronunciationResult:
        if audio is None or len(audio) < 1000:
            raise RuntimeError("Die Aufnahme war zu kurz oder leer.")
        if not self.asr_ready:
            raise RuntimeError("Kein lokales japanisches ASR-Modell gefunden.")
        sr = int(sample_rate or self.sample_rate)
        clean, quality = _audio_quality(audio, sr)
        self.last_quality = quality
        if len(clean) < max(800, int(sr * 0.12)):
            raise RuntimeError("Nach dem Entfernen der Stille war zu wenig Sprache übrig.")

        accepted = list(accepted)
        candidates: list[tuple[str, str, SpeechScore]] = []

        primary = self._ensure_parakeet()
        if primary is not None:
            text = self._decode(primary, clean, sr)
            candidates.append(("Parakeet JA", text, grade_pronunciation(text, accepted)))

        # SenseVoice is now a second opinion, not the main judge. It is especially
        # useful for very short isolated words where one recognizer may be unstable.
        secondary = self._ensure_sensevoice()
        primary_score = candidates[0][2].score if candidates else 0
        short_target = min((len(_morae(x)) for x in accepted if x), default=99) <= 8
        if secondary is not None and (short_target or primary_score < 94):
            text = self._decode(secondary, clean, sr)
            candidates.append(("SenseVoice", text, grade_pronunciation(text, accepted)))

        if not candidates:
            raise RuntimeError("Die ASR-Modelle konnten nicht geladen werden.")

        candidates.sort(key=lambda x: x[2].score, reverse=True)
        engine, heard, best = candidates[0]
        final = best.score

        # Consensus bonus is small and only applied when two independent engines
        # both land near the expected phrase. We do not blindly average them.
        if len(candidates) >= 2:
            second = candidates[1][2]
            if best.score >= 68 and second.score >= 68:
                agreement = similarity(candidates[0][1], candidates[1][1])
                if agreement >= 0.55:
                    final = min(100, final + 3)

        reliable = quality.status != "bad" or final >= 90
        return PronunciationResult(
            score=final,
            heard=heard,
            matched_target=best.matched_target,
            reading_heard=best.reading_heard,
            reading_target=best.reading_target,
            engine=engine,
            alternatives=[(e, t, s.score) for e, t, s in candidates],
            quality=quality,
            reliable=reliable,
        )

    def recognize(self, audio: np.ndarray, sample_rate: int | None = None) -> str:
        """Compatibility helper for free dictation. Uses the best available Japanese model."""
        sr = int(sample_rate or self.sample_rate)
        clean, quality = _audio_quality(audio, sr)
        self.last_quality = quality
        rec = self._ensure_parakeet() or self._ensure_sensevoice()
        if rec is None:
            raise RuntimeError("Kein lokales ASR-Modell gefunden.")
        return self._decode(rec, clean, sr)

    def play_recording(self, audio: np.ndarray, sample_rate: int | None = None) -> None:
        if sd is None:
            raise RuntimeError("sounddevice ist nicht verfügbar.")
        if audio is None or len(audio) == 0:
            raise RuntimeError("Keine Aufnahme vorhanden.")
        sd.stop()
        sd.play(np.asarray(audio, dtype=np.float32), int(sample_rate or self.sample_rate), blocking=True)
