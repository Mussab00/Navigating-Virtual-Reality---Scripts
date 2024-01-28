import pandas as pd


def add_timestamps_to_e4(file_path):
    data = pd.read_csv(file_path, header=None)
    data_title = file_path.split('\\')[-1].strip('.csv')
    initial_timestamp = data.iloc[0, 0]
    sample_rate_hz = data.iloc[1, 0]
    spike_factor = 11
    positive_avg = 0
    negative_avg = 0

    new_data = ['Timestamp' + ';' + data_title]
    for index in range(2, len(data)):
        time_offset = (index - 2) / sample_rate_hz
        utc_timestamp = initial_timestamp + time_offset

        value = data.iloc[index, 0]

        if index > 200:
            if value < 0:
                negative_avg += value
                if value <= spike_factor * (negative_avg/index):
                    continue
            else:
                positive_avg += value
                if value >= spike_factor * (positive_avg/index):
                    continue

        row_data = str(utc_timestamp) + ";" + str(data.iloc[index, 0])
        new_data.append(row_data)

    new_df = pd.DataFrame(new_data)
    new_df.to_csv(file_path, index=False, header=False)
