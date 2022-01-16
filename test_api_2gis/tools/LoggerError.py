# from concurrent.futures._base import LOGGER
from test_api_2gis.tools.CurlReurn import CurlReturn
import logging

LOGGER = logging.getLogger(__name__)


class LoggerError:
    LOGGER = logging.getLogger(__name__)

    @staticmethod
    def logging_error(result):
        if result.status_code >= 400:
            if result.status_code < 500:
                response_json = result.json()
                curl = CurlReturn.curlReturn(result)
                try:
                    idError = response_json['error']['id']
                except:
                    idError = None

                if idError is not None:
                    LOGGER.info(f"ERROR CODE: {result.status_code} -- id: {response_json['error']['id']}")
                else:
                    LOGGER.info(f"ERROR CODE: {result.status_code} -- curl: {curl}")
        if result.status_code >= 500:
            curl = CurlReturn.curlReturn(result)
            LOGGER.info(f"ERROR CODE: {result.status_code} --  {curl}")
