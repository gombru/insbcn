import numpy as np
import matplotlib.pyplot as plt

neigh = ['ciutatvella','barceloneta','gotic','raval','born','eixample','santantoni','novaesquerra','antigaesquerra','dretaeixample','portpienc','sagradafamilia','santsmontjuic','sants','badal','labordeta','hostafrancs','fontdelaguatlla','marinadeport','poblesec','marinadelpratvermell','lescorts','maternitat','pedralbes','sarriasantgervasi','sarria','santgervasi','lestrestorres','elputxet','labonanova','vallvidrera','gracia','gracianova','viladegracia','lasalut','elcoll','vallcarca','hortaguinardo','baixguinardo','elguinardo','canbaro','lafontdenfargues','elcarmel','laclota','lateixonera','lavalldhebron','horta','montbau','santgenisdelsagudells','noubarris','villapicina','porta','elturodelapeira','canpeguera','prosperitat','verdum','trinitatnova','laguineueta','lesroquetes','torrebaro','canyelles','vallbona','ciutatmeridiana','santandreu','navas','lasagrera','bonpastor','elcongresielsindians','santandreudelpalomar','barodeviver','trinitatvella','santmarti','villaolimpica','poblenou','diagonalmar','elbesos','provenals','llacuna','elclot','santmartideprovenals','campdelarpa','lavernedailapau']
neigh = ['barceloneta','raval','gotic','born','poblesec','poblenou']
path = '../../../datasets/instaBarcelona/ImageNetfeatures/'
district_indices = [0,5,12,21,24,31,37,49,63,71]

def cos_sim(a, b):
	dot_product = np.dot(a, b)
	norm_a = np.linalg.norm(a)
	norm_b = np.linalg.norm(b)
	return dot_product / (norm_a * norm_b)

disimilarities = np.zeros(len(neigh))

for i,cur_neigh in enumerate(neigh):
    ca_features = np.loadtxt(path + 'ca/' + cur_neigh + '.txt')
    es_features = np.loadtxt(path + '/es/' + cur_neigh + '.txt')
    local_features = (ca_features + es_features) / 2
    en_features = np.loadtxt(path + '/en/' + cur_neigh + '.txt')
    disimilarities[i] = 1 - cos_sim(en_features, local_features)

x =  np.asarray(range(len(neigh)))
plt.xticks(x, neigh, size=8, rotation=70)
ax = plt.subplot(111)
barlist = ax.bar(x, disimilarities, color='b',align='center')
# for i in district_indices:
#     barlist[i].set_color('r')
plt.tight_layout()
plt.show()

