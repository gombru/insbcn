import matplotlib.pyplot as plt
import json
import operator

lan_file = open("../../../datasets/instaBarcelona/lang_data.json","r")

languages = json.load(lan_file)

print languages
print "Number of languages: " + str(len(languages.values()))
print "Languages with max repetitions has:  " + str(max(languages.values()))


#Plot
lan_sorted = sorted(languages.items(), key=operator.itemgetter(1))
lan_count_sorted = languages.values()
lan_count_sorted.sort(reverse=True)
topX = min(10,len(lan_count_sorted))
x = range(topX)
my_xticks = []
for l in range(0,topX):
    my_xticks.append(lan_sorted[-l-1][0])
plt.xticks(x, my_xticks, size = 20)
width = 1/1.5
barlist = plt.bar(x, lan_count_sorted[0:topX], width, align="center")
barlist[0].set_color('r')
barlist[1].set_color('g')
barlist[2].set_color('b')
# plt.title("Number of images per language")
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
lan_count_sorted = [float(i) / total * 100.0 for i in lan_count_sorted]
for l in range(0,topX):
    my_xticks.append(lan_sorted[-l-1][0])
plt.xticks(x, my_xticks, size = 11)
width = 1/1.5
barlist = plt.bar(x, lan_count_sorted[0:topX], width, align="center")
barlist[0].set_color('r')
barlist[1].set_color('g')
barlist[2].set_color('b')
plt.title("% of images per language")
plt.tight_layout()
plt.show()




print "Done"