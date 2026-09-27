"""Reproducible structural inventory and explicit first-package review status.

Never reads learner data. Full linguistic review is deliberately NOT inferred.
Usage: python tools/audit_course.py --output <report-directory>
"""
import argparse,csv,hashlib,json,re,subprocess,unicodedata
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='3eb4384273b981962dd67aae75bc56eacf45b917'

def normalize(text):
    return re.sub(r'[\s。、！？!?.,・\-]','',unicodedata.normalize('NFKC',text)).lower()

def export(out):
    out.mkdir(parents=True,exist_ok=True)
    source_files=['data/course.json','data/deep_lessons.json','data/catalog.json','mobile/web/talk.mjs','learning.py','study.py','lesson_ui.py','mobile/web/core.mjs','mobile/web/app.mjs','tools/upgrade_foundations.py','tools/audit_course.py']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_files}
    d=json.loads((ROOT/'data/course.json').read_text('utf-8'))
    deep=json.loads((ROOT/'data/deep_lessons.json').read_text('utf-8'))
    cat=json.loads((ROOT/'data/catalog.json').read_text('utf-8'))
    raw={l.get('id',f'{u}:{i}'):(l,u,i,unit) for u,unit in enumerate(d['units']) for i,l in enumerate(unit['lessons'])}
    order=d['learning_order'];cards=[];matrix=[];edges=[];first={};raw_jp=[]
    for pos,key in enumerate(order,1):
        l,u,i,unit=raw[key];path=f'data/course.json#/units/{u}/lessons/{i}'
        guide=l.get('study_guide');status='Paket 01: redaktionell überarbeitet' if guide else 'erfasst; inhaltliche Einzelprüfung offen'
        matrix.append({'position':pos,'lektion':key,'quelle':path,'titel':l['title'],'abschnitt':l.get('stage',unit['level']),
          'karten':len(l['cards']),'explizite_sprechziele':len(l.get('speech',[])),'lernziel':l.get('goal','nicht explizit angegeben'),
          'vorwissen':'; '.join(guide['prerequisites']) if guide else 'nicht explizit modelliert',
          'erklaerung': 'study_guide: 3 Lernhilfen' if guide else ('intro vorhanden' if l.get('intro') else 'Kartenprofil / Laufzeit-Fallback'),
          'erfassung':'vollständig','inhaltsstatus':status,'menschliche_fachpruefung':'offen',
          'gespraech':'BESTAND.md#gesprächsverknüpfung'})
        if pos>1:edges.append({'from':order[pos-2],'to':key,'type':'technisch','basis':'aus learning_order abgeleitet','note':'Normaler Erstlernweg; Altfreigaben und bestehende Abschlüsse werden separat berücksichtigt.'})
        if guide:
            for p in guide['prerequisites']:edges.append({'from':p,'to':key,'type':'didaktisch','basis':'explizit redaktionell eingeführt in 11.0.2','source':path+'/study_guide/prerequisites'})
        for ci,c in enumerate(l['cards']):
            ck=f'{key}:{ci}';norm=normalize(c['jp']);first.setdefault(norm,ck);raw_jp.append(c['jp'])
            profile=c.get('detail') or deep['profiles'].get(c['jp']);ex=c.get('example') or cat['EXAMPLES'].get(c['jp'])
            target=next((t for t in l.get('speech',[]) if t['target'].rstrip('。！？!?')==c['jp'].rstrip('。！？!?')),None)
            cards.append({'karte':ck,'lektion':key,'quelle':path+f'/cards/{ci}','japanisch':c['jp'],'romaji':c['romaji'],'deutsch':c['de'],
              'erstes_vorkommen_normalisiert':first[norm],'einfuehrung':'Karte mit Vorlage in Schritt 1; Beherrschung nicht daraus ableiten',
              'erklaerungsquelle':'card.detail' if c.get('detail') else 'deep_lessons.profiles' if profile else 'Laufzeit-Fallback',
              'beispielquelle':'card.example' if c.get('example') else 'catalog.EXAMPLES' if ex else 'Karte selbst als Fallback',
              'sprechen':'explizites Sprechziel' if target else 'Kartenform als Laufzeit-Fallback',
              'anwendungsfrage':profile['scenario']['question'] if profile else 'Generische Bedeutungszuordnung',
              'erfassung':'vollständig','inhaltsstatus':status,'menschliche_fachpruefung':'offen'})
    for name,rows in [('LERNZIELMATRIX.csv',matrix),('KARTENPRUEFUNG.csv',cards)]:
        with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    positions={k:i for i,k in enumerate(order)}
    assert len(order)==len(set(order))==len(raw)
    assert all(e['from'] in raw and e['to'] in raw and positions[e['from']]<positions[e['to']] for e in edges)
    (out/'VORAUSSETZUNGEN.json').write_text(json.dumps({'schema':1,'nodes':order,'edges':edges,'unknown':'Keine automatisierte Vollanalyse impliziter Sprachvoraussetzungen; Wiederholungsimpulse stehen bei den 30 Lernhilfen. Technische Reihenfolge ist keine fachliche Voraussetzungenliste.'},ensure_ascii=False,indent=2)+'\n','utf-8')
    def md(name,text): (out/name).write_text(text.strip()+'\n','utf-8')
    counts=Counter(raw_jp);normcounts=Counter(normalize(x) for x in raw_jp)
    guided=[m for m in matrix if m['inhaltsstatus'].startswith('Paket')]
    # Serialize every actual conversation node and route, including executable text
    # templates as source instead of inventing a single representative dialogue.
    script="import {SCENES} from './mobile/web/talk.mjs'; console.log(JSON.stringify(SCENES,(_k,v)=>v instanceof RegExp?v.toString():typeof v==='function'?v.toString():v));"
    scenes=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],cwd=ROOT,text=True,encoding='utf-8'))
    scene_text=[]
    for scene in scenes:
        scene_text.append(f"### {scene['id']}: {scene['title']}\n\nZiel: {scene['goal']}\n\nStart: `{scene['start']}`. Passende Kurslektion: `v11:dialog-{scene['id']}`. Das ist eine thematische Verbindung, kein Nachweis vollständiger Vorbereitung.")
        for nk,node in scene['nodes'].items():
            scene_text.append(f"#### Knoten `{nk}`\n\nQuelle: `mobile/web/talk.mjs: SCENES[{scene['id']}].nodes.{nk}`\n\n```json\n{json.dumps(node,ensure_ascii=False,indent=2)}\n```")
        scene_text.append('Vorwissen bleibt pro Gespräch fachlich zu prüfen. Unbekannte Antworten führen zu einer Rückfrage, Wiederholungsbitten bleiben am Knoten. Erkannten Text kann man korrigieren; Hilfen liefern ganze Antwortvarianten. Abschluss bleibt von Kurs-XP und Freischaltung getrennt. Die automatisierten Routentests prüfen erreichbare Ziele, keine freie Konversationsfähigkeit.')
    md('BESTAND.md',f'''# Kursbestand 11.0.2

Ausgangscommit vor Umsetzung: `{BASE}`. Laufzeitquellen: `data/course.json`, `data/catalog.json`, `data/deep_lessons.json`; beide Plattformen verwenden diese Quellen. Android kopiert sie mit `mobile/tools/prepare_assets.py`, Windows mit `tools/stage_release.py`.

- {len(order)} Lektionen, {len(cards)} Karten, {sum(m['explizite_sprechziele'] for m in matrix)} explizite Sprechdatensätze; fehlende explizite Ziele bekommen einen Laufzeit-Fallback. {len(cat['TEACHERS'])} Lehrer.
- {len(counts)} unterschiedliche rohe japanische Kartenformen, {len(normcounts)} nach NFKC, Kleinschreibung sowie Entfernung von Leerraum und definierter Interpunktion. Hiragana und Katakana werden dabei nicht gleichgesetzt.
- {sum(v-1 for v in counts.values())} weitere Vorkommen bereits vorhandener roher Formen. Dopplungen bleiben bewusst erhalten und sind nicht automatisch Inhaltsfehler.
- {len(guided)} Lektionen und {sum(m['karten'] for m in guided)} Karten im ersten überarbeiteten Paket. Die übrigen {len(order)-len(guided)} Lektionen sind strukturell erfasst, nicht einzeln fachlich abgenommen.

## Zähl- und Prüfgrenzen

Eine Karte zählt je vorhandener Position, ein explizites Sprechziel je speech-Datensatz. Erstvorkommen bedeutet nur erste Karte im Lernweg; Beispiele, Hörtexte und Gesprächsformen können früher vorkommen. Es wird weder eine vollständige Vokabelliste noch eine geprüfte Ersteinführung aller sprachlichen Bestandteile behauptet. Ein Strukturtest ersetzt keine muttersprachliche Sprachprüfung und keine Anfänger-Erprobung.

## Gesprächsverknüpfung

Alle fünf tatsächlich vorhandenen Szenen, Knoten, Muster und Folgeknoten folgen. Funktionen sind ihre tatsächlichen Quelltextvorlagen; dadurch bleiben Platzhalter und alternative Zweige erkennbar. Die vollständige sprachliche Vorbereitung aller Antwortwege ist noch offen.

{chr(10).join(scene_text)}
''')
    md('LUECKEN_UND_SPRUENGE.md','''# Belegte Befunde und verbleibende Lücken

Stand: erstes Umsetzungspaket 11.0.2, keine vollständige Fachabnahme.

| Priorität | Fundstelle | Befund am Ausgangsstand | Umsetzung / Rest |
| --- | --- | --- | --- |
| Hoch | lesson_ui.py: draw_lesson, _draw_study_content | Windows zeigte während Bedeutung, Schreiben und Abschlussrunde JP, Romaji und deutsche Lösung; ein Beispiel verriet zusätzlich die Bedeutung. | Vorlage nur beim Erklären oder nach bewusstem Hilfeaufruf; Beispiele nach Erfolg. Native UI geprüft. |
| Hoch | mobile/web/app.mjs: explanation, task; course.json: intro | Android zeigte die Lektions-Einführung nicht; vorhandene Kartenprofile waren standardmäßig eingeklappt. | Sichtbares Lernziel und Lernhilfen für 30 Lektionen; vorhandene intro-Texte der weiteren Lektionen sind jetzt erreichbar. |
| Hoch | 0:1:0 sowie v11:long-vowels, v11:small-tsu, v11:mora-n | Wörter setzen Kana voraus, deren systematische Reihen erst später kommen, z. B. さ in あさ. | Lokale Zeichenhilfen erklären benötigte neue Zeichen vor dem systematischen Drill. Reihenfolge unverändert. Dies ist eine didaktische Einschätzung, kein Syntaxfehler. |
| Mittel | v11:kata-basics bis v11:kata-combinations | Einsteiger benötigen weitere Katakana neben den frühen Grundreihen. | Zeichenhilfen, Längen, kleine Zeichen und Wortzerlegungen in den sechs Lektionen ergänzt. |
| Mittel | Kartenprofile: scenario.question | Viele Aufgaben fragten nur nach „dieser Karte“, obwohl die mobile Vorlage verborgen war. Manche Leseaufgaben zeigten ihren Ausgangstext nicht. | Einstieg: konkrete Bezüge plus 18 Situationsaufgaben. Generische übrige Aufgaben nennen ihre Form in der UI; Leseverständnis zeigt den JP-Text. Weitere Abwechslung bleibt offen. |

Die Daten enthalten viele sinnvolle eigene Erklärungen, Gegensatzpaare und bestehende Alltagsszenen. Erhalten: stabile IDs, sechs Android-Schritte mit echten Freigabebedingungen, getrennte Kana-Selbstprüfung, wiederholbare Karten und Offline-Gesprächswege. Die automatische Erkennung ist Textabgleich, keine Akzentnote.

Offen: implizite Grammatik- und Wortschatzvoraussetzungen der weiteren 120 Lektionen sowie jedes Gesprächszweigs fachlich einzeln prüfen. Keine bloße Zählung wird als Schließung dieser Lücke ausgegeben.
''')
    package=['# Paket 01: tatsächlich umgesetzt','30 bestehende Lektionen vertieft, keine neue Lektions-ID. Gemeinsame Kursdaten werden in Windows und Android geladen. Alle ursprünglichen Kartenpositionen und Zieltexte bleiben erhalten.','Abnahme pro Lektion: Erklärungen vor bzw. während bewusster Hilfe erreichbar; sechs Schritte weiterhin lösbar; Voraussetzungsschlüssel gültig; muttersprachliche Prüfung und Anfänger-Erprobung noch offen.']
    for m in guided:
        l=raw[m['lektion']][0];g=l['study_guide']
        package.append(f"## {m['position']}. {m['titel']} (`{m['lektion']}`)\n\nArt: Überarbeitung. Position unverändert.\n\nZiel: {m['lernziel']}\n\nVoraussetzungen: {m['vorwissen'] or 'keine'}.\n\n"+'\n\n'.join(g['points'])+f"\n\nAbruf / Wiederholung: {g['recall']}\n\nÜbungen: bestehende sechs Schritte; situationsbezogene Ergänzungen siehe Kartenmatrix. Gesprächsbezug: Grundlagen für Kennenlernen; bei Aussprache und Schrift auch für alle weiteren Szenen. Eine vollständige Gesprächsvorbereitung wird daraus nicht abgeleitet.")
    md('PAKET_01.md','\n\n'.join(package))
    md('AUSBAUPLAN.md','''# Weiterer Ausbau nach Paket 01

Das erste Paket ist in beiden Programmen umgesetzt. 150 Lektionen bleiben 150; 300–400 sind kein Abnahmekriterium. Erst die folgenden Einzelprüfungen entscheiden, ob neue Lektionen erforderlich sind.

| Folgepaket | Ziel / Position | Umfang als Planung | Erklärungen und Übungen | Gespräch / Abnahme |
| --- | --- | --- | --- | --- |
| 02: Satzbau und Rückfragen | Nach den 30 Einstiegslektionen: Partikeln, Ortsangaben, Besitz, Fragewörter | 15–25 vorhandene Lektionen vertiefen; 0–5 neue Brücken nur nach Befund | Vorher nötige Wörter kenntlich machen; Aussagen in Fragen umformen; bekannte Satzmuster mischen | Kennenlernen und Wegfragen; jede neue Form vor freiem Abruf erklären, menschlich gegenprüfen |
| 03: Einkaufen und Café | Auf Partikeln und Zahlen aufbauen | 15–25 Überarbeitungen; 0–6 neue Brücken nach Prüfung der tatsächlichen Gesprächszweige | Preise, Mengen, Temperatur, Größen, Mitnehmen und Bezahlen als echte Auswahlaufgaben | Beide Szenen mit mindestens zwei verschiedenen Wegen ohne ungelernte Pflichtantwort absolvieren |
| 04: Zeit und Verabredungen | Auf Zeitangaben, Verben und Einladungen aufbauen | 15–25 Überarbeitungen; 0–5 Ergänzungen bei nachgewiesenen Lücken | Tag/Uhrzeit/Treffpunkt austauschen, Alternativen anbieten, später erneut abrufen | Wochenendszene; menschliche Sprachprüfung und Anfänger-Durchlauf |
| 05: Lesen und Wiederholen | Über mehrere Kapitel verteilt, nach den jeweiligen Formen | 10–20 bestehende Lektionen prüfen; neue Anzahl offen | Kurze ungesehene Texte mit bekanntem Wortschatz; zeitlich versetzter Abruf und echte Verständnisfragen | Inhalt beantworten statt Vorlage kopieren; jede falsche Auswahl begründbar |

Die Spannen sind Planungsannahmen, keine vollständig spezifizierten Zusatzlektionen. Alle Pakete betreffen die gemeinsamen Kursdaten und beide Oberflächen; Offline-Gespräche bleiben zunächst Android-Funktion. Neue IDs nur für wirklich neue Inhalte, keine Neunummerierung alter Fortschritte. Voraussetzungsketten werden vor neuen Aufgaben geprüft. Wiederholung ist keine harte Freischaltbedingung.

Fachliche Abnahme: muttersprachliche Person prüft Natürlichkeit, Bedeutungen und Höflichkeit; Anfänger-Durchlauf prüft Verständlichkeit ohne externe Hilfe. Geräteabnahme: echte Stimme/Mikrofon/Lautsprecher am S24 Ultra und Windows, einschließlich Update über die vorhandene Installation. Automatische Modelltests ersetzen diese Schritte nicht.
''')
    md('PRUEFBERICHT.md',f'''# Struktureller Prüfbericht

{len(matrix)} eindeutige Lektionszeilen und {len(cards)} eindeutige Kartenzeilen; vollständige Abdeckung der tatsächlichen Kursquellen. {len(edges)} getrennt typisierte Beziehungen; alle Ziele vorhanden, alle hier explizit modellierten Voraussetzungskanten zeigen auf eine frühere Lektion und sind damit zyklenfrei. Unbekannte implizite Voraussetzungen bleiben unbekannt.

Redaktionell bearbeitet: erste 30 Lektionen. Vollständige fachliche Prüfung aller 150 Lektionen: **nicht abgeschlossen**. Menschliche Sprach- und Anfängerprüfung: **nicht ausgeführt**.

Export: `python tools/audit_course.py --output <Zielordner>`. Fachliche Ausgaben enthalten keine Laufzeitstempel. Gleiche Eingabedateien einschließlich redaktioneller Guides und dieses Skripts ergeben dieselben Berichte. Prüfergebnisse der Programmtests und fertigen Builds werden separat in `TESTBERICHT_11.0.2.md` festgehalten.

Die Lehrtexte wurden eigenständig formuliert. Abgleich einzelner Schrift-/Leseregeln mit [Kana-Übersicht der Japan Foundation](https://www.irodori.jpf.go.jp/assets/data/Kana_all.pdf), Vorstellungen mit [Irodori Starter, Lektion 3](https://www.irodori.jpf.go.jp/assets/data/starter/pdf/X_L03.pdf). Diese Stichproben sind keine komplette externe Kursvalidierung.

## Eingabefingerabdrücke (SHA-256)

```json
{json.dumps(hashes,indent=2)}
```
''')
    print(json.dumps({'lessons':len(matrix),'cards':len(cards),'reviewedLessons':len(guided),'reviewedCards':sum(m['karten'] for m in guided),'scenes':len(scenes),'nodes':sum(len(s['nodes']) for s in scenes),'edges':len(edges)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);export(p.parse_args().output)
