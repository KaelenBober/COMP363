from __future__ import annotations
import random


def create_random_undirected_graph(
    n: int, prob: float, no_edge: int, max_edge_wait: int
) -> list[list[int]]:
    """
    Create a random undirected graph represented as an adjacency matrix.

    Parameters
    ----------
    n : int
        The number of vertices in the graph.
    prob : float
        The probability of an edge existing between any two vertices.
    no_edge : int
        The value to represent no edge between two vertices in the
        adjacency matrix. This value will be used to indicate that
        there is no edge between two vertices.
    max_edge_wait : int
        The maximum value to represent an edge between two vertices
        in the adjacency matrix. This value will be used to indicate that
        there is an edge between two vertices. If max_edge_wait is 1,
        then the graph will be unweighted. If max_edge_wait is
        greater than 1, then the graph will be weighted with random
        weights between 1 and max_edge_wait.

    Returns
    -------
    list[list[int]]
        The adjacency matrix representing the random undirected graph.
    """
    # Initialize the adjacency matrix with no_edge values
    g = [[no_edge for _ in range(n)] for _ in range(n)]
    # Consider every vertex i
    for i in range(n):
        # We know that (i,i) is always no_edge. Also, because the graph is
        # undirected, we only need to consider j > i.
        for j in range(i + 1, n):
            # Flip a biased coin for the edge (i, j)
            if random.random() < prob:
                # Unweighted graphs (max_edge_wait == 1) just use that
                # fixed value; weighted graphs draw a random weight in
                # [1, max_edge_wait]
                this_edge = (
                    max_edge_wait
                    if max_edge_wait == 1
                    else random.randint(1, max_edge_wait)
                )
                g[i][j] = this_edge
                # In an undirected graph, the edge (i,j) is the same as (j,i)
                g[j][i] = this_edge
    # Done!
    return g



def reached(starting_vertex: int, g: list[list[int]]) -> list[int]:
    visited: list[int] = []  # vertices already explored
    gonext: list[int] = [starting_vertex]  # worklist, seeded with the start
    while len(gonext) > 0:
        u = gonext.pop()  # LIFO: explore the most recently found vertex next
        if u not in visited:
            visited.append(u)
            # row u of the adjacency matrix lists u's neighbors
            for v in range(len(g)):
                if g[u][v] != 0 and v not in visited:
                    gonext.append(v)  # found a new vertex to explore
    return visited



def count_components(g: list[list[int]]) -> int:
    """
    Count the number of connected components in an undirected graph.

    Parameters
    ----------
    g : list[list[int]]
        The adjacency matrix representing the undirected graph.

    Returns
    -------
    int
        The number of connected components in the graph.
    """

    components: int = 0
    marked: list[int] = []  # vertices already swept into some component
    # Try every vertex as a potential "new" starting point: a graph
    # doesn't have to be fully connected (vertex 5 in the class example
    # can't reach anything), so no single reached() call is guaranteed
    # to touch every vertex -- we have to give each one a chance to start
    # a component of its own.
    for starting_vertex in range(len(g)):
        if starting_vertex not in marked:
            # Not marked yet means nobody's reached() call has swept this
            # vertex in before, so we've found a vertex in a component we
            # haven't counted -- that's one more component.
            components += 1
            # Sweep in everything reachable from here -- the whole
            # component -- so none of its vertices re-trigger the count
            # above when the loop reaches them later.
            marked.extend(reached(starting_vertex, g))
    return components



"""
MY PART
"""
def label_components(g):
    n = len(g)
    labels = [-1] * n
    next_label = 0
    for starting_vertex in range(n):
        if labels[starting_vertex] == -1:
            for v in reached(starting_vertex, g):
                labels[v] = next_label
            next_label += 1
    return labels


def connected(u,v,g, labels=None):
    if labels is None:
        labels = label_components(g)
    return labels[v]==labels[u]
 

def largest_component(g, labels=None):
    if labels is None:
        labels = label_components(g)

    n= len(g)
    sizes = [0] * (max(labels)+ 1)
    for v in range(n):
        sizes[labels[v]] += 1
    #largest label
    largest = 0
    for i in range(len(sizes)):
        if sizes[i] > sizes[largest]:
            largest = i
    #vertices with labels
    vertices = []
    for v in range(n):
        if labels[v] == largest:
            vertices.append(v)

    return sizes[largest], vertices





g = create_random_undirected_graph(5, 0.5, 0, 5)
for i in g:
    print(i)
print()
print(reached(0, g))
print(count_components(g))
print()
labels = label_components(g)
print(labels)
print()
print(connected(0,2,g,labels))
print(largest_component(g, labels))

