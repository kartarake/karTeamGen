import os
import json

path = 'sprites'

namelist = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

namelist2 = []

for item in namelist:
	namelist2.append(item.replace('.png',''))

with open('namelist.json','w') as f:
	json.dump(namelist2,f,indent=5)