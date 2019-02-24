import sys
import time
import pathfinding as greedyBFS
#############################################################################################
#expectiMax(World, Character, MonsterList, [int xf, int yf], int)-> [int xOp, int yOp]
#Given a world, ticked for any bombs, a character, a monsterlist of size 1 or 2 (as there is a max of 2 monsters)
#a positional tuple of the exit, and the max depth to reach. The depth will early exit in the case of succsess (reaching
#the exit) and failure (death)
def expectiMax(wrld, Exit, Depth, CostLookup):
  #________________________________________________________________________________#
    #Set up charicter placement, converting charicters to optimized charicters
    Mlist = []
    t = time.time()
    for monList in wrld.monsters.values():
        for mon in monList:
            Mlist.append(mon)
    cExt = next(iter(wrld.characters.values()))[0]


    c = OpChar(cExt.x, cExt.y)
    m1 = None
    m2 = None

    if len(Mlist)==0:
        raise Exception('Trying to use expectimax with no monster')
    else:

        try:
            rnge = Mlist[0].rnge
        except:
            rnge = 2
        m1 = OpMonster(Mlist[0].x, Mlist[0].y, rnge)


        if len(Mlist)>=2:

            try:
                rnge = Mlist[1].rnge
            except:
                rnge = 0
            m2 = OpMonster(Mlist[1].x, Mlist[1].y, rnge)


  #________________________________________________________________________________#
    #tick the world once for bombs, then generate all possible lists of movements
    #generate all worlds at begining, so it doesn't have to be constantly recreated
    wrld.character = {}
    wrldList = []
    for i in range(Depth+2):

        (newwrld, events) = wrld.next()
        wrldList.append(newwrld)

    cList = find_actions_OpObj(wrldList[0], c)
    m1List = find_actions_monster(wrldList[0], m1, c, Depth)
    m2List = find_actions_monster(wrldList[0], m2, c, Depth)


  #________________________________________________________________________________#
    #for every action possible, make a move then choose arg max

    BestAction = [-(sys.maxsize - 1), c]


    for char in cList:
        v = 0
        for mon in m2List:
            v += expVal(wrldList[1:], mon, char, Exit, 0, Depth, CostLookup)

        for mon in m1List:
            v += expVal(wrldList[1:], mon, char, Exit, 0, Depth, CostLookup)

        if v > BestAction[0]:
            BestAction = [v, char]

    #extract the char's movement
    print("time:", time.time()-t)

    return [BestAction[1].x, BestAction[1].y]


#############################################################################################
#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def expVal(wrldList, m, c, Exit, D, DMax, CostLookup):

    if D == DMax or ((m is not None) and moveDist(m,c)<=1) or (m is None):
        return cost(wrldList[0], m, c, Exit, D, DMax)

    v=0

    cList = find_actions_OpObj(wrldList[0], c)
    mList = find_actions_monster(wrldList[0], m, c, DMax - D)


    for mon in mList:
        for char in cList:
            p = 1/(len(mList) + len(cList))
            v = v + p * maxVal(wrldList[1:], mon, char, Exit, D + 1, DMax, CostLookup)

    return v


#############################################################################################
#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def maxVal(wrldList, m, c, Exit, D, DMax, CostLookup):

    if D == DMax or ((m is not None) and moveDist(m, c) <= 1) or (m is None):
        return cost(wrldList[0], m, c, Exit, D, DMax)

    v = -(sys.maxsize - 1)

    cList = find_actions_OpObj(wrldList[0], c)
    mList = find_actions_monster(wrldList[0], m, c, DMax - D)

    for mon in mList:
        for char in cList:
            v = max(v, expVal(wrldList[1:], mon, char, Exit, D + 1, DMax, CostLookup))

    return v


#############################################################################################
#moveDist(OpMonster, OpChar)-> int
#returns the number of movements (disreguarding walls) needed to hit the charicter
def moveDist(m, c):
    return abs(m.x - c.x)+ abs(m.y - c.y)


#############################################################################################
#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def cost(wrld, m, c, Exit, D, DMax):

    cost = 0
    #cost += - .5*max(abs(Exit[0] - c.x), abs(Exit[0] - c.y))
    # Elen = greedyBFS.getPathLen([c.x, c.y], Exit, wrld)
    # if Elen is not None:
    #     cost += -Elen*.5

  # ________________________________________________________________________________#
    #set Monster cost, trigger high value for death, and early death

    if m is not None:
        if moveDist(m, c) <= 1:
            return -100**(DMax+2-D)

        cost += - 5 ** (4 - moveDist(m, c)) - 100 ** (8 - len(find_actions_OpObj(wrld, c)))


  # ________________________________________________________________________________#
    #if at the exit w/o death, nice, choose this
    if c.x == Exit[0] and c.y == Exit[1]:
        return 1

    return cost


#############################################################################################
#find_actions_monster(World, OpMonster, OpChar, Int)-> List[OpMonster]
#given the world, a monster, and a charicter, returns a list of monster objects in all new positions
#if close to the charicter, the only move is towards the char
#if further than 2*depth+1, then the char is too far for any movements to afftect the charicter
def find_actions_monster(wrld, m, c, DMax):
    if m is None:
        return [None]

    actions = []

    #if its in range, the monster walks at the charicter
    if moveDist(m,c) <= m.rnge:
        actions.append(OpMonster(m.x + (c.x - m.x), m.y + (c.y - m.y), m.rnge))

    #if too far away to kill the charicter in depth number of moves, then the monster should be ignored.
    #TODO make sure this doesn't cause problems
    elif moveDist(m,c) > DMax*2+1:
        return [None]

    # otherwise it moves randomly into a new safe space
    else:
        # check 8 connected for walls and out of bounds.
        actions = find_actions_OpObj(wrld, m)
        for Mon in actions:
            Mon.rnge = m.rnge

    return actions


#############################################################################################
# find_actions_Char(World, OpObj)-> List[OpChar]
# given the world and a charicter, returns a list of Charicter objects in all new positions
def find_actions_OpObj(wrld, OpObj):
    actions = []

    width = wrld.width()
    height = wrld.height()

    # check 8 connected for walls and out of bounds.
    for i in range(3):

        i -= 1

        for j in range(3):

            j -= 1

            if not (OpObj.x + i >= width or OpObj.x + i < 0 or OpObj.y + j >= height or OpObj.y + j < 0):

                if not (wrld.wall_at(OpObj.x + i, OpObj.y + j)) and not wrld.explosion_at(OpObj.x + i, OpObj.y + j):

                    if isinstance(OpObj, OpChar):
                        actions.append(OpChar(OpObj.x + i, OpObj.y + j))
                    elif (not (i == 0 and j == 0)):
                        actions.append(OpMonster(OpObj.x + i, OpObj.y + j))

    return actions


#############################################################################################
#a version of the monster that is optimized for expectimax
#takes an x,y position and a range for attack
class OpMonster:

    def __init__(self, x, y, rnge= 0):
        self.x = x
        self.y = y
        self.rnge = rnge


#x and y position
class OpChar:

    def __init__(self, x, y):
        self.x = x
        self.y = y

#############################################################################################