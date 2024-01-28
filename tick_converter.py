import csv
from datetime import datetime

def process_tick_log(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            timestamp = parts[0]
            left_tick = int(parts[1].split('=')[1].split('Right')[0].strip(' '))
            right_tick = int(parts[1].split('=')[2].strip(' '))

            if timestamp not in data:
                data[timestamp] = {'left_sum': 0, 'right_sum': 0, 'count': 0}

            data[timestamp]['left_sum'] += left_tick
            data[timestamp]['right_sum'] += right_tick
            data[timestamp]['count'] += 1

    processed_data = []
    for timestamp, values in data.items():
        unix_timestamp = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S').timestamp()
        avg_left = round(values['left_sum'] / values['count'])
        avg_right = round(values['right_sum'] / values['count'])
        ticks_diff = 0

        if (avg_left < 0 < avg_right) or (avg_left > 0 > avg_right):
            ticks_diff = abs(avg_left - avg_right)

        processed_data.append([unix_timestamp, avg_left, avg_right, ticks_diff])

    return processed_data


def convert_tick_log(file_path, output_file_path):
    processed_data = process_tick_log(file_path)

    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Timestamp', 'LeftTick', 'RightTick', 'TicksDiff'])
        writer.writerows(processed_data)