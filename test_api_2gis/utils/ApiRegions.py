import configparser
from test_api_2gis.tools.LoggerError import LoggerError


import requests
import os


class ApiRegions:
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.ini'))


    BASE_URL = parser.get('2gis', 'basic_url')

    REGIONS = BASE_URL + "/1.0/regions"

    @staticmethod
    def get_regions(**args):
        url = ApiRegions.REGIONS
        headers = {'Content-Type': 'application/json'}
        payload = args
        result = requests.request("GET", url, headers=headers, params=payload)

        LoggerError.logging_error(result)

        return result
