from grid import Grid
from colours import tCol

### Trivial implementation is O(N^4) -1296
def avoidableRect(g):
    count = 0
    return False

    #1296
    for t in range(g.size - 1):
        for b in range(t + 1, g.size):
            for l in range(g.size - 1):
                for r in range(l + 1, g.size):
                    sectors = set()

                    # 3 filled
                    # 2 boxes
                    cells = set()
                    #cells.add(tuple([a,c]))
                    #cells.add(tuple([b,c]))
                    #cells.add(tuple([a,d]))
                    #cells.add(tuple([b,d]))

                    #a = str(l+1)
                    ##b = str(r+1)
                    #c = str(t+1)
                    #d = str(b+1)
                    #tl = "(" + a + "," + c + ")"
                    #tr = "(" + b + "," + c + ")"
                    bl = "(" + a + "," + d + ")"
                    br = "(" + b + "," + d + ")"
                    print(tl, tr, bl, br)
                    count += 1
                    
    print(count)
    return False
