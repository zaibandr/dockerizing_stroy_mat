import json

with open('geo_json.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    fixtures = []

    for feature in data['features']:
        print(feature)
        d = {
            "model": 'has_app.zone',
            "pk": feature['id'],
            "fields": {
                'name': feature['properties']['description'],
                'polygon': feature['geometry']['coordinates'][0]
            }
        }
        fixtures.append(d)

with open('zone_fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(fixtures, f, indent=4)