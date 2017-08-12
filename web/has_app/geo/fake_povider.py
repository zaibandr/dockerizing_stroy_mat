from faker import Factory
import json
import random as rnd

fake = Factory.create('ru_RU')

# provider_names = ['stroy', 'pesok', 'carier', '24', 'moscow', 'construct', 'beton', 'dom', ]
providers = []

with open('rnd_poly_yandex.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    # print(data)

    d = {}
    for feature in data['features']:
        hex_color = [hex(rnd.randrange(0, 255))[2:] for _ in range(3)]
        color = '#{}'.format(''.join(hex_color))
        fake_name = fake.name()
        fake_corp = 'ООО "{}"'.format(fake_name)

        feature['properties']['fill'] = color
        feature['properties']['description'] = fake_corp

        print(data)

        rnd_phone = '8{}{}{}'.format(*list(map(str, [rnd.randint(900, 980), rnd.randint(100, 999), rnd.randint(1000, 9999)])))
        provider = {
            "model": 'has_app.provider',
            "pk": feature['id'],
            "fields": {
                'name': fake_corp,
                'contact_name': fake_name,
                'phone_number': rnd_phone,
                'products': list(set([rnd.randint(1, 21) for i in range(rnd.randint(10, 21))])),
                'geom': {
                    'type': 'Polygon',
                    'coordinates': [feature['geometry']['coordinates'][0]]
                }
            }
        }
        print(provider)
        providers.append(provider)


with open('provider_fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(providers, f, indent=4)


with open('rnd_providers_geojson.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
