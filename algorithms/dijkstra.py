# Dijkstra – Weighted shortest path
import heapq

def dijkstra(graph, start):
    # graph is adjacency list: { A: [(B, weight), (C, weight)] }
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    parent = {start: None}
    pq = [(0, start)]

    while pq:
        current_dist, node = heapq.heappop(pq)
        if current_dist > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    return dist, parent
