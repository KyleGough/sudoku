import sys
from generator import easyGridTest, intermediateGridTest, difficultGridTest
from generator import xwingGridTest, swordfishGridTest, jellyfishGridTest
from grid import Grid
from itertools import chain, combinations
from colours import tCol

# Gets the structure name for a given k.
def getStructureName(k):
    if (k == 2):
        return "X-Wing"
    elif (k == 3):
        return "Swordfish"
    elif (k == 4):
        return "Jellyfish"
    else:
        return "NONE"

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

# Solo Candidate - Where a cell has only one possibility.
def soloCandidate(g):
    # Iterate over each non-filled cell.
    for x, y in g.unfilledCells():
        valid = g.getValid(x,y)
        # Check for a single possibility.
        if (len(valid) == 1):
            value = valid.pop()
            # Add value into grid.
            g.insert(x,y,value)
            g.logMove(0, tCol.HEADER + "Solo Candidate" + tCol.ENDC + " - Set cell " + tCol.OKBLUE + "(" + str(x+1) + "," + str(y+1) + ")" + tCol.ENDC + " to " + tCol.OKBLUE + str(value) + tCol.ENDC)
            return g, True
    return g, False

#
def getSetCoverName(newValid, oldValid):
    if (len(newValid) + 2 == len(oldValid)):
        return "Naked/Hidden Pairs"
    elif (len(newValid) + 3 == len(oldValid)):
        return "Naked/Hidden Triples"
    elif (len(newValid) + 4 == len(oldValid)):
        return "Naked/Hidden Quads"
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
                        g.logMove(0, tCol.HEADER + getSetCoverName(newValid, oldValid) + tCol.ENDC + " - Reduced cell " + tCol.OKBLUE + "(" + str(x+1) + "," + str(y+1) + ")" + tCol.ENDC + " from " + tCol.WARNING + str(oldValid) + tCol.ENDC + " to " + tCol.WARNING + str(newValid) + tCol.ENDC)
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

# Detects an X-Wing/Swordfish/Jellyfish in the grid.
def xsj(g, k):
    candidates = []
    candidateValues = []

    # Iterate over rows to find candidates.
    for x in range(g.size):
        allOccurences = []
        # Iterate over columns.
        for y in range(g.size):
            if (g.get(x,y) == 0):
                # Merges all valid values across the column.
                valid = g.getValid(x,y)
                for v in valid:
                    allOccurences.append([v,y])
        # Values that occur k-times in a column.
        values = set()
        for i in range(1,10):
            count = 0
            for j in allOccurences:
                if (j[0] == i):
                    count += 1
            if (count == k):###
                values.add(i)
        # Value/Row Pair.
        a = [a for a in allOccurences if a[0] in values]
        #print(values, a)
        candidates.append(a)
        candidateValues.append(values)
    
    # Identify which values can occur in the X-Wing/Swordfish/Jellyfish.
    for i in range(1,10):
        count = 0
        # Count if a value occurs k times in a column, for at least k rows.
        for a in range(g.size):
            if (i in candidateValues[a]):         
                count += 1
        # If restricted in at least k columns.
        if (count >= k):###
            rowList = []
            for a in range(g.size):
                rowList.append([c[1] for c in candidates[a] if c[0] == i])

            # Coordinates of the X-Wing/Swordfish/Jellyfish.
            cols = []
            rows = []

            # Detects occurences across columns.
            for p in range(g.size):
                if (len(rowList[p]) == k):###
                    if (rowList.count(rowList[p]) == k):###
                        cols.append(p)
                        rows = rowList[p]
            
            # Detects an X-Wing/Swordfish/Jellyfish.
            if (len(cols) == k and len(rows) == k):###
                g.log(1, getStructureName(k) + " of value " + str(i) + " found at rows:" + str(rows) + " cols:" + str(cols))
                g, success =  xsjSolve(g, k, i, rows, cols)
                if (success):
                    return g, success
                
    return g, False

# Reduces valid values for cells conflicting with an X-Wing/Swordfish/Jellyfish.
def xsjSolve(g, k, n, rows, cols):
    success = False
    for x in range(g.size):
        for y in rows:
            if (not x in cols and g.get(x,y) == 0):
                valid = g.getValid(x,y)
                if (n in valid):
                    msg = tCol.HEADER + getStructureName(k) + tCol.ENDC + " - "
                    msg += "Reduced cell " + tCol.OKBLUE + "(" + str(x+1) + "," + str(y+1) + ")" + tCol.ENDC + " from "
                    msg += tCol.WARNING + str(valid) + tCol.ENDC + " to "
                    valid.discard(n)
                    msg += tCol.WARNING + str(valid) + tCol.ENDC
                    msg += " using " + getStructureName(k) + " at rows " + tCol.OKBLUE + str(rows) + tCol.ENDC
                    msg += ", cols " + tCol.OKBLUE + str(cols) + tCol.ENDC
                    g.logMove(0, msg)
                    g.updateCellValid(x,y,valid)
                    success = True         
    return g, success

# Updates the valid cells for every cell on the board.
def updateAllValid(g):
    for x, y in g.unfilledCells():
        poss = checkCell(g, x, y)
        g.updateCellValid(x, y, poss)
    return g

# Tests the grid against the rules and set solution.
def testGrid(g):
        if (g.error):
            print("Incorrect value inserted inconsistent with rules.")
            return False
        elif (not g.checkSolution):
            print("Incorrect value inserted inconsistent with solution.")
            return False
        else:
            return True

# Solves a sudoku by applying a list of strategies until new information is obtained.
def strategicSolver(g, show):
    found = True
    g.logMove(0, tCol.HEADER + "Initial Configuration" + tCol.ENDC)

    while (found):
        found = False

        # Displays the grid after each move.
        if (show == "True"):
            print(show)
            g.printClean()

        # Prints solution if the grid gets filled.
        if (g.isFilled()):
            print("[" + tCol.OKGREEN, "SOLVED IN", g.move - 1, "MOVES", tCol.ENDC + "]")
            return g, True
        
        # Solo Candidate.
        g, found = soloCandidate(g)
        if (found):
            continue
        if (not testGrid(g)):
            return g, False
        
        # Heuristic 2.
        g, found = h2(g)
        if (found):
            continue
        if (not testGrid(g)):
            return g, False

        # X-Wing along columns.
        g, found = xsj(g, 2)
        if (found):
            continue
        if (not testGrid(g)):
            return g, False

        #X-Wing along rows.
        g.transpose()
        g, found = xsj(g, 2)
        g.transpose()
        if (found):
            continue
        if (not testGrid(g)):
            return g, False
       
        # Swordfish along columns.
        g, found = xsj(g, 3)
        if (found):
            continue
        if (not testGrid(g)):
            return g, False

        # Swordfish along rows.
        g.transpose()
        g, found = xsj(g, 3)
        g.transpose()
        if (found):
            continue
        if (not testGrid(g)):
            return g, False

        # Jellyfish along columns.
        g, found = xsj(g, 4)
        if (found):
            continue
        if (not testGrid(g)):
            return g, False

        # Jellyfish along rows.
        g.transpose()
        g, found = xsj(g, 4)
        g.transpose()
        if (found):
            continue
        if (not testGrid(g)):
            return g, False

        # Exhausted Possibilities.
        print("[" + tCol.FAIL + " EXHAUSTED SEARCH " + tCol.ENDC + "]")

    return g, True


if __name__ == "__main__":
    # Grid Tests.
    g = easyGridTest()
    g = intermediateGridTest()
    g = difficultGridTest()
    g = xwingGridTest()
    g = swordfishGridTest()
    g = jellyfishGridTest()

    # Command Line arguments.
    print("Command Line Arguments")
    show = False
    if (len(sys.argv) - 1 >= 1):
        g.verbose = int(sys.argv[1])
        print("Verbose set to:", sys.argv[1])
    if (len(sys.argv) - 1 >= 2):
        show = sys.argv[2]
        print("Show grid set to:", sys.argv[2])

    # Initial Grid.
    print()
    print("[" + tCol.OKGREEN + " INITIAL " + tCol.ENDC + "]")
    g.printClean()
    print()

    # Solves the puzzle.
    g = updateAllValid(g)
    g, success = strategicSolver(g, show)
    print()
    print("[" + tCol.OKGREEN + " SOLUTION " + tCol.ENDC + "]")
    g.printClean()
    
    ###
    ###print()
    ###g.printValid()