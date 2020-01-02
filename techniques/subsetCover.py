from grid import Grid
from colours import tCol
from itertools import chain, combinations

# Uses subset cover inconsistencies to eliminate values.
def subsetCover(g):
    success = rowSubsetCover(g)
    if (success): return success
    g.transpose()
    success = rowSubsetCover(g)
    g.transpose()
    if (success): return success
    success = sectorSubsetCover(g)
    return success

# Returns the structure name for a given n.
def getTitleName(n):
    if (n == 2):
        return "Subset Cover (Pairs):"
    elif (n == 3):
        return "Subset Cover (Triples):"
    else:
        return "Subset Cover (Quads):"
    
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
                if (g.get(cx + i, cy + j) == 0) and (len(g.getCandidates(cx + i, cy + j)) <= 4): ###
                    empty.append([i,j])
            if (len(empty) < 3):
                continue

            # Permutes the list of empty cells.
            perm = list(chain.from_iterable(combinations(empty, r) for r in range(len(empty))))
            # Filter permutations of length at least 2.
            perm = [i for i in perm if (len(i) >= 2 and len(i) <= 4)]

            # Test each permutation.
            for p in perm:
                candidateSubset = set()
                for i in p:
                    candidateSubset.update(g.getCandidates(cx + i[0], cy + i[1]))
                if (len(candidateSubset) != len(p)):
                    continue

                # Uses subset cover to eliminate values in other cells of the row.
                for a, b in g.sectorCells():
                    if (not [a, b] in p and g.get(cx + a, cy + b) == 0):
                        
                        cellCandidates = g.getCandidates(cx + a, cy + b)
                        msg = tCol.header(getTitleName(len(p)))
                        msg += " Using " + g.printSet(candidateSubset) + " in sector"
                        msg += ", reduced cell " + g.printCell(cx + a, cy + b)
                        msg += " from " + g.printSet(cellCandidates) + " to "
                        
                        # Removes possible values if in v.
                        removed = False
                        for v in candidateSubset:
                            if (v in cellCandidates):
                                removed = True
                                cellCandidates.discard(v)
                        # Update cell.            
                        if (removed):
                            msg += g.printSet(cellCandidates)
                            g.logMove(msg)
                            success = True

                if (success):
                    return True
            
    return success

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
            if (g.get(x,y) == 0) and (len(g.getCandidates(x,y)) <= 4): ###
                empty.append(x)
        if (len(empty) < 3):
            continue

        # Permutes the list of empty cells.
        perm = list(chain.from_iterable(combinations(empty, r) for r in range(len(empty))))
        # Filter permutations of length at least 2.
        perm = [i for i in perm if (len(i) >= 2 and len(i) <= 4)] 

        # Test each permutation.
        for p in perm:
            candidateSubset = set()
            for i in p:
                candidateSubset.update(g.getCandidates(i,y))
            if (len(candidateSubset) != len(p)):
                continue

            # Uses subset cover to eliminate values in other cells of the row.
            for x in range(g.size):
                if (not x in p and g.get(x,y) == 0):
                    cellCandidates = g.getCandidates(x,y)
                    msg = tCol.header(getTitleName(len(p)))
                    msg += " Using " + g.printSet(candidateSubset) + " in "
                    msg += "column" if g.transposed else "row"
                    msg += ", reduced cell " + g.printCell(x,y)
                    msg += " from " + g.printSet(cellCandidates) + " to "
                    
                    # Removes possible values if in v.
                    removed = False
                    for v in candidateSubset:
                        if (v in cellCandidates):
                            removed = True
                            cellCandidates.discard(v)
                    # Update cell.
                    if (removed):
                        msg += g.printSet(cellCandidates)
                        g.logMove(msg)
                        success = True

    return success
