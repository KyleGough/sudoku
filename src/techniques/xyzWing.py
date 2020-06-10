from grid import Grid
from colours import tCol
from techniques.xyzWingPairs import findXYZPairs

def xyzWing(g): 
  XYZPairs = findXYZPairs(g).get()
  
  # Iterate over adjacent pairs.
  for cell in XYZPairs:
    adjCellList = XYZPairs[cell][0]
    adjCandidateList = XYZPairs[cell][1]

    # Cell must have at least 2 adjacencies.
    if (len(adjCellList) < 2):
      continue

    headCandidates = g.getCandidates(cell[0], cell[1])

    # Iterate over adjacent cells.
    for i in range(len(adjCellList)):
      for j in range(len(adjCellList)):

        # Skip duplicates.
        if (i <= j):
          continue
        # Skip links that have the same candidate. 
        if (adjCandidateList[i] == adjCandidateList[j]):
          continue

        xzCandidates = g.getCandidates(adjCellList[i][0], adjCellList[i][1])
        yzCandidates = g.getCandidates(adjCellList[j][0], adjCellList[j][1])        
        xz = xzCandidates.intersection(headCandidates)
        yz = yzCandidates.intersection(headCandidates)

        z = xz.intersection(yz)
        if (len(z) != 1):
          continue
        
        z = z.pop()

        # Common cells between cells with z.
        commonCells = g.getCommonEmptyCells(adjCellList[i], adjCellList[j])
        if (z in headCandidates):
          commonCellsHeadXZ = g.getCommonEmptyCells(cell, adjCellList[i])
          commonCells = commonCells.intersection(commonCellsHeadXZ)
        
        found = False

        for c in commonCells:
          candidates = g.getCandidates(c[0], c[1])

          if (z in candidates):
            msg = tCol.header("XYZ-Wing:") + " Using " + g.printCell(cell[0], cell[1])
            msg += " with Wings at " + g.printCell(adjCellList[i][0], adjCellList[i][1])
            msg += ", " + g.printCell(adjCellList[j][0], adjCellList[j][1])
            msg += " reduced cell " + g.printCell(c[0], c[1])
            msg += " from " + g.printSet(candidates)
            
            candidates.discard(z)
            found = True

            msg += " to " + g.printSet(candidates)
            g.logMove(msg)

        if (found):
          return True

  return False
