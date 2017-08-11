import fitbit
import os
import json
from dotenv import load_dotenv, find_dotenv


class FitbitData(object):

    def __init__(self, base_date, data_type):

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

        self.base_date = base_date

        self.data_type = data_type

        file_name = "{}_{}.json".format(
            self.data_type, str(self.base_date.date()))
        project_dir = '/Users/rbussman/Projects/sleep-bit'
        raw_dir = os.path.join(project_dir, 'data', 'raw')
        self.file_path = os.path.join(raw_dir, file_name)

    def download_from_fitbit(self):

        if self.data_type == 'intraday':

            data = self.authd_client.intraday_time_series(
                'activities/steps', base_date=self.base_date,
                detail_level='1min')

        elif self.data_type == 'sleep':
            data = self.authd_client.get_sleep(self.base_date)

        else:
            print("data_type must be `intraday` or `sleep`")
            data = None

        return data

    def load_from_disk(self):
        try:
            with open(self.file_path, 'r') as data_file:
                data = json.load(data_file)
        except OSError:
            data = self.download_from_fitbit()

        return data

    def write_to_disk(self, data):
        with open(self.file_path, 'w') as data_file:
            json.dump(data, data_file)

