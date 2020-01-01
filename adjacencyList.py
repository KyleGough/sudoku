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

    # Deletes a key from the graph.
    def delete(self, el):
        if el in self._adjacencyList:
            del self._adjacencyList[el]

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

    # Gets a list of all cells in the adjacency list.
    def getCells(self):
        return list(self._adjacencyList.keys())

    # Outputs the adjacency list as a string.
    def toString(self):
        return str(self._adjacencyList)

