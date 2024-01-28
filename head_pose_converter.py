import csv
from datetime import datetime


def convert_headpose(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=';')

        previous_time = None
        csv_writer.writerow(["Timestamp", "RotationX", "RotationY", "RotationZ", "RotationW"])

        for line in infile:
            parts = line.split(': ')

            timestamp_str = parts[0]
            rotation_str = parts[3].strip('), Forward')
            timestamp = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').timestamp()

            if previous_time is not None and previous_time == timestamp:
                continue
            else:
                previous_time = timestamp

            rotation_values = rotation_str.strip('Rotation: ()\n').split(', ')
            csv_writer.writerow([int(timestamp), *rotation_values])
