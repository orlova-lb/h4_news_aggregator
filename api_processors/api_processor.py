import requests
from main_logger import MainLogger


class BaseAPIProcessor:
    def __init__(self):
        self.url = ""
        self.api_key = ""
        self.offset = 0
        self.limit = 5
        # TODO: make logging module and use it
        self.log = MainLogger(self)

    def refresh_data(self):
        self.log.info(f'refresh_data - '
                      f'Start')
        try:
            new_data = self._get_data()
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to get data from API: '
                           f'{e}')
            return False

        try:
            clean_data = self._clean_news(raw_news=new_data)
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to clean data: '
                           f'{e}')
            return False

        try:
            self._save_news(data_to_save=clean_data)
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to save data: '
                           f'{e}')
            return False
        self.log.info(f'refresh_data - '
                      f'Done')
        try:
            self._save_tags(data_to_save=clean_data)
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to save tags: '
                           f'{e}')
            return False
        return True

    def _get_data(self):
        req_params = {
            "api-key": self.api_key,
            "offset": self.offset
        }
        try:
            response = requests.get(self.url, params=req_params)
        except Exception as e:
            self.log.error(f'_get_data - '
                           f'failed to make a request: '
                           f'{e}')
            raise e
        if response.status_code != 200:
            self.log.error(f'_get_data - '
                           f'received {response.status_code}')
            raise RuntimeError(f'{response.status_code}: {response.text}')

        return response.json()

    def _clean_news(self, raw_news):
        raise NotImplementedError

    def _save_news(self, data_to_save):
        raise NotImplementedError

    def _clean_tags(self, raw_news):
        raise NotImplementedError

    def _save_tags(self, data_to_save):
        raise NotImplementedError


if __name__ == '__main__':
    t = BaseAPIProcessor()
    t.refresh_data()

