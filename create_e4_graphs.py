import os
import data_visualizer

directory = "C:\\Users\\mussa\\Desktop\\MussabLucasData - complete - Kopi"
test_environments = ['Day', 'Night']

for x in os.listdir(directory):
    if not os.path.isdir(os.path.join(directory, x)):
        print(x + " is not a directory!")
        continue

    print("\n-------- Processing User: " + x + " --------")

    for y in os.listdir(os.path.join(directory, x)):
        if y in test_environments:
            has_files = False
            print("\n" + " " * 4 + "Processing " + y + " Environment:")
            files_to_merge = []
            comfort_path = None

            for z in os.listdir(os.path.join(directory, x, y)):
                current_file_path = os.path.join(directory, x, y, z)

                if "merged_data" in z:
                    data_visualizer.create_e4_plots(current_file_path, os.path.join(directory, x, y))