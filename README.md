# karTeamGen
This is a code which generates a team of pokemon from your cores. The team consists of 6 pokemon including your core. You can also create weather teams using this code.

# Instruction
1) First copy the code and data.json to your dirc and import them.
2) Use the teamgenalgo.main() where the args are as follows
3) You can input pokemon names (string) (lowercase) either by
```py
import teamgenalgo
team = teamgenalgo.main('charizard','venusaur')
#or
team = teamgenalgo.main(['charizard','venusaur'])
```
4) Now you can also set weather and team type by
```py
import teamgenalgo
team = teamgenalgo.main('charizard','venusaur',weather='sun',team_type='ho')
```
All possible inputs for weather = 'sun'/ 'rain'/ 'sand'/ 'normal' (default)  
All possible inputs for team_type = 'balanced' / 'ho' (hyper offensive) / 'defenisve'

This is code is in development and would encourage your contribution.
