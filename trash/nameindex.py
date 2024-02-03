import json

with open('trash\\namelist.json','r') as f:
    namelist = json.load(f)

with open('E:\\Coding\\karTeamGen\\pokemon.json','r') as f:
    data = json.load(f)

namei = {}
for index in namelist:
    name = data[index]['name']
    namei[name] = index

with open('nameindex.json','w') as f:
    json.dump(namei,f,indent=3)