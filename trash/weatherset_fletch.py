import json

with open('pokemon.json','r') as f:
    data = json.load(f)

col = []
for no in data:
    if sum(data[no]['base_stat']) >= 350:
        check = True
    else:
        check = False

    if any(ability in (data[no]['ability'].values()) for ability in ['drought','drizzle','sand-stream']) and check:
        print(data[no]['name'])
        col.append(no)

with open('weatherset.json','w') as f:
    json.dump(col,f,indent=3)

