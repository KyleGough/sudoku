from grid import Grid
from colours import tCol
from techniques.wxyzWingPairs import findWXYZPairs


#1. Head and Wings have total 4 candidates between them.
#2. find head (cells that can see every other cell).
#3. find z.
#4. Remove candidates in all cells that intersect with all WXYZ-Wing cells that contain Z.

def wxyzWing(g): 
  WXYZPairs = findWXYZPairs(g).get()
  #print(WXYZPairs[tuple([2,3])])

  # Iterate over adjacent pairs.
  for cell in WXYZPairs:
    adjCellList = WXYZPairs[cell][0]
   
    # Cell must have at least 3 adjacencies.
    if (len(adjCellList) < 3):
      continue

    headCandidates = g.getCandidates(cell[0], cell[1])

    # Iterate over adjacent cells.
    for i in range(0, len(adjCellList)):
      for j in range(i + 1, len(adjCellList)):
        for k in range(j + 1, len(adjCellList)):

          # Skip links that have the same cell. 
          if (adjCellList[i] == adjCellList[j]):
            continue
          if (adjCellList[j] == adjCellList[k]):
            continue
          if (adjCellList[i] == adjCellList[k]):
            continue
          
          xzCandidates = g.getCandidates(adjCellList[i][0], adjCellList[i][1])
          yzCandidates = g.getCandidates(adjCellList[j][0], adjCellList[j][1])        
          wzCandidates = g.getCandidates(adjCellList[k][0], adjCellList[k][1])
          
          ### CAPTURE SPECIFIC HEAD CELL.
          #a = tuple([3,3])
          #if (adjCellList[i] != a and adjCellList[j] != a and adjCellList[k] != a):
            
          # Checks the cells form a 4 cell group with 4 candidates shared among the cells.
          wingCandidates = xzCandidates.union(yzCandidates).union(wzCandidates).union(headCandidates)
          if (len(wingCandidates) != 4):
            continue

          restrictedSetCount = 0
          for wc in wingCandidates:
            candidateCells = []
            if (wc in headCandidates):
              candidateCells.append(cell)
            if (wc in xzCandidates):
              candidateCells.append(adjCellList[i])
            if (wc in yzCandidates):
              candidateCells.append(adjCellList[j])
            if (wc in wzCandidates):
              candidateCells.append(adjCellList[k])
            if (isRestricted(g, candidateCells)):
              restrictedSetCount += 1
          
          if (restrictedSetCount != 3):
            continue

          ### INFO
          #print()
          #print("XZ: " + str(adjCellList[i]))
          #print("YZ: " + str(adjCellList[j]))
          #print("WZ: " + str(adjCellList[k]))

          xyVis = g.cellsVisible(adjCellList[i], adjCellList[j])
          xwVis = g.cellsVisible(adjCellList[i], adjCellList[k])
          ywVis = g.cellsVisible(adjCellList[j], adjCellList[k])

          # List of head cells (cells that can see every other cell).
          headCells = set()
          wingCells = []
          headCells.add(cell)

          # Checks connectivity of XZ.
          if (xyVis and xwVis):
            headCells.add(adjCellList[i])
          else:
            wingCells.append(adjCellList[i])

          # Checks connectivity of YZ.
          if (xyVis and ywVis):
            headCells.add(adjCellList[j])
          else:
            wingCells.append(adjCellList[j])

          # Checks connectivity of WZ.
          if (xwVis and ywVis):
            headCells.add(adjCellList[k])
          else:
            wingCells.append(adjCellList[k])

          # If not at least 2 wing cells then not a valid WXYZ-Wing.
          if (len(wingCells) < 2):
            continue

          ###
          #print(headCells)
          #print(wingCells)

          # Intersection of all wing cells to finds the non-restricted candidate.
          z = g.getCandidates(wingCells[0][0], wingCells[0][1])
          for idx in range(len(wingCells)):
            z = z.intersection(g.getCandidates(wingCells[idx][0], wingCells[idx][1]))

          # Gets the non-restricted candidate z.
          if (len(z) != 1):
            continue
          z = z.pop()

          # Set of cells that contain candidate z.
          candidateCells = set()
          if (z in headCandidates):
            candidateCells.add(cell)
          if (z in xzCandidates):
            candidateCells.add(adjCellList[i])
          if (z in yzCandidates):
            candidateCells.add(adjCellList[j])
          if (z in wzCandidates):
            candidateCells.add(adjCellList[k])

          ###
          commonCells = []
          if (len(candidateCells) == 2):
            tmp1 = candidateCells.pop()
            tmp2 = candidateCells.pop()
            commonCells = g.getCommonEmptyCells(tmp1, tmp2)
          elif (len(candidateCells) == 3):
            tmp1 = candidateCells.pop()
            tmp2 = candidateCells.pop()
            tmp3 = candidateCells.pop()
            commonCells = g.getCommonEmptyCells(tmp1, tmp2).intersection(g.getNeighbourCells(tmp3))
          elif (len(candidateCells) == 4):
            tmp1 = candidateCells.pop()
            tmp2 = candidateCells.pop()
            tmp3 = candidateCells.pop()
            tmp4 = candidateCells.pop()
            commonCells1 = g.getCommonEmptyCells(tmp1, tmp2)
            commonCells2 = g.getCommonEmptyCells(tmp3, tmp4)
            commonCells = commonCells1.intersection(commonCells2)
          else:
            continue

          ###
          #print(candidateCells)
          #print(commonCells)

          found = False
        
          for c in commonCells:
            candidates = g.getCandidates(c[0], c[1])

            if (z in candidates):
              msg = tCol.header("WXYZ-Wing:") + " Using "
              
              for head in headCells:
                msg += g.printCell(head[0], head[1]) + " "

              msg += "with Wings at "
              
              for wing in wingCells:
                msg += g.printCell(wing[0], wing[1]) + " "

              msg += "reduced cell " + g.printCell(c[0], c[1])
              msg += " from " + g.printSet(candidates)
              
              candidates.discard(z)
              found = True

              msg += " to " + g.printSet(candidates)
              g.logMove(msg)
         
          if (found):
            return True

  return False

# Checks the list of cells occupy at least 2 rows, columns or sectors.
def isRestricted(g, cellList):
  # Trivially true is length is less than 2.
  if (len(cellList) < 2):
    return True

  rowCheck = True
  columnCheck = True
  sectorCheck = True

  # Row check.
  fstX = cellList[0][0]
  for x in range(1, len(cellList)):
    if (cellList[x][0] != fstX):
      rowCheck = False
      break

  # Column check.
  fstY = cellList[0][1]
  for y in range(1, len(cellList)):
    if (cellList[y][1] != fstY):
      columnCheck = False
      break

  # Sector check.
  cx, cy = g.getSectorCoord(cellList[0][0], cellList[0][1])
  for z in range(1, len(cellList)):
    px, py = g.getSectorCoord(cellList[z][0], cellList[z][1])
    if (cx != px or cy != py):
      sectorCheck = False
      break

  return (rowCheck or columnCheck or sectorCheck)




