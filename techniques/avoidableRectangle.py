from grid import Grid
from colours import tCol

### Trivial implementation is O(N^4) -1296
def avoidableRect(g):

    # Iterates over all rectangles.
    for t in range(g.size - 1):
        for b in range(t + 1, g.size):
            for l in range(g.size - 1):
                for r in range(l + 1, g.size):

                    # Sets of cells in the AR.
                    cells = set()
                    cells.add(tuple([l,t]))
                    cells.add(tuple([r,t]))
                    cells.add(tuple([l,b]))
                    cells.add(tuple([r,b]))

                    # Count filled cells.
                    filledCount = 0
                    values = set()
                    for c in cells:
                        value = g.get(c[0], c[1])
                        if (value == 0):
                            emptyCell = c
                        elif (g.clue[c[0]][c[1]] == True):
                            values.add(value)
                            filledCount += 1

                    # AR requires 3 filled cells.
                    if (filledCount != 3):
                        continue

                    # Filled cells are only 2 values.
                    if (len(values) != 2):
                        continue

                    # AR occupies two sectors.
                    sector = set()  
                    for c in cells:
                        cx, cy = g.getSectorCoord(c[0], c[1])                  
                        sector.add(tuple([cx, cy]))
                    if (len(sector) != 2):
                        continue

                    candidates = g.getCandidates(emptyCell[0], emptyCell[1])
                    msg = tCol.header("Avoidable Rectangle:") + " Reduced cell "
                    msg += g.printCell(emptyCell[0], emptyCell[1]) + " from "
                    msg += g.printSet(candidates) + " to "
                    newCandidates = candidates.difference(values)
                    if (len(candidates) != len(newCandidates)):
                        g.updateCandidates(emptyCell[0], emptyCell[1], newCandidates)
                        msg += g.printSet(newCandidates) + " using cells"
                        for c in cells:
                            msg += " (" + str(c[0]+1) + "," + str(c[1]+1) + ")"
                        g.logMove(msg)
                        print(msg)
                        return True
  
    return False
