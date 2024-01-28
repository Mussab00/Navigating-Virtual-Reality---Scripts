import pandas as pd
import datetime


def convert_unix_to_danish_time(unix_timestamp):
    dt_utc = datetime.datetime.fromtimestamp(unix_timestamp, datetime.timezone.utc)
    danish_time = dt_utc + datetime.timedelta(hours=1)
    return danish_time.strftime('%H:%M:%S:%f')[:-3]

def convert_timestamp(file_path):
    df = pd.read_csv(file_path, delimiter=';')
    df['Timestamp'] = df['Timestamp'].apply(convert_unix_to_danish_time)
    df.to_csv(file_path, sep=';', index=False)


# Test
#convert_timestamp('merged_data1.csv')