# 2gisTestAPIregions

Automation API teststhe  for https://regions-test.2gis.com/1.0/regions
* language: Python3 
* framework: Pytest 
* libs: requests, configparser, os, logging

## Structure of the project

* test_api_2gis/test_region/test_regions_params_func.py -- функциональные тесты api regions
* test_api_2gis/utils/ApiRegions.py ------------------------- APIRegions + requests
* test_api_2gis/config.ini ----------------------------------- конфиг файл, в котором прописан базовый url
* test_api_2gis/tools/LoggerError.py ------------------------ логер ошибок 4хх и 5хх
* test_api_2gis/tools/CurlReturn.py -------------------------- cURL maker

### Example of test

In the test, I check that the passed page_size parameter == the number of elements on the page. The test uses parameterization to test all possible positive scenarios. The status code is checked using assert. The number of elements in the items array is counted. The total amount is compared with the value of the passed parameter.
```
@pytest.mark.parametrize("page_size", ["5", "10", "15"])
def test_get_regions_page_size_valid(page_size):
    result: Response = ApiRegions.get_regions(page_size=page_size)
    assert result.status_code == 200
    response_json = result.json()
    assert len(response_json['items']) == int(page_size)
```

### Example of API helper class + requests (ApiRegions)

This class is required to make an API request. I am using configparser to read the base url from config.ini. Based on the BASE_URL, I form the url of the REGIONS request. Using the requests library and Python features, I wrote a function that sends a GET request over REGIONS with an optional set of parameters. Before returning a response, I call the LoggerError.logging_error() function, which logs the error (if any). I will write more about the artisanal logger below.
```
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

```

### Logger

The LoggerError.logging_error(result) function takes the required parameter result (the result of the API request). Also, to form a cURL request that can be easily imported into Postman, I use the CurlReturn.curlReturn(result) function. Logging occurs if the response code == 4xx or 5xx. Nuances:

* If a response with a 4xx code returns a standard error response with an error identifier, then the error code and error id are written to the log

Standard server response on error:
```

{
    "error": {
        "id": "86e976e4-c0e1-4ac6-8095-166b9286e098",
        "message": "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz"
    }
}

```
Example of logging:
```
-------------------------------- live log call ---------------------------------
ERROR CODE: 400 -- id: 86e976e4-c0e1-4ac6-8095-166b9286e098

```
* If for some reason, the response with the 4xx code does not return a standard error response, then the error code will be written to the log and cURL for manual verification

Example of logging:
```
-------------------------------- live log call ---------------------------------
ERROR CODE: 400 --  curl --location --request GET 'https://regions-test.2gis.com/1.0/regions?page=0' --header 'User-Agent: python-requests/2.25.1' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive' --header 'Content-Type: application/json'

```
* In the case of a response with a 5xx code, the error code and cURL for manual verification are also written to the log

Example of logging:
```
-------------------------------- live log call ---------------------------------
ERROR CODE: 500 --  curl --location --request GET 'https://regions-test.2gis.com/1.0/regions?page=0' --header 'User-Agent: python-requests/2.25.1' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive' --header 'Content-Type: application/json'
