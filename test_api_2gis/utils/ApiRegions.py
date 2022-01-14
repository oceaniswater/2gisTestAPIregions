import configparser
import requests


class ApiRegions:
    parser = configparser.ConfigParser()
    parser.read('test_api_2gis/config.ini')

    BASE_URL = parser.get('2gis', 'basic_url')

    REGIONS = BASE_URL + "/1.0/regions"

    @staticmethod
    def get_regions(**args):
        url = ApiRegions.REGIONS
        headers = {'Content-Type': 'application/json'}
        payload = args
        result = requests.request("GET", url, headers=headers, params=payload)

        return result
