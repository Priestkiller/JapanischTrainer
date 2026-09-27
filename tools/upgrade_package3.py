"""Authored package 03: shared production content, stable IDs/order, no migration.

Own linguistic review, not human expert approval. Run after packages 01 and 02.
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = {}
APPLICATIONS = {}

def guide(key, prerequisites, goal, points, recall, build, retrieves=''):
    GUIDES[key] = dict(goal=goal, study_guide=dict(revision=1, package=3,
        prerequisites=prerequisites.split(), points=points, recall=recall,
        retrieves=retrieves.split()), build=build)

def task(key, index, question, correct, wrong):
    APPLICATIONS[(key,index)] = dict(question=question, correct=correct,
        wrong=list(wrong), feedback=wrong, explanation='Zur Situation passt: '+correct)

guide('12:0','0:0 v11:small-ya',
 'Die Zahlen eins bis zehn den richtigen Werten zuordnen und die Sammelkarte als Zahlenfolge lesen.',[
 'Zahlenreihe: いち ichi = 1, に ni = 2, さん san = 3, よん yon = 4, ご go = 5. Auf der letzten Karte folgen außerdem ろく roku = 6, なな nana = 7, はち hachi = 8, きゅう kyū = 9, じゅう jū = 10. Die Punkte trennen Zahlen; sie werden nicht gesprochen.',
 'Hier sind es reine Zahlen, noch keine Stückzahlen, Uhrzeiten oder Altersangaben. Alternative Lesungen wie し shi für 4 und しち shichi für 7 kommen in bestimmten Verbindungen vor. Übe auf diesen Karten zunächst die angegebene Reihe; die nächste Lektion trennt 6 bis 10 in Einzelkarten.',
 'Aussprache: ち ist chi, ん bekommt einen eigenen Takt. In kyū und jū ist ū lang; kleines ゅ gehört zum vorherigen Zeichen. Eine Zahlenfolge wird langsam gelernt und dann ohne Vorlage abgerufen. です desu im Beispiel macht eine höfliche Antwort: にです, es ist zwei.'
 ],'Zähle von eins bis fünf. Welche Zahl steht zwischen drei und fünf?',
 'Bei der Sammelkarte bleibt die Reihenfolge fünf bis zehn; die Trenner sind keine Wörter.')
guide('v11:numbers-six-ten','12:0',
 'Sechs bis zehn einzeln erkennen und beim Abruf sicher auseinanderhalten.',[
 'Die Sammelreihe wird zerlegt: ろく roku 6, なな nana 7, はち hachi 8, きゅう kyū 9 und じゅう jū 10. Jede Karte prüft jetzt genau eine Zahl; sage nicht die ganze Reihe.',
 'Die Beispiele Zahl + です nennen nur den Wert. Sie beantworten keine Frage nach Stückzahl oder Uhrzeit. きゅう und じゅう unterscheiden sich schon im ersten Laut: k gegenüber stimmhaftem j.',
 'Sprich ro-ku und ha-chi mit zwei Takten. kyū und jū haben jeweils einen langen Vokal; na-na hat zwei kurze a. Lies eine zufällig gewählte Ziffer und prüfe dich erst danach an der Vorlage.'
 ],'Rufe zuerst 4 und 5 ab, dann 8 und 9. Welche zwei Formen haben ein langes ū?',
 'Eine Zahl pro Karte; die höfliche Endung gehört nur zu einem vollständigen Beispielsatz.','12:0')
guide('v11:numbers-eleven','v11:numbers-six-ten',
 '11, 15, 20, 21 und 99 nach dem Zehner-Einer-Muster unterscheiden.',[
 'じゅう jū heißt zehn. Danach steht ein zusätzlicher Einer: じゅういち jūichi = 11, じゅうご jūgo = 15. Eine Zahl davor zählt die Zehner: にじゅう nijū = 20.',
 'にじゅういち nijūichi ist 2 × 10 + 1. きゅうじゅうきゅう kyūjūkyū ist 9 × 10 + 9. Die Reihenfolge geht von groß nach klein, anders als beim deutschen einundzwanzig. Die Nullstelle wird nicht extra gesprochen.',
 'Lange ū bleiben auch in zusammengesetzten Zahlen hörbar. Trenne beim Lernen nach Bedeutung: ni-jū-ichi. Das ist eine Merkhilfe, kein Auftrag, zwischen allen Teilen lange Pausen zu machen. Die Beispiele ergänzen nur das bekannte です.'
 ],'Vergleiche 11 und 21. Was ändert die zusätzliche Zwei vor zehn?',
 'Zahl der Zehner – zehn – Einer; eine Eins vor zehn wäre hier keine Elf.','12:0 v11:numbers-six-ten')
guide('v11:numbers-hundreds','v11:numbers-eleven v11:small-tsu',
 '100, 300, 600, 1.000 und 10.000 lesen und in einem Yen-Preis erkennen.',[
 'ひゃく hyaku = 100, せん sen = 1.000; まん man bezeichnet 10.000 und erhält hier いち: いちまん ichiman. Neu im Beispiel: えん en ist die japanische Bezeichnung für Yen. Zahl + えん + です nennt einen Preis.',
 'Lautwechsel als ganze Formen lernen: さんびゃく sanbyaku = 300, ろっぴゃく roppyaku = 600. Bei roppyaku gehört die kurze Verschlusspause zum p. Für spätere Preise außerdem: にひゃく nihyaku = 200, ごひゃく gohyaku = 500, さんぜん sanzen = 3.000.',
 'Größere Stellen kommen zuerst: せんにひゃく sen nihyaku = 1.200. Nicht jede Kombination ist regelmäßig; hier werden nur ausdrücklich erklärte Zahlen verlangt. hyaku enthält kleines ゃ; sanzen hat stimmhaftes z, kein deutsches ts.'
 ],'Lies gedanklich 300 Yen und 600 Yen. Welcher Betrag hat eine Pause vor p?',
 'Erst die größere Zahlstelle, dann die kleinere; えん folgt dem ganzen Betrag.','v11:numbers-eleven')
guide('v11:count-objects','v11:numbers-six-ten',
 'Ein bis fünf Stück bestellen und die allgemeinen Zählformen von Grundzahlen unterscheiden.',[
 'Allgemeine Stückzahlen: ひとつ hitotsu 1, ふたつ futatsu 2, みっつ mittsu 3, よっつ yottsu 4, いつつ itsutsu 5. Diese Formen sind keine frei gebildete Kombination aus Grundzahl und tsu.',
 'ください kudasai ist hier bitte geben Sie mir. ふたつください bestellt zwei Stück einer schon bekannten Ware. Später kannst du die Ware nennen: Ware + を + Stückzahl + ください. Für Menschen, Uhrzeit oder Geld benutzt man andere Formen.',
 'みっつ und よっつ enthalten eine kurze Pause; いつつ hat drei Takte i-tsu-tsu. Eine Bestellung von zwei Stück sagt noch nichts über den Preis. Merke dir Zahl und Verwendungsbereich zusammen.'
 ],'Erinnere dich an に = 2. Wie sagst du stattdessen zwei Stück, bitte?',
 'Ware – を – Stückzahl – ください; bei bekannter Ware darf nur Stückzahl + ください stehen.','12:0')
guide('17:0','2:0 v11:this-noun',
 'Eigenschaften mit い- und な-Adjektiven beschreiben und nicht teuer erkennen.',[
 'おおきい ōkii = groß, おいしい oishii = lecker; beide enden auf い. しずか shizuka = ruhig ist ein な-Adjektiv. Neue Beispielwörter: いぬ inu Hund, ラーメン rāmen Ramen-Nudeln, まち machi Stadt, たかい takai teuer oder hoch.',
 'Vor einem Nomen: おおきいいぬ großer Hund; しずかなまち ruhige Stadt. Das な verbindet nur das な-Adjektiv mit dem Nomen. Als höfliche Aussage: しずかです. Nicht jedes Wort auf i ist deshalb automatisch ein い-Adjektiv.',
 'Hier wird die Verneinung von たかい erklärt: Schluss-い durch くない ersetzen → たかくない; mit です höflich nicht teuer. Bei ōkii sind ō und ii lang, bei oishii nur das abschließende ii. Die Aufgaben verlangen noch keine übrigen Adjektivformen.'
 ],'Beschreibe einen großen Hund und eine ruhige Stadt. In welcher Verbindung brauchst du な?',
 'い-Adjektiv direkt vor Nomen; な-Adjektiv mit な. Die Verneinung endet auf くないです.')
guide('v11:staples','5:0 14:0',
 'Fünf Grundnahrungsmittel benennen und im Muster etwas essen verstehen.',[
 'ごはん gohan meint gekochten Reis oder eine Mahlzeit. パン pan Brot, にく niku Fleisch, さかな sakana Fisch, たまご tamago Ei. Rohes Reiskorn heißt gewöhnlich こめ kome; das ist hier keine Pflichtantwort.',
 'Bekannt: を o markiert das Objekt, たべます tabemasu heißt essen. ごはんをたべます bedeutet hier ich esse Reis. Ein Nomen enthält ohne Kontext weder eine bestimmte Stückzahl noch eine feste Einzahl-/Mehrzahl-Angabe.',
 'Pan endet auf einen eigenen n-Takt; ta-ma-go hat drei Takte. Fisch kann Tier oder Lebensmittel sein, die Essenshandlung klärt den Kontext. Sage zunächst den Namen des Lebensmittels, anschließend den ganzen Satz.'
 ],'Wiederhole を aus Essen und Trinken. Tausche Reis gegen Brot, ohne das Verb zu ändern.',
 'Lebensmittel – を – たべます; das Objekt steht vor dem Verb.','5:0')
guide('v11:fruit-veg','v11:staples v11:count-objects',
 'Obst und Gemüse sowie drei konkrete Lebensmittel unterscheiden und einen Kauf ausdrücken.',[
 'やさい yasai = Gemüse, くだもの kudamono = Obst. りんご ringo Apfel, みかん mikan Mandarine und トマト tomato Tomate sind konkrete Lebensmittel. Eine Kategorie benennt noch keine einzelne Sorte.',
 'Neu: かいます kaimasu heißt kaufe; das Grundverb ist かう kau. Mit bekanntem を: りんごをかいます, ich kaufe Äpfel. Das sagt allein weder drei Äpfel noch einen Preis. Für zwei Stück kannst du das bekannte ふたつ verwenden.',
 'Rin-go und mi-ka-n behalten den n-Takt. ト・マ・ト sind drei große Katakana. Unterscheide beim Antworten: Was wird gekauft, wie viel davon oder wie viel kostet es? Diese Lektion prüft zuerst die Ware.'
 ],'Bestelle zwei Äpfel mit dem bekannten Stückwort und ください. Erinnere dich an die Wortfolge Ware – を – Menge.',
 'Ware – を – かいます; Stückzahl und Kaufverb erfüllen verschiedene Aufgaben.','v11:count-objects v11:staples')
guide('v11:drinks','5:0 v11:count-objects v11:kata-long',
 'Fünf Getränke benennen und mit をください bestellen.',[
 'みず mizu Wasser, おちゃ ocha Tee, コーヒー kōhī Kaffee, ぎゅうにゅう gyūnyū Milch und ジュース jūsu Saft beziehungsweise süßes Kaltgetränk. ジュース bedeutet nicht zwingend reinen Fruchtsaft.',
 'をください o kudasai verbindet das Getränk mit einer Bitte: みずをください, Wasser bitte. ひとつ hitotsu ergänzt eine Portion: コーヒーをひとつください. Die Mengenangabe bestimmt nicht automatisch eine Bechergröße.',
 'Kōhī hat zwei lange Vokale, gyūnyū ebenfalls; jūsu hat langes ū. In mizu ist z stimmhaft, nicht deutsches ts. お in おちゃ gehört zum üblichen Wort. Bestellen und nur den Getränkenamen nennen sind unterschiedliche Aufgaben.'
 ],'Bestelle erst Wasser, dann zwei Portionen Kaffee. Rufe das Stückwort aus der Mengenlektion ab.',
 'Getränk – を – gegebenenfalls Menge – ください.','v11:count-objects 5:0')
guide('v11:taste','17:0 v11:drinks',
 'Süß, scharf, lecker, heiß und kalt als Geschmack oder Temperatur unterscheiden.',[
 'あまい amai süß, からい karai scharf, おいしい oishii lecker, あつい atsui heiß und つめたい tsumetai kalt. Neue Beispielwörter: ケーキ kēki Kuchen, りょうり ryōri Gericht, とても totemo sehr. Warm, weniger stark als heiß, heißt あたたかい atatakai.',
 'Mit bekanntem は … です: おちゃはあついです, der Tee ist heiß. からい beschreibt hier die Schärfe, nicht die Temperatur. つめたい passt zu einem kalten Getränk; kaltes Wetter hätte ein anderes Wort.',
 'Alle fünf Kartenwörter sind い-Adjektive. Bei oishii bleibt das abschließende ii lang; atsui hat a-tsu-i. Für die spätere Bestellung: ホット hotto nennt die heiße/warm servierte Variante, アイス aisu die gekühlte Variante; アイス bedeutet im Café nicht automatisch Speiseeis.'
 ],'Beschreibe kaltes Wasser und scharfes Essen. Warum kannst du scharf nicht einfach für heiß einsetzen?',
 'Eigenschaft vor です; Geschmack und Temperatur sind verschiedene Informationen.','17:0 v11:drinks')
guide('v11:food-preferences','v11:staples v11:taste v11:polite-past',
 'Vorliebe, Essensverzicht, Weglassen, nicht scharf und Lob nach dem Essen auseinanderhalten.',[
 'すし sushi Sushi; すきです suki desu bedeutet mögen. Das Gemochte steht hier vor が: すしがすきです. にくはたべません setzt Fleisch als Thema und sagt esse ich nicht; es nennt keinen Grund für den Verzicht.',
 'ねぎ negi sind hier Frühlingszwiebeln/Laucharten. ぬきで nuki de = ohne, bitte weglassen; おねがいします onegai shimasu macht die Bitte vollständig. もの mono heißt Sache/etwas. からい wird wie たかい zu からくない: からくないもの, etwas nicht Scharfes.',
 'Neu erklärte Vergangenheit eines い-Adjektivs: Schluss-い durch かった ersetzen. おいしい → おいしかったです, es war lecker. Nicht einfach でした an おいしい hängen. Sprich ne-gi kurz, das ii in oishii lang; in oishikatta gehört die Pause vor t dazu.'
 ],'Nach der Mahlzeit loben: Welche Form berichtet rückblickend? Wiederhole danach die Verneinung nicht teuer und bilde nicht scharf.',
 'Vorliebe mit が; Verzicht als Thema mit は; Bitte um Weglassen mit ぬきで.','17:0 v11:taste v11:staples')
guide('6:0','v11:drinks v11:count-objects v11:numbers-hundreds',
 'Im Café bestellen, nach dem Preis fragen und danken; Mitnehmen von Vor-Ort unterscheiden.',[
 'Wiederholung: コーヒーをください bestellt Kaffee. これ kore ist das hier; いくら ikura fragt nach dem Preis. これはいくらですか heißt wie viel kostet das hier? ありがとうございます bedankt sich höflich. Ein Preis endet auf えん en, nicht auf つ.',
 'Vor der Anwendung: ここで koko de heißt hier/vor Ort; もちかえりで mochikaeri de heißt zum Mitnehmen. Beides kann mit おねがいします onegai shimasu als Bitte enden. てんない tennai heißt im Laden; 店内 und 持ち帰り sind die Schreibungen für diese zwei Wahlmöglichkeiten.',
 'Die Servicefrage こちらでおめしあがりですか (kochira de omeshiagari desu ka) fragt höflich nach dem Verzehr hier. Du brauchst diese Höflichkeitsform noch nicht selbst abzuleiten. Antworte mit der erklärten Ortswahl. Arigatō hat langes ō; mochikaeri bleibt mo-chi-ka-e-ri.'
 ],'Bestelle Kaffee zum Mitnehmen. Wiederhole dazu zuerst die bekannte Ortsmarkierung で.',
 'Getränk – を – ください; die Ortswahl ist eine eigene Antwort, keine Mengenangabe.','v11:drinks v11:count-objects 15:0')
guide('v11:shop-prices','6:0 v11:numbers-hundreds 17:0 v11:this-noun',
 'Nach einem Preis fragen, 500 und 1.200 Yen lesen und teuer/günstig unterscheiden.',[
 'いくらですか fragt nach dem Preis eines bekannten Produkts. このほん kono hon dieses Buch, このペン kono pen dieser Stift, このかばん kono kaban diese Tasche verwenden bekannte Nomen und Zeigewörter.',
 'ごひゃくえん gohyaku en = 500 Yen; せんにひゃくえん sen nihyaku en = 1.200 Yen: 1.000 + 200. Wiederhole die früher eingeführten Zahlenbausteine. Alle Beträge sind erfundene Übungspreise.',
 'やすい yasui heißt hier günstig, たかい takai teuer. Ein Urteil über den Preis ist keine Frage nach dem Betrag. En beginnt ohne y; bei hyaku verbinden kleines ゃ und vorheriges Zeichen den Laut hya.'
 ],'Vergleiche 300, 500 und 1.200 Yen. Frage danach nach dem Preis dieser Tasche.',
 'Gegenstand – は – いくらですか; Betrag – えん – です für die Antwort.','v11:numbers-hundreds v11:this-noun')
guide('v11:shop-choice','v11:shop-prices v11:existence',
 'Ansehen, Kaufen, eine Alternative und Weiterüberlegen im Einkauf unterscheiden.',[
 'みせてください misete kudasai = bitte zeigen; これにします kore ni shimasu = ich entscheide mich dafür. ほか hoka anderes + の + もの mono Sache wird ほかのもの, etwas anderes; ありますか fragt nach dessen Verfügbarkeit.',
 'みているだけです mite iru dake desu = ich schaue nur. みている beschreibt gerade schauen, だけ begrenzt auf nur. もうすこし mō sukoshi noch ein wenig + かんがえます kangaemasu überlegen. Diese längeren Formen werden als erklärte Wendungen gelernt; eigene て-Bildung folgt später.',
 'Für den späteren Gesprächszweig: やめておきます yamete okimasu bedeutet hier ich lasse es lieber, eine Absage an den Kauf. Das ist keine Zusage. Mō hat langes ō; in misete und mite sind die Formen verschieden: zeigen gegenüber selbst schauen.'
 ],'Ein Angebot ist zu teuer: Frage nach etwas anderem oder sage ab. Unterscheide das vom Kauf mit これにします.',
 'を vor zeigen; に vor sich entscheiden. Nur anschauen bestätigt noch keinen Kauf.','v11:this-that v11:shop-prices')
guide('v11:clothes','v11:kata-combinations v11:fruit-veg',
 'Kleidung, Hemd, Hose, Schuhe und Mantel benennen und als Kaufgegenstand verwenden.',[
 'ふく fuku Kleidung ist der Sammelbegriff. シャツ shatsu Hemd, ズボン zubon Hose, くつ kutsu Schuhe und コート kōto Mantel benennen konkrete Arten. Die Nomen tragen keine eigene deutsche Pluralendung.',
 'Das bekannte Muster Ware + を + かいます gilt auch hier: くつをかいます, ich kaufe Schuhe. Es sagt noch nichts über Farbe oder Größe. Diese Eigenschaften kommen in der folgenden Lektion hinzu.',
 'In シャツ bildet kleines ャ mit シ sha; großes ツ ist ein eigener tsu-Takt. Zubon endet auf n, kōto hat langes ō. Nicht die deutsche oder englische Aussprache der Lehnwörter übernehmen.'
 ],'Rufe Kaufen aus der Obstlektion ab. Setze nun Hemd statt Apfel ein.',
 'Kleidungswort – を – かいます.','v11:fruit-veg')
guide('v11:size-color','17:0 v11:clothes v11:shop-choice',
 'Vier Farben beschreiben, eine Größe erfragen und S/M/L als Auswahl verstehen.',[
 'あかい akai rot, あおい aoi blau, しろい shiroi weiß, くろい kuroi schwarz stehen direkt vor einem Nomen. Als Farbnamen ohne Nomen: あか aka, あお ao, しろ shiro, くろ kuro. 赤・青・白・黒 sind ihre Kanji; in dieser Auswahlhilfe stehen Lesungen bereit.',
 'サイズ saizu Größe; おおきいサイズ ōkii saizu große Größe. ありますか fragt nach Verfügbarkeit. Für Cafégrößen: S = エス esu klein, M = エム emu mittel, L = エル eru groß. エムサイズでおねがいします (emu saizu de onegai shimasu) bestellt die mittlere Größe.',
 'Die Farbauswahl くろをおねがいします (kuro o onegai shimasu) bedeutet schwarz bitte. あおがいいです (ao ga ii desu) heißt ich hätte gern blau. A-o-i hat drei Vokaltakte, ōkii zwei lange Vokale. Größe und Anzahl sind unabhängig: zwei Becher können beide klein sein.'
 ],'Nenne schwarze Schuhe. Wähle danach im Café Größe M, ohne eine Stückzahl daraus zu machen.',
 'Farbadjektiv direkt vor Nomen; der Farbname kann selbstständig vor を stehen.','17:0 v11:clothes v11:count-objects')
guide('v11:checkout','v11:shop-choice v11:size-color 15:0',
 'Zahlungsart, Tütenfrage und Bonwunsch verstehen und eine eindeutige Antwort auswählen.',[
 'カード kādo Karte, げんきん genkin Bargeld, ふくろ fukuro Tüte, レシート reshīto Kassenbon. で markiert das Zahlungsmittel. いいですか fragt ob es geht; おねがいします äußert eine Bitte. いります irimasu heißt brauchen, anders als います imasu, da sein.',
 'Für die Gespräche: おしはらい oshiharai Zahlung; おしはらいはどうなさいますか (oshiharai wa dō nasaimasu ka) fragt höflich nach der Zahlungsweise. はらいます haraimasu = bezahle. げんきんではらいます = ich zahle bar; カードでおねがいします = mit Karte bitte.',
 'だいじょうぶです daijōbu desu ist ohne Situation mehrdeutig. Hier: Nach der Tütenfrage lehnt ふくろはだいじょうぶです eine Tüte ab. Eindeutiger wäre いいえ、いりません (iie, irimasen), nein, brauche ich nicht. Lange Vokale in kādo, reshīto und daijōbu beibehalten.'
 ],'Wiederhole で als Mittel. Antworte auf eine Zahlungsfrage mit Karte und auf die Tütenfrage mit einer Absage.',
 'Zahlungsart – で – Bitte; Tüte – は – Antwort auf den Bedarf.','15:0 6:0 v11:shop-choice')
guide('v11:transport','v11:location-action v11:here-there',
 'Bahn, U-Bahn und Haltestelle unterscheiden sowie Einsteigen und Aussteigen verstehen.',[
 'でんしゃ densha Zug/Bahn, ちかてつ chikatetsu U-Bahn, バスてい basutei Bushaltestelle. バス basu ist das Fahrzeug, nicht die Haltestelle. Die bekannten Muster …でいきます und …はどこですか beschreiben Fahrtmittel oder fragen nach einem Ort.',
 'のります norimasu heißt hier einsteigen/mitfahren, おります orimasu aussteigen. In den Beispielen steht バスにのります für in den Bus steigen und バスをおります für aus dem Bus steigen. を markiert hier das Verlassen, nicht einen gegessenen Gegenstand.',
 'Densha enthält kleines ゃ; chikatetsu endet auf tsu. Für eine Ticketfrage musst du zuerst das Verkehrsmittel und das Reiseziel auseinanderhalten. Hier werden nur die fünf Kartenformen und die erklärten Beispiele geprüft.'
 ],'Vergleiche バスでいきます und バスにのります. Welcher Satz nennt das Einsteigen?',
 'Verkehrsmittel – に – einsteigen; Verkehrsmittel – を – aussteigen.','v11:location-action')
guide('v11:station','v11:transport v11:numbers-six-ten v11:fruit-veg',
 'Fahrkartenkauf, Gleisfrage, nächste Station, Fahrtziel und Umsteigen unterscheiden.',[
 'きっぷ kippu Fahrkarte; をかいます ist das bekannte Kaufen. なんばんせん nanbansen fragt welches Gleis: なん welche Nummer + ばんせん nummeriertes Gleis. Eine mögliche Antwort ist にばんせん nibansen, Gleis zwei; das ist kein Preis.',
 'つぎ tsugi nächste + の + えき eki Station = nächste Station. とうきょう Tōkyō Tokio + まで made bis = bis Tokio. ここでのりかえます (koko de norikaemasu) heißt hier steige ich um; で ist der Ort der Handlung.',
 'Kippu enthält eine Pause vor p, Tōkyō zwei lange ō. Beim Ticketkauf kann とうきょうまでおねがいします das Ziel nennen. Für Preis oder Menge nutzt du die bereits erklärten Formen; まで ist keine Preis- oder Mengenmarkierung.'
 ],'Kaufe gedanklich eine Fahrkarte bis Tokio. Frage anschließend nach Gleis zwei und unterscheide dies von zwei Stück.',
 'Ziel – まで – Bitte; Ort – で – umsteigen.','v11:count-objects v11:shop-prices v11:transport')
guide('v11:hotel','v11:rooms v11:checkout v11:clock-hours',
 'Reservierung, Einchecken, Schlüsselwunsch, Frühstückszeit und WLAN-Frage verstehen.',[
 'よやく yoyaku Reservierung; よやくしています yoyaku shite imasu heißt hier ich habe eine Reservierung. チェックイン chekkuin Einchecken, かぎ kagi Schlüssel, あさごはん asagohan Frühstück, ワイファイ waifai WLAN. へやのかぎ = Zimmerschlüssel.',
 'Die bekannten Bitten mit おねがいします oder ください passen zum Einchecken beziehungsweise Schlüssel. なんじ nanji fragt wie viel Uhr, anders als いくら nach dem Preis. ありますか fragt nach Vorhandensein; WLAN wird dabei als Angebot, nicht als Person beschrieben.',
 'Die Reservierungsform wird hier als Zustand erklärt, ohne neue freie Beugung zu verlangen. Bei チェ ist kleines ェ Teil von che; kleines ッ hält k kurz zurück. あさごはんはなんじですか fragt nach der Frühstückszeit und bestellt noch kein Essen.'
 ],'Wiederhole の aus dem Besitzmuster: Was wird in へやのかぎ zugeordnet? Stelle anschließend eine Frage nach der Frühstückszeit.',
 'Frühstück – は – なんじですか; Schlüssel als Gegenstand vor をください.','v11:rooms v11:checkout v11:clock-hours')
guide('v11:travel-help','v11:polite-past v11:shop-choice v11:directions',
 'Verlaufen, Verlust, fehlende Nutzbarkeit und zwei konkrete Hilfsbitten auseinanderhalten.',[
 'みち michi Weg, まよいます mayoimasu sich verirren, さいふ saifu Portemonnaie, なくします nakushimasu verlieren. Die bekannte Vergangenheit ました berichtet: みちにまよいました, ich habe mich verlaufen; さいふをなくしました, ich habe mein Portemonnaie verloren.',
 'でんわ denwa Telefon; つかえません tsukaemasen heißt kann nicht benutzen. Das nennt keine technische Ursache. ちず chizu ist Stadt-/Landkarte, nicht die Zahlungskarte カード. ちずをみせてください verwendet die bekannte Zeigebitte.',
 'てつだってください tetsudatte kudasai = bitte helfen Sie mir, hier bei einer Tätigkeit. Lerne diese て-Bitte als Ganzes; keine neue freie Konjugation nötig. Die Pause vor t und stimmhaftes z in chizu beachten. すみません kann die Bitte höflich einleiten.'
 ],'Bitte um einen Stadtplan. Warum passt hier nicht die Zahlungskarte aus dem Einkauf?',
 'Verlorener Gegenstand – を – Verlustverb; gewünschte Hilfe – てください.','v11:shop-choice v11:polite-past')
guide('8:0','v11:location-action v11:languages v11:travel-help',
 'Einen Reisewunsch von einer sprachlichen Fähigkeit unterscheiden.',[
 'にほん Nihon Japan, にほんご Nihongo Japanisch. いきます ikimasu heißt gehe/fahre; ohne ます bleibt いき iki, daran たい: いきたい ikitai, möchte gehen. へ markiert hier das Ziel und wird e gelesen.',
 'はなせます hanasemasu heißt kann sprechen, aus はなす hanasu sprechen. にほんごがはなせます nennt eine Fähigkeit; が steht hier bei der Sprache. Die ähnliche Form はなします hanashimasu sagt spreche, ohne ausdrücklich können zu nennen.',
 'Im früheren Hilfesatz つかえません ging es um fehlende Möglichkeit; jetzt erkennst du die bejahte Fähigkeit. Ein Wunsch beweist kein Können. Beide Zielsätze enden höflich; bei Japanisch als Sprache darf ご nicht fehlen.'
 ],'Sage, dass du nach Japan möchtest. Welche zweite Aussage würde stattdessen dein Japanischkönnen beschreiben?',
 'Reiseziel – へ – Wunsch; Sprache – が – Fähigkeit.','v11:travel-help v11:languages')
guide('v11:wishes','8:0 v11:food-preferences v11:drinks v11:hobbies',
 'Vier Wünsche bilden und einen verneinten Wunsch von einer fehlenden Fähigkeit unterscheiden.',[
 'Von der bekannten ます-Form aus: たべます → たべたい tabetai essen wollen; のみます → のみたい nomitai trinken wollen; いきます → いきたい ikitai gehen wollen; します → したい shitai tun wollen. ゲーム gēmu Spiel und すし sushi sind schon bekannt.',
 'Das Schluss-い von たい wird zur Verneinung durch くない ersetzt: いきたくない ikitakunai, möchte nicht gehen. きょう kyō bedeutet heute. です macht die Aussage höflich. Ein fehlender Wunsch ist keine Aussage darüber, ob jemand gehen kann.',
 'Ein Wunsch wie おちゃをのみたいです sagt, was du möchtest. Zum direkten Bestellen steht dir weiterhin おちゃをください zur Verfügung. Später im Gespräch: カフェ kafe Café + にいきたいです = ich möchte ins Café gehen. Kyō und gēmu haben lange Vokale.'
 ],'Wiederhole die Bestellung eines Tees. Formuliere danach denselben Inhalt als eigenen Wunsch statt als Bitte an die Bedienung.',
 'ます entfernen, たい anhängen; Verneinung たくない, danach です.','8:0 v11:drinks v11:food-preferences')
guide('v11:dialog-cafe','6:0 v11:size-color v11:checkout v11:taste v11:wishes',
 'Eine Cafébestellung mit Menge, Temperatur, Größe, Verzehrort und Zahlungsweise verstehen.',[
 'Rollen: いらっしゃいませ irasshaimase begrüßt Kundschaft. ごちゅうもんは gochūmon wa fragt nach der Bestellung. おまたせしました omatase shimashita begleitet die Ausgabe nach dem Warten; du musst diese Serviceformen hier erkennen, nicht selbst herleiten.',
 'Wiederhole コーヒーをひとつください und Temperatur: あたたかいの atatakai no = das warme Getränk; の ersetzt das bekannte Getränk. In あたたかいのでいいですか ist の + で gemeint, keine Begründung mit weil. はい、それでおねがいします bestätigt die angebotene Wahl.',
 'Für die Gesprächswege: ホット hotto warm/heiß oder アイス aisu kalt; エス esu S, エム emu M, エル eru L; ここで koko de hier oder もちかえりで mochikaeri de mitnehmen. Mit カードでおねがいします zahlst du per Karte. Die Offline-Szene nimmt die Bestellung ohne Mengenwort an: コーヒーをください. Sie bietet nur S/klein oder L/groß; M und Stückzahlen bleiben zusätzliche Kursübungen. Diese Antworten bestimmen verschiedene Eigenschaften; eine Größe beantwortet keine Temperaturfrage.'
 ],'Spiele zwei Bestellungen durch: Wasser hier und bar; Kaffee kalt in Größe L zum Mitnehmen mit Karte. Antworte erst frei, öffne bei Bedarf die Hilfe.',
 'Bestellung und Servicefrage unterscheiden. Antworte mit der Information, nach der gerade gefragt wird.','v11:count-objects v11:drinks v11:taste 6:0 v11:size-color v11:checkout')
guide('v11:dialog-shopping','v11:shop-prices v11:shop-choice v11:size-color v11:checkout 8:0',
 'Beim Taschenkauf Preis, Farbe, Entscheidung und Bezahlmöglichkeit auseinanderhalten.',[
 'Wiederholung: このかばん kono kaban diese Tasche, みせてください bitte zeigen. ごらんください goran kudasai ist eine respektvolle Aufforderung des Verkaufs zum Anschauen. どうぞ dōzo begleitet das Angebot. Dies ist keine Bestellung durch den Kunden.',
 'さんぜんえん sanzen en = 3.000 Yen, aus der Zahlenlektion; nicht さんせん sagen. では dewa heißt dann, これをください bestätigt den Kauf. やめておきます yamete okimasu lehnt ihn im Gespräch ab. Beides darf nicht verwechselt werden.',
 'カードでしはらえますか (kādo de shiharaemasu ka) fragt kann ich mit Karte bezahlen? しはらう shiharau bezahlen → しはらえる shiharaeru bezahlen können; hier als ganze höfliche Frage. Wiederhole Farbnamen くろ kuro schwarz und あお ao blau: くろをおねがいします bestellt Schwarz, keine weitere Tasche.'
 ],'Spiele erst Preisfrage und Kauf einer schwarzen Tasche mit Karte, dann denselben Preis mit höflicher Absage durch. Bleibt bei der Absage eine Bestellung bestehen?',
 'Produkt – を – Zeigebitte; Zahlungsmittel – で – Frage nach dem Bezahlen.','v11:numbers-hundreds v11:shop-prices v11:shop-choice v11:size-color v11:checkout')

task('12:0',0,'Welche gelernte Zahl steht zwischen drei und fünf?','よん',{'に':'に ist zwei und steht vor drei. よん bezeichnet vier.','ご':'ご ist fünf, also bereits die obere Grenze; dazwischen liegt vier.'})
task('v11:numbers-six-ten',0,'Welche Grundzahl entspricht der Ziffer 9?','きゅう',{'じゅう':'じゅう ist zehn. Neun beginnt mit k: きゅう.','なな':'なな bedeutet sieben; gesucht ist neun.'})
task('v11:numbers-eleven',0,'Du liest 21. Welche Reihenfolge der Zahlenbausteine passt?','にじゅういち',{'じゅういち':'じゅういち enthält nur einen Zehner und einen Einer: 11.','にじゅう':'にじゅう ist genau 20; der zusätzliche Einer fehlt.'})
task('v11:numbers-hundreds',0,'Ein Übungspreis beträgt 600 Yen. Welche gelernte Zahl gehört vor えん?','ろっぴゃく',{'さんびゃく':'さんびゃく ist 300, nicht 600.','せん':'せん ist 1.000. Für 600 hat die Form eine Pause vor p.'})
task('v11:count-objects',0,'Die Ware ist schon klar. Du möchtest zwei Stück. Was passt?','ふたつください。',{'にください。':'に ist die Grundzahl zwei. Für die hier geübte Stückbestellung brauchst du ふたつ.','みっつください。':'みっつ bestellt drei Stück; du möchtest nur zwei.'})
task('17:0',0,'Welche Verbindung heißt eine ruhige Stadt?','しずかなまち',{'しずかまち':'Vor dem Nomen braucht das な-Adjektiv しずか die Verbindung な.','おおきいまち':'おおきい beschreibt Größe, nicht Ruhe.'})
task('v11:staples',0,'In パンをたべます: Was wird gegessen?','Brot.',{'Reis.':'Reis wäre ごはん; hier steht パン.','Fisch.':'Fisch wäre さかな; パン bezeichnet Brot.'})
task('v11:fruit-veg',0,'Welche Bitte bestellt genau zwei Äpfel?','りんごをふたつください。',{'りんごをみっつください。':'みっつ bedeutet drei Stück; es ist ein Apfel zu viel.','みかんをふたつください。':'Die Menge stimmt, aber みかん sind Mandarinen, keine Äpfel.'})
task('v11:drinks',0,'Du möchtest Wasser bestellen. Welche Bitte passt?','みずをください。',{'おちゃをください。':'おちゃ ist Tee; die Bitte würde das andere Getränk bestellen.','コーヒーをください。':'コーヒー ist Kaffee. Wasser heißt みず.'})
task('v11:taste',0,'Das Wasser hat eine niedrige Temperatur. Welche Eigenschaft passt?','つめたい',{'からい':'からい beschreibt Schärfe beim Essen, keine niedrige Temperatur.','あつい':'あつい ist heiß und bezeichnet die entgegengesetzte Temperatur.'})
task('v11:food-preferences',0,'Die Mahlzeit ist beendet. Du möchtest rückblickend den Geschmack loben. Was passt?','おいしかったです。',{'おいしいです。':'Das lobt den Geschmack in der Nichtvergangenheit. Die Aufgabe verlangt ausdrücklich die Rückschau.','にくはたべません。':'Das erklärt einen Verzicht auf Fleisch; es lobt die Mahlzeit nicht.'})
task('6:0',0,'Du nimmst deinen Kaffee mit. Welche gelernte Ortswahl passt?','もちかえりでおねがいします。',{'ここでおねがいします。':'ここで bedeutet hier vor Ort; du möchtest das Getränk mitnehmen.','ふたつください。':'Das bestellt zwei Stück. Es sagt nichts über Mitnehmen oder Vor-Ort aus.'})
task('v11:shop-prices',0,'Der Preis lautet せんにひゃくえん. Welcher Betrag ist gemeint?','1.200 Yen.',{'200 Yen.':'にひゃく ist 200, aber davor steht zusätzlich せん für 1.000.','500 Yen.':'500 wäre ごひゃく. Hier werden 1.000 und 200 zusammengefügt.'})
task('v11:shop-choice',0,'Du möchtest ausdrücklich noch nichts kaufen und nur schauen. Was passt?','みているだけです。',{'これにします。':'Damit entscheidest du dich für den Gegenstand, statt nur zu schauen.','これをみせてください。':'Das bittet um Zeigen eines Gegenstands, sagt aber nicht ausdrücklich nur schauen.'})
task('v11:clothes',0,'Du kaufst einen Mantel. Welches Wort gehört vor をかいます?','コート',{'シャツ':'シャツ bezeichnet ein Hemd, keinen Mantel.','くつ':'くつ bezeichnet Schuhe; hier ist ein Mantel gefragt.'})
task('v11:size-color',0,'Du möchtest im Café die mittlere Größe M. Was passt?','エムサイズでおねがいします。',{'エスサイズでおねがいします。':'エス ist S, also klein. M wird エム gelesen.','ふたつください。':'ふたつ nennt zwei Stück, keine mittlere Bechergröße.'})
task('v11:checkout',0,'Du antwortest als Kunde auf die Frage nach der Zahlungsweise und möchtest bar bezahlen. Was passt?','げんきんではらいます。',{'カードでおねがいします。':'カード wählt Kartenzahlung. Du möchtest mit Bargeld zahlen.','レシートをください。':'Das verlangt einen Kassenbon, nennt aber noch keine Zahlungsweise.'})
task('v11:transport',0,'Du verlässt den Bus. Welcher Satz passt?','バスをおります。',{'バスにのります。':'のります bezeichnet Einsteigen/Mitfahren, nicht das Verlassen.','バスていはどこですか。':'Das fragt nach der Haltestelle; es beschreibt kein Aussteigen.'})
task('v11:station',0,'Die Antwort ist にばんせん, Gleis zwei. Welche Frage passt dazu?','なんばんせんですか。',{'いくらですか。':'いくら fragt nach einem Preis, nicht nach der Gleisnummer.','つぎのえきですか。':'Das fragt nach der nächsten Station, nicht nach dem Abfahrtsgleis.'})
task('v11:hotel',0,'Du möchtest die Uhrzeit des Frühstücks erfahren. Welche Frage passt?','あさごはんはなんじですか。',{'あさごはんはいくらですか。':'いくら fragt nach dem Preis; für die Uhrzeit steht なんじ.','ワイファイはありますか。':'Das fragt nach WLAN und enthält keine Frage zum Frühstück.'})
task('v11:travel-help',0,'Du möchtest dir zur Orientierung einen Stadtplan zeigen lassen. Was passt?','ちずをみせてください。',{'カードでいいですか。':'カード ist hier eine Zahlungskarte; die Frage betrifft das Bezahlen.','さいふをなくしました。':'Das meldet ein verlorenes Portemonnaie, verlangt aber keinen Stadtplan.'})
task('8:0',0,'Welche Aussage beschreibt eine Fähigkeit statt eines Reisewunsches?','にほんごがはなせます。',{'にほんへいきたいです。':'たい drückt den Wunsch aus, nach Japan zu fahren; es belegt keine Sprachfähigkeit.','にほんにいきます。':'Das sagt, dass jemand nach Japan fährt/geht. Es sagt nichts über dessen Japanischkenntnisse.'})
task('v11:wishes',0,'Du möchtest heute ausdrücklich nicht gehen. Welche Form passt?','きょうはいきたくないです。',{'きょうはいきたいです。':'たい ist der bejahte Wunsch. Die Verneinung たくない fehlt.','きょうはいきます。':'いきます ist eine Aussage über Gehen/Fahren und verneint keinen Wunsch.'})
task('v11:dialog-cafe',0,'Im Café möchtest du Kaffee kalt. Welche Temperaturwahl passt?','アイスをおねがいします。',{'ホットをおねがいします。':'ホット wählt die warme/heiße Variante; gewünscht ist kalt.','エムサイズでおねがいします。':'Das wählt Größe M, beantwortet aber nicht die Temperaturfrage.'})
task('v11:dialog-cafe',2,'Du möchtest deinen Kaffee in Größe L. Welche Antwort passt zur Größenfrage?','エルサイズでおねがいします。',{'エムサイズでおねがいします。':'エム ist die mittlere Größe M. L wird エル gelesen.','アイスをおねがいします。':'アイス nennt die Temperaturvariante, keine Größe.'})
task('v11:dialog-cafe',3,'Nach der Größenwahl möchtest du vor Ort trinken. Welche Antwort passt?','ここでおねがいします。',{'もちかえりでおねがいします。':'もちかえりで würde Mitnehmen wählen. Du möchtest hier trinken.','カードでおねがいします。':'Das nennt die Zahlungsweise, nicht den Verzehrort.'})
task('v11:dialog-cafe',4,'Die Bestellung ist fertig. Du möchtest mit Karte zahlen. Was passt?','カードでおねがいします。',{'げんきんではらいます。':'げんきん ist Bargeld. Das wäre eine andere Zahlungsweise.','ひとつください。':'Das bestellt ein Stück und beantwortet die Zahlungsfrage nicht.'})
task('v11:dialog-shopping',0,'Die Tasche ist dir zu teuer; du entscheidest dich ausdrücklich gegen den Kauf. Was passt?','やめておきます。',{'では、これをください。':'Damit bestätigst du den Kauf. Die Situation verlangt eine Absage.','これにします。':'Auch diese Wendung trifft eine positive Kaufentscheidung.'})
task('v11:dialog-shopping',3,'Du kaufst die Tasche und wählst Schwarz. Welche Antwort passt zur Farbfrage?','くろをおねがいします。',{'あおがいいです。':'あお ist Blau. Die Entscheidung zum Kauf bleibt, aber die Farbe wäre falsch.','カードでおねがいします。':'Das nennt Kartenzahlung, keine Taschenfarbe.'})

LEGACY = {
 '12:0':['Die Grundzahl eins ist いち (ichi).','に (ni) ist die Grundzahl zwei; es ist hier keine Partikel.','さん (san) nennt drei; es ist hier keine Namensanrede.','よん (yon) ist die hier geübte Lesung für vier.','Die Sammelkarte nennt nacheinander fünf, sechs, sieben, acht, neun und zehn; die Punkte sind Trenner.'],
 '17:0':['おおきい (ōkii) beschreibt Größe. Vor dem Nomen steht kein な.','おいしい (oishii) lobt den Geschmack; das abschließende ii ist lang.','しずか (shizuka) ist ein な-Adjektiv: vor まち steht な, vor です nicht.','たかい (takai) wird verneint zu たかくない (takakunai); です macht die Aussage höflich.'],
 '6:0':['コーヒーをください bestellt einen Kaffee; を folgt dem gewünschten Getränk.','これはいくらですか fragt nach dem Preis des gezeigten Gegenstands.','ありがとうございます bedankt sich höflich, ohne eine neue Bestellung aufzugeben.'],
 '8:0':['いきたいです drückt einen eigenen Wunsch aus: möchte gehen/fahren. へ wird hier e gelesen.','はなせます sagt kann sprechen; にほんご ist die Sprache und steht hier vor が.']
}

def upgrade():
    path=ROOT/'data/course.json'; data=json.loads(path.read_text('utf-8'))
    lessons={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
    deep=json.loads((ROOT/'data/deep_lessons.json').read_text('utf-8'))
    for key,authored in GUIDES.items():
        l=lessons[key]
        assert l.get('study_guide',{}).get('package',3)==3, 'Never overwrite previous packages'
        l['goal']=authored['goal'];l['study_guide']=copy.deepcopy(authored['study_guide'])
        l['intro']=authored['goal']+' Die Lernhilfe erklärt die benötigten Wörter und Muster vor dem Abruf.'
        for i,c in enumerate(l['cards']):
            p=copy.deepcopy(c.get('detail') or deep['profiles'].get(c['jp']) or {})
            if key in LEGACY:p['explain']=LEGACY[key][i]
            p.setdefault('explain',c['note']);p.setdefault('kind','Zahlen, Einkauf und Anwendung')
            p.setdefault('usage',c['de']);p.setdefault('register','Höfliche Sätze; einzelne Nomen und Zahlen sind neutral.')
            p.setdefault('parts',[]);p.setdefault('extra',[]);p.setdefault('pitfall',authored['build'])
            if isinstance(c.get('example'),str):
                c['example']={'jp':c['example'],'romaji':c['example_romaji'],'de':c['example_de']}
            if not c.get('example'):
                c['example']={'jp':c['jp'],'romaji':c['romaji'],'de':c['de']}
            if (key,i) in APPLICATIONS:
                scenario=copy.deepcopy(APPLICATIONS[(key,i)])
            else:
                scenario=copy.deepcopy(p.get('scenario') or {'question':f'Welche Bedeutung passt zu {c["jp"]}?',
                    'correct':c['de'],'wrong':[x['de'] for j,x in enumerate(l['cards']) if j!=i][:3]})
                scenario['question']=scenario['question'].replace('dieser Karte',c['jp']).replace('dieser Lernkarte',c['jp'])
                scenario['feedback']={}
                for wrong in scenario['wrong']:
                    other=next((x for x in l['cards'] if x is not c and
                        (x['de']==wrong or (x.get('detail') or deep['profiles'].get(x['jp'],{})).get('scenario',{}).get('correct')==wrong)),None)
                    scenario['feedback'][wrong]=(f'Das gehört zu {other["jp"]} ({other["romaji"]}), {other["de"]}. ' if other else 'Diese Auswahl erfüllt eine andere Funktion. ')+p['explain']
            p['scenario']=scenario
            p['feedback']={'build':authored['build'],'write':c['note']+' Prüfe die vollständige Lesung und ihre langen Vokale.','listen':p['explain']}
            c['detail']=p
    data['content_version']='11.0.5'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'package':3,'lessons':len(GUIDES),'cards':sum(len(lessons[k]['cards']) for k in GUIDES),'applications':len(APPLICATIONS),'new_lessons':0},ensure_ascii=False))

if __name__=='__main__':upgrade()
