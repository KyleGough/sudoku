from grid import Grid
from colours import tCol

#
def pointingPairs(g):
    success = False

    # Iterates over the sector midpoints.
    for cx in range(1,8,3):
        for cy in range(1,8,3):

            # For each value 1 to 9.
            for n in range(1,10):
                count = 0
                # Count occurences of n in the sector.
                for i, j in g.sectorCells():
                    if (n in g.getValid(cx+i,cy+j)):
                        count += 1

                if (count != 2 and count != 3):
                    continue
                
                # Valid for each cell in the sector.
                a1 = n in g.getValid(cx-1,cy-1)
                a2 = n in g.getValid(cx,cy-1)
                a3 = n in g.getValid(cx+1,cy-1)
                b1 = n in g.getValid(cx-1,cy)
                b2 = n in g.getValid(cx,cy)
                b3 = n in g.getValid(cx+1,cy)
                c1 = n in g.getValid(cx-1,cy+1)
                c2 = n in g.getValid(cx,cy+1)
                c3 = n in g.getValid(cx+1,cy+1)

                # Pointing Pairs.
                # Pair in row cy-1.
                if (count == 2 and ((a1 and a2) or (a1 and a3) or (a2 and a3))) or (count == 3 and a1 and a2 and a3):
                    success = checkRow(g, cy-1, n, cx, cy) or success
                    continue
                # Pair in row cy.
                elif (count == 2 and ((b1 and b2) or (b1 and b3) or (b2 and b3))) or (count == 3 and a2 and b2 and c2):
                    success = checkRow(g, cy, n, cx, cy) or success
                    continue
                # Pair in row cy+1.
                elif (count == 2 and ((c1 and c2) or (c1 and c3) or (c2 and c3))) or (count == 3 and a3 and b3 and c3):
                    success = checkRow(g, cy+1, n, cx, cy) or success
                    continue
                # Pair in column cx-1.
                elif (count == 2 and ((a1 and b1) or (a1 and c1) or (b1 and c1))) or (count == 3 and a1 and b1 and c1):
                    success = checkColumn(g, cx-1, n, cx, cy) or success
                    continue
                # Pair in column cx.
                elif (count == 2 and ((a2 and b2) or (a2 and c2) or (b2 and c2))) or (count == 3 and a2 and b2 and c2):
                    success = checkColumn(g, cx, n, cx, cy) or success
                    continue
                # Pair in column cx+1.
                elif (count == 2 and ((a3 and b3) or (a3 and c3) or (b3 and c3))) or (count == 3 and a3 and b3 and c3):
                    success = checkColumn(g, cx+1, n, cx, cy) or success
                    continue 
                            
    return g, success


# Checks along the row.
def checkRow(g, y, n, cx, cy):
    success = False
    for x in range(g.size):
        # If cell is not in sector.
        if (abs(x - cx) > 1):
            valid = g.getValid(x, y)
            if (n in valid):
                msg = tCol.header("Pointing Pair") + " - Reduced cell "
                msg += g.printCell(x,y) + " from " + tCol.warning(str(valid))

                valid.discard(n)
                g.updateCellValid(x, y, valid)

                msg += " to " + tCol.warning(str(valid))
                msg += " using sector " + g.printCell(cx,cy)
                g.logMove(0, msg)
                success = True 
    return success 

# Checks along the column.
def checkColumn(g, x, n, cx, cy):

    success = False
    for y in range(g.size):
        # If cell is not in sector.
        if (abs(y - cy) > 1):
            valid = g.getValid(x, y)
            if (n in valid):
                msg = tCol.header("Pointing Pair") + " - Reduced cell "
                msg += g.printCell(x,y) + " from " + tCol.warning(str(valid))

                valid.discard(n)
                g.updateCellValid(x, y, valid)

                msg += " to " + tCol.warning(str(valid))
                msg += " using sector " + g.printCell(cx,cy)
                g.logMove(0, msg)
                success = True 
    return success 