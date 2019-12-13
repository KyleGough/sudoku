class Logger:
    def __init__(self):
        self.showOutput = False      # Shows main output.
        self.showMoves = False       # Shows/Hides the moves performed by the solver.
        self.showErrors = False     # Shows/Hides error messages.
        self.showAllGrid = False    # Show/Hides the grid after each move.
        self.showGridLarge = True   # Show large/small version of the initial and solution grid.
