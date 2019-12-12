from grid import Grid
from colours import tCol
from adjacencyList import AdjacencyList

#
def singlesChain(g):
    ###
    success = False
    for n in range(g.size):
        conjugatePairs = findConjugatePairs(g,n)
        # Must contain at least 2 conjugate pairs to form a chain.
        if (conjugatePairs.pairs >= 2):
            singlesChainCheck(g, n, conjugatePairs)
    return g, success

#
def singlesChainCheck(g, n, conjugatePairs):
    ###
    #onCells = set()
    #offCells = set()
    print(n)
    print(conjugatePairs.toString())
    print()
    return g, False


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
               candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the sector.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])
 
    return conjugatePairs


# Checks if a cell can see two oppositely coloured cells.
def canSee(g, x, y):
    # iterate over list.
    return False

#########################################################

# Strong Link/Conjugate Pair.
# One MUST be true and the other MUST be false.
# Cannot have both false, or both true.

# Add terminology section to the readme file.
# Remove grid in returns because it should be passed by reference anyways.
# Calculate big-o complex of other techniques.

# Find all conjugate pair cells. DONE
# Mark first as colour 1
# Mark corresponding as colour 2.
# Check both cells to queue.
# Check for other pairs connected.

# METHOD: Check if cell can be coloured (not conflicting with colours elsewhere)

