

#expectiMax(World, Character, MonsterList, [int xf, int yf], int)-> [int xOp, int yOp]
#Given a world, ticked for any bombs, a character, a monsterlist of size 1 or 2 (as there is a max of 2 monsters)
#a positional tuple of the exit, and the max depth to reach. The depth will early exit in the case of succsess (reaching
#the exit) and failure (death)
def expectiMax(wrld, c, Mlist=0, Exit=0, Depth=0):

    for i in range(15000):
        wrld.next()
        # OpMonster(0,0,0)
        # OpChar(0,0)
    return [0,0]


#a version of the monster that is optimized for expectimax
#takes an x,y position and a range for attack
class OpMonster:

    def __init__(self, x, y, range):
        self.x = x
        self.y = y
        self.range = range


class OpChar:

    def __init__(self, x, y):
        self.x = x
        self.y = y