from __future__ import absolute_import
import sys
import os
import techniques as t
import queue
import pandas as pd
from grid import Grid
from generator import easyGridTest, intermediateGridTest, difficultGridTest
from generator import xwingGridTest, swordfishGridTest, jellyfishGridTest
from generator import pointingPairsGridTest
from gridInit import initGrid
from colours import tCol

class Logger:
    def __init__(self):
        self.showOutput = False
        self.showMoves = False # Shows/Hides the moves performed by the solver.
        self.showErrors = False # Shows/Hides error messages.
        self.showOther = False
        self.showAllGrid = False # Show/Hides the grid after each move.
        self.showGridLarge = False


# Solves a sudoku by applying a list of strategies until new information is obtained.
def strategicSolver(g, logger):
    g.logMove(0, tCol.HEADER + "Initial Configuration" + tCol.ENDC)
    found = True

    # Order of strategies.
    strats = [
        # Cell can only be one possible value.
        t.soloCandidate,
        # Value can only occur in one cell of a column/row/sector.
        # 17-clue test coverage: 44.6%.
        t.hiddenCandidate, 
        # Subsets of pairs/triples/quads to remove possibilities.
        # 17-clue test coverage: 68.6%.
        t.subsetCover, 
        # Uses pairs/triples of possible values in a sector that are on
        # the same row/column to eliminate possibilities in the row/column.
        # 17-clue test coverage: 77.5%.
        t.pointingPairs,
        # Value restricted in n places along a column in n columns
        # that all share the same rows.
        # 17-clue test coverage: ???. 
        t.jellyfish, 
        t.swordfish,
        t.xwing             
    ]

    # Applies each technique to the puzzle until new information is gained.
    while (found):
        found = False

        # Prints solution if the grid gets filled.
        if (g.isFilled()):
            if logger.showOther:
                print("[" + tCol.OKGREEN + " SOLVED IN " + str(g.move - 1) + " MOVES " + tCol.ENDC + "]")
            return g, True

        # Displays the grid after each move.
        if (logger.showAllGrid == "True"):
            g.printValid()

        # Executes each strategy in order.
        # If information has been gained, repeat from first strategy.
        for func in strats:
            g, found = func(g)
            if (found):
                break
            if (not g.testGrid()):
                return g, False

        # Exhausted Possibilities. No solution found.
        if (not found and logger.showErrors):
            print("[" + tCol.FAIL + " EXHAUSTED SEARCH " + tCol.ENDC + "]")

    return g, True

# Imports a set grid from a string input.    
def importGrid(gridStr, logger):
    size = 9
    newGrid = [[0 for i in range(9)] for j in range(9)]

    if (len(gridStr) < size * size):
        if (logger.showErrors):
            print("[ " + tCol.FAIL + "Incorrect length of grid input." + tCol.ENDC + " ]")
        return newGrid, False
    c = 0
    gridStr = gridStr[0:81]
    for i in gridStr:
        try:
            value = int(i)
        except:
            if (logger.showErrors):
                print("[ " + tCol.FAIL + "Invalid character {" + i + "} in grid input." + tCol.ENDC + " ]")
            return newGrid, False
        newGrid[c % size][c // size] = value
        c += 1
    return newGrid, True

# Imports test puzzles.
def importTestGrids(filename, logger):
    # Reads data from the csv file.
    ds = pd.read_csv(filename, header=None, converters={0: lambda x: str(x), 1: lambda x: str(x)})

    # Iterates over each row (Initial grid/Solution pair).
    for n, row in ds.iterrows():
        txtGrid = str(row[0])
        # Imports the initial grid.
        grid, success = importGrid(txtGrid, logger)
        if (not success):
            continue
        # Imports the solution.
        if (len(ds.columns) == 2):
            txtSolution = str(row[1])
            solution, success = importGrid(txtSolution, logger)
            if (not success):
                continue

        # Creates a new grid object.
        g = Grid()
        g.grid = grid
        if (len(ds.columns) == 2): g.solution = solution
        yield g, n + 1

# Imports grid, and solves it.
def init():
    g = Grid()
    logger = Logger()

    if (len(sys.argv) - 1 == 1):
        filename = str(sys.argv[1])
    else:
        print("No input CSV file specified.")
        return    
    #filename = "datasets/daily-05-12-2019.csv"
    
    # Test set.
    testQueue = queue.Queue()
    for g, n in importTestGrids(filename, logger):
        solveGrid(g, n, logger, testQueue)
  
    passCount = 0
    failCount = 0
    print("\n[", tCol.WARNING + "Tests" + tCol.ENDC, "]")

    # Analyses test outcomes.
    while not testQueue.empty():
        t = testQueue.get()
        if (t[1]):
            passCount += 1
        else:
            failCount += 1
        sys.stdout.write("\r - Solved " + str(passCount) + " out of " + str(passCount + failCount) + " tests.\t")
        sys.stdout.flush()

    # Prints the test outcomes.
    #print("Passed: " + str(passCount) + " [ " + str(100 * passCount / (passCount + failCount)) + "% ]")
    #print("Failed: " + str(failCount) + " [ " + str(100 * failCount / (passCount + failCount)) + "% ]")

# Attempts the solve the given grid.
def solveGrid(g, n, logger, testQueue):
    # Initial Grid.
    if logger.showOutput:
        print("\n[" + tCol.OKGREEN + "Test " + str(n) + tCol.ENDC + "]")        
        print("\n[" + tCol.OKGREEN + " INITIAL " + tCol.ENDC + "]")
        if logger.showGridLarge:
            g.printValid()
        else:
            g.printClean()
        print()

    # Solves the puzzle.
    g = initGrid(g)
    g.verbose = logger.showMoves
    g, success = strategicSolver(g, logger)
    if logger.showOutput:
        print("\n[" + tCol.OKGREEN + " SOLUTION " + tCol.ENDC + "]")
        if logger.showGridLarge:
            g.printValid()
        else:
            g.printClean()

    # Adds to the test queue.
    testQueue.put([n, g.isFilled()])

if __name__ == "__main__":
    init()    