import pandas as pd
import os
import file_merger


def timestamp_to_minute(file_path):
    data = pd.read_csv(file_path, sep=';')
    first_timestamp = data['Timestamp'].iloc[0]
    data['Timestamp'] = ((data['Timestamp'] - first_timestamp) / 60).round(4)
    data.to_csv(file_path, sep=';', index=False)


def ex_to_csv(file_path):
    excel_data = pd.read_excel(file_path)
    excel_data.to_csv(file_path.replace(".xlsx", ".csv"), sep=';', index=False)


def unix_to_minute(file_path):
    data = pd.read_csv(file_path, sep=';')
    data['Recording timestamp'] = (data['Recording timestamp'] / 1e6 / 60).round(4)
    data.rename(columns={'Recording timestamp': 'Timestamp'}, inplace=True)
    data.to_csv(file_path, sep=';', index=False)


def remove_comp_timestamp(file_path):
    data = pd.read_csv(file_path, sep=';')
    try:
        data.drop('Computer timestamp', axis=1, inplace=True)
        data.to_csv(file_path, sep=';', index=False)
    except:
        print("err")



"""
directory = "C:\\Users\\mussa\\Desktop\\Data with min - Kopi"
test_environments = ['Day', 'Night']

for x in os.listdir(directory):
    if not os.path.isdir(os.path.join(directory, x)):
        print(x + " is not a directory!")
        continue

    print("\n-------- Processing User: " + x + " --------")

    for y in os.listdir(os.path.join(directory, x)):
        if y in test_environments:
            has_files_1 = False
            has_files_2 = False
            print("\n" + " " * 4 + "Processing " + y + " Environment:")
            files_to_merge = []

            for z in os.listdir(os.path.join(directory, x, y)):
                current_file_path = os.path.join(directory, x, y, z)

                if "gaze" in z:
                    if ".csv" in z:
                        has_files_1 = True
                        files_to_merge.append(current_file_path)

                if "merged_data" in z:
                    has_files_2 = True
                    files_to_merge.append(current_file_path)

            if has_files_1 and has_files_2:
                output_file = os.path.join(directory, x, y, "merged_data.csv")
                file_merger.merge_files(files_to_merge, output_file)
"""