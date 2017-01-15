# Configuration
PATH_IN_SLEEPBOT_EXPORT = "E:/Pending/Sleep/SleepBot/Exports/14_01_17_1484325789185.csv"
PATH_IN_SLEEPBOT_EXPORT = "E:/Pending/Sleep/SleepBot/Exports/14_01_17_1484325789185_dev.csv"
PATH_OUT_SLEEP_AS_ANDROID = ""
SLEEPBOT_EXPORT_DATE_FORMAT = "%d/%m/%y"
SLEEPBOT_EXPORT_TIME_FORMAT = "%H:%M"
TIMEZONE = "Asia/Hong_Kong"

# Constants
SLEEPBOT_EXPORT_HEADER = ["Date", "Sleep Time", "Wake Time", "Hours", "Note"]

# Import
import csv
from datetime import datetime, timedelta
import math
from collections import namedtuple

# Define named tuple
SleepbotExportRow = namedtuple('SleepbotExportRow', 'sleep_time wake_time note')

# Functions implementation
def check_header(row):
    result = True
    size = len(row)
    if size == len(SLEEPBOT_EXPORT_HEADER):
        for i in range(size):
            if SLEEPBOT_EXPORT_HEADER[i].lower() != row[i].strip().lower():
                result = False
                break
    else:
        result = False
    return result

def parse_sleepbot_row(row):
    result = None
    if len(row) == 5:
        # Trim all space characters
        map(str.strip, row)
        # Parse the sleep time and wake time
        sleep_time = datetime.strptime(row[0] + ' ' + row[1], SLEEPBOT_EXPORT_DATE_FORMAT + ' ' + SLEEPBOT_EXPORT_TIME_FORMAT)
        wake_time = datetime.strptime(row[0] + ' ' + row[2], SLEEPBOT_EXPORT_DATE_FORMAT + ' ' + SLEEPBOT_EXPORT_TIME_FORMAT)
        # Check whether the sleep time advanced some days, in Sleepbot, the date is the date of the wake time
        if wake_time < sleep_time:
            # Check the sleep hours, just in case someone sleep over 24 hours which will across 2 days
            sleep_hours = float(row[3])
            day_adj = math.ceil(sleep_hours / 24)
            # Adjust the sleep time
            sleep_time -= timedelta(days = day_adj)
        # Build the result
        result = SleepbotExportRow(sleep_time, wake_time, row[4])
    else:
        print('WARN: Skipping invalid Sleepbot data', row)
    return result

def process(row):
    row = parse_sleepbot_row(row)
    print(row)

# Main implementation
with open(PATH_IN_SLEEPBOT_EXPORT, 'r') as in_file:
    reader = csv.reader(in_file)
    header = next(reader, [])
    if check_header(header):
        for row in reader:
            process(row)
    else:
        print('ERROR: Header of Sleepbot export file is not correct, expected ', SLEEPBOT_EXPORT_HEADER, ', given ', header, sep = '')
