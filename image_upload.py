import os
from flask import request
import io
import base64
import numpy as np
import re


from PIL import Image
import numpy as np
from skimage import transform


class Images(object):

    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        

    def Upload(self):
        target = os.path.join(self.APP_ROOT, 'static/images')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
        
        print(request.files.getlist("file"))

        for file in request.files.getlist("file"):
            print('come here')
            print(file)
            filename = file.filename
            print(filename)
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

        return destination

    def load(self,filename):
        np_image = Image.open(filename)
        np_image = np.array(np_image).astype('float32')/255
        np_image = transform.resize(np_image, (224, 224, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image