import sys

import batch

sys.path.insert(0, "..")
import pytest

YEAR = 2023
MONTH = 1


def test_predictions_sum():
    fake_data_predictions_path = batch.get_output_path(YEAR, MONTH)
    df = batch.read_data(fake_data_predictions_path)

    actual_predicitons_sum = df.predicted_duration.sum()

    expected_predictions_sum = 36.2772

    assert actual_predicitons_sum == pytest.approx(expected_predictions_sum, 1e-3)
