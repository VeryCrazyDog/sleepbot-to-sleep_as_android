# Configuration
PATH_IN_SLEEPBOT_EXPORT = "E:/Pending/Sleep/SleepBot/Exports/14_01_17_1484325789185.csv"
PATH_OUT_SLEEP_AS_ANDROID = "E:/Pending/Sleep/SleepBot/Exports/14_01_17_1484325789185_out.csv"
SLEEPBOT_EXPORT_DATE_FORMAT = "%d/%m/%y"
SLEEPBOT_EXPORT_TIME_FORMAT = "%H:%M"
TIMEZONE = "Asia/Hong_Kong"
NOTE_PREFIX = "[Import from Sleepbot]"

# Constants
SLEEPBOT_EXPORT_HEADER = ["Date", "Sleep Time", "Wake Time", "Hours", "Note"]
SLEEP_AS_ANDROID_TIME_FORMAT = '%H:%M'
SLEEP_AS_ANDROID_DATETIME_FORMAT = '%d. %m. %Y %-H:%M'
SLEEP_AS_ANDROID_DATETIME_FORMAT = '{dt:%d}. {dt:%m}. {dt:%Y} {dt.hour}:{dt:%M}'

# Import
import collections
import csv
from datetime import datetime, timedelta
import decimal
import math

# Define named tuple
SleepbotExportRow = collections.namedtuple('SleepbotExportRow', 'sleep_time wake_time hours note')

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
        # Parse the sleep time, wake time and sleep hours
        sleep_time = datetime.strptime(row[0] + ' ' + row[1], SLEEPBOT_EXPORT_DATE_FORMAT + ' ' + SLEEPBOT_EXPORT_TIME_FORMAT)
        wake_time = datetime.strptime(row[0] + ' ' + row[2], SLEEPBOT_EXPORT_DATE_FORMAT + ' ' + SLEEPBOT_EXPORT_TIME_FORMAT)
        sleep_hours = decimal.Decimal(row[3])
        # Check whether the sleep time advanced some days, in Sleepbot, the date is the date of the wake time
        if wake_time < sleep_time:
            # Check the sleep hours, just in case someone sleep over 24 hours which will across 2 days
            day_adj = math.ceil(sleep_hours / 24)
            # Adjust the sleep time
            sleep_time -= timedelta(days = day_adj)
        # Build the result
        result = SleepbotExportRow(sleep_time, wake_time, sleep_hours, row[4])
    else:
        print('WARN: Skipping invalid Sleepbot data', row)
    return result

def write_sleep_as_android_row(csv_writer, row):
    csv_writer.writerow([
        'Id',
        'Tz',
        'From',
        'To',
        'Sched',
        'Hours',
        'Rating',
        'Comment',
        'Framerate',
        'Snore',
        'Noise',
        'Cycles',
        'DeepSleep',
        'LenAdjust',
        'Geo',
        '"' + datetime.strftime(row.wake_time, SLEEP_AS_ANDROID_TIME_FORMAT) + '"'
    ])
    csv_writer.writerow([
        '"' + str(int(row.sleep_time.timestamp()) * 1000) + '"',
        '"' + TIMEZONE + '"',
        '"' + SLEEP_AS_ANDROID_DATETIME_FORMAT.format(dt = row.sleep_time) + '"',
        '"' + SLEEP_AS_ANDROID_DATETIME_FORMAT.format(dt = row.wake_time) + '"',
        '"' + SLEEP_AS_ANDROID_DATETIME_FORMAT.format(dt = row.wake_time) + '"',
        '"' + '{0:.3f}'.format(row.hours) + '"',
        '"0.0"',
        '"' + NOTE_PREFIX + row.note + '"',
        '"10000"',
        '"-1"',
        '"-1.0"',
        '"-1"',
        '"-2.0"',
        '"0"',
        '""',
        '"0.0"'
    ])

def process(csv_writer, row):
    row = parse_sleepbot_row(row)
    write_sleep_as_android_row(csv_writer, row)

# Main implementation
with open(PATH_IN_SLEEPBOT_EXPORT, 'r') as in_file, open(PATH_OUT_SLEEP_AS_ANDROID, 'w', newline = '') as out_file:
    reader = csv.reader(in_file)
    header = next(reader, [])
    if check_header(header):
        writer = csv.writer(out_file, quoting = csv.QUOTE_NONE, escapechar = '', quotechar = '')
        count = 0
        for row in reader:
            process(writer, row)
            count += 1
            if count % 50 == 0:
                print('Converted', count, 'records!' if count > 1 else 'record!')
        print('Converted', count, 'records!' if count > 1 else 'record!')
        print('Convertion finished!')
    else:
        print('ERROR: Header of Sleepbot export file is not correct, expected ', SLEEPBOT_EXPORT_HEADER, ', given ', header, sep = '')
