import os
import os.path
import sys
import configparser
import requests
import json
from google.protobuf import text_format
#import tensorflow as tf
from tag_pb2 import Data

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
    #print (text_format.MessageToString(data))
else:
    data = Data()
    if os.path.isfile("tags.pb"):
        with open("tags.pb", 'rb') as f:
            data.ParseFromString(f.read())
            f.close()

    found = 0
    for image in data.image:
        if image.url == sys.argv[1]:
            found = 1

    if found == 0:
        print ("Adding another one")
        image = data.image.add()
        image.url = sys.argv[1]
        prediction = model.predict_by_url(url=image.url)

        for tag in prediction['outputs'][0]['data']['concepts']:
            feature = image.feature.add()
            feature.label = tag['name']
            feature.confidence = tag['value']

        with open("tags.pb", 'wb') as f:
            serializedMessage = data.SerializeToString()
            f.write(serializedMessage)
            f.close()
