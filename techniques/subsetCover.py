from grid import Grid
from colours import tCol
from itertools import chain, combinations

# Uses subset cover inconsistencies to eliminate values.
def subsetCover(g):
    g, success = columnSetCover(g)
    if (success): return g, success
    g.transpose()
    g, success = columnSetCover(g)
    g.transpose()
    if (success): return g, success
    g, success = sectorSetCover(g)
    return g, success

# Returns the structure name for a given k.
def getSetCoverName(newValid, oldValid):
    if (len(newValid) + 2 == len(oldValid)):
        return "Subset Cover Pairs"
    elif (len(newValid) + 3 == len(oldValid)):
        return "Subset Cover Triples"
    elif (len(newValid) + 4 == len(oldValid)):
        return "Subset Cover Quads"
    else:
        return "Set Cover Inconsistency"
          
# Sector Set Cover.
def sectorSetCover(g):
    for x, y in g.unfilledCells():
        # Sector Midpoint.
        cx, cy = g.getSectorCoord(x,y)
        available = []
        # Compare sector cells.
        for i, j in g.sectorCells():
            if ((cx + i != x or cy + j != y) and g.get(cx+i, cy+j) == 0):
                available.append([cx + i, cy + j])
        # Requires at least 1 other empty cell.
        if (len(available) > 1):
            perm = list(chain.from_iterable(combinations(available, r) for r in range(1, len(available) + 1)))
            for k in range(len(perm)):
                combo = perm[k]
                empty = len(combo)
                valid = set()
                for m in range(len(combo)):
                    valid.update(g.getValid(combo[m][0], combo[m][1]))
                # Checks for set cover inconsistencies.
                if (empty > 0 and empty == len(valid)):
                    oldValid = g.getValid(x,y)
                    newValid = oldValid - valid
                    # Checks if valid states have changed.
                    if (newValid != oldValid):
                        g.updateCellValid(x,y,newValid)
                        g.logMove(0, tCol.HEADER + getSetCoverName(newValid, oldValid) + tCol.ENDC + " - Reduced cell " + tCol.OKBLUE + "(" + str(x+1) + "," + str(y+1) + ")" + tCol.ENDC + " from " + tCol.WARNING + str(oldValid) + tCol.ENDC + " to " + tCol.WARNING + str(newValid) + tCol.ENDC)
                        print(valid)###
                        return g, True
    return g, False

# Column Set Cover.
def columnSetCover(g):
    for x, y in g.unfilledCells():
        available = []
        # Compare column cells.
        for j in range(g.size):
            if (j != y and g.get(x,j) == 0):
                available.append([x,j])
        # Requires at least 1 other empty cell.
        if (len(available) > 1):
            perm = list(chain.from_iterable(combinations(available, r) for r in range(1, len(available) + 1)))
            for k in range(len(perm)):
                combo = perm[k]
                empty = len(combo)
                valid = set()
                for m in range(len(combo)):
                    valid.update(g.getValid(combo[m][0], combo[m][1]))
                # Checks for set cover inconsistencies.
                if (empty > 0 and empty == len(valid)):
                    oldValid = g.getValid(x,y)
                    newValid = oldValid - valid
                    # Checks if valid states have changed.
                    if (newValid != oldValid):
                        g.updateCellValid(x,y,newValid)
                        g.logMove(0, tCol.HEADER + getSetCoverName(newValid, oldValid) + tCol.ENDC + " - Reduced cell " + tCol.OKBLUE + "(" + str(x+1) + "," + str(y+1) + ")" + tCol.ENDC + " from " + tCol.WARNING + str(oldValid) + tCol.ENDC + " to " + tCol.WARNING + str(newValid) + tCol.ENDC)
                        return g, True
    return g, False