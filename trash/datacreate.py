import json

# A py script used to create a master json file which contains all of the individual json into one.

#Master variable
master = {}

#version
version = 'karTeamGen data v0.1'
master['version'] = version

#loading all json files and fitting them in master
json_list = ['nameindex.json','pokemon.json','poketype.json','weatherset.json']

for file in json_list:
    with open(file,'r') as f:
        data = json.load(f)
    
    name = file.replace('json','')

    master[name] = data

    print(f'Completed flecthing data for {name}')

print('*'*70)

with open('data.json','w') as f:
    json.dump(master,f,indent=3)

print('Success! created data.json')