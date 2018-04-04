from gensim import models

model_name = 'word2vec_model_instaBarcelona.model'
model_path = '../../../datasets/instaBarcelona/models/word2vec/' + model_name

print "Loading model ... "
model = models.Word2Vec.load(model_path)

print "Checking model"

print model.wv.most_similar(positive=['woman', 'king'], negative=['man'])
# print model.wv.most_similar(positive=['beach', 'sea'], negative=['mountain'])
print model.wv.doesnt_match("breakfast cereal dinner lunch".split())
print model.wv.doesnt_match("man woman kid dog".split())
print model.wv.similarity('woman', 'man')

print 'DONE'

# words = ['restaurant','beer','food','shopping','fun','holidays','tourism','morning','breakfast','lunch','dinner','night','hotel','hostel','nightlife','sleep','club','night','nightclub','drink']

words = ['flaxkale','cangambus','thegreenspot','gruponomo','elpalace','mobarcelona','ghotelcentral','peretarres','hostelone','hostelfun','yeahhostel','suttonclub','sutton','pachabcn','razz','razzmatazz','apolo']

for w in words:
    out = ""
    print "Most similar words for: " + w
    results = model.wv.most_similar(positive=[w], topn=20)
    for r in results: out = out + " " + str(r[0])
    print out

w = ['club','night']
print "Most similar words for: " + w[0] + ' + ' + w[1]
results = model.wv.most_similar(positive=w, topn=20)
out = ""
for r in results: out = out + " " + str(r[0])
print out

w = ['healthy','restaurant']
print "Most similar words for: " + w[0] + ' + ' + w[1]
results = model.wv.most_similar(positive=w, topn=20)
out = ""
for r in results: out = out + " " + str(r[0])
print out

w = ['sushi','restaurant']
print "Most similar words for: " + w[0] + ' + ' + w[1]
results = model.wv.most_similar(positive=w, topn=20)
out = ""
for r in results: out = out + " " + str(r[0])
print out

print "DONE"