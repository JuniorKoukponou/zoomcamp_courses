import pickle
from flask import Flask, request, jsonify


with open('./model/lin_reg.bin', 'rb') as file_input:
    (dv, model) = pickle.load(file_input)

def prepare_features(ride):
    features = dict()
    features["PU_DO"] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features["trip_distance"] = features["trip_distance"]
    print(features)
    return features


def predict(features):
    X = dv.transform(features)
    prediction = model.predict(X)
    return prediction[0]


def predict_endpoint():
