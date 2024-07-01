# from lambda_function import prepare_features


def test_prepare_features():
    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66,
    }

    actual_features = 1 # prepare_features(ride)

    # expected_fetures = 1  # {
    #     "PU_DO": "130_205",
    #     "trip_distance": 3.66,
    # }

    assert actual_features == expected_fetures