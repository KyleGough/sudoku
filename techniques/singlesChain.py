from grid import Grid
from colours import tCol

def singlesChain(g):
    return g, False

def singlesChainCheck(g, n):
    return g, False



# assume value i.
# i can be filled in between 0-6
# grid needs a colour attribute.

# find all cells that contain i.
# create a set (row, col, sector)
# choose starting point
# colour cell
# add all cells in same sector, column and row that have i a different colour.
# iterate through queue.
# colour cells
# find violations
# if found cell, add its neighbors to the queue.
# repeat until violation found or all cells reviewed.

# list of all cells containing i.
# list of cells in the chain
# queue
# contradictions

# row[9] each element is the count of coloured cels in the row. if row[i] == 2 then cannot add -> contradiction
