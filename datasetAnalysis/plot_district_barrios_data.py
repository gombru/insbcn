import json
import operator
import matplotlib.pyplot as plt
import numpy as np

district_2_plot = "Gracia"
colors = ["r","g","b"]
neightbourhood_names = []


# CiutatVella
if district_2_plot == "CiutatVella":
    neightbourhood_names.append(['Barceloneta','labarceloneta','barceloneta'])
    neightbourhood_names.append(['Raval','elraval','raval'])
    neightbourhood_names.append(['Gotic','gothic','gotic','gotico','elgotic','elgotico','barriogotico','gtico','barriogtico','gtic'])
    neightbourhood_names.append(['Sant Pere','santpere','santacaterina','laribera','born','borne','elborne','elborn'])

# Eixample
if district_2_plot == "Eixample":
    neightbourhood_names.append(['SantAntoni','santantoni','sanantoni'])
    neightbourhood_names.append(['NovaEsquerra','esquerraeixample'])
    neightbourhood_names.append(['AntigaEsquerra','antigaesquerra'])
    neightbourhood_names.append(['DretaEixample','dretaeixample','eixampledreta'])
    neightbourhood_names.append(['FortPienc','elfortpienc','fortpienc'])
    neightbourhood_names.append(['SagradaFamilia','sagradafamilia'])

# SantMarti
if district_2_plot == "SantMarti":
    neightbourhood_names.append(['CampArpa','campdelarpa'])
    neightbourhood_names.append(['Verneda','verneda','lapau','laverneda'])
    neightbourhood_names.append(['Clot','clot','elclot'])
    neightbourhood_names.append(['SantMarti','santmarti','sanmarti','sanmarti','sanmartin'])
    neightbourhood_names.append(['Provencals','provenals'])
    neightbourhood_names.append(['Besos','besos','maresme','elmaresme','elbesos','bess','vilaolmpica','elbess'])
    neightbourhood_names.append(['DiagonalMar','diagonalmar'])
    neightbourhood_names.append(['Poblenou','poblenou','pueblonuevo'])
    neightbourhood_names.append(['VilaOlimpica','villaolimpica','vilaolimpica'])
    neightbourhood_names.append(['Llacuna','llacuna','lallacuna'])

# Sants
if district_2_plot == "Sants-Montjuic":
    neightbourhood_names.append(['Sants','sants'])
    neightbourhood_names.append(['Badal','badal','santsbadal'])
    neightbourhood_names.append(['Bordeta','labordeta','bordeta'])
    neightbourhood_names.append(['Hostafrancs','hostafrancs'])
    neightbourhood_names.append(['FontGuatlla','fontdelaguatlla'])
    neightbourhood_names.append(['MarinaPort','marinadelport'])
    neightbourhood_names.append(['MarinaPrat','prat','zonafranca'])
    neightbourhood_names.append(['PobleSec','poblesec','puebloseco'])


# Sarria
if district_2_plot == "Sarria-SantGervasi":
    neightbourhood_names.append(['Vallvidrera','vallvidreara','tibidabo','lesplanes','vallvidrera','vallvidriera'])
    neightbourhood_names.append(['Sarria','sarria','sarri'])
    neightbourhood_names.append(['Bonanova','bonanova','santgervasi','sangervasio'])
    neightbourhood_names.append(['TresTorres','lestrestorres','trestorres'])
    neightbourhood_names.append(['Putxet','elputxet','putget','elputget','farro','putxet'])
    neightbourhood_names.append(['Galvany','galvany','santgervasi','sangervasio'])

# Gracia
if district_2_plot == "Gracia":
    neightbourhood_names.append(['Vallcarca','vallcarca','penitents'])
    neightbourhood_names.append(['Coll','coll','elcoll'])
    neightbourhood_names.append(['Salut','salut','lasalut','lasalud'])
    neightbourhood_names.append(['VilaGracia','viladegracia','vilagracia'])
    neightbourhood_names.append(['GraciaNova','campgrassoti','grassot','gracianova','campdengrassot'])

print "Loading data"
with open("../../../datasets/instaBarcelona/barrios_data.json","r") as file:
    data = json.load(file)


# SINGLE PLOT PER LANGUAGE
# Plot % of images per district per language
# l_count = 0
# for lan, lan_data in data.iteritems():
#     for district, district_data in lan_data.iteritems():
#         if district != district_2_plot: continue
#         cur_data = {}
#         for barrio, val in district_data.iteritems():
#             if str(barrio) == "total": continue
#             cur_data[barrio] = val
#         barrio_count_sorted = []
#         barrio_sorted = sorted(cur_data.items(), key=operator.itemgetter(1), reverse=True)
#         for el in barrio_sorted: barrio_count_sorted.append(el[1])
#         x = range(len(barrio_count_sorted))
#         my_xticks = []
#         total = sum(barrio_count_sorted)
#         barrio_count_sorted = [float(c) / total * 100.0 for c in barrio_count_sorted]
#         for l in range(0, len(barrio_count_sorted)):
#             my_xticks.append(barrio_sorted[l][0])
#         plt.xticks(x, my_xticks, size=11, rotation='vertical')
#         width = 1 / 1.5
#         plt.bar(x, barrio_count_sorted, width, color=colors[l_count], align="center")
#         plt.title("% of images per neighbourhood (" + str(district) + " district, " +  str(lan) + ")")
#         plt.tight_layout()
#         plt.show()
#         l_count += 1

# PLOT TOGUETHER
mentions_data = [[],[],[]]
langs = ['en','es','ca']
names = [d[0] for d in neightbourhood_names]

for i,lan in enumerate(langs):
    for n in names: mentions_data[i].append(0)
    lan_data = data[lan]
    for neigh in lan_data[district_2_plot]:
        if str(neigh) == "total": continue
        assigned = False
        for n_idx, n in enumerate(neightbourhood_names):
            if neigh in n:
                mentions_data[i][n_idx] += lan_data[district_2_plot][neigh]
                assigned = True
        if not assigned: print "Not assigned: " + neigh

    total = sum(mentions_data[i])
    mentions_data[i] = [float(c) / total * 100.0 for c in mentions_data[i]]


x = np.asarray(range(len(names)))
plt.xticks(x, names, size=17, rotation=70)
width = 0.2

ax = plt.subplot(111)
l1 = ax.bar(x-width, mentions_data[0], width, color='r',align='center')
l2 = ax.bar(x, mentions_data[1], width, color='g',align='center')
l3 = ax.bar(x+width, mentions_data[2], width, color='b',align='center')
ax.legend((l1[0], l2[0], l3[0]), ('en', 'es', 'ca'), fontsize = 15)
# plt.title("% of images per neighbourhood (" + str(district_2_plot) + " district)")
plt.title(str(district_2_plot) + " district", fontsize=20)
plt.legend(fontsize="x-large")
plt.tight_layout()
plt.show()

