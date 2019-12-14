from grid import Grid
from adjacencyList import AdjacencyList

# Finds all the conjugate pairs with candidate n.
# Constructs an adjacency list of conjugate pairs.
def findConjugatePairs(g, n):

    # Dictionary of all conjugate pairs.
    conjugatePairs = AdjacencyList()

    # Check columns for conjugate pairs.
    for x in range(g.size):
        candidateCells = []
        for y in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the column.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])
    
    # Check rows for conjugate pairs.
    for y in range(g.size):
        candidateCells = []
        for x in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the row.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])

    # Check sectors for conjugate pairs.
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        x = 4 + (3 * a)
        y = 4 + (3 * b)
        candidateCells = []
        for i, j in g.sectorCells():
            if (n in g.getValid(x + i, y + j)):
               candidateCells.append(tuple([x + i,y + j]))
        # Detects a conjugate pair in the sector.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])
 
    return conjugatePairs

