import json
import operator
import matplotlib.pyplot as plt


districts_2_plot = ["CiutatVella"]
colors = ["r","g","b"]


print "Loading data"
with open("../../../ssd2/instaBarcelona/barrios_data.json","r") as file:
    data = json.load(file)

# Plot % of images per district per language
l_count = 0
for lan, lan_data in data:
    for district, district_data in lan_data:
        if district not in districts_2_plot: continue
        cur_data = {}
        for barrio, val in district_data:
            if barrio is "total": continue
            if barrio in val:
                cur_data[barrio] += 1
            else:
                cur_data[barrio] = 1

        barrio_sorted = sorted(cur_data.items(), key=operator.itemgetter(1))
        barrio_count_sorted = cur_data.values().sort(reverse=True)
        x = range(len(barrio_count_sorted))
        my_xticks = []
        total = sum(barrio_count_sorted)
        barrio_count_sorted /= total * 1
        for l in range(0, len(barrio_count_sorted)):
            my_xticks.append(barrio_sorted[-l - 1][0])
        plt.xticks(x, my_xticks, size=11)
        width = 1 / 1.5
        plt.bar(x, barrio_count_sorted, width, color=colors[l_count], align="center")
        plt.title("% of images per neighbourhood (" + str(district) + " district, " +  str(lan) + ")")
        plt.tight_layout()
        plt.show()
        l_count += 1

