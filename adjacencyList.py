class AdjacencyList:
    def __init__(self):
        self.size = 0 # Number of keys in the graph.
        self.pairs = 0 # Number of conjugate pairs.
        self._adjacencyList = {} # Graph in adjacency list representation.

    # Inserts a pair into the graph.
    def insert(self, el1, el2):
        if el1 in self._adjacencyList:
            self._adjacencyList[el1].append(el2)
        else:
            self._adjacencyList[el1] = [el2]
            self.size += 1

        if el2 in self._adjacencyList:
            self._adjacencyList[el2].append(el1)
        else:
            self._adjacencyList[el2] = [el1]
            self.size += 1

        self.pairs += 1

    # Outputs the adjacency list as a string.
    def toString(self):
        return str(self._adjacencyList)

