from grid import Grid
from colours import tCol
from conjugatePairs import findColumnPairs, findRowPairs
from ajacencyList import AdjacencyList

def xwing(g):

    for n in range(1, 10):
        conjugatePairs = AdjacencyList()
        conjugatePairs = findColumnPairs(g, n, conjugatePairs) i

        print("X-Wing Test for ", n)
        print(conjugatePairs.toString())
   
        # An X-Wing is a formation of two conjugate pairs.
        if (conjugatePairs.getSize() < 2):
            continue
        
        # Gets a list of all cells that are part of a conjugate pair.
        candidateCells = conjugatePairs.getCells()

        # can be at most 18 cells.
        print(candidateCells)



        # Checks for rows with at least two candidate cells.
        for y in range(g.size):
            count = 0
            for i in candidateCells:
                if (i[1] == y):
                    count += 1
            if (count == 2): ### ?


        # check there are two rows which have at least two cells?




    # Must be at least 2 conjugate pairs.
    # Find weak links between conjugate pairs.
    # Can use transpose to do along rows.
    # Modify conjugate pair code to allow for conjugate triples and quads (2 <= N <= 4)

