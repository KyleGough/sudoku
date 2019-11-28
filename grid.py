class Grid:
    def __init__(self):
        self.size = 9
        self.grid = [[0 for i in range(self.size)] for j in range(self.size)]
        self.valid = [[set() for i in range(self.size)] for j in range(self.size)]

    # Prints basic grid info.
    def printInfo(self):
        print("Size:", self.size)
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
        cx = ((x // 3) * 3) + 1
        cy = ((y // 3) * 3) + 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.get(cx,cy) == n):
                    return False
        return True

    # Checks if the next move is valid.
    def isValidMove(self, x, y, n):
        return (self.ruleRow(x,y,n) and self.ruleColumn(x,y,n) and self.ruleSector(x,y,n))
        
    # Assigns a grid cell.
    def insert(self, x, y, n):
        self.grid[x][y] = n
        # Cell has no more valid values.
        self.updateCellValid(x,y,set())
        # Updates row validities.
        for x in range(self.size):
            valid = self.getValid(x,y)
            valid = set([y for y in valid if y != n])
            self.updateCellValid(x,y,valid)
        # Updates column validities.
        for y in range(self.size):
            valid = self.getValid(x,y)
            valid = set([y for y in valid if y != n])
            self.updateCellValid(x,y,valid)
        #sector###

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
            return self.get(x,y)

    # Updates the valid values of a cell.
    def updateCellValid(self, x, y, valid):
        self.valid[x][y] = valid
    

if __name__ == "__main__":
    test = Grid()
    test.printInfo()