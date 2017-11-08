import matplotlib.pyplot as plt
import operator
from stop_words import get_stop_words
import json
from langdetect import detect, detect_langs



print "Loading data"
with open("../../../datasets/instaBarcelona/captions.json","r") as file:
    data = json.load(file)

symbols = ['.','/','\\',',']
stop = ['que','the','and','para','con','los','por','una','del','las','for','you','with','this','mas','are','como','that']
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

for k,v in data.iteritems():
    caption = v.replace('#', ' ')
    caption = caption.lower()
    lan = detect(caption)
    c_words = caption.split()

    # Filter stop_words
    filtered_words = []
    for i in c_words:
        if i not in stop: filtered_words.append(i)

    for w in filtered_words:

        # Filter short words
        if len(w) < 3: continue

        # Filter symbols
        symbol = False
        for s in symbols:
            if s in w:
                symbol = True
                break
        if symbol: continue

        if lan == 'en':
            l = 0

        if lan == 'es':
            l = 1

        if lan == 'ca':
            l = 2

        if w not in words[l]:
            words[l][w] = 1
        else:
            words[l][w] = words[l][w] + 1



print "Number of words en: " + str(len(words[0]))
print "Word with max repetitions has:  " + str(max(words[0].values()))

print "Number of words es: " + str(len(words[1]))
print "Word with max repetitions has:  " + str(max(words[1].values()))

print "Number of words ca: " + str(len(words[2]))
print "Word with max repetitions has:  " + str(max(words[2].values()))


#Plot
languages = ['en','es','ca']
for l in range(3):
    words_sorted = sorted(words[l].items(), key=operator.itemgetter(1))
    words_count_sorted = words[l].values()
    words_count_sorted.sort(reverse=True)
    topX = 20
    x = range(topX-1)
    my_xticks = []
    for l in range(1,topX):
        my_xticks.append(words_sorted[-l-1][0])
    plt.xticks(x, my_xticks, rotation=90, size=8)
    width = 1/1.5
    plt.bar(x, words_count_sorted[1:topX], width, color="blue", align="center")
    plt.title("Num of top words " + languages[l])
    plt.show()

print "Done"