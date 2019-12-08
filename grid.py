from copy import deepcopy
from colours import tCol

class Grid:
    def __init__(self):
        self.size = 9
        self.grid = [[0 for i in range(self.size)] for j in range(self.size)]
        self.solution = [[0 for i in range(self.size)] for j in range(self.size)]
        self.valid = [[set() for i in range(self.size)] for j in range(self.size)]
        self.error = False # Error has occurred in the grid.
        self.transposed = False # Is the grid transposed.
        self.move = 0 # Current move.
        self.verbose = True # Flas to display moves.
        self.clues = 0 # Initial numbers on the grid.

    # Sets the grid.
    def setGrid(self, grid):
        count = 0
        self.grid = grid
        for x in range(self.size):
            for y in range(self.size):
                if grid[x][y] != 0:
                    count += 1
        self.clues = count

    # Checks the current grid against the set solution.
    def checkSolution(self):
        for x, y in self.cells():
            value = self.get(x,y)
            if (value != 0 and self.solution[x][y] != 0 and self.solution[x][y] != value):
                return False
        return True

    #
    def log(self, msg):
        if self.verbose:
            print(msg)
    
    # Tests the grid against the rules and set solution.
    def testGrid(self):
        if (self.error):
            self.log("[ " + tCol.FAIL + "Incorrect value inserted inconsistent with rules" + tCol.ENDC + " ]")
            return False
        elif (not self.checkSolution):
            self.log("[" + tCol.FAIL + "Incorrect value inserted inconsistent with solution" + tCol.ENDC + " ]")
            return False
        else:
            return True

    # Clones the grid object.
    def clone(self):
        cp = Grid()
        cp.size = self.size
        cp.grid = [row[:] for row in self.grid]
        cp.solution = [row[:] for row in self.solution]
        cp.valid = [row[:] for row in self.valid]
        cp.error = self.error
        cp.transposed = self.transposed
        cp.move = self.move
        cp.it = self.it
        cp.verbose = self.verbose
        return cp

    # Transposes the grid and valid grid.
    def transpose(self):
        self.transposed = not self.transposed
        self.grid = [list(i) for i in zip(*self.grid)]
        self.valid = [list(i) for i in zip(*self.valid)]

    # Logs a move that yields information.
    def logMove(self, v, msg):
        self.log("[" + tCol.OKBLUE + " MOVE " + str(self.move) + tCol.ENDC + " ] " + msg)
        self.move += 1
    
    # Checks if the grid has been filled.
    def isFilled(self):
        return (sum(x.count(0) for x in self.grid) == 0)

    # Prints the cell position, corrects for if the grid is transposed.
    def printCell(self, x, y):
        msg = tCol.OKBLUE + "("
        msg += str(y+1) + "," + str(x+1) if self.transposed else str(x+1) + "," + str(y+1)
        msg += ")" + tCol.ENDC
        return msg

    # Prints a set.
    def printSet(self, s):
        msg = tCol.WARNING + "{"
        if (len(s) > 0):
            for i in s:
                msg += str(i) + ","
            msg = msg[:-1]            
        else:
            msg += "{}"
        msg += "}" + tCol.ENDC
        return msg

    # Prints the grid contents.
    def printClean(self):
        for y in range(self.size):
            for x in range(self.size):
                print(self.get(x,y), end=" ")
            print()

    # Prints valid values of the grid.
    def printValid(self):
        hSep = tCol.okgreen("█████████████████████████████████████████████████████████████████████████")
        hPt = tCol.okgreen("█") 
        print(hSep)        
        for k in range(self.size):
            for j in [1,4,7]:
                print(hPt, end=' ')
                for x in range(self.size):
                    for i in range(j,j+3):
                        if (self.get(x,k) == 0):
                            if (i in self.getValid(x,k)):
                                if (((x // 3) + (k // 3)) % 2 == 0):
                                    print(tCol.WARNING, end='')
                                else:
                                    print(tCol.FAIL, end='')    
                                print(str(i) + tCol.ENDC, end=' ')
                            else:
                                print(":", end=' ')
                        elif (i == 5):
                            if (((x // 3) + (k // 3)) % 2 == 0):
                                print(tCol.OKBLUE, end='')
                            else:
                                print(tCol.OKGREEN, end='')
                            print(str(self.get(x,k)) + tCol.ENDC, end=' ')
                        else:
                            print(" ", end=' ')

                    print(hPt, end=' ')
                print()
            print(hSep)

    # Row rule.
    def ruleRow(self, x, y, n):
        for i in range(self.size):
            if (self.get(x,i) == n):
                return False
        return True
        
    # Column Rule.
    def ruleColumn(self, x, y, n):
        for i in range(self.size):
            if (self.get(i,y) == n):
                return False
        return True
        
    # Sector Rule.
    def ruleSector(self, x, y, n):
        cx, cy = self.getSectorCoord(x,y)
        for i, j in self.sectorCells():
            if (self.get(cx+i,cy+j) == n):
                return False
        return True

    # Checks if the next move is valid.
    def isValidMove(self, x, y, n):
        return (self.ruleRow(x,y,n) and self.ruleColumn(x,y,n) and self.ruleSector(x,y,n))
        
    # Assigns a grid cell.
    def insert(self, x, y, n):
        if (not self.isValidMove(x,y,n)):
            ###
            print("######")
            print("###ERROR###")
            print("######")
            ###

        # Assign the grid value.
        self.grid[x][y] = n
        # Cell has no more valid values.
        self.updateCellValid(x,y,set())

        # Updates row validities.
        for i in range(self.size):
            if (x != i and self.get(i,y) == 0):
                valid = self.getValid(i,y)
                valid.discard(n)
                if (len(valid) == 0):
                    self.error = True
                self.updateCellValid(i,y,valid)

        # Updates column validities.
        for j in range(self.size):
            if (y != j and self.get(x,j) == 0):
                valid = self.getValid(x,j)
                valid.discard(n)
                if (len(valid) == 0):
                    self.error = True
                self.updateCellValid(x,j,valid)

        # Updates sector validites.
        cx, cy = self.getSectorCoord(x,y)
        for i, j in self.sectorCells():
            if ((cx + i != x or cy + j != y) and self.get(cx + i, cy + j) == 0):
                valid = self.getValid(cx + i, cy + j)
                valid.discard(n)
                if (len(valid) == 0):
                    self.error = True
                self.updateCellValid(cx + i, cy + j, valid)
    
        return True

    # Gets the value of a cell.
    def get(self, x, y):
        return self.grid[x][y]
    
    # Gets the valid values of a cell.
    def getValid(self, x, y):
        val = self.get(x,y)
        if (val == 0):
            return self.valid[x][y]
        else:
            return set()

    # Updates the valid values of a cell.
    def updateCellValid(self, x, y, valid):
        self.valid[x][y] = valid

    # Generator for set of all cell indexes.
    def cells(self):
        for x in range(self.size):
            for y in range(self.size):
                yield x, y

    # Generator for set of all cells not filled.
    def unfilledCells(self):
        for x in range(self.size):
            for y in range(self.size):
                if (self.get(x,y) == 0):
                    yield x, y

    # Generator for cells in a sector.
    def sectorCells(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                yield i, j

    # Gets the centre point coordinate for a sector of a given cell.
    def getSectorCoord(self, x, y):
        cx = ((x // 3) * 3) + 1
        cy = ((y // 3) * 3) + 1
        return cx, cy
