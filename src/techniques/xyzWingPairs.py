from grid import Grid
from adjacencyList import WingAdjacencyList

# Finds all the weak bi-value pairs.
# Constructs an adjacency list of XYZ pairs.
def findXYZPairs(g):
    # Dictionary of all pairs.
    pairs = WingAdjacencyList()
    findColumnPairs(g, pairs)
    findRowPairs(g, pairs)
    findSectorPairs(g, pairs)
    return pairs

# Finds all pairs along columns.
def findColumnPairs(g, pairs):
    for x in range(g.size):
        for yi in range(g.size):
            yiCandidates = g.getCandidates(x, yi)
            if (len(yiCandidates) < 2):
                continue
            for yj in range(g.size):
                if (yi == yj):
                    continue
                yjCandidates = g.getCandidates(x, yj)
                if (len(yiCandidates) + len(yjCandidates) != 5):
                    continue
                commonCandidates = list(yiCandidates.intersection(yjCandidates))
                if (len(commonCandidates) == 2):
                    if (len(yiCandidates) == 3):
                        pairs.insert(tuple([x, yi]), tuple([x, yj]), commonCandidates)               
                    if (len(yjCandidates) == 3):
                        pairs.insert(tuple([x, yj]), tuple([x, yi]), commonCandidates)               
                    
# Finds all pairs along rows.
def findRowPairs(g, pairs):
    for y in range(g.size):
        for xi in range(g.size):
            xiCandidates = g.getCandidates(xi,y)
            if (len(xiCandidates) < 2):
                continue
            for xj in range(g.size):
                if (xi == xj):
                    continue
                xjCandidates = g.getCandidates(xj, y)
                if (len(xiCandidates) + len(xjCandidates) != 5):
                    continue
                commonCandidates = list(xiCandidates.intersection(xjCandidates))
                if (len(commonCandidates) == 2):
                    if (len(xiCandidates) == 3):
                        pairs.insert(tuple([xi, y]), tuple([xj, y]), commonCandidates)
                    if (len(xjCandidates) == 3):
                        pairs.insert(tuple([xj, y]), tuple([xi, y]), commonCandidates)

# Finds all pairs along sectors.
def findSectorPairs(g, pairs):
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        cx = 4 + (3 * a)
        cy = 4 + (3 * b)

        for xi, yi in g.sectorCells():
            iCandidates = g.getCandidates(cx + xi, cy + yi)
            if (len(iCandidates) < 2):
                continue
            for xj, yj in g.sectorCells():
                if (xi == xj and yi == yj):
                    continue
                jCandidates = g.getCandidates(cx + xj, cy + yj)
                if (len(iCandidates) + len(jCandidates) != 5):
                    continue
                commonCandidates = list(iCandidates.intersection(jCandidates))
                if (len(commonCandidates) == 2):
                    if (len(iCandidates) == 3):
                        pairs.insert(tuple([cx + xi, cy + yi]), tuple([cx + xj, cy + yj]), commonCandidates)
                    if (len(jCandidates) == 3):
                        pairs.insert(tuple([cx + xj, cy + yj]), tuple([cx + xi, cy + yi]), commonCandidates)
                        
