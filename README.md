# 2gisTestAPIregions

Автотесты для API https://regions-test.2gis.com/1.0/regions
* Язык: Python3 
* Фреймворк: Pytest 
* Библиотеки: requests, configparser, os 

## Структура проекта

* test_api_2gis/test_region/test_regions_params_func.py -  функциональные тесты
* test_api_2gis/utils/ApiRegions.py - APIRegions manager (для каждого раздела API создается свой класс)
* test_api_2gis/config.ini - конфиг файл, в котором прописан базовый url

### Пример теста

В тесте я проверяю, что передаваемому параметру page_size соответствует количество элементов на странице. В тесте используется параметризация. Проверяется статус-код. Переберается масив с регионами. Затем итоговая сумма сравнивается с значением переданного параметра.

```
@pytest.mark.parametrize("page_size", ["5", "10", "15"])
def test_get_regions_page_size_valid(page_size):
    result: Response = ApiRegions.get_regions(page_size=page_size)
    assert result.status_code == 200
    response_json = result.json()
    countItem = 0
    for _ in response_json['items']:
        countItem += 1
    assert countItem == int(page_size)
```

### Пример APIManager (ApiRegions)

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

        return result

```
