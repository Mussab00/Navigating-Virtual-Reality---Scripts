import pandas as pd


def merge_multiple_csv(files, output_file, timestamp_column):
    merged_data = pd.DataFrame()

    for file in files:
        data = pd.read_csv(file, delimiter=';')
        data[timestamp_column] = data[timestamp_column].astype(float)

        if merged_data.empty:
            merged_data = data
        else:
            merged_data = pd.merge(merged_data, data, on=timestamp_column, how='outer')

    merged_data.sort_values(by=timestamp_column, inplace=True)
    merged_data.to_csv(output_file, sep=';', index=False)


def merge_files(file_paths, output_file):
    timestamp_column = 'Timestamp'
    merge_multiple_csv(file_paths, output_file, timestamp_column)
