from grid import Grid
from colours import tCol

# Solo Candidate - Where a cell has only one possibility.
# Complexity: O(x * y).
def soloCandidate(g):
    success = False
    # Iterate over each non-filled cell.
    for x, y in g.unfilledCells():
        candidates = g.getCandidates(x,y)
        # Check for a single possibility.
        if (len(candidates) == 1):
            value = candidates.pop()
            # Add value into grid.
            g.insert(x,y,value)
            g.logMove(tCol.header("Solo Candidate:") + " Set cell " + g.printCell(x,y) + " to " + tCol.okblue(str(value)))
            success = True
    return success
