# app.py
import tkinter as tk
from tkinter import ttk

from gui import info_tab
from gui.campus_navigator import NavigatorTab
from gui.info_tab import AlgorithmInfoTab
from gui.notes_search import NotesSearchTab
from gui.study_planner import StudyPlannerTab
from algorithms.graphs import sample_campus_graph  # You define this


class TCAAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Titan Campus Algorithmic Assistant (TCAA)")
        self.geometry("900x700")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Campus Navigator Tab
        navigator = NavigatorTab(notebook, sample_campus_graph)
        notebook.add(navigator, text="Campus Navigator")

        # Algorithm Info Tab
        info_tab = info_tab.AlgorithmInfoTab(notebook)
        notebook.add(info_tab, text="Algorithm Info")

        # Notes Search Tab
        notes_tab = NotesSearchTab(notebook)
        notebook.add(notes_tab, text="Notes Search")

        # Study Planner Tab
        study_tab = StudyPlannerTab(notebook)
        notebook.add(study_tab, text="Study Planner")


if __name__ == "__main__":
    app = TCAAApp()
    app.mainloop()
