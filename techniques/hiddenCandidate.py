from grid import Grid
from colours import tCol

# Hidden Candidate.
# Complexity: O(x * y * i)
def hiddenCandidate(g):
    foundCol = hiddenCandidateColumn(g)
    foundSec = hiddenCandidateSector(g)
    g.transpose()
    foundRow = hiddenCandidateColumn(g)
    g.transpose()
    return (foundCol or foundSec or foundRow)

# Hidden Candidate - In a column where a value is only valid in one position.
def hiddenCandidateColumn(g):
    success = False
    # Finds hidden candidates along columns.
    for x in range(g.size):
        # All candidate values along the column.
        candidates = []
        for y in range(g.size):
            candidates.append(g.getCandidates(x,y))
        # Checks each value.
        for i in range(1,10):
            count = sum([1 for v in candidates if i in v])
            # If a value occurs only once in the column.
            if (count == 1):
                for y in range(g.size):
                    if i in candidates[y]:
                        g.insert(x,y,i)
                        msg = "row" if g.transposed else "column"
                        g.logMove(tCol.header("Hidden Candidate:") + " Set cell " + g.printCell(x,y) + " to " + tCol.okblue(str(i)) + " as only candidate in " + msg)
                        success = True
                        break
    return success

# Hidden Candidate - In a sector where a value is only valid in one position.
def hiddenCandidateSector(g):
    success = False
    # Set of all 3x3 sector centre points.
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        x = 4 + (3 * a)
        y = 4 + (3 * b)
        # All candidate values in the 3x3 sector.
        candidates = []
        for c, d in g.sectorCells():
            candidates.append(g.getCandidates(x + c, y + d))
        # Checks each value.
        for i in range(1,10):
            count = sum([1 for v in candidates if i in v])
            # If a value occurs once in the sector.
            if (count == 1):
                # Finds the cell containing the hidden candidate.
                for e, f in g.sectorCells():
                    if (i in g.getCandidates(x + e, y + f)):
                        g.insert(x + e, y + f, i)
                        g.logMove(tCol.header("Hidden Candidate:") + " Set cell " + g.printCell(x + e, y + f) + " to " + tCol.okblue(str(i)) + " as only candidate in sector")
                        success = True
                        break
    return success
