import os
import pandas as pd
from tqdm import tqdm
import get_fitbit


sleep_logs = []

data_type = 'sleep'
datetimes = pd.date_range('2016-11-09', '2017-08-10')

sleep_list = []

for datetime in tqdm(datetimes):
    fitbit_data = get_fitbit.FitbitData(datetime, data_type)
    sleep_log = fitbit_data.load_from_disk()

    for sleep_event in sleep_log['sleep']:
        trim_dict = {}
        key_list = sleep_event.keys()
        for this_key in key_list:
            if this_key != 'minuteData':
                trim_dict[this_key] = sleep_event[this_key]
        sleep_list.append(trim_dict)

df_sleep = pd.DataFrame(sleep_list)

start_sleep = pd.to_datetime(df_sleep['startTime'])
df_sleep['start_datetime'] = start_sleep

# Sum from 6pm to 6pm instead of midnight to midnight.
df_sleep['datetime'] = df_sleep['start_datetime'] + pd.Timedelta(hours=6)
df_sleep = df_sleep.set_index('datetime')

data_path = os.path.join(
    os.getcwd(), os.pardir, os.pardir, 'data', 'interim', 'sleep_data.csv')
df_sleep.to_csv(data_path, index_label='datetime')

