import json
import random

with open('qwerty_04-08-2017_18-17-42.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    # print(data)

    d = {}
    for feature in data['features']:
        if feature['geometry']['type'] == 'Point':
            key = str(feature['properties'].get('description', None)).replace('\n', '')
            d[key] = feature['geometry']['coordinates']


a = '120'
b = '80'
print(d)


features = []
cardinal = ['NNE', 'ENE', 'ESE', 'SSE', 'SSW', 'WSW', 'WNW', 'NNW']

for a, b in [('120', '80'), ('80', '50'), ('50', '20'), ('20', '0')]:
    for c in cardinal:
        x, y = c[0], c[1:]
        # print(x, y)
        if a == '20' and b == '0':
            p1 = '{} {}'.format(x, a)
            p2 = '{} {}'.format(y, a)

            poly = [d['(0, 0)'], d[p1], d[p2], d['(0, 0)']]
        else:
            point_s = '{} {}, {} {}, {} {}, {} {}'.format(x, a, x, b, y, b, y, a)

            poly = [d[i] for i in point_s.split(', ')]
            poly += [poly[0]]

        hex_color = [hex(random.randrange(0, 255))[2:] for _ in range(3)]
        color = '#{}'.format(''.join(hex_color))

        print(poly)
        feature = {
            'properties': {
                'fill': color,
                'stroke-opacity': 0.9,
                'stroke-width': '5',
                'fill-opacity': 0.6,
                'stroke': '#ed4543',
                'description': '{} {}-{}'.format(c, a, b)
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

print(features)

geo_json = {
        'type': 'FeatureCollection',
        'features': features
}

with open('geo_json.json', 'w', encoding='utf-8') as f:
    json.dump(geo_json, f)
