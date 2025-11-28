import tkinter as tk
from tkinter import ttk


class InfoTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Algorithm Info & P vs NP", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10, anchor="w", padx=8)

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        content = ttk.Frame(canvas)

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y")

        # Sections
        self.add_section(content, "Graph Algorithms (Big-O)", """
BFS: O(V + E)
DFS: O(V + E)
Dijkstra (binary heap): O((V + E) log V)
Prim's MST (binary heap): O(E log V)
        """)

        self.add_section(content, "Greedy & Dynamic Programming", """
Greedy Scheduling: O(n log n) (due to sorting)
0/1 Knapsack (DP): O(n * W) time, O(n * W) space (where W is capacity)
        """)

        self.add_section(content, "String Matching", """
Naive: O(n * m)
Rabin–Karp: Average O(n + m), Worst-case O(n * m)
KMP: O(n + m)
        """)

        self.add_section(content, "P vs NP (Short Reflection)", """
P: Problems solvable in polynomial time.
NP: Problems whose solutions can be verified in polynomial time.
Open question: Does P == NP? Unknown.
Examples of NP problems: SAT, exact Knapsack, TSP.

Note: The DP knapsack solution runs in pseudo-polynomial time (depends on capacity W).
        """)

    def add_section(self, parent, header, body):
        hdr = ttk.Label(parent, text=header, font=("Segoe UI", 12, "bold"))
        hdr.pack(anchor="w", pady=(8, 2))
        lbl = ttk.Label(parent, text=body, justify="left", wraplength=800)
        lbl.pack(anchor="w")
