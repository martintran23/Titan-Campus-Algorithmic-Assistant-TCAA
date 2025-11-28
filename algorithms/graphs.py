# Simple mock campus graph
# For BFS / DFS (unweighted) → adjacency list
unweighted_graph = {
    "CS": ["Library", "Hall"],
    "Library": ["CS", "Quad"],
    "Hall": ["CS", "Gym"],
    "Quad": ["Library", "Gym"],
    "Gym": ["Hall", "Quad"],
}

# For Dijkstra / Prim (weighted)
weighted_graph = {
    "CS": [("Library", 2), ("Hall", 4)],
    "Library": [("CS", 2), ("Quad", 3)],
    "Hall": [("CS", 4), ("Gym", 6)],
    "Quad": [("Library", 3), ("Gym", 1)],
    "Gym": [("Hall", 6), ("Quad", 1)],
}
