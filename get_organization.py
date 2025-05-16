import requests

api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
search_api_server = "https://search-maps.yandex.ru/v1/"


def get_org(ll, org_name):
    search_params = {
        "apikey": api_key,
        "text": org_name,
        "lang": "ru_RU",
        "ll": ll,
        "spn":'0.5,0.5',
        "type": "biz",
        "rspn": '1',
        'results': '1'
    }
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    try:
        pt = json_response['features'][0]['geometry']['coordinates']
        address = json_response['features'][0]['properties']['name']
        return pt, address
    except IndexError:
        return None, None