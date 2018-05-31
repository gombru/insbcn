import json

out_dis = open('../../../datasets/instaBarcelona/opendataBCN/pisos_uso_turistico_per_district.json', 'w')
out_nei = open('../../../datasets/instaBarcelona/opendataBCN/pisos_uso_turistico_per_neigh.json', 'w')


data = open('../../../datasets/instaBarcelona/opendataBCN/pisos_uso_turistico.csv', 'r')
districts = {}
neighbourhoods = {}

for i,line in enumerate(data):
    if i == 0: continue
    el = line.split(',')
    if el[1] in districts:
        districts[el[1]] += 1
    else:
        print "New district: " + el[1]
        districts[el[1]] = 1

    if el[2] in neighbourhoods:
        neighbourhoods[el[2]] += 1
    else:
        print "New neighbourhood: " + el[2]
        neighbourhoods[el[2]] = 1

print districts
print neighbourhoods

json.dump(districts,out_dis)
json.dump(neighbourhoods,out_nei)
