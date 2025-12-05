import heapq

def dijkstra(adj, start, end):
    if start not in adj or end not in adj:
        return []

    pq = [(0, start)]
    dist = {start: 0}
    parent = {start: None}

    while pq:
        curr_dist, node = heapq.heappop(pq)

        if node == end:
            break

        for neighbor, weight in adj.get(node, []):
            new_dist = curr_dist + weight

            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    if end not in parent:
        return []

    # reconstruct path
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]
