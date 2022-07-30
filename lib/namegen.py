import random
import sys

"""
This module generates new names using a Markov Chain model read from a newline
separated list. It saves user-approved generated names to a new list. Rejected
names are stored in a third list and will never be output again. 

The Markov dictionary is built using both the original name lists and the
generated names, if available.
"""
keep_file = "./data/keep.txt"
real_world_file = "./data/inspiration.txt"
blacklist_file = "./data/reject.txt"

with open(keep_file, "r") as places_file: #output list
    places = places_file.read().splitlines()
with open(real_world_file, "r") as real_file: #initial list
    inspiration = [line.strip() for line in real_file]
with open(blacklist_file, "r") as rejects_file: #rejected list
    rejects = rejects_file.read().splitlines()

name_data = places + inspiration
blacklist = rejects + inspiration

menu_options = {
    1: 'Train the name generator.',
    2: 'Generate batch names.',
    3: 'View/edit list of place names.',
    4: 'View/edit list of rejects.',
    5: 'Quit.',
}

list_menu = {
    1: 'Add names',
    2: 'Remove names',
    3: 'Output list to file',
    4: 'Save and return',
}

def print_menu():
    #prints a formatted main menu
    print('What would you like to do?')
    for key in menu_options.keys():
        print (key, '--', menu_options[key])

def print_list_menu():
    #prints a formatted main menu
    print('What would you like to do?')
    for key in list_menu.keys():
        print (key, '--', list_menu[key])

class Markov_Dict:
    def __init__(self):
        self.dict = {}
    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            raise KeyError(key)
    def add_key(self, prefix, suffix):
        if prefix in self.dict:
            self.dict[prefix].append(suffix)
        else:
            self.dict[prefix] = [suffix]
    def get_suffix(self,prefix):
        l = self[prefix]
        return random.choice(l)

class Markov_Name:
    """
    A name from a Markov chain
    """
    def __init__(self, chainlen = 3):
        """
        Building the dictionary
        """
        if chainlen > 10 or chainlen < 1:
            print("Chain length must be between 1 and 10, inclusive")
            sys.exit(0)
    
        self.mcd = Markov_Dict()
        oldnames = []
        self.chainlen = chainlen
    
        for l in name_data:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")
    
    def New(self):
        """
        New name from the Markov chain
        """
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if suffix == "\n" or len(name) > 9:
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.title()  
        
def train_names():
    """
    Uses markov model to generate novel names. Allows user to accept or 
    reject names, adding them to respective list. Queue allows user to revist
    a name they are undecided on at the end of the loop.
    """
    run_count = 0
    yes_count = 0
    queue_count = 0
    no_count = 0
    loop = True
    queue = []
    while loop == True:
        name = Markov_Name().New()
        if name not in name_data and name not in rejects:
            run_count += 1
            print(name)
            keep_raw = input('1 - Keep, 2 - Add to queue, 3 - Reject. Press Q to quit.\n')
            keep = keep_raw.lower()
            if keep == '1':
                yes_count += 1
                places.append(name)
            elif keep == '2':
                queue_count += 1
                queue.append(name)
                continue 
            elif keep == '3':
                no_count += 1
                rejects.append(name)
                continue
            elif keep == 'q':
                loop = False
                if queue_count > 0:
                    print(f'{queue_count} items in queue:')
                    print(queue)
                    q_raw = input('Reprocess (1) or discard (2) queue?')
                    q = q_raw.lower()
                    if q == '1':
                        for i in queue:
                            print(i)
                            q_keep_inp = input("1 - Keep, 2 - Reject. 'Q' to quit. ")
                            q_keep = q_keep_inp.lower()
                            if q_keep == '1':
                                yes_count += 1
                                places.append(i)
                                queue.remove(i)
                            elif q_keep == '2':
                                no_count +=1
                                rejects.append(i)
                                queue.remove(i)
                            elif q_keep == 'Q':
                                print('Queue cleared. Returning to menu.')
                                queue = []
                                break
                            else:
                                print('Invalid input.')
                                continue
                    if q == '2':
                        print('Queue cleared. Returning to menu.')
                        queue = []
                        break
            else:
                print('Invalid input. Input 1, 2, or 3. Q to quit.')
                continue
        else:
            continue


    print('Updating dictionary...')
    print(f'Generated {run_count} names. Kept {yes_count} and rejected {no_count}.')

    with open(keep_file, 'w') as fi:
        for place in places:
            fi.write(place + "\n")
    with open(blacklist_file, 'w') as fi:
        for reject in rejects:
            fi.write(reject + "\n")

    input('Dictionary updated. Press any key to quit.')

def new_name():
    name = Markov_Name().New()
    if name not in blacklist:
        return name
    else:
        return new_name()

def generate_names(num = 25):
    """
    Use markov model to generate num names.
    """
    count = 0
    while count < num:
        count += 1
        print(new_name())
    print(f'{count} names generated.')

def add_names(x):
    """
    Add names to list.
    """
    name_list = x    
    while(True):
        name_raw = input("Enter name to add or press 'Q' to quit.")
        name = name_raw.title()
        if name != 'Q':
            name_list.append(name)
            print(f'Added {name} to list!')
            print(f'There are {len(name_list)} names in the list.')
            continue
        else:
            print('Returning to main menu')
            break

def remove_names(x):
    """
    Remove specific names from list.
    """
    name_list = x    
    while(True):
        name_raw = input("Enter name to add or press 'Q' to quit.")
        name = name_raw.title()
        if name != 'Q':
            if name in name_list:
                name_list.remove(name)
                print(f'Removed {name} to list!')
                print(f'There are {len(name_list)} names in the list.')
                continue
            else:
                print('Name not found. Check spelling and try again.')
                continue
        else:
            print('Returning to main menu')
            break

def access_list(x):
    """
    Allow user to view and edit the list of accepted or rejected names.
    """
    name_list = x
    which_list = None
    if name_list is places:
        which_list = 'Places'
    elif name_list is rejects:
        which_list = 'Rejects'
    else:
        print('Invalid which list')
        main_menu()

    print(name_list)
    print(f'There are currently {len(name_list)} names in {which_list}.')
    while(True):
        print_list_menu()
        option = ''
        try:
            option = int(input('\nInput: '))
        except:
            print(
                '\nPlease enter numbers only.\n'
                )
            continue
        # Check which choice was entered and act accordingly        
        if option == 1: 
            print('\nAdding names...\n')
            add_names(name_list)
        elif option == 2:
            print('\nRemoving names...\n')
            remove_names(name_list)
        elif option == 3:
            print('\nWriting list to new file...\n')
            with open(f'{which_list}_new.txt', 'w') as o:
                for name in name_list:
                    o.write(f'{name}\n')
        elif option == 4:
            print('\nReturning to main menu\n')
            with open(keep_file, 'w') as fi:
                for place in places:
                    fi.write(place + "\n")
            with open(blacklist_file, 'w') as fi:
                for reject in rejects:
                    fi.write(reject + "\n")
            break
        else: 
            print(
                '\nInvalid input. Please enter a number between 1 and 4.\n'
                )


def main_menu():
    """
    Print main menu options and save name lists on exit.
    """
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('\nInput: '))
        except:
            print(
                '\nPlease enter numbers only.\n'
                )
            continue
        # Check which choice was entered and act accordingly        
        if option == 1: 
            print('\nGenerating new names:\n')
            train_names()
        elif option == 2:
            print('\nGenerating batch of names...\n')
            generate_names()
        elif option == 3:
            print('\nAccessing list of places...\n')
            access_list(places)
        elif option == 4:
            print('\nAccessing rejected names....\n')
            access_list(rejects)
        elif option == 5:
            print('\nExiting...')
            with open(keep_file, 'w') as fi:
                for place in places:
                    fi.write(place + "\n")
            with open(blacklist_file, 'w') as fi:
                for reject in rejects:
                    fi.write(reject + "\n")
            exit()
        else: 
            print(
                '\nInvalid input. Please enter a number between 1 and 5.\n'
                )

# Main Code Block
if __name__ == "__main__":
    print("System Name Generator\n")
    main_menu()
