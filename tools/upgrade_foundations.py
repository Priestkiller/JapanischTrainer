"""Apply the reviewed 11.0.2 foundation package without changing progress keys.

The resulting data/course.json is the runtime source for BOTH platforms.
Re-running this editorial migration is idempotent. No learner data is accessed.
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# key, objective, prerequisite keys, explanation, supported recall prompt
GUIDES = [
    ('0:0', 'Die fünf Vokale erkennen und mit je einem Takt nachsprechen.', [],
     'Hiragana sind japanische Lautzeichen. あ = a, い = i, う = u, え = e, お = o. Romaji schreibt die Lesung mit lateinischen Buchstaben.|Sprich jeden Vokal kurz und gleichmäßig. Mache aus e kein ei und aus o kein ou. Die Aufnahme vergleicht erkannten Text; sie bewertet deinen Akzent nicht.|Lerne zuerst mit der sichtbaren Vorlage. Ab Schritt 2 rufst du Bedeutung oder Lesung selbst ab. Über die Hilfe kannst du gezielt nachsehen.',
     'Decke die Lesung ab: Welcher Laut gehört zu い, welcher zu え?'),
    ('0:1', 'Kurze Wörter aus bekannten Vokalen und dem neuen Zeichen さ lesen.', ['0:0'],
     'Neu ist さ = sa. Zusammen mit あ entsteht あさ (asa), der Morgen. Du musst die übrigen Hiragana dafür noch nicht kennen.|いえ (ie, Haus) besteht aus i und e; うえ (ue, oben) aus u und e. Beide haben zwei Takte. Sprich die Vokale einzeln, ohne daraus einen deutschen Doppellaut zu machen.|Einzelne Wörter sind noch keine vollständigen Sätze. Lerne hier die Bedeutung und die Reihenfolge der Zeichen.',
     'Lies いえ und うえ. Welches Wort nennt ein Haus, welches eine Position?'),
    ('v11:long-vowels', 'Kurze und lange Vokale als Bedeutungsunterschied erkennen.', ['0:0','0:1'],
     'Neue Zeichen in diesen Wörtern: ば = ba, じ = ji, さ = sa, ん = n, き = ki. Die vollständigen Reihen folgen später; nutze hier die Lesung als Stütze.|おばさん (obasan, Tante) und おばあさん (obaasan, Großmutter) unterscheiden sich durch ein zusätzliches a. おじさん (ojisan, Onkel) und おじいさん (ojiisan, Großvater) durch ein zusätzliches i.|Ein langer Vokal dauert zwei Takte. ō ist eine Kurzschreibweise für einen langen o-Laut: おおきい (ōkii, groß). Beim Tippen kannst du hier ookii verwenden.',
     'Vergleiche obasan und obaasan. Welche zusätzliche Länge verändert die Bedeutung?'),
    ('v11:small-tsu', 'Die kleine Pause っ von einem gesprochenen つ unterscheiden.', ['v11:long-vowels'],
     'Zeichenhilfe: き = ki, て = te, さ = sa, か = ka, ま = ma. Kleines っ ist hier kein eigenes tsu, sondern hält den folgenden Konsonanten einen Takt zurück.|きて (kite, komm bitte) hat zwei Takte. きって (kitte, Briefmarke) hat drei: ki, Pause, te. Ebenso unterscheiden sich さか (saka, Steigung) und さっか (sakka, Schriftsteller).|まって (matte, warte) ist eine vertraute Bitte. Höfliche Bitten mit ください (kudasai, bitte) lernst du bald als feste Wendung.',
     'Wo liegt die Pause in kitte? Sprich danach kite ohne diese Pause.'),
    ('v11:mora-n', 'ん als eigenen Sprechtakt hören und mitsprechen.', ['v11:small-tsu'],
     'Zeichenhilfe: ほ = ho, み = mi, な = na, せ = se, し = shi, ぶ = bu. ん ist der n-Laut am Ende eines Taktes.|ほん (hon, Buch) hat zwei Takte: ho-n. みんな (minna, alle) hat drei: mi-n-na. Das n nicht mit dem folgenden Zeichen verschlucken.|せんせい (sensei, Lehrkraft) wird in normaler Aussprache meist mit langem e gesprochen. Geschrieben und in dieser Romaji-Aufgabe bleibt es sensei. さん (san) steht höflich hinter dem Namen anderer Personen.',
     'Klopfe die Takte von ほん und みんな mit. Zähle ん jeweils mit.'),
    ('1:0', 'Begrüßen, danken und höflich Kontakt aufnehmen.', ['v11:mora-n'],
     'Lerne diese Begrüßungen zunächst als ganze Wendungen. こんにちは (konnichiwa) heißt tagsüber Hallo. Das letzte は wird hier wa gelesen.|ありがとう (arigatō) ist ein kurzer Dank. ありがとうございます (arigatō gozaimasu) ist höflicher. すみません (sumimasen) kann entschuldigen oder eine fremde Person ansprechen.|はい (hai) kann Ja, aber auch Ich höre zu bedeuten. いいえ (iie, nein) beginnt mit langem ii; いえ (ie) bedeutet Haus.',
     'Du möchtest eine fremde Person ansprechen: Welche der gelernten Wendungen passt?'),
    ('1:1', 'Begrüßungen nach Tageszeit und Situation auswählen.', ['1:0'],
     'おはようございます (ohayō gozaimasu) ist der höfliche Morgengruß. Unter Freunden reicht oft おはよう (ohayō).|こんばんは (konbanwa) begrüßt am Abend. Wie bei konnichiwa wird das letzte は wa gelesen.|おやすみなさい (oyasuminasai) wünscht Gute Nacht, etwa vor dem Schlafengehen. Es ersetzt nicht automatisch den Gruß beim Ankommen am Abend.',
     'Du kommst abends an, statt schlafen zu gehen. Welcher Gruß passt?'),
    ('v11:learning-help', 'Ein Gespräch verlangsamen, wiederholen oder erklären lassen.', ['1:0','1:1'],
     'ゆっくり (yukkuri) bedeutet langsam, もういちど (mō ichido) noch einmal. Im Gespräch können diese kurzen Bitten schon helfen.|わかりません (wakarimasen) heißt Ich verstehe es nicht. Eine Rückfrage ist erlaubt und kein misslungener Gesprächsversuch.|かいてください (kaite kudasai, bitte aufschreiben) und おしえてください (oshiete kudasai, bitte erklären / mitteilen) lernst du zunächst als feste Bitten. Die Verbform vor kudasai wird später systematisch erklärt.',
     'Bitte erst um langsameres Sprechen und dann um eine Wiederholung.'),
    ('4:0', 'Vokal-, K- und S-Reihe systematisch lesen.', ['0:0','v11:learning-help'],
     'Die Spalten folgen immer a, i, u, e, o. K-Reihe: か ka, き ki, く ku, け ke, こ ko.|S-Reihe: さ sa, し shi, す su, せ se, そ so. Merke besonders し = shi, nicht si in der hier verwendeten Romaji-Schreibweise.|Die Leerzeichen trennen in den Reihen einzelne Zeichen als Lernhilfe. Im Wort すし (sushi) stehen す und し direkt nebeneinander.',
     'Lies か, こ und し einzeln, danach すし als Wort.'),
    ('4:1', 'T- und N-Reihe lesen und unregelmäßige Lesungen erkennen.', ['4:0'],
     'T-Reihe: た ta, ち chi, つ tsu, て te, と to. Besonders chi und tsu unterscheiden sich von einer regelmäßigen ti-/tu-Reihe.|N-Reihe: な na, に ni, ぬ nu, ね ne, の no. Das sind ganze Lautzeichen; ん ist dagegen ein eigener n-Takt ohne folgenden Vokal.|なつ (natsu, Sommer) besteht aus な und normal großem つ. Hier sprichst du tsu; nur das kleine っ kennzeichnet eine Pause.',
     'Was unterscheidet つ von っ? Lies dann なつ.'),
    ('10:0', 'Die übrigen Grundreihen lesen und Sonderfälle einordnen.', ['4:1'],
     'H-Reihe: は ha, ひ hi, ふ fu, へ he, ほ ho. Bei ふ berühren die oberen Zähne nicht wie beim deutschen f die Unterlippe. M-Reihe: ま ma, み mi, む mu, め me, も mo.|Y-Reihe: や ya, ゆ yu, よ yo. R-Reihe: ら ra, り ri, る ru, れ re, ろ ro; höre den kurzen Zungenschlag in der Vorlage.|わ = wa, を wird als Partikel o gelesen, ん = n. は liest man als Zeichen ha, als Themenpartikel später wa. Das sind unterschiedliche Verwendungen desselben Zeichens.',
     'Erkenne ふ, ゆ, ろ und ん ohne die ganze Reihe aufzusagen.'),
    ('10:1', 'Zusatzzeichen, kleine Kana und Pausen unterscheiden.', ['10:0','v11:small-tsu'],
     'Zwei Striche heißen Dakuten: か→が (ka→ga), さ→ざ (sa→za), た→だ (ta→da), は→ば (ha→ba). Dabei werden し→じ (shi→ji) und つ→づ (tsu→zu) besonders gelesen.|Der kleine Kreis macht aus der H- die P-Reihe: ぱ pa, ぴ pi, ぷ pu, ぺ pe, ぽ po. Striche und Kreis sind bedeutungsentscheidend.|Kleines ゃ verbindet sich etwa mit き zu きゃ (kya), einem Takt. Kleines っ markiert dagegen eine Pause: がっこう (gakkō, Schule) hat ga, Pause, ko, o.',
     'Vergleiche は, ば und ぱ. Was ändert der Kreis gegenüber den Strichen?'),
    ('v11:kana-k', 'Bekannte Hiragana in kurzen Wörtern selbst zusammensetzen.', ['4:0','4:1'],
     'かお (kao, Gesicht) liest du か ka + お o. き (ki, Baum) ist schon allein ein Wort.|くち (kuchi, Mund) verbindet ku mit chi. いけ (ike, Teich) und こえ (koe, Stimme) haben jeweils zwei klare Vokaltakte.|Die Beispiele mit です (desu) sind höfliche Benennungen, etwa かおです (kao desu, es ist ein Gesicht). Du lernst den Satzbau später; hier steht das Lesen der Wörter im Mittelpunkt.',
     'Lies こえ zuerst selbst und kontrolliere erst danach mit der Stimme.'),
    ('v11:kana-s', 'Die S-Reihe in wechselnden Wortpositionen abrufen.', ['v11:kana-k','4:0'],
     'かさ (kasa, Schirm) endet auf sa; いす (isu, Stuhl) endet auf su. Achte auf die genaue Reihenfolge.|すし (sushi) hat su und shi. Das einzelne し wird nicht als deutsches sch ohne Vokal gesprochen.|せかい (sekai, Welt) hat se-ka-i; そら (sora, Himmel) hat so-ra. Die Vokale in kai bleiben zwei Takte.',
     'Welche Zeichen unterscheiden いす und すし? Lies beide ohne die Romaji.'),
    ('v11:kana-tn', 'T- und N-Laute in bekannten kurzen Wortformen lesen.', ['4:1','10:0'],
     'たこ (tako, Oktopus) hat ta-ko. つき (tsuki, Mond) beginnt mit tsu, nicht mit su.|て (te) bedeutet Hand. ねこ (neko, Katze) und いぬ (inu, Hund) üben ne und nu an verschiedenen Stellen.|Ein Wort kann aus einem oder mehreren Kana bestehen. Sprich jeden Takt gleichmäßig, ohne automatisch das erste Zeichen stark zu betonen.',
     'Lies ねこ und いぬ und ordne die beiden Tiere zu.'),
    ('v11:kana-hm', 'H- und M-Zeichen in kurzen Alltagswörtern erkennen.', ['10:0','v11:kana-tn'],
     'はな (hana) bedeutet auf dieser Karte Blume. Derselbe Kana-Text kann je nach Wortkontext auch anderes bedeuten; hier lernst du nur die angegebene Bedeutung.|ひと (hito, Mensch) und ふね (fune, Schiff) üben hi und fu. Höre bei fu genau auf die Vorlage.|みみ (mimi, Ohr / Ohren) wiederholt mi. もも (momo, Pfirsich) wiederholt mo. Kana unterscheiden diese Wörter auch ohne unterschiedliche Konsonanten.',
     'Welcher Vokal unterscheidet みみ von もも?'),
    ('v11:kana-voiced', 'Dakuten und Handakuten beim Lesen von Wörtern beachten.', ['10:1'],
     'かぎ (kagi, Schlüssel): ぎ trägt zwei Striche und wird gi gesprochen. みず (mizu, Wasser) enthält ず = zu.|でんわ (denwa, Telefon) enthält で = de und einen eigenen n-Takt. かばん (kaban, Tasche) enthält ば = ba.|えんぴつ (enpitsu, Bleistift) enthält ぴ = pi mit kleinem Kreis. Das n kann vor p ähnlich wie m klingen; die gelernte Romaji-Schreibweise bleibt enpitsu.',
     'Finde in えんぴつ den Kreis und in かばん die zwei Striche.'),
    ('v11:small-ya', 'Kombinierte Laute von getrennten Kana unterscheiden.', ['10:1','v11:long-vowels'],
     'きゃ (kya) wird in einem Takt gesprochen. きや (kiya) mit großem や hätte zwei Takte. Die Größe des zweiten Zeichens zählt.|きゅう (kyū, neun) und きょう (kyō, heute) verlängern den kombinierten Laut um einen Vokaltakt.|しゃしん (shashin, Foto) beginnt mit sha; おちゃ (ocha, Tee) enthält cha. Lies die kleinen Zeichen zusammen mit ihrem Vorgänger, nicht als eigenes ya.',
     'Vergleiche kya mit kiya. Welche Form braucht zwei statt eines Taktes?'),
    ('11:0', 'Katakana als zweite Lautschrift erkennen und erste Wörter lesen.', ['4:0','10:1'],
     'Katakana stehen oft in Fremdwörtern. Sie bezeichnen Laute wie Hiragana: ア a, イ i, ウ u, エ e, オ o; カ ka, キ ki, ク ku, ケ ke, コ ko.|Neue Zeichen für die Wörter: ゲ ge, ム mu, ヒ hi, ド do, ツ tsu. ゲーム (gēmu) heißt Spiel; コーヒー (kōhī) Kaffee; ドイツ (Doitsu) Deutschland.|Der Strich ー verlängert den unmittelbar vorher gesprochenen Vokal. In コーヒー ist erst o, dann i lang.',
     'Lies コーヒー und nenne die beiden Vokale, die ー verlängert.'),
    ('v11:kata-basics', 'Neue Katakana direkt an kurzen Alltagswörtern lernen.', ['11:0'],
     'Zeichenhilfe: メ me, ラ ra, テ te, ス su, ト to, ホ ho, ル ru, バ ba, ペ pe, ン n. Verbinde sie mit den schon bekannten Zeichen.|カメラ (kamera, Kamera), テスト (tesuto, Test) und ホテル (hoteru, Hotel) folgen der japanischen Lautform. Sprich nicht einfach das deutsche Wort aus.|バス (basu, Bus) enthält su; ペン (pen, Stift) endet mit einem eigenen n-Takt. Der Kreis in ペ macht pe, die Striche in バ machen ba.',
     'Zerlege ホテル in ho-te-ru und ペン in pe-n.'),
    ('v11:kata-long', 'Lange Vokale in Katakana hören, lesen und tippen.', ['v11:kata-basics','v11:long-vowels'],
     'Zeichenhilfe: パ pa, チ chi, ズ zu, タ ta, シ shi, ジ ji, ュ kleines yu. Bei ジュ liest du ju zusammen.|スーパー (sūpā, Supermarkt) enthält langes u und a. ケーキ (kēki, Kuchen) enthält langes e. チーズ (chīzu, Käse) enthält langes i.|タクシー (takushī, Taxi) endet auf langes i; ジュース (jūsu, Saft) hat langes u. Tippe lange Vokale bei Bedarf doppelt: suupaa, keeki, chiizu, takushii, juusu.',
     'Welchen Vokal verlängert der Strich jeweils in チーズ und ケーキ?'),
    ('v11:kata-similar', 'Ähnliche Katakana anhand ihrer Form und im Wort unterscheiden.', ['v11:kata-long'],
     'Vergleiche シ (shi) und ツ (tsu) bewusst im Schriftbild, ebenso ソ (so) und ン (n). Lies nicht allein nach dem Umriss des gesamten Wortes.|Neue Zeichen: ナ na, フ fu, kleines ァ a, ャ kleines ya. ファ wird zusammen fa gelesen; シャ zusammen sha.|シカ (shika, Hirsch), ツナ (tsuna, Thunfisch), ソファ (sofa, Sofa), パン (pan, Brot) und シャツ (shatsu, Hemd) geben dir feste Ankerwörter.',
     'Finde in シャツ zuerst shi + kleines ya und danach großes tsu.'),
    ('v11:kata-media', 'Technikwörter lesen, ohne die deutsche Lautung zu übernehmen.', ['v11:kata-similar'],
     'Neue Zeichen: ビ bi, オ o, リ ri, マ ma, プ pu. テレビ (terebi) bezeichnet einen Fernseher, ラジオ (rajio) ein Radio.|パソコン (pasokon, Computer) und スマホ (sumaho, Smartphone) sind gebräuchliche Kurzformen. Lerne sie als ganze Wörter.|アプリ (apuri, App) hat drei Takte. Dass ein Fremdwort vertraut aussieht, bedeutet nicht, dass seine japanische Aussprache der deutschen entspricht.',
     'Sprich アプリ in drei Takten und lies danach スマホ.'),
    ('v11:kata-combinations', 'Kleine Katakana und Pausen auch in Fremdwörtern lesen.', ['v11:kata-similar','v11:small-tsu'],
     'Zeichenhilfe: ニ ni, グ gu, kleines ィ i. ニュ wird nyu, ティ wird ti und ファ wird fa gelesen; das kleine Zeichen gehört jeweils zum vorherigen.|チケット (chiketto, Ticket) hat die Pause vor t; バッグ (baggu, Tasche) vor g. Kleines ッ wird hier nicht als tsu gesprochen.|ニュース (nyūsu, Nachrichten) und ティー (tī, Tee) verlängern den kombinierten Vokal. ファイル (fairu, Datei) hat fa-i-ru, also drei Takte.',
     'Markiere in チケット die Pause und in ティー den langen Vokal.'),
    ('2:0', 'Mit Thema + Aussage + です einen einfachen höflichen Satz bilden.', ['1:0','v11:kana-k'],
     'わたし (watashi) heißt ich. がくせい (gakusei) bedeutet Schüler oder Student. In わたしはがくせいです (watashi wa gakusei desu) ist watashi das Thema und gakusei die Aussage dazu.|Die Themenpartikel は wird wa gelesen. Sie steht nach dem Thema. です (desu) beendet diese Art Aussage höflich; es ist nicht ein beliebig einsetzbares Wort für sein.|Wenn aus der Situation klar ist, um wen es geht, kann わたしは fehlen. Lerne zunächst das vollständige Muster und danach die kurze Form がくせいです (gakusei desu).',
     'Ordne watashi, wa, gakusei und desu zu einer höflichen Aussage.'),
    ('2:1', 'Ein Land und die Nationalität einer Person unterscheiden.', ['2:0','11:0'],
     'ドイツ (Doitsu) ist das Land Deutschland. ドイツじん (Doitsu-jin) bezeichnet eine deutsche Person. じん (jin) wird hier an den Ländernamen angehängt.|わたしはドイツじんです (watashi wa Doitsu-jin desu) heißt Ich bin deutsch. Das Muster aus der vorherigen Lektion bleibt gleich; du tauschst nur die Aussage aus.|Nicht jede Information über eine Person ist ihre Nationalität. Mit diesem Satz sagst du noch nicht, wo sie gerade wohnt oder welche Sprache sie spricht.',
     'Welche Form brauchst du für die Person: Doitsu oder Doitsu-jin?'),
    ('3:0', 'Aus einer höflichen Aussage eine Ja-/Nein-Frage bilden und bestätigen.', ['2:0','2:1'],
     'がくせいです (gakusei desu) ist eine Aussage. Mit か (ka) am Ende entsteht がくせいですか (gakusei desu ka), Bist du Schüler oder Student? Die Wortreihenfolge bleibt gleich.|はい、そうです (hai, sō desu) bestätigt: Ja, das stimmt. そう (sō) bedeutet hier so / so ist es und hat einen langen o-Laut.|Das Thema kann fehlen, wenn klar ist, wen du fragst. Verwechsle diese Fragepartikel か nicht mit は (wa), das vorher das Thema markiert.',
     'Mache aus ドイツじんです eine Frage und antworte bestätigend.'),
    ('v11:first-meeting', 'Eine kurze erste Vorstellung in passender Reihenfolge führen.', ['3:0','1:0'],
     'はじめまして (hajimemashite) passt zum ersten Kennenlernen. Danach kannst du deinen Namen mit です (desu) nennen: さくらです (Sakura desu). Sakura ist hier ein Beispielname.|よろしくおねがいします (yoroshiku onegai shimasu) ist eine feste freundliche Formel beim Kennenlernen. Eine starre wortwörtliche deutsche Übersetzung hilft hier weniger als die Situation.|こちらこそ (kochira koso) erwidert die Freundlichkeit. またあした (mata ashita, bis morgen) passt nur, wenn ein Wiedersehen morgen gemeint ist.',
     'Begrüße eine neue Person, nenne deinen Namen und schließe freundlich ab.'),
    ('v11:asking-names', 'Den eigenen Namen nennen und höflich nach dem anderen fragen.', ['v11:first-meeting'],
     'なまえ (namae) heißt Name. おなまえは (onamae wa) fragt höflich nach dem Namen des Gegenübers. Das o ist hier eine Höflichkeitsvorsilbe; wa wird als は geschrieben.|Bei anderen Personen folgt さん (san) dem Namen: たなかさん (Tanaka-san). Beim eigenen Namen lässt du san weg.|さくらといいます (Sakura to iimasu) ist die feste Vorstellung Ich heiße Sakura. どうぞ (dōzo) kann dem Gegenüber das Wort anbieten. Die Grammatik von to iimasu wird später vertieft.',
     'Frage nach dem Namen und antworte mit deinem eigenen Namen ohne san.'),
    ('v11:countries', 'Fünf Ländernamen lesen und das Nationalitätsmuster übertragen.', ['2:1','v11:asking-names'],
     'にほん (Nihon) bezeichnet Japan, ドイツ (Doitsu) Deutschland, フランス (Furansu) Frankreich, イギリス (Igirisu) das Vereinigte Königreich und アメリカ (Amerika) hier die USA.|Noch benötigte Katakana: ン n, ギ gi, ア a. Das sind dieselben Laute wie in den bekannten Hiragana; ぎ und ギ gehören zur G-Reihe.|Für eine Person ergänzt du in diesen Beispielen じん (jin): にほんじん (Nihon-jin), ドイツじん (Doitsu-jin). Mit です (desu) entsteht eine höfliche Aussage. Beim Gesprächstraining darfst du Antworten und Hilfen erst ansehen und dann selbst sprechen.',
     'Wähle einen Ländernamen, ergänze jin und bilde eine Aussage mit desu.'),
]

# One concrete transfer task per lesson, with alternatives already taught locally.
APPLICATIONS = {
    'v11:long-vowels': ('Du meinst die Tante. Welche Form hat dafür die passende Vokallänge?', 'おばさん', ['おばあさん','おじいさん']),
    'v11:small-tsu': ('Auf dem Umschlag fehlt eine Briefmarke. Welches Wort enthält dafür die nötige Pause?', 'きって', ['きて','さか']),
    'v11:mora-n': ('Du willst ein Buch benennen. Welche Form enthält ho und einen eigenen n-Takt?', 'ほん', ['みんな','さん']),
    'v11:learning-help': ('Dein Gegenüber spricht zu schnell. Welche kurze Bitte hilft zuerst?', 'ゆっくり', ['もういちど','かいてください']),
    'v11:kana-k': ('Du zeigst auf dein Gesicht. Welches gelernte Wort benennt es?', 'かお', ['こえ','いけ']),
    'v11:kana-s': ('Es regnet und du suchst deinen Schirm. Welches Wort brauchst du?', 'かさ', ['いす','そら']),
    'v11:kana-tn': ('Im Aquarium siehst du einen Oktopus. Wie heißt dieses Tier?', 'たこ', ['ねこ','いぬ']),
    'v11:kana-hm': ('Du zeigst auf eine Blume. Welches Wort passt hier?', 'はな', ['ひと','ふね']),
    'v11:kana-voiced': ('Vor der verschlossenen Tür suchst du deinen Schlüssel. Welches Wort passt?', 'かぎ', ['みず','かばん']),
    'v11:small-ya': ('Welche Schreibweise verbindet ki und kleines ya zu einem einzigen Takt?', 'きゃ', ['きゅう','きょう']),
    'v11:kata-basics': ('Du möchtest ein Foto machen und brauchst eine Kamera. Welches Wort passt?', 'カメラ', ['ホテル','ペン']),
    'v11:kata-long': ('Du suchst einen Supermarkt. Welches Wort kannst du auf dem Schild erkennen?', 'スーパー', ['タクシー','チーズ']),
    'v11:kata-similar': ('Im Tierpark steht ein Hirsch. Welches Ankerwort mit シ bezeichnet ihn?', 'シカ', ['ツナ','シャツ']),
    'v11:kata-media': ('Du willst den Fernseher einschalten. Welches Wort bezeichnet das Gerät?', 'テレビ', ['ラジオ','スマホ']),
    'v11:kata-combinations': ('Du brauchst eine Eintrittskarte. Welches gelernte Wort enthält die Pause vor t?', 'チケット', ['バッグ','ニュース']),
    'v11:first-meeting': ('Du wirst einer Person zum ersten Mal vorgestellt. Womit beginnst du?', 'はじめまして', ['またあした','こちらこそ']),
    'v11:asking-names': ('Du suchst in einem Formular das Feld für den Namen. Welches gelernte Wort bezeichnet diese Information?', 'なまえ', ['どうぞ','たなかさん']),
    'v11:countries': ('Du möchtest Japan als Land nennen. Welche Form brauchst du?', 'にほん', ['ドイツ','イギリス']),
}

def main():
    path = ROOT/'data/course.json'
    course = json.loads(path.read_text('utf-8'))
    deep = json.loads((ROOT/'data/deep_lessons.json').read_text('utf-8'))
    lessons = {l.get('id', f'{ui}:{li}'): l for ui,u in enumerate(course['units']) for li,l in enumerate(u['lessons'])}
    assert [g[0] for g in GUIDES] == course['learning_order'][:30]
    for key,goal,prereqs,points,recall in GUIDES:
        lesson=lessons[key]
        lesson['goal']=goal
        lesson['study_guide']={'revision':1,'prerequisites':prereqs,'points':points.split('|'),'recall':recall}
        for c in lesson['cards']:
            profile=copy.deepcopy(c.get('detail') or deep['profiles'].get(c['jp']))
            if profile is None:
                profile={'kind':'Zeichen lesen','usage':'Diese Zeichenfolge lesen und den Lauten zuordnen.',
                         'explain':points.replace('|',' '),'register':'Lesetraining; die Reihe ist kein Gesprächssatz.',
                         'parts':[], 'extra':[], 'pitfall':'Beachte die Größe der Zeichen und die Zusatzstriche.',
                         'scenario':{'question':f'Welche Lesung passt zur Zeichenfolge „{c["jp"]}“?',
                                     'correct':c['romaji'],'wrong':[other['romaji'] for other in lesson['cards'] if other['romaji']!=c['romaji']]}}
            if profile['scenario']['question']=='Welche Verwendung passt zu dieser Karte?':
                profile['scenario']['question']=f'In welcher Situation passt „{c["jp"]}“ ({c["romaji"]})?'
            c['detail']=profile
        if key in APPLICATIONS:
            q,correct,wrong=APPLICATIONS[key]
            lesson['cards'][0]['detail']['scenario']={'question':q,'correct':correct,'wrong':wrong}
    # Same order, same revision, same card keys: no progress migration is necessary.
    course['content_version']='11.0.2'
    path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
