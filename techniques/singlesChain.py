from grid import Grid
from colours import tCol

def singlesChain(g):
    return g, False

def singlesChainCheck(g, n):
    return g, False

### must find at leasr 2 pairs.
def findConjugatePairs(g, n):

    # List of all conjugate pairs.
    conjugatePairs = []

    # Check columns for pairs.
    for x in range(g.size):
        candidateCells = []
        for y in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple(x,y))
        # Detects a conjugate pair in the column.
        if (len(candidateCells) == 2):
            conjugatePairs.append(candidateCells)
    
    # Check rows for pairs.
    for y in range(g.size):
        candidateCells = []
        for x in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple(x,y))
        # Detects a conjugate pair in the row.
        if (len(candidateCells) == 2):
            conjugatePairs.append(candidateCells)

    # Check sectors for pairs.

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

