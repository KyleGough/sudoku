from grid import Grid
from adjacencyList import BiValueAdjacencyList

# Finds all the weak bi-value pairs.
# Constructs an adjacency list of bi-value pairs.
def findWeakBiValuePairs(g):
    # Dictionary of all bi-value pairs.
    biValuePairs = BiValueAdjacencyList()
    findColumnPairs(g, biValuePairs)
    findRowPairs(g, biValuePairs)
    findSectorPairs(g, biValuePairs)
    return biValuePairs

# Finds all bi-value pairs along columns.
def findColumnPairs(g, biValuePairs):
    for x in range(g.size):
        for yi in range(g.size):
            yiCandidates = g.getCandidates(x, yi)
            if (len(yiCandidates) != 2):
                continue
            for yj in range(g.size):
                if (yi == yj):
                    continue
                yjCandidates = g.getCandidates(x, yj)
                if (len(yjCandidates) != 2):
                    continue
                commonCandidates = yiCandidates.intersection(yjCandidates)
                for cc in commonCandidates:
                    biValuePairs.insert(tuple([x, yi]), tuple([x, yj]), cc)               
             
# Finds all bi-value pairs along rows.
def findRowPairs(g, biValuePairs):
    for y in range(g.size):
        for xi in range(g.size):
            xiCandidates = g.getCandidates(xi,y)
            if (len(xiCandidates) != 2):
                continue
            for xj in range(g.size):
                if (xi == xj):
                    continue
                xjCandidates = g.getCandidates(xj, y)
                if (len(xjCandidates) != 2):
                    continue
                commonCandidates = xiCandidates.intersection(xjCandidates)
                for cc in commonCandidates:
                    biValuePairs.insert(tuple([xi, y]), tuple([xj, y]), cc)

# Finds all bi-value pairs along sectors.
def findSectorPairs(g, biValuePairs):
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        cx = 4 + (3 * a)
        cy = 4 + (3 * b)

        for xi, yi in g.sectorCells():
            iCandidates = g.getCandidates(cx + xi, cy + yi)
            if (len(iCandidates) != 2):
                continue
            for xj, yj in g.sectorCells():
                if (xi == xj and yi == yj):
                    continue
                jCandidates = g.getCandidates(cx + xj, cy + yj)
                if (len(jCandidates) != 2):
                    continue
                commonCandidates = iCandidates.intersection(jCandidates)
                for cc in commonCandidates:
                    biValuePairs.insert(tuple([cx + xi, cy + yi]), tuple([cx + xj, cy + yj]), cc)