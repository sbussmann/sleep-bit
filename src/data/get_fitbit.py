import fitbit
import os
import json
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv


class ActivityData(object):
    def __init__(self):
        # find .env automagically by walking up directories until it's found
        dotenv_path = find_dotenv()

        # load up the entries as environment variables
        load_dotenv(dotenv_path)

        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")
        access_token = os.environ.get("ACCESS_TOKEN")
        refresh_token = os.environ.get("REFRESH_TOKEN")
        expires_at = float(os.environ.get("EXPIRES_AT"))

        self.authd_client = fitbit.Fitbit(
            client_id, client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at)

        self.raw_dir = os.path.join(os.pardir, os.pardir, 'data', 'raw')

    def download_intraday(self, base_date):
        intraday = self.authd_client.intraday_time_series(
            'activities/steps', base_date=base_date, detail_level='1min')
        return intraday

    def load_intraday(self, base_date):

        file_name = "intraday_{}".format(base_date)
        file_path = os.path.join(self.raw_dir, file_name)
        try:
            with open(file_path, 'r') as data_file:
                intraday = json.load(data_file)
        except OSError:
            intraday = self.download_intraday(base_date)

        return intraday

    def write_intraday(self, intraday, base_date):
        file_name = "intraday_{}".format(base_date)
        file_path = os.path.join(self.raw_dir, file_name)
        with open(file_path, 'w') as data_file:
            json.dump(intraday, data_file)
