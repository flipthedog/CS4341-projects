# This is necessary to find the main code
import sys
import pathfinding as greedyBFS
import pathfinding4conn as conn4
import ExpectimaxOptimized as EM

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
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.ticked = False


    def do(self, wrld):
        print("doing")
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
        # elif isThereBomb and isThereExplosion:
        #     # There is both at least 1 bomb and 1 explosion within 2 steps
        #     self.avoidanceNoMster(wrld, exit, meX, meY, isThereBomb, isThereExplosion)
        elif isThereExplosion and isThereMonster:
            # There is both at least 1 explosion and 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY, False)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb:
            self.expectimax(wrld, exit, meX, meY)
        #     # There is at least 1 bomb within 2 steps
        #     self.avoidanceNoMster(wrld, exit, meX, meY, isThereBomb, isThereExplosion)
        elif isThereExplosion:
            self.expectimax(wrld, exit, meX, meY, False)
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
            m = wrld.monsters.values()

            # Filtering only close monsters
            for monstr in m:
                for ms in monstr:
                    if self.MoveDist([meX, meY], [ms.x, ms.y]) <= 2:
                        return True
                return False

    def expectimax(self, wrld, exit, meX, meY, TickForwards = True):
        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = EM.expectiMax(wrld, exit, 2, TickForwards)
        if  goTo[0] == exit[0] and goTo[1] == exit[1]:
            raise ValueError
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
            if goTo[0] == exit[0] and goTo[1] == exit[1]:
                raise ValueError
            if wrld.wall_at(goTo[0],goTo[1]):
                self.place_bomb()
            else:
                self.move(-meX + goTo[0], -meY + goTo[1])
        else:
            if goTo[0] == exit[0] and goTo[1] == exit[1]:
                raise ValueError
            #move in direction to get to x,y found in prev step
            self.move(-meX + goTo[0], -meY + goTo[1])

    def bombAvoidanceNoMster(self, wrld, meX, meY):
        # Get the bomb object
        thisBomb = next(iter(wrld.bombs.values()))[0]

        # Figure out the amount of time left on the bomb before it explodes
        timeLeft = thisBomb.timer
        # Figure out how far the explosion will reach when it occurs
        bRange = wrld.expl_range
        # Figure out how far away from the explosion you are using euclidean distance
        manhattan = meX-thisBomb.x+ meY-thisBomb.y
        # Figure if on the same x or y as the bomb
        horz = False
        if bomb.x == meX:
            horz = True
        vert = False
        if bomb.y = meY:
            vert = True
        if manhattan <= bRange and straightShot:
            # then you are still within the range of the bomb

            # Figure out how much further you'd have to move to be out of the range of the bomb
            howMuchFurther = bRange - euclid
            if timeLeft <= howMuchFurther:
                # if you can't escape it in time by going straight, see if you can go diagonally
                #TODO: fill in
                pass
            else:
                # continue running away in the same direction
                #TODO: fill in
                pass
        else:
            # Don't move into the path 
