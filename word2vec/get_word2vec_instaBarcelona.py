# Load trained LDA model and infer topics for unseen text.
# Make the train/val/test splits for CNN regression training
# It also creates the splits train/val/test randomly

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import glob
from random import randint
import string
from joblib import Parallel, delayed
import numpy as np
import gensim
import multiprocessing
import json

# Load data and model
base_path = '../../../hd/datasets/instaBarcelona/'
instaBCN_text_data_path = base_path + 'captions.json'
model_path = base_path + 'models/word2vec/word2vec_model_instaBarcelona.model'
tfidf_weighted = True
tfidf_model_path = base_path + 'models/tfidf/tfidf_model_instaBarcelona.model'
tfidf_dictionary_path = base_path + 'models/tfidf/docs.dict'

# Create output files
dir = "word2vec_mean_gt"
if tfidf_weighted: dir = "word2vec_tfidf_weighted_gt"
gt_path_train = base_path + dir + '/train_instaBarcelona_divbymax.txt'
gt_path_val = base_path + dir + '/val_instaBarcelona_divbymax.txt'
gt_path_test = base_path + dir + '/test_instaBarcelona_divbymax.txt'
train_file = open(gt_path_train, "w")
val_file = open(gt_path_val, "w")
test_file = open(gt_path_test, "w")

words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog']


model = gensim.models.Word2Vec.load(model_path)
tfidf_model = gensim.models.TfidfModel.load(tfidf_model_path)
tfidf_dictionary = gensim.corpora.Dictionary.load(tfidf_dictionary_path)


size = 300 # vector size
cores = multiprocessing.cpu_count()

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

whitelist = string.letters + string.digits + ' '


def infer_word2vec(id, caption):
    filtered_caption = ""
    caption = caption.replace('#', ' ')
    for char in caption:
        if char in whitelist:
            filtered_caption += char
    filtered_caption = filtered_caption.decode('utf-8').lower()
    #Gensim simple_preproces instead tokenizer
    tokens = gensim.utils.simple_preprocess(filtered_caption)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    tokens_filtered = [token for token in stopped_tokens if token in model.wv.vocab]


    embedding = np.zeros(size)

    if not tfidf_weighted:
        c = 0
        for tok in tokens_filtered:
            try:
                embedding += model[tok]
                c += 1
            except:
                #print "Word not in model: " + tok
                continue
        if c > 0:
            embedding /= c

    if tfidf_weighted:
        vec = tfidf_dictionary.doc2bow(tokens_filtered)
        vec_tfidf = tfidf_model[vec]
        for tok in vec_tfidf:
            word_embedding = model[tfidf_dictionary[tok[0]]]
            embedding += word_embedding * tok[1]

    embedding = embedding - min(embedding)
    # if sum(embedding) > 0:
    #     embedding = embedding / sum(embedding)
    if max(embedding) > 0:
        embedding = embedding / max(embedding)

    # out_string = ''
    # for t in range(0,size):
    #     out_string = out_string + ',' + str(embedding[t])

    return id, embedding



parallelizer = Parallel(n_jobs=cores)
tasks_iterator = (delayed(infer_word2vec)(id,caption) for id, caption in data.iteritems())
results = parallelizer(tasks_iterator)
count = 0
for r in results:
    # Create splits random
    if sum(r[1]) == 0:
        print "Continuing, sum = 0"
        continue
    try:
        out = str(r[0])
        for v in r[1]:
            out = out + ',' + str(v)
        out = out + '\n'
        split = randint(0,19)
        if split < 16:
            train_file.write(out)
        elif split == 19: val_file.write(out)
        else: test_file.write(out)
    except:
        print "Error writing to file: "
        print r[0]
        continue


train_file.close()
val_file.close()
test_file.close()

print "Done"
