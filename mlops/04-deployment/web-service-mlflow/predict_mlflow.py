import pickle
from flask import Flask, request, jsonify
import mlflow


with open('./model/lin_reg.bin', 'rb') as file_input:
    (dv, model) = pickle.load(file_input)

def prepare_features(ride):
    features = dict()
    features["PU_DO"] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features["trip_distance"] = ride["trip_distance"]
    print(features)
    return features


def predict(features):
    X = dv.transform(features)
    prediction = model.predict(X)
    return prediction[0]

app = Flask("duration-prediction")

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """take web request and return the prediction"""
    ride = request.get_json()
    features = prepare_features(ride)
    preds = predict(features)
    result = {
        "duration": preds
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
