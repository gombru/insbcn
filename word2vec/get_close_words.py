from gensim import models

lans = ['en','es','ca']
model_name = 'word2vec_model_instaBarcelona_lan.model'
model_path = '../../../datasets/instaBarcelona/models/word2vec/' + model_name

models_list = []
print "Loading models ... "
for l in lans:
    models_list.append(models.Word2Vec.load(model_path.replace('lan',l)))

# districts = ['surf','ciutatvella', 'eixample', 'santsmontjuic', 'lescorts', 'sarria', 'gracia', 'hortaguinardo', 'noubarris', 'santandreu', 'santmarti']
# districts += ['poblenou','poblesec','sagradafamilia','barceloneta','gothic','vallcarca','gotic','gotico','viladegracia','viladegracia','vallvidrera','diagonalmar','raval','born','borne']
# districts = ['elborn','santmarti','poblesec','barceloneta','gothic','vallcarca','gotic','gotico','born','raval','sants','poblenou','vallcarca','viladegracia','gracia','sagradafamilia','vallvidrera']
districts = ['poblesec','poblenou','born']

print "Checking models"

for d in districts:
    print '\n' + d
    for m in models_list:
        try:
            topw = m.wv.most_similar(positive=[d], topn=30)
        except:
            topw = [('Not in voc','')]
        toprint = ''
        for w in topw:
            toprint += str(w[0]) + ' '
        print toprint

print "DONE"