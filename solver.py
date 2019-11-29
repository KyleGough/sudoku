from generator import easyGridTest, intermediateGridTest, difficultGridTest
from generator import xwingGridTest, swordfishGridTest
from grid import Grid
from itertools import chain, combinations

# Checks conflicts in a row.
def checkRow(g, y):
    perm = set()
    for x in range(g.size):
        perm.add(g.get(x,y))
    return perm

# Checks conflicts in a column.
def checkColumn(g, x):
    perm = set()
    for y in range(g.size):
        perm.add(g.get(x,y))
    return perm

# Checks conflicts in a 3x3 sector.
def checkSector(g, x, y):
    perm = set()
    cx, cy = g.getSectorCoord(x,y)
    for i, j in g.sectorCells():
        perm.add(g.get(cx + i,cy + j))
    return perm

# Checks all conflicts for a given cell.
def checkCell(g, x, y):
    # Conflicting values.
    conflicts = checkRow(g, y)
    conflicts.update(checkColumn(g, x))
    conflicts.update(checkSector(g, x, y))
    # Possibilities.
    return {1,2,3,4,5,6,7,8,9} - conflicts

# Heuristic 1 - Uses solo candidate and unique candidate technques.
def h1(g):
    # Iterate over each non-filled cell.
    for x, y in g.unfilledCells():
        valid = g.getValid(x,y)
        # Check for a single possibility.
        if (len(valid) == 1):
            value = valid.pop()
            # Add value into grid.
            g.insert(x,y,value)
            print(value, "- in cell ", x+1, y+1, "due to ruleset. [H1]")
            return g, True
    return g, False

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
                        print("Sector set cover inconsistency in cell", x+1, y+1, "from", oldValid, "to", newValid, "[H2]")
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
                        print("Column set cover inconsistency in cell", x+1, y+1, "from", oldValid, "to", newValid, "[H2]")
                        return g, True
    return g, False

# Row Set Cover.
def rowSetCover(g):
    for x, y in g.unfilledCells():
        available = []
        # Compare row cells.
        for i in range(g.size):
            if (i != x and g.get(i,y) == 0):
                available.append([i,y])
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
                        print("Row set cover inconsistency in cell", x+1, y+1, "from", oldValid, "to", newValid, "[H2]")
                        return g, True
    return g, False

#
def h2(g):
    g, success = rowSetCover(g)
    if (success): return g, success
    g, success = columnSetCover(g)
    if (success): return g, success
    g, success = sectorSetCover(g)
    return g, success

#
# Structure for example could be: X-Wing, Swordfish, Jellyfish, etc.
def xwing(g, k):
    # Row candidates for X-Wing.
    candidates = set()
    candidateColumns = []

    # Iterate over rows.
    for y in range(g.size):
        # Count empty cells in the row.
        empty = 0
        columns = set()
        for x in range(g.size):
            if (g.get(x,y) == 0):
                empty += 1
                columns.add(x)
        # Add as X-Wing candidate.
        if (empty == k):
            candidates.add(y)
            candidateColumns.append(columns)

    print(candidates)
    print(candidateColumns)

    ys = candidates
    if (len(ys) == k):
        xs = candidateColumns[0]
        count = candidateColumns.count(xs)
        if (count == len(candidateColumns)):######
            # Possible values that can occupy all cells of the structure.
            candidateValues = {1,2,3,4,5,6,7,8,9}
            for a in xs:
                for b in ys:
                    candidateValues = candidateValues.intersection(g.getValid(a,b))
            if (len(candidateValues) == 1):
                print("X-Wing found.")
                g, success = xwingExecute(g, xs, ys, k, candidateValues.pop())
                return g, success
            
    return g, False
#
def xwingExecute(g, xs, ys, k, n):

    for y in range(g.size):
        for x in xs:
            if (not y in ys):
                valid = g.getValid(x,y)
                # Updates valid values conflicting with the X-Wing.
                print("Cell ", x, y, "removed possibility of ", n, "due to X-Wing")                
                valid.discard(n)
                g.updateCellValid(x,y,valid)
    return g, True

# Updates the valid cells for every cell on the board.
def updateAllValid(g):
    for x, y in g.unfilledCells():
        poss = checkCell(g, x, y)
        g.updateCellValid(x, y, poss)
    return g

#
def strategicSolver(g):
    found = True
    move = 0

    while (found):
        print("[ MOVE", move, "]")
        g.printClean()
        move += 1
        
        # Heuristic 1.
        found = False
        g, found = h1(g)
        if (found):
            continue
        if (g.error):
            print("Heuristic 1 failed.")
            return g, False

        # Heuristic 2.
        found = False
        g, found = h2(g)
        if (found):
            continue
        if (g.error):
            print("Heuristic 2 failed.")
            return g, False

        # X-Wing.
        found = False
        g, found = xwing(g, 2)
        if (found):
            continue
        if (g.error):
            print("X-Wing failed.")
            return g, False

        # Swordfish.
        found = False
        g, found = xwing(g, 3)
        if (found):
            continue
        if (g.error):
            print("Swordfish failed.")
            return g, False

        # Exhausted Possibilities.
        print("Exhausted Search. [EX]")

    return g, True


if __name__ == "__main__":
    g = easyGridTest()
    g = intermediateGridTest()
    g = difficultGridTest()
    g = xwingGridTest()
    g = swordfishGridTest()

    g = updateAllValid(g)
    g = strategicSolver(g)    


    #X-wing
    #Swordfish