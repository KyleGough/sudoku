from grid import Grid
  
# Checks conflicts in a row.
def checkRow(g, y):
    perm = set()
    for x in range(g.size):
        perm.add(g.get(x,y))
    return perm

# Checks conflicts in a column.
def checkColumn(g, x):
    perm = set()
    for y in range(g.size):
        perm.add(g.get(x,y))
    return perm

# Checks conflicts in a 3x3 sector.
def checkSector(g, x, y):
    perm = set()
    cx, cy = g.getSectorCoord(x,y)
    for i, j in g.sectorCells():
        perm.add(g.get(cx + i,cy + j))
    return perm

# Checks all conflicts for a given cell.
def checkCell(g, x, y):
    # Conflicting values.
    conflicts = checkRow(g, y)
    conflicts.update(checkColumn(g, x))
    conflicts.update(checkSector(g, x, y))
    # Possibilities.
    return {1,2,3,4,5,6,7,8,9} - conflicts

# Updates the valid cells for every cell on the board.
def initGrid(g):
    for x, y in g.unfilledCells():
        poss = checkCell(g, x, y)
        g.updateCellValid(x, y, poss)
    return g
