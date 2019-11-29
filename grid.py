from copy import deepcopy

class Grid:
    def __init__(self):
        self.size = 9
        self.grid = [[0 for i in range(self.size)] for j in range(self.size)]
        self.valid = [[set() for i in range(self.size)] for j in range(self.size)]
        self.error = False

    # Clones the grid object.
    def clone(self):
        cp = Grid()
        cp.size = self.size
        cp.grid = [row[:] for row in self.grid]
        cp.valid = [row[:] for row in self.valid]
        cp.error = self.error
        return cp

    # Prints basic grid info.
    def printInfo(self):
        print("Size:", self.size)
        print("Correct:", self.correct)
        print(self.grid)

    # Prints the grid contents.
    def printClean(self):
        for y in range(self.size):
            for x in range(self.size):
                print(self.get(x,y), end=" ")
            print()

    # Prints valid values of the grid.
    def printValid(self):
        for y in range(self.size):
            for x in range(self.size):
                print(self.getValid(x,y))

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
            if (self.get(cx,cy) == n):
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
    def getSectorCoord(self, x,y):
        cx = ((x // 3) * 3) + 1
        cy = ((y // 3) * 3) + 1
        return cx, cy

if __name__ == "__main__":
    test = Grid()
    test.printInfo()