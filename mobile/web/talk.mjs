/* GPL-3.0-or-later. Authored, branching offline conversations; no language model. */
export const normalizeTalk=text=>String(text??'').normalize('NFKC').toLowerCase().replace(/[ァ-ヶ]/g,c=>String.fromCharCode(c.charCodeAt(0)-0x60)).replace(/[\s。、，,.！？!?「」『』"'・:：]/gu,'');
const line=(jp,romaji,de)=>({jp,romaji,de});
const hint=(jp,romaji,de)=>({jp,romaji,de});
const route=(id,pattern,next,slots={})=>({id,pattern,next,slots});
const yes=/^(?:(?:はい|ええ|うん)(?:わかりました|分かりました|そうです)?|いいですね|いいです|大丈夫です|だいじょうぶです|わかりました|分かりました|お願いします|おねがいします)$/u;
const thanks=/^(?:はい)?(?:ありがとうございます|ありがとう|どうもありがとうございます|どうも)(?:さようなら|またね)?$/u;
const polite='(?:を)?(?:ください|お願いします|おねがいします|にします|がいいです|です)?';
const selection=(words)=>new RegExp(`^(?:じゃあ|では)?(?:${words})${polite}$`,'u');
const drinkHints=[hint('コーヒーをお願いします。','kōhī o onegai shimasu.','Einen Kaffee, bitte.'),hint('お茶をください。','ocha o kudasai.','Einen Tee, bitte.'),hint('水をください。','mizu o kudasai.','Wasser, bitte.')];
const moneyHints=[hint('カードでお願いします。','kādo de onegai shimasu.','Mit Karte, bitte.'),hint('現金で払います。','genkin de haraimasu.','Ich zahle bar.')];
const moneyRoutes=[route('card',/^(?:かーど|くれじっとかーど)(?:で)?(?:お願いします|おねがいします|払います|はらいます|いいですか)?$/u,'done',{payment:'カード'}),route('cash',/^(?:現金|げんきん)(?:で)?(?:お願いします|おねがいします|払います|はらいます)?$/u,'done',{payment:'現金'})];
const end=(say)=>({say,done:true});

export const SCENES=[
 {id:'meeting',title:'Jemanden kennenlernen',icon:'✿',role:'Eine neue Bekanntschaft',goal:'Stell dich vor, erzähle etwas über dich und stelle selbst eine Frage.',start:'name',nodes:{
  name:{say:line('こんにちは。はじめまして。お名前は何ですか。','konnichiwa. hajimemashite. onamae wa nan desu ka.','Hallo, schön dich kennenzulernen. Wie heißt du?'),cue:'Stell dich mit deinem Namen vor.',hints:[hint('アレックスです。','Arekkusu desu.','Ich bin Alex.'),hint('私はマリアです。','watashi wa Maria desu.','Ich bin Maria.')],routes:[route('name',/^(?:はじめまして)?(?:私は|わたしは)?([ぁ-ん一-龯a-zー]{1,20})(?:です|と言います|といいます)(?:よろしくお願いします|よろしくおねがいします)?$/u,'country')]},
  country:{say:line('よろしくお願いします。どこから来ましたか。','yoroshiku onegai shimasu. doko kara kimashita ka.','Freut mich. Woher kommst du?'),cue:'Nenne dein Herkunftsland. Diese Szene kennt Deutschland, Österreich, die Schweiz und Japan.',hints:[hint('ドイツから来ました。','Doitsu kara kimashita.','Ich komme aus Deutschland.'),hint('オーストリアから来ました。','Ōsutoria kara kimashita.','Ich komme aus Österreich.'),hint('スイスから来ました。','Suisu kara kimashita.','Ich komme aus der Schweiz.'),hint('日本から来ました。','Nihon kara kimashita.','Ich komme aus Japan.')],routes:[
   route('germany',/^(?:私は|わたしは)?どいつ(?:から)?(?:来ました|きました|です)$/u,'hobby',{country:'ドイツ',countryRomaji:'Doitsu'}),route('austria',/^(?:私は|わたしは)?おーすとりあ(?:から)?(?:来ました|きました|です)$/u,'hobby',{country:'オーストリア',countryRomaji:'Ōsutoria'}),route('switzerland',/^(?:私は|わたしは)?すいす(?:から)?(?:来ました|きました|です)$/u,'hobby',{country:'スイス',countryRomaji:'Suisu'}),route('japan',/^(?:私は|わたしは)?(?:日本|にほん|にっぽん)(?:から)?(?:来ました|きました|です)$/u,'hobby',{country:'日本',countryRomaji:'Nihon'})]},
  hobby:{say:s=>line(`${s.country}からですか。趣味は何ですか。`,`${s.countryRomaji} kara desu ka. shumi wa nan desu ka.`,'Ach, von dort kommst du. Was ist dein Hobby?'),cue:'Erzähle von Anime, Musik, Spielen oder Reisen.',hints:[hint('アニメが好きです。','anime ga suki desu.','Ich mag Anime.'),hint('音楽が好きです。','ongaku ga suki desu.','Ich mag Musik.'),hint('ゲームが好きです。','gēmu ga suki desu.','Ich mag Spiele.'),hint('旅行が好きです。','ryokō ga suki desu.','Ich reise gern.')],routes:[route('anime',/^(?:私は|わたしは)?あにめ(?:が好きです|がすきです|を見ることです|をみることです|です)$/u,'ask',{hobby:'アニメ',hobbyRomaji:'anime'}),route('music',/^(?:私は|わたしは)?(?:音楽|おんがく)(?:が好きです|がすきです|を聞くことです|をきくことです|です)$/u,'ask',{hobby:'音楽',hobbyRomaji:'ongaku'}),route('games',/^(?:私は|わたしは)?げーむ(?:が好きです|がすきです|をすることです|です)$/u,'ask',{hobby:'ゲーム',hobbyRomaji:'gēmu'}),route('travel',/^(?:私は|わたしは)?(?:旅行|りょこう)(?:が好きです|がすきです|です)$/u,'ask',{hobby:'旅行',hobbyRomaji:'ryokō'})]},
  ask:{say:s=>line(`${s.hobby}、いいですね。私にも何か聞いてください。`,`${s.hobbyRomaji}, ii desu ne. watashi ni mo nanika kiite kudasai.`,'Das klingt schön. Frag mich auch etwas.'),cue:'Frage nach meinem Hobby oder meiner Herkunft.',hints:[hint('趣味は何ですか。','shumi wa nan desu ka.','Was ist dein Hobby?'),hint('どこから来ましたか。','doko kara kimashita ka.','Woher kommst du?')],routes:[route('ask-hobby',/^(?:あなたの)?(?:趣味|しゅみ)は(?:何|なん)ですか$/u,'hobby-end'),route('ask-country',/^(?:あなたは)?どこから(?:来ました|きました)か$/u,'country-end')]},
  'hobby-end':end(line('私は旅行が好きです。お話しできてうれしいです。また会いましょう。','watashi wa ryokō ga suki desu. ohanashi dekite ureshii desu. mata aimashō.','Ich reise gern. Es war schön, mit dir zu reden. Bis zum nächsten Mal.')),
  'country-end':end(line('日本から来ました。お話しできてうれしいです。また会いましょう。','Nihon kara kimashita. ohanashi dekite ureshii desu. mata aimashō.','Ich komme aus Japan. Es war schön, mit dir zu reden. Bis zum nächsten Mal.'))
 }},
 {id:'cafe',title:'Im Café',icon:'☕',role:'Im Service',goal:'Bestelle dein Getränk, hier oder zum Mitnehmen, und bezahle.',start:'order',nodes:{
  order:{say:line('いらっしゃいませ。ご注文は何になさいますか。','irasshaimase. gochūmon wa nani ni nasaimasu ka.','Willkommen. Was möchten Sie bestellen?'),cue:'Bestelle Kaffee, Tee oder Wasser.',hints:drinkHints,routes:[route('coffee',selection('こーひー'),'temperature',{drink:'コーヒー',drinkRomaji:'kōhī'}),route('tea',selection('お茶|おちゃ|紅茶|こうちゃ'),'temperature',{drink:'お茶',drinkRomaji:'ocha'}),route('water',selection('水|みず|お水|おみず'),'where',{drink:'お水',drinkRomaji:'omizu',size:'',temperature:''})]},
  temperature:{say:s=>line(`${s.drink}ですね。温かいものと冷たいもの、どちらがいいですか。`,`${s.drinkRomaji} desu ne. atatakai mono to tsumetai mono, dochira ga ii desu ka.`,'Gern. Möchten Sie es warm oder kalt?'),cue:'Wähle ein warmes oder kaltes Getränk.',hints:[hint('温かいものをお願いします。','atatakai mono o onegai shimasu.','Ein warmes, bitte.'),hint('冷たいものをお願いします。','tsumetai mono o onegai shimasu.','Ein kaltes, bitte.')],routes:[route('hot',selection('温かいもの|あたたかいもの|あったかいもの|温かいの|あたたかいの|ほっと'),'size',{temperature:'温かい'}),route('cold',selection('冷たいもの|つめたいもの|冷たいの|つめたいの|あいす'),'size',{temperature:'冷たい'})]},
  size:{say:line('かしこまりました。サイズはどうなさいますか。','kashikomarimashita. saizu wa dō nasaimasu ka.','Sehr gern. Welche Größe möchten Sie?'),cue:'Wähle klein oder groß.',hints:[hint('小さいサイズでお願いします。','chiisai saizu de onegai shimasu.','Die kleine Größe, bitte.'),hint('大きいサイズをください。','ōkii saizu o kudasai.','Die große Größe, bitte.')],routes:[route('small',/^(?:小さい|ちいさい|s|えす)(?:さいず)?(?:で|を)?(?:お願いします|おねがいします|ください|です)?$/u,'where',{size:'小さい'}),route('large',/^(?:大きい|おおきい|l|える)(?:さいず)?(?:で|を)?(?:お願いします|おねがいします|ください|です)?$/u,'where',{size:'大きい'})]},
  where:{say:line('店内でお召し上がりですか。お持ち帰りですか。','tennai de omeshiagari desu ka. omochikaeri desu ka.','Möchten Sie hier trinken oder es mitnehmen?'),cue:'Entscheide dich für hier oder zum Mitnehmen.',hints:[hint('ここで飲みます。','koko de nomimasu.','Ich trinke hier.'),hint('持ち帰りでお願いします。','mochikaeri de onegai shimasu.','Zum Mitnehmen, bitte.')],routes:[route('here',/^(?:(?:ここ|店内|てんない)で(?:飲みます|のみます|お願いします|おねがいします)?|店内です|てんないです)$/u,'payment',{place:'店内'}),route('takeout',/^(?:お?持ち帰り|お?もちかえり|ていくあうと)(?:で|です)?(?:お願いします|おねがいします)?$/u,'payment',{place:'持ち帰り'})]},
  payment:{say:s=>line(`${s.place}ですね。お支払いは現金ですか、カードですか。`,`${s.place==='店内'?'tennai':'mochikaeri'} desu ne. oshiharai wa genkin desu ka, kādo desu ka.`,'Gern. Zahlen Sie bar oder mit Karte?'),cue:'Sage, wie du bezahlen möchtest.',hints:moneyHints,routes:moneyRoutes},
  done:end(s=>line(`${s.drink}ですね。ありがとうございます。少々お待ちください。`,`${s.drinkRomaji} desu ne. arigatō gozaimasu. shōshō omachi kudasai.`,'Vielen Dank für Ihre Bestellung. Einen kleinen Moment, bitte.'))
 }},
 {id:'shopping',title:'Eine Tasche kaufen',icon:'▣',role:'Im Geschäft',goal:'Frage nach dem Preis und entscheide, ob und wie du kaufen möchtest.',start:'price',nodes:{
  price:{say:line('いらっしゃいませ。何かお探しですか。','irasshaimase. nanika osagashi desu ka.','Willkommen. Suchen Sie etwas Bestimmtes?'),cue:'Du siehst eine Tasche. Frage nach ihrem Preis.',hints:[hint('このバッグはいくらですか。','kono baggu wa ikura desu ka.','Wie viel kostet diese Tasche?'),hint('これはいくらですか。','kore wa ikura desu ka.','Wie viel kostet das?')],routes:[route('price',/^(?:この(?:ばっぐ|かばん|鞄)は|これは)?(?:いくら|幾ら)ですか$/u,'buy')]},
  buy:{say:line('三千円です。いかがですか。','sanzen en desu. ikaga desu ka.','Sie kostet dreitausend Yen. Möchten Sie sie kaufen?'),cue:'Kaufe die Tasche oder lehne höflich ab.',hints:[hint('これをください。','kore o kudasai.','Die nehme ich, bitte.'),hint('すみません、やめておきます。','sumimasen, yamete okimasu.','Entschuldigung, ich lasse es lieber.')],routes:[route('buy',/^(?:はい)?(?:これをください|買います|かいます|お願いします|おねがいします)$/u,'color'),route('decline',/^(?:すみません)?(?:やめておきます|いりません|要りません|結構です|けっこうです)$/u,'declined')]},
  color:{say:line('ありがとうございます。赤、青、黒があります。何色がいいですか。','arigatō gozaimasu. aka, ao, kuro ga arimasu. naniiro ga ii desu ka.','Vielen Dank. Wir haben Rot, Blau und Schwarz. Welche Farbe möchten Sie?'),cue:'Wähle Rot, Blau oder Schwarz.',hints:[hint('黒をお願いします。','kuro o onegai shimasu.','Schwarz, bitte.'),hint('青がいいです。','ao ga ii desu.','Ich hätte gern Blau.'),hint('赤をください。','aka o kudasai.','Rot, bitte.')],routes:[route('black',selection('黒|くろ'),'payment',{color:'黒',colorRomaji:'kuro'}),route('blue',selection('青|あお'),'payment',{color:'青',colorRomaji:'ao'}),route('red',selection('赤|あか'),'payment',{color:'赤',colorRomaji:'aka'})]},
  payment:{say:s=>line(`${s.color}ですね。お支払いはどうなさいますか。`,`${s.colorRomaji} desu ne. oshiharai wa dō nasaimasu ka.`,'Gern. Wie möchten Sie bezahlen?'),cue:'Bezahle mit Karte oder bar.',hints:moneyHints,routes:moneyRoutes},
  done:end(line('ありがとうございます。こちらが商品です。またお越しください。','arigatō gozaimasu. kochira ga shōhin desu. mata okoshi kudasai.','Vielen Dank. Hier ist Ihre Ware. Besuchen Sie uns gern wieder.')),
  declined:end(line('かしこまりました。またお越しください。','kashikomarimashita. mata okoshi kudasai.','Natürlich. Besuchen Sie uns gern wieder.'))
 }},
 {id:'directions',title:'Nach dem Weg fragen',icon:'↗',role:'Eine hilfsbereite Person',goal:'Frage nach einem Ziel und hake nach, bis du die Wegbeschreibung verstehst.',start:'destination',nodes:{
  destination:{say:line('こんにちは。どうしましたか。','konnichiwa. dō shimashita ka.','Hallo. Kann ich helfen?'),cue:'Frage nach dem Bahnhof, einem Convenience-Store oder der Toilette.',hints:[hint('駅はどこですか。','eki wa doko desu ka.','Wo ist der Bahnhof?'),hint('コンビニはどこですか。','konbini wa doko desu ka.','Wo ist ein Convenience-Store?'),hint('トイレはどこですか。','toire wa doko desu ka.','Wo ist die Toilette?')],routes:[route('station',/^(?:すみません)?(?:駅|えき)はどこですか$/u,'detail',{destination:'駅',destinationRomaji:'eki'}),route('shop',/^(?:すみません)?こんびにはどこですか$/u,'detail',{destination:'コンビニ',destinationRomaji:'konbini'}),route('toilet',/^(?:すみません)?といれはどこですか$/u,'detail',{destination:'トイレ',destinationRomaji:'toire'})]},
  detail:{say:s=>line(`${s.destination}ですね。まっすぐ行って、右に曲がってください。`,`${s.destinationRomaji} desu ne. massugu itte, migi ni magatte kudasai.`,'Gehe geradeaus und biege dann rechts ab.'),cue:'Frage nach der Dauer oder bestätige die Richtung.',hints:[hint('歩いて何分ですか。','aruite nanpun desu ka.','Wie viele Minuten sind es zu Fuß?'),hint('右ですか。','migi desu ka.','Rechts?')],routes:[route('time',/^(?:歩いて|あるいて)?(?:何分|なんぷん|なんふん)ですか$|^どのくらいかかりますか$/u,'time'),route('right',/^(?:右|みぎ)(?:ですか|に曲がりますか|にまがりますか)$/u,'right')]},
  time:{say:line('歩いて五分ぐらいです。大丈夫ですか。','aruite gofun gurai desu. daijōbu desu ka.','Es sind ungefähr fünf Minuten zu Fuß. Kommst du zurecht?'),cue:'Bestätige, wenn du verstanden hast. Du kannst auch um Wiederholung bitten.',hints:[hint('はい、わかりました。','hai, wakarimashita.','Ja, ich habe verstanden.'),hint('もう一度お願いします。','mō ichido onegai shimasu.','Noch einmal, bitte.')],routes:[route('understood',yes,'thanks')]},
  right:{say:line('はい、右です。まっすぐ行ってから、右に曲がってください。わかりましたか。','hai, migi desu. massugu itte kara, migi ni magatte kudasai. wakarimashita ka.','Ja, rechts. Erst geradeaus, dann rechts. Hast du verstanden?'),cue:'Bestätige, wenn du verstanden hast.',hints:[hint('はい、わかりました。','hai, wakarimashita.','Ja, ich habe verstanden.')],routes:[route('understood',yes,'thanks')]},
  thanks:{say:line('よかったです。気をつけて。','yokatta desu. ki o tsukete.','Gut. Pass auf dich auf.'),cue:'Bedanke dich zum Abschied.',hints:[hint('ありがとうございます。','arigatō gozaimasu.','Vielen Dank.')],routes:[route('thanks',thanks,'done')]},
  done:end(line('どういたしまして。よい一日を。','dō itashimashite. yoi ichinichi o.','Gern geschehen. Hab einen schönen Tag.'))
 }},
 {id:'weekend',title:'Das Wochenende planen',icon:'☀',role:'Eine Freizeitbekanntschaft',goal:'Schlage etwas vor und vereinbare Tag, Uhrzeit und Treffpunkt.',start:'activity',nodes:{
  activity:{say:line('週末、一緒に出かけませんか。何をしたいですか。','shūmatsu, issho ni dekakemasen ka. nani o shitai desu ka.','Wollen wir am Wochenende etwas unternehmen? Was möchtest du machen?'),cue:'Schlage Kino, Café oder einen Parkbesuch vor.',hints:[hint('映画を見たいです。','eiga o mitai desu.','Ich möchte einen Film sehen.'),hint('カフェに行きたいです。','kafe ni ikitai desu.','Ich möchte in ein Café gehen.'),hint('公園に行きたいです。','kōen ni ikitai desu.','Ich möchte in den Park gehen.')],routes:[route('cinema',/^(?:映画|えいが)を(?:見たいです|みたいです|見ましょう|みましょう)$/u,'day',{activity:'映画',activityRomaji:'eiga'}),route('cafe',/^かふぇに(?:行きたいです|いきたいです|行きましょう|いきましょう)$/u,'day',{activity:'カフェ',activityRomaji:'kafe'}),route('park',/^(?:公園|こうえん)に(?:行きたいです|いきたいです|行きましょう|いきましょう)$/u,'day',{activity:'公園',activityRomaji:'kōen'})]},
  day:{say:s=>line(`${s.activity}、いいですね。土曜日と日曜日、どちらがいいですか。`,`${s.activityRomaji}, ii desu ne. doyōbi to nichiyōbi, dochira ga ii desu ka.`,'Gute Idee. Passt dir Samstag oder Sonntag besser?'),cue:'Wähle Samstag oder Sonntag.',hints:[hint('土曜日がいいです。','doyōbi ga ii desu.','Samstag passt gut.'),hint('日曜日にしましょう。','nichiyōbi ni shimashō.','Nehmen wir Sonntag.')],routes:[route('saturday',/^(?:土曜日|どようび)(?:がいいです|にしましょう|でお願いします|でおねがいします|です)?$/u,'time',{day:'土曜日',dayRomaji:'doyōbi'}),route('sunday',/^(?:日曜日|にちようび)(?:がいいです|にしましょう|でお願いします|でおねがいします|です)?$/u,'time',{day:'日曜日',dayRomaji:'nichiyōbi'})]},
  time:{say:s=>line(`${s.day}ですね。何時に会いましょうか。`,`${s.dayRomaji} desu ne. nanji ni aimashō ka.`,'Gut. Um wie viel Uhr treffen wir uns?'),cue:'Diese Szene bietet 10 Uhr vormittags, 14 Uhr oder 15 Uhr.',hints:[hint('午前十時はどうですか。','gozen jūji wa dō desu ka.','Wie wäre es mit 10 Uhr vormittags?'),hint('午後二時がいいです。','gogo niji ga ii desu.','14 Uhr passt gut.'),hint('午後三時にしましょう。','gogo sanji ni shimashō.','Treffen wir uns um 15 Uhr.')],routes:[route('ten',/^(?:午前|ごぜん)?(?:十時|10時|じゅうじ)(?:はどうですか|がいいです|にしましょう|です)?$/u,'place',{time:'午前十時',timeRomaji:'gozen jūji'}),route('two',/^(?:(?:午後|ごご)(?:二時|2時|にじ)|14時)(?:はどうですか|がいいです|にしましょう|です)?$/u,'place',{time:'午後二時',timeRomaji:'gogo niji'}),route('three',/^(?:(?:午後|ごご)(?:三時|3時|さんじ)|15時)(?:はどうですか|がいいです|にしましょう|です)?$/u,'place',{time:'午後三時',timeRomaji:'gogo sanji'})]},
  place:{say:s=>line(`${s.time}ですね。駅の前で会いましょう。どうですか。`,`${s.timeRomaji} desu ne. eki no mae de aimashō. dō desu ka.`,'Gut. Treffen wir uns vor dem Bahnhof. Passt das?'),cue:'Stimme zu oder schlage das Café als Treffpunkt vor.',hints:[hint('はい、いいですね。','hai, ii desu ne.','Ja, das klingt gut.'),hint('カフェの前はどうですか。','kafe no mae wa dō desu ka.','Wie wäre es vor dem Café?')],routes:[route('station',/^(?:はい)?(?:いいですね|いいです|大丈夫です|だいじょうぶです|わかりました|分かりました)$/u,'done',{place:'駅の前',placeRomaji:'eki no mae'}),route('cafe',/^かふぇの(?:前|まえ)(?:はどうですか|がいいです)$/u,'done',{place:'カフェの前',placeRomaji:'kafe no mae'})]},
  done:end(s=>line(`では、${s.day}の${s.time}に、${s.place}で会いましょう。楽しみです。`, `dewa, ${s.dayRomaji} no ${s.timeRomaji} ni, ${s.placeRomaji} de aimashō. tanoshimi desu.`,'Dann steht unsere Verabredung. Ich freue mich darauf.'))
 }}
];

const sceneMap=new Map(SCENES.map(s=>[s.id,s]));
const object=v=>v&&typeof v==='object'&&!Array.isArray(v);
const text=(v,max=500)=>typeof v==='string'?v.slice(0,max):'';
function message(say,slots) {const value=typeof say==='function'?say(slots):say;return {role:'teacher',...value};}
export function cleanTalk(input) {
 const out={sessions:{},completed:{}};if(!object(input))return out;
 for(const scene of SCENES) {
  const count=input.completed?.[scene.id];if(Number.isSafeInteger(count)&&count>0)out.completed[scene.id]=Math.min(count,100000);
  const saved=input.sessions?.[scene.id];if(!object(saved)||saved.revision!==1||!scene.nodes[saved.node])continue;
  // Derive slot values by replaying accepted replies. Imported slot strings cannot alter tutor dialogue.
  let node=scene.start,derived={},accepted=0;
  const replies=Array.isArray(saved.replies)?saved.replies.slice(0,20):[];
  for(const reply of replies) {const route=scene.nodes[node].routes?.find(r=>r.pattern.test(normalizeTalk(reply)));if(!route)break;derived={...derived,...route.slots};node=route.next;accepted++;}
  if(node!==saved.node)continue;
  const history=Array.isArray(saved.history)?saved.history.slice(-40).filter(x=>object(x)&&['user','teacher'].includes(x.role)).map(x=>({role:x.role,jp:text(x.jp),romaji:text(x.romaji),de:text(x.de),source:['spoken','typed','selection'].includes(x.source)?x.source:undefined})).filter(x=>x.jp):[];
  // Render the current prompt from our authored graph, never from an imported last prompt.
  const current=message(scene.nodes[node].say,derived);if(history.at(-1)?.role==='teacher')history[history.length-1]=current;else history.push(current);
  out.sessions[scene.id]={revision:1,node,slots:derived,replies:replies.slice(0,accepted).map(r=>text(r,300)),history,teacherId:text(saved.teacherId,20),draft:text(saved.draft,300),source:['spoken','selection'].includes(saved.source)?saved.source:'typed',turn:Math.max(accepted,Math.min(100000,Number(saved.turn)||0))};
 }
 return out;
}

export class TalkSession {
 constructor(store,sceneId,teacherId='sakura',restore=true) {
  this.store=store;this.scene=sceneMap.get(sceneId);if(!this.scene)throw Error('Diese Gesprächsszene gibt es nicht.');
  store.data.talk=cleanTalk(store.data.talk);
  const saved=restore?store.data.talk.sessions[sceneId]:null;
  Object.assign(this,saved??{node:this.scene.start,slots:{},replies:[],history:[],teacherId,draft:'',source:'typed',turn:0});
  if(!this.history.length)this.history.push(this.prompt);this.feedback='';this.save();
 }
 get current(){return this.scene.nodes[this.node];}
 get done(){return this.current.done===true;}
 get prompt(){return message(this.current.say,this.slots);}
 get context(){return `talk:${this.scene.id}:${this.turn}`;}
 setDraft(value,source='typed'){this.draft=String(value??'').slice(0,300);this.source=['spoken','selection'].includes(source)?source:'typed';}
 save(){this.history=this.history.slice(-40);this.store.data.talk.sessions[this.scene.id]={revision:1,node:this.node,slots:{...this.slots},replies:[...this.replies],history:this.history,teacherId:this.teacherId,draft:this.draft,source:this.source,turn:this.turn};this.store.save();}
 respond() {
  if(this.done)return {accepted:false};const reply=this.draft.trim(),normalized=normalizeTalk(reply);
  if(!normalized){this.feedback='Sprich eine Antwort oder tippe sie ein.';return {accepted:false};}
  const repeat=/^(?:すみません)?(?:もう一度|もういちど|ゆっくり)(?:言ってください|いってください|お願いします|おねがいします)$/u.test(normalized);
  const picked=this.current.routes?.find(r=>r.pattern.test(normalized));
  this.history.push({role:'user',jp:reply,source:this.source});this.turn++;this.draft='';
  if(repeat) {
   this.feedback='Natürlich – höre die Frage noch einmal langsam an.';
   this.history.push(this.prompt);this.save();return {accepted:false,repeated:true,reply:this.prompt};
  }
  if(!picked) {
   this.feedback='Diese Antwort passt noch nicht zu den vorbereiteten Wegen dieser Offline-Szene. Prüfe den erkannten Text oder nutze eine Antwortidee.';
   this.draft=reply;this.save();return {accepted:false};
  }
  this.slots={...this.slots,...picked.slots};this.node=picked.next;this.replies.push(reply);this.feedback='';
  const next=this.prompt;this.history.push(next);
  if(this.done){const old=this.store.data.talk.completed[this.scene.id]??0;this.store.data.talk.completed[this.scene.id]=old+1;}
  this.save();return {accepted:true,reply:next,done:this.done,route:picked.id};
 }
}
