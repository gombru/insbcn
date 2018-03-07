import matplotlib.pyplot as plt
import plotly.plotly as py
import json
import operator
from langdetect import detect, detect_langs

en_ids = open("../../../ssd2/instaBarcelona/en_ids.txt", "w")
es_ids = open("../../../ssd2/instaBarcelona/es_ids.txt", "w")
ca_ids = open("../../../ssd2/instaBarcelona/ca_ids.txt", "w")


print "Loading data"
with open("../../../ssd2/instaBarcelona/captions.json","r") as file:
    data = json.load(file)

print "Counting languages"
languages = {}
en = []
es = []
ca = []

for k,v in data.iteritems():
    caption = v.replace('#', ' ')
    caption = caption.lower()
    try:
        lan = detect(caption)
    except:
        print "Lang detection failed. Continuing"
        continue

    if lan not in languages:
        languages[lan] = 1
    else:
        languages[lan] = languages[lan] + 1

    if lan == 'en': en.append(k)
    elif lan == 'es': es.append(k)
    elif lan == 'ca': ca.append(k)


print languages
print "Number of languages: " + str(len(languages.values()))
print "Languages with max repetitions has:  " + str(max(languages.values()))


#Plot
lan_sorted = sorted(languages.items(), key=operator.itemgetter(1))
lan_count_sorted = languages.values()
lan_count_sorted.sort(reverse=True)
topX = min(3,len(lan_count_sorted))
x = range(topX)
my_xticks = []
for l in range(0,topX):
    my_xticks.append(lan_sorted[-l-1][0])
plt.xticks(x, my_xticks, size = 11)
width = 1/1.5
plt.bar(x, lan_count_sorted[0:topX], width, color="blue", align="center")
plt.title("Number of images per language")
plt.tight_layout()
plt.show()


print "Saving id's per language"
for id in en: en_ids.write(str(id) + '\n')
for id in es: es_ids.write(str(id) + '\n')
for id in ca: ca_ids.write(str(id) + '\n')
en_ids.close()
es_ids.close()
ca_ids.close()

print "Done"