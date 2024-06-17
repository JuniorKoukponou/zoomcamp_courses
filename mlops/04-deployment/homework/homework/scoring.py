#!/usr/bin/python

import os
import sys
import click
import pickle
import logging

import numpy as np
import pandas as pd



year = 2023
month = 3
categorical = ['PULocationID', 'DOLocationID']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_data(year, month):
    filename = f'http://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    logger.info(f'reading yellow trip data from {filename}...')
    df = pd.read_parquet(filename, engine='pyarrow')
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    dicts = df[categorical].to_dict(orient='records')
    return dicts


def load_model(model_path='model.bin'):
    with open(model_path, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model


def save_results(df, y_pred, output_file, engine='pyarrow'):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result["prediction"] = y_pred

    df_result.to_parquet(output_file, engine=engine, compression=None, index=False)


def apply_model(year, month, model_path, output_file):
    df = read_data(year, month)
    dicts = prepare_dictionaries(df)

    logger.info(f'loading the model from model_path={model_path}...')
    dv, model = load_model(model_path)

    logger.info(f'applying the model...')
    X_pred = dv.transform(dicts)
    y_pred = model.predict(X_pred)

    logger.info(f'Prediction std {np.std(y_pred)} Prediction mean {np.mean(y_pred)}...')

    logger.info(f'saving the result to {output_file}...')

    save_results(df, y_pred, output_file)
    return output_file



@click.command()
@click.option('--year', default=2023, help='Data year')
@click.option('--month', default=3, help='Data month.')
def run(year, month):
    model_path = f'./model.bin'
    output_file = f'./output/yellow_tripdata_{year:04d}_{month:02d}_prediction.parquet'
    # s3://nyc-duration-prediction-val
    apply_model(year, month, model_path, output_file)

if __name__ == '__main__':
    run()