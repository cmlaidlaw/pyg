__author__ = 'cml'

from collections import deque

class GraphNode(object):
    """
    Holds data about each graph node
    """
    _name = ""
    _edges = []

    def __init__(self, name, edges):
        self._name = name
        self._edges = edges

    def get_name(self):
        return self._name

    def add_edge(self, destination):
        self._edges.append(destination)

    def remove_edge(self, destination):
        if destination not in self._edges:
            raise KeyError("Cannot remove non-existent edge from node.")
        self._edges.remove(destination)

    def get_edges(self):
        return self._edges

    def __repr__(self):
        return "<GraphNode>: \"" + self._name + "\" with edges " + str(self._edges)


class Graph(object):
    """
    Holds meta-data and provides graph operations
    """
    _nodes = {}
    _isDirected = False

    def __init__(self, nodes=None, edges=None, directed=False):
        self._isDirected = directed
        if len(nodes) > 0:
            for node in nodes:
                self.add_node(node)
        if len(edges) > 0:
            for edge in edges:
                origin, destination = edge
                self.add_edge(origin, destination)

    def is_directed(self):
        return self._isDirected

    def add_node(self, node):
        if node in self._nodes:
            raise KeyError("Cannot add duplicate node `" + node + "` to graph.")
        self._nodes[node] = GraphNode(node,[])

    def remove_node(self, node):
        if node not in self._nodes:
            raise KeyError("Cannot remove non-existent node `" + node + "` from graph.")
        del self._nodes[node]

    def get_node(self, node):
        if node not in self._nodes:
            raise KeyError("Cannot get non-existent node `" + node + "`.")
        return self._nodes[node]

    def enumerate_nodes(self):
        return self._nodes.keys()

    def add_edge(self, origin, destination):
        if origin not in self._nodes:
            raise KeyError("Cannot add edge from non-existent node `" + origin + "`.")
        if destination not in self._nodes:
            raise KeyError("Cannot add edge to non-existent node `" + destination + "`.")
        self._nodes[origin].add_edge(destination)
        if not self._isDirected:
            self._nodes[destination].add_edge(origin)

    def remove_edge(self, origin, destination):
        if origin not in self._nodes:
            raise KeyError("Cannot remove edge from non-existent node `" + origin + "`.")
        if destination not in self._nodes:
            raise KeyError("Cannot remove edge to non-existent node `" + destination + "`.")
        self._nodes[origin].remove_edge(destination)
        if not self._isDirected:
            self._nodes[destination].remove_edge(origin)

    def __repr__(self):
        return "<Graph>:\n  " + ("\n  ".join([str(self.get_node(node)) for node in self._nodes]))


def BFS(graph, process_node_early, process_edge, process_node_late, node=None):
    """
    Performs a customizable breadth-first search on the graph
    """
    if node == None:
        node = graph.enumerate_nodes()[0]

    state = {}
    parents = {}
    unprocessed = deque(node)

    for temp_node in graph.enumerate_nodes():
        state[temp_node] = "undiscovered"
        parents[temp_node] = None
    state[node] = "discovered"

    while (len(unprocessed) > 0):
        node = unprocessed.popleft()
        process_node_early(node)
        edges = graph.get_node(node).get_edges()
        for edge in edges:
            origin, destination = node, edge
            if state[destination] != "processed":
                process_edge(origin, destination)
            if state[destination] == "undiscovered":
                state[destination] = "discovered"
                parents[destination] = origin
                unprocessed.append(destination)
            state[origin] = "processed"
        process_node_late(node)
    return { "parents": parents }

def DFS(graph, process_node_early, process_edge, process_node_late, node=None, data=None):
    """
    Performs a customizable depth-first search on the graph
    """
    if data == None: # Initialize our search meta-data
        data = { "time": 0, "discovered": {}, "processed": {}, "parents": {}, "entry_times": {}, "exit_times": {} }
        for temp_node in graph.enumerate_nodes():
            data["discovered"][temp_node] = False
            data["processed"][temp_node] = False
            data["parents"][temp_node] = None
            data["entry_times"][temp_node] = -1
            data["exit_times"][temp_node] = -1
    if node == None: # Arbitrarily choose a starting node if none is provided
        node = graph.enumerate_nodes()[0]

    data["time"] += 1
    data["discovered"][node] = True
    data["entry_times"][node] = data["time"]

    process_node_early(node, data)

    edges = graph.get_node(node).get_edges()
    for edge in edges:
        origin, destination = node, edge
        if data["discovered"][destination] == False:
            data["parents"][destination] = origin
            process_edge(origin, destination, data)
            DFS(graph, process_node_early, process_edge, process_node_late, destination, data)
        elif (data["processed"][destination] == False and data["parents"][origin] != destination)\
                or graph.is_directed():
            process_edge(origin, destination, data)

    process_node_late(node, data)

    data["time"] += 1
    data["exit_times"][node] = data["time"]
    data["processed"][node] = True

    return data

def process_node_early(node, data=None):
    pass

def process_edge(origin, destination, data=None):
    """
    As an example, the following will classify graph edges:

    if data:
        if data["parents"][destination] == origin:
            classification = "TREE"
        elif data["discovered"][destination] and not data["processed"][destination]:
            classification = "BACK"
        elif data["processed"][destination] and (data["entry_times"][destination] > data["entry_times"][origin]):
            classification = "FORWARD"
        elif data["processed"][destination] and (data["entry_times"][destination] < data["entry_times"][origin]):
            classification = "CROSS"
        else:
            raise ValueError("Could not classify edge from `" + origin + "` to `" + destination + "`.")

    """
    pass

def process_node_late(node, data=None):
    pass

# Do a test run:
g = Graph(nodes=["1","2","3","4","5","6"],\
          edges=[("1","6"),("1","2"),("1","5"),("2","3"),("2","5"),("3","4"),("4","5")],\
          directed=False)

print(g) # Print the graph
print("\nBFS\n-----\n")
print(BFS(g, process_node_early, process_edge, process_node_late)) # Print BFS results
print("\n\nDFS\n-----\n")
print(DFS(g, process_node_early, process_edge, process_node_late)) # Print DFS results