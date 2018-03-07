import json
import gensim
import string
from nltk.tokenize import RegexpTokenizer



langs = ['en','es','ca']

langs_ids = {}
for lan in langs:
    # Load lan ids
    langs_ids[lan] = []
    lan_ids_file = open("../../../ssd2/instaBarcelona/" + lan + "_ids.txt", "r")
    for line in lan_ids_file:
        langs_ids[lan].append(line.replace('\n', ''))
    lan_ids_file.close()

base_path = '../../../ssd2/instaBarcelona/'
instaBCN_text_data_path = base_path + 'captions.json'
out_file = open(base_path + 'barrios_data.json','w')


print "Creating disticts dictionary"
barrios = {}
barrios['CiutatVella'] = ['ciutatvella','barceloneta','labarceloneta','gotic','elgotic','raval','elraval','santpere','santacaterina','laribera','elgotico','gotico','gothic','barriogotico']
barrios['Eixample'] = ['eixample','ensanche','elfortpienc','fortpienc','sagradafamilia','dretadeleixample','dretaeixample','eixampledreta','antigaesquerradeleixample','santantoni','novaesquerradeleixample','eixampleesquerra']
barrios['Sants-Montjuic'] = ['sants','monjuic','santsmonjuic','puebloseco','poblesec','lamarinadelpratvermell','marinapratvermell','marinadeport','marinadelport','lafontdelaguatlla','fontdelaguatlla','hostafrancs','labordeta','bordeta','santsbadal','badal','zonafranca']
barrios['LesCorts'] = ['lescorts','corts','lamaternitat','lamaternidad','maternitat','maternidad','maternitatisantramon','maternidadysanramon','sanramon','santramon','pedralbes']
barrios['Sarria-SantGervasi'] = ['sarria','santgervasi','sarriasantgervasi','sarriasangervasio','sangervasio','vallvidrera','tibidabo','tibidaboilesplanes','lestrestorres','trestorres','santgervasibonanova','bonanova','santgervasigalvany','galvany','elputgetifarro','elputget','putget','farro']
barrios['Gracia'] = ['gracia','viladegracia','vilagracia','vallcarca','vallcarcaylospenitentes','lospenitentes','elspenitents','vallcarcaielspenitents','campdengrassot','campgrassot','grassot','gracianova']
barrios['Horta-Guinardo'] = ['horta','guinardo','hortaguinardo','baixguinardo','canbaro','elguinardo','lafontdenfargues','fontdenfargues','elcarmelo','elcarmel','carmelo','carmel','lateixonera','teixonera','santgenis','santgenisdelsagudells','montblau','elvalledhebron','valldhebron','laclota','clota','horta']
barrios['NouBarris'] = ['vilapicina','noubarris','vilapicinailatorrellobeta','torrellobeta','latorrellobeta','porta','turodelapeira','canpeguera','peguera','laguineueta','guineueta','canyelles','lesroquetes','roquetes','verdun','verdum','laprosperitat','latrinitatnova','trinitatnova','torrebaro','meridiana','ciutatmeridiana','vallbona']
barrios['SantAndreu'] = ['santandreu','sanandreu','sanandres','latrinitatvella','trinitatvella','barodeviver','elbuenpastor','elbonpastor','bonpastor','elcongresielsindians','congresielsindians','navas','sagrera','lasagrera','']
barrios['SantMarti'] = ['santmarti','sanmarti','sanmartin','elcampodelarpadelclot','elcampodelarpa','elcampdelarpa','campdelarpa','elcampdelarpadelclot','elclot','clot','elparcilallacunadelpoblenou','llacunadelpoblenou','llacuna','poblenou','pueblonuevo','vilaolimpica','vilaolimpicadelpoblenou','lavilaolimpica','diagonalmar','fontmaritimdelpoblenou','elbesos','besos','elbesosielmaresme','elmaresme','provenalsdelpoblenou','sanmartideprovenals','lavernedailapau','laverneda','verneda','lapau','']

print "Loading data"
with open(instaBCN_text_data_path,"r") as file:
    data = json.load(file)

whitelist = string.letters + string.digits + ' '
tokenizer = RegexpTokenizer(r'\w+')

out = {'en':{},'es':{},'ca':{}}

counter = 0

for id, caption in data.iteritems():

    counter += 1
    # Find language
    if id in langs_ids['en']: lan = 'en'
    elif id in langs_ids['es']: lan = 'es'
    elif id in langs_ids['ca']: lan = 'ca'

    # Get words in caption
    filtered_caption = ""
    caption = caption.replace('#', ' ')
    for char in caption:
        if char in whitelist:
            filtered_caption += char
    tokens = gensim.utils.simple_preprocess(filtered_caption)

    for barrio, barrio_words in data.iteritems:
        for barrio_word in barrio_words:
            if barrio_word in tokens: # This instance belongs to this barrio and to this barrio word
                # Check if element already existed in dict
                if barrio in out[lan]:
                    if barrio_word in out[lan][barrio]:
                        out[lan][barrio][barrio_word] += 1
                        out[lan]['total'] += 1
                    else:
                        print "New barrio found: " + barrio_word
                        out[lan]['total'] += 1
                else:
                    print "New district found: " + barrio
                    out[lan][barrio][barrio_word] = 1
                    out[lan]['total'] = 1

    if counter % 10000 == 0:
        print counter

json.dump(out_file, out)


print "DONE"