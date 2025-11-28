import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.prim import prim_mst
from algorithms.graphs import unweighted_graph, weighted_graph


class CampusNavigator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Use copies so the GUI can be modified later if needed
        self.unweighted = unweighted_graph
        self.weighted = weighted_graph

        self.buildings = sorted(list(self.unweighted.keys()))
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Campus Navigator", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="w")

        ttk.Label(self, text="Start:").grid(row=1, column=0, sticky="e", padx=4)
        ttk.Label(self, text="End:").grid(row=2, column=0, sticky="e", padx=4)

        self.start_var = tk.StringVar(value=self.buildings[0])
        self.end_var = tk.StringVar(value=self.buildings[0])

        self.start_cb = ttk.Combobox(self, values=self.buildings, textvariable=self.start_var, state="readonly")
        self.end_cb = ttk.Combobox(self, values=self.buildings, textvariable=self.end_var, state="readonly")

        self.start_cb.grid(row=1, column=1, padx=4, pady=4, sticky="w")
        self.end_cb.grid(row=2, column=1, padx=4, pady=4, sticky="w")

        ttk.Button(self, text="Run BFS (fewest hops)", command=self.handle_bfs).grid(row=1, column=2, padx=6)
        ttk.Button(self, text="Run DFS (traversal)", command=self.handle_dfs).grid(row=2, column=2, padx=6)
        ttk.Button(self, text="Run Dijkstra (weighted)", command=self.handle_dijkstra).grid(row=3, column=0, padx=6, pady=6)
        ttk.Button(self, text="Prim's MST", command=self.handle_prim).grid(row=3, column=1, padx=6, pady=6)

        # Output area
        self.output = tk.Text(self, width=80, height=20, wrap="word")
        self.output.grid(row=4, column=0, columnspan=4, padx=8, pady=8)

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def handle_bfs(self):
        start = self.start_var.get()
        end = self.end_var.get()
        if not start or not end:
            messagebox.showerror("Input error", "Please select both start and end.")
            return

        path = bfs(self.unweighted, start, end)
        self.clear_output()
        if path:
            self.output.insert(tk.END, f"BFS path (fewest hops) from {start} to {end}:\n{path}\n")
            self.output.insert(tk.END, f"Hops: {len(path) - 1}\n")
        else:
            self.output.insert(tk.END, f"No path found between {start} and {end} using BFS.\n")

    def handle_dfs(self):
        start = self.start_var.get()
        if not start:
            messagebox.showerror("Input error", "Please select a start building.")
            return

        order = dfs(self.unweighted, start)
        connected = len(order) == len(self.unweighted)
        self.clear_output()
        self.output.insert(tk.END, f"DFS traversal starting at {start}:\n")
        self.output.insert(tk.END, f"{order}\n\nGraph connected: {connected}\n")

    def handle_dijkstra(self):
        start = self.start_var.get()
        end = self.end_var.get()
        if not start or not end:
            messagebox.showerror("Input error", "Please select both start and end.")
            return

        dist, parent = dijkstra(self.weighted, start)
        self.clear_output()
        if end not in parent and end != start and dist.get(end, float("inf")) == float("inf"):
            self.output.insert(tk.END, f"No path found from {start} to {end}.\n")
            return

        # reconstruct path from parent map
        path = []
        cur = end
        # if there is no parent for end but end == start, path is [start]
        if cur == start:
            path = [start]
        else:
            while cur is not None:
                path.append(cur)
                cur = parent.get(cur)
            path.reverse()

        self.output.insert(tk.END, f"Dijkstra shortest path from {start} to {end}:\n")
        self.output.insert(tk.END, f"Path: {path}\n")
        self.output.insert(tk.END, f"Distance: {dist.get(end, float('inf'))}\n")

    def handle_prim(self):
        # Choose an arbitrary start (first building)
        start = self.buildings[0]
        mst = prim_mst(self.weighted, start)
        self.clear_output()
        if not mst:
            self.output.insert(tk.END, "MST could not be constructed (graph may be disconnected).\n")
            return

        total_weight = sum(w for _, _, w in mst)
        self.output.insert(tk.END, "Prim's MST edges (u - v : weight):\n")
        for u, v, w in mst:
            self.output.insert(tk.END, f"{u} - {v} : {w}\n")
        self.output.insert(tk.END, f"\nTotal MST weight: {total_weight}\n")
