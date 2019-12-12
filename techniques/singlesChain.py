from grid import Grid
from colours import tCol

#
def singlesChain(g):
    ###
    for n in range(g.size):
        singlesChainCheck(g, n)
    return g, False

#
def singlesChainCheck(g, n):
    conjugatePairs = findConjugatePairs(g,n)
    if (len(conjugatePairs) >= 2):
        ###
        print()
        ###
    return g, False

# Finds all the conjugate pairs with candidate n.
def findConjugatePairs(g, n):

    # List of all conjugate pairs.
    conjugatePairs = []

    # Check columns for conjugate pairs.
    for x in range(g.size):
        candidateCells = []
        for y in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the column.
        if (len(candidateCells) == 2):
            conjugatePairs.append(candidateCells)
    
    # Check rows for conjugate pairs.
    for y in range(g.size):
        candidateCells = []
        for x in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the row.
        if (len(candidateCells) == 2):
            conjugatePairs.append(candidateCells)

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
            conjugatePairs.append(candidateCells)

    print(conjugatePairs)
    print(len(conjugatePairs))

    return conjugatePairs

#########################################################

# Strong Link/Conjugate Pair.
# One MUST be true and the other MUST be false.
# Cannot have both false, or both true.

# Find all conjugate pairs.
  # Loop over rows.
  # Loop over columns.
  # Loop over sectors.

# Add terminology section to the readme file.


# Find all conjugate pair cells.
  # Store in list.
# Mark first as colour 1
# Mark corresponding as colour 2.
# Check both cells to queue.
# Check for other pairs connected.

# METHOD: Check if cell can be coloured (not conflicting with colours elsewhere)

