from grid import Grid
from colours import tCol
from itertools import chain

# O(x * y)
def bivalueUniversalGrave(g):
    success = False
    foundTriple = False

    # Detects a Bivalue Universal Grave.
    for x in range(g.size):
        for y in range(g.size):
            valid = g.getValid(x,y)
            if (len(valid) == 0):
                continue
            elif (len(valid) == 2):
                continue
            elif (len(valid) == 3 and foundTriple == False):
                foundTriple = True
                bugCell = tuple([x,y])
            else:
                return False

    # Bivalue Universal Grave must contain exactly one triple candidate.    
    if (not foundTriple):
        return False

    # Reduces the Bivalue Universal Grave.
    for n in g.getValid(bugCell[0], bugCell[1]):
        success = success or bugReduce(g, {n}, bugCell)

    return success

#
def bugReduce(g, n, bugCell):

    # Check column.
    candidateList = []
    for y in range(g.size):
        valid = g.getValid(bugCell[0], y)
        if (y == bugCell[1]):
            valid = valid.difference(n)
        candidateList.append(list(valid))
    # Flattens the list.
    candidateList = list(chain.from_iterable(candidateList))
    # Checks candidates either do not appear or appear exactly twice.
    for i in range(1,10):
        occurences = candidateList.count(i)
        if (occurences != 0 and occurences != 2):
            return False

    # Check row.
    candidateList = []
    for x in range(g.size):
        valid = g.getValid(x, bugCell[1])
        if (x == bugCell[0]):
            valid = valid.difference(n)
        candidateList.append(list(valid))
    # Flattens the list.
    candidateList = list(chain.from_iterable(candidateList))
    # Checks candidates either do not appear or appear exactly twice.
    for i in range(1,10):
        occurences = candidateList.count(i)
        if (occurences != 0 and occurences != 2):
            return False

    # Check sector.
    candidateList = []
    cx, cy = g.getSectorCoord(bugCell[0], bugCell[1])
    for i,j in g.sectorCells():
        valid = g.getValid(cx + i, cy + j)
        if (bugCell[0] == cx + i and bugCell[1] == cy + j):    
            valid = valid.difference(n)
        candidateList.append(list(valid))
    # Flattens the list.
    candidateList = list(chain.from_iterable(candidateList))
    # Checks candidates either do not appear or appear exactly twice.
    for i in range(1,10):
        occurences = candidateList.count(i)
        if (occurences != 0 and occurences != 2):
            return False
        
    # Sets the value of the cell as it doesn't yield a deadly pattern.
    n = n.pop()
    msg = tCol.header("BUG:") + " Set cell "
    msg += g.printCell(bugCell[0], bugCell[1]) + " to " + tCol.okblue(str(n))
    msg += " as candidates " + g.printSet(g.getValid(bugCell[0], bugCell[1]).difference({n}))
    msg += " yield multiple solutions"
    g.insert(bugCell[0], bugCell[1], n)
    g.logMove(msg)
    return True 
