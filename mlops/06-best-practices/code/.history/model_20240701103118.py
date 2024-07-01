import os
import json
import boto3
import base64

import mlflow

def get_model_location(run_id):
    model_loation = os.getenv("MODEL_LOCATION", )
    model_bucket = os.getenv("MODEL_BUCKET", 'mlflow-models-alexey')
    experiment_id = os.getenv("EXPERIMENT_ID", "1")
    logged_model = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model'
    return logged_model

def load_model(run_id):
    model_location = get_model_location(run_id=run_id)
    model = mlflow.pyfunc.load_model(model_location)
    return model

def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    ride_event = json.loads(decoded_data)
    return ride_event

class ModelService:

    def __init__(self, model, model_version=None, callbacks=None) -> None:
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, ride):
        features = {}
        features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
        features['trip_distance'] = ride['trip_distance']
        return features


    def predict(self, features):
        pred = self.model.predict(features)
        return float(pred[0])


    def lambda_handler(self, event):
        # print(json.dumps(event))

        predictions_events = []

        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            ride_event = base64_decode(encoded_data)

            # print(ride_event)
            ride = ride_event['ride']
            ride_id = ride_event['ride_id']

            features = self.prepare_features(ride)
            prediction = self.predict(features)

            prediction_event = {
                'model': 'ride_duration_prediction_model',
                'version': self.model_version,
                'prediction': {
                    'ride_duration': prediction,
                    'ride_id': ride_id
                }
            }

            for callback in self.callbacks:
                callback(prediction_event)
            # if not TEST_RUN:
            #     kinesis_client.put_record(
            #         StreamName=PREDICTIONS_STREAM_NAME,
            #         Data=json.dumps(prediction_event),
            #         PartitionKey=str(ride_id)
            #     )

            predictions_events.append(prediction_event)

        return {
            'predictions': predictions_events
        }

class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name) -> None:
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        ride_id = prediction_event['prediction']['ride_id']
        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id)
            )

def init(prediction_stream_name: str, run_id: str, test_run: bool):
    model = load_model(run_id)

    callbacks = []
    if not test_run:
        kinesis_client = boto3.client('kinesis')
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)
    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)
    return model_service
