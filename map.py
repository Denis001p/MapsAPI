import requests
from io import BytesIO
from PIL import Image
from functions import find_toponym

if '?':  # Поиск объекта, а также его адреса и почтового индекса
    map_params, address, postal = find_toponym('Moscow')
    print(address)
    print(postal)
else:  # Если запроса на поиск нет
    lon, lat = '39.599220', '52.608820'
    l = 2
    z = '13'
    map_params = {
        "ll": ",".join([lon, lat]),
        "l": ('map', 'sat', 'sat,skl')[l],
        "z": z
    }

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
