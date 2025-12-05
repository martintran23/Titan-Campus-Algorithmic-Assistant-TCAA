from collections import deque

def bfs(adj, start, end):
    if start not in adj or end not in adj:
        return []

    queue = deque([start])
    visited = {start: None}

    while queue:
        node = queue.popleft()

        if node == end:
            break

        for neighbor, _ in adj.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = node
                queue.append(neighbor)

    # reconstruct path
    if end not in visited:
        return []

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = visited[curr]
    return path[::-1]
