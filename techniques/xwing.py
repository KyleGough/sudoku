from grid import Grid
from colours import tCol
from techniques.conjugatePairs import findColumnPairs, findRowPairs
from adjacencyList import AdjacencyList

# Reduces candidates using X-Wings.
def xWing(g):
    success = xWingDetect(g)
    g.transpose()
    success = success or xWingDetect(g)
    g.transpose()
    return success

# Detects X-Wings with strong links along columns and weak links along rows.
def xWingDetect(g):
    success = False

    for n in range(1, 10):
        conjugatePairs = AdjacencyList()
        findColumnPairs(g, n, conjugatePairs)

        # An X-Wing is a formation of two conjugate pairs.
        if (conjugatePairs.getSize() < 2):
            continue
        
        # Gets a list of all cells that are part of a conjugate pair.
        candidateCells = conjugatePairs.getCells()

        # Constructs a list of the row indices for each column.
        rowIdx = []
        for i in range(g.size):
            rows = []
            for cell in candidateCells:
                if cell[0] == i:
                    rows.append(cell[1])
            rowIdx.append(rows)

        # Detects an X-Wing by comparing common rows.
        for i in range(0, g.size):
            for j in range(i + 1, g.size):
                if (len(rowIdx[i]) > 0 and rowIdx[i] == rowIdx[j]):
                    success = success or xwingReduce(g, n, [i,j], rowIdx[i])

    return success

# Uses an X-Wing to reduce candidates of cells intersecting the X-Wing.
def xwingReduce(g, n, cols, rows):
    success = False

    for y in rows:
        for x in range(g.size):
            if (not x in cols):
                candidates = g.getCandidates(x,y)
                # Avoids cells that form the X-Wing.
                if (n in candidates):
                    msg = tCol.header("X-Wing:") + " Reduced cell "
                    msg += g.printCell(x, y) + " from " + g.printSet(candidates)
                    candidates.discard(n)
                    msg += " to " + g.printSet(candidates) + " using X-Wing at "
                    msg += "cols" if g.transposed else "rows"
                    msg += " " + g.printSet(list(map(lambda x: x+1, rows))) + ", "
                    msg += "rows" if g.transposed else "cols"
                    msg += " " + g.printSet(list(map(lambda x: x+1, cols)))
                    g.logMove(msg)
                    success = True
    
    return success