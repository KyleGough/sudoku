from grid import Grid
from colours import tCol


def ur(g):

    for a, b, c, d in rectangleGenerator(g):

        corners = [a,b,c,d]
        cornerCandidates = []
        cornerCandidates.append(g.getCandidates(a[0], a[1]))
        cornerCandidates.append(g.getCandidates(b[0], b[1]))
        cornerCandidates.append(g.getCandidates(c[0], c[1]))
        cornerCandidates.append(g.getCandidates(d[0], d[1]))

        urCandidates = cornerCandidates[0].intersection(cornerCandidates[1])
        urCandidates = urCandidates.intersection(cornerCandidates[2])
        urCandidates = urCandidates.intersection(cornerCandidates[3])
        
        # Checks there is a common bi-value candidate in the rectangle.
        if (len(urCandidates) != 2):
            continue

        # Checks that 3 corner cells are equal to the bi-value candidate.
        biCandCornerCount = 0

        for i in range(len(cornerCandidates)):
            if (cornerCandidates[i] == urCandidates):
                biCandCornerCount += 1
            else:
                uniqueCorner = i

        if (biCandCornerCount == 4):
            print("Should not have happened. UR found, multiple solutions.")
        elif (biCandCornerCount == 3):
            c = corners[uniqueCorner]
            candidates = g.getCandidates(c[0], c[1])
            
            #print(candidates)
            #print(urCandidates)
            msg = tCol.header("Unique Rectangles:") + " Reduced cell "
            msg += g.printCell(c[0], c[1]) + " from " + g.printSet(candidates)

            for n in urCandidates:
                candidates.discard(n)
            #print(candidates)
            msg += " to " + g.printSet(candidates) + " using UR "
            msg += g.printCell(a[0], a[1]) + " " + g.printCell(b[0], b[1]) + " "
            msg += g.printCell(c[0], c[1]) + " " + g.printCell(d[0], d[1])
            g.logMove(msg)
            return True

    return False

# Generates valid rectangles in the grid spanning two sectors.
def rectangleGenerator(g):
    aid = -1
    for ax, ay in g.unfilledCells():
        aid += 1
        bid = -1
        for bx, by in g.unfilledCells():
            bid += 1
            if (bid <= aid):
                continue
            elif (bx <= ax or by <= ay):
                continue
            # Checks corner C is empty.
            elif (g.get(bx, ay) != 0):
                continue
            # Checks corner D is empty.
            elif (g.get(ax, by) != 0):
                continue

            # Counts how many sectors the UR covers.
            sectorSet = set()
            sectorSet.add(tuple(g.getSectorCoord(ax,ay)))
            sectorSet.add(tuple(g.getSectorCoord(bx,by)))
            sectorSet.add(tuple(g.getSectorCoord(bx,ay)))
            sectorSet.add(tuple(g.getSectorCoord(ax,by)))
            
            # UR must cover exactly 2 sectors.
            if (len(sectorSet) != 2):
                continue

            a = tuple([ax,ay])
            b = tuple([bx,by])
            c = tuple([bx,ay])
            d = tuple([ax,by])
            yield a, b, c, d
          