from grid import Grid
from colours import tCol
from techniques.bivaluePairs import findBiValuePairs

def ywing(g):
  
  biValuePairs = findBiValuePairs(g).get()

  # Iterate over adjacent pairs.
  for cell in biValuePairs:
    adjCellList = biValuePairs[cell][0]
    adjCandidateList = biValuePairs[cell][1]

    # Cell must have at least 2 adjacencies.
    if (len(adjCellList) < 2):
      continue

    # Iterate over adjacent cells.
    for i in range(len(adjCellList)):
      for j in range(i + 1, len(adjCellList)):
        # Skip links that have the same candidate. 
        if (adjCandidateList[i] == adjCandidateList[j]):
          continue

      
        iCandidates = g.getCandidates(adjCellList[i][0], adjCellList[i][1])
        print(iCandidates)

        #print("")

        #print(i, "", j)
        



    print(adjCandidateList)




  # For each element in the adjacency list. ###
   # Check it has at least two pairs.
   # Iterate over every pair of 2 links.
   # If AB BC AC pairs then detect Y-Wing.
   # Remove candidates that intersect two pairs.

  return False
