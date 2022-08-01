from unicodedata import name
from lib.namegen import new_name as randname
from random import randint, choice
from lib.roll_dice import roll_dice as roll

class World:
  """A random Traveller main world"""

  def set_starport_class(self, starport=None):
    port_class = {
    2 : 'A', 3 : 'A', 4 : 'B', 5 :'B', 6 :'C', 7 : 'C', 8 : 'D', 9 : 'E',
    10 : 'E', 11:  'X', 12 : 'X'
    }

    if starport == None:
        self.starport = port_class[roll(2)]
    else:
        self.starport = starport
  
  def set_bases(self, bases = None):
    if bases == None:
        self.bases = self.determine_base_code


  def determine_base_code(self):
        # Starports A, B contain naval bases on 8+.
    navy = False
    if self.starport in ['A', 'B'] and roll(2) > 7:
        navy = True

    # Starports A, B, C, and D contain scout bases on 7+, with a penalty
    # inversely related to port quality.
    scout = False
    if self.starport == 'A' and roll(2) > 9:
        scout = True
    elif self.starport == 'B' and roll(2) > 8:
        scout = True
    elif self.starport == 'C' and roll(2) > 7:
        scout = True
    elif self.starport == 'D' and roll(2) > 6:
        scout = True

    # Determine base code
    if navy and scout == True:
        return 'B'
    elif navy == True:
        return 'N'
    elif scout == True:
        return 'S'
    else:
        return ' '

