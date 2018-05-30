import json
import operator
import matplotlib.pyplot as plt
import numpy as np

print "Loading data"
with open("../../../datasets/instaBarcelona/barrios_data.json","r") as file:
    data = json.load(file)

colors = ["b","r","g"]

# PLOT PER LANGUAGE
# Plot % of images per district per language
# l_count = 0
# for lan, lan_data in data.iteritems():
#     cur_data = {'CiutatVella': 0, 'Eixample': 0, 'Sants-Montjuic': 0, 'LesCorts': 0, 'Sarria-SantGervasi': 0, 'Gracia': 0, 'Horta-Guinardo': 0, 'NouBarris': 0, 'SantAndreu': 0, 'SantMarti': 0}
#     for district, district_data in lan_data.iteritems():
#         cur_data[district] = district_data['total']
#     district_count_sorted = []
#     district_sorted = sorted(cur_data.items(), key=operator.itemgetter(1), reverse=True)
#     for el in district_sorted: district_count_sorted.append(el[1])
#     x = range(len(district_count_sorted))
#     my_xticks = []
#     total = sum(district_count_sorted)
#     district_count_sorted = [float(c)/total * 100.0 for c in district_count_sorted]
#     for l in range(0, len(district_count_sorted)):
#         my_xticks.append(district_sorted[l][0])
#     plt.xticks(x, my_xticks, size=10, rotation='vertical')
#     width = 1 / 1.5
#     plt.bar(x, district_count_sorted, width, color=colors[l_count], align="center")
#     plt.title("% of images per district (" + str(lan) + ")")
#     plt.ylim([0,35])
#     plt.tight_layout()
#     plt.show()
#     l_count += 1

# # PLOT TOGUETHER
# mentions_data = []
# districts = ['CiutatVella', 'Eixample', 'Sants-Montjuic', 'LesCorts', 'Sarria-SantGervasi', 'Gracia', 'Horta-Guinardo', 'NouBarris', 'SantAndreu', 'SantMarti']
#
# district_count_sorted_arr = []
# langs = ['en','es','ca']
# for i, lan in enumerate(langs):
#     lan_data = data[lan]
#     mentions_data.append([])
#     for district in districts:
#         mentions_data[i].append(lan_data[district]['total'])
#
#     total = sum(mentions_data[i])
#     mentions_data[i] = [float(c) / total * 100.0 for c in mentions_data[i]]
#
# x =  np.asarray(range(len(districts)))
# my_xticks = []
# for d in districts:
#     my_xticks.append(d)
# plt.xticks(x, districts, size=11, rotation=70)
# width = 0.2
# ax = plt.subplot(111)
# l1 = ax.bar(x-width, mentions_data[0], width, color='r',align='center')
# l2 = ax.bar(x, mentions_data[1], width, color='g',align='center')
# l3 = ax.bar(x+width, mentions_data[2], width, color='b',align='center')
#
# ax.legend((l1[0], l2[0], l3[0]), ('en', 'es', 'ca'))
#
# # plt.title("% of images per district")
# # plt.ylim([0,37])
# plt.tight_layout()
# plt.show()



# PLOT TOGUETHER WITH DEMOGRAPHY
# population = [6.2553329849,16.4372236334,11.2234075699,5.0612379374,9.2101536949,7.4868167687,10.4115290574,10.2775219042,9.1061932652,14.5305831841]
# youth = [29.895351475,21.6983964927,17.6917156836,20.8038228518,19.3376161416,22.7141997742,16.01649768,19.0396148374,19.2128406304,19.3624131152]
hotels = [28.3,28.8,9.7,8.4,5.4,1.4,1.4,0.4,0.3,15.8]
hotels_vs_pop = [0.2057022827, 0.07948972917, 0.03842898073 ,0.07542713076 ,0.02638150258, 0.008535485952 ,0.006057133991, 0.001982166563, 0.001513230543, 0.04912246257]
hotels_vs_pop_norm = []
for h in hotels_vs_pop:
    hotels_vs_pop_norm.append(100*h/sum(hotels_vs_pop))

hotels_sup = [19.2,8.7,6.5,8.1,4.3,4.1,2.2,3,1.2,6.6]
hotels_sup_norm = []
for h in hotels_sup:
    hotels_sup_norm.append(100*h/sum(hotels_sup))
mentions_data = []
districts = ['CiutatVella', 'Eixample', 'Sants-Montjuic', 'LesCorts', 'Sarria-SantGervasi', 'Gracia', 'Horta-Guinardo', 'NouBarris', 'SantAndreu', 'SantMarti']

district_count_sorted_arr = []
langs = ['en','es','ca']
for i, lan in enumerate(langs):
    lan_data = data[lan]
    mentions_data.append([])
    for district in districts:
        mentions_data[i].append(lan_data[district]['total'])

    total = sum(mentions_data[i])
    mentions_data[i] = [float(c) / total * 100.0 for c in mentions_data[i]]

x =  np.asarray(range(len(districts)))
plt.xticks(x, districts, size=11, rotation=70)
width = 0.15
ax = plt.subplot(111)

# hotels
l0 = ax.bar(x-width*1.5, hotels, width, color='y',align='center')
l1 = ax.bar(x-width*0.5, mentions_data[0], width, color='r',align='center')
l2 = ax.bar(x+width*0.5, mentions_data[1], width, color='g',align='center')
l3 = ax.bar(x+width*1.5, mentions_data[2], width, color='b',align='center')
# Population
# l4 = ax.bar(x+width, mentions_data, width, color='orange',align='center')
# Youth
# l5 = ax.bar(x+width*2, youth, width, color='y',align='center')



ax.legend((l0[0], l1[0], l2[0], l3[0]), ('hotel beds','en', 'es', 'ca'))

# plt.title("% of images per district")
# plt.ylim([0,40])
plt.tight_layout()
plt.show()


