class AdjacencyList:
    def __init__(self):
        self.pairs = 0 # Number of conjugate pairs.
        self._adjacencyList = {} # Graph in adjacency list representation.

    # Gets the number of keys in the adjacency list.
    def getSize(self):
        return len(list(self._adjacencyList.keys()))

    # Inserts a pair into the graph.
    def insert(self, a, b):
        if a in self._adjacencyList and b not in self._adjacencyList[a]:
            self._adjacencyList[a].append(b)
        else:
            self._adjacencyList[a] = [b]
            

        if b in self._adjacencyList and a not in self._adjacencyList[b]:
            self._adjacencyList[b].append(a)
        else:
            self._adjacencyList[b] = [a]

        self.pairs += 1

    # Removes a pair from the graph.
    def remove(self, a, b):
        
        # Removes relationship a -> b.
        if a in self._adjacencyList and b in self._adjacencyList[a]:
            self._adjacencyList[a].remove(b)
            if (len(self._adjacencyList[a]) == 0):
                del self._adjacencyList[a]

        # Removes relationship b -> a.
        if b in self._adjacencyList and a in self._adjacencyList[b]:
            self._adjacencyList[b].remove(a)
            if (len(self._adjacencyList[b]) == 0):
                del self._adjacencyList[b]

    # Gets the first pair.
    def getFirst(self):
        start = list(self._adjacencyList.keys())[0]
        connections = self._adjacencyList[start]
        return start, connections

    # Returns the corresponding cells paired with a given cell.
    def getLinks(self, el):
        if el in self._adjacencyList:
            return self._adjacencyList[el]
        else:
            return []

    # Outputs the adjacency list as a string.
    def toString(self):
        return str(self._adjacencyList)

