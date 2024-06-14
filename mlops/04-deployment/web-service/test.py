import predict_flask as predict

ride = {
    "PULocationID": 8 * 5,
    "DOLocationID": 50,
    "trip_distance": 10
}

features = predict.prepare_features(ride)
pred = predict.predict(features)
print(pred)
