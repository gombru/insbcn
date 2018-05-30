from load_jsons import *

directory = '../../../datasets/instaBarcelona/img/'
data = load(directory)
print "Number of jsons: " + str(len(data))
locations = {}
for k, v in data.iteritems():
    if v['location'] is not None:
        if str(v['location']['slug']) in locations:
            locations[str(v['location']['slug'])] += 1
        else:
            locations[str(v['location']['slug'])] = 1

print locations
print "DONE"