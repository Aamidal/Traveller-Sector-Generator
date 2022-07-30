 #system_presence.py
from random import randint, choice
from lib.namegen import new_name
import requests


def roll_dice(x = 1):
    '''Roll x 6 sided dice, return the sum.'''
    count = 0
    total = 0
    while count < x:
        count = count + 1
        total = total + randint(1, 6)
    return total

def map_gen(map_size = 'subsector'):
    '''Generate a list of coordinates '''
    if map_size.lower() == 'subsector':
        x = 10
        y = 8
    elif map_size.lower() == 'sector':
        x = 40
        y = 32
    else:
        print('map_gen(map_size) must equal sector or subsector')

    grid = [str(row + 1).zfill(2) + str(col + 1).zfill(2)
            for row in range(y) for col in range(x)]

    return grid

def check_systems(subsector, n):
    ''' Accept (list, n) where n is the minimum dice value signifying system
        at coordinates. Check n against 1d6, return a list of coordinates
        containing a system'''

    hex_map = subsector
    print('Checking for sytems on', str(n) + '+.')
    systems = [x for x in hex_map if roll_dice() >= n]
    return systems

def get_trade(x):
    uwp_raw = x  
    uwp = uwp_raw.upper()
    trade_codes = []

    # Rich Worlds: Any world with a government type of 4 - 9, an atmosphere of 6 or
    # 8, and a population of 6 - 8 is a rich world.
    if uwp[5] in ('4', '5', '6', '7', '8', '9'):
        if uwp[2] in ('6', '8'):
            if uwp[4] in ('6', '7', '8'):
                trade_codes.append('Ri ')

    # Agricultural Worlds: Any world with atmosphere 4 - 9, hydrographic percentage
    # 4 - 8, and population 5 - 7 is an agricultural world.
    if uwp[2] in ('4', '5', '6', '7', '8', '9'):
        if uwp[3] in ('4', '5', '6', '7', '8'):
            if uwp[4] in ('5', '6', '7'):
                trade_codes.append('Ag ')

    # Industrial Worlds: A world with an atmosphere 0, 1, 2, 4, 7, or 9, and a popula-
    # tion of 9 or more is an industrial world.
    if uwp[2] in ('0', '1', '2', '4', '7', '9'):
        if uwp[4] in ('9', 'A'):
            trade_codes.append('In ')

    # Poor World: Any world with an atmosphere of 2 - 5, and a hydrographic percen-
    # tage of 3 or less is a poor world.
    if uwp[2] in ('2', '3', '4', '5'):
        if uwp[3] in ('0', '1', '2', '3'):
            trade_codes.append('Po ')


    # Non-Agricultural Worlds: Any world with an atmosphere 3 or less, hydrographic
    # percentage 3 or less, and population 6 or greater is a non-agricultural world.
    if uwp[2] in ('0', '1', '2', '3'):
        if uwp[3] in ('0', '1', '2', '3'):
            if uwp[4] in ('6', '7', '8', '9', 'A'):
                trade_codes.append('Na ')

    # Non-Industrial Worlds: Any world with a population of 6 or less is a non-
    # industrial world.
    if uwp[4] in ('0', '1', '2', '3', '4', '5', '6'):
        trade_codes.append('Ni ')

    return trade_codes

def get_world(x = '0101'):
    """Generate a Traveller world and return it's profile"""

    portclass = {
        2 : 'A', 3 : 'A', 4 : 'B', 5 :'B', 6 :'C', 7 : 'C', 8 : 'D', 9 : 'E',
        10 : 'E', 11:  'X', 12 : 'X'
        }
    num = {
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
        9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G',
        17 : 'H', 18: 'I'
    }

    prime_star = {0 : 'B', 1 : 'B', 2 : 'A', 3 : 'M', 4 : 'M', 5 : 'M', 6: 'M',
    7 : 'M', 8: 'K', 9: 'G', 10: 'F', 11: 'F', 12: 'F'
    }

    prime_size = {0 : 'Ia', 1 : 'Ib', 2 : 'II', 3 : 'III', 4 : 'IV', 5 : 'V',
     6: 'V', 7 : 'V', 8: 'V', 9: 'V', 10: 'V', 11: 'VI', 12: 'D'
    }

    comp_star = {0 : 'B', 1 : 'B', 2 : 'A', 3 : 'F', 4 : 'F', 5 : 'G', 6: 'G',
    7 : 'K', 8: 'K', 9: 'M', 10: 'M', 11: 'M', 12: 'M'
    }

    comp_size = {0 : 'Ia', 1 : 'Ib', 2 : 'II', 3 : 'III', 4 : 'IV', 5 : 'D',
     6: 'D', 7 : 'V', 8: 'V', 9: 'VI', 10: 'D', 11: 'D', 12: 'D'
    }

    name = str(new_name(15)).ljust(17)

    # System hex number
    coord = x

    # Starport assigned a class based on 2d6 roll.
    starport = portclass[roll_dice(2)]

    # Starports A, B contain naval bases on 8+.
    navy = False
    if starport in ['A', 'B'] and roll_dice(2) > 7:
        navy = True

    # Starports A, B, C, and D contain scout bases on 7+, with a penalty
    # inversely related to port quality.
    scout = False
    if starport == 'A' and roll_dice(2) > 9:
        scout = True
    elif starport == 'B' and roll_dice(2) > 8:
        scout = True
    elif starport == 'C' and roll_dice(2) > 7:
        scout = True
    elif starport == 'D' and roll_dice(2) > 6:
        scout = True

    # Determine base code
    if navy and scout == True:
        bases = 'B'
    elif navy == True:
        bases = 'N'
    elif scout == True:
        bases = 'S'
    else:
        bases = ' '

    # Size is 2d6-2.
    size = roll_dice(2) - 2

    # Atmosphere is 2d6-7+size. Size 0 = Atmosphere 0.
    atmosphere = roll_dice(2) - 7 + size
    if size == 0 or atmosphere < 0:
        atmosphere = 0
    if atmosphere > 12:
        atmosphere = 12

    # Hydrographics is 2d6-7+size. 0 if size 0, and -4 if extreme atmosphere
    hydrographics = roll_dice(2) - 7 + size
    if atmosphere in [0, 1, 9, 10, 11, 12]:
        hydrographics -= 4
    if size == 0 or hydrographics < 0:
        hydrographics = 0
    if hydrographics > 10:
        hydrographics = 10

    # population is 2d6-2
    population = roll_dice(2) - 2
    # determine population mod
    p = randint(1, 9)

    # Government is 2d6-7+population. If no population, then no government.
    government = roll_dice(2) - 7 + population
    if population == 0 or government < 0:
        government = 0
    if government > 13:
        government = 13

    # Law is 2d6-7+government. If no population, then no law.
    law = roll_dice(2) - 7 + government
    if population == 0 or law < 0:
        law = 0
    if law > 10:
        law = 10
    
    # Determine tech level based on 1d6 + various modifiers.
    tech = 0
    if starport == 'A':
        tech += 6
    elif starport == 'B':
        tech += 4
    elif starport == 'C':
        tech += 2
    elif starport == 'E':
        tech -= 2
    elif starport == 'X':
        tech -= 4
    if size < 2:
        tech += 2
    elif size < 5:
        tech += 1
    if atmosphere < 4 or atmosphere > 9 :
        tech += 1
    if hydrographics == 9:
        tech += 1
    elif hydrographics == 10:
        tech += 2
    if population > 0 and population < 6:
        tech += 1
    elif population == 10:
        tech += 2
    if government == (0, 5):
        tech += 1
    elif government == 13:
        tech -= 2
    tech_level = roll_dice(1) + tech
    if tech_level < 0:
        tech_level = 0

    # Determine travel zone. 12+ on 2d6, select randomly from zones.
    check_zone = roll_dice(2)
    zones = [' ', 'A', 'R']
    if check_zone < 12:
        zone = ' '
    elif check_zone == 12:
        zone = choice(zones)

    # Expanded Star system Generation per Book 6: Scouts

    # Determine Solo, Binary or Trinary star system
    nature = 1
    nature_roll = roll_dice(2)
    if nature_roll < 8:
        nature = 1
    elif nature_roll < 12:
        nature = 2
    elif nature_roll == 12:
        nature = 3

    # Determine primary star type and size, save roll to modify any companions
    primary_roll = roll_dice(2)
    primary_mod = 0
    if atmosphere in [4, 5, 6, 7, 8, 9] or population > 7:
        primary_mod += 4
    primary_type = roll_dice(2) + primary_mod
    if primary_type < 0:
        primary_type = 0
    if primary_type > 12:
        primary_type = 12
    spectral1 = randint(1, 9)
    primary_size = roll_dice(2) + primary_mod
    if primary_size < 0:
        primary_size = 0
    if primary_size > 12:
        primary_size = 12
    if primary_size == 12:
        spectral1 = ''
    star_1 = f'{prime_star[primary_type]}{spectral1} {prime_size[primary_size]}'

    # Companion star generation
    comp1_type = None
    comp2_type = None
    comp1_size = None
    comp2_size = None
    star_2 = ''
    star_3 = ''
    if nature == 2:
        comp1_type = roll_dice(2) + primary_roll
        if comp1_type < 0:
            comp1_type = 0
        if comp1_type > 12:
            comp1_type = 12
        spectral2 = randint(1, 9)
        comp1_size = roll_dice(2) + primary_roll
        if comp1_size < 0:
            comp1_size = 0
        if comp1_size > 12:
            comp1_size = 12
        if comp1_size in [5, 6, 10, 11, 12]:
            spectral2 = ''
        star_2 = f'{comp_star[comp1_type]}{spectral2} {comp_size[comp1_size]}'

        if nature == 3:
            comp2_type = roll_dice(2) + primary_roll
            if comp2_type < 0:
                comp2_type = 0
            if comp2_type > 12:
                comp2_type = 12
            spectral3 = randint(1, 9)  
            comp2_size = roll_dice(2) + primary_roll
            if comp2_size < 0:
                comp2_size = 0
            if comp2_size > 12:
                comp2_size = 12
            if comp2_size in [5, 6, 10, 11, 12]:
                spectral3 = ''      
            star_3 = f'{comp_star[comp2_type]}{spectral3} {comp_size[comp2_size]}'


    stellar = f'{star_1} {star_2} {star_3}'
    
    # Planetoid belt and Gas giants generation
    
    # Determine maximum orbits, modified by star size and type
    orbits = roll_dice(2)
    if primary_type in [3, 4, 5, 6, 7]:
        orbits -=4
    elif primary_type == 8:
        orbits -= 2
    if primary_size in [0, 1, 2]:
        orbits += 8
    elif primary_size == 3:
        orbits +=4
    elif orbits < 0:
        orbits = 0
    
    # Determine gas giant presence and number, not exceeding orbits
    if roll_dice(2) >= 10: # A system does not contain a gas giant on a 10+.
        gas = False
    else:
        gas = True
    
    gas_roll = roll_dice(2)
    if gas_roll < 4:
        g = 1
    elif gas_roll < 6:
        g = 2
    elif gas_roll < 8:
        g = 3
    elif gas_roll < 10:
        g = 4
    elif gas_roll < 13:
        g = 5
    
    # Determine belt presence and quantity
    belt_presence = False
    if roll_dice(2) - g < 7:
        belt_presence = True
    if belt_presence == True:
        belt_roll = roll_dice(2) - g
        if belt_roll < 0:
            b = 3
        if belt_roll < 7:
            b = 2
        else:
            b = 1
    else: 
        b = 0
    
    # checking number of orbits against belts and gas giants
    if b + g > orbits:
        b = orbits - g
        if b < 0:
            b = 0
    

    # Start bringing it all together. 

    uwp = str(starport + num[size] + num[atmosphere] + num[hydrographics] + 
    num[population] + num[government] + num[law] + '-' + num[tech_level])

    pbg = f'{p}{b}{g}'

    # Parse UWP to determine world's trade codes.

    trade_raw = ''.join(get_trade(uwp))
    trade = trade_raw.ljust(14)

    # Let's make it pretty. Format the world and it's hex coordinate in GENIE
    # format to be used on travellermap.com
    world = f'{name} {coord} {uwp}  {bases} {trade} {zone}   {pbg} --'
    
    return world

def save_data(sector_data, file = 'sector_gen.txt'):
    """
    Exports sector_data to text file, accepts an optional file name.
    """
    f = open(file, 'w')
    for x in sector_data:
        print(x)
        f.write(x + '\n')

    f.close()
    print("Data saved to " + file)

    sec_map = open(file, 'r')
    export_map(sec_map)
    sec_map.close()


def print_grid_results(map_size, sector):
    """
    Output world count and hex numbers with system presence
    """
    print(
    '''
    Initializing League of the Road survey data...
    Pulling up-to-date travel advisories from the Society of Many Journeys...
    '''
    )
    print("The following hexes contain notable systems: " + ' '.join(sector))
    print(
        "For a total of:", str(len(sector)), "systems in the", map_size.lower() +
        ':'
        )

def generate_worlds(sector):
    """
    Accepts a list of coordinates and assigns a randomly generated world to each
    """
    sector_data = []
    for x in sector:
        world = (get_world(x))
        sector_data.append(world)
    return sector_data

def new_sector(map_size = "sector", system_presence = 5, verbose = True):
    '''
    map_size accepts accepts 'sector' for 32x40 grid, and 'subsector' for 8x10 grid.
    system_presence sets chance for system presence where a system is present 
    on a roll of n+ on 1d6.
    Prints hex numbers and world count if verbose flag = true
    '''
    sector = check_systems(map_gen(map_size), system_presence)
    if verbose == True:
        print_grid_results(map_size, sector)
    generate_worlds(sector)
    save_data(generate_worlds(sector))

def export_map(sector_data):
    """
    Exports sector data to https://travellermap.com/make/poster and returns an
    image in pdf format
    """
    url = "https://travellermap.com/api/poster"
    params = { 
        'accept': 'application/pdf',
        'options': '25591',
        'style': 'poster'
         }
    headers = {
        'Content-Type': 'text/plain',
    }
    response = requests.post(url, data = sector_data, json = None, params = params, headers = headers)

    print(response.url)

    with open('sector_map.pdf', 'wb') as f:
        f.write(response.content)
    f.close()

    print("Map exported to sector_map.pdf")

# Main Code Block
if __name__ == "__main__":
    new_sector()
    input("Press enter to quit...")