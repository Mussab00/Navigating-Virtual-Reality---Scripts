import os

import openpyxl
import csv
import time
from collections import defaultdict


def extract_date(text):
    date_part = text.split('_')[1]
    parts = date_part.split('-')
    return parts[2] + '-' + parts[1] + '-' + parts[0]


def convert_to_unix_utc(timestamp_str):
    time_struct = time.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S')
    return int(time.mktime(time_struct))


def convert_sickness_level(date, input_path):
    workbook = openpyxl.load_workbook(input_path)
    sheet = workbook['Sheet1']
    comfort_data = defaultdict(list)

    for row in sheet.iter_rows(min_row=2, values_only=True):
        value = row[1]

        if value is None:
            continue

        timestamp = convert_to_unix_utc(date + ' ' + str(row[0]))
        comfort_data[timestamp].append(value)

    with open(input_path.replace('.xlsx', '.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Timestamp', 'Comfort Level'])

        for timestamp, c_level in comfort_data.items():
            writer.writerow([timestamp, c_level[0]])

    os.remove(input_path)