from grid import Grid
from adjacencyList import BiValueAdjacencyList

# Finds all the bi-value pairs.
# Constructs an adjacency list of bi-value pairs.
def findBiValuePairs(g):
    # Dictionary of all bi-value pairs.
    biValuePairs = BiValueAdjacencyList()
    findColumnPairs(g, biValuePairs)
    findRowPairs(g, biValuePairs)
    findSectorPairs(g, biValuePairs)
    return biValuePairs

# Finds all bi-value pairs along columns.
def findColumnPairs(g, biValuePairs):
    for x in range(g.size):
        for n in range(1, 10):
            candidateCells = []
            for y in range(g.size):
                valid = g.getValid(x,y)
                if (len(valid) == 2 and n in valid):
                    candidateCells.append(tuple([x,y])) ###
            # Detects a bi-value pair in the column.
            if (len(candidateCells) == 2):
                biValuePairs.insert(candidateCells[0], candidateCells[1], n)

# Finds all bi-value pairs along rows.
def findRowPairs(g, biValuePairs):
    for y in range(g.size):
        for n in range(1, 10):
            candidateCells = []
            for x in range(g.size):
                valid = g.getValid(x,y)
                if (len(valid) == 2 and n in valid):
                    candidateCells.append(tuple([x,y])) ###
            # Detects a bi-value pair in the row.
            if (len(candidateCells) == 2):
                biValuePairs.insert(candidateCells[0], candidateCells[1], n)

# Finds all bi-value pairs along sectors.
def findSectorPairs(g, biValuePairs):
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        x = 4 + (3 * a)
        y = 4 + (3 * b)
        for n in range(1, 10):
            candidateCells = []
            for i, j in g.sectorCells():
                valid = g.getValid(x + i, y + j)
                if (len(valid) == 2 and n in valid):
                    candidateCells.append(tuple([x+i,y+j])) ###
            # Detects a bi-value pair in the sector.
            if (len(candidateCells) == 2):
                biValuePairs.insert(candidateCells[0], candidateCells[1], n)