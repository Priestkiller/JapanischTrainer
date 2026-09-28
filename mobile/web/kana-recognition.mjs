import {isShortKana,speechMatch} from './core.mjs';

// Called only for a current, completed native recording with detected speech.
// Uncertain transcription is a technical outcome, not a learner's mistake.
export function applyKanaRecognition(session,text,qualified=false) {
 if(!qualified||session.mode!=='learn'||session.phase!=='speak'||session.success||!session.audio_seen||!isShortKana(session.card.jp))return false;
 const target=session.course.speechTarget(session.card,session.lesson);
 if(speechMatch(text,[target.target,...(target.accept??[])])){session.checkSpeech(text);return true;}
 session.shortSpeechReady=true;session.metrics().speech_attempts++;
 session.feedback='Deine Aufnahme enthält Sprache. Einzelne Kana lassen sich nicht immer sicher verschriftlichen. Das zählt nicht als Lernfehler: Höre deine Aufnahme und die Vorlage an und bestätige bei Bedarf die Selbstprüfung.';
 session.snapshot();return true;
}
