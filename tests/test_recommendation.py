import pytest
import requests
import json
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG

## Alwasy happens before and after each test
@pytest.fixture(autouse=True)
def run_around_tests():
    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.database_service.delete_and_populate()


def test_recommendation_invalid():
    populate_tests_different_ratings()
    "Tries to get recommendation for user numer 1000"
    print("Testing GET URL: /users/1000/recommendation")

    url = 'http://rest_api_service/users/1000/recommendation'
    get_resp = requests.get(url)

    assert get_resp.status_code == 404
    assert get_resp.text == 'User ID does not exist!'


def test_recommendation_2():
    populate_tests_different_ratings()
    "Gets recommendation for user numer 2"
    print("Testing GET URL: /users/2/recommendation")

    url = 'http://rest_api_service/users/2/recommendation'
    get_resp = requests.get(url)

    assert get_resp.status_code == 200
    assert len(get_resp.json()) == 10



def test_recommendation_5():
    populate_tests_different_ratings()
    "Tries to get recommendation for user numer 5"
    print("Testing GET URL: /users/5/recommendation")

    url = 'http://rest_api_service/users/5/recommendation'
    get_resp = requests.get(url)

    response = [
        {
            'id': 5,
            'title': 'Automated regional firmware',
            'director': 'Celesta Richardeau',
            'type': 'Betamax',
            'release_date': '1992-06-15T00:00:00',
            'eidr': '10.5240/FAFF-EFFF-FEEF-EAEF-DEEC-C',
            'avg rating': '2.5000000000000000'
        },
        {
            'id': 3,
            'title': 'Business-focused neutral productivity',
            'director': 'Teddie Mackrell',
            'type': 'VHS',
            'release_date': '2010-09-19T00:00:00',
            'eidr': '10.5240/FFFF-DCEF-EEFD-FFFD-DCFF-C',
            'avg rating': '5.4000000000000000'
        },
        {
            'id': 2,
            'title': 'Ameliorated background superstructure',
            'director': 'Beale Riguard',
            'type': 'Betamax',
            'release_date': '2003-06-12T00:00:00',
            'eidr': '10.5240/FFCE-FBFB-EFFF-FEEB-FEEE-C',
            'avg rating': '6.0000000000000000'
        },
        {
            'id': 1,
            'title': 'Adaptive 24/7 parallelism',
            'director': 'Melony Kearley',
            'type': 'Betamax',
            'release_date': '1999-09-23T00:00:00',
            'eidr': '10.5240/FFFF-EFDF-EEED-DEEE-EFFF-C',
            'avg rating': '6.0000000000000000'
        },
        {
            'id': 6,
            'title': 'Reverse-engineered bi-directional budgetary management',
            'director': 'Terry Carayol',
            'type': 'Betamax',
            'release_date': '1999-11-29T00:00:00',
            'eidr': '10.5240/FEFF-FFFD-FFFD-EFFF-FFFF-C',
            'avg rating': '4.0000000000000000'
        },
        {
            'id': 7,
            'title': 'Multi-tiered responsive frame',
            'director': 'Seth Rubke',
            'type': 'VHS',
            'release_date': '2009-03-17T00:00:00',
            'eidr': '10.5240/EABD-FDFD-EDEF-DFEE-FFEF-C',
            'avg rating': '5.5000000000000000'
        },
        {
            'id': 8,
            'title': 'Up-sized asymmetric synergy',
            'director': 'Had Haselgrove',
            'type': 'VHS',
            'release_date': '1995-06-11T00:00:00',
            'eidr': '10.5240/FDFC-FFEE-FEDF-FFEB-6AFE-C',
            'avg rating': '7.0000000000000000'
        },
        {
            'id': 4,
            'title': 'Optional responsive hardware',
            'director': 'Jenine Winnett',
            'type': 'Betamax',
            'release_date': '1991-09-12T00:00:00',
            'eidr': '10.5240/EEFE-FDFE-FDFF-FEFF-FEB4-C',
            'avg rating': '3.7500000000000000'
        },
        {
            'id': 10,
            'title': 'Down-sized multi-state utilisation',
            'director': 'Balduin Ransley',
            'type': 'Betamax',
            'release_date': '2012-03-23T00:00:00',
            'eidr': '10.5240/FEEF-EEEF-FFFF-FDEE-DFDF-C',
            'avg rating': None
        },
        {
            'id': 9,
            'title': 'Synchronised client-driven artificial intelligence',
            'director': 'Aline McGrill',
            'type': 'VHS',
            'release_date': '1997-03-29T00:00:00',
            'eidr': '10.5240/DEEF-CCFD-CFDF-FFCF-FFFD-C',
            'avg rating': None
        }
    ]

    assert get_resp.status_code == 200
    assert get_resp.json() == response


## Utils
# Adds few reviews to the database
def populate_tests_different_ratings():

    for i in range(1, 10):
        for j in range(1, i):
            data = {
                'rating': (i + j) % 10
            }

            url = 'http://rest_api_service/users/' + \
                str(i) + '/reviews/' + str(j)
            requests.post(url, params=data)
