import configparser
from concurrent.futures._base import LOGGER

import requests
import os
import logging

LOGGER = logging.getLogger(__name__)


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

        if result.status_code >= 400:
            if result.status_code < 500:
                response_json = result.json()
                LOGGER.info(f"Error code: {result.status_code} -- id: {response_json['error']['id']}")
        if result.status_code == 500:
            LOGGER.info(f"Error code: {result.status_code}")

        return result
