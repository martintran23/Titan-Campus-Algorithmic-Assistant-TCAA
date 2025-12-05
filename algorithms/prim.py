# Prim's MST using heap
import heapq

def prim_mst(graph, start=None):
    """
    graph format:
    {
        'A': [('B', w), ('C', w)],
        'B': [('A', w), ...]
    }

    Returns:
        mst_edges = [(u, v, w), ...]
        total_weight = sum of edge weights
    """

    if not graph:
        return [], 0

    # Pick a default start node if none given
    if start is None:
        start = next(iter(graph))

    visited = set()
    mst_edges = []
    pq = []

    visited.add(start)

    # Load initial edges
    for neighbor, weight in graph[start]:
        heapq.heappush(pq, (weight, start, neighbor))

    while pq:
        w, u, v = heapq.heappop(pq)

        if v in visited:
            continue

        visited.add(v)
        mst_edges.append((u, v, w))

        for nxt, wt in graph[v]:
            if nxt not in visited:
                heapq.heappush(pq, (wt, v, nxt))

    total_weight = sum(edge[2] for edge in mst_edges)
    return mst_edges, total_weight
