import requests
import math


def find_toponym(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['formatted']
    try:
        toponym_postal = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']
    except KeyError:
        toponym_postal = 'Объект не имеет почтового индекса!'
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    spn = degree(toponym)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(spn),
        "l": "sat,skl",
        "pt": ",".join([toponym_longitude, toponym_lattitude, 'pm2blywl'])
    }
    return map_params, toponym_address, toponym_postal


def degree(obj):
    corners = obj['boundedBy']['Envelope']
    left_bottom, right_upper = corners['lowerCorner'].split(), corners['upperCorner'].split()
    return str(abs((float(left_bottom[0]) - float(right_upper[0])) / 2)), \
           str(abs((float(left_bottom[1]) - float(right_upper[1])) / 2))


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance