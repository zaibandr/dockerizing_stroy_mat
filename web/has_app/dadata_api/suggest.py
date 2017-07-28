# -*- coding: utf-8 -*-

import json
import requests

API_KEY = 'cd3175f7b81a01e3ca532680c32d0011fe8336f6'
BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/%s'


def suggest(query, resource):
    url = BASE_URL % resource
    headers = {
        'Authorization': 'Token %s' % API_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        'query': query
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(r.text, encoding='utf-8')


q = 'Синявинская, 11 13'
resp = suggest(q, 'address')
try:
    print(resp["suggestions"][0]["value"])
    print(resp["suggestions"][0]["unrestricted_value"])
except Exception as e:
    print(e)
json.dump(resp, open('test.txt', 'w', encoding='utf-8'), indent=4)
