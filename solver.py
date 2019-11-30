import sys
from grid import Grid
from generator import easyGridTest, intermediateGridTest, difficultGridTest
from generator import xwingGridTest, swordfishGridTest, jellyfishGridTest
from generator import pointingPairsGridTest
from gridInit import init
from soloCandidate import soloCandidate
from hiddenCandidate import hiddenCandidate
from subsetCover import subsetCover
from xsj import xwing, swordfish, jellyfish, getStructureName
from colours import tCol

# Tests the grid against the rules and set solution.
def testGrid(g):
        if (g.error):
            print("[ " + tCol.FAIL + "Incorrect value inserted inconsistent with rules" + tCol.ENDC + " ]")
            return False
        elif (not g.checkSolution):
            print("[" + tCol.FAIL + "Incorrect value inserted inconsistent with solution" + tCol.ENDC + " ]")
            return False
        else:
            return True

# Solves a sudoku by applying a list of strategies until new information is obtained.
def strategicSolver(g, show):
    found = True
    print("[" + tCol.OKBLUE, "MOVE", g.move, tCol.ENDC + "]")
    g.logMove(0, tCol.HEADER + "Initial Configuration" + tCol.ENDC)
    g.it += 1

    while (found):
        found = False

        # Prints solution if the grid gets filled.
        if (g.isFilled()):
            print("[" + tCol.OKGREEN, "SOLVED IN", g.move - 1, "MOVES", tCol.ENDC + "]")
            return g, True

        # Print the move count.
        print("[" + tCol.OKBLUE, "MOVE", g.move, tCol.ENDC + "]")
        g.it += 1

        # Displays the grid after each move.
        if (show == "True"):
            print(show)
            g.printClean()

        # Order of strategies.
        strats = [
            soloCandidate,
            hiddenCandidate,
            subsetCover,
            xwing,
            swordfish,
            jellyfish
        ]

        # Executes each strategy in order.
        for func in strats:
            g, found = func(g)
            if (found):
                break
            if (not testGrid(g)):
                return g, False

        # Exhausted Possibilities.
        if (not found):
            print("[" + tCol.FAIL + " EXHAUSTED SEARCH " + tCol.ENDC + "]")

    return g, True


if __name__ == "__main__":
    # Grid Tests.
    g = easyGridTest()
    g = intermediateGridTest()
    g = difficultGridTest()
    g = xwingGridTest()
    g = swordfishGridTest()
    g = jellyfishGridTest()
    g = pointingPairsGridTest()

    # Command Line arguments.
    print("Command Line Arguments")
    show = False
    showValid = False
    if (len(sys.argv) - 1 >= 1):
        g.verbose = int(sys.argv[1])
        print("Verbose set to:", sys.argv[1])
    if (len(sys.argv) - 1 >= 2):
        show = sys.argv[2]
        print("Show grid set to:", sys.argv[2])
    if (len(sys.argv) - 1 >= 3):
        showValid = sys.argv[3]
        print("Show grid valid set to:", sys.argv[3])

    # Initial Grid.
    print("\n[" + tCol.OKGREEN + " INITIAL " + tCol.ENDC + "]")
    g.printClean()
    print()

    # Solves the puzzle.
    g = init(g)
    g, success = strategicSolver(g, show)
    print("\n[" + tCol.OKGREEN + " SOLUTION " + tCol.ENDC + "]")
    g.printClean()
    
    # Shows validities of each cell at the end.
    if (showValid):
        print()
        g.printValid()