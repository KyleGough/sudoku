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

def randomGrid():
    return
    

if __name__ == "__main__":
    g = intermediateGridTest()
    g.printClean()
