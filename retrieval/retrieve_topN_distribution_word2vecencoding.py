# Retrieves nearest images given a text query and saves them in an given folder
import string
import numpy as np
import operator
import os
from shutil import copyfile
from gensim import corpora, models
import gensim

data = 'instaBarcelona_contrastive_distribution_randomNeg_en_m04_iter_100000'
model_name = 'word2vec_model_instaBarcelona_en.model'
num_topics = 82 # Embedding dimensionality
num_results = 20 # Num retrival results

# Topic distribution given by the CNN to test images. .txt file with format city/{im_id},score1,score2 ...
database_path = '../../../ssd2/instaBarcelona/regression_output/' + data +'/test.txt'
model_path = '../../../ssd2/instaBarcelona/models/word2vec/' + model_name

# Load text embedding model
print("Loading " + model_name + " model ...")
model = models.Word2Vec.load(model_path)

neighbourhoods = ['ciutatvella','barceloneta','gotic','raval','born','eixample','santantoni','novaesquerra','antigaesquerra','dretaeixample','portpienc','sagradafamilia','santsmontjuic','sants','badal','labordeta','hostafrancs','fontdelaguatlla','marinadeport','poblesec','marinadelpratvermell','lescorts','maternitat','pedralbes','sarriasantgervasi','sarria','santgervasi','lestrestorres','elputxet','labonanova','vallvidrera','gracia','gracianova','viladegracia','lasalut','elcoll','vallcarca','hortaguinardo','baixguinardo','elguinardo','canbaro','lafontdenfargues','elcarmel','laclota','lateixonera','lavalldhebron','horta','montbau','santgenisdelsagudells','noubarris','villapicina','porta','elturodelapeira','canpeguera','prosperitat','verdum','trinitatnova','laguineueta','lesroquetes','torrebaro','canyelles','vallbona','ciutatmeridiana','santandreu','navas','lasagrera','bonpastor','elcongresielsindians','santandreudelpalomar','barodeviver','trinitatvella','santmarti','villaolimpica','poblenou','diagonalmar','elbesos','provenals','llacuna','elclot','santmartideprovenals','campdelarpa','lavernedailapau']

def load_regressions_from_txt(path, num_topics):
    database = {}
    file = open(path, "r")
    print("Loading data ...")
    print(path)
    for line in file:
        d = line.split(',')
        if len(d) < num_topics -1:
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
    embedding = np.zeros(len(neighbourhoods))
    c = 0
    for tok in tokens:
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
        copyfile('../../../ssd2/instaBarcelona/img_resized/' + id[0] + '.jpg' , results_path + id[0].replace('/', '_') + '.jpg')
        if idx == num_results - 1: break


# Define queries
q = ['ciutatvella','barceloneta','gotic','raval','born','eixample','santantoni','novaesquerra','antigaesquerra','dretaeixample','portpienc','sagradafamilia','santsmontjuic','sants','badal','labordeta','hostafrancs','fontdelaguatlla','marinadeport','poblesec','marinadelpratvermell','lescorts','maternitat','pedralbes','sarriasantgervasi','sarria','santgervasi','lestrestorres','elputxet','labonanova','vallvidrera','gracia','gracianova','viladegracia','lasalut','elcoll','vallcarca','hortaguinardo','baixguinardo','elguinardo','canbaro','lafontdenfargues','elcarmel','laclota','lateixonera','lavalldhebron','horta','montbau','santgenisdelsagudells','noubarris','villapicina','porta','elturodelapeira','canpeguera','prosperitat','verdum','trinitatnova','laguineueta','lesroquetes','torrebaro','canyelles','vallbona','ciutatmeridiana','santandreu','navas','lasagrera','bonpastor','elcongresielsindians','santandreudelpalomar','barodeviver','trinitatvella','santmarti','villaolimpica','poblenou','diagonalmar','elbesos','provenals','llacuna','elclot','santmartideprovenals','campdelarpa','lavernedailapau']

for e,cur_q in enumerate(q):
    print(cur_q)
    results_path = "../../../ssd2/instaBarcelona/retrieval_results/" + data + "/" + cur_q.replace(' ', '_') + '_word2vec/'
    if not os.path.exists(results_path):
        print("Creating dir: " + results_path)
        os.makedirs(results_path)
    topics = word2vec(cur_q, model, num_topics)
    get_results(database, topics, num_results,results_path)







