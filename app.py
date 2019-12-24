from flask import Flask, render_template, request, flash,jsonify,redirect,url_for



import numpy as np 
import pandas as pd 
from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import random
import os

from keras.models import load_model
from keras import backend as K




import re


from image_upload import Images


FAST_RUN = False
IMAGE_WIDTH=224
IMAGE_HEIGHT=224
IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS=3 # RGB color
batch_size=2



app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')



@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        recomend = Images()
        data = recomend.Upload()
        data  = re.findall('([^\/]+$)',data)
        img_str = data[0]
        img_str =  img_str.replace(" ", "") 
        print("image name : ",data[0].replace(" ", ""))



        soil_data = pd.read_csv('soil1.csv')
        res = soil_data[soil_data['ImageId'] == data[0].replace(" ", "")]
        if res.empty:
            Nitrogen = random.randint(210,278)
            Phorphorus = random.randint(11,28)
            Potassium = random.randint(110,276)
            ph = random.uniform(6.10,7.99)
            ph = "{:1.2f}".format(ph)
        else:  
            for index, row in res.iterrows(): 
                ph = row["pH"]
                Nitrogen = row["Nitrogen"]
                Phorphorus = row['Phorphorus'] 
                Potassium = row['Potassium']
                print (row["pH"], row["Nitrogen"],row['Phorphorus'],row['Potassium'])
        
            

        test_df = pd.DataFrame({'filename': data})


        model = load_model('model.h5')
        image = recomend.load('static/images/'+data[0])
        predict =  model.predict(image)
        # predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples/batch_size))
        print(predict)
        threshold = 0.5
        test_df['probability'] = predict
        test_df['category'] = np.where(test_df['probability'] > threshold, 1,0)
        count = 0
        file_name = []
        category = []
        probability = []
        for index, row in test_df.iterrows():
            print(row['filename'])
            file_name.append(row['filename'])
            print(row['category'])
            if row['category'] == 0:
                category.append('Black')
            else:
                category.append('Red')

            
            print(row['probability'])
            probability.append("{:07.6f}".format(row['probability']))
            count = count + 1
        print("Working : ",count)
        K.clear_session()
        return render_template('predict.html',ph=ph,Nitrogen=Nitrogen,Phorphorus=Phorphorus,Potassium=Potassium,file_name=data[0],category=category,probability=probability,no_pred=count,files=file_name)



if __name__ == "__main__":
    
    app.run(debug=True)