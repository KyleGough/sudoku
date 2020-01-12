from colours import tCol
from stats import Stats

class Grid:
    def __init__(self):
        self.size = 9 # Size of the grid.
        self.clue = [[False for i in range(self.size)] for j in range(self.size)] # Initial clue locations.
        self.grid = [[0 for i in range(self.size)] for j in range(self.size)] # Current grid values.
        self.solution = [[0 for i in range(self.size)] for j in range(self.size)] # Solution of the puzzle.
        self.candidates = [[set() for i in range(self.size)] for j in range(self.size)] # Candidates in each cell.
        self.error = False # Error has occurred in the grid.
        self.transposed = False # Is the grid transposed.
        self.verbose = True # Flag to display moves.
        self.stats = Stats() # Puzzle difficulty analysis.
        
    # Sets the grid.
    def setGrid(self, grid):
        count = 0
        self.grid = grid
        for x in range(self.size):
            for y in range(self.size):
                if grid[x][y] != 0:
                    self.clue[x][y] = True
                    count += 1
        self.stats.clues = count

    # Checks the current grid against the set solution.
    def checkSolution(self):
        for x, y in self.cells():
            value = self.get(x,y)
            if (value != 0 and self.solution[x][y] != 0 and self.solution[x][y] != value):
                return False
        return True
    
    # Tests the grid against the rules and set solution.
    def testGrid(self):
        if (self.error):
            print("[ " + tCol.fail("Incorrect value inserted inconsistent with rules") + " ]")
            return False
        elif (not self.checkSolution):
            print("[" + tCol.fail("Incorrect value inserted inconsistent with solution") + " ]")
            return False
        else:
            return True

    # Transposes the grid and candidate grid.
    def transpose(self):
        self.transposed = not self.transposed
        self.grid = [list(i) for i in zip(*self.grid)]
        self.candidates = [list(i) for i in zip(*self.candidates)]

    # Logs a move that yields information.
    def logMove(self, msg):
        if (self.verbose):
            print("[" + tCol.okblue(" MOVE " + str(self.stats.moves)) + " ] " + msg)
        self.stats.moves += 1
    
    # Checks if the grid has been filled.
    def isFilled(self):
        return (sum(x.count(0) for x in self.grid) == 0)

    # Prints the cell position, corrects for if the grid is transposed.
    def printCell(self, x, y):
        msg = tCol.OKBLUE + "("
        msg += str(y+1) + "," + str(x+1) if self.transposed else str(x+1) + "," + str(y+1)
        msg += ")" + tCol.ENDC
        return msg

    # Prints a set object , sorted and compact.
    def printSet(self, s):
        msg = tCol.WARNING + "{"
        if (len(s) > 0):
            for i in sorted(s):
                msg += str(i) + ","
            msg = msg[:-1]            
        else:
            msg += "{}"
        msg += "}" + tCol.ENDC
        return msg

    # Prints candidate values of the grid.
    def printGrid(self):
        hSep = tCol.okgreen("█████████████████████████████████████████████████████████████████████████")
        hPt = tCol.okgreen("█") 
        print(hSep)        
        for k in range(self.size):
            for j in [1,4,7]:
                print(hPt, end=' ')
                for x in range(self.size):
                    for i in range(j,j+3):
                        if (self.get(x,k) == 0):
                            if (i in self.getCandidates(x,k)):
                                if (((x // 3) + (k // 3)) % 2 == 0):
                                    print(tCol.OKBLUE, end='')
                                else:
                                    print(tCol.FAIL, end='')    
                                print(str(i) + tCol.ENDC, end=' ')
                            else:
                                print("-", end=' ')
                        elif (i == 5):
                            if (((x // 3) + (k // 3)) % 2 == 0):
                                print(tCol.WARNING, end='')
                            else:
                                print(tCol.HEADER, end='')
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
        
    # Assigns a grid cell and remove candidates along corresponding row, column and sector.
    def insert(self, x, y, n):

        self.grid[x][y] = n             # Assign the grid value.
        self.updateCandidates(x,y,set()) # Cell has no more candidate values.

        # Updates row candidates.
        for i in range(self.size):
            if (x != i and self.get(i,y) == 0):
                candidates = self.getCandidates(i,y)
                candidates.discard(n)
                if (len(candidates) == 0):
                    self.error = True

        # Updates column candidates.
        for j in range(self.size):
            if (y != j and self.get(x,j) == 0):
                candidates = self.getCandidates(x,j)
                candidates.discard(n)
                if (len(candidates) == 0):
                    self.error = True

        # Updates sector candidates.
        cx, cy = self.getSectorCoord(x,y)
        for i, j in self.sectorCells():
            if ((cx + i != x or cy + j != y) and self.get(cx + i, cy + j) == 0):
                candidates = self.getCandidates(cx + i, cy + j)
                candidates.discard(n)
                if (len(candidates) == 0):
                    self.error = True

        return True

    # Gets a set of common cells between two cells.
    def getCommonCells(self, cellA, cellB):
        neighboursCellA = self.getNeighbourCells(cellA)
        neighbourCellB = self.getNeighbourCells(cellB)
        commonCells = neighboursCellA.intersection(neighbourCellB)
        return commonCells

    # Gets a set of common cells that are empty between two cells.
    def getCommonEmptyCells(self, cellA, cellB):
        commonCells = self.getCommonCells(cellA, cellB)
        commonEmpty = set()
        while (len(commonCells) != 0):
            cell = commonCells.pop()
            if (self.get(cell[0], cell[1]) == 0):
                commonEmpty.add(cell)
        return commonEmpty

    def getNeighbourCells(self, cell):
        neighbourCells = set()

        # Adds the row.
        for x in range(self.size):
            neighbourCells.add(tuple([x, cell[1]]))
        # Adds the column.
        for y in range(self.size):
            neighbourCells.add(tuple([cell[0], y]))
        # Adds the sector.
        cx, cy = self.getSectorCoord(cell[0], cell[1])
        for i,j in self.sectorCells():
            neighbourCells.add(tuple([cx+i,cy+j]))

        neighbourCells.discard(tuple([cell[0], cell[1]]))
        return neighbourCells


    # Gets the value of a cell.
    def get(self, x, y):
        return self.grid[x][y]
    
    # Gets the candidate values of a cell.
    def getCandidates(self, x, y):
        return self.candidates[x][y]
        
    # Updates the candidate values of a cell.
    def updateCandidates(self, x, y, candidates):
        self.candidates[x][y] = candidates

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
