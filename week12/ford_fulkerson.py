from copy import deepcopy
from test_graphs.py import GRAPH_A, GRAPH_B, SOURCE
"""Week 11 starter: Ford-Fulkerson, maximum flow and minimum cut.

A flow network is a directed acyclic graph stored as an adjacency matrix:
graph[u][v] is the CAPACITY of the edge from u to v, and 0 means there is no
edge. One vertex is the source (no incoming edges) and one is the target (no
outgoing edges). The method, as in class on 11/4 and 11/6:

    1. make a working copy of the matrix, the RESIDUAL graph;
    2. while the residual graph has a path from source to target
       (an AUGMENTING PATH):
           find the weakest edge on the path,
           SATURATE the path: subtract that flow from every forward edge
           and add it to every back edge;
           an edge whose capacity drops to 0 is gone;
    3. the vertices still reachable from the source are the set S, everything
       else is T. The edges of the ORIGINAL graph that go from S to T are the
       minimum cut, and their capacities add up to the maximum flow.

Read everything above the line "YOUR CODE STARTS HERE" before you write
anything. The functions below the line are yours. Every function that
returns a value has exactly one return.
"""

# Vertex names for the class example, so printed answers are readable.
NAMES = ["S", "A", "B", "C", "D", "E", "F", "T"]

# The class-style example: 8 vertices, source S = 0, target T = 7.
# Row u, column v holds the capacity of the edge u -> v (0 = no edge).
CLASS_GRAPH = [
    #S  A   B  C  D   E  F  T
    [0, 40, 0, 0, 40, 0, 0, 0],  # S -> A (40), S -> D (40)
    [0,  0, 5, 0,  0, 5, 0, 0],  # A -> B (5), A -> E (5)
    [0,  0, 0, 5,  0, 0, 0, 0],  # B -> C (5)
    [0,  0, 0, 0,  0, 0, 0, 15],  # C -> T (15)
    [0,  0, 0, 0,  0, 10, 0, 0],  # D -> E (10)
    [0,  0, 0, 10, 0, 0,  5, 0],  # E -> C (10), E -> F (5)
    [0,  0, 0, 0,  0, 0, 0, 15],  # F -> T (15)
    [0,  0, 0, 0,  0, 0, 0, 0],  # T has no outgoing edges
]

# A tiny second example: two disjoint routes from 0 to 3.
DIAMOND = [
    [0, 3, 2, 0],  # 0 -> 1 (3), 0 -> 2 (2)
    [0, 0, 0, 2],  # 1 -> 3 (2)
    [0, 0, 0, 3],  # 2 -> 3 (3)
    [0, 0, 0, 0],
]

# =====================================================================
# YOUR CODE STARTS HERE
# =====================================================================
# =====================================================================
# Part A: the building blocks, then ford_fulkerson itself.
# Part B: is_acyclic and your own tests for it.
# =====================================================================



def deep_copy(matrix: list[list[int]]) -> list[list[int]]:
    """Return a new matrix with the same numbers as matrix, sharing no memory.

    Write it by hand: allocate an n x n matrix of zeros, then copy element by
    element with two nested loops. Do not use the copy module here. (In
    production code you would, and the 11/6 class explains why a plain
    `residual = graph` is not a copy at all.)
    """
    n = len(matrix)
    copy = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            copy[i][j] = matrix[i][j]
    return copy


def find_augmenting_path(residual, current, target, path_so_far):
    """Return a list of vertices from current to target, or None if no path.

    path_so_far holds the vertices already on the path, not including current.
    Recursion, as on 11/4: if there is a path from current to the target, then
    one of current's neighbors has a path to the target. A neighbor is a vertex
    v with residual[current][v] > 0.

    Never put a vertex on the path twice. Back edges make u -> v and v -> u
    both exist in the residual graph, so without this rule your recursion can
    bounce between two vertices forever.

    Warning: on a graph with over 100 vertices this search can become very
    slow (minutes, not seconds), even though it is correct. The cause: a
    vertex can be reached by many different routes, and if the search only
    remembers the vertices on its CURRENT path, every time it reaches a dead
    end it forgets what it learned and tries the same dead ends again by the
    next route. The number of routes grows exponentially with the size of the
    graph. Small graphs hide the problem; the large test graph does not.
    """
    #if we reached the target, return the total path
    if current == target:
        result = path_so_far + [current]
    else:
        result = None
        for v in range(len(residual)):
            #if a neighbor is found and it isnt the same as current
            #restart the search from the found vertex and add the current vertex into the path
                #need to make sure that the vertex isnt the same as current and isnt in the path, without these, it can create a loop
                if residual[current][v] > 0 and result is None and v != current and v not in path_so_far:
                    result = find_augmenting_path(residual,v,target,path_so_far+[current])
    return result


def bottleneck(residual, path):
    """Return the smallest capacity among the edges along path.

    path is a list of vertices, for example [0, 1, 5, 6, 7], so its edges are
    (0,1), (1,5), (5,6), (6,7). Use the 'assume the first is smallest, then
    revise' scan from COMP 170. Do not use min().
    """
    #assuming the first edge is the smallest
    smallest = residual[path[0]][path[1]]

    #loop through rest of the edges, start 1 ahead to skip current weakest edge.
    #make sure to end before last element to not go beyond length
    for i in range(1,len(path)-1):
        #if next edge is smaller than our current weakest
        #set edge to weakest
        if residual[path[i]][path[i+1]] < smallest:
            smallest = residual[path[i]][path[i+1]]
    return smallest


def saturate(residual, path, flow):
    """Send flow along path, changing residual in place.

    For every edge (u, v) on the path: residual[u][v] goes DOWN by flow and the
    back edge residual[v][u] goes UP by flow. An edge whose capacity reaches 0
    is, by convention, no edge, so there is nothing more to do to 'remove' it.
    Returns nothing.
    """
    for i in range(0,len(path)-1):
        #path down flow
        residual[path[i]][path[i+1]] -= flow
        #back edge up flow
        residual[path[i+1]][path[i]] += flow



def reachable(residual, source):
    """Return the set of vertices reachable from source in residual.

    Follow only edges with capacity > 0. Any traversal will do; the 11/4
    class suggests depth-first. A set (not a list) means each vertex counts
    once.
    """
    seen = set()
    #DFS = stack
    stack = [source]
    while len(stack) > 0:
        vertex = stack.pop()
        #add values into seen if not already there, from there check if it is above 
        if vertex not in seen:
            seen.add(vertex)
            for j in range(len(residual)):
                if residual[vertex][j] > 0 and j not in seen:
                    stack.append(j)
    return seen



def cut_edges(graph, reachable_set):
    """Return the list of edges (u, v) of the ORIGINAL graph that cross the cut.

    S is reachable_set; T is every other vertex. An edge crosses the cut when
    u is in S, v is not, and graph[u][v] > 0. For every u in S, consider every
    v in T (the 11/6 class). Edges from T back into S are not part of the cut.
    """
    crossing = []
    for u in reachable_set:
        for v in range(len(graph)):
            #v is in not in the reachable set
            #graphs value at graph[u][v] > 0
            if v not in reachable_set and graph[u][v] > 0:
                crossing.append((u,v))
    return crossing


def ford_fulkerson(graph, source, target):
    """Return (max_flow, cut) for graph.

    max_flow is the sum of the bottlenecks of the augmenting paths you
    saturate. cut is the list of edges (u, v) of the minimum cut, from
    cut_edges. graph itself must come back unchanged: all the work happens on
    a deep copy.

    Raise ValueError if the graph is not acyclic (Part B gives you is_acyclic
    for exactly this).
    """
    if is_acyclic(graph) == False:
        raise ValueError("Theres a loop")
    

    max_flow = 0  # pessimistic: no flow, no cut
    cut = []
    #create the residual graph
    residual = deep_copy(graph)
    #get start path
    path = find_augmenting_path(residual, source, target, [])
    #keep emptying the path
    #keep updating the flow for max flow
    while path is not None:
        flow = bottleneck(residual, path)
        saturate(residual,path, flow)
        max_flow += flow
        path = find_augmenting_path(residual, source, target, [])
    #get the reachable set for getting the cutt
    reachable_set = reachable(residual,source)
    cut = cut_edges(graph, reachable_set)
    return (max_flow, cut)

long_flow, long_cut = ford_fulkerson(GRAPH_A, SOURCE, len(GRAPH_A) - 1)
(print(long_flow,long_cut))

# --------------------------- Part B ----------------------------------


def is_acyclic(graph):
    """Return True if the directed graph has no cycle, False if it has one.

    A reciprocal pair (u -> v and v -> u) is a cycle, and so is 0 -> 2 -> 4 ->
    1 -> 0. You cannot see long cycles by eye in a graph of 500 vertices.
    One way, from 10/30: Kahn's algorithm. Copy the graph; repeatedly remove a
    vertex whose in-degree is 0 (column sum of the matrix); if you remove every
    vertex, there was no cycle; if you get stuck with vertices left over, each
    with an incoming edge, there is one. Any correct method is welcome.
    """
    n = len(graph)
    #copy of the graph
    work = deep_copy(graph)
    removed = [False] * n
    #counter for removed vertices
    count = 0
    #progress = acyclic in this case
    progress = True
    while progress:
        progress = False
        for v in range(n):
            if not removed[v]:
                has_incoming = False
                # loop u over range(n): if work[u][v] > 0, has_incoming = True
                for u in range(n):
                    if work[u][v] > 0:
                        has_incoming = True
                if not has_incoming:
                    removed[v] = True
                    count += 1
                    # loop w over range(n): set work[v][w] = 0
                    for w in range(n):
                        work[v][w] = 0
                    progress = True
    return count == n


def test_is_acyclic() -> None:
    """YOUR TESTS for Part B.

    Write asserts that check is_acyclic on graphs you build yourself:
      * at least two acyclic graphs (one with more than one source or sink),
      * a graph whose only cycle is a reciprocal pair,
      * a graph whose cycle is longer than two vertices,
      * a graph with a cycle that does not pass through the source.
    Explain in a comment, for each, what it would catch.
    """

    pass  # TODO: write your asserts here


# =====================================================================
# GIVEN TESTS FOR PART A -- DO NOT CHANGE ANYTHING BELOW THIS LINE
# =====================================================================
# assert condition, "message" does nothing when the condition is True, and
# stops with an AssertionError (and the message) when it is False.
# The runner catches that error so one failing test does not hide the others.
# =====================================================================


def test_deep_copy_is_independent() -> None:
    """Why: destroying an edge of the copy must not destroy the original."""
    original = [[0, 5], [0, 0]]
    copy = deep_copy(original)
    assert copy == original, "the copy must start with the same numbers"
    copy[0][1] = 0  # 'destroy' an edge of the copy
    assert original[0][1] == 5, "changing the copy changed the original"


def test_path_exists_and_is_valid() -> None:
    """Why: an augmenting path starts at S, ends at T, and uses real edges."""
    path = find_augmenting_path(CLASS_GRAPH, 0, 7, [])
    assert path is not None, "there is a path from S to T"
    assert path[0] == 0 and path[-1] == 7, f"path must run S to T, got {path}"
    for i in range(len(path) - 1):
        assert CLASS_GRAPH[path[i]][path[i + 1]] > 0, f"{path} uses a missing edge"


def test_no_path_returns_none() -> None:
    """Why: the loop in ford_fulkerson stops when the path finder says None."""
    cut_off = [[0, 0, 0], [0, 0, 1], [0, 0, 0]]  # no edge out of vertex 0
    assert find_augmenting_path(cut_off, 0, 2, []) is None, "no path should be None"


def test_path_does_not_loop_on_back_edges() -> None:
    """Why: with u -> v and v -> u both present, a careless search never ends."""
    both_ways = [[0, 4, 0], [4, 0, 4], [0, 0, 0]]  # 0 <-> 1, and 1 -> 2
    path = find_augmenting_path(both_ways, 0, 2, [])
    assert path == [0, 1, 2], f"expected [0, 1, 2], got {path}"


def test_bottleneck() -> None:
    """Why: the flow on a path is the capacity of its weakest edge."""
    path = [0, 1, 5, 6, 7]  # S -> A -> E -> F -> T: 40, 5, 5, 15
    assert bottleneck(CLASS_GRAPH, path) == 5, "the weakest edge on this path is 5"
    assert bottleneck(CLASS_GRAPH, [0, 4]) == 40, "a one-edge path is its own bottleneck"


def test_saturate() -> None:
    """Why: forward edges lose capacity, back edges gain the same amount."""
    residual = deep_copy(CLASS_GRAPH)
    saturate(residual, [0, 1, 2, 3, 7], 5)  # S -> A -> B -> C -> T
    assert residual[0][1] == 35, "S -> A: 40 - 5"
    assert residual[1][0] == 5, "A -> S back edge: 0 + 5"
    assert residual[1][2] == 0, "A -> B was saturated"
    assert residual[3][7] == 10, "C -> T: 15 - 5"
    assert CLASS_GRAPH[0][1] == 40, "saturate must change the residual graph only"


def test_reachable() -> None:
    """Why: the cut is found from the vertices the source can still reach."""
    chain = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]  # 0 -> 1 only
    assert reachable(chain, 0) == {0, 1}, "0 reaches itself and 1, not 2"


def test_class_graph_max_flow_and_cut() -> None:
    """Why: the example from class: maximum flow 20, three cut edges."""
    flow, cut = ford_fulkerson(CLASS_GRAPH, 0, 7)
    assert flow == 20, f"maximum flow is 20, got {flow}"
    assert sorted(cut) == [(1, 2), (1, 5), (4, 5)], f"wrong cut: {sorted(cut)}"
    assert sum(CLASS_GRAPH[u][v] for u, v in cut) == flow, (
        "the cut's capacities must add up to the maximum flow"
    )


def test_diamond() -> None:
    """Why: a second graph, small enough to check by hand: 2 + 2 = 4."""
    flow, cut = ford_fulkerson(DIAMOND, 0, 3)
    assert flow == 4, f"maximum flow is 4, got {flow}"
    assert sum(DIAMOND[u][v] for u, v in cut) == 4, "the cut must carry 4"


def test_input_graph_unchanged() -> None:
    """Why: the input is the map; only the working copy may be destroyed."""
    before = deep_copy(CLASS_GRAPH)
    ford_fulkerson(CLASS_GRAPH, 0, 7)
    assert CLASS_GRAPH == before, "ford_fulkerson changed its input graph"


def test_disconnected_target() -> None:
    """Why: no path at all means no flow and no edges to cut."""
    islands = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]  # nothing reaches vertex 2
    flow, cut = ford_fulkerson(islands, 0, 2)
    assert flow == 0 and cut == [], f"expected (0, []), got ({flow}, {cut})"


def test_rejects_a_cycle() -> None:
    """Why: the algorithm is only promised for acyclic graphs (needs Part B)."""
    looped = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]  # 0 -> 1 -> 2 -> 0
    try:
        ford_fulkerson(looped, 0, 2)
        raised = False
    except ValueError:
        raised = True
    assert raised, "a cyclic graph should raise ValueError"


def run_tests() -> None:
    """Run every given test and report the result."""
    tests = [
        test_deep_copy_is_independent,
        test_path_exists_and_is_valid,
        test_no_path_returns_none,
        test_path_does_not_loop_on_back_edges,
        test_bottleneck,
        test_saturate,
        test_reachable,
        test_class_graph_max_flow_and_cut,
        test_diamond,
        test_input_graph_unchanged,
        test_disconnected_target,
        test_rejects_a_cycle,
        test_is_acyclic,  # yours: it passes trivially until you write asserts
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  ok    {test.__name__}")
            passed += 1
        except Exception as problem:  # a crash is a failure too
            print(f"  FAIL  {test.__name__}: {problem}")
    print(f"\n{passed} of {len(tests)} tests passed.")


if __name__ == "__main__":
    run_tests()
    maximum, edges = ford_fulkerson(CLASS_GRAPH, 0, 7)
    print(f"Maximum flow: {maximum}")
    print("Minimum cut: " + ", ".join(f"{NAMES[u]}->{NAMES[v]}" for u, v in edges))


"""
QUESTIONS:
1. 
2. If i made a shallow copy of the graph, the test to see if the graph comes back unchanged would fail because a shallow copy would take the 
    changes on the residual and impact the original graph
3. 
"""
