import glob
import json

def load(path):
    data = {}
    print "Loading data"
    c = 0
    for file in glob.glob(path+ "/*.json"):
        c += 1
        if c % 50000 == 0:
            print c
        with open(file) as data_file:
            try:
                data[file.split('/')[-1][:-5]] = json.load(data_file)
            except:
                print "Failed decoding JSON, skipping"
                continue
    return data

