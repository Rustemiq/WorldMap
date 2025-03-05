import requests

server_address = 'http://geocode-maps.yandex.ru/1.x/?'
apikey = '8013b162-6b42-4997-9691-77b7074026e0'


def get_obj_info(geocode):
    params = {
        'apikey': apikey,
        'geocode': geocode,
        'format': 'json'
    }

    response = requests.get(server_address, params=params)
    response_json = response.json()
    toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['formatted']
    toponym_coordinates = list(map(float, toponym_coordinates.split()))
    return toponym_coordinates, toponym_address