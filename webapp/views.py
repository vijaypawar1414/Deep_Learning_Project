from django.shortcuts import render
import pandas as pd
import numpy as np
from .models import eye
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Create your views here.
homepage = 'index.html'
resultpage = 'result.html'
img_height, img_width = 224, 224

eyes = ['Based on the model\'s prediction, the patient is likely suffering from cardiovascular disease. A consultation with a specialist is strongly recommended for further evaluation.', 'The model predicts a very low likelihood of cardiovascular disease, and a specialist consultation is not necessary.']


def home(request):
    return render(request, homepage)

def second_page(request):
    return render(request, 'second_page.html')

def third_page(request):
    return render(request, 'third_page.html')


def result(request):
    if request.method == 'POST':
        m = int(request.POST['alg'])
        file = request.FILES['file']
        fn = eye(images=file)
        fn.save()
        path = os.path.join('webapp/static/image/', fn.filename())
        # acc = pd.read_csv("webapp\Acc.csv")

        if m == 1:
            new_model = load_model(r"webapp\models\CNN.h5", compile=False)
            test_image = image.load_img(
                path, target_size=(img_height, img_width))
            test_image = image.img_to_array(test_image)
            test_image /= 255
            # a = acc.iloc[m - 1, 1]

        elif m == 2:
            new_model = load_model(
                r"webapp\models\MobileNet.h5", compile=False)
            test_image = image.load_img(
                path, target_size=(img_height, img_width))
            test_image = image.img_to_array(test_image)
            test_image /= 255
            # a = acc.iloc[m-1, 1]
        elif m == 3:
            new_model = load_model(
                r"webapp\models\GoogleNet.h5", compile=False)
            test_image = image.load_img(
                path, target_size=(img_height, img_width))
            test_image = image.img_to_array(test_image)
            test_image /= 255
            # a = acc.iloc[m-1, 1]

        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        print(result)
        print(result[0][0])
        prediction_vaue = result[0][0] * 100
        prediction_vaue = prediction_vaue.round(2)
        print(prediction_vaue)
        if result[0][0] >= 0.5:
            pred = eyes[0]
        else:
            pred = eyes[1]
        print(pred)

        return render(request, resultpage, {'text': pred, 'prediction_vaue' : prediction_vaue ,  'path': 'static/image/'+fn.filename()})
    return render(request, resultpage)
