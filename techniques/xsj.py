from grid import Grid
from colours import tCol

# X-Wing.
def xwing(g):
    return xsj(g,2)

# Swordfish.
def swordfish(g):
    return xsj(g,3)

# Jellyfish.
def jellyfish(g):
    return xsj(g,4)
    
# Uses either X-Wing, Swordfish or Jellyfish technique.
# Complexity: O(x * y * n)
def xsj(g, k):
    g, foundCol = xsjDetect(g,k)
    g.transpose()
    g, foundRow = xsjDetect(g,k)
    g.transpose()
    return g, (foundCol or foundRow)

# Detects an X-Wing/Swordfish/Jellyfish in the grid.
def xsjDetect(g, k):
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
                    colsM = list(map(lambda x: x + 1, cols))
                    rowsM = list(map(lambda x: x + 1, rows))
                    
                    msg = tCol.HEADER + getStructureName(k) + tCol.ENDC + " - "
                    msg += "Reduced cell " + g.printCell(x,y) + " from "
                    msg += tCol.WARNING + str(valid) + tCol.ENDC + " to "
                    valid.discard(n)
                    msg += tCol.WARNING + str(valid) + tCol.ENDC
                    msg += " using " + getStructureName(k) + " at rows " + tCol.OKBLUE
                    msg += str(colsM) if g.transposed else str(rowsM) 
                    msg += tCol.ENDC + ", cols " + tCol.OKBLUE
                    msg += str(rowsM) if g.transposed else str(colsM)
                    msg += tCol.ENDC
                    g.logMove(0, msg)
                    g.updateCellValid(x,y,valid)
                    success = True         
    return g, success

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
