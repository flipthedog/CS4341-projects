# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')
sys.path.insert(1, '../Scenario2Characters')
from finitestatecharacterfinalS2 import FiniteStateCharacter



# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(FiniteStateCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go()
