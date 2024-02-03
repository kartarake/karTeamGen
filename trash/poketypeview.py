import json

with open('poketype.json','r') as f:
    poketype = json.load(f)

with open('pokemon.json','r') as f:
    data = json.load(f)

for cat in poketype:
    print(cat.upper())
    for natno in poketype[cat]:
        name = data[natno]['name']
        print(f'{natno} : {name}')
    print()