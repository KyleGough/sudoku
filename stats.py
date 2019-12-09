from colours import tCol

class Stats:
    def __init__(self):
        self.moves = 0
        self.clues = 0
        self.techniqueMoves = [0,0,0,0,0,0,0,0]

    def print(self): 
        msg = "Moves: " + tCol.warning(str(self.moves))
        msg += ", Clues: " + tCol.warning(str(self.clues))
        msg += ", Techniques: " + tCol.okblue(str(self.techniqueMoves))
        msg += ", Difficulty: " + tCol.fail(str(self.getDifficulty()))
        print(msg)

    def getDifficulty(self):
        difficulty = 0
        for i in range(len(self.techniqueMoves)):
            difficulty += (i + 1) * self.techniqueMoves[i]
        return difficulty