from generator import easyGridTest, intermediateGridTest
from grid import Grid

# Checks conflicts in a row.
def checkRow(g, y):
    perm = set()
    for x in range(g.size):
        a = g.get(x,y)
        if (a != 0):
            perm.add(a)
    return perm

# Checks conflicts in a column.
def checkColumn(g, x):
    perm = set()
    for y in range(g.size):
        a = g.get(x,y)
        if (a != 0):
            perm.add(a)
    return perm

# Checks conflicts in a sector.
def checkSector(g, x, y):
    perm = set()
    cx = ((x // 3) * 3) + 1
    cy = ((y // 3) * 3) + 1
    for i in range(-1, 2):
        for j in range(-1, 2):
            perm.add(g.get(cx + i,cy + j))
    return perm

# Checks all conflicts for a given cell.
def checkCell(g, x, y):
    # Conflicting values.
    conflicts = checkRow(g, y)
    conflicts.update(checkColumn(g, x))
    conflicts.update(checkSector(g, x, y))
    # Removes empty cells (0).
    conflicts = set([y for y in conflicts if y != 0])
    # Possibilities.
    poss = {1,2,3,4,5,6,7,8,9}
    return poss - conflicts


def normalPass(g):
    for x in range(g.size):
        for y in range(g.size):
            if (g.get(x,y) == 0):
                poss = checkCell(g, x, y)

                if (len(poss) == 1):
                    # New cell value.
                    a = poss.pop()
                    g.updateCellValid(x, y, poss)

                    # Logging.
                    print(a, "- in cell ", x+1, y+1, "due to ruleset. [H1]")

                    # Failsafe.
                    if (not g.isValidMove(x,y,a)):
                        print("Invalid Move. [ER]")

                    # Update Board.
                    g.insert(x,y,a)
                    return g, True

                

    print("Exhausted Search. [EX]")
    return g, False


#row set cover inconstency.
#for each cell.
#check union of valids of other cell.
#if len == empty cells.
#remove valid from cell


# Updates the valid cells for every cell on the board.
def updateAllValid(g):
    for x in range(g.size):
        for y in range(g.size):
            if (g.get(x,y) == 0):
                poss = checkCell(g, x, y)
                g.updateCellValid(x, y, poss)
    return g

#
def strategicSolver(g):
    g = updateAllValid(g)
    return g


if __name__ == "__main__":
    ex = False
    g = easyGridTest()
    #g = intermediateGridTest()

    for i in range(200):
        print("======[", i , "]======")
        g.printClean()
        g, ex = normalPass(g)
        if (not ex):
            break
        
    #If search has been exhausted, terminate.
    if (ex):
        print("[SOLVED IN", i, " moves]")
        g.printClean()
        #g = updateAllValid(g)
        #g.printValid()