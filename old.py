
#
# Structure for example could be: X-Wing, Swordfish, Jellyfish, etc.
def xwing(g, k):
    # Row candidates for X-Wing.
    candidates = set()
    candidateColumns = []

    # Iterate over rows.
    for y in range(g.size):
        # Count empty cells in the row.
        empty = 0
        columns = set()
        for x in range(g.size):
            if (g.get(y,x) == 0):#***
                empty += 1
                columns.add(x)
        # Add as X-Wing candidate.
        if (empty == k):
            candidates.add(y)
            candidateColumns.append(columns)

    print(candidates)
    print(candidateColumns)

    ys = candidates
    if (len(ys) == k):
        xs = candidateColumns[0]
        count = candidateColumns.count(xs)
        if (count == len(candidateColumns)):######
            # Possible values that can occupy all cells of the structure.
            candidateValues = {1,2,3,4,5,6,7,8,9}
            for a in xs:
                for b in ys:
                    candidateValues = candidateValues.intersection(g.getValid(b,a))#***
            if (len(candidateValues) == 1):
                print("X-Wing found.")
                g, success = xwingExecute(g, xs, ys, k, candidateValues.pop())
                return g, success
            
    return g, False


###8 moves beforehand
###30 moves with h4
def h3(g):
    for x, y in g.unfilledCells():
        valid = g.getValid(x,y)

        # Row.
        rowValid = set()
        for i in range(g.size):
            if (i != x):
                rowValid.update(g.getValid(i,y))
        for v in valid:
            if (not v in rowValid):
                g.insert(x,y,v)
                print("[H3]")
                return g, True

        # Column.
        columnValid = set()
        for j in range(g.size):
            if (j != y):
                columnValid.update(g.getValid(x,j))
        for v in valid:
            if (not v in columnValid):
                g.insert(x,y,v)
                print("[H3]")
                return g, True

        # Sector.
        sectorValid = set()
        cx, cy = g.getSectorCoord(x,y)
        for i, j in g.sectorCells():
            if (i != x or j != y):
                sectorValid.update(g.getValid(cx + i, cy + j))
        for v in valid:
            if (not v in sectorValid):
                g.insert(x,y,v)
                print("[H3]")
                return g, True
        
    return g, False

#
def h4(g, depth):
    print("H4 START", depth)
    if (depth >= 2):###
        print("Maximum depth reached.")
        return g, False

    for x, y in g.unfilledCells():
        valid = g.getValid(x,y)
        if (len(valid) == 0):
            return g, False
        assumption = valid.pop()

        cp = g.clone()

        g.printValid()###

        print("sep===========+++")
        cp.insert(x,y,assumption)
        cp.printValid()###
        cp, success = strategicSolver(cp, depth + 1)

        if (not success):
            valid.discard(assumption)
            g.updateCellValid(x, y, valid)
            if (depth == 0): print("Contradiction in cell", x+1, y+1, " cannot be value", assumption, "[H4]")
            return g, True
        else:
            print("?????")###
            continue

    return g, False
