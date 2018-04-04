import matplotlib.pyplot as plt
import plotly.plotly as py
import json
import operator
from langdetect import detect, detect_langs
from joblib import Parallel, delayed
import numpy as np

en_ids = open("../../../ssd2/instaBarcelona/en_ids.txt", "w")
es_ids = open("../../../ssd2/instaBarcelona/es_ids.txt", "w")
ca_ids = open("../../../ssd2/instaBarcelona/ca_ids.txt", "w")
out_file = open("../../../ssd2/instaBarcelona/lang_data.json",'w')

print "Loading data"
with open("../../../ssd2/instaBarcelona/captions.json","r") as file:
    data = json.load(file)

print "Counting languages"
languages = {'en': 0, 'es': 0, 'ca': 0}
en = []
es = []
ca = []

def detect_lang(k,v):
    cap_lan = "unknown"
    caption = v.replace('#', ' ')
    caption = caption.lower()
    it = 0
    while cap_lan == "unknown": # Using while because the LSTM gives different answers, and we are supposed to have fitlered other languages
        try:
            langs = detect_langs(caption)
            for cur_lan in langs:
                cur_lan_str = str(cur_lan).split(':')[0]
                if cur_lan_str in languages.keys():
                    cap_lan = cur_lan_str
                    break
        except:
            print "Lang detection failed. Continuing"
            return k + ',' + cap_lan
        it += 1
        if it == 10:
            print "Limit of iterations reached. Continuing"
            break

    if cap_lan is 'unknown':
        print caption
        print langs
        print "Lang not found"
        return k + ',' + cap_lan

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



print languages
print "Number of languages: " + str(len(languages.values()))
print "Languages with max repetitions has:  " + str(max(languages.values()))
print "Discarded intances:  " + str(dicarded)


json.dump(languages, out_file)
out_file.close()

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