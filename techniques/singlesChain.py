from grid import Grid
from colours import tCol
from techniques.conjugatePairs import findConjugatePairs
from queue import Queue

# Performs the singles chain strategy to find violations of colour rules to eliminate candidates.
def singlesChain(g):
    success = False
    for n in range(1,10):
        conjugatePairs = findConjugatePairs(g,n)
        # Must contain at least 2 conjugate pairs to form a chain.
        if (conjugatePairs.pairs >= 2):
            success = singlesChainCheck(g, n, conjugatePairs) or success
    return success

# Constructs a chain of conjugate pairs with candidate n, to find violations.
def singlesChainCheck(g, n, conjugatePairs):

    while (conjugatePairs.getSize() >= 2):
        # A cell in a conjugate pair must be either ON or OFF.
        onCells = set() # Cells marked with ON.
        offCells = set() # Cells marked with OFF.
        cellQueue = Queue() # Queue of cells to check.

        # Gets an initial conjugate pair to construct a chain.
        chainStart, chainStartConnections = conjugatePairs.getFirst()
        # Mark the start of the chain as ON.
        onCells.add(chainStart)
        # Removes from the adjacency list.
        conjugatePairs.delete(chainStart)

        # Mark cells that form a pair with the start of the chain as OFF.
        for i in chainStartConnections:
            offCells.add(i)
            cellQueue.put(i)
    
        # Process cell queue to form a singles chain.
        while (not cellQueue.empty()):
            c = cellQueue.get()
            links = conjugatePairs.getLinks(c)
            
            for l in links:
                # Checks l is not coloured.
                if l not in offCells and l not in onCells:
                    if c in onCells:
                        offCells.add(l)
                        # If violation in offCell set, so remove all candidates of cells in the set.
                        if checkViolation(l, offCells):
                            removeViolationCells(g, n, offCells)
                            return True                        
                    else: 
                        onCells.add(l)
                        # If violation in onCell set, remove all candidates of cells in the set.
                        if checkViolation(l, onCells):
                            #print("VIOLATION ON", str(l))
                            #print(str(onCells))
                            removeViolationCells(g, n, onCells)
                            return True
                    cellQueue.put(l)

            # Removes from the adjacency list.
            conjugatePairs.delete(c)

        # Checks all cells for a violation where a cell can "see" both colours.
        for x in range(g.size):
            for y in range(g.size):
                cell = tuple([x,y])
                valid = g.getValid(x,y)
                # Checks cells has candidate n and not coloured.
                if ((n in valid) and (cell not in onCells) and (cell not in offCells)):
                    # If the cell can "see" both colours then eliminate candidate.
                    if (checkViolation(cell, onCells) and checkViolation(cell, offCells)):
                        msg = tCol.header("Singles Chain:") + " Reduced cell "
                        msg += g.printCell(x,y) + " from " + g.printSet(valid)
                        valid.discard(n)
                        g.updateCellValid(x, y, valid)
                        msg += " to " + g.printSet(valid) + " as can see both colours."
                        g.logMove(0, msg) 
                        return True

    return False

# Removes candidate n from all cells in the given coloured set.
def removeViolationCells(g, n, cellSet):
    for c in cellSet:
        x = c[0]
        y = c[1]
        valid = g.getValid(x,y)
        msg = tCol.header("Singles Chain:") + " Reduced cell "
        msg += g.printCell(x,y) + " from " + g.printSet(valid)
        valid.discard(n)
        g.updateCellValid(x, y, valid)
        msg += " to " + g.printSet(valid) + " due to colour violation."
        g.logMove(0, msg) 

# Checks if a cell can see another cell in ON or OFF state.
def checkViolation(cell, colourSet):
    # Check each cell in the set.
    for i in colourSet:
        # Ignore the newly inserted cell.
        if cell == i:
            continue
        # Check row for 
        if (cell[0] == i[0]):
            return True
        # Check column.
        elif (cell[1] == i[1]):
            return True
        # Check sector.
        else:
            cx = ((cell[0] // 3) * 3) + 1
            cy = ((cell[1] // 3) * 3) + 1
            ix = ((i[0] // 3) * 3) + 1
            iy = ((i[1] // 3) * 3) + 1
            if (cx == ix and cy == iy):
                return True

    return False
