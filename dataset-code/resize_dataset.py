# Resizes the images in a folder and creates a resized datasetcd in another
# It also filters  corrupted images

import glob
from PIL import Image
from joblib import Parallel, delayed
import os
from shutil import copyfile

images_path = "../../../hd/datasets/instaBarcelona/img/"
im_dest_path = "../../../hd/datasets/instaBarcelona/img_resized/"

minSize = 256

def resize(file):

    try:
        im = Image.open(file)\

        w = im.size[0]
        h = im.size[1]

        if w < h:
            new_width = minSize
            new_height = minSize * (h/w)

        if h <= w:
            new_height = minSize
            new_width = minSize * (w/h)

        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        im.save(im_dest_path + file.split('/')[-1])
    except:
        print "Failed copying image: "
        return



if not os.path.exists(im_dest_path):
    os.makedirs(im_dest_path)
Parallel(n_jobs=8)(delayed(resize)(file) for file in glob.glob(images_path + "/*.jpg"))
