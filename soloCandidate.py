from grid import Grid
from colours import tCol

# Solo Candidate - Where a cell has only one possibility.
# Complexity: O(x * y).
def soloCandidate(g):
    success = False
    # Iterate over each non-filled cell.
    for x, y in g.unfilledCells():
        valid = g.getValid(x,y)
        # Check for a single possibility.
        if (len(valid) == 1):
            value = valid.pop()
            # Add value into grid.
            g.insert(x,y,value)
            g.logMove(0, tCol.HEADER + "Solo Candidate" + tCol.ENDC + " - Set cell " + tCol.OKBLUE + "(" + str(x+1) + "," + str(y+1) + ")" + tCol.ENDC + " to " + tCol.OKBLUE + str(value) + tCol.ENDC)
            success = True
    return g, success