import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.greedy import greedy_schedule
from algorithms.knapsack import knapsack

# Theme
BG = "#f6fbff"
PANEL = "#eaf4ff"
TEXT = "#1b1b1b"

class StudyPlanner(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="Card.TFrame")
        self.tasks = []
        self._setup_style()
        self._create_layout()

    def _setup_style(self):
        style = ttk.Style()
        style.configure("Card.TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background=BG)

    def _create_layout(self):
        ttk.Label(self, text="Study Planner", style="Title.TLabel").grid(row=0, column=0, sticky="w", padx=12, pady=10)

        # Input panel
        panel = ttk.Frame(self, style="Panel.TFrame", padding=(10,8))
        panel.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        ttk.Label(panel, text="Task Name:").grid(row=0, column=0, sticky="e", padx=6, pady=4)
        ttk.Label(panel, text="Time (int):").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        ttk.Label(panel, text="Value (int):").grid(row=2, column=0, sticky="e", padx=6, pady=4)

        self.name_entry = ttk.Entry(panel, width=30)
        self.time_entry = ttk.Entry(panel, width=10)
        self.value_entry = ttk.Entry(panel, width=10)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=6)
        self.time_entry.grid(row=1, column=1, sticky="w", padx=6)
        self.value_entry.grid(row=2, column=1, sticky="w", padx=6)

        ttk.Button(panel, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=8)

        # Task list & controls
        list_panel = ttk.Frame(self, style="Panel.TFrame", padding=(10,8))
        list_panel.grid(row=2, column=0, sticky="nsew", padx=12, pady=6)
        ttk.Label(list_panel, text="Tasks:").grid(row=0, column=0, sticky="w")
        self.task_listbox = tk.Listbox(list_panel, height=6)
        self.task_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=6, pady=6)

        ttk.Label(list_panel, text="Available Time:").grid(row=2, column=0, sticky="e")
        self.available_entry = ttk.Entry(list_panel, width=10)
        self.available_entry.grid(row=2, column=1, sticky="w", padx=6)
        self.available_entry.insert(0, "8")

        ttk.Button(list_panel, text="Run Greedy", command=self.run_greedy).grid(row=2, column=2, padx=6)
        ttk.Button(list_panel, text="Run DP (Knapsack)", command=self.run_dp).grid(row=2, column=3, padx=6)

        # Results panel
        results = ttk.Frame(self, style="Panel.TFrame", padding=(10,8))
        results.grid(row=3, column=0, sticky="nsew", padx=12, pady=6)
        ttk.Label(results, text="Results:").grid(row=0, column=0, sticky="w")
        self.results_text = tk.Text(results, height=12, wrap="word")
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)

    def add_task(self):
        name = self.name_entry.get().strip()
        t_s = self.time_entry.get().strip()
        v_s = self.value_entry.get().strip()

        if not name or not t_s or not v_s:
            messagebox.showerror("Input error", "Please fill all fields.")
            return
        try:
            t = int(t_s)
            v = int(v_s)
            if t <= 0:
                raise ValueError("Time must be positive")
        except ValueError as e:
            messagebox.showerror("Input error", f"Invalid numbers: {e}")
            return

        self.tasks.append((name, t, v))
        self.task_listbox.insert(tk.END, f"{name} — time: {t}, value: {v}")
        self.name_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def run_greedy(self):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks added.")
            return
        try:
            avail = int(self.available_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Available time must be integer.")
            return

        chosen, total_time, total_value = greedy_schedule(self.tasks, avail)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "=== Greedy Scheduler ===\n")
        if not chosen:
            self.results_text.insert(tk.END, "No tasks selected.\n")
            return
        for name, t, v in chosen:
            self.results_text.insert(tk.END, f"{name} — time: {t}, value: {v}\n")
        self.results_text.insert(tk.END, f"\nTotal time: {total_time}\nTotal value: {total_value}\n")

    def run_dp(self):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks added.")
            return
        try:
            avail = int(self.available_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Available time must be integer.")
            return

        chosen, total_time, total_value = knapsack(self.tasks, avail)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "=== 0/1 Knapsack (DP) ===\n")
        if not chosen:
            self.results_text.insert(tk.END, "No tasks selected.\n")
            return
        for name, t, v in chosen:
            self.results_text.insert(tk.END, f"{name} — time: {t}, value: {v}\n")
        self.results_text.insert(tk.END, f"\nTotal time: {total_time}\nOptimal value: {total_value}\n")
