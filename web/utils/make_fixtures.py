import json

with open('products.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n')
    f_name = f.name

print(f_name)
model = data[0]
in_fields = data[1].split(', ')
items = data[2:]
print(in_fields)


fixt = []

for pk, values in enumerate(items, start=1):
    print(values)
    fields = {}
    for i, k in enumerate(in_fields):
        if k == 'price':
            fields[k] = int(values.split('\t')[i].replace(' ', ''))
        else:
            fields[k] = values.split('\t')[i]
    print(fields)

    d = {
        "model": model,
        "pk": pk,
        "fields": fields
    }
    fixt.append(d)

print(fixt)

with open('{}.json'.format(f_name.split('.')[0]), 'w', encoding='utf-8') as f:
    json.dump(fixt, f, indent=4)
