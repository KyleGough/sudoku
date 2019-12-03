from grid import Grid
from colours import tCol
from itertools import chain, combinations

# Uses subset cover inconsistencies to eliminate values.
def subsetCover(g):
    g, success = rowSubsetCover(g)
    if (success): return g, success
    g.transpose()
    g, success = rowSubsetCover(g)
    g.transpose()
    if (success): return g, success
    g, success = sectorSubsetCover(g)
    return g, success

# Returns the structure name for a given n.
def getTitleName(n):
    if (n == 2):
        return "Subset Cover [Pairs]"
    elif (n == 3):
        return "Subset Cover [Triples]"
    else:
        return "Subset Cover [Quads]"
    
# Sector subset cover.
def sectorSubsetCover(g):
    success = False

    # Iterates over the sector midpoints.
    for cx in range(1,8,3):
        for cy in range(1,8,3):

            # Gets the indexes of cells in the sector that are empty.
            empty = []
            # Iterate over cells in the sector.
            for i, j in g.sectorCells():
                if (g.get(cx + i, cy + j) == 0):
                    empty.append([i,j])
            if (len(empty) < 3):
                continue

            # Permutes the list of empty cells.
            perm = list(chain.from_iterable(combinations(empty, r) for r in range(len(empty))))
            # Filter permutations of length at least 2.
            perm = [i for i in perm if (len(i) >= 2 and len(i) <= 4)]

            # Test each permutation.
            for p in perm:
                valid = set()
                for i in p:
                    valid.update(g.getValid(cx + i[0], cy + i[1]))
                if (len(valid) != len(p)):
                    continue

                # Uses subset cover to eliminate values in other cells of the row.
                for a, b in g.sectorCells():
                    if (not [a, b] in p and g.get(cx + a, cy + b) == 0):
                        
                        cellValid = g.getValid(cx + a, cy + b)
                        msg = tCol.HEADER + getTitleName(len(p)) + tCol.ENDC
                        msg += " - Using " + tCol.WARNING
                        msg += str(valid) + tCol.ENDC + " in 3x3 sector"
                        msg += ", reduced cell " + g.printCell(cx + a, cy + b)
                        msg += " from " + tCol.WARNING + str(cellValid) + tCol.ENDC + " to "
                        
                        # Removes possible values if in v.
                        removed = False
                        for v in valid:
                            if (v in cellValid):
                                removed = True
                                cellValid.discard(v)
                        # Update cell.            
                        if (removed):
                            g.updateCellValid(cx + a, cy + b, cellValid)
                            msg += tCol.WARNING + str(cellValid) + tCol.ENDC
                            g.logMove(0, msg)
                            success = True

                if (success):
                    return g, True
            
    return g, success

# Subset cover along rows.
# Complexity: O(y * perm(X) * x)###
def rowSubsetCover(g):
    success = False
    # Iterate over rows.
    for y in range(g.size):
        
        # Gets the indexes of cells in the row that are empty.
        empty = []
        # Iterate over cells in a row.
        for x in range(g.size):
            if (g.get(x,y) == 0):
                empty.append(x)
        if (len(empty) < 3):
            continue

        # Permutes the list of empty cells.
        perm = list(chain.from_iterable(combinations(empty, r) for r in range(len(empty))))
        # Filter permutations of length at least 2.
        perm = [i for i in perm if (len(i) >= 2 and len(i) <= 4)] 

        # Test each permutation.
        for p in perm:
            valid = set()
            for i in p:
                valid.update(g.getValid(i,y))
            if (len(valid) != len(p)):
                continue

            # Uses subset cover to eliminate values in other cells of the row.
            for x in range(g.size):
                if (not x in p and g.get(x,y) == 0):
                    cellValid = g.getValid(x,y)
                    msg = tCol.HEADER + getTitleName(len(p)) + tCol.ENDC
                    msg += " - Using " + tCol.WARNING
                    msg += str(valid) + tCol.ENDC + " in "
                    msg += "column" if g.transposed else "row"
                    msg += ", reduced cell " + g.printCell(x,y)
                    msg += " from " + tCol.WARNING + str(cellValid) + tCol.ENDC + " to "
                    
                    # Removes possible values if in v.
                    removed = False
                    for v in valid:
                        if (v in cellValid):
                            removed = True
                            cellValid.discard(v)
                    # Update cell.
                    if (removed):
                        msg += tCol.WARNING + str(cellValid) + tCol.ENDC
                        g.updateCellValid(x, y, cellValid)
                        g.logMove(0, msg)
                        success = True

    return g, success