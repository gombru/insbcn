import matplotlib.pyplot as plt
import operator
from stop_words import get_stop_words
import json


# Load word counts
en_words = json.load(open('../../../datasets/instaBarcelona/word_count_en.json','r'))
es_words = json.load(open('../../../datasets/instaBarcelona/word_count_es.json','r'))
ca_words = json.load(open('../../../datasets/instaBarcelona/word_count_ca.json','r'))


words = [en_words, es_words, ca_words]
# words_2_filter = ['\xeb\xb0\x94\xeb\xa5\xb4\xec\x85\x80\xeb\xa1\x9c\xeb\x82\x98','visitbarcelona','gaud\xc3\xad','ig_barcelona','fcb','leomessi','ok_catalunya','\xe2\xad\x95\xe2\x97\xaf\xe2\x97\xa6','photographer','catalunyaexperience','barca','igerscatalunya','barcelonacity','instadaily','barcelonagram','igersbarcelona','igersbcn','travelgram','travelphotography','instatravel','m\xc3\xa9s','spain','catalunya','catalonia','espa\xc3\xb1a','catalu\xc3\xb1a','lecheria','venezuela','anzoategui','puertodelacruz','puertolacruz','dels','2017','vamos','gracias','gran','puedes','hoy','mejor','gusta','fin','guanta','as\xc3\xad','d\xc3\xada','solo','d\xc3\xadas','barcelona.','foto','photography']
# words_2_filter = ['\xeb\xb0\x94\xeb\xa5\xb4\xec\x85\x80\xeb\xa1\x9c\xeb\x82\x98','visitbarcelona','gaud\xc3\xad','ig_barcelona','fcb','leomessi','ok_catalunya','\xe2\xad\x95\xe2\x97\xaf\xe2\x97\xa6','photographer','catalunyaexperience','barca','igerscatalunya','barcelonacity','instadaily','barcelonagram','igersbarcelona','igersbcn','travelgram','travelphotography','instatravel','m\xc3\xa9s','spain','catalunya','catalonia','espa\xc3\xb1a','catalu\xc3\xb1a','lecheria','venezuela','anzoategui','puertodelacruz','puertolacruz','dels','2017','vamos','gracias','gran','puedes','hoy','mejor','gusta','fin','guanta','as\xc3\xad','d\xc3\xada','solo','d\xc3\xadas','barcelona.','foto','photography']
words_2_filter = ['lecheria', 'venezuela','anzoategui','puertolacruz','barcelona.','barca']
print "Number of words en: " + str(len(words[0]))
print "Word with max repetitions has:  " + str(max(words[0].values()))

print "Number of words es: " + str(len(words[1]))
print "Word with max repetitions has:  " + str(max(words[1].values()))

print "Number of words ca: " + str(len(words[2]))
print "Word with max repetitions has:  " + str(max(words[2].values()))

# Get current size
fig_size = plt.rcParams["figure.figsize"]
# Prints: [8.0, 6.0]
print "Current size:", fig_size
# Set figure width to 12 and height to 9
fig_size[0] = 6.5
fig_size[1] = 3
plt.rcParams["figure.figsize"] = fig_size

#Plot
languages = ['en','es','ca']
colors = ["r","g","b"]
for l in range(3):
    print languages[l]
    words_sorted = sorted(words[l].items(), key=operator.itemgetter(1))
    words_sorted = [w for w in words_sorted if len(w[0]) > 2 and str(w[0].encode('utf-8')) not in words_2_filter]

    # Print top words
    num2print =50
    out = ""
    for i in range(num2print):
        out = out + ' ' + words_sorted[-i - 1][0]
    print out

    words_count_sorted = words[l].values()
    words_count_sorted.sort(reverse=True)
    topX = 20
    x = range(topX-1)
    my_xticks = []
    for c in range(0,topX-1):
        my_xticks.append(words_sorted[-c-1][0])
    plt.xticks(x, my_xticks, rotation=90, size=11)
    width = 1/1.5
    plt.bar(x, words_count_sorted[0:topX-1], width, color=colors[l], align="center")
    # plt.title("Instances of most repeated words (" + languages[l] + ")")
    plt.tight_layout()
    plt.show()

print "Done"