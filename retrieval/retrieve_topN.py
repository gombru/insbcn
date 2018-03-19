# Retrieves nearest images given a text query and saves them in an given folder
import string
import numpy as np
import operator
import os
from shutil import copyfile
from gensim import corpora, models
import gensim

data = 'instaBarcelona_contrastive_ca_m015_iter_50000'
model_name = 'word2vec_model_instaBarcelona_ca.model'
num_topics = 300 # Embedding dimensionality
num_results = 20 # Num retrival results

# Topic distribution given by the CNN to test images. .txt file with format city/{im_id},score1,score2 ...
database_path = '../../../datasets/instaBarcelona/regression_output/' + data +'/test.txt'
model_path = '../../../datasets/instaBarcelona/models/word2vec/' + model_name

# Load text embedding model
print("Loading " + model_name + " model ...")
model = models.Word2Vec.load(model_path)


def load_regressions_from_txt(path, num_topics):
    database = {}
    file = open(path, "r")
    print("Loading data ...")
    print(path)
    for line in file:
        d = line.split(',')
        if len(d) < 301:
            print len(d)
            continue
        regression_values = np.zeros(num_topics)
        for t in range(0,num_topics):
            regression_values[t] = d[t + 1]
        database[d[0]] = regression_values
    return database

# Load dataset
database = load_regressions_from_txt(database_path, num_topics)

def word2vec(text, model, num_topics):
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
    for tok in tokens:
        word_embedding = model[tok]
        embedding += word_embedding

    embedding /= len(tokens)
    if min(embedding) < 0:
        embedding = embedding - min(embedding)
    if sum(embedding) > 0:
        embedding = embedding / np.linalg.norm(embedding)

    return embedding

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
        copyfile('../../../datasets/instaBarcelona/img_resized/' + id[0] + '.jpg' , results_path + id[0].replace('/', '_') + '.jpg')
        if idx == num_results - 1: break


# Define queries
q = ['ciutatvella','eixample','sants','santsmonjuic','monjuic','lescorts','sarria','gracia','horta','noubarris','santmarti','vallcarca','vilagracia','salut','vallvidrera','sarria','poblenou','besos','barceloneta','raval','gotic','santpere','born','elborn','gotico','gothic','poblesec','sagradafamilia']

for e,cur_q in enumerate(q):
    print(cur_q)
    results_path = "../../../datasets/instaBarcelona/retrieval_results/" + data + "/" + cur_q.replace(' ', '_') + '/'
    if not os.path.exists(results_path):
        print("Creating dir: " + results_path)
        os.makedirs(results_path)
    topics = word2vec(cur_q, model, num_topics)
    get_results(database, topics, num_results,results_path)







