# This is necessary to find the main code
import sys
import pathfinding as greedyBFS
import expectimaxV5 as EM

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class FiniteStateCharacter(CharacterEntity):

    #TODO:

    # State machine:
        # Check for Danger:

        # Danger:
        # Expectimax to avoid monsters
        # Remove explosion cells
        # Remove dangerous bomb cells

        # No Danger:
        # 1. Perform greedyBFS
        # 2. If no path: 4 connected, A* to place a bomb
        # 3. If path: Walk

    def do(self, wrld):
        # This method calls different algorithms to find the next position to
        # move based on the finite state the character is in.

        # Find the exit to move towards
        exit = self.get_exit(wrld)

        #get current position
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        dangers = self.check_danger(meX, meY, wrld)

        # Check if there are dangers
        if dangers != [-1]:
            # There are dangers
            dangerous_bombs = dangers[1]
            dangerous_monsters = dangers[0]
            dangerous_explosions = dangers[2]
        else:
            # There are no dangers

            # Try and move
            if not self.move(wrld, exit, meX, meY):
                # We didn't move, so let's do some bomb placement
                self.blocked_move(wrld, exit, meX, meY)


    def blocked_move(self, wrld, exit, meX, meY):
        pass

    def move(self, wrld, exit, meX, meY):

        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)

        if goTo != None:

            # move in direction to get to x,y found in prev step
            self.move(-meX + goTo[0], -meY + goTo[1])

            return True

        else:

            return False

    # check_danger()
    # Find all the dangers that are actually dangerous, and return them
    # Input: meX = me x
    # Input: meY = me y
    # Input: wrld: world object
    # Return: Array of dangers [monsters, bombs, explosion cells] or [-1] for no danger
    def check_danger(self, wrld, meX, meY, monster_range = 5, bomb_range = 4, explosion_range = 1):

        danger_monsters = self.find_dangerous_monsters(wrld, meX, meY, monster_range)

        danger_bombs = self.find_dangerous_bombs(wrld, meX, meY, bomb_range)

        danger_explosion = self.find_dangerous_explosions(wrld, meX, meY, explosion_range)

        if len(danger_monsters) < 1 and len(danger_bombs) < 1 and len(danger_explosion) < 1:
            return [-1]

        # Return Array:
        # 1. Array of Monsters
        # 2. Array of bombs
        # 3. Dangerous explosion cells
        return [danger_monsters, danger_bombs, danger_explosion]


    # get_exit()
    # Find the exit in wrld, and return it
    # Input: current wrld object
    # Output: array exit [x, y]
    def get_exit(self, wrld):

        exit = [0, 0]

        #check every gridcell for the exit. Uses the last exit found as the "goal"
        for i in range(wrld.width()):

            for j in range(wrld.height()):

                if wrld.exit_at(i, j):
                    exit = [i, j]

        return exit

    # Find the manhattan distance to a spot
    def MoveDist(self, start, end):
        return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

    # find_dangerous_monsters()
    # Search the area for all the dangerous monsters
    # Input: wrld: world object
    # Input: meX: me x
    # Input: meY: me y
    # Input: search_range: How far away are the monsters dangerous
    # Return: Array of monsters that are the dangerous monsters
    def find_dangerous_monsters(self, wrld, meX, meY, search_range = 3):

        returnArr = []

        for m in wrld.monsters.values():

            if self.MoveDist([meX, meY], [m.x, m.y]) <= search_range:
                returnArr.append(m)

        return returnArr

    # find_dangerous_bombs()
    # Input: wrld: world object
    # Input: meX: me x
    # Input: meY: me y
    # Input: bomb_range
    # Return: Array of bomb entities that are the dangerous
    def find_dangerous_bombs(selfs, wrld, meX, meY, bomb_range = 3):

        bombs = []

        # Check the 4 directions
        for i in range(-1, 1):

            for j in range(-1, 1):

                # Filter out diagonals
                if i == 0 or j == 0 :

                    # Check to the bomb range
                    for k in range(0, bomb_range):
                        possible_bomb = wrld.bomb_at(meX + bomb_range * i, meY + bomb_range * j)

                        # Add the bomb if there
                        if possible_bomb:
                            bombs.append(possible_bomb)

        # Return all the bombs
        return bombs

    # find_dangerous_explosions()
    # Return the dangerous explosions within a range (DEFAULT = 1)
    # Input: wrld: world object
    # Input: meX: me x
    # Input: meY: me y
    # Input: check_range: range to check for dangerous explosions
    # Return: Array of explosion entities that are dangerous
    def find_dangerous_explosions(self, wrld, meX, meY, check_range = 1):

        dangerous_explosions = []

        for i in range(-1, 1):

            for j in range(-1, 1):

                for k in range(0, check_range):

                    possible_explosion = wrld.explosion_at(meX + i * check_range, meY + j * check_range)
                    if possible_explosion:

                        dangerous_explosions.append(possible_explosion)

        return dangerous_explosions

    def checkPerimeter2(self, wrld, meX, meY):
        # Check the perimeter around the character at a depth of 2 for any other
        # objects, return a list of lists [typeNum, x, y] that represents anything
        # found

        # TypeNum represents each type of object as follows:
        # 0 = wall
        # 1 = bomb
        # 2 = monster
        # 3 = explosion

        # Does not currently detect other characters or exit, but can be made to

        # The list to be returned
        closeObjects = []

        # Go through each space in the box around the character
        for i in range(-2,2):
            for j in range(-2,2):
                # if this is not the space the character is in
                if i != 0 and j != 0:
                    # if the postition is in world bounds
                    if not meX + i >= wrld.width() and meX + i <= 0 and meY + j >= wrld.height() and meY + j <= 0:
                        # check if there is a wall there and append if so
                        if wrld.wall_at(meX + i, meY + j):
                            closeObjects.append([0, meX + i, meY + j])
                        # check if there is a bomb there and append if so
                        elif wrld.bomb_at(meX + i, meY + j):
                            closeObjects.append([1, meX + i, meY + j])
                        # check if there is a monster(s) there and append if so
                        elif wrld.monsters_at(meX + i, meY + j):
                            closeObjects.append([2, meX + i, meY + j])
                        # check if there is an explosion there and append if so
                        elif wrld.explosion_at(meX + i, meY + j):
                            closeObjects.append([3, meX + i, meY + j])

        return closeObjects

    def isThereBomb(self, closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is a bomb nearby
        isThereBomb = False

        # Extract all the bombs
        bmbs = [item for item in closeObjects if item[0] == 1]

        # If there are bombs, set isThereBomb to True
        if len(bmbs):
            isThereBomb = True

        return isThereBomb

    def isThereWall(self, closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is a wall nearby
        isThereWall = False

        # Extract all the bombs
        wlls = [item for item in closeObjects if item[0] == 0]

        # If there are bombs, set isThereWall to True
        if len(wlls):
            isThereWall = True

        return isThereWall

    def isThereMonster(self, closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is a wall nearby
        isThereMonster = False

        # Extract all the bombs
        mnstrs = [item for item in closeObjects if item[0] == 2]

        # If there are bombs, set isThereMonster to True
        if len(mnstrs):
            isThereMonster = True

        return isThereMonster

    def isThereExplosion(self, closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is an explosion nearby
        isThereExplosion = False

        # Extract all the bombs
        exps = [item for item in closeObjects if item[0] == 3]

        # If there are bombs, set isThereExplosion to True
        if len(exps):
            isThereExplosion = True

        return isThereExplosion

    def expectimax(self, wrld, exit, meX, meY):
        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = EM.exptectiMax(wrld, 2)

        # move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])
