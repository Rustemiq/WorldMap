import requests
import sys

server_address = 'https://static-maps.yandex.ru/v1?'
apikey = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
map_file = "map.png"


def get_map(ll, spn, pt, theme):
    ll = ','.join(map(str, ll))
    spn = str(spn) + ',' + str(spn)
    params = {
        'apikey': apikey,
        'll': ll,
        'spn': spn,
        'theme': theme,
    }
    if pt is not None:
        params['pt'] = ','.join(map(str, pt))

    response = requests.get(server_address, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)