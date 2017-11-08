from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import gensim
import string
import glob
import multiprocessing
import json
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


cores = multiprocessing.cpu_count()

base_path = '../../../hd/datasets/instaBarcelona/'

whitelist = string.letters + string.digits + ' '
instaBCN_text_data_path = base_path + 'captions.json'
model_name = 'tfidf_model_instaBarcelona.model'
model_path = base_path + 'models/tfidf/'
words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog','wikipedia','google', 'flickr', 'figure', 'photo', 'image', 'homepage', 'url', 'youtube','wikipedia','google', 'flickr', 'figure', 'photo', 'image', 'homepage', 'url', 'youtube', 'images', 'blog', 'pinterest']

print "Loading data"
with open(instaBCN_text_data_path,"r") as file:
    data = json.load(file)

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
    for k, v in data.iteritems():
        filtered_caption = ""
        caption = v.replace('#', ' ')
        for char in caption:
            if char in whitelist:
                filtered_caption += char
        posts_text.append(filtered_caption.decode('utf-8').lower())
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

dictionary = gensim.corpora.Dictionary(texts)
dictionary.save(model_path +  'docs.dict')
raw_corpus = [dictionary.doc2bow(t) for t in texts]
gensim.corpora.MmCorpus.serialize(model_path + 'docs.mm', raw_corpus)
dictionary = gensim.corpora.Dictionary.load(model_path + 'docs.dict')
corpus = gensim.corpora.MmCorpus(model_path + 'docs.mm')
model = gensim.models.TfidfModel(corpus)
model.save(model_path + model_name)
print "DONE"