def dfs(adj, start, end):
    stack = [start]
    visited = {start: None}

    while stack:
        node = stack.pop()

        if node == end:
            break

        for neighbor, _ in adj.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = node
                stack.append(neighbor)

    # reconstruct path
    if end not in visited:
        return []

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = visited[curr]
    return path[::-1]
