import matplotlib.pyplot as plt
import plotly.plotly as py
import json
import operator
from langdetect import detect, detect_langs

print "Loading data"
with open("../../../hd/datasets/instaBarcelona/captions.json","r") as file:
    data = json.load(file)

print "Counting languages"
languages = {}

for k,v in data.iteritems():
    caption = v.replace('#', ' ')
    caption = caption.lower()
    lan = detect(caption)

    if lan not in languages:
        languages[lan] = 1
    else:
        languages[lan] = languages[lan] + 1

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
plt.xticks(x, my_xticks)
width = 1/1.5
plt.bar(x, lan_count_sorted[0:topX], width, color="blue")
plt.title("Num of top languages")
plt.show()

print "Done"