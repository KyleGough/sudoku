from grid import Grid
from colours import tCol

# Reduces candidates using Jellyfish.
def jellyfish(g):
    success = jellyfishDetect(g)
    g.transpose()
    success = success or jellyfishDetect(g)
    g.transpose()
    return success

# Detects Jellyfish with strong links along columns and weak links along rows.
def jellyfishDetect(g):
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

        # Checks at least 4 columns contain at least 3 candidates of n.
        candidateColumnCount = 0
        for i in candidateLocations:
            if (len(i) == 3 or len(i) == 4): ###
                candidateColumnCount += 1
        if (candidateColumnCount < 4):
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
                    for l in range(k+1, g.size):
                        if (len(candidateLocations[l]) == 0):
                            continue

                        # Union of rows.
                        rowUnion = candidateLocations[i].union(candidateLocations[j]).union(candidateLocations[k]).union(candidateLocations[l])
                        if (len(rowUnion) != 4):
                            continue

                        cols = [i,j,k,l]
                        rows = list(rowUnion)
                        
                        ###
                        #print(i,j,k)
                        #print(candidateLocations[i])
                        #print(candidateLocations[j])
                        #print(candidateLocations[k])
                        #print("N:    " + str(n))
                        #print("Rows: " + g.printSet(rows))
                        #print("Cols: " + g.printSet(cols))

                        success = jellyfishReduce(g, n, cols, rows)
                        
                        if (success):
                            return True

    return False

# Uses an Jellyfish to reduce candidates of cells intersecting it.
def jellyfishReduce(g, n, cols, rows):
    success = False
    
    for r in rows:
        for x in range(g.size):
            if (x in cols):
                continue

            ###print(x+1, r+1, n)

            candidates = g.getCandidates(x, r)
            if (n in candidates):
                msg = tCol.header("Jellyfish:") + " Reduced cell "
                msg += g.printCell(x, r) + " from " + g.printSet(candidates)            
                candidates.discard(n)
                msg += " to " + g.printSet(candidates) + " using Jellyfish at "
                msg += "cols" if g.transposed else "rows"
                msg += " " + g.printSet(list(map(lambda x: x+1, rows))) + ", "
                msg += "rows" if g.transposed else "cols"
                msg += " " + g.printSet(list(map(lambda x: x+1, cols)))
                g.logMove(msg)
                success = True
    
    return success