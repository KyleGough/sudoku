from grid import Grid
from colours import tCol
from techniques.weakBiValuePairs import findWeakBiValuePairs

def yWing(g):
  
  biValuePairs = findWeakBiValuePairs(g).get()

  # Iterate over adjacent pairs.
  for cell in biValuePairs:
    adjCellList = biValuePairs[cell][0]
    adjCandidateList = biValuePairs[cell][1]

    # Cell must have at least 2 adjacencies.
    if (len(adjCellList) < 2):
      continue

    # Iterate over adjacent cells.
    for i in range(len(adjCellList)):
      for j in range(len(adjCellList)):
        # Skip duplicates.
        if (i == j):
          continue
        # Skip links that have the same candidate. 
        if (adjCandidateList[i] == adjCandidateList[j]):
          continue

        iCandidates = g.getCandidates(adjCellList[i][0], adjCellList[i][1])
        jCandidates = g.getCandidates(adjCellList[j][0], adjCellList[j][1])        
        iSing = iCandidates.difference({adjCandidateList[i]})
        jSing = jCandidates.difference({adjCandidateList[j]})

        # Checks adjacent cells have a common value.
        if (iSing.pop() in jSing):
          sectorI = tuple(g.getSectorCoord(adjCellList[i][0], adjCellList[i][1]))
          sectorJ = tuple(g.getSectorCoord(adjCellList[j][0], adjCellList[j][1]))
          sectorC = tuple(g.getSectorCoord(cell[0], cell[1]))
          sectorSet = set()
          sectorSet.add(sectorI)
          sectorSet.add(sectorJ)
          sectorSet.add(sectorC)

          # Ignore pairs in the same sector (caught in subset cover).
          if (len(sectorSet) == 1):
            continue

          commonCells = g.getCommonCells(adjCellList[i], adjCellList[j])
          # Common candidate in the wings.
          wingCandidate = jSing.pop()

          found = False

          for c in commonCells:
            candidates = g.getCandidates(c[0], c[1])
            if (wingCandidate in candidates):
              msg = tCol.header("Y-Wing:") + " Using " + g.printCell(cell[0], cell[1])
              msg += " with Wings at " + g.printCell(adjCellList[i][0], adjCellList[i][1])
              msg += ", " + g.printCell(adjCellList[j][0], adjCellList[j][1])
              msg += " reduced cell " + g.printCell(c[0], c[1])
              msg += " from " + g.printSet(candidates)
              
              candidates.discard(wingCandidate)
              found = True

              msg += " to " + g.printSet(candidates)
              g.logMove(msg)

          if (found):
              return True

  return False
