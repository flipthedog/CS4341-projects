# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
sys.path.insert(1, '../Scenario1Characters')
from finitestatecharacterV5Ex2 import FiniteStateCharacter

# Create the game
random.seed(12) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("monster", # name
                                    "A",       # avatar
                                    3, 13,     # position
                                    2          # detection range
))

# TODO Add your character
g.add_character(FiniteStateCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go()