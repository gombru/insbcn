# -*- coding: utf-8 -*-#

import matplotlib.pyplot as plt
import json
import operator
from joblib import Parallel, delayed
import numpy as np
import time


omited_words_file = open("../../../ssd2/instaBarcelona/words_2_filter.txt", "r")

en_ids = open("../../../ssd2/instaBarcelona/en_ids_dict.txt", "w")
es_ids = open("../../../ssd2/instaBarcelona/es_ids_dict.txt", "w")
ca_ids = open("../../../ssd2/instaBarcelona/ca_ids_dict.txt", "w")
out_file = open("../../../ssd2/instaBarcelona/lang_data_dict.json",'w')

languages = {'en': 0, 'es': 0, 'ca': 0}
dictionaries = {'en': 0, 'es': 0, 'ca': 0}

en = []
es = []
ca = []
omited_words = []

for line in omited_words_file:
    w = unicode(line.rstrip(), "utf-8")
    omited_words.append(w)

print omited_words

def read_dict(lan):
    print("Reading dictionary " + lan)
    dict = ""
    with open("../../../ssd2/instaBarcelona/dictionaries/" + lan + ".dict", "r") as file:
        for l in file:
            dict += l
    dict = dict.replace(' ','\n').splitlines()

    dict_words = []
    for w in dict:
         dict_words.append(unicode(w, "utf-8"))

    return dict_words

print "Loading data"
with open("../../../ssd2/instaBarcelona/captions.json","r") as file:
    data = json.load(file)

print "Reading dictionaries"
for k,v in languages.iteritems():
    dictionaries[k] = read_dict(k)

print "Counting languages"


def detect_lang(k,v):
    cap_lan = "unknown"
    caption = v.replace('#', ' ')
    caption = caption.lower()
    words = caption.replace(' ', '\n').splitlines()
    words_per_lang = {'en': 0, 'es': 0, 'ca': 0}
    for w in words:

        if len(w) < 3: continue

        if w in omited_words:
            continue

        for lan_key, dic_words in dictionaries.iteritems():
            if w in dic_words:
                words_per_lang[lan_key] += 1

    lan = max(words_per_lang.iteritems(), key=operator.itemgetter(1))[0]
    if words_per_lang[lan] > 0: cap_lan = lan

    if cap_lan is 'unknown':
        print "Lang not found"
        print caption

    return k + ',' + cap_lan


parallelizer = Parallel(n_jobs=12)
tasks_iterator = (delayed(detect_lang)(k,v) for k,v in data.iteritems())
r = parallelizer(tasks_iterator)
# merging the output of the jobs
strings = np.vstack(r)
print "Computing done, geting results ..."

dicarded = 0
for r in strings:
    k = r[0].split(',')[0]
    cap_lan = r[0].split(',')[1]
    if cap_lan == 'unknown':
        print "Unknown language"
        dicarded += 1
        continue
    if cap_lan == 'en': en.append(k)
    elif cap_lan == 'es': es.append(k)
    elif cap_lan == 'ca': ca.append(k)
    languages[cap_lan] +=  1

print "SELECTED LANGUAGES"
print languages
print "Number of languages: " + str(len(languages.values()))
print "Languages with max repetitions has:  " + str(max(languages.values()))
print "Discarded intances:  " + str(dicarded)

print "Saving id's per language"
for id in en: en_ids.write(str(id) + '\n')
for id in es: es_ids.write(str(id) + '\n')
for id in ca: ca_ids.write(str(id) + '\n')
en_ids.close()
es_ids.close()
ca_ids.close()

#Plot
lan_sorted = sorted(languages.items(), key=operator.itemgetter(1))
lan_count_sorted = languages.values()
lan_count_sorted.sort(reverse=True)
topX = min(10,len(lan_count_sorted))
x = range(topX)
my_xticks = []
for l in range(0,topX):
    my_xticks.append(lan_sorted[-l-1][0])
plt.xticks(x, my_xticks, size = 11)
width = 1/1.5
plt.bar(x, lan_count_sorted[0:topX], width, color="brown", align="center")
plt.title("Number of images per language")
plt.tight_layout()
plt.show()


#Plot %
lan_sorted = sorted(languages.items(), key=operator.itemgetter(1))
lan_count_sorted = languages.values()
lan_count_sorted.sort(reverse=True)
topX = min(10,len(lan_count_sorted))
x = range(topX)
my_xticks = []
total = sum(lan_count_sorted)
lan_count_sorted /= total * 100
for l in range(0,topX):
    my_xticks.append(lan_sorted[-l-1][0])
plt.xticks(x, my_xticks, size = 11)
width = 1/1.5
plt.bar(x, lan_count_sorted[0:topX], width, color="brown", align="center")
plt.title("% of images per language")
plt.tight_layout()
plt.show()


print "Done"