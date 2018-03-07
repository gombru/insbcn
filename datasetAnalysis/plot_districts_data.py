import json
import operator
import matplotlib.pyplot as plt

print "Loading data"
with open("../../../ssd2/instaBarcelona/barrios_data.json","r") as file:
    data = json.load(file)

colors = ["r","g","b"]

# Plot % of images per district per language
l_count = 0
for lan, lan_data in data:
    cur_data = {'CiutatVella': 0, 'Eixample': 0, 'Sants-Montjui': 0, 'Eixample': 0, 'LesCorts': 0, 'Sarria-SantGervasi': 0, 'Gracia': 0, 'Horta-Guinardo': 0, 'NouBarris': 0, 'SantAndreu': 0, 'SantMarti': 0}
    for district, district_data in lan_data:
        cur_data[district] = district_data['total']

    district_sorted = sorted(cur_data.items(), key=operator.itemgetter(1))
    district_count_sorted = cur_data.values().sort(reverse=True)
    x = range(len(district_count_sorted))
    my_xticks = []
    total = sum(district_count_sorted)
    district_count_sorted /= total * 100
    for l in range(0, len(district_count_sorted)):
        my_xticks.append(district_sorted[-l - 1][0])
    plt.xticks(x, my_xticks, size=11)
    width = 1 / 1.5
    plt.bar(x, district_count_sorted, width, color=colors[l_count], align="center")
    plt.title("% of images per district (" + str(lan) + ")")
    plt.tight_layout()
    plt.show()
    l_count += 1

