from sklearn import svm
import os
import os.path
import sys
import json
from google.protobuf import text_format
from tag_pb2 import Data
import numpy as np
import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('secrets/keys.ini')

from clarifai import rest
from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key=config['clarifai']['api_key'])
model = app.models.get("general-v1.3")

         
if sys.argv[1].endswith('.pb'):
    data = Data()
    with open(sys.argv[1], 'rb') as f:
        data.ParseFromString(f.read())
        f.close()
    tags = {}
    count = 0
    images = []
    X = []
    y = []
    features = []
    for image in data.image:
        count = count + 1
        images.append(image.url)
        image_features = []
        for tag in image.tags.split(' '):
            if '?' in tag:
                continue
            if tag in tags:
                tags[tag] = tags[tag] + 1
            else:
                tags[tag] = 1
        for feature in image.feature:
            found = 0
            l = len(features)
            for i in range(1, l):
                if features[i] == feature.label:
                    found = 1
                    image_features.insert(i, feature.confidence)
            if not found:
                features.append(feature.label)
                image_features.insert(l, feature.confidence)
        X.append(image_features)
        if 'generic' in image.tags.split(' '):
            y.append(0)
        else:
            y.append(1)
    clf = svm.SVC()
    clf.fit(X, y)  
    svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    prediction = model.predict_by_url(url=sys.argv[2])
    image_features = []
    for tag in prediction['outputs'][0]['data']['concepts']:
       label = tag['name']
       confidence = tag['value']
       found = 0
       l = len(features)
       for i in range(1, l):
            if features[i] == feature.label:
               found = 1
               image_features.insert(i, feature.confidence)
       if not found:
           features.append(feature.label)
           image_features.insert(l, feature.confidence)
    print(image_features)
    print(clf.predict([image_features]))
