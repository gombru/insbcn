from load_jsons import *
import json
from shutil import copyfile
from langdetect import detect, detect_langs

filtered_jsons_dir = "../../../ssd2/instaBarcelona/json_filtered/"
output_file_path = "../../../ssd2/instaBarcelona/captions.json"

word_TH = 3

data = load("../../../ssd2/instaBarcelona/json/")
print "Number of jsons: " + str(len(data))

# Load duplicated blacklist
duplicated_blacklist = []
users_blacklist_file = open("../../../ssd2/instaBarcelona/duplicated_blacklist.txt", "r")
for line in users_blacklist_file:
    duplicated_blacklist.append(line.replace('\n', ''))
duplicated_blacklist.close()
print("Blacklisted imgs: " + str(len(duplicated_blacklist)))

# Load users blacklist
users_blacklist = []
users_blacklist_file = open("../../../ssd2/instaBarcelona/users_blacklist50.txt", "r")
for line in users_blacklist_file:
    users_blacklist.append(line.replace('\n', ''))
print("Blacklisted users: " + str(len(users_blacklist)))
users_blacklist_file.close()

# City names to filter: We'll filter images containing other city names appart from barcelona. That will discard spam
cities = []
cities_file = open("../../../ssd2/instaBarcelona/cities.txt", "r")
for line in cities_file:
    cities.append(line.replace('\n', ''))
print("Blacklisted cities: " + str(len(cities)))
cities_file.close()

discarded_by_user = 0
discarded_by_city = 0
discarded_by_short_caption = 0
discarded_by_nul_caption = 0
discarded_by_lan = 0
discarded_by_duplicated = 0


output_data = {}

c = 0

for k, v in data.iteritems():

    c += 1
    if c % 50000 == 0:
        print c

    # Discard by user
    if v['owner']['id'] in users_blacklist:
        discarded_by_user += 1
        if discarded_by_user % 500 == 0:
            print "Num of posts dicarded by user: " + str(discarded_by_user)
        continue

    # Discard by duplicated
    if k in duplicated_blacklist:
        discarded_by_duplicated += 1
        if discarded_by_duplicated % 500 == 0:
            print "Num of posts dicarded by duplicated: " + str(discarded_by_duplicated)
        continue

    # Check if post has caption
    if 'caption' not in v:
        discarded_by_nul_caption += 1
        if discarded_by_nul_caption % 500 == 0:
            print "Num of posts dicarded by no caption: " + str(discarded_by_nul_caption)
        continue

    # Preprocess text: Here I only filter to be able to look for cities. The text processing will be done when training text models, because I want to save the captions as they are
    caption = v['caption']
    caption = caption.replace('#', ' ')
    caption = caption.lower()
    words = caption.split()

    # Check num of words. Discard if under the threshold
    if len(words) < word_TH:
        discarded_by_short_caption += 1
        if discarded_by_short_caption % 1000 == 0:
            print "Num of posts dicarded by short caption: " + str(discarded_by_short_caption)
        continue

    # Check if caption contains cities
    cur_discarded = False
    for city in cities:
        if city in caption:
            discarded_by_city += 1
            if discarded_by_city % 1000 == 0:
                print "Num of posts dicarded by city: " + str(discarded_by_city)
            cur_discarded = True
            break
    if cur_discarded: continue

    # Check language
    try:
        languages = detect_langs(caption)
        languages_names = []
        for l in languages:
            languages_names.append(l.lang)

        if 'en' not in languages_names and 'es' not in languages_names and 'ca' not in languages_names:
            discarded_by_lan += 1
            if discarded_by_lan % 1000 == 0:
                print "Num of posts dicarded by language: " + str(discarded_by_lan)
            continue
    except:
        print "Error detecting language, continuing"
        discarded_by_lan += 1
        continue

    # Else save the data in a dir with keys the id and with values the captions (originals)
    output_data[k] = v['caption']

    # And save the original json in a separate folder
    with open(filtered_jsons_dir + k + '.json', 'w') as outfile:
        json.dump(v, outfile)

print "Discards: No captions: " + str(discarded_by_nul_caption) + " Short: " + str(
    discarded_by_short_caption) + " City: " + str(discarded_by_city) + " User: " + str(
    discarded_by_user) + " Language: " + str(discarded_by_lan) + " Duplicated: " + str(discarded_by_duplicated)
print "Number of original vs resulting elements: " + str(len(output_data)) + " vs " + str(len(data))

print "Saving JSON"
with open(output_file_path, 'w') as outfile:
    json.dump(output_data, outfile)

print "Done"
