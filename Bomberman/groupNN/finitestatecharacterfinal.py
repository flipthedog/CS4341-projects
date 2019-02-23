# This is necessary to find the main code
import sys
import pathfinding as greedyBFS
import pathfinding4conn as conn4
import expectimaxV4 as EM

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
#
# We need to:
# 1) Figure out how to widen paths
# 2) Improve bomb avoidance so that it's not hardcoded
# 3) Deal with bombs and explosions in expectiMax
# 4) Higher level algorithms


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

        # True if there is at least 1 monster within 5 steps
        isThereMonster = self.isThereMonster(wrld, meX, meY)

        # A list of bombs if there are bombs on the board, empty otherwise
        isThereBomb = self.isThereBomb(wrld, meX, meY)

        # A list of explosions if there is at least 1 explosion within 2 steps, empty otherwise
        isThereExplosion = self.isThereExplosion(wrld, meX, meY)

        if isThereBomb and isThereMonster and isThereExplosion:
            # There at least 1 bomb, 1 monster, and 1 explosion within the danger zone
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb and isThereMonster:
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb and isThereExplosion:
            # There is both at least 1 bomb and 1 explosion within 2 steps
            self.move(-1,-1)
        elif isThereExplosion and isThereMonster:
            # There is both at least 1 explosion and 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb:
            self.move(-1,-1)
            # There is at least 1 bomb within 2 steps
            # self.greedy(wrld, exit, meX, meY)
        elif isThereExplosion:
            self.move(-1,-1)
            # There is at least 1 explosion within 2 steps
            # TODO: eliminate this case, handle in greedy
            # self.greedy(wrld, exit, meX, meY)
        else:
            # There is no danger nearby
            self.greedy(wrld, exit, meX, meY)



    def MoveDist(self, start, end):
        return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

    def isThereBomb(self, wrld, meX, meY):
        bmbs = []
        # List of bombs across the entire board
        bombs = wrld.bombs.items()

        for x,bmb in bombs:
            bmbs.append(bmb)
        return bmbs

    def isThereExplosion(self, wrld, meX, meY):
        # Returns all of the close explosions
        exps = []

        # All of the explosions
        e = wrld.explosions.items()

        # Filtering only close monsters
        for x,exp in e:
            if self.MoveDist([meX, meY], [exp.x, exp.y]) <= 1:
                exps.append(exp)

        return exps


    def isThereMonster(self, wrld, meX, meY):
            # All of the monsters
            m = wrld.monsters.items()

            # Filtering only close monsters
            for x,monstr in m:
                ms = monstr
                for ms in monstr:
                    if self.MoveDist([meX, meY], [ms.x, ms.y]) <= 3:
                        return True
                return False

    def expectimax(self, wrld, exit, meX, meY):
        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = EM.expectiMax(wrld, 1)

        # move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])


    def greedy(self, wrld, exit, meX, meY):
        # Returns true if the character can be moved, false if not

        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)

        if goTo is None:
            # TODO: Improve bomb placement and pathfinding combinations
            goTo = conn4.getNextStep([meX, meY], exit, wrld)
            if wrld.wall_at(goTo[0],goTo[1]):
                self.place_bomb()
            else:
                self.move(-meX + goTo[0], -meY + goTo[1])
        else:
            #move in direction to get to x,y found in prev step
            self.move(-meX + goTo[0], -meY + goTo[1])
