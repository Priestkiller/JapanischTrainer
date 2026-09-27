"""Authored package 04: time, invitations and reuse. No progress migration.

Own review, not human linguistic approval. Historical packages stay intact
except the documented preparation of card 12:0:4 (same assessment targets).
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = {}
APPLICATIONS = {}

def guide(key, prerequisites, goal, points, recall, build, retrieves=''):
    GUIDES[key] = dict(goal=goal, study_guide=dict(revision=1, package=4,
        prerequisites=prerequisites.split(), points=points, recall=recall,
        retrieves=retrieves.split()), build=build)

def task(key, index, question, correct, wrong):
    APPLICATIONS[(key,index)] = dict(question=question, correct=correct,
        wrong=list(wrong), feedback=wrong, explanation='Zur Situation passt: '+correct)

guide('v11:people-age','v11:numbers-eleven v11:count-objects',
 'Eine bis drei Personen zählen und Altersangaben für zwanzig und dreißig davon unterscheiden.',[
 'ひとり hitori = eine Person, ふたり futari = zwei Personen, さんにん sannin = drei Personen. Das zählt Menschen: Zwei Gäste sind ふたり, zwei bestellte Dinge dagegen ふたつ. Mit です wird daraus eine höfliche Antwort, etwa ふたりです, wir sind zu zweit.',
 'Alter: はたち hatachi heißt zwanzig Jahre alt; さんじゅっさい sanjussai dreißig Jahre alt. さい sai zählt Lebensjahre, にん nin Personen. Die Zahl allein beantwortet noch nicht beide Fragen. Für dreißig Jahre kommt auch さんじっさい sanjissai vor; hier übst du die angegebene Form.',
 'Sprich hi-to-ri, fu-ta-ri und ha-ta-chi in kurzen Takten. Bei san-nin stehen zwei n hintereinander; sanjussai enthält eine Pause vor s. Im Beispiel ひとりです entscheidet die Situation, ob jemand allein kommt oder eine Person gemeint ist.'
 ],'Du reservierst für zwei Gäste. Antworte mit der Personenanzahl und nenne danach getrennt das Alter zwanzig.',
 'Personenzahl mit ひとり・ふたり・にん; Alter mit はたち oder さい.','v11:count-objects v11:numbers-eleven')

guide('12:1','v11:people-age v11:numbers-six-ten',
 'Eine Frage nach der jetzigen Uhrzeit von einer Altersfrage unterscheiden und sieben Uhr nennen.',[
 'いま ima = jetzt; なんじ nanji = wie viel Uhr. いまなんじですか fragt nach der jetzigen Uhrzeit. じ ji kennzeichnet eine Uhrzeit. Neu im Beispiel: さんじ sanji = drei Uhr; いまさんじです bedeutet jetzt ist es drei Uhr.',
 'しちじ shichiji ist die hier geübte Form für sieben Uhr. Die Grundzahl なな nana wird also nicht einfach unverändert übernommen. なんさい nansai fragt dagegen wie alt. Antworte darauf mit einer Altersangabe wie dem bekannten さんじゅっさいです, ich bin dreißig.',
 'Eine Altersfrage ist persönlich; die höfliche Satzform allein macht sie nicht in jeder Begegnung passend. Nan-ji enthält den n-Takt vor ji; shi-chi-ji besteht aus drei kurzen Silbentakten. Die ganze Frage endet auf ですか, eine Antwort nur auf です.'
 ],'Jemand antwortet mit sieben Uhr. Welche Frage könnte davor stehen? Warum passt die Altersfrage nicht?',
 'いま – なんじ – ですか fragt nach jetzt; なんさい – ですか nach dem Alter.','v11:people-age')

guide('v11:weekdays','12:1 v11:long-vowels',
 'Alle sieben Wochentage zuordnen und Samstag von Sonntag für eine Verabredung unterscheiden.',[
 'Erste Gruppe: げつようび getsuyōbi Montag, かようび kayōbi Dienstag, すいようび suiyōbi Mittwoch. Zweite Gruppe: もくようび mokuyōbi Donnerstag, きんようび kinyōbi Freitag. Wochenende: どようび doyōbi Samstag und にちようび nichiyōbi Sonntag.',
 'ようび yōbi ist der gemeinsame Teil für Wochentag. なんようび nanyōbi fragt welcher Wochentag; das ist nicht die Uhrzeitfrage なんじ. どようびです bedeutet es ist Samstag. Die Kalenderzeichen 月・火・水・木・金・土・日 stehen in dieser Reihenfolge für Montag bis Sonntag; sie werden hier nur als Lesehilfe eingeführt.',
 'In allen sieben Wörtern bleibt yō lang. Kinyōbi behält den n-Takt vor yō; suiyōbi beginnt su-i. Lerne zuerst die drei Gruppen, rufe danach einzelne Tage in gemischter Reihenfolge ab. Ein Wochentag legt noch keine Stunde fest.'
 ],'Ein Treffen soll nicht am Samstag, sondern am Sonntag sein. Nenne den neuen Tag, dann den vorherigen Freitag.',
 'Verschiedener Tagesanfang, gemeinsames ようび; Samstag beginnt ど, Sonntag にち.','12:1')

guide('v11:clock-hours','12:1 v11:numbers-six-ten',
 '1, 4, 7 und 9 Uhr lesen und 2:30 von 3:30 unterscheiden.',[
 'Uhrzeiten: いちじ ichiji 1 Uhr, よじ yoji 4 Uhr, しちじ shichiji 7 Uhr, くじ kuji 9 Uhr. Merke die Sonderlesungen als ganze Formen: vier Uhr hat kein n, neun Uhr kein langes ū. Zusätzlich für Beispiele: にじ niji 2 Uhr, さんじ sanji 3 Uhr, じゅうじ jūji 10 Uhr.',
 'はん han = halb, nach einer Uhrzeit eine halbe Stunde später. にじはん niji han ist zwei Uhr plus eine halbe Stunde: 2:30, auf Deutsch halb drei. さんじはん sanji han wäre 3:30, halb vier. Gehe beim Umrechnen immer von der genannten vollen Stunde aus.',
 'Eine Antwort kann auf です enden: よじです, es ist vier Uhr. Uhrzeiten allein unterscheiden noch nicht morgens und nachmittags. Sprich yo-ji und ku-ji kurz, jū-ji mit langem ū. Han endet auf einen eigenen n-Takt.'
 ],'Lies 4:00, 9:00 und 2:30 in anderer Reihenfolge. Erkläre, warum halb drei auf Japanisch mit zwei beginnt.',
 'Genannte Stunde – じ – gegebenenfalls はん; halb bezieht sich auf die bereits erreichte Stunde.','12:1 v11:numbers-six-ten')

guide('v11:clock-minutes','v11:clock-hours v11:small-tsu',
 '1, 5 und 10 Minuten sowie 9 Uhr vormittags und 15 Uhr unterscheiden.',[
 'Minuten: いっぷん ippun 1 Minute, ごふん gofun 5 Minuten, じゅっぷん juppun 10 Minuten. Für zehn Minuten ist auch じっぷん jippun gebräuchlich. Die Formen werden hier einzeln gelernt; Zahl + fun wird nicht immer unverändert zusammengesetzt. なんぷん nanpun fragt wie viele Minuten.',
 'ごぜん gozen steht vor einer Uhrzeit am Vormittag, ごご gogo am Nachmittag: ごぜんくじ = 9 Uhr, ごごさんじ = 15 Uhr. Für spätere Termine außerdem: ごぜんじゅうじ gozen jūji = 10 Uhr vormittags; ごごにじ gogo niji = 14 Uhr. Eine Dauer von fünf Minuten ist keine Uhrzeit fünf Uhr.',
 'In ippun und juppun liegt eine kurze Verschlusspause vor p; in gofun nicht. Das z in gozen ist stimmhaft. Für spätere Wegfragen: あるいて aruite = zu Fuß, ぐらい gurai = ungefähr. あるいてごふんぐらいです heißt es sind ungefähr fünf Minuten zu Fuß; keine genaue Startzeit.'
 ],'Jemand fragt nach der Dauer des Wegs. Antworte fünf Minuten. Nenne danach getrennt einen Treffzeitpunkt um 15 Uhr.',
 'Tageshälfte vor der Stunde; Minutenzahl vor ふん oder ぷん.','v11:clock-hours v11:numbers-six-ten')

guide('v11:calendar','v11:people-age v11:clock-hours',
 'Januar, April, September und den ersten/zwanzigsten Monatstag vom Alter unterscheiden.',[
 'Monate: いちがつ ichigatsu Januar, しがつ shigatsu April, くがつ kugatsu September. がつ gatsu kennzeichnet hier den Monatsnamen. Vier und neun haben wie bei bestimmten Uhrzeiten besondere Lesungen; lerne しがつ und くがつ als ganze Wörter.',
 'ついたち tsuitachi bezeichnet den Ersten eines Monats, はつか hatsuka den Zwanzigsten. はつか kann auch eine Dauer von zwanzig Tagen bedeuten; das einzelne Wort legt den Kontext nicht fest. しがつついたち shigatsu tsuitachi = 1. April: Monat zuerst, danach der Tag.',
 'Vergleiche はつか hatsuka, zwanzigster Tag, mit はたち hatachi, zwanzig Jahre alt. Eine Dauer von einem Tag heißt いちにち ichinichi und nicht ついたち. Diese Ausnahme wird erklärt, aber weitere unbekannte Datumslesungen werden hier nicht verlangt.'
 ],'Lies den 1. April. Nenne dann zwanzig Jahre alt und den zwanzigsten Monatstag, ohne die Endungen zu vertauschen.',
 'Monat vor Kalendertag; はつか und はたち haben verschiedene Zählerfunktionen.','v11:people-age v11:clock-hours')

guide('v11:relative-time','v11:weekdays v11:clock-hours 2:0',
 'Gestern, heute, morgen, jeden Tag und nächste Woche in einfachen Beispielen zeitlich einordnen.',[
 'きのう kinō gestern, きょう kyō heute, あした ashita morgen (nächster Tag), まいにち mainichi jeden Tag, らいしゅう raishū nächste Woche. Das deutsche morgen ist hier keine Tageszeit; der Morgen als Tageszeit heißt あさ asa. 毎日 und 来週 sind häufige Schreibungen für mainichi und raishū.',
 'Vor den Beispielen: やすみ yasumi = frei/Pause, いきます ikimasu = gehe/fahre, べんきょうします benkyō shimasu = lerne. やすみです heißt habe frei, やすみでした hatte frei. Bei diesem Nomen macht でした die Aussage vergangen. あしたいきます beschreibt mit derselben höflichen Verbform einen Plan für morgen.',
 'Diese Zeitwörter können direkt vor dem Satz stehen; für heute oder morgen braucht man hier kein に. まいにち beschreibt Wiederholung, らいしゅう eine kommende Woche. Kinō und kyō haben langes ō, raishū langes ū. Die Endung des Satzes und das Zeitwort gemeinsam lesen.'
 ],'Ordne einen freien Tag gestern und einen geplanten Weg morgen ein. Welches Wort würde tägliche Wiederholung ausdrücken?',
 'Zeitwort zuerst möglich; です und でした unterscheiden den heutigen vom vergangenen freien Tag.','v11:weekdays 2:0')

guide('v11:frequency','v11:relative-time v11:polite-past v11:work-study',
 'Regelmäßigkeit, gelegentliche Handlung, wenig/selten und überhaupt nicht auseinanderhalten.',[
 'いつも itsumo immer/gewöhnlich, よく yoku oft, ときどき tokidoki manchmal. Die Abstufungen sind keine festen Prozentzahlen. Beispiele nutzen bekannte Formen: ほんをよみます lese Bücher, みずをのみます trinke Wasser. ゲーム gēmu = Spiel; ゲームをします heißt ich spiele.',
 'あまり amari steht in den hier geübten Sätzen mit Verneinung: あまりのみません trinke nicht viel/nicht oft. ぜんぜん zenzen + ません verneint ganz: ぜんぜんみません schaue überhaupt nicht. テレビ terebi heißt Fernsehen. Ohne die Verneinung wäre die gelernte Aussage nicht mehr dieselbe.',
 'Im Kontext einer Gewohnheit bedeutet よく oft; es kann anderswo gut heißen. いつも und ときどき werden nicht mit に an das Verb gehängt. Tokidoki hat stimmhaftes d im zweiten toki-Teil; in zenzen ist z stimmhaft. Halte bei gēmu das ē lang.'
 ],'Beschreibe tägliches Lernen mit まいにち. Tausche dann nur die Häufigkeit gegen manchmal; verneine anschließend Fernsehen vollständig.',
 'あまり und ぜんぜん passen hier zur negativen Verbendung ません.','v11:relative-time v11:polite-past')

guide('v11:seasons','v11:calendar v11:relative-time v11:food-preferences',
 'Vier Jahreszeiten zuordnen und Jahreszeit von Monat und Wetter unterscheiden.',[
 'はる haru Frühling, なつ natsu Sommer, あき aki Herbst, ふゆ fuyu Winter. きせつ kisetsu ist der Oberbegriff Jahreszeit, keine fünfte Jahreszeit. Alle fünf Wörter sind Nomen. Ein Monatsname wie しがつ benennt dagegen einen Kalenderabschnitt.',
 'いまははるです (ima wa haru desu) heißt jetzt ist Frühling. Die Beispiele fragen nach Vorlieben: はるがすきです, ich mag den Frühling; どのきせつがすきですか, welche Jahreszeit mögen Sie? どの dono fragt welches vor einem Nomen. あつい atsui heiß und さむい samui kalt sind Eigenschaften; eine Jahreszeit legt das Wetter eines Tages nicht fest.',
 'Haru, natsu, aki und fuyu haben jeweils zwei kurze Vokale; kisetsu drei Takte ki-se-tsu. Sprich fu mit sanftem Luftstrom, nicht wie ein kräftiges deutsches f. Ein Satz wie ふゆです ist eine jahreszeitliche Angabe, keine Datumsangabe.'
 ],'Nenne einen Monat und eine Jahreszeit getrennt. Welche Jahreszeit folgt in der üblichen Reihenfolge auf den Sommer?',
 'Jahreszeit als Nomen vor です; きせつ ist der Sammelbegriff.','v11:calendar v11:relative-time')

guide('v11:weather-words','v11:seasons v11:taste v11:relative-time',
 'Sonne, Regen und Schnee benennen und Kälte der Umgebung von kaltem Wasser unterscheiden.',[
 'はれ hare klares/sonniges Wetter, あめ ame Regen und ゆき yuki Schnee sind Nomen. てんき tenki bedeutet Wetter. Mit dem bekannten Tageswort: きょうはあめです (kyō wa ame desu), heute regnet es. Du musst hier kein neues Wetterverb bilden.',
 'さむい samui beschreibt kaltes Wetter beziehungsweise dass jemand friert. つめたい tsumetai aus der Getränkelektion beschreibt beispielsweise kaltes Wasser. あたたかい atatakai heißt warm und kann Wetter oder Gegenstände beschreiben. Wetter und Getränketemperatur haben also nicht in jeder Richtung dasselbe Wort.',
 'Lies sa-mu-i und a-ta-ta-ka-i mit ihren Vokalen; die zwei ta nicht zusammenziehen. ゆき yuki hat kurzes u. あめ kann ohne Schrift und Kontext auch ein anderes Wort bezeichnen; in diesen Wetterbeispielen ist Regen gemeint. Der Kurs vergibt keine Tonhöhenbewertung.'
 ],'Beschreibe einen kalten Tag und kaltes Wasser mit den unterschiedlichen Adjektiven. Wiederhole danach das Wort für Schnee.',
 'Wetter-Nomen oder Eigenschaft vor です; Umgebungskälte heißt さむい.','v11:taste v11:relative-time')

guide('v11:adjective-time','17:0 v11:weather-words v11:rooms v11:relative-time',
 'Gegenwart, Vergangenheit und verneinte Vergangenheit bei den erklärten Adjektiven unterscheiden.',[
 'Bei い-Adjektiven verändert sich das Adjektiv: あつい atsui heiß → あつかった atsukatta war heiß. さむい samui kalt → さむくない samukunai nicht kalt → さむくなかった samukunakatta war nicht kalt. です macht diese Sätze höflich; nicht zusätzlich でした anhängen.',
 'いい ii gut verwendet beim Beugen den Stamm よ: よかった yokatta war gut. Neu erklärtes Beispiel: てんきがよかったです (tenki ga yokatta desu), das Wetter war gut. しずか shizuka ruhig ist ein な-Adjektiv: しずかでした war ruhig; hier verändert sich die höfliche Endung.',
 'きのうは gestern und きょうは heute legen den Zeitbezug fest. へや heya ist das bekannte Zimmer. きのうはさむくなかったです berichtet ausdrücklich keine Kälte gestern, nicht bloß keine Kälte jetzt. In katta steckt eine Pause vor t; in shizuka ist z stimmhaft.'
 ],'Sage nicht kalt für heute und für gestern. Beschreibe danach ein Zimmer rückblickend als ruhig.',
 'い-Adjektiv: かった / くない / くなかった; な-Adjektiv: でした.','17:0 v11:weather-words v11:relative-time')

guide('v11:feelings','v11:adjective-time v11:polite-past',
 'Schläfrigkeit, Erschöpfung, Freude und Spaß als unterschiedliche Aussagen über Befinden erkennen.',[
 'げんきです genki desu = mir geht es gut/bin fit; ねむいです nemui desu = bin schläfrig. つかれました tsukaremashita berichtet Erschöpfung nach Anstrengung. Das Bedürfnis zu schlafen und Müdigkeit nach einer Tätigkeit sind nicht genau dasselbe.',
 'うれしい ureshii = erfreut, たのしい tanoshii = macht Spaß. すこし sukoshi etwas und とても totemo sehr sind Gradangaben: すこしねむいです, etwas schläfrig. べんきょう benkyō ist Lernen; べんきょうはたのしいです bewertet diese Tätigkeit als angenehm.',
 'げんき ist ein な-Adjektiv; ねむい・うれしい・たのしい sind い-Adjektive. Das lange ii in ureshii und tanoshii bleibt. Die ました-Form in つかれました kann einen jetzt spürbaren Zustand ausdrücken. Aus diesen Alltagssätzen lässt sich keine Diagnose ableiten.'
 ],'Eine Tätigkeit macht dir Spaß, danach bist du erschöpft. Formuliere die beiden Aussagen getrennt; welche Form würde stattdessen Schlafbedarf nennen?',
 'Das Zustandswort entscheidet: ねむい ist schläfrig, つかれました berichtet Erschöpfung.','v11:adjective-time v11:polite-past')

guide('v11:games','v11:hobbies v11:frequency v11:polite-past',
 'Gemeinsames Spielen, Sieg, Niederlage und den Wunsch nach einer weiteren Runde unterscheiden.',[
 'ゲームをします gēmu o shimasu = spiele ein Spiel. いっしょに issho ni = gemeinsam; あそびます asobimasu = spiele/verbringe Freizeit. ともだち tomodachi Freund und と als Begleitung ergeben ともだちといっしょにあそびます, ich spiele mit einem Freund.',
 'かちます kachimasu gewinnen → かちました habe gewonnen. まけます makemasu verlieren → まけました habe verloren, hier einen Wettbewerb. Das ist nicht なくしました für einen verlorenen Gegenstand. Beide Beispiele verwenden die schon erklärte höfliche Vergangenheit.',
 'もう mō hier noch, いっかい ikkai einmal: もういっかい bedeutet noch einmal/noch eine Runde. Mit おねがいします wird eine Bitte daraus. Gēmu und mō enthalten lange Vokale; issho und ikkai haben einen verdoppelten Konsonantentakt. よく wiederholt das bekannte oft.'
 ],'Berichte einen Sieg gestern und bitte dann um eine weitere Runde. Welche andere Form würde eine Niederlage melden?',
 'かちました ist Sieg, まけました Niederlage; もういっかい bittet um Wiederholung.','v11:frequency v11:polite-past v11:travel-help')

guide('v11:media-actions','v11:hobbies v11:games v11:location-action',
 'Film schauen, Manga lesen, Musik hören, fotografieren und singen mit dem passenden Verb verbinden.',[
 'えいが eiga Film + みます mimasu schauen; まんが manga Comic + よみます yomimasu lesen; おんがく ongaku Musik + ききます kikimasu hören. Das Objekt steht mit を vor dem Verb. Ein Wort kann mehrere Bedeutungen haben: ききます meint hier hören, nicht nachfragen.',
 'しゃしん shashin Foto + とります torimasu aufnehmen, うた uta Lied + うたいます utaimasu singen. Vor dem Beispiel: こうえん kōen = Park; こうえんでしゃしんをとります heißt im Park Fotos machen. で zeigt den Handlungsort, を das Aufgenommene.',
 'いえで ie de zu Hause, よく yoku oft, まいにち mainichi jeden Tag sind Wiederholungen. にほんごのうた ist ein japanisches Lied; の ordnet die Sprache zu. Kōen hat langes ō, shashin einen n-Takt. Verb und Gegenstand zusammen abrufen, nicht nur das erste Wort erkennen.'
 ],'Tausche beim Satz über einen Film die Tätigkeit gegen Musik hören. Nenne danach den Ort, an dem du Fotos machst.',
 'Objekt – を – passendes Verb; Ort – で kann davor stehen.','v11:location-action v11:frequency v11:hobbies')

guide('v11:inviting','v11:media-actions v11:weekdays v11:polite-past',
 'Mit ませんか zu einer gemeinsamen Tätigkeit einladen und nach einem passenden Termin fragen.',[
 'Aus いきます ikimasu wird die Einladungsfrage いきませんか ikimasen ka. Obwohl darin die Verneinungsform steckt, bedeutet sie hier möchten wir gehen? いっしょに issho ni betont gemeinsam. Ohne か wäre いきません eine negative Aussage statt dieser Einladung.',
 'Das gleiche Muster mit bekannten Tätigkeiten: えいがをみませんか wollen wir einen Film schauen; おちゃをのみませんか wollen wir Tee trinken. を und das Objekt bleiben. いつ itsu fragt wann; いつがいいですか fragt nach einem passenden Zeitpunkt.',
 'Termin vorschlagen: どようびはどうですか (doyōbi wa dō desu ka), wie wäre es mit Samstag? は stellt Samstag zur Wahl, どうですか erbittet eine Einschätzung. In doyōbi und dō ist ō lang. Eine Einladung garantiert noch keine Zusage; die Antwort muss abgewartet werden.'
 ],'Lade jemanden zum Filmschauen ein. Frage erst offen nach einem Termin, schlage dann Samstag vor.',
 'ます durch ませんか ersetzen; ein Terminangebot kann mit はどうですか folgen.','v11:media-actions v11:weekdays v11:polite-past')

guide('v11:reply-invites','v11:inviting v11:existence v11:checkout',
 'Einladung annehmen, einen Tag höflich ablehnen und eine noch unverbindliche spätere Möglichkeit nennen.',[
 'いいですね ii desu ne = gute Idee; いきましょう ikimashō = gehen wir. Dafür wird bei いきます die Endung ます durch ましょう ersetzt. Neu als wiederverwendbarer Vorschlag: しましょう shimashō machen wir. だいじょうぶです bestätigt hier einen passenden Termin.',
 'どようびはちょっと (doyōbi wa chotto) deutet an, dass Samstag nicht gut passt; nicht als feste Zusage lesen. ようじ yōji eine Erledigung/Verpflichtung + があります ich habe: ようじがあります, ich habe etwas vor. そのひ sono hi = an dem Tag, aus その dieser/jener und ひ Tag.',
 'またこんどおねがいします (mata kondo onegai shimasu) lässt ein anderes Mal offen, vereinbart aber keinen neuen Tag. だいじょうぶ ist situationsabhängig: Beim Termin hier Zustimmung, bei der Tütenfrage zuvor eine mögliche Absage. ましょう hat langes ō, ちょっと eine Pause vor t.'
 ],'Sage Samstag höflich ab und lasse ein anderes Mal offen. Warum ist damit noch kein Sonntagstermin vereinbart?',
 'ましょう schlägt Gemeinsamkeit vor; はちょっと signalisiert in diesem Kontext ein Problem.','v11:inviting v11:checkout')

guide('23:0','v11:media-actions v11:reply-invites v11:relative-time',
 'Vier Wörterbuchformen den bekannten höflichen Formen zuordnen und ihren Zeitbezug aus dem Kontext lesen.',[
 'Wörterbuchform bedeutet Nachschlageform, keine neue Zeitstufe: たべる taberu essen ↔ たべます, いく iku gehen/fahren ↔ いきます, する suru machen ↔ します, くる kuru kommen ↔ きます. する und くる folgen eigenen Wechseln. Wie die Gruppen funktionieren, wird in der nächsten Einheit vertieft.',
 'Die neutrale Form kann in vertrauter Rede stehen; sie bedeutet nicht automatisch einen Befehl. Mit あした morgen ist あしたとうきょうへいく ein zukünftiger Weg nach Tokio. とうきょう Tōkyō ist der Ortsname; へ liest man als Zielmarkierung e.',
 'Vor den Beispielen: しゅくだい shukudai Hausaufgaben; しゅくだいをする heißt Hausaufgaben machen. ともだちがくる meldet, dass ein Freund kommt. Sushi und Freund sind bekannt. Kuru und suru haben kurze Vokale, Tōkyō zwei lange ō. Wähle die Höflichkeit passend zur Situation.'
 ],'Ordne きます und します ihren Grundformen zu. Lies dann einen Satz mit morgen, ohne die Grundform als Vergangenheit zu verstehen.',
 'たべる ↔ たべます, いく ↔ いきます; する und くる wechseln unregelmäßig.','v11:media-actions v11:relative-time')

guide('v11:verb-groups','23:0 v11:media-actions v11:work-study',
 'Die fünf erklärten Verben ihrer Gruppe zuordnen und die passende höfliche Form auswählen.',[
 'Ichidan-Verben behalten hier einen Stamm: たべる taberu → たべます tabemasu; みる miru → みます mimasu. Das Schluss-る fällt weg. Die Beispielobjekte パン Brot und えいが Film sind bereits bekannt.',
 'Godan-Verben ändern den letzten Laut für ます. Gegenbeispiel zur bloßen Endung: かえる kaeru zurückkehren → かえります kaerimasu. Trotz eru ist dieses Verb Godan. いえにかえります heißt nach Hause zurückkehren; いえ Haus und に als Ziel sind bekannt.',
 'Unregelmäßig: する suru → します shimasu; くる kuru → きます kimasu. べんきょうします lerne und あしたきます komme morgen zeigen beide im Kontext. Keine Regel alle Verben auf iru/eru sind Ichidan ableiten; diese fünf Gruppenangaben ausdrücklich mitlernen.'
 ],'Eine Person kehrt nach Hause zurück. Wähle die höfliche Form von かえる und erkläre, warum das Weglassen von る allein hier nicht reicht.',
 'Nur bei den erklärten Ichidan-Verben る durch ます ersetzen; かえる wird かえります.','23:0 v11:work-study')

guide('7:0','v11:verb-groups v11:polite-past v11:inviting',
 'Bejahung, Verneinung, Vergangenheit und die verbindende て-Form von essen auseinanderhalten.',[
 'Mit dem Stamm たべ tabe: たべます tabemasu esse/werde essen, たべません tabemasen esse nicht/werde nicht essen, たべました tabemashita habe gegessen. Zeitwörter wie あした morgen oder きのう gestern machen den Bezug deutlich. Die Höflichkeitsendung allein nennt keine Person.',
 'たべて tabete ist die て-Form von たべる, noch kein vollständiger höflicher Aussagesatz. Bei diesem Ichidan-Verb fällt る weg, dann folgt て. Bekanntes ください macht daraus たべてください, bitte essen Sie. Die systematischen Formen anderer Verben werden später behandelt.',
 'Vergleiche たべません mit たべませんか: Erst die Frageendung ergibt im Einladungskontext die gelernte Einladung. たべて berichtet keine Vergangenheit; dafür steht hier たべました. Sprich tabe-te und tabe-mashita verschieden; die Formen sind keine frei austauschbaren Endungen.'
 ],'Berichte, dass du gestern gegessen hast. Lade danach jemanden zum Essen ein und unterscheide beides von der て-Form.',
 'ます bejaht, ません verneint, ました blickt zurück; て verbindet mit einer weiteren Wendung.','v11:polite-past v11:inviting 23:0')

guide('v11:appointments','v11:clock-minutes v11:reply-invites v11:workday',
 'Beginn und Ende erfragen, eine Uhrzeit festlegen und einen alternativen Tag vorschlagen.',[
 'から kara markiert bei Uhrzeiten den Beginn, まで made das Ende. なんじからですか fragt ab wann, なんじまでですか bis wann. かいぎ kaigi Besprechung und しごと shigoto Arbeit sind die bekannten Themen: かいぎはなんじからですか fragt nach dem Beginn der Besprechung.',
 'にじにしましょう (niji ni shimashō) schlägt zwei Uhr als gemeinsame Wahl vor. Hier gehört に zu にします, sich entscheiden/festlegen. Ohne Tageshälfte ist die Uhrzeit mehrdeutig; mit ごごにじ sind 14 Uhr gemeint. きょうはむずかしいです bedeutet im Terminkontext heute passt es schlecht.',
 'あしたでもいいですか (ashita demo ii desu ka) fragt, ob auch morgen als Alternative geht. でも bedeutet hier auch bei dieser Wahl, nicht einfach aber. Sprich mu-zu-ka-shii mit langem ii, shimashō mit langem ō. Eine Frage nach einer Alternative ist noch keine bestätigte Verschiebung.'
 ],'Erfrage Anfang und Ende eines Termins. Schlage 14 Uhr vor; frage danach, ob stattdessen morgen möglich wäre.',
 'から = Anfang, まで = Ende; Alternative + でもいいですか fragt nach einer Möglichkeit.','v11:clock-minutes v11:reply-invites')

guide('v11:messages','v11:appointments v11:wishes v11:feelings',
 'Eine höfliche Nachricht in Gruß, Dank, Änderungswunsch, Antwortbitte und Abschluss gliedern.',[
 'おつかれさまです otsukaresama desu ist eine übliche kollegiale Wendung, keine wörtliche Meldung eigener Müdigkeit. れんらく renraku Nachricht/Kontaktaufnahme + ありがとうございます ergibt den Dank für die Mitteilung. Der passende Gruß hängt von Beziehung und Anlass ab.',
 'じかん jikan Zeit/Uhrzeit, へんこう henkō Änderung; へんこうする heißt ändern. Mit bekanntem Wunschmuster: じかんをへんこうしたいです, ich möchte die Uhrzeit ändern. へんじ henji heißt dagegen Antwort; へんじをおねがいします bittet darum, ohne den Änderungswunsch bereits als angenommen auszugeben.',
 'では、またあした (dewa, mata ashita) schließt mit dann bis morgen. Das ist keine neue Uhrzeit. Henkō und arigatō haben lange ō, henji ein n vor ji. Nutze diese Bausteine bewusst nach Funktion; eine höfliche Nachricht braucht nicht in jedem Fall alle fünf.'
 ],'Du möchtest den Termin ändern. Wähle Änderungswunsch und Antwortbitte; welche Rückmeldung müsste kommen, bevor du den neuen Termin als vereinbart behandelst?',
 'へんこう ist Änderung, へんじ Antwort; を markiert jeweils das gewünschte Objekt.','v11:appointments v11:wishes v11:relative-time')

guide('v11:dialog-weekend','v11:inviting v11:reply-invites v11:appointments v11:wishes v11:positions',
 'Gemeinsam Tätigkeit, Tag, Uhrzeit und Treffpunkt vereinbaren und die vier Angaben getrennt bestätigen.',[
 'Wiederhole Sonntag にちようび nichiyōbi, Park こうえん kōen, Bahnhof えき eki und 前/まえ mae davor. あいます aimasu heißt sich treffen; あいましょう aimashō treffen wir uns. えきのまえで markiert den Ort der Handlung. たのしみにしています tanoshimi ni shite imasu ist die feste Wendung ich freue mich darauf, anders als gerade Spaß haben.',
 'Vor der Offline-Szene: 週末/しゅうまつ shūmatsu Wochenende, 一緒に/いっしょに issho ni gemeinsam, 出かけませんか/でかけませんか dekakemasen ka wollen wir ausgehen/etwas unternehmen. 何をしたいですか/なにをしたいですか nani o shitai desu ka fragt nach dem Wunsch. Antworten: えいがをみたいです Film sehen, カフェにいきたいです ins Café, こうえんにいきたいです in den Park.',
 'Die Szene bietet Samstag oder Sonntag, 10 Uhr vormittags oder 14/15 Uhr sowie Bahnhofsvorplatz oder vor dem Café. どようびがいいです wählt Samstag; ごごにじがいいです wählt 14 Uhr. 何時に会いましょうか/なんじにあいましょうか fragt nach der Treffzeit. カフェのまえはどうですか schlägt den Cafévorplatz vor; はい、いいですね stimmt dem Bahnhof zu. Im Abschluss verbindet の Tag und Uhrzeit, に markiert die Zeit, で den Ort; 楽しみです/たのしみです heißt freue mich darauf. Andere freie Vorschläge sind nicht vollständig unterstützt.'
 ],'Plane erst Film, Samstag, 10 Uhr, Bahnhof; danach Park, Sonntag, 14 Uhr, Cafévorplatz. Halte Wunsch und bestätigten Termin auseinander.',
 'Tätigkeit, Tag, Uhrzeit und Treffpunkt beantworten jeweils eine andere Frage.','v11:weekdays v11:clock-minutes v11:media-actions v11:inviting v11:appointments v11:positions')

guide('v11:read-weekend','v11:dialog-weekend v11:media-actions v11:adjective-time v11:relative-time',
 'Aus fünf Sätzen Zeitpunkt, Begleitung, Ziel, Wetter und Tätigkeit eines vergangenen Ausflugs entnehmen.',[
 'Wiederholung: きのう gestern + やすみでした hatte frei; ともだちと mit einem Freund, こうえんに in den Park, いきました bin gegangen. と markiert die Begleitung, に das Ziel. Lese zuerst das Zeitwort und das Satzende; die Erzählung berichtet über gestern.',
 'てんきはよかったです bedeutet das Wetter war gut, mit der bekannten Sonderform von いい. Neu im Fotobeispiel: たくさん takusan = viel/viele. しゃしんをたくさんとりました heißt habe viele Fotos gemacht, ohne genaue Anzahl. とてもたのしかったです (totemo tanoshikatta desu) verbindet sehr mit hat Spaß gemacht.',
 'Die Vorlage bleibt in den Leseaufgaben sichtbar; ihre deutsche Bedeutung erscheint bei bewusster Hilfe oder nach der Antwort. Behaupte nichts, was im Text fehlt: Ein Freund nennt keinen Namen, viele Fotos keine Uhrzeit. In kinō und kōen bleibt ō lang; katta enthält eine kurze Pause.'
 ],'Erzähle den Ausflug in drei deutschen Angaben nach: wann, mit wem und wohin. Welche genaue Uhrzeit kannst du aus dem Text nicht entnehmen?',
 'Zeitwort und Satzende verbinden; と = Begleitung, に = Ziel, を = Objekt.','v11:relative-time v11:media-actions v11:adjective-time')

guide('v11:read-plan','v11:dialog-weekend v11:weather-words v11:station v11:hotel v11:wishes 31:0',
 'In einem Ausflugsplan Abfahrt, Treffort, Wunsch und wetterabhängige Alternative unterscheiden.',[
 'きょうと Kyōto Kyoto ist der Ortsname, nicht きょう kyō heute. あした morgen macht いきます zum Plan. でんしゃ Zug + くじに um 9 Uhr + でます demasu fährt ab: Hier ist das Subjekt ein Zug. えきで Bahnhof als Treffort und ともだちに die getroffene Person stehen vor あいます aimasu treffen.',
 'Neu: おてら otera Tempel, やすみます yasumimasu ausruhen. みます sehen → みたいです möchte sehen wiederholt たい. あめだったら ame dattara = falls es regnet: Nomen あめ plus だったら bezeichnet hier die Bedingung für die folgende Handlung. ホテルでやすみます nennt den Plan bei Regen, keine Aussage, dass Regen sicher kommt.',
 'Lies zuerst den Grundplan, dann die bedingte Alternative. Die 9-Uhr-Abfahrt ist nicht automatisch die vorherige Treffzeit am Bahnhof. Kyoto hat zwei Vokalteile kyō-to; dattara eine Pause vor t. Neue Wörter sind in dieser Hilfe erklärt, die allgemeine Bedingungsbildung wird nicht aus diesem einen Beispiel vorausgesetzt.'
 ],'Was wird bei Regen anders? Nenne die Abfahrtszeit und erkläre, welche genaue Treffzeit im Text offenbleibt.',
 'だったら leitet hier eine Bedingung ein; で markiert den Handlungsort.','v11:clock-hours v11:weather-words v11:wishes v11:station')

guide('v11:read-message','v11:messages v11:reply-invites v11:dialog-weekend 31:0',
 'Grund, neuen Tag, mögliche Tageshälfte und offene Rückfrage einer Terminänderung herauslesen.',[
 'Die Anrede さくらさん、こんにちは richtet sich an Sakura. あしたはしごとがあります heißt wörtlich morgen habe ich Arbeit, hier als Grund für das Terminproblem. Das ist keine allgemeine Grammatikform für müssen. にちようびにあいませんか fragt mit dem bekannten Einladungsmuster nach einem Treffen am Sonntag.',
 'ごごならだいじょうぶです (gogo nara daijōbu desu) sagt wenn es am Nachmittag ist, passt es. なら nimmt eine mögliche Wahl als Bedingung auf; es vereinbart keine genaue Uhrzeit. つごう tsugō bedeutet Verfügbarkeit/persönliche Passung; つごうはどうですか fragt, wie es der anderen Person passt.',
 'Die Nachricht schlägt eine Änderung vor, zeigt aber keine Antwort von Sakura. Sonntag ist daher noch nicht beiderseits bestätigt. ごご ist Nachmittag, nicht morgen; だいじょうぶ bestätigt hier die eigene Möglichkeit. Tsugō und daijōbu haben langes ō. Lies die Aussagegrenze ebenso sorgfältig wie die Wörter.'
 ],'Nenne den Grund für die Änderung und den vorgeschlagenen Tag. Welche Antwort fehlt noch, bevor das Treffen feststeht?',
 'なら formuliert eine Bedingung; die abschließende Frage lässt die andere Zusage offen.','v11:messages v11:weekdays v11:clock-minutes v11:reply-invites')

task('v11:people-age',0,'Du meldest zwei Gäste an. Welche Personenangabe passt?','ふたりです。',{
 'ふたつください。':'ふたつ bestellt zwei Dinge. Gäste werden hier mit ふたり gezählt.',
 'はたちです。':'はたち nennt zwanzig Lebensjahre, keine Anzahl von Gästen.'})
task('12:1',0,'Du möchtest wissen, wie spät es jetzt ist. Welche Frage passt?','いまなんじですか。',{
 'なんさいですか。':'さい fragt nach Lebensjahren. Für die jetzige Uhrzeit steht いまなんじ.',
 'いくらですか。':'いくら fragt nach dem Preis. Die Frage nennt keine Uhrzeit.'})
task('v11:weekdays',0,'Das Treffen soll am Sonntag sein. Welcher Wochentag passt?','にちようび',{
 'どようび':'どようび ist Samstag, einen Tag vor dem gewünschten Sonntag.',
 'きんようび':'きんようび ist Freitag. Sonntag beginnt mit にち.'})
task('v11:clock-hours',0,'Eine Uhr zeigt 2:30, auf Deutsch halb drei. Welche Form passt?','にじはん',{
 'さんじはん':'さんじはん beginnt bei drei Uhr und ergänzt eine halbe Stunde: 3:30.',
 'くじ':'くじ ist neun Uhr und enthält keine halbe Stunde.'})
task('v11:clock-minutes',0,'Ihr trefft euch um 15 Uhr. Welche Zeitangabe passt?','ごごさんじ',{
 'ごぜんくじ':'ごぜんくじ ist neun Uhr vormittags, nicht 15 Uhr.',
 'ごふん':'ごふん sind fünf Minuten. Das nennt keine Treffuhrzeit.'})
task('v11:clock-minutes',2,'Die Wegbeschreibung lautet あるいてごふんぐらいです. Was erfährst du?','Ungefähr fünf Minuten zu Fuß.',{
 'Ein Treffen um fünf Uhr.':'ごふん bezeichnet Minuten, nicht ごじ für fünf Uhr.',
 'Genau zehn Minuten zu Fuß.':'ご ist fünf; ぐらい macht die Angabe ungefähr, nicht exakt.'})
task('v11:calendar',0,'Du liest den 1. April. Welche Reihenfolge passt?','しがつついたち',{
 'ついたちしがつ':'Hier steht zuerst der Monat, danach der Kalendertag.',
 'くがつついたち':'くがつ ist September. April wird しがつ gelesen.'})
task('v11:calendar',4,'Im Kalender ist der zwanzigste Tag gemeint. Welches Wort passt?','はつか',{
 'はたち':'はたち bedeutet zwanzig Jahre alt, nicht der zwanzigste Monatstag.',
 'ついたち':'ついたち ist der erste Monatstag. Der Zwanzigste heißt はつか.'})
task('v11:relative-time',0,'Jemand sagt あしたいきます. Wie ist die Handlung zeitlich gemeint?','Gehen oder Fahren am nächsten Tag.',{
 'Eine bereits abgeschlossene Fahrt gestern.':'あした heißt morgen; gestern wäre きのう.',
 'Tägliches Gehen ohne bestimmten nächsten Tag.':'Tägliche Wiederholung wäre まいにち. あした bezeichnet den nächsten Tag.'})
task('v11:frequency',0,'Du möchtest sagen, dass du überhaupt nicht schaust. Welche Form passt?','ぜんぜんみません',{
 'あまりのみません':'Das verneint viel/oft trinken, nicht jedes Schauen. Handlung und Stärke weichen ab.',
 'ときどき':'ときどき bedeutet manchmal und verneint die Handlung nicht vollständig.'})
task('v11:seasons',0,'Welche Jahreszeit folgt in der üblichen Reihenfolge auf den Sommer?','あき',{
 'はる':'はる ist Frühling und steht vor dem Sommer.',
 'きせつ':'きせつ ist der Sammelbegriff Jahreszeit, keine konkrete folgende Jahreszeit.'})
task('v11:weather-words',0,'Du beschreibst einen kalten Tag, nicht kaltes Wasser. Welches Adjektiv passt?','さむい',{
 'つめたい':'つめたい beschreibt hier etwa kaltes Wasser. Für die Umgebungskälte wird さむい geübt.',
 'あたたかい':'あたたかい bedeutet warm und beschreibt die entgegengesetzte Temperatur.'})
task('v11:adjective-time',0,'Du sagst ausdrücklich: Gestern war es nicht kalt. Welche Form passt?','きのうはさむくなかったです。',{
 'きょうはさむくないです。':'Das verneint die Kälte heute. Gesucht ist eine Rückschau auf gestern.',
 'きのうはあつかったです。':'Das behauptet Hitze gestern. Nicht kalt bedeutet nicht zwingend heiß.'})
task('v11:adjective-time',4,'Ein Zimmer war gestern ruhig. Welche Adjektivverbindung passt?','しずかでした',{
 'しずかかったです':'しずか ist ein な-Adjektiv; seine höfliche Vergangenheit verwendet でした.',
 'しずかです':'Das ist die Nichtvergangenheit. Für die verlangte Rückschau fehlt でした.'})
task('v11:feelings',0,'Du brauchst Schlaf. Welche Aussage nennt genau dieses Befinden?','ねむいです。',{
 'つかれました。':'Das meldet Erschöpfung nach Anstrengung, nicht ausdrücklich das Bedürfnis zu schlafen.',
 'うれしいです。':'Das drückt Freude aus. Schlafbedarf heißt ねむい.'})
task('v11:games',0,'Du hast ein Spiel gewonnen. Was meldest du?','かちました。',{
 'まけました。':'まけました meldet eine Niederlage; gewonnen heißt かちました.',
 'もういっかい。':'Das bittet um eine weitere Runde, sagt aber nicht, wer gewonnen hat.'})
task('v11:media-actions',0,'Du machst im Park Fotos. Welcher Satz passt?','こうえんでしゃしんをとります。',{
 'いえでえいがをみます。':'Das beschreibt einen Film zu Hause. Sowohl Ort als auch Tätigkeit sind anders.',
 'おんがくをききます。':'Das bedeutet Musik hören, nicht Fotos aufnehmen.'})
task('v11:inviting',0,'Du lädst zu gemeinsamem Filmschauen ein. Welche Form passt?','えいがをみませんか。',{
 'えいがをみません。':'Ohne か ist das hier eine negative Aussage, nicht die geübte Einladungsfrage.',
 'おちゃをのみませんか。':'Die Form lädt zwar ein, aber zum Teetrinken statt zum Film.'})
task('v11:reply-invites',0,'Samstag passt nicht. Du möchtest das höflich andeuten. Was passt?','どようびはちょっと。',{
 'どようびでだいじょうぶです。':'Im Terminkontext bestätigt das Samstag; die Situation verlangt eine Absage.',
 'いいですね、いきましょう。':'Damit nimmst du den Vorschlag an und schlägst gemeinsames Gehen vor.'})
task('v11:reply-invites',4,'Nach einer Absage heißt es またこんどおねがいします. Was ist damit vereinbart?','Noch kein genauer neuer Termin.',{
 'Ein festes Treffen am Sonntag.':'Die Wendung nennt keinen Sonntag und keine konkrete Vereinbarung.',
 'Dass Samstag nun doch sicher passt.':'Die Möglichkeit eines anderen Mals bestätigt den zuvor problematischen Samstag nicht.'})
task('23:0',0,'Welche Wörterbuchform gehört zu der höflichen Form きます?','くる',{
 'する':'する wird höflich zu します. Die Form きます gehört zu くる.',
 'いく':'いく wird zu いきます, mit zusätzlichem i am Anfang; das ist ein anderes Verb.'})
task('v11:verb-groups',0,'Du möchtest かえる, zurückkehren, höflich sagen. Welche Form passt?','かえります',{
 'かえます':'Bei diesem Godan-Verb reicht das Weglassen von る nicht. Die gelernte Form ist かえります.',
 'きます':'きます ist kommen, aus くる. Zurückkehren heißt hier かえります.'})
task('7:0',0,'Du berichtest, dass du gegessen hast. Welche höfliche Form passt?','たべました',{
 'たべません':'ません verneint in der Nichtvergangenheit, statt vergangenes Essen zu bestätigen.',
 'たべて':'Das ist eine verbindende て-Form, keine höfliche Vergangenheitsaussage.'})
task('7:0',3,'Welche Bedeutung hat たべて in der hier erklärten Formenübersicht?','Eine て-Form, die mit einer weiteren Wendung verbunden werden kann.',{
 'Eine vollständige höfliche Aussage über vergangenes Essen.':'Dafür steht たべました. たべて legt diese Aussage nicht fest.',
 'Eine Frage, ob wir gemeinsam essen wollen.':'Die hier gelernte Einladungsfrage lautet たべませんか, mit か.'})
task('v11:appointments',0,'Du kennst den Beginn der Besprechung und möchtest ihre Endzeit erfahren. Was fragst du?','なんじまでですか。',{
 'なんじからですか。':'から fragt nach dem Beginn. Für das Ende steht まで.',
 'なんさいですか。':'さい fragt nach Alter und passt nicht zur Endzeit einer Besprechung.'})
task('v11:appointments',4,'Heute geht es nicht. Du fragst, ob auch morgen als Alternative möglich wäre. Was passt?','あしたでもいいですか。',{
 'きょうはむずかしいです。':'Das benennt nur das heutige Problem. Es schlägt noch nicht morgen vor.',
 'にじにしましょう。':'Das schlägt zwei Uhr vor, fragt aber nicht nach dem alternativen Tag morgen.'})
task('v11:messages',0,'Du hast einen Änderungswunsch geschickt und möchtest eine Antwort erhalten. Was ergänzt du?','へんじをおねがいします。',{
 'じかんをへんこうしたいです。':'Das wiederholt den Wunsch nach Zeitänderung. へんじ bezeichnet dagegen die erbetene Antwort.',
 'では、またあした。':'Das ist ein Abschiedsgruß und keine ausdrückliche Antwortbitte.'})
task('v11:messages',2,'Was ist nach じかんをへんこうしたいです bereits sicher?','Die Person möchte die Uhrzeit ändern.',{
 'Die andere Person hat einer neuen Uhrzeit zugestimmt.':'たい beschreibt einen Wunsch. Eine Zustimmung der anderen Person steht nicht darin.',
 'Der Termin wurde auf genau 15 Uhr verschoben.':'Der Satz nennt keine neue Uhrzeit und keine abgeschlossene Vereinbarung.'})
task('v11:dialog-weekend',0,'Du beantwortest nur die Frage nach dem passenden Tag und wählst Samstag. Was passt?','どようびがいいです。',{
 'ごごにじがいいです。':'Das wählt 14 Uhr. Es beantwortet die Uhrzeitfrage, aber noch nicht den Tag.',
 'カフェのまえはどうですか。':'Das schlägt einen Treffort vor. Ein Tag wird damit nicht gewählt.'})
task('v11:dialog-weekend',2,'Für die Offline-Szene wählst du 14 Uhr. Welche Antwort passt zur Zeitfrage?','ごごにじがいいです。',{
 'ごぜんじゅうじはどうですか。':'Das schlägt 10 Uhr vormittags vor. Gewünscht sind 14 Uhr.',
 'にちようびにしましょう。':'Das legt Sonntag fest, nennt aber noch keine Uhrzeit.'})
task('v11:dialog-weekend',3,'Du möchtest den vorgeschlagenen Bahnhof durch den Cafévorplatz ersetzen. Was antwortest du?','カフェのまえはどうですか。',{
 'はい、いいですね。':'Das stimmt dem gerade vorgeschlagenen Bahnhof zu, statt einen neuen Ort vorzuschlagen.',
 'えいがをみたいです。':'Das nennt eine gewünschte Tätigkeit, keinen anderen Treffpunkt.'})
task('v11:read-weekend',0,'Im Text steht きのうはやすみでした. Wann hatte die Person frei?','Gestern.',{
 'Heute.':'きのう bedeutet gestern. Heute wäre きょう.',
 'Morgen.':'Morgen wäre あした; でした blickt hier auf einen vergangenen freien Tag zurück.'})
task('v11:read-weekend',3,'Du liest しゃしんをたくさんとりました. Welche Aussage ist belegt?','Es wurden viele Fotos gemacht.',{
 'Es wurden genau drei Fotos gemacht.':'たくさん nennt keine genaue Anzahl. Drei ist nicht aus diesem Satz ableitbar.',
 'Morgen sollen Fotos gemacht werden.':'とりました berichtet über die Vergangenheit, nicht einen Plan für morgen.'})
task('v11:read-plan',0,'Du liest あしたきょうとにいきます. Welche Aussage passt?','Morgen geht oder fährt die Person nach Kyoto.',{
 'Die Person war gestern in Kyoto.':'あした benennt morgen; eine vergangene Fahrt wird nicht berichtet.',
 'Die Person bleibt heute sicher im Hotel.':'Der Satz nennt Kyoto als Ziel für morgen. Er sagt nichts über einen sicheren heutigen Hotelaufenthalt.'})
task('v11:read-plan',4,'Der Satz あめだったら、ホテルでやすみます nennt welchen Plan?','Bei Regen im Hotel ausruhen.',{
 'Auf jeden Fall im Hotel bleiben, unabhängig vom Wetter.':'だったら setzt hier Regen als Bedingung. Ohne Regen ist die Aussage nicht zugesagt.',
 'Es wird auf jeden Fall regnen.':'Eine Bedingung ist keine Wettervorhersage. Der Satz sagt, was bei Regen geplant ist.'})
task('v11:read-message',0,'Im Text steht さくらさん、こんにちは. Welche Funktion hat dieser Anfang?','Eine freundliche Anrede an Sakura.',{
 'Eine feste Zusage zu einem neuen Termin.':'Der Gruß nennt noch keine Zustimmung und keinen Termin.',
 'Eine genaue Uhrzeit für das Treffen.':'こんにちは grüßt; es ist keine genaue Zeitangabe.'})
task('v11:read-message',3,'Die Antwort lautet ごごならだいじょうぶです. Was erfährst du?','Am Nachmittag würde es passen; eine genaue Stunde fehlt.',{
 'Genau 15 Uhr ist fest bestätigt.':'ごご benennt die Tageshälfte, nicht automatisch さんじ oder 15 Uhr.',
 'Am Vormittag geht es auf jeden Fall.':'ごご ist Nachmittag. Die Aussage nennt eine Bedingung und betrifft nicht den Vormittag.'})

# Preserve the useful existing text-comprehension questions and explain every
# actual distractor. These are not counted as newly authored questions.
READ_FEEDBACK = {
 ('v11:read-weekend',1):{'Allein in den Park':'ともだちと nennt die Begleitung: mit einem Freund. Allein steht nicht im Satz.', 'Mit einem Freund ins Kino':'Die Begleitung stimmt, aber こうえん ist der Park, nicht das Kino.', 'Mit der Familie zum Bahnhof':'ともだち ist ein Freund und こうえん der Park; beide Angaben wären verändert.'},
 ('v11:read-weekend',2):{'Schlecht':'よかった ist die Vergangenheit von gut. Schlechtes Wetter wird hier nicht behauptet.', 'Sehr kalt':'Der Satz bewertet das Wetter als gut, nennt aber keine niedrige Temperatur.', 'Regnerisch':'Eine Regenaussage steht nicht im Text. よかった bedeutet war gut.'},
 ('v11:read-weekend',4):{'Er war langweilig':'たのしかった bedeutet hat Spaß gemacht, das Gegenteil dieser Bewertung.', 'Er war zu teuer':'Der Satz nennt Spaß und keinen Preis; eine zu hohe Ausgabe lässt sich nicht daraus ableiten.', 'Er war zu anstrengend':'Der Text bewertet den Ausflug als sehr angenehm. Eine übermäßige Anstrengung wird nicht genannt.'},
 ('v11:read-plan',1):{'Um sieben Uhr':'くじ ist neun Uhr. Sieben Uhr wäre しちじ.', 'Um acht Uhr':'Im Satz steht くじ für neun Uhr, nicht acht.', 'Um zehn Uhr':'Zehn Uhr wäre じゅうじ. くじ nennt neun Uhr.'},
 ('v11:read-plan',2):{'Im Hotel':'えきで nennt den Bahnhof als Treffort. Das Hotel ist nicht dieser Ort.', 'Am Tempel':'えき ist der Bahnhof. Ein Tempel wäre おてら.', 'Im Park':'Der Treffort ist えき, der Bahnhof. Park wäre こうえん.'},
 ('v11:read-plan',3):{'Ein Museum':'おてら benennt einen Tempel; ein Museum wird in diesem Satz nicht genannt.', 'Eine Schule':'Der Wunsch betrifft おてら, einen Tempel, nicht eine Schule.', 'Ein Einkaufszentrum':'みたいです nennt den Besichtigungswunsch; sein Objekt おてら ist ein Tempel.'},
 ('v11:read-message',1):{'Die Person ist krank':'Der Satz nennt しごと, Arbeit. Eine Krankheit steht nicht darin.', 'Der Bus fährt nicht':'Ein Busproblem wird nicht genannt. Die Person hat morgen Arbeit.', 'Es ist ein Feiertag':'Der Text nennt Arbeit morgen, keinen Feiertag.'},
 ('v11:read-message',2):{'Samstag':'にちようび ist Sonntag; Samstag wäre どようび.', 'Montag':'Montag wäre げつようび. Vorgeschlagen wird にちようび, Sonntag.', 'Freitag':'Freitag wäre きんようび. Hier steht der Sonntag.'},
 ('v11:read-message',4):{'Wie viel die Reise kostet':'つごう fragt nach Passung/Verfügbarkeit. Für einen Preis stünde いくら.', 'Wo das Hotel liegt':'Der Satz fragt, ob es der anderen Person passt, nicht nach einem Hotelort.', 'Wie das Wetter wird':'つごう ist hier zeitliche Verfügbarkeit; eine Wetterfrage steht nicht im Satz.'}
}

NUMBER_CORRECTION = {
 'explain':'Die Sammelkarte verlangt später die ganze Reihe 5 bis 10. Bereite sie in drei Paaren vor: ご・ろく (go, roku) = 5, 6; なな・はち (nana, hachi) = 7, 8; きゅう・じゅう (kyū, jū) = 9, 10. Lies ein Paar, decke es ab und rufe es ohne Vorlage ab. Verbinde die Paare erst danach. Die Punkte werden nicht gesprochen.',
 'parts':[['ご・ろく','go, roku: fünf und sechs'],['なな・はち','nana, hachi: sieben und acht'],['きゅう・じゅう','kyū, jū: neun und zehn']],
 'extra':[['ご・ろく','go, roku','Miniübung 1: Welche Zahl folgt auf fünf? Erst selbst antworten, dann im Paar nachsehen.'],['なな・はち','nana, hachi','Miniübung 2: Rufe sieben und acht getrennt ab, dann in Reihenfolge.'],['きゅう・じゅう','kyū, jū','Miniübung 3: Unterscheide neun und zehn; beide haben langes ū.']],
 'pitfall':'Die Vorbereitung und bewusst geöffnete Hilfe geben keine Aufgabe frei. In Sprechen, Bausteinen und Schreiben bleibt die ganze Reihe verlangt; einzelne Formen reichen dort nicht. Einzelkarten für 6 bis 10 folgen direkt in der nächsten Lektion.',
 'scenario':{'question':'In der gerade erklärten Zahlenreihe: Welche Zahl folgt direkt auf sieben?', 'correct':'はち','wrong':['ろく','じゅう'],
   'feedback':{'ろく':'ろく ist sechs und kommt vor sieben. Direkt danach steht acht: はち.','じゅう':'じゅう ist zehn. Zwischen sieben und zehn stehen noch acht und neun.'},'explanation':'Auf なな, sieben, folgt はち, acht.'}
}

def improve_numbers(lessons):
    p=lessons['12:0']['cards'][4]['detail']
    p.update(copy.deepcopy(NUMBER_CORRECTION))
    p['feedback'].update(build='Ordne erst die Paare 5/6, 7/8 und 9/10, dann verbinde sie in dieser Reihenfolge.',
        write='Die ganze Reihe bleibt gefragt: go, roku, nana, hachi, kyū, jū. Übe zuvor die drei Zweiergruppen; ū in beiden letzten Zahlen lang schreiben.',listen=NUMBER_CORRECTION['explain'])

def upgrade():
    path=ROOT/'data/course.json'; data=json.loads(path.read_text('utf-8'))
    lessons={l.get('id',f'{u}:{i}'):l for u,unit in enumerate(data['units']) for i,l in enumerate(unit['lessons'])}
    deep=json.loads((ROOT/'data/deep_lessons.json').read_text('utf-8'))['profiles']
    for key,authored in GUIDES.items():
        l=lessons[key]
        assert l.get('study_guide',{}).get('package',4)==4, 'Never overwrite previous packages'
        l['goal']=authored['goal']; l['study_guide']=copy.deepcopy(authored['study_guide'])
        l['intro']=authored['goal']+' Die Lernhilfe erklärt Wörter und Muster vor der selbstständigen Anwendung.'
        original={c['jp']:copy.deepcopy(c.get('detail') or deep.get(c['jp']) or {}) for c in l['cards']}
        for i,c in enumerate(l['cards']):
            p=copy.deepcopy(original[c['jp']])
            p.setdefault('explain',c['note']);p.setdefault('kind','Zeit, Verabredung und Wiederholung')
            p.setdefault('usage',c['de']);p.setdefault('register','Die Beispiele zeigen die jeweils erklärte höfliche oder neutrale Form.')
            p.setdefault('parts',[]);p.setdefault('extra',[]);p.setdefault('pitfall',authored['build'])
            if isinstance(c.get('example'),str):
                c['example']={'jp':c['example'],'romaji':c['example_romaji'],'de':c['example_de']}
            if not c.get('example'):
                c['example']={'jp':c['jp'],'romaji':c['romaji'],'de':c['de']}
            if (key,i) in APPLICATIONS:
                scenario=copy.deepcopy(APPLICATIONS[(key,i)])
            elif (key,i) in READ_FEEDBACK:
                scenario=copy.deepcopy(p['scenario'])
                assert set(scenario['wrong'])==set(READ_FEEDBACK[(key,i)])
                scenario['feedback']=copy.deepcopy(READ_FEEDBACK[(key,i)])
            else:
                scenario=copy.deepcopy(p.get('scenario') or {'question':f'Welche Bedeutung passt zu {c["jp"]}?',
                    'correct':c['de'],'wrong':[x['de'] for j,x in enumerate(l['cards']) if j!=i][:3]})
                scenario['question']=scenario['question'].replace('dieser Karte',c['jp']).replace('dieser Lernkarte',c['jp'])
                scenario['feedback']={}
                for wrong in scenario['wrong']:
                    other=next((x for x in l['cards'] if x is not c and
                        (x['de']==wrong or original[x['jp']].get('usage')==wrong
                         or original[x['jp']].get('scenario',{}).get('correct')==wrong
                         or deep.get(x['jp'],{}).get('scenario',{}).get('correct')==wrong)),None)
                    assert other is not None,(key,i,wrong)
                    scenario['feedback'][wrong]=f'Deine Auswahl gehört zu {other["jp"]} ({other["romaji"]}): {other["de"]}. Für die gefragte Form gilt: '+p['explain']
            p['scenario']=scenario
            p['feedback']={'build':authored['build'],'write':c['note']+' Prüfe die erklärte Lesung und die Vokallänge.','listen':p['explain']}
            c['detail']=p
    improve_numbers(lessons)
    data['content_version']='11.0.6'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'package':4,'lessons':len(GUIDES),'cards':sum(len(lessons[k]['cards']) for k in GUIDES),'applications':len(APPLICATIONS),'corrected_previous_cards':['12:0:4'],'new_lessons':0},ensure_ascii=False))

if __name__=='__main__':upgrade()
