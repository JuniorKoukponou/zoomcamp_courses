import pandas as pd
import batch
from datetime import datetime
from deepdiff import DeepDiff


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    actual_prepared_data = batch.prepare_data(df=df, categorical=columns)
    print("actual_prepared_data", actual_prepared_data)
    expected_prepared_data = pd.DataFrame(
        [
            (-1, -1, dt(1, 1), dt(1, 10), 9),
            (1, 1, dt(1, 2), dt(1, 10), 8)  
        ],
        columns=columns + ["duration"])

    diff = DeepDiff(actual_prepared_data, expected_prepared_data, significant_digits=1)
    print(f'diff={diff}')

    assert 'values_changed' not in diff
    assert 'type_changes' not in diff