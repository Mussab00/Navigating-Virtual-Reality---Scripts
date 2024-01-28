import os
import e4_converter
import file_merger
import fps_converter
import tick_converter
import sickness_level_converter
import head_pose_converter
import gaze_plots

directory = "C:\\Users\\mussa\\Desktop\\MussabLucasData - with eye data - Kopi"
test_environments = ['Day', 'Night']
e4_files = ['BVP.csv', 'EDA.csv', 'HR.csv', 'TEMP.csv']

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

                if "Comfort Levels" in z:
                    comfort_path = current_file_path

                if "FPSLog" in z:
                    has_files = True
                    print(" " * 8 + "Processing FPS Log")
                    date = sickness_level_converter.extract_date(z)
                    fps_converter.process_log_file(current_file_path)
                    files_to_merge.append(current_file_path.replace('.txt', '.csv'))
                    os.remove(current_file_path)

                    print(" " * 8 + "Processing Comfort Level Log")
                    sickness_level_converter.convert_sickness_level(date, comfort_path)
                    files_to_merge.append(comfort_path.replace('.xlsx', '.csv'))

                if "tickLog" in z:
                    has_files = True
                    print(" " * 8 + "Processing Ticks Log")
                    tick_converter.convert_tick_log(current_file_path, current_file_path.replace('.txt', '.csv'))
                    files_to_merge.append(current_file_path.replace('.txt', '.csv'))
                    os.remove(current_file_path)

                if "poseLog" in z:
                    has_files = True
                    print(" " * 8 + "Processing Headpose Log")
                    head_pose_converter.convert_headpose(current_file_path, current_file_path.replace('.txt', '.csv'))
                    files_to_merge.append(current_file_path.replace('.txt', '.csv'))
                    os.remove(current_file_path)

                if "gaze" in z:
                    has_files = True
                    print(" " * 8 + "Processing Gaze Plots")
                    gaze_plots.create_gaze_plots(current_file_path, os.path.join(directory, x, y))

                if 'E4' in z:
                    has_files = True
                    print(" " * 8 + "Processing E4 Data:")
                    for e4_file in os.listdir(current_file_path):
                        if e4_file.endswith(".csv") and e4_file in e4_files:
                            print(" " * 10 + "- " + e4_file)
                            filepath = os.path.join(directory, x, y, z, e4_file)
                            e4_converter.add_timestamps_to_e4(filepath)
                            files_to_merge.append(filepath)

            if len(files_to_merge) > 0:
                output_file = os.path.join(directory, x, y, "merged_data.csv")
                file_merger.merge_files(files_to_merge, output_file)
                #print(" " * 8 + "Processing Timestamp Conversion")
                #timestamp_converter.convert_timestamp(output_file)

            if not has_files:
                empty_folder_path = os.path.join(directory, x, y)
                print(" " * 4 + "Removing " + y + " Environment folder because it's empty.")
                os.rmdir(empty_folder_path)