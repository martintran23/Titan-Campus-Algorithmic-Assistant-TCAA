import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.greedy import greedy_schedule
from algorithms.knapsack import knapsack


class StudyPlanner(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tasks = []  # list of tuples (name, time, value)
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Study Planner (Greedy + 0/1 Knapsack)", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10, anchor="w")

        form = ttk.Frame(self)
        form.pack(padx=10, pady=5, fill="x")

        ttk.Label(form, text="Task Name:").grid(row=0, column=0, sticky="e", padx=4, pady=2)
        ttk.Label(form, text="Time (int):").grid(row=1, column=0, sticky="e", padx=4, pady=2)
        ttk.Label(form, text="Value (int):").grid(row=2, column=0, sticky="e", padx=4, pady=2)

        self.name_entry = ttk.Entry(form, width=30)
        self.time_entry = ttk.Entry(form, width=10)
        self.value_entry = ttk.Entry(form, width=10)

        self.name_entry.grid(row=0, column=1, padx=4, pady=2, sticky="w")
        self.time_entry.grid(row=1, column=1, padx=4, pady=2, sticky="w")
        self.value_entry.grid(row=2, column=1, padx=4, pady=2, sticky="w")

        ttk.Button(form, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=6)

        # Task list
        list_frame = ttk.LabelFrame(self, text="Current Tasks")
        list_frame.pack(padx=10, pady=6, fill="both", expand=False)

        self.task_listbox = tk.Listbox(list_frame, height=6)
        self.task_listbox.pack(side="left", padx=6, pady=6, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        # time input and run buttons
        bottom = ttk.Frame(self)
        bottom.pack(padx=10, pady=8, fill="x")

        ttk.Label(bottom, text="Available Time (int):").grid(row=0, column=0, padx=4, pady=2, sticky="w")
        self.available_entry = ttk.Entry(bottom, width=10)
        self.available_entry.grid(row=0, column=1, padx=4, pady=2, sticky="w")
        self.available_entry.insert(0, "8")

        ttk.Button(bottom, text="Run Greedy Scheduler", command=self.run_greedy).grid(row=0, column=2, padx=8)
        ttk.Button(bottom, text="Run DP Knapsack (Optimal)", command=self.run_dp).grid(row=0, column=3, padx=8)

        # Results
        results_frame = ttk.LabelFrame(self, text="Results")
        results_frame.pack(padx=10, pady=6, fill="both", expand=True)

        self.results_text = tk.Text(results_frame, height=12, wrap="word")
        self.results_text.pack(padx=6, pady=6, fill="both", expand=True)

    def add_task(self):
        name = self.name_entry.get().strip()
        time_s = self.time_entry.get().strip()
        value_s = self.value_entry.get().strip()

        if not name or not time_s or not value_s:
            messagebox.showerror("Input error", "Please fill all fields.")
            return

        try:
            t = int(time_s)
            v = int(value_s)
            if t <= 0:
                raise ValueError("Time must be positive")
        except ValueError as e:
            messagebox.showerror("Input error", f"Invalid time/value: {e}")
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
            messagebox.showerror("Error", "Available time must be an integer.")
            return

        chosen, total_time, total_value = greedy_schedule(self.tasks, avail)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "=== Greedy Scheduler (value/time ratio) ===\n\n")
        if not chosen:
            self.results_text.insert(tk.END, "No tasks fit in the available time.\n")
            return
        for name, t, v in chosen:
            self.results_text.insert(tk.END, f"{name} — time: {t}, value: {v}\n")
        self.results_text.insert(tk.END, f"\nTotal time used: {total_time}\nTotal value: {total_value}\n")

    def run_dp(self):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks added.")
            return
        try:
            avail = int(self.available_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Available time must be an integer.")
            return

        chosen, total_time, total_value = knapsack(self.tasks, avail)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "=== 0/1 Knapsack (DP optimal) ===\n\n")
        if not chosen:
            self.resul
