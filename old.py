
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
