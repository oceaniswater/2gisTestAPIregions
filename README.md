# 2gisTestAPIregions

Автотесты для API https://regions-test.2gis.com/1.0/regions
* Язык: Python3 
* Фреймворк: Pytest 
* Библиотеки: requests, configparser, os, logging

## Структура проекта

* test_api_2gis/test_region/test_regions_params_func.py -- функциональные тесты api regions
* test_api_2gis/utils/ApiRegions.py ------------------------- APIRegions + requests
* test_api_2gis/config.ini ----------------------------------- конфиг файл, в котором прописан базовый url
* test_api_2gis/tools/LoggerError.py ------------------------ логер ошибок 4хх и 5хх
* test_api_2gis/tools/CurlReurn.py -------------------------- cURL maker

### Пример теста

В тесте я проверяю, что передаваемому параметру page_size соответствует количество элементов на странице. В тесте используется параметризация для проверки всех возможных позитивных сценариев. Выполняется проверка статус-кода с помощью assert. Подсчитывается колличество элементов массива items. Итоговая сумма сравнивается со значением переданного параметра.

```
@pytest.mark.parametrize("page_size", ["5", "10", "15"])
def test_get_regions_page_size_valid(page_size):
    result: Response = ApiRegions.get_regions(page_size=page_size)
    assert result.status_code == 200
    response_json = result.json()
    assert len(response_json['items']) == int(page_size)
```

### Пример класса API + requests (ApiRegions)

Этот класс необходим для соверешения API запроса. Я использую configparser чтобы считать base url из config.ini. На оснве BASE_URL я формирую url запроса REGIONS. Используя библиотеку requests и возможности Python, я написал функцию, которая отправляет GET запрос по REGIONS с необязательным набором параметров. Перед тем как вернуть ответ я вызываю функцию LoggerError.logging_error(), которая логирует ошибку (если таковая имеется). Подробнее о кустарном логере я напишу ниже.

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

### Логер

Функция LoggerError.logging_error(result) принимает обязательный параметр result (результат API запроса). Также для формирования cURL запроса, который можно без проблем импортировать в Postman, я использую функцию CurlReturn.curlReturn(result). Логирование происходит в случае, если код ответа == 4хх или 5хх. Ньюансы:

* В случае, если ответ с кодом 4хх возвращает стандартный для ошибок ответ, в котором есть идентификатор ошибки, то в лог записывается код ошибки и id ошибки

Стандартный ответ сервера при ошибке:
```

{
    "error": {
        "id": "86e976e4-c0e1-4ac6-8095-166b9286e098",
        "message": "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz"
    }
}

```
Пример логирования:
```
-------------------------------- live log call ---------------------------------
ERROR CODE: 400 -- id: 86e976e4-c0e1-4ac6-8095-166b9286e098

```
* Если по каким то причинам, ответ с кодом 4хх не возвращает стандартный ответ с ошибкой, то в лог запишется код ошибки и cURL для ручной проверки

Пример логирования:
```
-------------------------------- live log call ---------------------------------
ERROR CODE: 400 --  curl --location --request GET 'https://regions-test.2gis.com/1.0/regions?page=0' --header 'User-Agent: python-requests/2.25.1' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive' --header 'Content-Type: application/json'

```
* В случае с ответом с кодом 5хх в лог записывается так же код ошибки и cURL для ручной проверки

Пример логирования:
```
-------------------------------- live log call ---------------------------------
ERROR CODE: 500 --  curl --location --request GET 'https://regions-test.2gis.com/1.0/regions?page=0' --header 'User-Agent: python-requests/2.25.1' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive' --header 'Content-Type: application/json'
