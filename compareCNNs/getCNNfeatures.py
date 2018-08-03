import sys
import caffe
import numpy as np
from PIL import Image
import os

# Run in GPU
caffe.set_device(0)
caffe.set_mode_gpu()

#Model name
model = 'instaBarcelona_contrastive_distribution_randomNeg_ca_m04_iter_100000'
lan = 'ca'
#Output file
output_file_dir = '../../../datasets/instaBarcelona/ImageNetfeatures/' + lan
if not os.path.exists(output_file_dir):
    os.makedirs(output_file_dir)

net = caffe.Net('../../SocialMediaWeakLabeling/googlenet_regression/original_prototxt/deploy.prototxt', '../../../datasets/SocialMedia/models/pretrained/bvlc_googlenet.caffemodel', caffe.TEST)


neigh = ['ciutatvella','barceloneta','gotic','raval','born','eixample','santantoni','novaesquerra','antigaesquerra','dretaeixample','portpienc','sagradafamilia','santsmontjuic','sants','badal','labordeta','hostafrancs','fontdelaguatlla','marinadeport','poblesec','marinadelpratvermell','lescorts','maternitat','pedralbes','sarriasantgervasi','sarria','santgervasi','lestrestorres','elputxet','labonanova','vallvidrera','gracia','gracianova','viladegracia','lasalut','elcoll','vallcarca','hortaguinardo','baixguinardo','elguinardo','canbaro','lafontdenfargues','elcarmel','laclota','lateixonera','lavalldhebron','horta','montbau','santgenisdelsagudells','noubarris','villapicina','porta','elturodelapeira','canpeguera','prosperitat','verdum','trinitatnova','laguineueta','lesroquetes','torrebaro','canyelles','vallbona','ciutatmeridiana','santandreu','navas','lasagrera','bonpastor','elcongresielsindians','santandreudelpalomar','barodeviver','trinitatvella','santmarti','villaolimpica','poblenou','diagonalmar','elbesos','provenals','llacuna','elclot','santmartideprovenals','campdelarpa','lavernedailapau']

for cur_neigh in neigh:

    features = np.zeros(1024)

    test = os.listdir('../../../datasets/instaBarcelona/retrieval_results/' + model + '/' + cur_neigh)
    output_file_path = output_file_dir + '/' + cur_neigh + '.txt'

    size = 227
    # Reshape net
    batch_size = 300 #300
    net.blobs['data'].reshape(batch_size, 3, size, size)

    print 'Computing  ... ' + cur_neigh

    count = 0
    i = 0
    while i < len(test):
        indices = []

        # Fill batch
        for x in range(0, batch_size):

            if i > len(test) - 1: break

            # load image
            # filename = '../../../datasets/WebVision/test_images_256/' + test[i]
            filename = '../../../datasets/instaBarcelona/retrieval_results/' + model + '/' + cur_neigh + '/' + test[i].split(',')[0]
            im = Image.open(filename)
            im_o = im
            im = im.resize((size, size), Image.ANTIALIAS)
            indices.append(test[i])

            # Turn grayscale images to 3 channels
            if (im.size.__len__() == 2):
                im_gray = im
                im = Image.new("RGB", im_gray.size)
                im.paste(im_gray)

            #switch to BGR and substract mean
            in_ = np.array(im, dtype=np.float32)
            in_ = in_[:,:,::-1]
            in_ -= np.array((104, 117, 123))
            in_ = in_.transpose((2,0,1))

            net.blobs['data'].data[x,] = in_

            i += 1

        # run net and take scores
        net.forward()

        # Save results for each batch element
        for x in range(0,len(indices)):
            topic_probs = net.blobs['pool5/7x7_s1'].data[x][:,0,0]
            features += topic_probs

    features /= len(test)
    np.savetxt(output_file_path, features)

print "DONE"

