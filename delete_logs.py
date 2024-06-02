#this script run weekly and delete the logs older than 7days
import os
import datetime
import glob

# 7days ago
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# find and delete logs older than 7days
log_files = glob.glob('logs/log_*.log')
for log_file in log_files:
    file_date_str = log_file.split('_')[1].split('.')[0]  # extract date from the log name
    file_date = datetime.datetime.strptime(file_date_str, '%Y-%m-%d').date()
    if file_date < seven_days_ago:
        os.remove(log_file)