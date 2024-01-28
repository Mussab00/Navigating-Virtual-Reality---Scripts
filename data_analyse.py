import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import numpy as np

def get_all_files():
    lists = [['213456','Night','Healthy'],['213456','Night','Sick'],['362745','Day','Healthy'],['362745','Day','Sick'],['453627','Night','Healthy'],['453627','Night','Sick'],['456213','Day','Healthy'],['456213','Day','Sick'],['547236','Night','Healthy'],['547236','Night','Sick'],['843921','Night','Healthy'],['843921','Night','Sick'],['992934','Day','Healthy'],['992934','Day','Sick']]



    workbook = openpyxl.load_workbook('snippets.xlsx')
    sheet = workbook['Ark1']
    directory = "C:\\Users\\MussabAbdul-RazzakKa\\Desktop\\Data Snippets - Kopi"
    sicks = []
    healthys = []

    #for row in lists:
    for row in sheet.iter_rows(min_row=2, values_only=True):
        #user_id = row[0]
        #environment = row[1]
        #status = row[2]

        user_id = row[1]
        environment = row[2]
        status = row[5]

        file_path = directory + "\\" + str(user_id) + "\\" + environment + "\\" + status + "_snippet.csv"

        if status == "Sick":
            sicks.append(file_path)

        if status == "Healthy":
            healthys.append(file_path)

        print("finished processing " + str(user_id) + ", " + environment + ", " + status)

    workbook.close()

    return sicks, healthys



def analyze_dataset_excluding_columns(file_path, columns_to_exclude):
    try:
        dataset = pd.read_csv(file_path)
        filtered_dataset = dataset.drop(columns=columns_to_exclude, errors='ignore')

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        descriptive_stats = filtered_dataset.describe(include='all')

        return descriptive_stats

    except Exception as e:
        return f"An error occurred: {e}"

def save_stats_to_file(stats, save_path):
    try:
        stats.to_csv(save_path)
        print(f"Descriptive statistics saved to {save_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def visualize_snippets(paths, value_to_visualize):
    plt.figure(figsize=(12, 6))

    # Loop through each dataset
    for file_path in paths:
        data = pd.read_csv(file_path)

        if value_to_visualize in data.columns:
            data_filtered = data[value_to_visualize].dropna()  # Remove missing values
            num_points = len(data_filtered)
            time_axis = np.linspace(0, 2, num_points)
            plt.plot(time_axis, data_filtered)
        else:
            print(f"'HR' column not found in {file_path}")

    plt.xlabel('Time (minutes)')
    plt.ylabel('Heart Rate (HR)')
    plt.title('Heart Rate Over Artificial 2-minute Period from Multiple Datasets')
    plt.grid(True)
    plt.xlim(0, 2)
    plt.legend()
    plt.show()



sicks, healthys = get_all_files()
visualize_snippets(sicks, 'EDA')
#columns_to_exclude = ["Timestamp"]

# Analyze the dataset excluding specified columns
#stats = analyze_dataset_excluding_columns(sicks[3], columns_to_exclude)

#print(stats)

#save_stats_to_file(stats, "save_path.csv")
