import pytest

from requests import Response
from test_api_2gis.utils.ApiRegions import ApiRegions


# Проверяем запрос
# Проверяем, что статус код 200
# Проверяем если total != 0, то массив элементов items не пустой
# Проверяем, что total == количеству элементов в массиве items


def test_get_regions():
    result: Response = ApiRegions.get_regions()
    assert 200 == result.status_code
    response_json = result.json()
    assert isinstance(response_json['total'], int)
    assert isinstance(response_json['items'], list)
    total = response_json['total']

    if total == 0:
        assert response_json['items'] == []
    else:
        assert response_json['items'] != []
        idsCityCountSet = set()

        if total > 5:
            page_count = (response_json['total'] // 5) + 1
            for n in range(1, page_count + 1):
                result: Response = ApiRegions.get_regions(page_size=5, page=n)
                assert result.status_code == 200
                response_json = result.json()
                for item in response_json['items']:
                    idsCityCountSet.add(item['id'])
            assert total == len(idsCityCountSet)
        else:
            result: Response = ApiRegions.get_regions()
            assert result.status_code == 200
            response_json = result.json()
            for item in response_json['items']:
                idsCityCountSet.add(item['id'])
            assert total == len(idsCityCountSet)


# Проверяем country_code:
# Может принимать значения: ru, kg, kz, cz (проверяю, что регионы выводятся согласно фильтру) (required)
# По умолчанию отображаются регионы из всех стран (required)


@pytest.mark.parametrize("country_code", ["ru", "cz", "ua", "kz", "kg"])
def test_get_regions_country_code_filter(country_code):
    result: Response = ApiRegions.get_regions(page_size=15)
    assert result.status_code == 200
    response_json = result.json()
    if response_json['total'] > 15:
        page_count = (response_json['total'] // 15) + 1
        for n in range(1, page_count + 1):
            result: Response = ApiRegions.get_regions(country_code=country_code, page=n)
            assert result.status_code == 200
            response_json = result.json()
            for item in response_json['items']:
                print(item['country']['code'])
                assert country_code == item['country']['code']
    else:
        for item in response_json['items']:
            print(item['country']['code'])
            assert country_code == item['country']['code']


def test_get_regions_all_country_code():
    result: Response = ApiRegions.get_regions(page_size=15)
    assert result.status_code == 200
    response_json = result.json()
    countryCodeSet = set()
    if response_json['total'] > 15:
        page_count = (response_json['total'] // 15) + 1
        for n in range(1, page_count + 1):
            result: Response = ApiRegions.get_regions(page=n)
            response_json = result.json()
            for item in response_json['items']:
                countryCodeSet.add(item['country']['code'])
    else:
        for item in response_json['items']:
            countryCodeSet.add(item['country']['code'])

    assert countryCodeSet == {'ru', 'cz', 'ua', 'kz', 'kg'}


# Проверяем page_size:
# Может принимать значения: 5, 10, 15 (required)
# Значение по умолчанию == 15 (required)
# Проверяем, что сервер корректно реагирует на передачу невалидных значений


@pytest.mark.parametrize("page_size", ["5", "10", "15"])
def test_get_regions_page_size_valid(page_size):
    result: Response = ApiRegions.get_regions(page_size=page_size)
    assert result.status_code == 200
    response_json = result.json()
    countItem = 0
    for _ in response_json['items']:
        countItem += 1
    assert countItem == int(page_size)


def test_get_regions_page_size_default():
    result: Response = ApiRegions.get_regions()
    assert 200 == result.status_code
    response_json = result.json()
    countItem = 0
    for _ in response_json['items']:
        countItem += 1
    assert countItem == 15


@pytest.mark.parametrize("page_size", ["-1", "0", "4", "9", "14", "16"])
def test_get_regions_page_size_invalid(page_size):
    result: Response = ApiRegions.get_regions(page_size=page_size)
    assert result.status_code == 400
    response_json = result.json()
    assert response_json['error']['message'] == "Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15"


# Проверяем параметр q:
# Минимум — 3 символа (required) проверяем, что сервер корректно реагирует на отправку валидных/невалидных значений
# Регистр не имеет значения + вхождение (required)
# Если передан этот параметр, все остальные игнорируются (required)
# Пустой ответ, на запрос города, которого нет в БД


@pytest.mark.parametrize("q", ["", " ", "а", "ва", "ква"])
def test_get_regions_q_len(q):
    result: Response = ApiRegions.get_regions(q=q)
    if len(q) >= 3:
        assert result.status_code == 200
        response_json = result.json()
        assert isinstance(response_json['total'], int)
        assert isinstance(response_json['items'], list)
    else:
        assert result.status_code == 400
        response_json = result.json()
        assert response_json['error']['message'] == "Параметр 'q' должен быть не менее 3 символов"


@pytest.mark.parametrize("q", ["Москва", "москва", "ква"])
def test_get_regions_q(q):
    result: Response = ApiRegions.get_regions(q=q)
    assert result.status_code == 200
    response_json = result.json()
    assert isinstance(response_json['items'][0]['id'], int)
    assert response_json['items'][0]['name'] == "Москва"
    assert response_json['items'][0]['code'] == "moscow"
    assert response_json['items'][0]['country']['name'] == "Россия"
    assert response_json['items'][0]['country']['code'] == "ru"


@pytest.mark.parametrize("q", ["Прага", "Днепр"])
def test_get_regions_q_priority(q):
    result: Response = ApiRegions.get_regions(q=q, country_code="kz", page="2", page_size="5")
    assert result.status_code == 200
    response_json = result.json()
    assert response_json['items'][0]['name'] == q


@pytest.mark.parametrize("q", ["абракадабра"])
def test_get_regions_q_empty_result(q):
    result: Response = ApiRegions.get_regions(q=q)
    assert result.status_code == 200
    response_json = result.json()
    assert response_json != []
    assert isinstance(response_json['total'], int)
    assert response_json['items'] == []


# Проверяем параметр page:
# Пустой список при передаче в параметре несуществующей страницы
# Проверяю, что на каждой странице уникальные города
# Проверяю, что система выдает адекватную ошибку (статус код, описание ошибки) при передачи невалидных значений


def test_get_regions_page_empty_result():
    result: Response = ApiRegions.get_regions(page_size=5)
    assert result.status_code == 200
    response_json = result.json()
    if response_json['total'] > 5:
        page_count = (response_json['total'] // 5) + 1
        result: Response = ApiRegions.get_regions(page=page_count + 1)
        response_json = result.json()
        assert response_json != []
        assert isinstance(response_json['total'], int)
        assert response_json['items'] == []
    else:
        result: Response = ApiRegions.get_regions(page=2)
        response_json = result.json()
        assert response_json != []
        assert isinstance(response_json['total'], int)
        assert response_json['items'] == []


def test_get_regions_page_unique_data():
    result: Response = ApiRegions.get_regions()
    assert result.status_code == 200
    response_json = result.json()
    assert response_json != []
    total = response_json['total']
    if total > 10:
        firstPageIdsCitySet = set()
        secondPageIdsCitySet = set()
        result: Response = ApiRegions.get_regions(page_size=5, page=1)
        assert result.status_code == 200
        response_json = result.json()
        for item in response_json['items']:
            firstPageIdsCitySet.add(item['id'])
        result: Response = ApiRegions.get_regions(page_size=5, page=2)
        assert result.status_code == 200
        response_json = result.json()
        for item in response_json['items']:
            secondPageIdsCitySet.add(item['id'])
        if firstPageIdsCitySet & secondPageIdsCitySet:
            assert False
    else:
        pass


@pytest.mark.parametrize("page", ["-1", "0"])
def test_get_regions_page_bad_request(page):
    result: Response = ApiRegions.get_regions(page=page)
    assert result.status_code == 400
    response_json = result.json()
    assert "Параметр 'page' должен быть больше 0" == response_json['error']['message']
