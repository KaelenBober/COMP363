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
    n = len(graph)
    #reuse label_components from graphs assignment
    # unlabel everything
    comp = [_] * n
    next_label = 0
    for starting_vertex in range(n):
        if comp[starting_vertex] == _:
            for v in reach(starting_vertex, graph):
                comp[v] = next_label
            next_label += 1
    #next_label increments wiht new component, you might say its the count pershlaps
    count = next_label

    return (count, comp)




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
    #create the edge-less graph
    t = initialize_mst(graph)
    #get count of components 
    count, comp = count_label(t)
    #add components together until there is only one left
    
    while count > 1:
        addAllSafeEdges(graph, t, count, comp)
        count, comp = count_label(t)
    return t 




def addAllSafeEdges(graph, t, count, comp):
    #safe has a spot for each component
    safe = [None] * count
    #check through graph storing weight
    n = len(graph)
    for u in range(n):
        #need to go over higher to not repeat the same ones in different order
        for v in range(u+1, n):
            #ignore if no edge
            if graph[u][v] != float("inf"):
                #get edge weight
                w = graph[u][v]
                #compare two vertices, if not in same component check for minimal weight, add the edge in with its weight, 
                #weight comparison over and over
                if comp[u] != comp[v]:
                    if safe[comp[u]] is None or w < safe[comp[u]][-1]:
                        safe[comp[u]] = [u,v,w]
                    if safe[comp[v]] is None or w < safe[comp[v]][-1]:
                        safe[comp[v]] = [u,v,w]
    #return the safe edges to t
    for i in safe:
        if i is not None:
            u,v,w = i
            t[u][v] = w
            t[v][u] = w



t = boruvka_mst(g)
for i in t:
    print(i)
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



'''
NOTES:

This assignment was definitely the hardest one we have been given. Compared to other assignments the notation felt easier to grasp and the book + the slide show made
it very easy for me to understand what I needed to do on paper. Starting the code was similar, i thought of it like the graph assignment at first, but having the 
whole algorithm written out in the book made feel easy, with no big issues than small bugs up until getting to the helper method. That is where my progress pretty much stopped in its tracks. I
spent most of my time debugging the helper method addAllSafeEdges, with these three problems being my biggest issues.
1.      I couldn't figure out what how to pass uv into safe[comp[u/v]] like the book did, thinking it meant I was supposed to pass just the weight to represent the safeedge 
    using graph[u][v]. After some rereading and whiteboard work, i realized i needed to pass the edge [u][v] and its weight [w] because it needed a way to be added into t. I tried a few different ways to store the three vlaues, including trying to have a seperate list values 
    that stored them, then a dictionary before getting stuck and using claude to give me some guidance. I gave it my code and prompted 
    "I am trying to pass the edge and its weight after comparing the weights of the edge vs safe's index. Without giving me a direct implementation, lead me in the right direction of a way
    to do this."
    After some trial and error, I ended up with using [u,v,w] to pass the edge and its weight, then accessing the weight directly using [-1] index. 
2.      Returning the safe edges into t was tricky as well. I was getting stuck with the fact I had the list storing my values while I was trying to use a for loop 
    off of count like the book did, and couldnt figure out how to assign the index count was at to sign while still knowing what was at each index. After some time sitting and staring, re-reading my method,
    then finally tracing it out on a table, i realized i could actually just use safe becuase it holds the values directly, then do something similar to "safe[comp[u]] = [u,v,w]" but backwards. I used it to assign 
    the values from each edge together and then also mirrored it, as I accounted for the repeats earlier in my loop.
3. Accessing the graph in O(ElogV) time was something I didn't figure out. I was having so much trouble trying to figure out the time complexity and spent way too long
    that I needed to give up on it if I wanted to finish the rest of the method.

    I would say that this implementation of the boruvka algorithm isnt mine. While I did most of the implementation, the part i got
    assistance trying to figure out was arguably the most important part. I think if I started earlier and and reached out to you for assistance
    I could have ended up solving it without needing to use other resources, as the notation this time around was relatively straight forward compared to \
    other assignments.
'''