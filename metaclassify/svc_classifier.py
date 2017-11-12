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
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
sess.run(hello)
if 1:
    sys.exit(0)

from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from skflow import TensorFlowLinearClassifier

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
                    n = len(image_features)
                    if i <= n:
                        image_features.insert(i, feature.confidence)
                    else:
                        for j in range(n+1, i):
                            image_features.append(0)
                        image_features.insert(i, feature.confidence)
            if not found:
                features.append(feature.label)
                image_features.insert(l, feature.confidence)
        X.append(image_features)
        if 'generic' in image.tags.split(' '):
            y.append(0)
        else:
            y.append(1)

if sys.argv[2].endswith('pb'):
    data = Data()
    with open(sys.argv[2], 'rb') as f:
        data.ParseFromString(f.read())
        f.close()
    Z = []
    for image in data.image:
        image_features = []
        for feature in image.feature:
            found = 0
            l = len(features)
            for i in range(1, l):
                if features[i] == feature.label:
                    found = 1
                    n = len(image_features)
                    if i <= n:
                        image_features.insert(i, feature.confidence)
                    else:
                        for j in range(n+1, i):
                            image_features.append(0)
                        image_features.insert(i, feature.confidence)
            if not found:
                features.append(feature.label)
                image_features.insert(l, feature.confidence)
        Z.append(image_features)
# padding zeros to make X and Z uniform
max_l = 0
for x in X:
    if max_l < len(x):
        max_l = len(x)
for z in Z:
    if max_l < len(z):
        max_l = len(z)
if 0: 
    print(max_l)
for j in range(0, len(X)):
    x = X[j]
    for i in range(0, max_l - len(x)):
        x.append(0)
    X[j] = x
for j in range(0, len(Z)):
    z = Z[j]
    for i in range(0, max_l - len(z)):
        z.append(0)
    Z[j] = z
if 0:
    for x in X:
        print(len(x))
    sys.exit(0)
    for z in Z:
        print(len(z))
    sys.exit(0)
if 0:
    print(X[0])
    print(X[len(X)-1])
    print(Z[0])
    print(Z[len(Z)-1])
if 0:
    print(y)
training_X = []
training_y = []
testing_X = []
testing_y = []
N = int(len(X) * 2 / 3)
#N = int(len(X) * 4 / 5)
for i in range(0, N):
    training_X.append(X[i])
    training_y.append(y[i])
for i in range(N, len(X)):
    testing_X.append(X[i])
    testing_y.append(y[i])
for clf in [
     LogisticRegression(),  
     KNeighborsClassifier(),
     SVC(kernel='linear'), 
     SVC(), 
     GaussianNB(), 
     BernoulliNB(), 
     MultinomialNB(), 
     MultinomialNB(),
     Perceptron(max_iter=5, tol=None), 
     SGDClassifier(max_iter=5, tol=None),
     PassiveAggressiveClassifier(max_iter=5, tol=None),
     MLPClassifier(max_iter=10000),
#     MLPClassifier(solver='sgd', hidden_layer_sizes = (400,100), max_iter=10000),
#     MLPClassifier(solver='sgd', hidden_layer_sizes = (400), max_iter=10000, learning_rate_init=0.1),
#     MLPClassifier(solver='sgd', hidden_layer_sizes = (400), max_iter=10000, learning_rate_init=0.5),
#     MLPClassifier(solver='sgd', hidden_layer_sizes = (400), max_iter=10000),
#     MLPClassifier(solver='sgd', hidden_layer_sizes = (400), max_iter=1000),
#     MLPClassifier(solver='adam', hidden_layer_sizes = (400), max_iter=1000),
     KNeighborsClassifier(),
     KNeighborsClassifier(n_neighbors=1),
     KNeighborsClassifier(n_neighbors=2),
     KNeighborsClassifier(n_neighbors=3),
     KNeighborsClassifier(n_neighbors=4),
     KNeighborsClassifier(n_neighbors=5),
     TensorFlowLinearClassifier(n_classes=3)
]: 
    # clf.fit(training_X, training_y)  
    # predicted_testing_y = clf.predict(testing_X)
    # c = 0
    # correct = 0
    # interesting = 0
    # for i in range(0, len(testing_X)):
    #     if testing_y[i] == 1:
    #         interesting = interesting + 1
    #     if predicted_testing_y[i] == testing_y[i]:
    #         correct = correct + 1
    #     c = c + 1
    # print(correct * 100 / c)
    clf.fit(training_X, training_y)  
    score = metrics.accuracy_score(testing_y, clf.predict(testing_X))
    print("Accuracy: %f" % score)
