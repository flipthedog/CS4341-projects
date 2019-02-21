# This is necessary to find the main code
import sys
import pathfinding as greedyBFS

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class FiniteStateCharacter(CharacterEntity):

    def do(self, wrld):
        # This method calls different algorithms to find the next position to
        # move based on the finite state the character is in.

        # Find the exit to move towards
        exit = [0, 0]

        #check every gridcell for the exit. Uses the last exit found as the "goal"
        for i in range(wrld.width()):

            for j in range(wrld.height()):

                if wrld.exit_at(i, j):
                    exit = [i, j]

        #get current position
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        # A list of objects within the perimeter of 2 spaces
        closeObjects = self.checkPerimeter2(wrld, meX, meY)
        # True if there is an impassable wall within 1 space,
        # False otherwise
        isThereWall = self.impassableWall(wrld, meX, meY)
        # True if there is at least 1 bomb within a + shaped area
        isThereBomb = self.isThereBomb(wrld, meX, meY)
        # True if there is at least 1 monster within 2 steps
        isThereMonster = self.isThereMonster(wrld, meX, meY)
        # True if there is at least 1 explosion within 2 steps
        isThereExplosion = self.isThereExplosion(closeObjects)

        if not closeObjects and not isThereWall:
            # Character is alone and able to push forward unimpeded by wall
            self.greedy(wrld, exit, meX, meY)
        elif not closeObjects and isThereWall:
            # Character is alone but there is a wall impeding movement
            self.greedy(wrld, exit, meX, meY)
        elif isThereBomb and isThereMonster and isThereExplosion:
            # There at least 1 bomb, 1 monster, and 1 explosion within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereBomb and isThereMonster:
            # There is both at least 1 bomb and 1 monster within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereBomb and isThereExplosion:
            # There is both at least 1 bomb and 1 explosion within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereExplosion and isThereMonster:
            # There is both at least 1 explosion and 1 monster within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereBomb:
            # There is at least 1 bomb within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereExplosion:
            # There is at least 1 explosion within 2 steps
            self.greedy(wrld, exit, meX, meY)
        else:
            # there should be nothing left, if anything gets to this point,
            # fix it
            self.greedy(wrld, exit, meX, meY)

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

    def impassableWall(self, wrld, meX, meY):
        # Check to see if there is an impassable wall a step ahead of the
        # character

        # Note: checks for horizontal wall below or vertical wall to the right
        # but can be edited to check less or more

        # Note: can also be changed to be closer or farther away from wall

        isThereWall = False

        # Check all positions from left to right in 'front' of the character (if possible)
        if meY < wrld.height() - 1:
            for i in range(wrld.width()):
                isThereWall = isThereWall or wrld.wall_at(i, meY + 1)

        # Check all positions from top to bottom to the 'right' of the character (if possible)
        if meX < wrld.width() - 1:
            for j in range(wrld.height()):
                isThereWall = isThereWall or wrld.wall_at(meX + 1, j)

        return isThereWall

    def isThereBomb(self, wrld, meX, meY):
        # Go through each space in the box around the character
        for i in range(-wrld.expl_range, -1):
            # if the postition is in world bounds
            if not meX + i >= wrld.width() and meX + i <= 0:
                # check if there is a bomb there and append if so
                if wrld.bomb_at(meX + i, meY):
                    return True
            if not meY + i >= wrld.height() and meY + i <= 0:
                # check if there is a bomb there and append if so
                if wrld.bomb_at(meX, meY + i):
                    return True

        # Go through each space in the box around the character
        for j in range(1, wrld.expl_range):
            # if the postition is in world bounds
            if not meX + j >= wrld.width() and meX + j <= 0:
                # check if there is a bomb there and append if so
                if wrld.bomb_at(meX + j, meY):
                    return True
            if not meY + j >= wrld.height() and meY + j <= 0:
                # check if there is a bomb there and append if so
                if wrld.bomb_at(meX, meY + j):
                    return True



    def isThereMonster(self, wrld, meX, meY):
        # Go through each space in the box around the character
        for i in range(-2,2):
            for j in range(-2,2):
                # if this is not the space the character is in
                if i != 0 and j != 0:
                    # if the postition is in world bounds
                    if not meX + i >= wrld.width() and meX + i <= 0 and meY + j >= wrld.height() and meY + j <= 0:
                        # if there is a monster within the bounds, return true
                        if wrld.monsters_at(meX + i, meY + j):
                            return True
        # If a monster hasn't been found, return false
        return False

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

    def greedy(self, wrld, exit, meX, meY):
        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)

        #move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])
