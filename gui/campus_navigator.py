import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.prim import prim_mst
from algorithms.graphs import unweighted_graph, weighted_graph


# Theme constants (light blue accent)
BG = "#f6fbff"
PANEL = "#eaf4ff"
ACCENT = "#6fa8ff"
TEXT = "#1b1b1b"

class CampusNavigator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="Card.TFrame")
        # copy graph references
        self.unweighted = unweighted_graph
        self.weighted = weighted_graph
        self.buildings = sorted(list(self.unweighted.keys()))

        self._create_style()
        self._create_layout()

    def _create_style(self):
        style = ttk.Style()
        # Set theme-specific colors
        style.configure("Card.TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL, relief="flat")
        style.configure("Accent.TButton", background=ACCENT, foreground="white")
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background=BG, foreground=TEXT)
        style.configure("Label.TLabel", background=BG, foreground=TEXT)
        style.configure("Small.TLabel", background=PANEL, foreground=TEXT)
        style.configure("Output.TText", background="white", foreground=TEXT)

    def _create_layout(self):
        # Header
        header = ttk.Label(self, text="Campus Navigator", style="Title.TLabel")
        header.grid(row=0, column=0, columnspan=4, sticky="w", padx=12, pady=(12,6))

        # Left panel: controls
        controls = ttk.Frame(self, style="Panel.TFrame", padding=(12,10))
        controls.grid(row=1, column=0, sticky="nsew", padx=10, pady=8)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ttk.Label(controls, text="Start:", style="Small.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(controls, text="End:", style="Small.TLabel").grid(row=1, column=0, sticky="w")

        self.start_var = tk.StringVar(value=self.buildings[0] if self.buildings else "")
        self.end_var = tk.StringVar(value=self.buildings[0] if self.buildings else "")

        self.start_cb = ttk.Combobox(controls, values=self.buildings, textvariable=self.start_var, state="readonly", width=20)
        self.end_cb = ttk.Combobox(controls, values=self.buildings, textvariable=self.end_var, state="readonly", width=20)
        self.start_cb.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        self.end_cb.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        btn_frame = ttk.Frame(controls, style="Panel.TFrame")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(8,0))

        ttk.Button(btn_frame, text="BFS (Fewest Hops)", command=self._handle_bfs).grid(row=0, column=0, padx=4, pady=4)
        ttk.Button(btn_frame, text="DFS / Connectivity", command=self._handle_dfs).grid(row=0, column=1, padx=4, pady=4)
        ttk.Button(btn_frame, text="Dijkstra (Weighted)", command=self._handle_dijkstra).grid(row=1, column=0, padx=4, pady=4)
        ttk.Button(btn_frame, text="MST (Prim)", command=self._handle_prim).grid(row=1, column=1, padx=4, pady=4)

        # Middle: results (large)
        results_frame = ttk.Frame(self, style="Panel.TFrame", padding=(8,8))
        results_frame.grid(row=1, column=1, sticky="nsew", padx=(0,8), pady=8)
        self.grid_columnconfigure(1, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(results_frame, text="Output", style="Small.TLabel").grid(row=0, column=0, sticky="w")
        self.output = tk.Text(results_frame, height=20, wrap="word")
        self.output.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)

        # Right: adjacency / graph display
        graph_frame = ttk.Frame(self, style="Panel.TFrame", padding=(8,8))
        graph_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=8)
        self.grid_columnconfigure(2, weight=0)
        ttk.Label(graph_frame, text="Graph (adjacency list):", style="Small.TLabel").pack(anchor="w")
        self.graph_text = tk.Text(graph_frame, height=20, width=40, wrap="word")
        self.graph_text.pack(fill="both", expand=True, padx=6, pady=6)
        self._render_graph_display()

    def _render_graph_display(self):
        # show weighted adjacency nicely
        lines = []
        for node in sorted(self.weighted.keys()):
            neighs = ", ".join([f"{n}({w})" for n, w in self.weighted[node]])
            lines.append(f"{node}: {neighs}")
        self.graph_text.delete("1.0", tk.END)
        self.graph_text.insert(tk.END, "\n".join(lines))

    def _clear_output(self):
        self.output.delete("1.0", tk.END)

    def _handle_bfs(self):
        start = self.start_var.get()
        end = self.end_var.get()
        if not start or not end:
            messagebox.showerror("Input error", "Please select start and end.")
            return
        path = bfs(self.unweighted, start, end)
        self._clear_output()
        if path:
            self.output.insert(tk.END, f"BFS path ({start} → {end})\n")
            self.output.insert(tk.END, f"Path: {path}\nHops: {len(path)-1}\n")
        else:
            self.output.insert(tk.END, "No path found (BFS).")

    def _handle_dfs(self):
        start = self.start_var.get()
        if not start:
            messagebox.showerror("Input error", "Please select a start building.")
            return
        order = dfs(self.unweighted, start)
        connected = (len(order) == len(self.unweighted))
        self._clear_output()
        self.output.insert(tk.END, f"DFS traversal starting at {start}:\n{order}\n\n")
        self.output.insert(tk.END, f"Graph connected: {connected}\n")

    def _handle_dijkstra(self):
        start = self.start_var.get()
        end = self.end_var.get()
        if not start or not end:
            messagebox.showerror("Input error", "Please select start and end.")
            return
        dist, parent = dijkstra(self.weighted, start)
        self._clear_output()
        distance = dist.get(end, float("inf"))
        if distance == float("inf"):
            self.output.insert(tk.END, f"No reachable path from {start} to {end} (Dijkstra).\n")
            return
        # reconstruct path
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path.reverse()
        self.output.insert(tk.END, f"Dijkstra shortest path ({start} → {end}):\nPath: {path}\nDistance: {distance}\n")

    def _handle_prim(self):
        if not self.buildings:
            messagebox.showerror("Error", "Graph is empty.")
            return
        start = self.buildings[0]
        mst = prim_mst(self.weighted, start)
        self._clear_output()
        if not mst:
            self.output.insert(tk.END, "MST could not be constructed (disconnected?).\n")
            return
        total = sum(w for _, _, w in mst)
        self.output.insert(tk.END, "Prim's MST edges (u - v : w):\n")
        for u, v, w in mst:
            self.output.insert(tk.END, f"{u} - {v} : {w}\n")
        self.output.insert(tk.END, f"\nTotal MST cost: {total}\n")
