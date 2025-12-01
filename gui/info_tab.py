import tkinter as tk
from tkinter import ttk

BG = "#f6fbff"
PANEL = "#eaf4ff"
TEXT = "#1b1b1b"

class InfoTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_style()
        self._create_layout()

    def _setup_style(self):
        style = ttk.Style()
        style.configure("Card.TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background=BG)

    def _create_layout(self):
        ttk.Label(self, text="Algorithm Info & P vs NP", style="Title.TLabel").pack(anchor="w", padx=12, pady=10)

        container = ttk.Frame(self, style="Panel.TFrame", padding=(10,8))
        container.pack(fill="both", expand=True, padx=12, pady=6)

        canvas = tk.Canvas(container, background=PANEL)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        content = ttk.Frame(canvas, style="Panel.TFrame")

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Sections
        self._add_section(content, "Graph Algorithms — Big-O", """
BFS: O(V + E)
DFS: O(V + E)
Dijkstra (binary heap): O((V + E) log V)
Prim's MST (binary heap): O(E log V)
        """)

        self._add_section(content, "Greedy & Dynamic Programming", """
Greedy Scheduling: O(n log n) due to sorting.
0/1 Knapsack (DP): O(n * W) time, O(n * W) space (W = capacity). This is pseudo-polynomial.
        """)

        self._add_section(content, "String Matching", """
Naive: O(n * m)
Rabin-Karp: Average O(n + m), Worst-case O(n * m)
KMP: O(n + m)
        """)

        self._add_section(content, "P vs NP (Short Reflection)", """
P: Problems solvable in polynomial time.
NP: Problems whose solutions can be verified in polynomial time.
Whether P == NP is an open question. Many important optimization problems (e.g., exact Knapsack, TSP) are NP-hard.
Note: The DP knapsack solves exact knapsack in pseudo-polynomial time depending on capacity.
        """)

    def _add_section(self, parent, header, body):
        ttk.Label(parent, text=header, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(8,2))
        ttk.Label(parent, text=body, wraplength=820, justify="left").pack(anchor="w")
