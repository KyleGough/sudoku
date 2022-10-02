import math
from colours import tCol

class Stats:
    def __init__(self):
        self.moves = 0 # Number of moves executed to solve the grid.
        self.clues = 0 # Number of initial clues in the puzzle.
        self.techniqueMoves = [0,0,0,0,0,0,0,0,0,0,0,0,0,0] # Number of times each technique is used.
        self.techniqueTimes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0] # Time spent performing each technique.
        self.exitStatus = "INCOMPLETE" # {INCOMPLETE | SOLVED | EXHAUSTED | ERROR}

    # Prints sudoku statistics.
    def print(self): 
        msg = "Moves: " + tCol.warning(str(self.moves))
        msg += ", Clues: " + tCol.warning(str(self.clues))
        msg += ", Difficulty: " + tCol.fail(str(self.getDifficulty()))
        print(msg)

    # Calculates the relative difficulty of the sudoku.
    def getDifficulty(self):
        difficulty = 0
        n = 1
        for i in range(len(self.techniqueMoves)):
            n += math.floor(math.log(i+1,2))
            difficulty += (n * self.techniqueMoves[i])
        return difficulty
