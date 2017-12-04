import glob
import json

def load(path):
    data = {}
    print "Loading data"
    c = 0
    for file in glob.glob(path+ "/*.json"):
        c += 1
        if c % 10000 == 0:
            print c
        with open(file) as data_file:
            data[file.split('/')[-1][:-5]] = json.load(data_file)
    return data

