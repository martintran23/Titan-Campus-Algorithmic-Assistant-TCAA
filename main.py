import tkinter as tk
from tkinter import ttk
from gui.campus_navigator import CampusNavigator
from gui.study_planner import StudyPlanner
from gui.notes_search import NotesSearch
from gui.info_tab import InfoTab

def main():
    root = tk.Tk()
    root.title("Titan Campus Algorithmic Assistant (TCAA)")
    root.geometry("900x600")

    tabs = ttk.Notebook(root)

    tabs.add(CampusNavigator(tabs), text="Campus Navigator")
    tabs.add(StudyPlanner(tabs), text="Study Planner")
    tabs.add(NotesSearch(tabs), text="Notes Search Engine")
    tabs.add(InfoTab(tabs), text="Algorithm Info")

    tabs.pack(expand=True, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main()
