from argparse import ArgumentParser

from shapely.geometry import Polygon, Point
import json

from geopy.geocoders import Yandex
from geopy.distance import vincenty


def poly_contains_point(point):
    point = Point(point)
    with open('ya_map.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        # print(data)
        for feature in data['features']:
            if feature['geometry']['type'] == 'Polygon':
                #print(feature['geometry']['coordinates'][0])
                polygon = Polygon(feature["geometry"]['coordinates'][0])
                if polygon.contains(point):
                    print(feature['properties']['description'])

                    print('='*120)


def geocode(address):
    geolocator = Yandex()
    location = geolocator.geocode(address, timeout=10)
    print(location.address)
    print(location.point)
    print((location.latitude, location.longitude))
    center = geolocator.geocode('Москва', timeout=10)

    loc_coord = (location.latitude, location.longitude)
    center_coord = (center.latitude, center.longitude)
    print(vincenty(loc_coord, center_coord).km)

    return location.longitude, location.latitude


def main():
    parser = ArgumentParser(description="A command-line tool that polygon contains point")
    parser.add_argument('-a', '--address', help='')

    args = vars(parser.parse_args())
    address = args['address']

    point = geocode(address)
    poly_contains_point(point)


if __name__ == '__main__':
    main()