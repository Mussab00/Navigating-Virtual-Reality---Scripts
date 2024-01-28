import csv
import time
from collections import defaultdict


def convert_to_unix_utc(timestamp_str):
    time_struct = time.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S')
    return int(time.mktime(time_struct))


def process_log_file(file_path):
    fps_data = defaultdict(list)

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            timestamp, fps = parts[0], float(parts[1].split(' ')[-1].replace(',', '.'))
            unix_timestamp = convert_to_unix_utc(timestamp)
            fps_data[unix_timestamp].append(fps)

    averaged_fps_data = {timestamp: sum(fps_list) / len(fps_list) for timestamp, fps_list in fps_data.items()}

    with open(file_path.replace('.txt', '.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Timestamp', 'FPS'])  # Header row
        for timestamp, avg_fps in averaged_fps_data.items():
            writer.writerow([timestamp, round(avg_fps)])
