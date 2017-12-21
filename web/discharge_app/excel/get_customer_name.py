import os
import json
from discharge_app.excel.excel_import import discharge_excel_to_json
import pprint

customer_names = []

bank_dump_dir = 'bank_dump'
bank_dumps = os.listdir(bank_dump_dir)

for dis in bank_dumps:
    dis_json = discharge_excel_to_json(os.path.join(bank_dump_dir, dis))
    print(dis_json)
    for action in json.loads(dis_json):
        if action['credit'] != '':
            customer_names.append(action['name'])

unique_customer_names = set(customer_names)
print(len(unique_customer_names))
print(sorted(list(unique_customer_names)))
