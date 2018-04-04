import matplotlib.pyplot as plt
import operator
from stop_words import get_stop_words
import json

print "Loading languages ids"
en_ids = [line.strip('\n') for line in open("../../../ssd2/instaBarcelona/en_ids.txt", "r")]
es_ids = [line.strip('\n') for line in open("../../../ssd2/instaBarcelona/es_ids.txt", "r")]
ca_ids = [line.strip('\n') for line in open("../../../ssd2/instaBarcelona/ca_ids.txt", "r")]

print "Loading data"
with open("../../../ssd2/instaBarcelona/captions.json","r") as file:
    data = json.load(file)

# Get stop words
stop = ['que','the','and','para','con','los','por','una','del','las','for','you','with','this','mas','are','como','that','.','/','\\',',','instagood','picoftheday','like','',' ','photooftheday','photo','pic','vs','*','panathinaikos','pues','tbt','hem','mes','...','instagram','like4like','one','.',',','-','barcelona','bcn']

en_stop = get_stop_words('en')
for w in en_stop:
    stop.append(w)
es_stop = get_stop_words('es')
for w in es_stop:
    stop.append(w)
ca_stop = get_stop_words('ca')
for w in ca_stop:
    stop.append(w)

print "Counting words"
words = [dict() for x in range(3)]

c = 0
for k,v in data.iteritems():

    if k in en_ids: caption_lan = 0
    elif k in es_ids: caption_lan = 1
    elif k in ca_ids: caption_lan = 2
    else:
        print "Language not found"
        continue

    caption = v.replace('#', ' ')
    caption = caption.lower()
    c_words = caption.split()

    # Filter stop_words
    filtered_words = []
    for i in c_words:
        if i not in stop: filtered_words.append(i)

    for w in filtered_words:

        if w not in words[caption_lan]:
            words[caption_lan][w] = 1
        else:
            words[caption_lan][w] = words[caption_lan][w] + 1

    c+=1
    if c % 10000 == 0:
        print c

        print "Number of words en: " + str(len(words[0]))
        print "Word with max repetitions has:  " + str(max(words[0].values()))
        print "Number of words es: " + str(len(words[1]))
        print "Word with max repetitions has:  " + str(max(words[1].values()))
        print "Number of words ca: " + str(len(words[2]))
        print "Word with max repetitions has:  " + str(max(words[2].values()))

print words


#Plot
languages = ['en','es','ca']
colors = ["r","g","b"]
for l in range(3):
    print languages[l]
    words_sorted = sorted(words[l].items(), key=operator.itemgetter(1))

    # Print top words
    num2print = 50
    out = ""
    for i in range(num2print):
        out = out + ' ' + words_sorted[-i - 1][0]
    print out

    words_count_sorted = words[l].values()
    words_count_sorted.sort(reverse=True)
    topX = 20
    x = range(topX-1)
    my_xticks = []
    for c in range(1,topX):
        my_xticks.append(words_sorted[-c-1][0])
    plt.xticks(x, my_xticks, rotation=90, size=11)
    width = 1/1.5
    plt.bar(x, words_count_sorted[1:topX], width, color=colors[l], align="center")
    plt.tight_layout()
    plt.title("Instances of most repeated words (" + languages[l] + ")")
    plt.show()


with open('../../../ssd2/instaBarcelona/word_count_en.json','w') as file:
    json.dump(words[0],file)
with open('../../../ssd2/instaBarcelona/word_count_es.json','w') as file:
    json.dump(words[1],file)
with open('../../../ssd2/instaBarcelona/word_count_ca.json','w') as file:
    json.dump(words[2],file)

print "Done"