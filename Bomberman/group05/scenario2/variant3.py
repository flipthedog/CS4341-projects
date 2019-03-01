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
sys.path.insert(1, '../Scenario2Characters')
from finitestatecharacterfinalS2 import FiniteStateCharacter

wins = 0

for i in range(10):

    # Create the game
    random.seed(i) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("monster", # name
                                        "M",       # avatar
                                        3, 9,      # position
                                        1          # detection range
    ))

    # TODO Add your character
    g.add_character(FiniteStateCharacter("me", # name
                                  "C",  # avatar
                                  0, 0  # position
    ))

    # Run!
    try:
        g.go()
    except ValueError:
        wins += 1

print(wins)