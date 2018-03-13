from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import gensim
import string
import glob
import multiprocessing
import json
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lan = 'en'

cores = multiprocessing.cpu_count()

whitelist = string.letters + string.digits + ' '
instaBCN_text_data_path = '../../../ssd2/instaBarcelona/captions.json'
model_path = '../../../ssd2/instaBarcelona/models/word2vec/word2vec_model_instaBarcelona_' + lan + '.model'
words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog','wikipedia','google', 'flickr', 'figure', 'photo', 'image', 'homepage', 'url', 'youtube','wikipedia','google', 'flickr', 'figure', 'photo', 'image', 'homepage', 'url', 'youtube', 'images', 'blog', 'pinterest']


# Load lan ids
lan_ids = []
lan_ids_file = open("../../../ssd2/instaBarcelona/" + lan + "_ids.txt", "r")
for line in lan_ids_file:
    lan_ids.append(line.replace('\n', ''))
lan_ids_file.close()

print "Loading data"
with open(instaBCN_text_data_path,"r") as file:
    data = json.load(file)

size = 300 # vector size
min_count = 5 # minimum word count to 2 in order to give higher frequency words more weighting
iter = 50 # iterating over the training corpus x times
window = 8

#Initialize Tokenizer
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
es_stop = get_stop_words('es')
ca_stop = get_stop_words('ca')
for w in es_stop:
    en_stop.append(w)
for w in ca_stop:
    en_stop.append(w)

# add own stop words
for w in words2filter:
    en_stop.append(w)

posts_text = [] #List of lists of tokens

def get_instaBarcelona():
    lan_instances = 0
    for k, v in data.iteritems():
        if k in lan_ids:
            lan_instances +=1
            filtered_caption = ""
            caption = v.replace('#', ' ')
            for char in caption:
                if char in whitelist:
                    filtered_caption += char
            posts_text.append(filtered_caption.decode('utf-8').lower())
    print "Lan instances: " + str(lan_instances) + " , total instances: " + str(len(data))
    return posts_text

posts_text = get_instaBarcelona()

print "Number of posts: " + str(len(posts_text))

print "Creating tokens"
c= 0

texts = []
for t in posts_text:

    c += 1
    if c % 10000 == 0:
        print c

    try:
        #Gensim simple_preproces instead tokenizer
        tokens = gensim.utils.simple_preprocess(t)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        texts.append(stopped_tokens)
    except:
        continue

posts_text = []

#Train the model
print "Training ..."
model = gensim.models.Word2Vec(texts, size=size, min_count=min_count, workers=cores, iter=iter, window=window)

model.save(model_path)
print "DONE"