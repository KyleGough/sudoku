from __future__ import absolute_import
import sys
import os
import techniques as t
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
            t.soloCandidate,
            t.hiddenCandidate,
            t.subsetCover,
            t.swordfish,
            t.xwing,
            t.jellyfish
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
    g = Grid()
    size = g.size
    del g


    newGrid = [[0 for i in range(self.size)] for j in range(self.size)]

    if (len(gridStr) != self.size * self.size):
        print("[ " + tCol.FAIL + "Incorrect length of grid input." + tCol.ENDC + " ]")
        return newGrid, False
    c = 0
    for i in gridStr:
        try:
            value = int(i)
        except:
            print("[ " + tCol.FAIL + "Invalid character {" + i + "} in grid input." + tCol.ENDC + " ]")
            return newGrid, False
        newgrid[c % self.size][c // self.size] = value
        c += 1
    return newGrid, True

# Imports test puzzles.
def importTestGrids():
    directory = os.fsencode("tests/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(filename)
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
            yield g
        
# Imports grid, and solves it.
def init():
    # Grid Tests.
    #g = easyGridTest()
    #g = intermediateGridTest()
    #g = difficultGridTest()
    #g = xwingGridTest()
    g = swordfishGridTest()
    #g = jellyfishGridTest()
    #g = pointingPairsGridTest()

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

    ###
    for g in importTestGrids():
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

if __name__ == "__main__":
    importTestGrids()
    init()    