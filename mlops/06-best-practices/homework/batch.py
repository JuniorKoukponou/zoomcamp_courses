#!/usr/bin/env python
# coding: utf-8

import io
import logging
import os
import pickle

import click
import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
OPTIONS = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}


def get_input_path(year, month):
    default_input_pattern = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"

    input_pattern = os.getenv("INPUT_FILE_PATTERN", default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = (
        "./output/year_{year:04d}/month_{month:02d}/predictions.parquet"
    )
    output_pattern = os.getenv("OUTPUT_FILE_PATTERN", default_output_pattern)
    return output_pattern.format(year=year, month=month)


def read_data(input_file):
    logging.info(f"Loading data from {input_file} ...")
    if "https" in input_file:
        content = requests.get(input_file).content
        df = pd.read_parquet(io.BytesIO(content))
        return df
    if S3_ENDPOINT_URL is not None:
        df = pd.read_parquet(input_file, storage_options=OPTIONS)
    else:
        df = pd.read_parquet(input_file)
    return df


def prepare_data(df, categorical):
    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def save_data(df, output_file):
    output_path = os.path.dirname(output_file)
    print("output_path", output_path)
    os.makedirs(output_path, exist_ok=True)
    # if S3_ENDPOINT_URL is not None:
    logging.info(f"Saving df to {output_file}")
    df.to_parquet(
        output_file,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=OPTIONS if S3_ENDPOINT_URL is not None else None,
    )


@click.command()
@click.option("--year", default=2023, help="Data year")
@click.option("--month", default=3, help="Data month.")
def main(year, month):
    # input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'

    with open("model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ["PULocationID", "DOLocationID"]

    input_file = get_input_path(year, month)
    df = read_data(input_file)

    df = prepare_data(df, categorical)
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    logging.info(f"predicted mean duration: {y_pred.mean()}")

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    output_file = get_output_path(year, month)
    save_data(df_result, output_file)


if __name__ == "__main__":
    main()
