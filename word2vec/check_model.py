from gensim import models

model_name = 'word2vec_model_instaBarcelona.model'
model_path = '../../../hd/datasets/instaBarcelona/models/word2vec/' + model_name

print "Loading model ... "
model = models.Word2Vec.load(model_path)

print "Checking model"

print model.wv.most_similar(positive=['woman', 'king'], negative=['man'])

print model.wv.most_similar(positive=['beach', 'sea'], negative=['mountain'])

print model.wv.doesnt_match("breakfast cereal dinner lunch".split())

print model.wv.doesnt_match("man woman kid dog".split())

print model.wv.similarity('woman', 'man')

print 'DONE'

words = ['food','shopping','fun','holidays','tourism','morning','breakfast','lunch','dinner','night']

for w in words:
    print "Most similar words for :" + w
    print model.wv.most_similar(positive=[w])

print "DONE"