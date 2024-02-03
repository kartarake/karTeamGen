#IMPORTS
import os
import json
import random


#DASH BOARD
tstat_cutoff = 350
top_percent = 35

"""You can edit these numbers around according to your need.

Attributes:
    top_percent (int): The top percentage pokemons which will be choosen.
    tstat_cutoff (int): The minimum total stat allowed for picking.
"""


#ERROR CLASS
class karTeamGenError(Exception):

    """Summary
    """
    
    pass



#DATA LOADING
def load_data():
    """   
    Returns:
        TYPE: The total data from the json file will be returned.
    """
    with open('data.json','r') as f:
        all_data = json.load(f)

    return all_data

def load_coefficients():
    """   
    Returns:
        TYPE: The coefficients dict will be returned.
    """
    with open('coefficients.json', 'r') as f:
        coefficients = json.load(f)

    return coefficients



#CHART  
def chart_create():
    """    
    Returns:
        TYPE: Returns a new chart to work with.
    """
    chart = {
        'defense':{
            'normal':0,
            'fire':0,
            'water':0,
            'electric':0,
            'grass':0,
            'ice':0,
            'fighting':0,
            'poison':0,
            'ground':0,
            'flying':0,
            'psychic':0,
            'bug':0,
            'rock':0,
            'ghost':0,
            'dragon':0,
            'dark':0,
            'steel':0,
            'fairy':0
        },
        'attack':{
            'normal':0,
            'fire':0,
            'water':0,
            'electric':0,
            'grass':0,
            'ice':0,
            'fighting':0,
            'poison':0,
            'ground':0,
            'flying':0,
            'psychic':0,
            'bug':0,
            'rock':0,
            'ghost':0,
            'dragon':0,
            'dark':0,
            'steel':0,
            'fairy':0
        }
    }
    return chart

def chart_fill(data,nameindex,chart,core,type_chart):
    for poke in core:
        natno = nameindex[poke]
        types = data[natno]['type']

        for type in types:    
            for i in chart['defense']:
                chart['defense'][i] += type_chart[type]['defense'][i]
            for i in chart['attack']:
                chart['attack'][i] += type_chart[type]['attack'][i]
    
    return chart



#POKEMON TYPE CATEGORIZING 
def poke_type_cat(data):

    t_sweeper = {}
    t_spl_sweeper = {}
    t_tank = {}
    t_spl_tank = {}
    t_hazard = {}

    for poke in data:
        #exclusions
        if sum(data[poke]['base_stat']) < tstat_cutoff:
            continue

        if 'mega' in data[poke]['name']:
            continue
        elif 'eternamax' in data[poke]['name']:
            continue
        elif 'gmax' in data[poke]['name']:
            continue

        #real part
        base_stat = data[poke]['base_stat']

        t_sweeper[poke] = base_stat[1] + base_stat[5]
        t_spl_sweeper[poke] = base_stat[3] + base_stat[5]
        t_tank[poke] = base_stat[0] + base_stat[2]
        t_spl_tank[poke] = base_stat[0] + base_stat[4]

        if any(move in data[poke]['moves'] for move in ['stealth-rock','spikes','toxic-spikes']):
            t_hazard[poke] = base_stat[0]

    sweeper = []
    for i in range((len(t_sweeper) * top_percent) // 100):
        poke = max(t_sweeper, key= lambda k: t_sweeper[k])
        sweeper.append(poke)
        del t_sweeper[poke]

    spl_sweeper = []
    for i in range((len(t_spl_sweeper) * top_percent) // 100):
        poke = max(t_spl_sweeper, key= lambda k: t_spl_sweeper[k])
        spl_sweeper.append(poke)
        del t_spl_sweeper[poke]

    tank = []
    for i in range((len(t_tank) * top_percent) // 100):
        poke = max(t_tank, key= lambda k: t_tank[k])
        tank.append(poke)
        del t_tank[poke]

    spl_tank = []
    for i in range((len(t_spl_tank) * top_percent) // 100):
        poke = max(t_spl_tank, key= lambda k: t_spl_tank[k])
        spl_tank.append(poke)
        del t_spl_tank[poke]

    hazard = []
    for i in range((len(t_hazard) * top_percent) // 100):
        poke = max(t_hazard, key= lambda k: t_hazard[k])
        hazard.append(poke)
        del t_hazard[poke]

    poketype = {
        'sweeper':sweeper,
        'spl_sweeper':spl_sweeper,
        'tank':tank,
        'spl_tank':spl_tank,
        'hazard':hazard
    }

    with open('poketype.json','w') as f:
        json.dump(poketype, f, indent=3)

    return poketype    

def in_poketype(poke,poketype):

    for cat in poketype:
        if poke in poketype[cat]:
            return True
    else:
        return False

def detect_poketype(poke,poketype,nameindex):

    natno = nameindex[poke]
    col_key = []

    for key in poketype:
        if natno in poketype[key]:
            col_key.append(key)
    
    if col_key:
        return col_key
    else:
        return None



#HAS WEATHER
def hasweather(data,nameindex,core,weather):

    if weather == 'sun':
        for poke in core:
            natno = nameindex[poke]

            if 'drought' in data[natno]['ability'].values():
                return True
        else:
            return False

    elif weather == 'rain':
        for poke in core:
            natno = nameindex[poke]

            if 'drizzle' in data[natno]['ability'].values():
                return True
        else:
            return False

    elif weather == 'sand':
        for poke in core:
            natno = nameindex[poke]

            if 'sand-stream' in data[natno]['ability'].values():
                return True
        else:
            return False

    elif weather == 'normal':
        return True

    else:
        raise karTeamGenError(f'Invalid weather : {weather}')



#REQ COUNT
def reqcount(team_type,weather):

    if team_type == 'balanced' and weather == 'normal':
        team_type_count = {
            'sweeper' : 1,
            'spl_sweeper' : 1,
            'tank' : 1,
            'spl_tank' : 1,
            'rando' : 1,
            'weatherset' : 0,
            'hazard' : 1
        }

    elif team_type == 'ho' and weather == 'normal':
        team_type_count = {
            'sweeper' : 2,
            'spl_sweeper' : 2,
            'tank' : 0,
            'spl_tank' : 0,
            'rando' : 1,
            'weatherset' : 0,
            'hazard' : 1
        }

    elif team_type == 'defensive' and weather == 'normal':
        team_type_count = {
            'sweeper' : 0,
            'spl_sweeper' : 0,
            'tank' : 2,
            'spl_tank' : 2,
            'rando' : 1,
            'weatherset' : 0,
            'hazard' : 1
        }

    elif team_type == 'balanced' and weather in ['rain','sand','sun']:
        team_type_count = {
            'sweeper' : 1,
            'spl_sweeper' : 1,
            'tank' : 1,
            'spl_tank' : 1,
            'rando' : 0,
            'weatherset' : 1,
            'hazard' : 1
        }

    elif team_type == 'ho' and weather in ['rain','sand','sun']:
        team_type_count = {
            'sweeper' : 2,
            'spl_sweeper' : 2,
            'tank' : 0,
            'spl_tank' : 0,
            'rando' : 0,
            'weatherset' : 1,
            'hazard' : 1
        }

    elif team_type == 'defensive' and weather in ['rain','sand','sun']:
        team_type_count = {
            'sweeper' : 0,
            'spl_sweeper' : 0,
            'tank' : 2,
            'spl_tank' : 2,
            'rando' : 0,
            'weatherset' : 1,
            'hazard' : 1
        }

    else:
        raise karTeamGenError('Error loading required team count.')

    return team_type_count

def reqcheckoff(col_poketypes, team_type_count):

    for array in col_poketypes:
        for item in array:
            team_type_count[item] -= 1

    return team_type_count

def reqrando():
    """Summary
    
    Returns:
        TYPE: Description
    """
    choice = random.choice([
        'sweeper',
        'spl_sweeper',
        'tank',
        'spl_tank'
    ])

    return choice

def teamcountrando(team_type_count):

    team_type_count['rando'] -= 5

    return team_type_count

def reqguess(team_type_count,weather,core,nameindex,data):

    copy_team_type_count = team_type_count.copy()

    if hasweather(data,nameindex,core,weather) or weather == 'normal':
        del copy_team_type_count['weatherset']

    output = max(copy_team_type_count, key=lambda k: copy_team_type_count[k])
    
    if output == 'rando':
        team_type_count = teamcountrando(team_type_count)
        output = reqrando()

    return output 



#TEAM PICKING
def tree(poketype,data,poke_type,core,chart,type_chart,nameindex):

    tree = {}

    if os.path.exists('coefficients.json'):
        coefficients = load_coefficients()
    else:
        coefficients = {
            'stat_typing_atk':1,
            'stat_typing_def':1,
            'stat_':1
        }    

    for poke in poketype[poke_type]:
        if poke in [nameindex[natno] for natno in core]:
            continue

        potential = core.copy()
        potential.append(data[poke]['name'])

        copy_chart = chart.copy()
        copy_chart = chart_fill(data,nameindex,copy_chart,potential,type_chart)

        stat_typing_atk = sum(copy_chart['attack'].values())
        stat_typing_def = sum(copy_chart['defense'].values())

        base_stat = data[poke]['base_stat']

        if poke_type == 'sweeper':
            stat_ = base_stat[1] + base_stat[5] 
        elif poke_type == 'spl_sweeper':
            stat_ = base_stat[3] + base_stat[5]
        elif poke_type == 'tank':
            stat_ = base_stat[0] + base_stat[2]
        elif poke_type == 'spl_tank':
            stat_ = base_stat[0] + base_stat[4]
        elif poke_type == 'hazard':
            stat_ = base_stat[0]
        else:
            raise karTeamGenError(f'Invalid Poketype : {poke_type}')

        worth = sum([
            stat_typing_atk * coefficients['stat_typing_atk'],
            stat_typing_def * coefficients['stat_typing_def'],
            stat_ * coefficients['stat_']
        ])

        tree[poke] = worth

    poke = max(tree, key= lambda k: tree[k])
    return poke

def weatherpick(data,weatherset,core,weather):

    if weather == 'sun':
        need_aility = 'drought'
    elif weather == 'rain':
        need_aility = 'drizzle'
    elif weather == 'sand':
        need_aility = 'sand-stream'
    else:
        raise karTeamGenError(f'{weather} is invalid')

    potential = []
    for natno in weatherset:
        if any(name in data[natno]['name'] for name in ['mega','gmax','eternamax']):
            continue

        if need_aility in data[natno]['ability'].values():
            potential.append(natno)

    poke = random.choice(potential)

    return data[poke]['name']



#MAIN
def main(*args, **quargs):
    """This is the main function which takes in pokemon names as input and or list which contains pokemon names and 
    calcualtes the suitable team mates and returns them as a list which contains 6 pokemon names.
    
    Args:
        *args: Pokemons or seq of pokemons
        **quargs: More options like weather/ team type
    
    Returns:
        TYPE: A team of 6 pokemon
    
    Raises:
        karTeamGenError: Description
    """
    global team_type_count
    
    core = []
    for poke in args:
        if type(poke) in [list,tuple]:
            core.extend(poke)
        else:
            core.append(poke)

    for item in core:
        if type(item) != str:
            raise karTeamGenError('The arguments must be string')
    else:
        pass

    if len(core)>6:
        raise karTeamGenError('The number of cores must be less than or equal to 6')

    elif len(core) == 6:
        return core

    all_data = load_data()
    data = all_data['pokemon']
    nameindex = all_data['nameindex']
    poketype = all_data['poketype'] 
    weather_setter = all_data['weatherset']
    type_chart = all_data['type_chart']  

    chart = chart_create()
    chart = chart_fill(data,nameindex,chart,core,type_chart)

    if quargs:
        for key in quargs.keys():
            if key not in ['team_type','weather']:
                raise karTeamGenError(f'Key: {key} is not registered.')
        else:
            pass

    if 'team_type' in quargs.keys():
        if quargs['team_type'] == 'balanced':
            team_type = 'balanced'

        elif quargs['team_type'] == 'ho':
            team_type = 'ho'

        elif quargs['team_type'] == 'defensive':
            team_type = 'defensive'

        else:
            team_type = quargs['team_type']
            raise karTeamGenError(f'Team Type :{team_type} is not registered. Please use balanced/ho/defensive.')
    else:
        team_type = 'balanced'

    if 'weather' in quargs.keys():
        if quargs['weather'] == 'normal':
            weather = 'normal'
        
        elif quargs['weather'] == 'sun':
            weather = 'sun'

        elif quargs['weather'] == 'rain':
            weather = 'rain'

        elif quargs['weather'] == 'sand':
            weather = 'sand'

        else:
            weather = quargs['weather']
            raise karTeamGenError(f'Weather :{weather} is not registered. Please use normal/sun/rain/sand.')
    else:
        weather = 'normal'

    for poke in core:
        natno = nameindex[poke]
        if not in_poketype(natno,poketype):
            raise karTeamGenError(f'We are sorry. We dont accept poke: {poke} ')   

    col_poketypes = []
    for poke in core:
        temp = detect_poketype(poke,poketype,nameindex)
        if temp:
            col_poketypes.append(temp)
        else:
            raise karTeamGenError(f'We are sorry. We cant find poke: {poke} in poketype')
   
    team_type_count = reqcount(team_type, weather)
    team_type_count = reqcheckoff(col_poketypes, team_type_count)

    if weather != 'normal' and not hasweather(data,nameindex,core,weather):
        poke = weatherpick(data,weather_setter,core,weather)
        core.append(poke)

    for count in range(6 - len(core)):
        poke_type = reqguess(team_type_count,weather,core,nameindex,data)

        poke = tree(poketype, data,poke_type, core,chart, type_chart, nameindex)
        poke = data[poke]['name']
        core.append(poke)

        chart = chart_fill(data, nameindex, chart, core, type_chart)

        col_poketypes = []
        for poke in core:
            temp = detect_poketype(poke,poketype,nameindex)
            if temp:
                col_poketypes.append(temp)
            else:
                raise karTeamGenError(f'We are sorry. We cant find poke: {poke} in poketype')
    
        team_type_count = reqcount(team_type, weather)
        team_type_count = reqcheckoff(col_poketypes, team_type_count)

    return core



# SAMPLE RUN

if __name__ == '__main__':
    try:
        team = main('charizard')
        print(team)
        input()
    except Exception as e:
        print(e)
        input()