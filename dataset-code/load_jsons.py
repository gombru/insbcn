import glob
import json

def load(path):
    data = {}
    print "Loading data"
    for file in glob.glob(path+ "/*.json_toy"):
        with open(file) as data_file:
            data[file.split('/')[-1][:-9]] = json.load(data_file)
    return data

