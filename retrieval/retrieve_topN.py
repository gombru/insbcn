# Retrieves nearest images given a text query and saves them in an given folder

import string
import numpy as np
import operator
import os
from shutil import copyfile
from gensim import corpora, models
import gensim
import glove

data = 'instaBCN_Inception_frozen_word2vec_tfidf_iter_60000'
model_name = 'word2vec_model_instaBarcelona.model'
num_topics = 300 # Num LDA model topics
num_results = 15 # Num retrival results we want to take into accountnt

#-----------> if tfidf
tfidf_model_path = '../../../hd/datasets/instaBarcelona/models/tfidf/tfidf_model_instaBarcelona.model'
tfidf_dictionary_path = '../../../hd/datasets/instaBarcelona/models/tfidf/docs.dict'
tfidf_model = gensim.models.TfidfModel.load(tfidf_model_path)
tfidf_dictionary = gensim.corpora.Dictionary.load(tfidf_dictionary_path)

# Topic distribution given by the CNN to test images. .txt file with format city/{im_id},score1,score2 ...
database_path = '../../../hd/datasets/instaBarcelona/regression_output/' + data +'/test.txt'
model_path = '../../../hd/datasets/instaBarcelona/models/word2vec/' + model_name


# Load LDA model
print("Loading " +model_name+ " model ...")
model = models.Word2Vec.load(model_path)

def load_regressions_from_txt(path, num_topics):
    database = {}
    file = open(path, "r")
    print("Loading data ...")
    print(path)
    for line in file:
        d = line.split(',')
        regression_values = np.zeros(num_topics)
        for t in range(0,num_topics):
            regression_values[t] = d[t + 1]
        database[d[0]] = regression_values
    return database


def word2vec_tfidf(text, model, num_topics, tfidf_model, tfidf_dictionary):
    whitelist = string.ascii_letters + string.digits + ' '
    filtered_text = ''
    text = text.replace('#', ' ')
    for char in text:
        if char in whitelist:
            filtered_text += char
    filtered_text = filtered_text.lower()
    # Gensim simple_preproces instead tokenizer
    # en_stop = get_stop_words('en')
    tokens = gensim.utils.simple_preprocess(filtered_text)
    # stopped_tokens = [i for i in tokens if not i in en_stop]
    # tokens_filtered = [token for token in stopped_tokens if token in model.wv.vocab]
    embedding = np.zeros(num_topics)
    vec = tfidf_dictionary.doc2bow(tokens)
    vec_tfidf = tfidf_model[vec]
    for tok in vec_tfidf:
        word_embedding = model[tfidf_dictionary[tok[0]]]
        embedding += word_embedding * tok[1]
    embedding = embedding - min(embedding)
    if max(embedding) > 0:
        embedding = embedding / max(embedding)

    return embedding

# Load dataset
database = load_regressions_from_txt(database_path, num_topics)
for id in database:
    database[id] = database[id] / sum(database[id])

def get_results(database, topics, num_results, results_path):
    # Create empty dict for distances
    distances = {}
    #Compute distances
    for id in database:
        distances[id] = np.dot(database[id],topics)
    #Sort dictionary
    distances = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)
    # Get elements with min distances
    for idx,id in enumerate(distances):
        # Copy image results
        copyfile('../../../hd/datasets/instaBarcelona/img_resized/' + id[0] + '.jpg' , results_path + id[0].replace('/', '_') + '.jpg')
        if idx == num_results - 1: break

def get_results_complex(database, text, word_weights, num_results, results_path):

    words = text.split(' ')
    topics = np.zeros(num_topics)

    topics = word2vec_tfidf(text, model, num_topics, tfidf_model, tfidf_dictionary)
    topics = topics / len(words)

    # Create empty dict for distances
    distances = {}
    topics = topics / sum(topics)
    # Compute distances
    for id in database:
        distances[id] = np.dot(database[id], topics)
    # Sort dictionary
    distances = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)

    # Get elements with min distances
    for idx,id in enumerate(distances):
        # Copy image results
        copyfile('../../../hd/datasets/instaBarcelona/img_resized/' + id[0] + '.jpg', results_path + id[0].replace('/', '_') + '.jpg')
        if idx == num_results - 1: break


# Define queries
q = []
w = [] # Weights per word (can be negative)

word_list = ['sagradafamilia','gaudi','beer','cerveza','estrella','independencia','politica','politics','rambla','food','paella','sangria','healthy','burger','cocktail','restaurant','moritx','heineken','sanmiguel','vegan','healthyfood','sants','barri','gracia','sanantoni','santandreu','gotic','gothic','eixample','lescorts','poblenou','eurecat','pedralbes','sarria','poblesec','badalona','sitges']
for words in word_list:
    q.append(words)
    w.append('1')

word_list = ['sushi restaurant','healthy restaurant']
for words in word_list:
    q.append(words)
    w.append('1')



for e,cur_q in enumerate(q):
    print(cur_q)
    cur_w = w[e]
    results_path = "../../../hd/datasets/instaBarcelona/retrieval_results/" + data + "/" + cur_q.replace(' ', '_') + '__' + cur_w.replace(' ', '_') + '/'
    if not os.path.exists(results_path):
        print("Creating dir: " + results_path)
        os.makedirs(results_path)

    if len(cur_q.split(' ')) == 1:
        topics = word2vec_tfidf(cur_q, model, num_topics, tfidf_model, tfidf_dictionary)
        get_results(database, topics, num_results,results_path)

    else:
        get_results_complex(database, cur_q, cur_w, num_results, results_path)








