from __future__ import absolute_import
import sys
import os
import techniques as t
import queue
import pandas as pd
from grid import Grid
from init import initGrid
from colours import tCol
from logger import Logger
from datetime import datetime
from stats import Stats

# Order of strategies.
strats = [
    t.soloCandidate,
    t.hiddenCandidate,
    t.subsetCover,
    t.pointingPairs,
    t.boxLineReduction,
    t.xWing, # Single value chaining.
    t.singlesChain, # Single value chaining.
    t.yWing, # Bi-value chaining.
    t.swordfish, # Extension of X-Wing.
    t.jellyfish, # Extension of X-Wing and Swordfish.
    #t.avoidableRect ### Uniqueness Technique.
    t.bivalueUniversalGrave, # Uniqueness Technique.
    t.xyzWing, # Extension of Y-Wing.
    t.wxyzWing, # Extension of XYZ-Wing.
]

# Solves a sudoku by applying a list of strategies until new information is obtained.
def strategicSolver(g, logger):
    g.logMove(tCol.header("Initial Configuration"))
    found = True

    # Applies each technique to the puzzle until new information is gained.
    while (found):
        found = False

        # Prints solution if the grid gets filled.
        if (g.isFilled()):
            if logger.showOutput:
                print("[" + tCol.okgreen(" SOLVED IN " + str(g.stats.moves - 1) + " MOVES ") + "]")
            g.stats.exitStatus = "SOLVED"
            return g.stats

        # Displays the grid after each move.
        if (logger.showAllGrid == "True"):
            g.printCandidates()

        # Executes each strategy in order.
        # If information has been gained, repeat from first strategy.
        for i in range(len(strats)):
            pStart = datetime.now()
            found = strats[i](g)
            pEnd = datetime.now()
            g.stats.techniqueTimes[i] += (pEnd - pStart).total_seconds()
            if (found):
                g.stats.techniqueMoves[i] += 1
                break
            if (not g.testGrid()):
                g.stats.exitStatus = "ERROR"
                return g.stats

        # Exhausted Possibilities. No solution found.
        if (not found):
            g.stats.exitStatus = "EXHAUSTED"
            if (logger.showErrors):
                print("[" + tCol.fail(" EXHAUSTED SEARCH ") + "]")

    return g.stats

# Imports a set grid from a string input.    
def importGrid(gridStr, logger):
    size = 9
    newGrid = [[0 for i in range(9)] for j in range(9)]

    if (len(gridStr) < size * size):
        if (logger.showErrors):
            print("[ " + tCol.fail("Incorrect length of grid input.") + " ]")
        return newGrid, False
    c = 0
    gridStr = gridStr[0:81]
    for i in gridStr:
        try:
            value = int(i)
        except:
            if (logger.showErrors):
                print("[ " + tCol.fail("Invalid character {" + i + "} in grid input.") + " ]")
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
        g.setGrid(grid)
        if (len(ds.columns) == 2): g.solution = solution
        yield g, n + 1

# Imports grid, and solves it.
def init():
    g = Grid()
    logger = Logger()

    # Command Line Arguments.
    filename = str(sys.argv[1])
    logger.showOutput = True if (sys.argv[2] == "0") else False
    logger.showMoves = True if (sys.argv[3] == "0") else False

    # Test set.
    testQueue = queue.Queue()
    statQueue = queue.Queue()
    pStart = datetime.now()
    for g, n in importTestGrids(filename, logger):
        solveGrid(g, n, logger, testQueue, statQueue)
    pEnd = datetime.now()

    print()
    testAnalysis(testQueue)
    print()
    count = statAnalysis(statQueue)
    print()
    timeAnalysis(pEnd - pStart, count)
    
# Test Analysis.
def testAnalysis(testQueue):
    
    totalCount = 0
    solveCount = 0
    exhaustCount = 0
    errorCount = 0

    print("[ " + tCol.warning("Tests") + " ]")

    # Analyses test outcomes.
    while not testQueue.empty():
        t = testQueue.get()
        
        totalCount += 1
        if t[1] == "SOLVED":
            solveCount += 1
        elif t[1] == "EXHAUSTED":
            exhaustCount += 1
        elif t[1] == "ERROR":
            errorCount += 1

    solveRate = str(round(100 * solveCount / totalCount, 1))
    exhaustRate = str(round(100 * exhaustCount / totalCount, 1))
    errorRate = str(round(100 * errorCount / totalCount, 1))

    solveRate = tCol.okgreen(str(solveRate) + "%") if solveRate == "100.0" else tCol.fail(str(solveRate) + "%")
    exhaustRate = tCol.okgreen(str(exhaustRate) + "%") if exhaustRate == "0.0" else tCol.fail(str(exhaustRate) + "%")
    errorRate = tCol.okgreen(str(errorRate) + "%") if errorRate == "0.0" else tCol.fail(str(errorRate) + "%")

    print("Solved:             " + str(solveCount) + " out of " + str(totalCount) + " tests (" + solveRate + ")")
    print("Exhausted:          " + str(exhaustCount) + " out of " + str(totalCount) + " tests (" + exhaustRate + ")")
    print("Errors:             " + str(errorCount) + " out of " + str(totalCount) + " tests (" + errorRate + ")")

# Stat Analysis.
def statAnalysis(statQueue):
    count = 0 # Total number of tests.
    difficultyTotal = 0 # Total of the difficulty values.
    clueTotal = 0 # Total number of clues.
    difficultyMin = 1000000 # Minimum difficulty.
    difficultyMax = 0 # Maximum difficulty.
    techniqueCountTotal = Stats().techniqueMoves # Total amount of each technique used.
    techniqueUsedAmount = Stats().techniqueMoves # Amount of puzzles using each technique.

    techniqueRequiredCount = Stats().techniqueMoves # Number of puzzles requiring featuring a technique.
    techniqueTotalTimes = Stats().techniqueTimes # Total time spend on each technique.

    while not statQueue.empty():
        s = statQueue.get()
        count += 1
        difficulty = s.getDifficulty()
        difficultyTotal += difficulty
        if (difficulty > difficultyMax):
            difficultyMax = difficulty
        if (difficulty < difficultyMin):
            difficultyMin = difficulty
        clueTotal += s.clues
        techniqueCountTotal = [x + y for x, y in zip(techniqueCountTotal, s.techniqueMoves)]
        techniqueUsedAmount = [x + 1 if y > 0 else x for x, y in zip(techniqueUsedAmount, s.techniqueMoves)]
        techniqueTotalTimes = [x + y for x, y in zip(techniqueTotalTimes, s.techniqueTimes)]
        if (s.exitStatus == "SOLVED"):
            for x in range(len(techniqueRequiredCount)):
                if (s.techniqueMoves[x] > 0):
                    techniqueRequiredCount[x] += 1


    difficultyAvg = round(difficultyTotal / count, 0)
    cluesAvg = round(clueTotal / count, 0)
    print("[ " + tCol.warning("Stats") + " ]")
    print("Mean Clues:         " + str(int(cluesAvg)))
    print("Mean Difficulty:    " + str(int(difficultyAvg)))
    print("Min Difficulty:     " + str(difficultyMin))
    print("Max Difficulty:     " + str(difficultyMax))

    techniqueList = [
        "Solo Candidate:     ",
        "Hidden Candidate:   ",
        "Subset Cover:       ",
        "Pointing Pairs:     ",
        "Box/Line Reduction: ",
        "X-Wing:             ",
        "Singles Chain:      ",
        "Y-Wing:             ",
        "Swordfish:          ",
        "Jellyfish:          ",
        "BUG:                ",
        "XYZ-Wing:           ",
        "WXYZ-Wing:          ",
    ]

    padLength = len(str(count)) + 2
    timeThreshold = sorted(techniqueTotalTimes, reverse=True)[4]

    for i in range(len(techniqueList)):
        msg = techniqueList[i] + printTechniqueUsed(techniqueCountTotal[i])
        msg += str(techniqueCountTotal[i]).rjust(padLength, ' ')
        usedAmount = "{:.1f}".format(100 * techniqueUsedAmount[i] / count) + "%" 
        usedAmount = usedAmount.rjust(8, ' ')
        msg +=  tCol.okblue(usedAmount)
        msg += str(techniqueRequiredCount[i]).rjust(padLength, ' ')
        totalTime = techniqueTotalTimes[i]
        if (totalTime >= timeThreshold and totalTime > 0):
            msg += tCol.fail("  {:.2f}s".format(totalTime))
        else:
            msg += tCol.okgreen("  {:.2f}s".format(totalTime))
        print(msg)

    return count

# Prints the number of times a technique has been used.
def printTechniqueUsed(count):
    if (count == 0):
        msg = tCol.fail("False ")
    else:
        msg = tCol.okgreen("True  ")
    return msg

# Time Analysis.
def timeAnalysis(timeElapsed, count):
    print("[ " + tCol.warning("Time") + " ]")
    print("Time Elapsed:       " + "{:.2f}".format(timeElapsed.total_seconds()) + "s")
    print("Mean Time Elapsed:  " + "{:.3f}".format(timeElapsed.total_seconds() / count) + "s")
    

# Attempts the solve the given grid.
def solveGrid(g, n, logger, testQueue, statQueue):
    # Initial Grid.
    if logger.showOutput:
        print("\n[ " + tCol.okgreen("Test " + str(n)) + " ]")        
        print("[ " + tCol.okgreen("INITIAL") + " ]")
        g.printGrid()
        print()

    # Solves the puzzle.
    g = initGrid(g)
    g.verbose = logger.showMoves
    stats = strategicSolver(g, logger)
    if logger.showOutput:
        # Difficulty analysis.
        print("\n[ " + tCol.okgreen("DIFFICULTY") + " ]")
        stats.print()
        # Solution.
        print("\n[ " + tCol.okgreen("SOLUTION") + " ]")
        g.printGrid()

    # Adds to the test queue.
    testQueue.put([n, g.stats.exitStatus])
    # Adds to the stats queue.
    statQueue.put(stats)

if __name__ == "__main__":
    init()    
