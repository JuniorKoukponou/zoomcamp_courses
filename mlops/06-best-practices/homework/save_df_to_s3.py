from batch import get_input_path, save_data
from tests.test_batch import df

YEAR = 2023
MONTH = 1

output_file = get_input_path(YEAR, MONTH)
save_data(df, output_file)
