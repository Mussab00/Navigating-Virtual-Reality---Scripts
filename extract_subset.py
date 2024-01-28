import pandas as pd
import openpyxl
import numpy as np

def extract_data_between_timestamps(input_file, output_file, start_timestamp, end_timestamp):
    try:
        data = pd.read_csv(input_file, delimiter=';')
        timestamp_col = data.columns[0]
        data[timestamp_col] = pd.to_numeric(data[timestamp_col], errors='coerce')
        filtered_data = data[(data[timestamp_col] >= start_timestamp) & (data[timestamp_col] <= end_timestamp)]
        if filtered_data.empty and not data[data[timestamp_col] >= start_timestamp].empty:
            filtered_data = data[data[timestamp_col] >= start_timestamp]
        filtered_data.to_csv(output_file, index=False)

        return f"Data successfully extracted and saved to {output_file}"
    except Exception as e:
        return f"An error occurred: {e}"




def analyze_dataset(file_path):
    columns = ["Pupil diameter left", "Pupil diameter right", "BVP", "EDA", "HR", "TEMP", "FPS", "TicksDiff"]
    try:
        dataset = pd.read_csv(file_path)
        available_columns = [col for col in columns if col in dataset.columns]
        missing_columns = set(columns) - set(available_columns)
        if missing_columns:
            print(
                f"Warning: The following columns were not found in the dataset and will be skipped: {missing_columns}")

        filtered_dataset = dataset[available_columns]
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        descriptive_stats = filtered_dataset.describe(include='all')

        return descriptive_stats

    except Exception as e:
        return f"An error occurred: {e}"


def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)

    return roll_x, pitch_y, yaw_z



workbook = openpyxl.load_workbook('snippets.xlsx')
sheet = workbook['Ark1']
directory = "C:\\Users\\mussa\\Desktop\\Data Snippets - Kopi"

for row in sheet.iter_rows(min_row=2, values_only=True):
    userId = row[1]
    environment = row[2]
    start = row[3]
    end = row[4]
    status = row[5]

    #input_file = directory + "\\" + str(userId) + "\\" + environment + "\\" + "merged_data.csv"
    file_path = directory + "\\" + str(userId) + "\\" + environment + "\\" + status + "_snippet.csv"
    # data = pd.read_csv(file_path)
    #
    # data.dropna(subset=data.columns.difference(['timestamp']), how='all')
    # data.to_csv(file_path, index=False)
    #stats = analyze_dataset(file)
    #print(stats)

    df = pd.read_csv(file_path)
    df_cleaned = df.dropna(subset=df.columns.difference(['timestamp']), how='all')
    df_cleaned.to_csv(file_path, index=False)


    print("finished processing " + str(userId) + ", " + environment + ", " + status)

workbook.close()
