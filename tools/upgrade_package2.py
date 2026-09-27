"""Authored package 02. Idempotent; never changes IDs, order or card targets.

Run only on an existing course with package 01. Human linguistic review is open.
"""
import copy,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GUIDES={}
def guide(key,prerequisites,goal,points,recall,build):
    GUIDES[key]={'goal':goal,'study_guide':{'revision':1,'package':2,
      'prerequisites':prerequisites.split(), 'points':points,'recall':recall},'build':build}

guide('v11:languages','v11:countries 2:0',
 'Japanisch, Deutsch und Englisch unterscheiden und sagen, welche Sprache du lernst.',[
 'Bekannt: にほん (Nihon, Japan), ドイツ (Doitsu, Deutschland), は … です. Neu: ご (go) bezeichnet hier eine Sprache; えいご (eigo, Englisch) ist eine eigene Wortform. ～じん nennt dagegen eine Person nach ihrer Nationalität.',
 'Vor dem langen Satz: を liest du o; es steht nach dem, was du lernst. べんきょうしています (benkyō shite imasu) bedeutet hier: ich bin mit dem Lernen beschäftigt. Lerne diesen Ausdruck zunächst als Ganzes; die Bildung der て-Form folgt später. すこし (sukoshi) heißt ein wenig; わかります (wakarimasu) heißt verstehen.',
 'にほんごをべんきょうしています: Japanisch + Objektmarkierung + lerne. Sprich ben-kyō mit langem ō; kleines ょ verbindet k und yo. Im Beispiel すこしわかります begrenzt すこし das Verstehen, nicht den Namen einer Sprache.'
 ],'Erinnere dich an ドイツじん: Wie unterscheidet sich das von ドイツご? Sage anschließend, dass du Japanisch lernst.',
 'Eine Sprache steht vor を; die Tätigkeit folgt am Satzende. ご gehört zum Sprachnamen.')
guide('v11:jobs','2:0 3:0 v11:asking-names',
 'Vier Berufsangaben verstehen und eine höfliche Frage nach dem Beruf erkennen.',[
 'Bekannt: Nomen + です und die Frageendung か. しごと (shigoto) bedeutet Arbeit oder Beruf. お in おしごと macht die Frage höflicher; なん (nan) heißt hier was. おしごとはなんですか fragt nach dem Beruf.',
 'かいしゃいん (kaishain) ist eine angestellte Person einer Firma; かいしゃ heißt Firma. じえいぎょう (jieigyō) bezeichnet Selbstständigkeit. きょうし (kyōshi) benennt den Lehrberuf, せんせい (sensei) dient auch als Anrede einer anderen Lehrkraft. エンジニア (enjinia) bedeutet Ingenieur/in.',
 'Mit です wird aus der Berufsbezeichnung im Vorstellungsgespräch eine höfliche Aussage: きょうしです. Keine eigene Verbform für ich nötig. In kyōshi und jieigyō ist ō lang; ka-i-sha-in enthält mehrere Vokaltakte. Die Beispiele verlangen noch keinen Satz mit arbeiten.'
 ],'Antworte auf おしごとはなんですか mit einem Beruf + です. Frage danach wie in der Namenslektion zurück.',
 'Die Berufsbezeichnung kommt zuerst, eine höfliche Satzendung zuletzt. Ein einzelner Beruf ist noch keine Frage.')
guide('14:0','2:0 3:0 v11:languages',
 'Thema, neu genanntes Subjekt, Objekt und Zugehörigkeit in einfachen Sätzen unterscheiden.',[
 'Bekannt: わたし (watashi, ich), ほん (hon, Buch), みず (mizu, Wasser), は … です. Neu für diese Beispiele: ねこ (neko, Katze), います (imasu, ist da), のみます (nomimasu, trinke). Du musst diese Verben noch nicht selbst beugen.',
 'は (wa) setzt ein Thema: わたしは … . が (ga) markiert hier, wer oder was neu genannt wird: ねこがいます, eine Katze ist da. は und が sind nicht einfach zwei Wörter für ist. Ihr Gebrauch hängt vom Gespräch ab; hier werden nur diese klaren Grundfälle geprüft.',
 'を (o) folgt dem Objekt: みずをのみます, ich trinke Wasser. の (no) verbindet Nomen: わたしのほん, mein Buch. Erst die zuordnende Person, dann の, dann der Gegenstand. Partikel stehen nach ihrem Bezug; は als Partikel wa, を o sprechen.'
 ],'Vergleiche わたしは … mit わたしのほん. Was macht die Aussage über mich, was ordnet mir ein Buch zu?',
 'Partikel folgen ihrem Bezugswort. Bei Besitz: Person – の – Gegenstand; bei einer Handlung steht das Verb am Ende.')
guide('15:0','14:0 v11:languages',
 'Ziel, Handlungsort, Verkehrsmittel, Begleitung und auch anhand des Satzes unterscheiden.',[
 'Bekannt: にほん (Nihon, Japan), いえ (ie, Zuhause), バス (basu, Bus), わたし. Neu: いきます (ikimasu, gehe/fahre), ともだち (tomodachi, Freund/in), はなします (hanashimasu, spreche), おきます (okimasu, stehe auf), しちじ (shichiji, sieben Uhr).',
 'に (ni) markiert ein Ziel oder einen bestimmten Zeitpunkt: えきにいきます, ich gehe zum Bahnhof; しちじにおきます, ich stehe um sieben auf. えき (eki) heißt Bahnhof. へ als Richtungspartikel liest du e: にほんへいきます. に und へ können beide ein Bewegungsziel begleiten; eine Aufgabe darf sie dort nicht künstlich gegeneinander ausspielen.',
 'で (de) begleitet den Handlungsort oder das Mittel: いえでべんきょうします, ich lerne zu Hause; バスでいきます, ich fahre mit dem Bus. と (to) begleitet eine Person oder verbindet Nomen; die Zitatfunktion folgt später. も (mo) heißt auch: わたしもいきます. Es ersetzt hier は.'
 ],'Wiederhole を: Was lernt man? Vergleiche danach いえで (wo?) und バスで (womit?).',
 'Erst Ort, Zeit oder Begleitperson, dann die zugehörige Partikel. Das Verb schließt den Handlungssatz ab.')
guide('16:0','14:0 15:0',
 'Für Gegenstände und Pflanzen あります, für Menschen und Tiere います wählen und nach einem Ort fragen.',[
 'Bekannt: ほん (hon, Buch), ねこ (neko, Katze), が, に. Neu in den Beispielen: へや (heya, Zimmer), つくえ (tsukue, Tisch), うえ (ue, oben), どこ (doko, wo), えき (eki, Bahnhof). Großes や in heya bleibt ein eigener Takt; tsu-ku-e enthält getrennte Vokale.',
 'Ort + に + Ding + が + あります beschreibt das Vorhandensein eines Gegenstands. Für Menschen und Tiere steht います. Pflanzen werden normalerweise ebenfalls mit あります beschrieben; die Einteilung ist keine biologische Definition von lebendig.',
 'つくえのうえ heißt auf dem Tisch: Tisch + の + Oberseite. Im Beispiel つくえのうえにほんがあります steht das ganze Ortsstück vor に. どこにありますか fragt nach dem Standort eines bekannten Dings. Bei einer Person wäre どこにいますか passend.'
 ],'Entscheide ohne Vorlage: Buch, Katze oder Blume – welche Existenzform passt jeweils? Erinnere dich an の bei einer Ortsgruppe.',
 'Ortsgruppe – に – Ding oder Person – が – Existenzverb. In der Ortsfrage steht か am Ende.')
guide('13:0','3:0 16:0',
 'Für Sache, Person, Ort, Zeitpunkt und Grund das passende Fragewort wählen.',[
 'Fragen behalten die normale Satzfolge; か steht am Ende. なに / なん sind zwei Lesungen für was. Vor です verwendest du hier なん: なんですか. Die Karte zeigt beide Lesungen; beim Sprechen oder Schreiben genügt eine der beiden.',
 'だれ (dare) fragt nach einer Person, どこ (doko) nach einem Ort, いつ (itsu) nach dem Zeitpunkt, どうして (dōshite) nach dem Grund. Bei どうして ist ō lang. どなた (donata) ist eine höflichere Alternative zu だれ; sie ist hier keine Pflichtantwort.',
 'Wörter der Beispiele: これ (kore, das hier), あのひと (ano hito, jene Person), トイレ (toire, Toilette), いきます (ikimasu, gehe/fahre). いついきますか fragt nach dem Zeitpunkt; トイレはどこですか nach dem Ort. Ein Fragewort wird nach der gesuchten Information gewählt.'
 ],'Denke an どこにありますか. Tausche nicht bloß ein Wort aus: Welche Antwortart passt zu wo, wer und wann?',
 'Fragewort im passenden Satzteil, höfliche Endung und zuletzt か. nani und nan sind Alternativen, keine gemeinsame Wortkette.')
guide('v11:this-that','13:0 14:0',
 'Bei räumlichem Zeigen dies hier, das bei dir und jenes dort unterscheiden; nach der Sache oder einer Auswahl fragen.',[
 'Bekannt: ほん (hon, Buch), かぎ (kagi, Schlüssel), は … です, なん. Neu im Beispiel: やま (yama, Berg). これ・それ・あれ stehen selbstständig; ein Nomen folgt nicht direkt auf diese Formen.',
 'In der gezeigten räumlichen Situation liegt これ (kore) bei mir, それ (sore) bei dir, あれ (are) von uns beiden entfernt. それ kann außerdem bereits Erwähntes aufgreifen. Die Übungen nennen ausdrücklich den räumlichen Kontext.',
 'どれ (dore) fragt welches aus einer Auswahl. なんですか fragt was etwas ist. これはほんです nennt die Art eines Gegenstands, どれですか verlangt eine Auswahl. Die kurzen e-Vokale nicht zu deutschem ei machen.'
 ],'Frage bei einem unbekannten Ding nach seiner Bezeichnung und bei drei bekannten Dingen nach der Auswahl.',
 'Zeigewort steht allein als Nomenersatz; は setzt das Thema, です schließt die Aussage ab.')
guide('v11:this-noun','v11:this-that',
 'Zeigewörter mit nachfolgendem Nomen bilden und von den selbstständigen Formen unterscheiden.',[
 'Bekannt: ほん (hon, Buch), かばん (kaban, Tasche), ひと (hito, Person), ペン (pen, Stift). Neu: くるま (kuruma, Auto). Alle Wörter werden ohne Pluralendung gelernt.',
 'この (kono), その (sono), あの (ano), どの (dono) benötigen unmittelbar ein Nomen: このほん. Anders als これ kann この hier nicht allein stehen. Kein zusätzliches の einsetzen: この enthält bereits die richtige Endung.',
 'Nähe wie zuvor: この bei mir, その bei dir, あの von beiden entfernt. どのくるまですか fragt welches Auto. In ひと ist h weich; bei かばん erhält ん einen eigenen Takt. Lerne immer Zeigewort und Bezugsnomen zusammen.'
 ],'Wiederhole これです und bilde danach このほんです. Warum braucht nur der zweite Ausdruck ein zusätzliches Nomen?',
 'この・その・あの・どの stehen direkt vor dem Nomen; nicht noch の dazwischensetzen.')
guide('v11:whose','14:0 13:0 v11:this-noun v11:languages',
 'Besitzer oder Thema mit の zuordnen, nach Besitz fragen und einen bekannten Gegenstand weglassen.',[
 'Bekannt: わたし, せんせい (sensei, Lehrkraft), だれ, ほん, ペン, かばん und にほんご. A の B bezeichnet B, das A zugeordnet ist. Das letzte Nomen bestimmt, um welchen Gegenstand es geht.',
 'わたしのほん ist mein Buch; せんせいのペン der Stift der Lehrkraft. だれのかばんですか fragt wessen Tasche. の verbindet nicht nur Besitz: にほんごのほん ist ein Buch über/zu Japanisch; die Sprache ist kein Besitzer.',
 'Wenn der Gegenstand bereits klar ist, genügt わたしのです, es ist meins. の ersetzt hier zusammen mit dem Kontext die erneute Nennung des Gegenstands. Sprich sensei mit der gehörten langen e-Qualität; die Lernschreibweise bleibt sensei.'
 ],'Erinnere dich an だれ. Wie wird daraus wessen? Vergleiche Besitz mit dem Thema eines Japanischbuchs.',
 'Besitzer oder Zuordnung – の – Gegenstand. Nur wenn dieser bekannt ist, darf er in わたしのです entfallen.')
guide('v11:here-there','13:0 v11:this-that',
 'Auf einen Ort zeigen, nach einem Ort fragen und eine höfliche Wegweisung erkennen.',[
 'Bekannt: どこ (doko, wo), ですか, トイレ (toire, Toilette). Anders als これ für einen Gegenstand bezeichnet ここ (koko) einen Ort. そこ (soko) liegt räumlich beim Gegenüber, あそこ (asoko) weiter von beiden entfernt.',
 'トイレはどこですか fragt nach dem Standort der Toilette. ここです antwortet hier. Das Fragewort steht an der Stelle der fehlenden Ortsangabe; keine deutsche Umstellung des Verbs.',
 'こちら (kochira) ist eine höfliche Orts- oder Richtungsangabe: こちらです, hier entlang. In anderem Kontext kann es auch diese Person bedeuten. In dieser Lektion gilt die Wegweisung. In a-so-ko hat jedes Zeichen seinen Takt.'
 ],'Wiederhole これ, dann ここ: Welches zeigt ein Ding, welches einen Ort? Beantworte eine Ortsfrage aus drei Entfernungen.',
 'Ortswort vor です; Fragewort vor ですか. Gegenstandswörter und Ortswörter nicht vertauschen.')
guide('v11:existence','16:0 v11:here-there',
 'Vorhandensein und Standort unterscheiden und vier Nomen mit dem passenden Existenzverb verbinden.',[
 'Bekannt: ほん (hon, Buch), ねこ (neko, Katze), せんせい (sensei, Lehrkraft), はな (hana, Blume), かぎ (kagi, Schlüssel), ここ, が und に. Die neuen Sätze verbinden diese Bausteine.',
 'ほんがあります und はながあります melden Dinge oder Pflanzen. ねこがいます und せんせいがいます melden Tiere oder Menschen. が steht bei dem neu genannten Ding oder Wesen; eine Blume zählt in diesem Muster zu あります.',
 'かぎはここにあります nennt den Standort eines bekannten Schlüssels. Vergleiche: Was ist da? → Nomen + が; wo ist es? → Ort + に. Höre den Unterschied a-ri-ma-su und i-ma-su am Anfang.'
 ],'Rufe die Regel aus あります・います ab und beschreibe jetzt eine Katze hier sowie einen Schlüssel hier.',
 'Bei Vorhandensein: Nomen – が – Verb. Bei Standort: Ort – に – Verb; die Art des Wesens entscheidet über das Verb.')
guide('5:0','14:0 v11:languages',
 'Essen und Trinken unterscheiden und Wasser als Objekt eines höflichen Handlungssatzes benennen.',[
 'Bekannt: みず (mizu, Wasser) und を (o). Neu: たべます (tabemasu, esse/werde essen), のみます (nomimasu, trinke/werde trinken). Die Endung ます drückt Höflichkeit aus, keine bestimmte Person.',
 'みずをのみます ordnet zuerst das Wasser als Objekt zu und nennt dann die Handlung. Das Verb steht am Ende. ます ist Nichtvergangenheit: Gewohnheit oder Zukunft ergeben sich aus dem Zusammenhang; gerade dabei braucht später ein weiteres Muster.',
 'In mizu ist z stimmhaft, nicht deutsches ts. を wird o gesprochen. In der Vorlage kann das u von masu schwach hörbar sein; beim Schreiben bleibt masu vollständig. Die Erklärung dieser vier Karten reicht für alle Aufgaben der Lektion.'
 ],'Erinnere dich an にほんごをべんきょうしています: Was steht dort vor を, was im Satz mit Wasser?',
 'Was gegessen oder getrunken wird, steht vor を; danach folgt das Verb. Nicht die deutsche Reihenfolge übertragen.')
guide('v11:morning-evening','5:0 15:0 v11:clock-hours v11:numbers-eleven',
 'Aufstehen, Schlafengehen, Hingehen, Heimkehren und Pausieren in einem Tagesablauf unterscheiden.',[
 'Bekannt: ます, Zeit + に, いえ (ie, Zuhause), がっこう (gakkō, Schule), すこし (sukoshi, ein wenig). Uhrzeiten der Beispiele: しちじ (shichiji, 7 Uhr), じゅういちじ (jūichiji, 11 Uhr).',
 'おきます (okimasu) heißt aufstehen/aufwachen, ねます (nemasu) schlafen/ins Bett gehen. Mit Uhrzeit nennt ねます hier das Schlafengehen. いきます (ikimasu) bewegt sich zu einem Ziel; かえります (kaerimasu) ist eine Rückkehr. やすみます (yasumimasu) heißt sich ausruhen oder pausieren.',
 'しちじにおきます: bestimmte Zeit + に + Tätigkeit. いえにかえります: Ziel + に + Rückkehr. Grundformen in den Karten sind Zusatzinformation, noch keine Beugungsaufgabe. In がっこう und じゅういちじ auf Pause bzw. Vokallänge achten.'
 ],'Erinnere dich an に für Ziel und Zeit. Nenne im Kopf eine Zeit zum Aufstehen und das Ziel deiner Rückkehr.',
 'Zeit oder Ziel mit に steht vor dem Tätigkeitsverb. Hingehen und Zurückkehren sind verschiedene Verben.')
guide('v11:work-study','v11:languages v11:jobs 5:0 15:0',
 'Arbeiten, Lernen, Lesen, Schreiben und Hören anhand von Handlung und Objekt unterscheiden.',[
 'Bekannt: かいしゃ (kaisha, Firma), にほんご, ほん, なまえ (namae, Name). Neu im Hörbeispiel: おんがく (ongaku, Musik). で markiert den Arbeitsplatz; を den Lernstoff oder das Gelesene/Gehörte.',
 'はたらきます (hatarakimasu) heißt arbeiten. べんきょうします (benkyō shimasu) heißt lernen; べんきょう + します bildet hier die Tätigkeit. Gegenüber dem früheren べんきょうしています ist dies die einfache höfliche Nichtvergangenheit.',
 'よみます (yomimasu) lesen, かきます (kakimasu) schreiben und ききます (kikimasu) hören unterscheiden sich am Stamm. ききます kann mit anderem Kontext fragen heißen; mit おんがく ist hören gemeint. In benkyō bleibt ō lang, in ongaku hat n einen eigenen Takt.'
 ],'Wiederhole を und で: Was markiert にほんごを, was かいしゃで? Vergleiche anschließend ka-ki und ki-ki.',
 'Objekt – を – Tätigkeit; Arbeitsplatz – で – arbeiten. Den Stamm vor ます genau vergleichen.')
guide('v11:location-action','15:0 v11:work-study v11:morning-evening v11:clock-hours',
 'Aus einem Satz Ziel, Handlungsort, Verkehrsmittel, Begleitung oder Uhrzeit herauslesen.',[
 'Bekannt: いきます, べんきょうします, いえ, バス und くじ (kuji, 9 Uhr). Wieder aufgegriffen: えき (eki, Bahnhof), ともだち (tomodachi, Freund/in). Alle fünf Sätze haben ein unterschiedliches Informationsziel.',
 'えきにいきます nennt wohin; いえでべんきょうします nennt wo die Handlung stattfindet. バスでいきます nennt womit. Entscheidend ist das Bezugswort vor der Partikel, nicht nur die Partikel allein.',
 'ともだちといきます nennt mit wem; くじにいきます nennt wann. Vergleiche えきに und くじに: dieselbe Partikel übernimmt je nach Wort eine andere Funktion. Lange Vokale in benkyō nicht verkürzen; kuji ohne zusätzliches y sprechen.'
 ],'Rufe die Unterscheidung von に und で aus der Partikellektion ab. Welche Frage beantwortet jeder der fünf Sätze?',
 'Erst Bezugswort, dann Partikel, dann Tätigkeit. Ein Verkehrsmittel ist kein Ziel und eine Begleitung kein Handlungsort.')
guide('v11:polite-past','5:0 3:0 v11:relative-time',
 'Bejahung, Verneinung, Vergangenheit und Frage bei einem höflichen Verb erkennen.',[
 'Bekannt: のみます, みず, コーヒー (kōhī, Kaffee), おちゃ (ocha, Tee), きのう (kinō, gestern), を und か. Der gleichbleibende Stamm ist のみ; die Endung liefert neue Information.',
 'のみます: trinke/werde trinken. のみません: trinke nicht/werde nicht trinken. のみました: habe getrunken. のみませんでした: habe nicht getrunken. Bei der letzten Form die ganze Endung beachten, nicht nur ません.',
 'のみますか fragt höflich nach dem Trinken; in einem Angebot kann das heißen möchten Sie trinken. Das ist keine eigene Wunschform des Verbs. ma-su, ma-sen, ma-shi-ta und ma-sen de-shi-ta bewusst vergleichen; die Vokallängen der Getränkenamen bleiben erhalten.'
 ],'Wiederhole か aus der ersten Fragelektion. Wie erkennst du unabhängig davon, ob ein Satz vergangen und verneint ist?',
 'Der Stamm bleibt vor der höflichen Endung. でした gehört zur verneinten Vergangenheit; eine Frage endet zusätzlich auf か.')
guide('v11:rooms','v11:existence 2:0',
 'Zimmer, Küche, Tisch, Fenster und Bett benennen und ihre Anwesenheit ausdrücken.',[
 'Bekannt: Nomen + です und Nomen + があります. Neu: へや (heya, Zimmer), だいどころ (daidokoro, Küche), つくえ (tsukue, Tisch), まど (mado, Fenster), ベッド (beddo, Bett). Diese Wörter sind Grundlage für spätere Ortsangaben.',
 'へやです benennt einen Raum. つくえがあります meldet, dass ein Tisch vorhanden ist. Alle hier genannten Gegenstände verwenden あります. Keine Person wird mit あります beschrieben.',
 'He-ya hat ein großes や, tsu-ku-e getrennte Vokale. Im Katakana ベッド erzeugt das kleine ッ eine Pause vor d: bed-do. Es ist kein zusätzliches tsu. だいどころ benennt den Raum, keine Kochtätigkeit.'
 ],'Wiederhole あります・います: Beschreibe einen Tisch und eine Katze im Zimmer. Welches Verb ändert sich?',
 'Nomen zuerst; bei Vorhandensein danach があります. Das kleine ッ gehört zum folgenden Konsonanten.')
guide('v11:positions','v11:rooms v11:whose v11:existence v11:this-noun',
 'Auf, unter, in, vor und neben als Ortsgruppen bilden und einen Gegenstand dort lokalisieren.',[
 'Bekannt: つくえ, いえ, えき, ほん, かばん, かぎ, くるま (kuruma, Auto), ホテル (hoteru, Hotel). Neu: はこ (hako, Schachtel), した (shita, unter), なか (naka, innen), まえ (mae, vor), となり (tonari, neben). うえ (ue, oben) wird wiederholt.',
 'Bezugsding + の + Positionswort: つくえのうえ, auf dem Tisch. Diese gesamte Gruppe bekommt に: ほんはつくえのうえにあります. の verbindet hier eine räumliche Beziehung, nicht einen Besitzer.',
 'つくえのした ist unter dem Tisch; はこのなか in der Schachtel; いえのまえ vor dem Haus; えきのとなり neben dem Bahnhof. Ortsgruppe + です ist ebenfalls möglich. In mae und ue bleiben die Vokale getrennt; keinen deutschen Doppellaut einsetzen.'
 ],'Vergleiche わたしのほん aus der Besitzlektion mit つくえのうえ. Woran hängt das folgende に?',
 'Bezugsding – の – Positionswort bildet eine Gruppe; erst danach folgt bei einer Standortangabe に.')
guide('v11:directions','v11:positions v11:here-there v11:learning-help',
 'Rechts, links und geradeaus unterscheiden sowie eine einfache Bitte zum Abbiegen verstehen.',[
 'Bekannt: えき (eki, Bahnhof), です, die Bitte mit ください. Neu: みぎ (migi, rechts), ひだり (hidari, links), まっすぐ (massugu, geradeaus), ちかく (chikaku, Nähe). Die Blickrichtung ist die der gehenden Person.',
 'Vor dem ersten Abruf: いってください (itte kudasai) heißt bitte gehen; まがってください (magatte kudasai) bitte abbiegen. Dies sind feste Bitten mit て-Form + ください. Ihre systematische Bildung folgt später; hier sind beide Formen vollständig erklärt.',
 'みぎにまがってください verbindet Richtung + に + Bitte. ちかくです nennt nur Nähe, keine genaue Entfernung. Kleine っ in massugu, itte und magatte erzeugen eine Pause vor dem folgenden Konsonanten. Links und rechts nicht aus Sicht eines Gegenübers vertauschen.'
 ],'Wiederhole die Ortsfrage どこですか. Reagiere dann im Kopf auf rechts, geradeaus, links in dieser Reihenfolge.',
 'Die Richtung steht vor に; die Abbiegeform steht vor ください. Kleine っ bleiben als Konsonantenverdopplung erhalten.')
guide('v11:smalltalk','3:0 v11:learning-help v11:small-tsu',
 'Neue Information aufnehmen, Zustimmung oder Überraschung ausdrücken und um eine kurze Pause bitten.',[
 'Bekannt: です, か und ください. Neu bzw. wiederholt: そう (sō, so), いい (ii, gut), ほんとう (hontō, wirklich), ね (ne, sucht hier eine geteilte Einschätzung). Die Reaktion hängt auch vom Tonfall ab.',
 'そうですか kann ach so heißen, während ほんとうですか ausdrücklich Überraschung oder Nachfrage signalisiert. いいですね reagiert positiv. そうですね kann zustimmen oder Zeit zum Nachdenken geben; die Aufgaben geben die Situation an und beanspruchen keine einzig mögliche Reaktion in jedem Gespräch.',
 'ちょっとまってください heißt bitte warten Sie kurz: ちょっと (chotto, kurz) + まって (matte, Warteform) + ください. Beide kleinen っ hörbar halten. In sō und hontō ist ō lang, ii besteht aus zwei Vokaltakten.'
 ],'Wiederhole もういちど aus der Hilfslektion. Unterscheide eine Wiederholungsbitte von einer kurzen Denkpause.',
 'Gesprächsreaktionen als Wendung behalten. Bei der Wartebitte steht kurz vor warten und ください am Ende.')
guide('v11:hobbies','13:0 14:0 v11:small-ya v11:kata-long',
 'Nach einem Hobby fragen und Musik, Filme, Reisen oder Sport als Interesse benennen.',[
 'Bekannt: は … ですか, なん, が. Neu: しゅみ (shumi, Hobby), おんがく (ongaku, Musik), えいが (eiga, Film), りょこう (ryokō, Reise/Reisen), スポーツ (supōtsu, Sport). しゅみはなんですか fragt nach einem Hobby.',
 'Nomen + がすきです (ga suki desu) heißt ich mag dieses Nomen. すき ist hier kein Verb mit を; lerne das Muster mit が. Mit しゅみは…です wird direkt das Hobby genannt. Ein einzelnes Nomen wie しゅみ ist selbst noch keine Frage.',
 'In shumi und ryokō verbinden kleine ゅ bzw. ょ die Laute. In on-ga-ku bleibt n ein eigener Takt; ryokō und supōtsu haben langes ō. Mit diesen Wörtern kannst du später beim Kennenlernen eine Frage nach Interessen beantworten.'
 ],'Wiederhole das Fragewort なん und stelle die Hobbyfrage. Antworte einmal mit しゅみは…です, einmal mit …がすきです.',
 'Bei Vorlieben folgt がすきです auf das Nomen. Bei einer Hobbyfrage steht は nach しゅみ und か am Ende.')
guide('v11:dialog-meeting','v11:first-meeting v11:countries v11:languages v11:polite-past v11:hobbies',
 'Eine Vorstellung erwidern, Herkunft erfragen und einen Vorschlag für gemeinsames Lernen verstehen.',[
 'Wiederholung: はじめまして, Name + です, よろしくおねがいします, ドイツ, にほんご. Ren und Sakura sind die Namen der beiden Rollen. Beim eigenen Namen kein さん hinzufügen.',
 'どこから (doko kara) heißt woher; から bezeichnet hier den Ausgangsort. きました (kimashita) ist kam/bin gekommen, höfliche Vergangenheit von kommen. ドイツからきました nennt die Herkunft, nicht das Reiseziel. どこからきましたか ist im Kennenlernen eine Herkunftsfrage.',
 'いっしょに (issho ni) heißt gemeinsam; べんきょうしましょう (benkyō shimashō) ist lernen wir. Gegenüber べんきょうします wird die Endung zum gemeinsamen Vorschlag. shō und kyō sind lang. Für die Rückfrage im Gespräch: しゅみはなんですか, was ist Ihr Hobby?'
 ],'Rufe die Länder- und Hobbylektion ab. Antworte auf woher und stelle anschließend selbst die Hobbyfrage.',
 'Herkunft vor から; きました danach. Ein gemeinsamer Vorschlag endet auf ましょう statt auf die Frageendung か.')
guide('v11:dialog-directions','v11:directions v11:positions v11:here-there v11:smalltalk',
 'Eine Wegbeschreibung in ihrer Reihenfolge verstehen und Standort von Bewegung unterscheiden.',[
 'Wiederholung: すみません, えき, どこ, まっすぐ, ひだり, みぎ, あります. Neu: みち (michi, Weg/Straße), それから (sorekara, danach). このみち bezeichnet diese Straße; この benötigt das Nomen みち.',
 'このみちをまっすぐいってください: Straße + を markiert hier den durchquerten Weg, kein gegessenes oder bearbeitetes Objekt. Die feste Bitte いってください wurde bei den Richtungen erklärt. Erst geradeaus, danach (それから) links abbiegen.',
 'えきはみぎにあります nennt die Seite des Ziels nach diesen Schritten. Es fordert nicht zum Rechtsabbiegen auf. わかりました (wakarimashita) bestätigt verstanden; ありがとうございます bedankt sich. Kleine っ und das lange ō in arigatō beibehalten.'
 ],'Wiederhole の + Position und にあります aus der Ortslektion. Sage, ob rechts stehen und rechts abbiegen dasselbe bedeuten.',
 'Weg vor を, Richtung vor に. Die Bitte endet mit ください, die Standortangabe mit あります.')
guide('v11:read-profile','v11:jobs v11:hobbies v11:work-study v11:whose v11:relative-time',
 'Aus fünf Sätzen Name, Wohnland, Beruf, Hobby und Lernhäufigkeit korrekt entnehmen.',[
 'Wiederholung: わたしは…です, ドイツ, しごと, エンジニア, しゅみ, ゲーム (gēmu, Spiel), にほんごをべんきょうします. Neue Verbindung: まち (machi, Stadt) + にすんでいます (ni sunde imasu, wohne in). Die gesamte Wohnform wird vor der Prüfung erklärt.',
 'ドイツのまち ist eine Stadt in Deutschland, keine Aussage über die Staatsangehörigkeit. に markiert hier den Wohnort; すんでいます beschreibt einen bestehenden Zustand. まいにち (mainichi) heißt jeden Tag und steht hier ohne に.',
 'Beim Anwenden liest du den japanischen Satz und entnimmst nur die gefragte Information. Lesung und deutsche Hilfe kannst du bewusst öffnen. Beim Schreiben rufst du die Lesung selbst ab. gēmu hat langes ē; in mainichi werden die Vokale nicht verschluckt.'
 ],'Rufe Beruf und Hobby aus den früheren Lektionen ab: Welche zwei Angaben darfst du bei Ren nicht verwechseln?',
 'Thema vor は; im Wohnsatz steht Land – の – Stadt – に – Wohnform. Häufigkeit braucht hier kein に.')
guide('v11:read-day','v11:morning-evening v11:work-study v11:location-action v11:clock-hours v11:clock-minutes',
 'Uhrzeit, Verkehrsmittel und Tätigkeit eines Tagesablaufs aus fünf Sätzen entnehmen.',[
 'Wiederholung: おきます, いきます, かえります, よみます, ほん, バス und Uhrzeiten. Zusätzliche Wörter: まいあさ (maiasa, jeden Morgen), あさごはん (asagohan, Frühstück), パン (pan, Brot), よる (yoru, Abend/Nacht).',
 'しちじ ist 7 Uhr, はちじ 8 Uhr. ごごろくじ (gogo rokuji) ist 6 Uhr nachmittags/abends, also 18 Uhr. に markiert die bestimmte Uhrzeit; バスで das Verkehrsmittel. Eine Uhrzeit ohne Tageshälfte ist nicht automatisch morgens.',
 'あさごはんはパンです nennt das Frühstück; よるはほんをよみます die abendliche Handlung. Beim Anwenden bleibt der japanische Lesetext sichtbar, weitere Hilfen öffnest du selbst. Nach einem Fehler erkennst du, welcher Zeit- oder Handlungsbaustein verwechselt wurde.'
 ],'Wiederhole die fünf Fragen aus Ziel, Ort und Verkehrsmittel: Welche beantwortet バスで, welche はちじに?',
 'Zeit vor に, Verkehrsmittel vor で, gelesenes Objekt vor を. Das Verb steht zuletzt.')

# One focused transfer task per lesson; two explicitly explained distractors.
# These are authored independently, not copied from a textbook.
APPLICATIONS={
'v11:languages':('Du hörst ドイツご. Was wird genannt?','Die deutsche Sprache.',{'Die deutsche Staatsangehörigkeit.':'Eine Person wäre ドイツじん; ご benennt hier die Sprache.','Das Land Japan.':'Japan heißt にほん; hier steht der deutsche Länderstamm ドイツ mit ご.'}),
'v11:jobs':('Jemand fragt おしごとはなんですか. Welche Art Antwort wird gesucht?','Eine Berufsangabe.',{'Eine Uhrzeit.':'しごと nennt Arbeit oder Beruf; eine Uhrzeit würde mit なんじ erfragt.','Der Name der Person.':'Nach dem Namen fragt man mit なまえ. Hier geht es um しごと, den Beruf.'}),
'14:0':('In わたしはドイツじんです: Welche Aufgabe hat は?','Es setzt ich als Thema.',{'Es markiert Deutschland als Besitz.':'Besitz würde mit の verbunden; は steht hier nach わたし.','Es stellt eine Frage.':'Die Fragepartikel ist か am Satzende. は steht nach dem Thema.'}),
'15:0':('Vergleiche えきにいきます und くじにいきます. Was markiert に jeweils?','Zuerst das Ziel, dann die Uhrzeit.',{'In beiden Sätzen nur ein Verkehrsmittel.':'えき ist der Bahnhof und くじ neun Uhr. Ein Verkehrsmittel wie バス wird hier mit で begleitet.','Zuerst die Uhrzeit, dann das Ziel.':'えき bezeichnet einen Ort, くじ eine Uhrzeit. Die Reihenfolge wurde vertauscht.'}),
'16:0':('Du siehst eine Katze im Zimmer. Welches Existenzverb passt?','います',{'あります':'Für eine Katze als Tier wird hier います verwendet; あります gilt für Dinge und Pflanzen.','ですか':'ですか ist eine höfliche Frageendung, kein Existenzverb für eine Katze.'}),
'13:0':('Du kennst die Abfahrtszeit nicht. Welches Fragewort brauchst du?','いつ',{'どこ':'どこ fragt nach einem Ort. Gesucht ist aber der Zeitpunkt.','だれ':'だれ fragt nach einer Person. Hier fehlt eine Zeitangabe.'}),
'v11:this-that':('Ein Buch liegt direkt bei dir. Du zeigst darauf, ohne das Wort Buch zu nennen. Was passt?','これです。',{'それです。':'Im hier gemeinten räumlichen Gebrauch zeigt それ zum Gegenüber, nicht zu dir.','あれです。':'あれ bezeichnet hier etwas von beiden Personen Entferntes; das Buch liegt direkt bei dir.'}),
'v11:this-noun':('Du zeigst auf ein Buch direkt bei dir und nennst Buch ausdrücklich. Welche Form passt?','このほん',{'これほん':'これ steht selbstständig; direkt vor einem Nomen benötigst du この.','そのほん':'その zeigt hier zum Gegenüber. Das Buch liegt aber bei dir.'}),
'v11:whose':('In せんせいのペン: Wem wird der Stift zugeordnet?','Der Lehrkraft.',{'Der sprechenden Person.':'Mein Stift wäre わたしのペン; hier steht せんせい vor の.','Der Tasche.':'Eine Tasche heißt かばん. Vor の steht hier eine Lehrkraft, kein Gegenstand.'}),
'v11:here-there':('Du suchst den Standort einer Toilette. Welche Frage passt?','トイレはどこですか。',{'トイレはなんですか。':'なん fragt, was eine Toilette ist; gesucht ist hier ihr Ort.','だれですか。':'だれ fragt nach einer Person, nicht nach dem Standort.'}),
'v11:existence':('Du meldest eine Blume. Welches Muster passt?','はながあります。',{'はながいます。':'Pflanzen werden in diesem Grundmuster mit あります beschrieben.','ねこがいます。':'ねこ heißt Katze. Der Satz ist möglich, beschreibt aber nicht die Blume.'}),
'5:0':('In みずをのみます: Was ist das Objekt der Handlung?','Das Wasser.',{'Die trinkende Person.':'みず heißt Wasser; die Person ist nicht ausdrücklich genannt. を markiert nicht die handelnde Person.','Eine Uhrzeit.':'Eine bestimmte Uhrzeit würde hier mit に stehen; みず ist ein Getränk.'}),
'v11:morning-evening':('Du kommst nach einem Ausflug wieder nach Hause. Welches Verb betont die Rückkehr?','かえります',{'おきます':'おきます heißt aufstehen oder aufwachen, nicht zurückkehren.','ねます':'ねます heißt schlafen oder ins Bett gehen. Das nennt keine Rückkehr.'}),
'v11:work-study':('Im Satz なまえをかきます: Was tut die Person mit dem Namen?','Sie schreibt ihn.',{'Sie hört Musik.':'かきます heißt schreiben; hören wäre ききます. なまえ bedeutet Name, nicht Musik.','Sie liest ein Buch.':'Lesen wäre よみます; hier steht かきます und das Objekt なまえ.'}),
'v11:location-action':('Vergleiche いえでべんきょうします und バスでいきます. Was nennt で?','Zuerst den Handlungsort, dann das Verkehrsmittel.',{'In beiden Fällen den Besitzer.':'Besitz wird mit の verbunden. いえ ist hier der Lernort, バス das Mittel der Fahrt.','Zuerst das Reiseziel, dann die Uhrzeit.':'Hier stehen weder Ziel + に noch Zeit + に. Entscheidend sind Zuhause und Bus vor で.'}),
'v11:polite-past':('Du hast gestern nichts getrunken. Welche Form passt zur verneinten Vergangenheit?','のみませんでした',{'のみません':'ません verneint die Nichtvergangenheit; für gestern fehlt hier でした.','のみました':'ました ist Vergangenheit, aber bejaht. Es fehlt die Verneinung.'}),
'v11:rooms':('Im Satz つくえがあります: Warum passt あります?','Der Tisch ist ein Gegenstand.',{'Der Tisch ist eine Person.':'つくえ bezeichnet einen Tisch. Eine Person würde hier います benötigen.','Der Satz beschreibt eine Fahrt.':'あります beschreibt Vorhandensein; fahren oder gehen hieße beispielsweise いきます.'}),
'v11:positions':('In ほんはつくえのうえにあります: Wo ist das Buch?','Auf dem Tisch.',{'Unter dem Tisch.':'した hieße unter; hier steht うえ für oben/auf.','Im Tisch.':'なか hieße innen; hier steht die Ortsgruppe つくえのうえ.'}),
'v11:directions':('Die Anweisung lautet みぎにまがってください. Was tust du?','Rechts abbiegen.',{'Links abbiegen.':'Links heißt ひだり; hier steht みぎ.','Nur geradeaus weitergehen.':'Geradeaus heißt まっすぐ; まがって fordert zum Abbiegen auf.'}),
'v11:smalltalk':('Du möchtest ausdrücklich sagen: Bitte warten Sie kurz. Welche Wendung passt?','ちょっとまってください',{'ほんとうですか':'Das fragt wirklich? und bittet nicht ums Warten.','いいですね':'Das ist eine positive Reaktion, aber keine Wartebitte.'}),
'v11:hobbies':('Jemand fragt しゅみはなんですか. Welche Information möchte die Person?','Dein Hobby.',{'Deinen Beruf.':'Beruf heißt しごと; die Frage nennt しゅみ.','Deinen Wohnort.':'Ein Wohnort wird mit wo erfragt. しゅみ nennt ein Interesse oder Hobby.'}),
'v11:dialog-meeting':('Die Antwort ist ドイツからきました. Welche Frage passt dazu?','どこからきましたか。',{'おなまえは。':'Das fragt nach dem Namen. Die Antwort nennt mit ドイツから die Herkunft.','しゅみはなんですか。':'Das fragt nach einem Hobby. Deutschland mit から ist hier eine Herkunftsangabe.'}),
'v11:dialog-directions':('Du hörst えきはみぎにあります. Ist dies eine Aufforderung zum Abbiegen?','Nein, es beschreibt den Standort des Bahnhofs.',{'Ja, ich soll sofort rechts abbiegen.':'Eine Abbiegebitte hätte まがってください. あります nennt den Standort.','Ja, ich soll links abbiegen.':'Hier steht weder ひだり noch eine Abbiegebitte, sondern みぎにあります.'}),
'v11:read-profile':('Im Lesetext steht しごとはエンジニアです. Welche Angabe ist das?','Rens Beruf.',{'Rens Hobby.':'Das Thema ist しごと, Beruf; Hobby würde mit しゅみ beginnen.','Rens Wohnland.':'エンジニア benennt einen Beruf. Das Wohnland steht im separaten Satz mit ドイツ.'}),
'v11:read-day':('Im Tagesablauf steht はちじにバスでいきます. Was bezeichnet バスで?','Das Verkehrsmittel.',{'Die Abfahrtszeit.':'Die Zeit steht bereits als はちじに, um acht Uhr. バスで nennt den Bus als Mittel.','Den Ort, an dem die Person lernt.':'いきます beschreibt gehen/fahren. バスで ist hier das Verkehrsmittel, kein Lernort.'}),
}

LEGACY_EXPLAIN={
 '14:0':['は setzt das Thema. Geschrieben ha, als Themenpartikel wa gelesen.', 'が zeigt hier das neu genannte Wesen: ねこがいます, eine Katze ist da. は und が haben kontextabhängige Funktionen.', 'を liest du o und setzt es nach dem direkten Objekt: みずをのみます.', 'の verbindet zwei Nomen: わたしのほん ist mein Buch. Die Zuordnung steht vor dem Gegenstand.'],
 '15:0':['に markiert hier Ziel oder Zeitpunkt; bei Existenzsätzen auch den Standort.', 'へ markiert eine Richtung und wird als Partikel e gelesen, nicht he.', 'で markiert den Ort einer Handlung oder ihr Mittel; beides entscheidet der Kontext.', 'と heißt bei einer Begleitung mit und zwischen Nomen und. Die Zitatfunktion wird später vertieft.', 'も bedeutet auch und ersetzt im Beispiel わたしもいきます die Themenpartikel は.'],
 '16:0':['あります beschreibt in diesen Grundsätzen Dinge und Pflanzen, nicht Menschen und Tiere.', 'います beschreibt hier Menschen und Tiere. Das Anfangs-i unterscheidet es von あります.', 'どこにありますか fragt nach dem Standort eines Gegenstands: どこ wo + に Standort + あります + か Frage.'],
 '13:0':['なに und なん sind zwei Lesungen für was. Vor です steht hier なん; beide Einzelvarianten sind bei dieser Überblickskarte zulässig.', 'だれ fragt nach einer Person, nicht nach deren Ort oder Alter.', 'どこ fragt nach einem Ort; es heißt nicht wer oder wann.', 'いつ fragt nach einem Zeitpunkt; vor dem Verb ist hier kein に erforderlich.', 'どうして fragt nach einem Grund. Ein Ort oder eine Uhrzeit beantwortet diese Frage nicht.']
}

def upgrade():
    path=ROOT/'data/course.json'; data=json.loads(path.read_text('utf8'))
    lessons={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
    deep=json.loads((ROOT/'data/deep_lessons.json').read_text('utf8'))
    for key,authored in GUIDES.items():
        l=lessons[key];l['goal']=authored['goal'];l['study_guide']=copy.deepcopy(authored['study_guide'])
        # The previous reading intro incorrectly promised solutions in every task.
        if key=='v11:read-profile':l['intro']='Lies fünf Aussagen über Ren und entnimm Name, Wohnland, Beruf, Hobby und Lernhäufigkeit. Lesung und Bedeutung stehen beim Lernen und über die bewusst aufrufbare Hilfe bereit.'
        if key=='v11:jobs':l['intro']='Benenne einen Beruf mit Nomen + です und verstehe die höfliche Frage おしごとはなんですか. Die nötigen Wörter werden vor dem Üben erklärt.'
        for i,c in enumerate(l['cards']):
            p=copy.deepcopy(c.get('detail') or deep['profiles'].get(c['jp']) or {})
            if key in LEGACY_EXPLAIN:p['explain']=LEGACY_EXPLAIN[key][i]
            p.setdefault('explain',c['note']);p.setdefault('kind','Satzbau und Rückfragen')
            p.setdefault('usage',c['de']);p.setdefault('register','Höfliche Beispielsätze; einzelne Wörter haben für sich keine Höflichkeitsendung.')
            p.setdefault('parts',[]);p.setdefault('extra',[])
            p.setdefault('pitfall',authored['build'])
            if isinstance(c.get('example'),str):
                c['example']={'jp':c['example'],'romaji':c['example_romaji'],'de':c['example_de']}
            # Replace an early example that previously required unexplained past tense.
            if key=='14:0' and i==1:
                c['example']={'jp':'ねこがいます。','romaji':'neko ga imasu.','de':'Eine Katze ist da.'}
            if key=='14:0' and i==2:
                c['example']={'jp':'みずをのみます。','romaji':'mizu o nomimasu.','de':'Ich trinke Wasser.'}
            if key=='14:0' and i==3:
                c['example']={'jp':'わたしのほんです。','romaji':'watashi no hon desu.','de':'Das ist mein Buch.'}
            if key=='14:0' and i in (1,2,3):
                c['example_romaji']=c['example']['romaji'];c['example_de']=c['example']['de']
            scenario=p.get('scenario') or {'question':f'Welche Aussage über {c["jp"]} ist richtig?', 'correct':p['explain'],
                'wrong':[LEGACY_EXPLAIN[key][j] for j in range(len(l['cards'])) if j!=i][:3]}
            if 'dieser Karte' in scenario['question'] or 'dieser Lernkarte' in scenario['question']:
                scenario['question']=f'Welche Verwendung passt zu {c["jp"]}?'
            reasons={w:('Diese Auswahl beschreibt eine andere Funktion. '+p['explain']) for w in scenario['wrong']}
            for w in scenario['wrong']:
                other=next((x for x in l['cards'] if x is not c and x.get('detail',{}).get('usage')==w),None)
                if other:reasons[w]=f'Diese Beschreibung gehört zu {other["jp"]} ({other["romaji"]}). Hier gilt: '+p['explain']
            scenario['feedback']=reasons
            if i==0:
                question,correct,wrong=APPLICATIONS[key]
                scenario={'question':question,'correct':correct,'wrong':list(wrong),'feedback':wrong,
                          'explanation':'Die passende Antwort auf die Situation ist: '+correct}
            p['scenario']=scenario
            # Per-card notes refer to its sounds; never present these until a failed
            # response or an intentional hint. All useful existing profiles survive.
            p['feedback']={'build':authored['build'], 'write':c['note']+' Prüfe außerdem die vollständige Lesung und ihre Vokallängen.',
                           'listen':p['explain']}
            c['detail']=p
        if key=='13:0':
            l['cards'][0]['romaji_aliases']=['nani','nan']
            if not any(t['target']==l['cards'][0]['jp'] for t in l['speech']):
                l['speech'].append({'target':l['cards'][0]['jp'],'romaji':l['cards'][0]['romaji'],'meaning':'was', 'accept':['なに','なん','何']})
    # Add explicit, taught retrieval links without adding gates or learner fields.
    reprises={
      'v11:whose':['14:0','13:0','v11:languages'],
      'v11:existence':['16:0','v11:here-there'],
      'v11:location-action':['15:0','v11:work-study','v11:morning-evening'],
      'v11:positions':['v11:rooms','v11:whose'],
      'v11:dialog-meeting':['v11:jobs','v11:languages','v11:hobbies','v11:polite-past'],
      'v11:dialog-directions':['v11:directions','v11:positions','v11:here-there','v11:smalltalk'],
      'v11:read-profile':['v11:jobs','v11:hobbies','v11:languages','v11:work-study'],
      'v11:read-day':['5:0','v11:morning-evening','v11:location-action','v11:work-study']}
    for key,prior in reprises.items():lessons[key]['study_guide']['retrieves']=prior
    data['content_version']='11.0.3'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'package':2,'lessons':len(GUIDES),'cards':sum(len(lessons[k]['cards']) for k in GUIDES),'ids':list(GUIDES)},ensure_ascii=False,indent=2))

if __name__=='__main__':upgrade()
