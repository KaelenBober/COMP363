from __future__ import annotations

# input graph: this is the example from the slides deck used in class.
_ = float("inf")
g = [
    [_, _, _, 5, 1, _],
    [_, _, 20, 5, _, 10],
    [_, 20, _, 10, _, _],
    [5, 5, 10, _, _, 15],
    [1, _, _, _, _, 20],
    [_, 10, _, 15, 20, _],
]



def reach(s: int, graph: list[list[float]]) -> list[int]:
    """Finds every vertex reachable from s by following edges in graph.

    A worklist-based traversal: start with only s to process, and keep
    pulling one vertex at a time off the worklist, adding it to the
    reached list the first time it's seen, and queuing up its neighbors
    to process next. The worklist's pop() takes from the end (last in,
    first out), which affects the order vertices come out in, but not
    which vertices end up reachable.

    Parameters:
        s: the starting vertex.
        graph: an adjacency matrix; graph[u][v] is the edge weight
            between u and v, or the sentinel value graph[0][0]
            (typically infinity) if no edge exists.
    Returns:
        list[int]: every vertex reachable from s, including s itself,
        in the order they were first reached.
    """
    no_edge = graph[0][0]  # the sentinel value this matrix uses for "no edge"
    n = len(graph)
    reached = list()  # vertices confirmed reachable, in the order found
    bag = [s]  # the worklist: vertices still waiting to be processed
    while bag:
        u = bag.pop()
        if u not in reached:
            reached.append(u)
            # queue every neighbor u has an edge to, so the loop above
            # eventually processes them too
            for v in range(n):
                if graph[u][v] != no_edge:
                    bag.append(v)
    return reached




def count_label(graph: list[list[float]]) -> tuple[int, list[int]]:
    """Counts the connected components of graph and labels every vertex
    with the id of the component it belongs to.

    Builds on reach(s, graph): for each vertex not yet reached by an
    earlier call, start a new component, find everything reachable from
    it, and label all of those vertices with the new component's count.

    Parameters:
        graph: an adjacency matrix (same no-edge convention as reach).
    Returns:
        tuple[int, list[int]]: (count, comp) -- the number of
        components, and a list where comp[v] is the component label of
        vertex v.
    """
    # TODO: mark every vertex as unlabeled first. For each vertex not
    # yet marked, increment the component count, call reach() to find
    # everything connected to it, label all of those vertices with the
    # current count, and mark them. Return (count, comp).
    
    n = len(graph)
    #comp
    #label_components from graphs assignment
    # unlabel everything
    comp = [_] * n
    next_label = 0
    for starting_vertex in range(n):
        if comp[starting_vertex] == _:
            for v in reach(starting_vertex, graph):
                comp[v] = next_label
            next_label += 1
    count = len(comp)

    return (count, comp)  # placeholder return value




def initialize_mst(graph: list[list[float]]) -> list[list[float]]:
    """Builds an edgeless working copy of graph: same size as graph,
    every entry set to infinity (no edge).

    Parameters:
        graph: the input adjacency matrix.
    Returns:
        list[list[float]]: a new n x n matrix, n = len(graph), with
        every entry set to infinity -- this is T before any edges are
        added.
    """
    # TODO: build and return a new n x n matrix where every entry is
    # float('inf'). This is the starting point for T.
    n = len(graph)
    t = [[_ for i in range(n)] for j in range(n)]
    return t
    




def boruvka_mst(graph) -> list[list[float]]:
    """Builds a minimum spanning tree from graph using the safe-edge
    algorithm: start from an edgeless working copy, and repeatedly find
    and add a safe edge between two different components until only one
    component remains.

    Parameters:
        graph: the input weighted adjacency matrix.
    Returns:
        list[list]: a working-copy-shaped matrix containing only the
        edges of the minimum spanning tree.
    """
    # TODO: initialize an edgeless working copy T of graph (see
    # initialize_mst), then count_label it. While more than one
    # component remains: for each component, find its cheapest edge
    # crossing to a different component (look up weights in graph, not
    # T); add each component's chosen edge into T; recount and relabel
    # components. Return T once a single component remains.
    
    #create the edge-less graph
    t = initialize_mst(graph)
    #Get count of components 
    count, comp = count_label(t)
    #add components together until there is only one left.
    while count > 1:
        pass        


    return [[0]]  # placeholder return value




t = boruvka_mst(g)
print(t)
no_edge = t[0][0]
n = len(t)
edges = [(u, v, t[u][v]) for u in range(n) for v in range(u + 1, n) if t[u][v] != no_edge]
total_weight = sum(weight for _, _, weight in edges)

print(f"Minimum spanning tree: {len(edges)} edges, total weight {total_weight}")
for u, v, weight in edges:
    print(f"  {u}-{v}: {weight}")

expected_weight = 31
match = "matches" if total_weight == expected_weight else "does NOT match"
print(f"\nExpected total from the hand-trace: {expected_weight} -- {match}")

