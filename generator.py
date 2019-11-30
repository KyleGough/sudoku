from random import randint
from random import seed
from grid import Grid

# Easy level sudoku.
# Can be solved with just the simple ruleset.
def easyGridTest():
    g = Grid()
    g.grid = [
        [0,6,1,8,0,0,0,0,7],
        [0,8,9,2,0,5,0,4,0],
        [0,0,0,0,4,0,9,0,3],
        [2,0,0,1,6,0,3,0,0],
        [6,7,0,0,0,0,0,5,1],
        [0,0,4,0,2,3,0,0,8],
        [7,0,5,0,9,0,0,0,0],
        [0,9,0,4,0,2,7,3,0],
        [1,0,0,0,0,8,4,6,0]]
    return g

# Intermediate level sudoku.
# Cannot be solved with just the simple ruleset.
def intermediateGridTest():
    g = Grid()
    g.grid = [
      [0,5,0,3,6,0,0,0,0],
      [2,8,0,7,0,0,0,0,0],
      [0,0,0,0,0,8,0,9,0],
      [6,0,0,0,0,0,0,8,3],
      [0,0,4,0,0,0,2,0,0],
      [8,9,0,0,0,0,0,0,6],
      [0,7,0,5,0,0,0,0,0],
      [0,0,0,0,0,1,0,3,9],
      [0,0,0,0,4,3,0,6,0]]
    return g

# Impossible level sudoku.
# Requires multiple heuristics to solve.
def difficultGridTest():
    g = Grid()
    g.grid = [
        [0,7,0,0,0,0,0,9,0],
        [0,0,0,0,5,0,4,0,2],
        [0,0,0,0,0,0,0,3,0],
        [6,0,0,0,1,3,2,0,0],
        [0,0,9,0,8,0,0,0,0],
        [0,3,1,0,0,6,0,0,0],
        [4,6,0,0,0,0,0,0,1],
        [0,0,8,0,0,4,6,0,0],
        [0,0,0,0,3,5,0,0,0]]
    return g

# X-Wing sudoku.
# Requires use of X-wing to solve.
def xwingGridTest():
    g = Grid()
    g.grid = [
        [0,7,0,0,0,0,2,0,9],
        [0,6,9,7,0,8,4,1,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,7,0,1,0,0],
        [0,1,0,5,0,3,0,9,0],
        [0,0,2,0,9,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,5,8,1,0,6,7,4,0],
        [4,0,1,0,0,0,0,5,0]]

    g.grid = [
        [1,4,0,0,0,2,0,9,6],
        [0,0,5,0,0,0,4,0,2],
        [0,2,0,0,0,8,0,0,1],
        [0,0,0,6,0,0,5,0,0],
        [0,0,0,4,1,3,0,0,0],
        [0,0,9,0,0,5,0,0,0],
        [5,0,0,8,0,0,0,4,0],
        [6,0,4,0,0,0,1,0,0],
        [9,8,0,1,0,0,0,2,5]]
    return g

# Swordfish sudoku.
# Requires use of the Swordfish strategy to solve.
def swordfishGridTest():
    g = Grid()
    g.grid = [
        [5,0,0,0,0,1,0,2,9],
        [0,0,0,0,0,9,0,0,0],
        [0,6,3,2,0,0,0,0,0],
        [0,0,2,3,0,0,0,8,0],
        [1,0,0,0,5,0,0,0,4],
        [0,3,0,0,0,7,9,0,0],
        [0,0,0,0,0,5,4,6,0],
        [0,0,0,7,0,0,0,0,0],
        [3,2,0,6,0,0,0,0,5]]
    return g

# Jellyfish sudoku.
# Requires use of the Jellyfish strategy to solve.
def jellyfishGridTest():
    g = Grid()
    g.grid = [
        [0,0,0,0,0,0,0,0,0],
        [0,7,1,0,0,5,9,0,4],
        [0,0,9,4,0,7,5,0,2],
        [0,0,0,0,0,0,1,0,3],
        [0,3,2,0,0,9,4,0,6],
        [0,0,5,0,0,0,0,0,7],
        [0,9,6,2,0,4,3,0,5],
        [0,9,6,2,0,4,3,0,5],
        [0,0,0,0,0,0,0,0,0]]
    return g


if __name__ == "__main__":
    print("Easy Test")
    easyGridTest().printClean()
    print("Intermediate Test")
    intermediateGridTest().printClean()
    print("X-Wing Test")
    xwingGridTest().printClean()
    print("Swordfish Test")
    swordfishGridTest().printClean()
    print("Jellyfish Test")
    jellyfishGridTest().printClean()
    print("Impossible Test")
    difficultGridTest.printClean()   
