"""
Searches module defines all different search algorithms
"""
from queue import *
from graph.graph import *
from graph.utils import *


def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    nodes_passed = []
    path = []
    parent_node = {}
    distance_btw = {}

    queue.append(initial_node)
    parent_node[initial_node] = None
    distance_btw[initial_node] = 0
    last_node = dest_node
    nodes_passed.append(initial_node)

    while bool(queue):
        current_node = queue.pop(0)
        for neighbor in graph.neighbors(current_node):
            if neighbor not in nodes_passed:
                queue.append(neighbor)
                distance_btw[neighbor] = distance_btw[current_node] + graph.distance(current_node, neighbor)
                parent_node[neighbor] = current_node
                nodes_passed.append(neighbor)
        if dest_node in nodes_passed:
            break

    while parent_node[last_node] is not None:
        path = [graph.get_edge(parent_node[last_node], last_node)] + path
        last_node = parent_node[last_node]

    return path


def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    nodes_passed = []
    path = []
    parent_node = {}
    distance_btw = {}

    queue.append(initial_node)
    parent_node[initial_node] = None
    distance_btw[initial_node] = 0
    last_node = dest_node
    nodes_passed.append(initial_node)

    while bool(queue):
        current_node = queue[0]
        neighbors_passed = True
        neighbors = graph.neighbors(current_node)
        neighbors.sort(key=lambda x: x.data)

        for i in neighbors:
            if i not in nodes_passed:
                neighbors_passed = False
                queue = [i] + queue
                distance_btw[i] = distance_btw[current_node] + graph.distance(current_node, i)
                parent_node[i] = current_node
                nodes_passed.append(i)
                break

        if neighbors_passed:
            queue.pop(0)

        if dest_node in nodes_passed:
            break

    while parent_node[last_node] is not None:
        path = [graph.get_edge(parent_node[last_node], last_node)] + path
        last_node = parent_node[last_node]

    return path


def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    nodes_passed = []
    path = []
    parent_node = {}
    distance_btw = {}
    queue[initial_node] = 0
    parent_node[initial_node] = None
    distance_btw[initial_node] = 0
    last_node = dest_node
    nodes_passed.append(initial_node)
    while (bool(queue)):
        current_node = min(queue, key=queue.get)
        queue.pop(current_node)
        nodes_passed.append(current_node)
        for neighbor in graph.neighbors(current_node):
            pass


def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = {}
    visited_nodes = []
    path = []
    parent_node = {}
    distance_btw = {}
    queue[initial_node] = 0

    parent_node[initial_node] = None
    distance_btw[initial_node] = 0
    last_node = dest_node
    visited_nodes.append(initial_node)

    while bool(queue):
        current_node = initial_node
        queue.pop(current_node)
        visited_nodes.append(current_node)

        for neighbor in graph.neighbors(current_node):
            pass

    while parent_node[last_node] is not None:
        path = [graph.get_edge(parent_node[last_node], last_node)] + path
        last_node = parent_node[last_node]

    return path
