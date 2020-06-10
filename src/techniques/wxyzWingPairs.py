from grid import Grid
from adjacencyList import WingAdjacencyList

# Finds all the weak bi-value pairs.
# Constructs an adjacency list of WXYZ pairs.
def findWXYZPairs(g):
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
            if (len(yiCandidates) < 2 or len(yiCandidates) > 4):
                continue
            for yj in range(yi + 1, g.size):
                if (yi == yj):
                    continue
                yjCandidates = g.getCandidates(x, yj)
                if (len(yjCandidates) < 2 or len(yjCandidates) > 4):
                    continue
                commonCandidates = list(yiCandidates.intersection(yjCandidates))
                if (len(commonCandidates) > 0):
                    pairs.insert(tuple([x, yi]), tuple([x, yj]), commonCandidates)               
                    pairs.insert(tuple([x, yj]), tuple([x, yi]), commonCandidates)               
                    
# Finds all pairs along rows.
def findRowPairs(g, pairs):
    for y in range(g.size):
        for xi in range(g.size):
            xiCandidates = g.getCandidates(xi,y)
            if (len(xiCandidates) < 2 or len(xiCandidates) > 4):
                continue
            for xj in range(xi + 1, g.size):
                if (xi == xj):
                    continue
                xjCandidates = g.getCandidates(xj, y)
                if (len(xjCandidates) < 2 or len(xjCandidates) > 4):
                    continue
                commonCandidates = list(xiCandidates.intersection(xjCandidates))
                if (len(commonCandidates) > 0):
                    pairs.insert(tuple([xi, y]), tuple([xj, y]), commonCandidates)
                    pairs.insert(tuple([xj, y]), tuple([xi, y]), commonCandidates)

# Finds all pairs along sectors.
def findSectorPairs(g, pairs):
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        cx = 4 + (3 * a)
        cy = 4 + (3 * b)

        iCount = -1
        for xi, yi in g.sectorCells():
            iCount += 1
            iCandidates = g.getCandidates(cx + xi, cy + yi)
            if (len(iCandidates) < 2 or len(iCandidates) > 4):
                continue
            jCount = -1
            for xj, yj in g.sectorCells():
                jCount += 1
                if (xi == xj and yi == yj):
                    continue
                if (jCount <= iCount):
                    continue
                jCandidates = g.getCandidates(cx + xj, cy + yj)
                if (len(jCandidates) < 2 or len(jCandidates) > 4):
                    continue
                commonCandidates = list(iCandidates.intersection(jCandidates))
                if (len(commonCandidates) > 0):
                    pairs.insert(tuple([cx + xi, cy + yi]), tuple([cx + xj, cy + yj]), commonCandidates)
                    pairs.insert(tuple([cx + xj, cy + yj]), tuple([cx + xi, cy + yi]), commonCandidates)
                        
