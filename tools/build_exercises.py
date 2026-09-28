"""Author the bounded exercise expansion. Existing course cards remain untouched."""
from pathlib import Path
import json, hashlib, csv

ROOT = Path(__file__).resolve().parents[1]

# Explicit selection; never generate exercises indiscriminately for the whole course.
SELECTION = {
    'v11:kata-basics': [0,2,3], 'v11:kata-long': [0,1,4],
    '2:0': [0,2,3], '2:1': [0,1,2], '3:0': [1,2],
    'v11:first-meeting': [0,1,4], 'v11:asking-names': [0,1,3],
    'v11:countries': [0,1,2], 'v11:languages': [0,1,4],
    'v11:this-that': [0,1,2], 'v11:this-noun': [0,1,4],
    'v11:whose': [0,1,2], 'v11:here-there': [0,1,2],
    'v11:existence': [0,1,4], '5:0': [0,1,3],
    'v11:location-action': [0,1,4], 'v11:polite-past': [0,1,2],
    'v11:drinks': [0,1,2], 'v11:food-preferences': [0,1,4],
    '6:0': [0,1,2], 'v11:clock-hours': [0,1,4],
    'v11:inviting': [0,1,2], 'v11:read-profile': [0,1,2],
    'v11:read-day': [0,1,2], 'v11:read-plan': [0,1,2],
}

# Source card, meaningful JP chunks, the specifically heard chunk, its Romaji,
# and a hint which does not contain the answer. All contexts are taught first.
BUILD = {
 '2:0': (3,['わたし','は','がくせい','です'],2,'gakusei','Nenne zuerst das Thema, dann den Beruf oder Status. Die höfliche Endung steht am Schluss.'),
 '2:1': (2,['わたし','は','ドイツじん','です'],2,'Doitsujin','Unterscheide den Ländernamen von der Bezeichnung einer Person aus diesem Land.'),
 '3:0': (1,['がくせい','です','か'],0,'gakusei','Die Frage endet mit der höflichen Endung und der Fragepartikel.'),
 'v11:asking-names': (3,['さくら','と','いいます'],0,'Sakura','Hier wird der eigene Name genannt; nach dem Namen steht eine feste Form für heißen.'),
 'v11:languages': (4,['にほんご','を','べんきょうしています'],0,'nihongo','Gesucht ist die Sprache, die gelernt wird, nicht die Tätigkeit selbst.'),
 'v11:this-noun': (0,['この','ほん'],1,'hon','Die Form für dieses steht unmittelbar vor dem benannten Gegenstand.'),
 'v11:whose': (0,['わたし','の','ほん'],2,'hon','Der Besitzer steht vor der Verbindungspartikel, der Gegenstand danach.'),
 'v11:existence': (0,['ほん','が','あります'],0,'hon','Ein unbelebter Gegenstand wird genannt; die Existenzform folgt danach.'),
 '5:0': (3,['みず','を','のみます'],0,'mizu','Nenne das Getränk. Es ist das direkte Objekt der Handlung, nicht der Handelnde.'),
 'v11:location-action': (0,['えき','に','いきます'],0,'eki','Die Ortsangabe bezeichnet das Ziel einer Bewegung.'),
 'v11:food-preferences': (1,['にく','は','たべません'],0,'niku','Behalte die Verneinung am Ende bei: Es geht um etwas, das nicht gegessen wird.'),
 '6:0': (0,['コーヒー','を','ください'],0,'kōhī','Das bestellte Getränk steht vor der Objektpartikel; die Bitte folgt am Ende.'),
 'v11:read-profile': (0,['わたし','は','れん','です'],2,'Ren','Der Name steht nach dem Thema und vor der höflichen Endung.'),
 'v11:read-day': (0,['まいあさ','しちじ','に','おきます'],1,'shichiji','Die gehörte Angabe ist eine Uhrzeit. Die Zeitpartikel bleibt bereits im Satz stehen.'),
 'v11:read-plan': (0,['あした','きょうと','に','いきます'],1,'Kyōto','Gesucht ist das Reiseziel; der Zeitpunkt steht schon am Anfang.'),
}

# Deliberately specified complete solution combinations, not independent bags of words.
MULTI = {
 '2:0': (3,['わたし','□1','がくせい','□2'],['は','です'],['です','は'],
          'Ergänze die Themenmarkierung und die höfliche Satzendung.',
          ['は kennzeichnet hier, worüber gesprochen wird; es steht nach わたし und wird wa gelesen.','です schließt die höfliche Aussage über den Status ab.']),
 'v11:whose': (0,['□1','の','□2'],['わたし','ほん'],['ほん','わたし'],
          'Bilde ausdrücklich „mein Buch“, nicht „das Ich des Buches“.',
          ['Vor の steht hier der Besitzer: die sprechende Person.','Nach の steht der besessene Gegenstand, das Buch.']),
 '5:0': (3,['□1','を','□2'],['みず','のみます'],['のみます','みず'],
          'Ergänze „Ich trinke Wasser“: Getränk und höfliche Handlung.',
          ['Das Getränk steht vor を, das hier das direkte Objekt markiert.','Die höfliche Tätigkeit steht am Satzende; sie ist bejaht.']),
 'v11:location-action': (0,['えき','□1','□2'],['に','いきます'],['いきます','に'],
          'Ergänze die Zielmarkierung und „gehen“ für „Ich gehe zum Bahnhof“.',
          ['に steht nach dem Ort und markiert hier das Ziel der Bewegung.','いきます ist die höfliche bejahte Bewegungsform am Schluss.']),
 '6:0': (0,['□1','を','□2'],['コーヒー','ください'],['ください','コーヒー'],
          'Bestelle ausdrücklich einen Kaffee mit der gelernten Bitte.',
          ['Das gewünschte Getränk steht vor der Objektmarkierung を.','ください steht nach dem gewünschten Gegenstand mit を und bildet die Bitte.']),
}

READ = {
 'v11:read-profile': ('Was erfahren wir über Rens Beruf?', 'Ingenieur',
   {'Lehrkraft':'Der Text nennt einen anderen Beruf; eine Lehrkraft wird hier nicht erwähnt.',
    'Noch keinen Beruf genannt':'Der dritte Satz nennt den Beruf ausdrücklich.'}, 2),
 'v11:read-day': ('Was tut die Person vor der Busfahrt?', 'Sie frühstückt Brot.',
   {'Sie kommt nach Hause.':'Die Rückkehr steht nicht im hier gezeigten Morgenabschnitt.',
    'Sie liest abends.':'Abendliches Lesen ist kein Ereignis vor der gezeigten morgendlichen Busfahrt.'}, 1),
 'v11:read-plan': ('Wo wird die Begleitung getroffen?', 'Am Bahnhof',
   {'Im Zug':'Der Zug wird als Verkehrsmittel mit Abfahrtszeit genannt; dort steht nicht der Treffort.',
    'In Kyoto':'Kyoto ist das Reiseziel. Der Treffort wird im dritten Satz separat genannt.'}, 2),
}

# Explicit, already explained contrasts. Never put an unrelated whole sentence
# into a noun slot just to fill another button. Each item is in introduced cards
# or their explicitly explained parts (checked in the structure test).
CHOICE = {
 '2:0': (2,'わたし','ich'), '2:1': (2,'ドイツ','Deutschland'),
 '3:0': (0,'そう','so / das ist so'),
 'v11:asking-names': (0,'なまえ','Name, nicht der Eigenname Sakura'),
 'v11:languages': (0,'ドイツご','Deutsch'),
 'v11:this-noun': (1,'ペン','Stift'), 'v11:whose': (2,'ペン','Stift'),
 'v11:existence': (0,'ねこ','Katze; für ein lebendes Tier verwendet man außerdem います'),
 '5:0': (2,'たべます','essen / werde essen, höflich'),
 'v11:location-action': (0,'いえ','Zuhause'),
 'v11:food-preferences': (0,'すし','Sushi'),
 '6:0': (None,'ありがとうございます。','Vielen Dank, höflich'),
 'v11:read-profile': (2,'エンジニア','Ingenieur'),
 'v11:read-day': (1,'はちじ','acht Uhr'),
 'v11:read-plan': (1,'えき','Bahnhof'),
}

RECALL_HINTS = {
 'v11:kata-basics':'Gesucht ist das kurze Katakana-Wort für ein öffentliches Verkehrsmittel, keine Unterkunft.',
 'v11:kata-long':'Beim Getränk ist der erste Vokal lang. Der Endkonsonant erhält im Japanischen einen kurzen Vokal.',
 '2:0':'Du stellst deinen Status vor. Das eigene Thema darf im eindeutigen Vorstellungskontext entfallen; bleibe bei der höflichen Endung.',
 '2:1':'Nenne die Staatsangehörigkeit, nicht nur das Land. Der Personenbestandteil steht nach dem Ländernamen.',
 '3:0':'Du bestätigst die gerade gestellte Frage mit der eingeführten bejahenden Antwort.',
 'v11:first-meeting':'Es ist ein Abschied bis zum nächsten Tag, keine Begrüßung beim ersten Treffen.',
 'v11:asking-names':'Nenne den eingeführten Namen. Die feste Form für heißen folgt danach.',
 'v11:countries':'Gesucht ist der eingeführte Ländername in Katakana, keine Bezeichnung seiner Bewohner.',
 'v11:languages':'Nenne zuerst die Sprache und danach die Tätigkeit des Lernens. Die Endung beschreibt das laufende Lernen.',
 'v11:this-that':'Der Gegenstand ist von beiden Gesprächspartnern entfernt; denke an den dritten Ausdruck der Gruppe.',
 'v11:this-noun':'Der Stift ist bei dir. Die demonstrative Form steht unmittelbar vor dem Gegenstand.',
 'v11:whose':'Du fragst nach dem Besitzer einer Tasche. Die Verbindung zwischen Besitzer und Gegenstand bleibt erhalten.',
 'v11:here-there':'Es geht um einen Ort, der von euch beiden entfernt liegt, nicht um einen Gegenstand.',
 'v11:existence':'Der Ort ist hier; gemeint ist ein unbelebtes Ding. Die Ortsangabe steht vor der Existenzform.',
 '5:0':'Nenne zuerst das Getränk und markiere es als direktes Objekt. Die höfliche bejahte Tätigkeit folgt am Schluss.',
 'v11:location-action':'Es geht um eine Bewegung zu einer bestimmten Uhrzeit; die Zeitangabe wird mit der passenden Partikel verbunden.',
 'v11:polite-past':'Die Handlung ist bereits geschehen und wird nicht verneint. Achte auf die höfliche Vergangenheitsendung.',
 'v11:drinks':'Das Katakana-Getränk hat zwei lange Vokale; lass diese beim Sprechen hörbar bestehen.',
 'v11:food-preferences':'Du bewertest etwas bereits Gegessenes positiv. Die Adjektivform verweist auf die Vergangenheit.',
 '6:0':'Hier ist die höfliche Dankeswendung gefragt, keine Bestellung oder Preisfrage.',
 'v11:clock-hours':'Im Deutschen wird die kommende Stunde genannt. Im Japanischen nennst du die bereits begonnene Stunde und eine Hälfte.',
 'v11:inviting':'Verwende die eingeführte Einladung: Die verneinte Frageform lädt zu einer gemeinsamen Handlung ein.',
 'v11:read-profile':'Nenne den Beruf aus der Vorstellung; das Thema Beruf steht am Anfang des Satzes.',
 'v11:read-day':'In diesem Satz geht es um Abfahrtszeit und Verkehrsmittel. Die Mittelpartikel verbindet das Verkehrsmittel mit der Bewegung.',
 'v11:read-plan':'Das Treffen hat einen Ort und eine Person. Unterscheide Handlungsort und die Person, die getroffen wird.',
}

def main():
 raw=json.loads((ROOT/'data/course.json').read_text(encoding='utf8'))
 details=json.loads((ROOT/'data/deep_lessons.json').read_text(encoding='utf8'))
 lessons={l.get('id',f'{ui}:{li}'):l for ui,u in enumerate(raw['units']) for li,l in enumerate(u['lessons'])}
 packs=[];tasks=[]
 def add(pack,kind,suffix,card_index,prompt,**fields):
  key=pack['lesson'];card=lessons[key]['cards'][card_index]
  p=card.get('detail') or details['profiles'].get(card['jp'])
  assert p, (key,card_index)
  target=next((t for t in lessons[key].get('speech',[]) if t['target'].rstrip('。！？!?')==card['jp'].rstrip('。！？!?')),None)
  task={'id':f'ex1:{key}:{suffix}','revision':1,'lesson':key,'card':f'{key}:{card_index}',
        'family':kind,'phase':{'pairs':'meaning','echo':'speak','recall':'apply','hear_gap':'listen','choice_gap':'apply','multi_gap':'build','translate':'build','read':'apply'}[kind],
        'goal':prompt,'prompt':prompt,'prerequisites':pack['introduced'],
        'audio':card['jp'],'reading':card['romaji'],
        'accepted_speech':list(dict.fromkeys([card['jp']]+(target or {}).get('accept',[]))),
        'hint':p['pitfall'],'why':p['explain'],'solution':card['jp']+' · '+card['romaji']+' · '+card['de'],
        'repeat':None,**fields}
  tasks.append(task);pack['tasks'].append(task['id']);return task
 for key,indices in SELECTION.items():
  lesson=lessons[key];cards=lesson['cards']
  pack={'lesson':key,'title':lesson['title'],'introduced':[f'{key}:{i}' for i in indices],'tasks':[]}
  packs.append(pack)
  # Each selected card is explicitly introduced, with the complete original profile.
  pairs=[{'id':f'p{i}','card':f'{key}:{i}','jp':cards[i]['jp'],'de':cards[i]['de'],'reading':cards[i]['romaji']} for i in indices]
  assert len({p['jp'] for p in pairs})==len(pairs)==len({p['de'] for p in pairs})
  # Avoid isolated grammatical particles as speech targets.
  speak_index=next(i for i in reversed(indices) if len(cards[i]['jp'].rstrip('。'))>=2)
  echo=add(pack,'echo','echo',speak_index,'Sprich die sichtbare Vorlage nach. Text, Bedeutung und Aussprachehilfe bleiben sichtbar.')
  ptext=add(pack,'pairs','pairs-text',indices[0],'Ordne die eingeführten Ausdrücke ihren Bedeutungen zu.',pairs=pairs,mode='text',hint='Verbinde jeden Ausdruck mit genau einer Bedeutung. Du kannst eine Zuordnung vor dem Prüfen ändern.')
  recall=add(pack,'recall','recall',speak_index,'Sag das auf Japanisch: '+cards[speak_index]['de']+'. Verwende die in der Einführung erklärte Form.',hint=RECALL_HINTS[key])
  paudio=add(pack,'pairs','pairs-audio',indices[0],'Höre die Ausdrücke und verbinde sie mit ihrer Bedeutung.',pairs=pairs,mode='audio',phase='listen',hint='Höre ein Feld vollständig an. Danach wähle seine Bedeutung; erneutes Anhören ist möglich.')
  ptext['repeat']=paudio['id'];paudio['repeat']=ptext['id'];echo['repeat']=recall['id'];recall['repeat']=echo['id']
  omitted={'2:0':['がくせいです','学生です'],'2:1':['ドイツじんです','ドイツ人です']}.get(key,[])
  recall['accepted_speech']=list(dict.fromkeys(recall['accepted_speech']+omitted))
  if key in BUILD:
   i,chunks,gap,reading,hint=BUILD[key]
   assert ''.join(chunks)==cards[i]['jp'].rstrip('。'), (key,chunks)
   tokens=[{'id':f't{j}','text':v} for j,v in enumerate(chunks)]
   solutions=[chunks]
   if key in ('2:0','2:1','v11:read-profile'):solutions.append(chunks[2:])
   build=add(pack,'translate','build-jp',i,'Setze die vorbereitete japanische Entsprechung zusammen: '+cards[i]['de'],tokens=tokens,solutions=solutions,direction='de-ja',hint=hint)
   hear=add(pack,'hear_gap','hear-gap',i,'Höre den Satz. Ergänze nur die markierte Einheit in Romaji.',frame=''.join(chunks[:gap])+ ' □ '+''.join(chunks[gap+1:]),answers=[reading]+(['doitsu-jin'] if key=='2:1' else []),input_mode='romaji',hint=hint)
   build['repeat']=hear['id'];hear['repeat']=build['id']
   choice_gap,other,other_meaning=CHOICE[key]
   target=cards[i]['jp'] if choice_gap is None else chunks[choice_gap]
   frame='□ (ganze höfliche Wendung)' if choice_gap is None else ''.join(chunks[:choice_gap])+' □ '+''.join(chunks[choice_gap+1:])
   choices=[{'id':'right','text':target,'feedback':ptext['why'] if choice_gap is None else hint},
            {'id':'other','text':other,'feedback':f'Diese Form bedeutet hier „{other_meaning}“. Das entspricht nicht dem ausdrücklich vorgegebenen Inhalt. Andere Kontexte sind damit nicht ausgeschlossen.'}]
   add(pack,'choice_gap','choice-gap',i,'Ergänze genau diese Bedeutung: '+cards[i]['de'],frame=frame,choices=choices,answers=['right'],hint=hint,repeat=build['id'])
  if key in MULTI:
   i,frame,solution,pool,prompt,feedback=MULTI[key]
   add(pack,'multi_gap','multi-gap',i,prompt,frame=frame,tokens=[{'id':f'm{j}','text':v} for j,v in enumerate(pool)],solutions=[solution],slot_feedback=feedback,hint='Wähle eine nummerierte Lücke und setze einen Baustein ein. Die vollständige Kombination muss zum vorgegebenen Inhalt passen.',repeat=f'ex1:{key}:build-jp')
  if key in ('5:0','v11:location-action','6:0'):
   i=BUILD[key][0]
   german={'5:0':['Ich','trinke','Wasser.'],'v11:location-action':['Ich','gehe','zum','Bahnhof.'],'6:0':['Einen','Kaffee,','bitte.']}[key]
   variants=[german]
   if key=='5:0':german=['ich','trinke','Wasser'];variants=[german,['Wasser','trinke','ich']]
   add(pack,'translate','build-de',i,'Übersetze ins Deutsche: '+cards[i]['jp'],tokens=[{'id':f'd{j}','text':v} for j,v in enumerate(german)],solutions=variants,direction='ja-de',hint='Alle nötigen deutschen Bausteine stehen bereit. Eine passende deutsche Umstellung ist bei dieser Aufgabe mitgeprüft.',repeat=f'ex1:{key}:build-jp')
  if key in READ:
   question,answer,wrong,evidence=READ[key]
   add(pack,'read','read',evidence,question,text='。'.join(cards[j]['jp'].rstrip('。') for j in indices)+'。',evidence=cards[evidence]['jp'].rstrip('。'),choices=[{'id':'right','text':answer,'feedback':'Der hervorgehobene Satz beantwortet die Frage.'}]+[{'id':f'w{j}','text':v,'feedback':reason} for j,(v,reason) in enumerate(wrong.items())],answers=['right'],hint='Lies die Sätze im Zusammenhang. Achte darauf, welche Angabe die Frage tatsächlich verlangt.')
 result={'revision':1,'course_revision':raw['revision'],'packs':packs,'tasks':tasks}
 (ROOT/'data/exercises.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 with (ROOT/'UEBUNGSTYPEN_ABDECKUNG.csv').open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.writer(f);writer.writerow(['Aufgaben-ID','Familie','Variante','Lektion','Karte','Kompetenz','Eingeführt vor Prüfung','Plattformnachweis'])
  for t in tasks:writer.writerow([t['id'],t['family'],t.get('mode',t.get('direction','')),t['lesson'],t['card'],t['phase'],' | '.join(t['prerequisites']),'Noch zu prüfen'])
 print(len(packs),'Lektionen;',len(tasks),'Aufgaben;',sorted({t['family'] for t in tasks}))

if __name__=='__main__':main()
