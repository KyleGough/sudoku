from __future__ import absolute_import
import sys
import os
import techniques as t
import queue
from grid import Grid
from generator import easyGridTest, intermediateGridTest, difficultGridTest
from generator import xwingGridTest, swordfishGridTest, jellyfishGridTest
from generator import pointingPairsGridTest
from gridInit import initGrid
from colours import tCol

# Solves a sudoku by applying a list of strategies until new information is obtained.
def strategicSolver(g, show):
    found = True
    g.logMove(0, tCol.HEADER + "Initial Configuration" + tCol.ENDC)

    while (found):
        found = False

        # Prints solution if the grid gets filled.
        if (g.isFilled()):
            print("[" + tCol.OKGREEN, "SOLVED IN", g.move - 1, "MOVES", tCol.ENDC + "]")
            return g, True

        # Displays the grid after each move.
        if (show == "True"):
            print(show)
            g.printValid()

        # Order of strategies.
        strats = [
            # Cell can only be one possible value.
            t.soloCandidate,
            # Value can only occur in one cell of a column/row/sector.
            t.hiddenCandidate,
            # Subsets of pairs/triples/quads to remove possibilities.
            t.subsetCover,
            # Uses pairs/triples of possible values in a sector that are on
            # the same row/column to eliminate possibilities in the row/column.
            t.pointingPairs,
            # Value restricted in n places along a column in n columns
            # that all share the same rows. 
            t.jellyfish, 
            t.swordfish,
            t.xwing             
        ]

        # Executes each strategy in order.
        for func in strats:
            g, found = func(g)
            if (found):
                break
            if (not g.testGrid()):
                return g, False

        # Exhausted Possibilities.
        if (not found):
            print("[" + tCol.FAIL + " EXHAUSTED SEARCH " + tCol.ENDC + "]")

    return g, True

# Imports a set grid from a string input.    
def importGrid(gridStr):
    size = 9
    newGrid = [[0 for i in range(9)] for j in range(9)]

    print(len(gridStr))
    if (len(gridStr) < size * size):
        print("[ " + tCol.FAIL + "Incorrect length of grid input." + tCol.ENDC + " ]")
        return newGrid, False
    c = 0
    gridStr = gridStr[0:81]
    for i in gridStr:
        try:
            value = int(i)
        except:
            print("[ " + tCol.FAIL + "Invalid character {" + i + "} in grid input." + tCol.ENDC + " ]")
            return newGrid, False
        newGrid[c % size][c // size] = value
        c += 1
    return newGrid, True

# Imports test puzzles.
def importTestGrids():
    # Test puzzle directory.
    directory = os.fsencode("tests/")

    # Iterate over files in the directory.
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"): 
            f = open("tests/" + filename, "r")
            txtGrid = f.readline()
            txtSolution = f.readline()
            # Imports the initial grid and corresponding solution.
            grid, success = importGrid(txtGrid)
            if (not success):
                continue
            solution, success = importGrid(txtSolution)
            if (not success):
                continue

            # Creates a new grid object.
            g = Grid()
            g.grid = grid
            g.solution = solution
            yield g, filename
        
# Imports grid, and solves it.
def init():
    # Grid Tests.
    #g = easyGridTest()
    #g = intermediateGridTest()
    #g = difficultGridTest()
    #g = xwingGridTest()
    #g = swordfishGridTest()
    #g = jellyfishGridTest()
    g = pointingPairsGridTest()

    # Command Line arguments.
    show = False
    showValid = False
    if (len(sys.argv) - 1 >= 1):
        g.verbose = int(sys.argv[1])
        print("[" + tCol.OKGREEN + "Verbose" + tCol.ENDC + "]: " + sys.argv[1])
    if (len(sys.argv) - 1 >= 2):
        show = sys.argv[2]
        print("[" + tCol.OKGREEN + "Show Grid" + tCol.ENDC + "]: " + sys.argv[2])
    if (len(sys.argv) - 1 >= 3):
        print("[" + tCol.OKGREEN + "Import Grid" + tCol.ENDC + "]: " + sys.argv[3])
        if (not g.importGrid(sys.argv[3])):
            return

    # Tests.
    testQueue = queue.Queue()
    for g, filename in importTestGrids():
        solveGrid(g, filename, show, showValid, testQueue)

    # Prints the test outcomes.  
    print("\n[", tCol.WARNING + "Tests" + tCol.ENDC, "]")
    while not testQueue.empty():
        t = testQueue.get()
        if (t[1]):
            print("[" + tCol.OKGREEN + "Pass" + tCol.ENDC + "]: " + t[0])
        else:
            print("[" + tCol.FAIL + "Fail" + tCol.ENDC + "]: " + t[0])
        
# Attempts the solve the given grid.
def solveGrid(g, filename, show, showValid, testQueue):
    # File Name.
    print("\n[" + tCol.OKGREEN, filename, tCol.ENDC + "]")
    
    # Initial Grid.
    print("\n[" + tCol.OKGREEN + " INITIAL " + tCol.ENDC + "]")
    g.printClean()
    print()

    # Solves the puzzle.
    g = initGrid(g)
    g, success = strategicSolver(g, show)
    print("\n[" + tCol.OKGREEN + " SOLUTION " + tCol.ENDC + "]")
    g.printClean()
    print()
    g.printValid()

    # Adds to the test queue.
    testQueue.put([filename, g.isFilled()])

if __name__ == "__main__":
    importTestGrids()
    init()    