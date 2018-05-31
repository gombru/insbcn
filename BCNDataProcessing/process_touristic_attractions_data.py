from xml.dom import minidom
import json

xmldoc = minidom.parse('../../../datasets/instaBarcelona/opendataBCN/puntos_interes_turistico.xml')

out_dis = open('../../../datasets/instaBarcelona/opendataBCN/atracciones_per_district.json', 'w')
out_nei = open('../../../datasets/instaBarcelona/opendataBCN/atracciones_per_neigh.json', 'w')

districts = {}
neighbourhoods = {}

itemlist = xmldoc.getElementsByTagName('district')
print(len(itemlist))
for s in itemlist:
    # print(s.childNodes[0].nodeValue)
    cur_district = s.childNodes[0].nodeValue
    if cur_district in districts:
        districts[cur_district] += 1
    else:
        print "New district: " + cur_district
        districts[cur_district] = 1


itemlist = xmldoc.getElementsByTagName('barri')
print(len(itemlist))
for s in itemlist:
    # print(s.childNodes[0].nodeValue)
    cur_neigh = s.childNodes[0].nodeValue
    if cur_neigh in neighbourhoods:
        neighbourhoods[cur_neigh] += 1
    else:
        print "New neighbourhood: " + cur_neigh
        neighbourhoods[cur_neigh] = 1

print districts
print neighbourhoods

json.dump(districts,out_dis)
json.dump(neighbourhoods,out_nei)