# Prim's MST using heap
import heapq

def prim_mst(graph, start):
    # graph format:
    # { A: [(B, w), (C, w)], B: [(A, w), ...] }

    visited = set()
    mst_edges = []
    pq = []

    visited.add(start)
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

    return mst_edges
