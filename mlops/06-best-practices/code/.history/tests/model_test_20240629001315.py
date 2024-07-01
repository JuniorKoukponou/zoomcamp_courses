import model

def test_prepare_features():
    model_service model.ModelService(None)
    ride = 1 {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66,
    }

    actual_features = model_service. prepare_features(ride)

    expected_fetures = 1 {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }

    assert actual_features == expected_fetures
