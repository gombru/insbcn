import matplotlib.pyplot as plt
import operator
from stop_words import get_stop_words
import json


# Load word counts
en_words = json.load(open('../../../ssd2/instaBarcelona/word_count_en.json','r'))
es_words = json.load(open('../../../ssd2/instaBarcelona/word_count_es.json','r'))
ca_words = json.load(open('../../../ssd2/instaBarcelona/word_count_ca.json','r'))


words = [en_words, es_words, ca_words]
words_2_filter = ['lecheria','venezuela','anzoategi','puertodekacruz']


print "Number of words en: " + str(len(words[0]))
print "Word with max repetitions has:  " + str(max(words[0].values()))

print "Number of words es: " + str(len(words[1]))
print "Word with max repetitions has:  " + str(max(words[1].values()))

print "Number of words ca: " + str(len(words[2]))
print "Word with max repetitions has:  " + str(max(words[2].values()))


#Plot
languages = ['en','es','ca']
colors = ["r","g","b"]
for l in range(3):
    print languages[l]
    words_sorted = sorted(words[l].items(), key=operator.itemgetter(1))
    words_sorted = [w for w in words_sorted if len(w) > 2 and w not in words_2_filter]

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