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
    source_files=['data/course.json','data/deep_lessons.json','data/catalog.json','mobile/web/talk.mjs','learning.py','study.py','lesson_ui.py','mobile/web/core.mjs','mobile/web/app.mjs','tools/upgrade_foundations.py','tools/upgrade_package2.py','tools/upgrade_package3.py','tools/audit_course.py']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_files}
    d=json.loads((ROOT/'data/course.json').read_text('utf-8'))
    deep=json.loads((ROOT/'data/deep_lessons.json').read_text('utf-8'))
    cat=json.loads((ROOT/'data/catalog.json').read_text('utf-8'))
    raw={l.get('id',f'{u}:{i}'):(l,u,i,unit) for u,unit in enumerate(d['units']) for i,l in enumerate(unit['lessons'])}
    order=d['learning_order'];cards=[];matrix=[];edges=[];first={};raw_jp=[]
    for pos,key in enumerate(order,1):
        l,u,i,unit=raw[key];path=f'data/course.json#/units/{u}/lessons/{i}'
        guide=l.get('study_guide');status=f'Paket {guide.get("package",1):02}: eigene sprachliche Durchsicht und Überarbeitung' if guide else 'erfasst; inhaltliche Einzelprüfung offen'
        matrix.append({'position':pos,'lektion':key,'quelle':path,'titel':l['title'],'abschnitt':l.get('stage',unit['level']),
          'karten':len(l['cards']),'explizite_sprechziele':len(l.get('speech',[])),'lernziel':l.get('goal','nicht explizit angegeben'),
          'vorwissen':'; '.join(guide['prerequisites']) if guide else 'nicht explizit modelliert',
          'erklaerung': 'study_guide: 3 Lernhilfen' if guide else ('intro vorhanden' if l.get('intro') else 'Kartenprofil / Laufzeit-Fallback'),
          'erfassung':'vollständig','inhaltsstatus':status,'menschliche_fachpruefung':'offen',
          'gespraech':'BESTAND.md#gesprächsverknüpfung'})
        if pos>1:edges.append({'from':order[pos-2],'to':key,'type':'technisch','basis':'aus learning_order abgeleitet','note':'Normaler Erstlernweg; Altfreigaben und bestehende Abschlüsse werden separat berücksichtigt.'})
        if guide:
            for p in guide['prerequisites']:edges.append({'from':p,'to':key,'type':'didaktisch','basis':'expliziter Guide; Paket '+str(guide.get('package',1)),'source':path+'/study_guide/prerequisites'})
            for p in guide.get('retrieves',[]):edges.append({'from':p,'to':key,'type':'wiederholung','basis':'späterer Abruf in Erklärung, Anwendungsaufgabe oder Lese-/Dialogkontext; keine Freigaberegel','source':path+'/study_guide/retrieves'})
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
              'erklaerte_falschantworten':len(profile['scenario'].get('feedback',{})) if profile else 0,
              'erfassung':'vollständig','inhaltsstatus':status,'menschliche_fachpruefung':'offen'})
    for name,rows in [('LERNZIELMATRIX.csv',matrix),('KARTENPRUEFUNG.csv',cards)]:
        with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    positions={k:i for i,k in enumerate(order)}
    assert len(order)==len(set(order))==len(raw)
    assert all(e['from'] in raw and e['to'] in raw and positions[e['from']]<positions[e['to']] for e in edges)
    (out/'VORAUSSETZUNGEN.json').write_text(json.dumps({'schema':1,'nodes':order,'edges':edges,'unknown':'Keine automatisierte Vollanalyse impliziter Sprachvoraussetzungen. 80 Guides, davon je 25 in Paket 02 und 03; technische Reihenfolge, didaktische Voraussetzungen und spätere Wiederholung sind getrennte Beziehungstypen. Keine zusätzliche Freischaltbedingung.'},ensure_ascii=False,indent=2)+'\n','utf-8')
    def md(name,text): (out/name).write_text(text.strip()+'\n','utf-8')
    counts=Counter(raw_jp);normcounts=Counter(normalize(x) for x in raw_jp)
    guided=[m for m in matrix if m['inhaltsstatus'].startswith('Paket')]
    package1=[m for m in guided if raw[m['lektion']][0]['study_guide'].get('package',1)==1]
    package2=[m for m in guided if raw[m['lektion']][0]['study_guide'].get('package')==2]
    package3=[m for m in guided if raw[m['lektion']][0]['study_guide'].get('package')==3]
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
    md('BESTAND.md',f'''# Kursbestand {d['content_version']} – Teststand Inhaltspaket 03

Ausgangscommit vor Umsetzung: `{BASE}`. Laufzeitquellen: `data/course.json`, `data/catalog.json`, `data/deep_lessons.json`; beide Plattformen verwenden diese Quellen. Android kopiert sie mit `mobile/tools/prepare_assets.py`, Windows mit `tools/stage_release.py`.

- {len(order)} Lektionen, {len(cards)} Karten, {sum(m['explizite_sprechziele'] for m in matrix)} explizite Sprechdatensätze; fehlende explizite Ziele bekommen einen Laufzeit-Fallback. {len(cat['TEACHERS'])} Lehrer.
- {len(counts)} unterschiedliche rohe japanische Kartenformen, {len(normcounts)} nach NFKC, Kleinschreibung sowie Entfernung von Leerraum und definierter Interpunktion. Hiragana und Katakana werden dabei nicht gleichgesetzt.
- {sum(v-1 for v in counts.values())} weitere Vorkommen bereits vorhandener roher Formen. Dopplungen bleiben bewusst erhalten und sind nicht automatisch Inhaltsfehler.
- Paket 01: {len(package1)} Lektionen / {sum(m['karten'] for m in package1)} Karten unverändert erhalten. Paket 02: {len(package2)} vorhandene Lektionen / {sum(m['karten'] for m in package2)} Karten tatsächlich überarbeitet. Paket 03: {len(package3)} Lektionen / {sum(m['karten'] for m in package3)} Karten überarbeitet. Zusammen {len(guided)} / {sum(m['karten'] for m in guided)}. Die übrigen {len(order)-len(guided)} Lektionen sind strukturell erfasst, nicht einzeln durchgesehen. Menschliche Fachabnahme bleibt für den gesamten Kurs offen.

## Zähl- und Prüfgrenzen

Eine Karte zählt je vorhandener Position, ein explizites Sprechziel je speech-Datensatz. Erstvorkommen bedeutet nur erste Karte im Lernweg; Beispiele, Hörtexte und Gesprächsformen können früher vorkommen. Es wird weder eine vollständige Vokabelliste noch eine geprüfte Ersteinführung aller sprachlichen Bestandteile behauptet. Ein Strukturtest ersetzt keine muttersprachliche Sprachprüfung und keine Anfänger-Erprobung.

## Gesprächsverknüpfung

Alle fünf tatsächlich vorhandenen Szenen, Knoten, Muster und Folgeknoten folgen. Funktionen sind ihre tatsächlichen Quelltextvorlagen; dadurch bleiben Platzhalter und alternative Zweige erkennbar. Die vollständige sprachliche Vorbereitung aller Antwortwege ist noch offen.

{chr(10).join(scene_text)}
''')
    md('LUECKEN_UND_SPRUENGE.md','''# Belegte Befunde und verbleibende Lücken

Stand: Paket 01 veröffentlicht mit 11.0.2, Paket 02 mit 11.0.4 und Paket 03 als Testversion 11.0.5; keine vollständige Fachabnahme.

| Priorität | Fundstelle | Befund am Ausgangsstand | Umsetzung / Rest |
| --- | --- | --- | --- |
| Hoch | lesson_ui.py: draw_lesson, _draw_study_content | Windows zeigte während Bedeutung, Schreiben und Abschlussrunde JP, Romaji und deutsche Lösung; ein Beispiel verriet zusätzlich die Bedeutung. | Vorlage nur beim Erklären oder nach bewusstem Hilfeaufruf; Beispiele nach Erfolg. Native UI geprüft. |
| Hoch | mobile/web/app.mjs: explanation, task; course.json: intro | Android zeigte die Lektions-Einführung nicht; vorhandene Kartenprofile waren standardmäßig eingeklappt. | Sichtbares Lernziel und Lernhilfen für 30 Lektionen; vorhandene intro-Texte der weiteren Lektionen sind jetzt erreichbar. |
| Hoch | 0:1:0 sowie v11:long-vowels, v11:small-tsu, v11:mora-n | Wörter setzen Kana voraus, deren systematische Reihen erst später kommen, z. B. さ in あさ. | Lokale Zeichenhilfen erklären benötigte neue Zeichen vor dem systematischen Drill. Reihenfolge unverändert. Dies ist eine didaktische Einschätzung, kein Syntaxfehler. |
| Mittel | v11:kata-basics bis v11:kata-combinations | Einsteiger benötigen weitere Katakana neben den frühen Grundreihen. | Zeichenhilfen, Längen, kleine Zeichen und Wortzerlegungen in den sechs Lektionen ergänzt. |
| Mittel | Kartenprofile: scenario.question | Viele Aufgaben fragten nur nach „dieser Karte“, obwohl die mobile Vorlage verborgen war. Manche Leseaufgaben zeigten ihren Ausgangstext nicht. | Einstieg: konkrete Bezüge plus 18 Situationsaufgaben. Generische übrige Aufgaben nennen ihre Form in der UI; Leseverständnis zeigt den JP-Text. Weitere Abwechslung bleibt offen. |
| Hoch | 14:0:1; 15:0; 16:0 | Frühe Beispiele benötigten u. a. Vergangenheit, Uhrzeit, Zimmer/Tisch oder Ortsgruppen vor deren systematischer Einführung. | Beispiel mit neuer Vergangenheit durch bekannten Existenzsatz ersetzt; lokales Vorwissen mit Lesung/Bedeutung vor dem Abruf erklärt. |
| Hoch | v11:languages:4; v11:directions:2–3; v11:smalltalk:4 | Laufende Tätigkeit und て-Bitten erscheinen vor den systematischen Verbform-Lektionen. | Ganze feste Formen ausdrücklich erklärt; keine selbstständige Herleitung vorausgesetzt. Späterer Abruf in Dialogen. |
| Hoch | study.py; mobile/web/core.mjs | Fehlversuche erklärten weder die gewählte Antwort noch die konkrete Verwechslung. | 121 Karten mit begründeten Anwendungsdistraktoren; Bedeutungs-/Hörfehler verwenden das tatsächlich gefragte Profil; gezielte Aufbau-/Schreibhilfe erst nach Versuch. |
| Mittel | 13:0:0 | Überblickskarte nani / nan verlangte beide Alternativen zusammen, obwohl eine Lesung genügt. | Einzelne Schreibvarianten sowie na-ni / nan als akzeptierte Sprechtexte ergänzt; vorhandenes Ziel unverändert. |
| Mittel | Legacy card.example; v11:read-profile | Alte Beispiele lagen als String statt als vom mobilen Renderer erwartetes Objekt vor; Leseintro versprach immer sichtbare Übersetzungen. | Betroffene Beispiele als JP/Romaji/DE-Objekt eingebunden; Leseintro beschreibt bewusste Hilfe korrekt. |
| Mittel | Android Session.answers, listen | Falsche Hör-Optionen konnten aus noch nicht bearbeiteten späteren Karten stammen. | Auswahl nun wie Windows nur aus den bis dahin eingeführten Karten. Sechs Schritte und Audiofreigabe unverändert. |

Die Daten enthalten viele sinnvolle eigene Erklärungen, Gegensatzpaare und bestehende Alltagsszenen. Erhalten: stabile IDs, sechs Android-Schritte mit echten Freigabebedingungen, getrennte Kana-Selbstprüfung, wiederholbare Karten und Offline-Gesprächswege. Die automatische Erkennung ist Textabgleich, keine Akzentnote.

Offen: eigene sprachliche Einzelprüfung der übrigen 70 Lektionen, menschliche Fachprüfung aller Lektionen und vollständige Vorbereitung sämtlicher Gesprächszweige. Die konkret verbesserten Verbindungen und verbleibenden Szenenlücken stehen in PAKET_02.md und PAKET_03.md. Paket 03 schließt die dort belegten Zahlen-/Bestelllücken mit 25 weiteren Einheiten, 29 Situationsaufgaben und erklärten Fehlantworten auf 119 Karten. Keine bloße Zählung wird als Schließung dieser Lücken ausgegeben.
''')
    package=['# Paket 01: tatsächlich umgesetzt','30 bestehende Lektionen vertieft, keine neue Lektions-ID. Gemeinsame Kursdaten werden in Windows und Android geladen. Alle ursprünglichen Kartenpositionen und Zieltexte bleiben erhalten.','Abnahme pro Lektion: Erklärungen vor bzw. während bewusster Hilfe erreichbar; sechs Schritte weiterhin lösbar; Voraussetzungsschlüssel gültig; muttersprachliche Prüfung und Anfänger-Erprobung noch offen.']
    for m in package1:
        l=raw[m['lektion']][0];g=l['study_guide']
        package.append(f"## {m['position']}. {m['titel']} (`{m['lektion']}`)\n\nArt: Überarbeitung. Position unverändert.\n\nZiel: {m['lernziel']}\n\nVoraussetzungen: {m['vorwissen'] or 'keine'}.\n\n"+'\n\n'.join(g['points'])+f"\n\nAbruf / Wiederholung: {g['recall']}\n\nÜbungen: bestehende sechs Schritte; situationsbezogene Ergänzungen siehe Kartenmatrix. Gesprächsbezug: Grundlagen für Kennenlernen; bei Aussprache und Schrift auch für alle weiteren Szenen. Eine vollständige Gesprächsvorbereitung wird daraus nicht abgeleitet.")
    md('PAKET_01.md','\n\n'.join(package))
    second=['# Paket 02: in Windows und Android umgesetzt, veröffentlicht mit 11.0.4',
      '25 bestehende Lektionen / 121 Karten. Keine neue Lektion nötig: vorhandene Einheiten bieten Platz für lokale Wort- und Mustererklärungen, Anwendung und spätere Wiederaufnahme. Keine Änderung an IDs, Kartenpositionen, learning_order, Kursrevision 11, Speicherschema oder Android FLOW_REVISION 2. Die ersten 30 Lektionen sind unverändert; ihr Inhalt und sämtliche Kartenidentitäten werden gegen einen gespeicherten 11.0.2-Vertrag getestet.',
      '## Auswahl anhand der Befunde',
      'Partikeln und Fragen an Position 31–41 werden gebraucht, bevor Orts- und Alltagssätze funktionieren. Position 54–58 setzt diese Markierungen in Handlungssätzen um. Zimmer/Positionen (62–63) und Richtungen (77) bereiten Standort und Wegbeschreibung vor. Smalltalk/Hobbys (86–87) bereiten echte Rückfragen beim Kennenlernen vor. Die späten Dialoge (130/133) und Lesetexte (135/136) geben diesen Formen eine spätere Anwendung. Zahlen-, Einkaufs- und andere Zwischenlektionen werden nicht nur wegen ihrer Position angefasst.',
      '## Konkrete Datenkorrekturen',
      'Kein japanischer Kartenzieltext, keine bestehende Lesung oder deutsche Kartenbedeutung wurde ersetzt. Korrigiert wurden didaktische Abhängigkeiten und Programmdarstellung: 14:0:1 ersetzt ein unnötig frühes Vergangenheitsbeispiel durch ねこがいます; die Objekt- und Besitzbeispiele verwenden bereits erklärten Wortschatz. Betroffene alte String-Beispiele werden als gemeinsames JP/Romaji/DE-Objekt lesbar. Bei 13:0:0 kommen zwei Schreibalternativen und ein zusätzliches Sprechziel mit akzeptierten Einzellesungen hinzu; alle alten Sprechziele bleiben erhalten. Die irreführende Aussage über dauerhaft sichtbare Lesetextübersetzungen wurde korrigiert.',
      '25 erste Karten besitzen neue gezielte Transferfragen. Auf allen 121 Karten haben Anwendungsdistraktoren eine Begründung. Bedeutung und Hören unterscheiden die ausgewählte Form vom Ziel; Hören verwendet das tatsächlich abgespielte Kartenprofil. Aufbau und Schreiben nennen passende Muster oder Stolperstellen. Begründungen erscheinen nach einer abgegebenen falschen Antwort, nicht als dauerhaft sichtbare Lösung. Bewusste Hilfe ist weiter möglich und erteilt weder Fortschritt noch XP.',
      '## Gesprächsraum als Bedarfsprüfung',
      '| Szene / Knoten | Vorbereitete Verbindung | Noch offen |\n| --- | --- | --- |\n| meeting / name, country | Paket 01: Name + です; Paket 02 dialog-meeting: どこからきましたか, ドイツからきました | Weitere Herkunftswörter Österreich/Schweiz; Kanji-Lesevarianten und vollständiges Verstehen aller Lehreraussagen |\n| meeting / hobby, ask | hobbies: おんがく・りょこう + がすきです; Rückfrage しゅみはなんですか; smalltalk: いいですね | Anime-Zweig und vollständige Bitte 私にも何か聞いてください sowie Abschiedsformulierungen sind nicht vollständig vorbereitet |\n| directions / destination, detail, right | here-there, directions, dialog-directions: Bahnhof/Toilette, Ortsfrage, geradeaus/rechts, Rückbestätigung; Lernhilfe für feste て-Bitten | Convenience-Store-Wort, vollständige Sequenz ～てから und sämtliche Hörvarianten noch nicht einzeln abgeglichen |\n| directions / time, thanks | Verständnisbestätigung, Dank; clock-minutes existiert außerhalb dieses Pakets | 歩いて何分・ぐらい, Begrüßungs-/Abschiedsformeln und jede alternative Route benötigen weitere Vorbereitung |\n| cafe, shopping, weekend | Allgemeine Partikel, Fragen, Orts- und Zeitmuster werden gefestigt | Temperatur/Größe, Mitnehmen, Zahlung, Wunschformen und Auswahlzweige bleiben Folgepakete; keine Vollabdeckung behauptet |',
      'Der Gesprächsraum bleibt Android-only. Keine Gesprächs-, Lehrer-, Modell- oder Audioänderung durch Paket 02.',
      '## Prüfgrenzen',
      'Erfassung: alle Kursquellen und acht ursprünglichen Berichte ausgewertet; Matrizen neu aus den veränderten Quellen erzeugt. Eigene sprachliche Durchsicht: alle ausgewählten Ziele, Guides, Kartenprofile, Beispiele und Aufgaben. Belegte Funktionsprobleme siehe LUECKEN_UND_SPRUENGE.md. Aussagen zu Natürlichkeit, Nuancen von は/が, Gesprächston und Angemessenheit sind keine muttersprachliche Abnahme. Menschliche Fachprüfung und Anfänger-Durchlauf offen. Automatische Tests und Build-Prüfungen stehen getrennt in TESTBERICHT_11.0.4.md; die öffentliche Prüfung in VEROEFFENTLICHUNG_11.0.4.md. TESTBERICHT_11.0.3_LOKAL.md bleibt der historische Nachweis des ersten lokalen Paketstands.']
    for m in package2:
        l=raw[m['lektion']][0];g=l['study_guide']
        second.append(f"## {m['position']}. {m['titel']} (`{m['lektion']}`)\n\n{m['karten']} bestehende Karten. Ziel: {m['lernziel']}\n\nVoraussetzungen: {m['vorwissen']}.\n\n"+'\n\n'.join(g['points'])+f"\n\nAbruf: {g['recall']}\n\nExplizite spätere Wiederaufnahme früherer Lektionen: {', '.join(g.get('retrieves',[])) or 'Abrufimpuls und bestehende Abschlussrunde'}.\n\nNeue Transferfrage: {l['cards'][0]['detail']['scenario']['question']}")
    md('PAKET_02.md','\n\n'.join(second))
    third=['# Paket 03 Zahlen Café und Einkaufen',
      '25 vorhandene Lektionen / 119 Karten, 75 Lernhilfe-Absätze und 29 gezielte Anwendungsaufgaben. Zusammen 80 Lektionen / 378 Karten selbst durchgesehen; keine menschliche Fachabnahme. Keine neue ID, kein Verschieben, Kursrevision 11 und Speicherschema unverändert. Die übrigen 125 Lektionen, darunter die bisherigen 55, sind über vollständige Lektionshashes gegen den Stand 11.0.4 geschützt.',
      '## Auswahl und behobene Befunde',
      'Zahlen 42–46 schließen die Voraussetzung für Stückzahl und Geldbetrag. Adjektive 60 bereiten Größe, Geschmack und Verneinung vor. Lebensmittel und Einkauf 66–76 verbinden Ware, Wunsch und Zahlung. Reiseanwendungen 78–81 greifen Kauf, Ortsfragen und Hilfsbitten wieder auf; hier standen zuvor unerklärte feste Verbformen und Karten-/Uhrzeitbegriffe. Die Wunschformen 105–106 und Dialoge 131–132 dienen dem späteren Abruf. Dies ist keine bloße Folge von 25 Kurspositionen.',
      'Belegt am Ausgangsstand: Für diese 25 Lektionen fehlten explizite study_guide-Voraussetzungen und begründete scenario.feedback-Falschantworten. Mengen- und Caféaufgaben benötigten nicht systematisch vorbereitete Orts-, Größen- und Zahlungswahl. 17:0 enthielt alte String-Beispiele, die Android nicht als gemeinsames Beispielobjekt auswertete. Diese sind jetzt JP/Romaji/DE-Objekte mit gleichem Text. Es werden keine weiteren sprachlichen Kartenkorrekturen behauptet; Zieltexte, Bedeutungen und Lesungen bleiben erhalten.',
      '## Grenzen und Gesprächswege',
      'Automatisch geprüfte gelehrte Antworten: Café Wasser → hier → bar; Kaffee → kalt → L → Mitnehmen → Karte. Einkauf Preisfrage → Kauf → Schwarz → Karte sowie Preisfrage → Absage. Die Szene akzeptiert keine freie Konversation: Mengenwörter bei der ersten Bestellung und Größe M sind dort nicht vorgesehen, obwohl sie Kursübungen bleiben. Die Lernhilfe grenzt das ausdrücklich ab. Temperaturantworten verwenden die von der Szene unterstützte Form mit を. Gesprächscode und Sprachmodelle bleiben unverändert.',
      'Offen bleiben vollständiges Verstehen aller Serviceäußerungen, weitere Gesprächsvarianten, Natürlichkeit der Höflichkeitsformeln, die kontextabhängige Ablehnung mit だいじょうぶ, Partikelnuancen, Aussprachehilfen und die kognitive Belastung der frühen Zahlen-Sammelkarte. Eigene Durchsicht ist keine muttersprachliche Abnahme. Menschliche Sprachprüfung, Anfänger-Erprobung und echte Mikrofon-/Hörtests stehen aus.',
      'Punktueller Primärquellenabgleich: Japan Foundation, Irodori Starter Lektion 6 (https://www.irodori.jpf.go.jp/assets/data/starter/pdf/X_L06.pdf), S. 4–5: Bestellung, Größen und Verzehrort. Lehrtexte und Beispiele wurden eigenständig formuliert; keine vollständige externe Validierung. Der Abruf des vollständigen PDFs Lektion 16 scheiterte; es wird nicht als vollständig geprüfte Quelle gezählt.',
      '## Konkrete Lektionen']
    for m in package3:
        l=raw[m['lektion']][0];g=l['study_guide']
        third.append(f"## {m['position']}. {m['titel']} (`{m['lektion']}`)\n\n{m['karten']} Karten. Lernziel: {m['lernziel']}\n\nVoraussetzungen: {m['vorwissen']}.\n\n"+'\n\n'.join(g['points'])+f"\n\nAbruf: {g['recall']}\n\nSpätere Wiederaufnahme: {', '.join(g.get('retrieves',[])) or 'Abrufimpuls und Abschlussrunde'}.\n\nAnwendung: {l['cards'][0]['detail']['scenario']['question']}")
    md('PAKET_03.md','\n\n'.join(third))
    md('AUSBAUPLAN.md','''# Weiterer Ausbau nach Paket 03

Paket 01, 02 und 03 sind in gemeinsamen Kursdaten und beiden Programmen umgesetzt. Paket 03: 25 bestehende Lektionen / 119 Karten als Testversion 11.0.5 veröffentlicht; keine neue ID, Reihenfolge- oder Speichermigration. Die ausgewählten Lücken ließen sich in bestehenden Einheiten schließen. 150 Lektionen bleiben 150; zusätzliche Lektionen sind kein Abnahmekriterium. Paket 04 und 05 sind weiterhin Planung.

| Folgepaket | Ziel / Position | Umfang als Planung | Erklärungen und Übungen | Gespräch / Abnahme |
| --- | --- | --- | --- | --- |
| 02: Satzbau und Rückfragen – veröffentlicht | Positionen 31–41, 54–58, 62–63, 77, 86–87, 130, 133, 135–136 | 25 Überarbeitungen, 121 Karten, keine neue Lektion | 75 Guide-Absätze, 25 zusätzliche Transferfragen, Fehlantwortbegründungen und spätere Wiederaufnahme | Kennenlernen, einfache Ortsfrage und Wegverständnis verbessert; nicht alle Gesprächszweige abgedeckt, menschliche Abnahme offen |
| 03: Einkaufen, Café und Reiseanwendungen – umgesetzt | 42–46, 60, 66–76, 78–81, 105–106, 131–132 | 25 vorhandene Lektionen / 119 Karten; keine neue ID | 75 Lernhilfe-Absätze, 29 gezielte Anwendungsaufgaben und erklärte Fehlantworten | Je zwei konkrete Café-/Einkaufswege mit gelehrten Antworten automatisch geprüft; vollständiges Hörverständnis und menschliche Abnahme offen |
| 04: Zeit und Verabredungen | Auf Zeitangaben, Verben und Einladungen aufbauen | 15–25 Überarbeitungen; 0–5 Ergänzungen bei nachgewiesenen Lücken | Tag/Uhrzeit/Treffpunkt austauschen, Alternativen anbieten, später erneut abrufen | Wochenendszene; menschliche Sprachprüfung und Anfänger-Durchlauf |
| 05: Lesen und Wiederholen | Über mehrere Kapitel verteilt, nach den jeweiligen Formen | 10–20 bestehende Lektionen prüfen; neue Anzahl offen | Kurze ungesehene Texte mit bekanntem Wortschatz; zeitlich versetzter Abruf und echte Verständnisfragen | Inhalt beantworten statt Vorlage kopieren; jede falsche Auswahl begründbar |

Die Spannen sind Planungsannahmen, keine vollständig spezifizierten Zusatzlektionen. Alle Pakete betreffen die gemeinsamen Kursdaten und beide Oberflächen; Offline-Gespräche bleiben zunächst Android-Funktion. Neue IDs nur für wirklich neue Inhalte, keine Neunummerierung alter Fortschritte. Voraussetzungsketten werden vor neuen Aufgaben geprüft. Wiederholung ist keine harte Freischaltbedingung.

Fachliche Abnahme: muttersprachliche Person prüft Natürlichkeit, Bedeutungen und Höflichkeit; Anfänger-Durchlauf prüft Verständlichkeit ohne externe Hilfe. Geräteabnahme: echte Stimme/Mikrofon/Lautsprecher am S24 Ultra und Windows, einschließlich Update über die vorhandene Installation. Automatische Modelltests ersetzen diese Schritte nicht.
''')
    md('PRUEFBERICHT.md',f'''# Struktureller Prüfbericht

{len(matrix)} eindeutige Lektionszeilen und {len(cards)} eindeutige Kartenzeilen; vollständige Abdeckung der tatsächlichen Kursquellen. {len(edges)} getrennt typisierte Beziehungen; alle Ziele vorhanden, alle hier explizit modellierten Voraussetzungskanten zeigen auf eine frühere Lektion und sind damit zyklenfrei. Unbekannte implizite Voraussetzungen bleiben unbekannt.

Erfassung: alle 150 Lektionen / 680 Karten. Eigene sprachliche Durchsicht und Überarbeitung: 80 Lektionen / 378 Karten (Paket 01: 30/138, Paket 02: 25/121, Paket 03: 25/119). Vollständige fachliche Prüfung aller 150 Lektionen: **nicht abgeschlossen**. Menschliche Sprach- und Anfängerprüfung: **nicht ausgeführt**. Automatische Programmtests sind getrennt im technischen Testbericht dokumentiert und keine Sprachabnahme.

Export: `python tools/audit_course.py --output <Zielordner>`. Fachliche Ausgaben enthalten keine Laufzeitstempel. Gleiche Eingabedateien einschließlich redaktioneller Guides und dieses Skripts ergeben dieselben Berichte. Aktuelle Paket-3-Prüfungen stehen in `TESTBERICHT_11.0.5_TEST.md`; die öffentliche Kontrolle der stabilen Ausgabe bleibt in `VEROEFFENTLICHUNG_11.0.4.md`; Berichte für 11.0.2 und den lokalen Stand 11.0.3 bleiben historische Evidenz.

Die Lehrtexte wurden eigenständig formuliert. Abgleich einzelner Schrift-/Leseregeln mit [Kana-Übersicht der Japan Foundation](https://www.irodori.jpf.go.jp/assets/data/Kana_all.pdf), Vorstellungen mit [Irodori Starter, Lektion 3](https://www.irodori.jpf.go.jp/assets/data/starter/pdf/X_L03.pdf). Diese Stichproben sind keine komplette externe Kursvalidierung.

## Eingabefingerabdrücke (SHA-256)

```json
{json.dumps(hashes,indent=2)}
```
''')
    print(json.dumps({'lessons':len(matrix),'cards':len(cards),'reviewedLessons':len(guided),'reviewedCards':sum(m['karten'] for m in guided),'scenes':len(scenes),'nodes':sum(len(s['nodes']) for s in scenes),'edges':len(edges)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);export(p.parse_args().output)
