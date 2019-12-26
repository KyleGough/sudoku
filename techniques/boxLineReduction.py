from grid import Grid
from colours import tCol

# Box/Line Reduction.
def boxLineReduction(g):
    return boxLineReductionRow(g) or boxLineReductionRow(g) 

# Performs Box/Line Reduction along grid rows.
# Complexity: O(i * y * x)
def boxLineReductionRow(g):
    success = False

    for i in range(1,10):
        for y in range(g.size):
            cy = ((y // 3) * 3) + 1
            count = 0
            sectors = set()
                    
            # If a value can be i, add what sector the cell is in the set.
            for x in range(g.size):
                if i in g.getValid(x,y):
                    cx = ((x // 3) * 3) + 1
                    sectors.add(tuple([cx, cy]))
                    count += 1

            # Box/Line Intersection detection.
            if ((count == 2 or count == 3) and len(sectors) == 1):
                # Sector intersecting the box/line reduction.            
                s = sectors.pop() 
                for a, b in g.sectorCells():
                    # Ignore if on same y coord.
                    if (y == s[1] + b): 
                        continue
                    valid = g.getValid(s[0] + a, s[1] + b)
                    # Remove possibility of i in the sector cells.
                    if (i in valid):
                        msg = tCol.header("Box/Line Reduction:") + " Reduced cell "
                        msg += g.printCell(s[0] + a, s[1] + b)
                        msg += " from " + g.printSet(valid) + " to "
                        valid.discard(i)
                        msg += g.printSet(valid) + " using "
                        msg += "column " if g.transposed else "row "
                        msg += tCol.okblue(str(y))
                        msg += ", sector " + g.printCell(s[0], s[1])
                        g.logMove(msg) 
                        success = True

    g.transpose()
    return success
