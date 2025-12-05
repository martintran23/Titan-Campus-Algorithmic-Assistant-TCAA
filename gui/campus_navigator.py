import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra

NODE_RADIUS = 18


# ============================================================
# GRAPH DATA STRUCTURES
# ============================================================

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.canvas_id = None
        self.text_id = None


class Edge:
    def __init__(self, a, b, weight=1):
        self.a = a
        self.b = b
        self.weight = weight
        self.line_id = None


class Graph:
    def __init__(self):
        self.nodes = {}       # name -> Node
        self.edges = {}       # (a,b) -> Edge

    def add_node(self, name, x, y):
        self.nodes[name] = Node(name, x, y)

    def connect(self, a, b, weight=1):
        key = tuple(sorted([a, b]))
        self.edges[key] = Edge(key[0], key[1], weight)

    def adjacency_list(self):
        adj = {n: [] for n in self.nodes}
        for (a, b), e in self.edges.items():
            adj[a].append((b, e.weight))
            adj[b].append((a, e.weight))
        return adj


# ============================================================
# GRAPH CANVAS (INTERACTIVE)
# ============================================================

class GraphCanvas(ttk.Frame):
    def __init__(self, parent, nav_callback):
        super().__init__(parent)
        self.nav_callback = nav_callback

        self.graph = Graph()

        self.selected = None
        self.drag_node = None
        self.drag_offset = (0, 0)

        self.connect_mode = False
        self.connect_first = None

        self.canvas = tk.Canvas(self, bg="white", height=350)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    # --------------------------------------------------------
    # INTERACTION
    # --------------------------------------------------------

    def on_click(self, event):
        x, y = event.x, event.y
        clicked = self.node_at(x, y)

        if self.connect_mode:
            self.handle_connect_mode(clicked)
            return

        # If clicked on a node: select it
        if clicked:
            self.selected = clicked
            node = self.graph.nodes[clicked]
            self.drag_node = clicked
            self.drag_offset = (node.x - x, node.y - y)

            self.nav_callback("select", clicked)
            return

        # Otherwise add a new node
        name = f"N{len(self.graph.nodes) + 1}"
        self.graph.add_node(name, x, y)
        self.draw_node(self.graph.nodes[name])
        self.nav_callback("graph_changed", None)

    def on_drag(self, event):
        if not self.drag_node:
            return

        name = self.drag_node
        node = self.graph.nodes[name]

        node.x = event.x + self.drag_offset[0]
        node.y = event.y + self.drag_offset[1]

        self.redraw()

    def on_release(self, event):
        self.drag_node = None

    # --------------------------------------------------------
    # CONNECTION MODE
    # --------------------------------------------------------

    def handle_connect_mode(self, clicked):
        if not clicked:
            return

        if not self.connect_first:
            self.connect_first = clicked
            return

        if clicked != self.connect_first:
            self.graph.connect(self.connect_first, clicked)
            self.redraw()
            self.nav_callback("graph_changed", None)

        self.connect_first = None

    # --------------------------------------------------------
    # HIT DETECTION
    # --------------------------------------------------------

    def node_at(self, x, y):
        for name, node in self.graph.nodes.items():
            if (node.x - x) ** 2 + (node.y - y) ** 2 <= NODE_RADIUS ** 2:
                return name
        return None

    # --------------------------------------------------------
    # DRAWING
    # --------------------------------------------------------

    def draw_node(self, node, highlight=False):
        r = NODE_RADIUS
        color = "yellow" if highlight else "white"

        cid = self.canvas.create_oval(
            node.x - r, node.y - r,
            node.x + r, node.y + r,
            fill=color, outline="black", width=2
        )
        tid = self.canvas.create_text(node.x, node.y, text=node.name)

        node.canvas_id = cid
        node.text_id = tid

    def draw_edge(self, e, highlight=False):
        a = self.graph.nodes[e.a]
        b = self.graph.nodes[e.b]
        col = "red" if highlight else "black"

        e.line_id = self.canvas.create_line(a.x, a.y, b.x, b.y, width=2, fill=col)

    def redraw(self, highlight_path=None):
        self.canvas.delete("all")

        # draw edges first
        for edge in self.graph.edges.values():
            key = (edge.a, edge.b)
            if highlight_path and key in highlight_path:
                self.draw_edge(edge, highlight=True)
            else:
                self.draw_edge(edge)

        # draw nodes
        for name, node in self.graph.nodes.items():
            hl = highlight_path and name in highlight_path
            self.draw_node(node, highlight=hl)

    # --------------------------------------------------------
    # PATH VISUALIZATION
    # --------------------------------------------------------

    def highlight_path(self, path):
        if not path or len(path) < 2:
            return self.redraw()

        edge_set = set()
        node_set = set(path)

        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            edge_set.add(tuple(sorted([a, b])))

        self.redraw(highlight_path=edge_set | node_set)


# ============================================================
# MAIN CAMPUS NAVIGATOR PANEL
# ============================================================

class CampusNavigator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.start = None
        self.end = None

        # HEADER
        ttk.Label(self, text="Campus Navigator", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=10
        )

        # CONTROLS LEFT
        control = ttk.Frame(self)
        control.grid(row=1, column=0, sticky="n")

        ttk.Button(control, text="Connect Nodes", command=self.enable_connect).pack(pady=4)
        ttk.Button(control, text="Set Start", command=lambda: self.set_mode("start")).pack(pady=4)
        ttk.Button(control, text="Set End", command=lambda: self.set_mode("end")).pack(pady=4)
        ttk.Button(control, text="Run BFS", command=self.run_bfs).pack(pady=4)
        ttk.Button(control, text="Run DFS", command=self.run_dfs).pack(pady=4)
        ttk.Button(control, text="Run Dijkstra", command=self.run_dijkstra).pack(pady=4)

        # OUTPUT
        self.output = tk.Text(self, width=50, height=15)
        self.output.grid(row=1, column=1, padx=10)

        # ADJACENCY
        self.adj_box = tk.Text(self, width=30, height=15)
        self.adj_box.grid(row=1, column=2, padx=10)

        # CANVAS
        self.canvas_panel = GraphCanvas(self, self.canvas_event)
        self.canvas_panel.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

        self.grid_rowconfigure(2, weight=1)

    # --------------------------------------------------------
    # EVENTS FROM CANVAS
    # --------------------------------------------------------

    def canvas_event(self, event_type, data):
        if event_type == "select":
            if self.mode == "start":
                self.start = data
                self.output.insert(tk.END, f"Start set: {data}\n")
            elif self.mode == "end":
                self.end = data
                self.output.insert(tk.END, f"End set: {data}\n")

        elif event_type == "graph_changed":
            self.update_adj_list()

    # --------------------------------------------------------
    # MODES
    # --------------------------------------------------------

    def set_mode(self, mode):
        self.mode = mode
        self.canvas_panel.connect_mode = False

    def enable_connect(self):
        self.canvas_panel.connect_mode = True
        self.mode = None

    # --------------------------------------------------------
    # ALGORITHMS
    # --------------------------------------------------------

    def update_adj_list(self):
        adj = self.canvas_panel.graph.adjacency_list()
        self.adj_box.delete("1.0", tk.END)
        for k, v in adj.items():
            self.adj_box.insert(tk.END, f"{k}: {v}\n")

    def run_bfs(self):
        if not (self.start and self.end):
            return messagebox.showerror("Error", "Set start and end nodes first.")

        adj = self.canvas_panel.graph.adjacency_list()
        path = bfs(adj, self.start, self.end)

        self.output.insert(tk.END, f"BFS Path: {path}\n")
        self.canvas_panel.highlight_path(path)

    def run_dfs(self):
        if not (self.start and self.end):
            return messagebox.showerror("Error", "Set start and end nodes first.")

        adj = self.canvas_panel.graph.adjacency_list()
        path = dfs(adj, self.start, self.end)

        self.output.insert(tk.END, f"DFS Path: {path}\n")
        self.canvas_panel.highlight_path(path)

    def run_dijkstra(self):
        if not (self.start and self.end):
            return messagebox.showerror("Error", "Set start and end nodes first.")

        adj = self.canvas_panel.graph.adjacency_list()
        path = dijkstra(adj, self.start, self.end)

        self.output.insert(tk.END, f"Dijkstra Path: {path}\n")
        self.canvas_panel.highlight_path(path)
