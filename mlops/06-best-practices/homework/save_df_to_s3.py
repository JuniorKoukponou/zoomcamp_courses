from tests.test_batch import df

from batch import save_data, get_input_path

year = 2023
month = 1

output_file = get_input_path(year, month)
save_data(df, year, month, output_file)