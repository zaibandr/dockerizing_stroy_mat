import json
import random

points = []
for i in range(1000):
    x = float('{}.{}'.format(random.randint(36, 38), random.randint(0, 100000000)))
    y = float('{}.{}'.format(random.randint(55, 56), random.randint(0, 100000000)))
    points.append((x, y))

points = [i for i in points if i[1] < 56.5]


features = []
for i in range(20):
    hex_color = [hex(random.randrange(0, 255))[2:] for _ in range(3)]
    color = '#{}'.format(''.join(hex_color))

    poly = [random.choice(points) for _ in range(random.randint(3, 4))]
    poly += [(poly[0])]
    print(poly)

    feature = {
        'properties': {
            'fill': color,
            'stroke-opacity': 0.9,
            'stroke-width': '5',
            'fill-opacity': 0.6,
            'stroke': '#ed4543',
            'description': ' '.join(map(str, poly))
        },
        'id': len(features),
        'geometry': {
            'coordinates': [
                poly
            ],
            'type': 'Polygon'
        },
        'type': 'Feature'
    }
    features.append(feature)

geo_json = {
        'type': 'FeatureCollection',
        'features': features
}

with open('rnd_poly.json', 'w', encoding='utf-8') as f:
    json.dump(geo_json, f)
