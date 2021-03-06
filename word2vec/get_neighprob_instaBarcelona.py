# Load trained LDA model and infer topics for unseen text.
# Make the train/val/test splits for CNN regression training
# It also creates the splits train/val/test randomly

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import os
from random import randint
import string
from joblib import Parallel, delayed
import numpy as np
import gensim
import multiprocessing
import json


lan = 'en'

# Load data and model
base_path = '../../../datasets/instaBarcelona/'
instaBCN_text_data_path = base_path + 'captions.json'
model_path = base_path + 'models/word2vec/word2vec_model_instaBarcelona_' + lan + '.model'

# Create output files
dir = "word2vec_l2norm_gt_" + lan
gt_path_train = base_path + dir + '/train_instaBarcelona_distribution_l2norm.txt'
gt_path_val = base_path + dir + '/val_instaBarcelona_distribution_l2norm.txt'
gt_path_test = base_path + dir + '/test_instaBarcelona_distribution_l2norm.txt'
train_file = open(gt_path_train, "w")
val_file = open(gt_path_val, "w")
test_file = open(gt_path_test, "w")

neighbourhoods = ['ciutatvella','barceloneta','gotic','raval','born','eixample','santantoni','novaesquerra','antigaesquerra','dretaeixample','portpienc','sagradafamilia','santsmontjuic','sants','badal','labordeta','hostafrancs','fontdelaguatlla','marinadeport','poblesec','marinadelpratvermell','lescorts','maternitat','pedralbes','sarriasantgervasi','sarria','santgervasi','lestrestorres','elputxet','labonanova','vallvidrera','gracia','gracianova','viladegracia','lasalut','elcoll','vallcarca','hortaguinardo','baixguinardo','elguinardo','canbaro','lafontdenfargues','elcarmel','laclota','lateixonera','lavalldhebron','horta','montbau','santgenisdelsagudells','noubarris','villapicina','porta','elturodelapeira','canpeguera','prosperitat','verdum','trinitatnova','laguineueta','lesroquetes','torrebaro','canyelles','vallbona','ciutatmeridiana','santandreu','navas','lasagrera','bonpastor','elcongresielsindians','santandreudelpalomar','barodeviver','trinitatvella','santmarti','villaolimpica','poblenou','diagonalmar','elbesos','provenals','llacuna','elclot','santmartideprovenals','campdelarpa','lavernedailapau']

print("Dimensionality = num neighbourhoods = " + str(len(neighbourhoods)))
words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog']


# Load lan ids
lan_ids = []
lan_ids_file = open("../../../datasets/instaBarcelona/" + lan + "_ids.txt", "r")
for line in lan_ids_file:
    lan_ids.append(line.replace('\n', ''))
lan_ids_file.close()

model = gensim.models.Word2Vec.load(model_path)

cores = multiprocessing.cpu_count()


def img_exists(path):
    im_path = base_path + "img_resized/" + path + ".jpg"
    return os.path.isfile(im_path)

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

    embedding = np.zeros(len(neighbourhoods))


    if id not in lan_ids: return id, embedding

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

    embedding = np.zeros(len(neighbourhoods))
    c = 0
    for tok in tokens_filtered:
        for i,n in enumerate(neighbourhoods):
            try:
                embedding[i] += model.wv.similarity(tok, n)
                c += 1
            except:
                # print "Error computing similarity: " + tok + " - " + n
                continue
    if c > 0:
        embedding /= c

    if min(embedding) < 0:
        embedding = embedding - min(embedding)

    # L2 normalized
    if sum(embedding) > 0:
        embedding = embedding / np.linalg.norm(embedding)

    return id, embedding


parallelizer = Parallel(n_jobs=cores)
tasks_iterator = (delayed(infer_word2vec)(id,caption) for id, caption in data.iteritems())
results = parallelizer(tasks_iterator)
count = 0
skipped = 0
for r in results:
    # Create splits random
    if sum(r[1]) == 0:
        print "Continuing, sum = 0"
        skipped += 1
        continue

    # Check if image file exists
    # if not img_exists(str(r[0])):
    #     print "Img file does not exist"
    #     continue

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
        count += 1
    except:
        print "Error writing to file: "
        print r[0]
        continue


train_file.close()
val_file.close()
test_file.close()

print "Done. Skipped: " + str(skipped)  + " Saved: " + str(count)
