from grid import Grid
from colours import tCol

# Reduces candidates using Swordfish.
def swordfish(g):
    success = swordfishDetect(g)
    g.transpose()
    success = success or swordfishDetect(g)
    g.transpose()
    return success

# Detects Swordfish with strong links along columns and weak links along rows.
def swordfishDetect(g):
    success = False

    for n in range(1, 10):
        # Finds the locations of candidate n.
        candidateLocations = []
        # Iterate over columns.
        for x in range(g.size):
            RowLocations = set()
            for y in range(g.size):
                if (n in g.getCandidates(x,y)):
                    RowLocations.add(y)
            candidateLocations.append(RowLocations)

        # Checks at least 3 columns contain at least 2 candidates of n.
        candidateColumnCount = 0
        for i in candidateLocations:
            if (len(i) == 2 or len(i) == 3):
                candidateColumnCount += 1
        if (candidateColumnCount < 3):
            continue

        for i in range(g.size):
            if (len(candidateLocations[i]) == 0):
                continue    
            for j in range(i+1, g.size):
                if (len(candidateLocations[j]) == 0):
                    continue
                for k in range(j+1, g.size):
                    if (len(candidateLocations[k]) == 0):
                        continue                    

                    # Union of rows.
                    rowUnion = candidateLocations[i].union(candidateLocations[j]).union(candidateLocations[k])
                    if (len(rowUnion) != 3):
                        continue

                    cols = [i,j,k]
                    rows = list(rowUnion)
                    
                    ###
                    #print(i,j,k)
                    #print(candidateLocations[i])
                    #print(candidateLocations[j])
                    #print(candidateLocations[k])
                    #print("N:    " + str(n))
                    #print("Rows: " + g.printSet(rows))
                    #print("Cols: " + g.printSet(cols))

                    success = swordfishReduce(g, n, cols, rows)
                    
                    if (success):
                        return True

    return False

# Uses an Swordfish to reduce candidates of cells intersecting it.
def swordfishReduce(g, n, cols, rows):
    success = False
    
    for r in rows:
        for x in range(g.size):
            if (x in cols):
                continue

            ###print(x+1, r+1, n)

            candidates = g.getCandidates(x, r)
            if (n in candidates):
                msg = tCol.header("Swordfish:") + " Reduced cell "
                msg += g.printCell(x, r) + " from " + g.printSet(candidates)            
                candidates.discard(n)
                msg += " to " + g.printSet(candidates) + " using Swordfish at "
                msg += "cols" if g.transposed else "rows"
                msg += " " + g.printSet(list(map(lambda x: x+1, rows))) + ", "
                msg += "rows" if g.transposed else "cols"
                msg += " " + g.printSet(list(map(lambda x: x+1, cols)))
                g.logMove(msg)
                success = True
    
    return success