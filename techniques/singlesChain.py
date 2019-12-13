from grid import Grid
from colours import tCol
from adjacencyList import AdjacencyList
from queue import Queue

#
def singlesChain(g):
    ###
    success = False
    ###for n in range(g.size):
    n = 5
    if (n == 5): ###remove this line and line above later.
        conjugatePairs = findConjugatePairs(g,n)
        # Must contain at least 2 conjugate pairs to form a chain.
        if (conjugatePairs.pairs >= 2):
            success = singlesChainCheck(g, n, conjugatePairs) or success
    return success

#
def singlesChainCheck(g, n, conjugatePairs):

    # Make chain until no more connections.
    # do stuff
    # if still conjugate pairs (at least 2)
    # make new chain
    # repeat until 0 or 1 conjugate pairs left.
    while (conjugatePairs.getSize() >= 2):
        
        # A cell in a conjugate pair must be either ON or OFF.
        onCells = set() # Cells marked with ON.
        offCells = set() # Cells marked with OFF.
        cellQueue = Queue() # Queue of cells to check.

        # Gets an initial conjugate pair to construct a chain.
        chainStart, chainStartConnections = conjugatePairs.getFirst()
        # Mark the start of the chain as ON.
        onCells.add(chainStart)

        # Mark cells that form a pair with the start of the chain as OFF.
        for i in chainStartConnections:
            offCells.add(i)
            cellQueue.put(i)
            conjugatePairs.remove(chainStart, i)

        ### init
        #print("<PRE>")
        #print(conjugatePairs.toString())
        #print(str(offCells))
        #print(str(onCells))
        #print("</PRE>")
        ###

        while (not cellQueue.empty()):
            c = cellQueue.get()
            links = conjugatePairs.getLinks(c)
            print("Queue item: ", str(c), "->", str(links)) ###
            print("Queue size:", cellQueue.qsize())
            
            for l in links:
                print("Queue process:", str(l)) ###
                # Checks l is not coloured.
                if l not in offCells and l not in onCells:
                    if c in onCells:
                        if checkViolation(l, offCells):
                            print("VIOLATION")
                            return
                        else:
                            offCells.add(l) 
                    else: 
                        if checkViolation(l, onCells):
                            print("VIOLATION")
                            return
                        else:
                            onCells.add(l)

                    cellQueue.put(l)
                    #conjugatePairs.remove(c, l)


        # Checks all cells for a violation where a cell can "see" both colours.
        for x in range(g.size):
            for y in range(g.size):
                cell = tuple([x,y])
                valid = g.getValid(x,y)
                # Checks cells has candidate n and not coloured.
                if ((n in valid) and (cell not in onCells) and (cell not in offCells)):
                    # If the cell can "see" both colours then eliminate candidate.
                    if (checkViolation(cell, onCells) and checkViolation(cell, offCells)):
                        ###
                        #print("BOTH COLOUR VIOLATION AT: ", x, y)
                        msg = tCol.header("Singles Chain:") + " Reduced cell "
                        msg += g.printCell(x,y) + " from " + g.printSet(valid)
                        valid.discard(n)
                        g.updateCellValid(x, y, valid)
                        msg += " to " + g.printSet(valid) + " as can see both colours."
                        g.logMove(0, msg) 
                        return True


        # delete everything in onells and offcells from adjacency list.

        print(conjugatePairs.toString())
        print(onCells)
        print(offCells)
        print("###END###")
        print()

    return False


# Finds all the conjugate pairs with candidate n.
# Constructs an adjacency list of conjugate pairs.
def findConjugatePairs(g, n):

    # Dictionary of all conjugate pairs.
    conjugatePairs = AdjacencyList()

    # Check columns for conjugate pairs.
    for x in range(g.size):
        candidateCells = []
        for y in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the column.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])
    
    # Check rows for conjugate pairs.
    for y in range(g.size):
        candidateCells = []
        for x in range(g.size):
            if (n in g.getValid(x,y)):
                candidateCells.append(tuple([x,y]))
        # Detects a conjugate pair in the row.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])

    # Check sectors for conjugate pairs.
    for a, b in g.sectorCells():
        # Maps (a,b) to (x,y), the sector centre point.
        x = 4 + (3 * a)
        y = 4 + (3 * b)
        candidateCells = []
        for i, j in g.sectorCells():
            if (n in g.getValid(x + i, y + j)):
               candidateCells.append(tuple([x + i,y + j]))
        # Detects a conjugate pair in the sector.
        if (len(candidateCells) == 2):
            conjugatePairs.insert(candidateCells[0], candidateCells[1])
 
    return conjugatePairs


# Checks if a cell can see another cell in ON or OFF state.
def checkViolation(cell, colourSet):
    # Check each cell in the set.
    for i in colourSet:
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

#########################################################

# Add terminology section to the readme file.
# Remove grid in returns because it should be passed by reference anyways.
# Calculate big-o complex of other techniques.

# Find all conjugate pair cells. DONE
# Mark first as colour 1
# Mark corresponding as colour 2.
# Check both cells to queue.
# Check for other pairs connected.

# METHOD: Check if cell can be coloured (not conflicting with colours elsewhere)

