import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import PyPDF2
from docx import Document

from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp
from algorithms.kmp import kmp_search


class NotesSearch(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text_data = ""
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Notes Search Engine", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=8)

        ttk.Button(
            self, text="Load File (TXT/PDF/DOCX)", command=self.load_file
        ).grid(row=1, column=0, padx=6, pady=6, sticky="w")

        ttk.Label(self, text="Pattern:").grid(row=2, column=0, sticky="e", padx=4)
        self.pattern_entry = ttk.Entry(self, width=40)
        self.pattern_entry.grid(row=2, column=1, padx=4, pady=4, sticky="w")

        ttk.Button(self, text="Naive", command=self.run_naive).grid(row=3, column=0, padx=4, pady=6)
        ttk.Button(self, text="Rabin-Karp", command=self.run_rk).grid(row=3, column=1, padx=4, pady=6)
        ttk.Button(self, text="KMP", command=self.run_kmp).grid(row=3, column=2, padx=4, pady=6)
        ttk.Button(self, text="Run All (Compare)", command=self.run_all).grid(row=3, column=3, padx=4, pady=6)

        self.output = tk.Text(self, height=20, width=95, wrap="word")
        self.output.grid(row=4, column=0, columnspan=4, padx=8, pady=8)

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("PDF Files", "*.pdf"),
                ("Word Files", "*.docx"),
            ]
        )
        if not path:
            return

        data = ""

        # TXT
        if path.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()

        # PDF
        elif path.lower().endswith(".pdf"):
            try:
                reader = PyPDF2.PdfReader(path)
                parts = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        parts.append(text)
                data = "\n".join(parts)
            except Exception as e:
                messagebox.showerror("PDF Error", f"Failed to read PDF:\n{e}")
                return

        # DOCX
        elif path.lower().endswith(".docx"):
            try:
                doc = Document(path)  # FIXED HERE
                data = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                messagebox.showerror("DOCX Error", f"Failed to read DOCX:\n{e}")
                return

        self.text_data = data
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"Loaded file: {path}\nCharacters: {len(self.text_data)}\n\n")

    def run_naive(self):
        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showerror("Input error", "Enter a pattern to search.")
            return

        start = time.time()
        matches = naive_search(self.text_data, pattern)
        elapsed = time.time() - start

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "=== Naive Search ===\n")
        self.output.insert(tk.END, f"Matches: {matches}\n")
        self.output.insert(tk.END, f"Count: {len(matches)} | Time: {elapsed:.6f} sec\n")

    def run_rk(self):
        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showerror("Input error", "Enter a pattern to search.")
            return

        start = time.time()
        matches = rabin_karp(self.text_data, pattern)
        elapsed = time.time() - start

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "=== Rabin-Karp ===\n")
        self.output.insert(tk.END, f"Matches: {matches}\n")
        self.output.insert(tk.END, f"Count: {len(matches)} | Time: {elapsed:.6f} sec\n")

    def run_kmp(self):
        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showerror("Input error", "Enter a pattern to search.")
            return

        start = time.time()
        matches = kmp_search(self.text_data, pattern)
        elapsed = time.time() - start

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "=== KMP ===\n")
        self.output.insert(tk.END, f"Matches: {matches}\n")
        self.output.insert(tk.END, f"Count: {len(matches)} | Time: {elapsed:.6f} sec\n")

    def run_all(self):
        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showerror("Input error", "Enter a pattern to search.")
            return

        self.output.delete("1.0", tk.END)

        # Naive
        t0 = time.time()
        naive_matches = naive_search(self.text_data, pattern)
        naive_t = time.time() - t0

        # Rabin-Karp
        t1 = time.time()
        rk_matches = rabin_karp(self.text_data, pattern)
        rk_t = time.time() - t1

        # KMP
        t2 = time.time()
        kmp_matches = kmp_search(self.text_data, pattern)
        kmp_t = time.time() - t2

        self.output.insert(tk.END, "=== All Algorithms Comparison ===\n\n")
        self.output.insert(tk.END, f"Naive: {len(naive_matches)} matches | {naive_t:.6f} sec\n")
        self.output.insert(tk.END, f"Rabin-Karp: {len(rk_matches)} matches | {rk_t:.6f} sec\n")
        self.output.insert(tk.END, f"KMP: {len(kmp_matches)} matches | {kmp_t:.6f} sec\n\n")

        self.output.insert(tk.END, f"First 50 Naive indices: {naive_matches[:50]}\n")
        self.output.insert(tk.END, f"First 50 Rabin-Karp indices: {rk_matches[:50]}\n")
        self.output.insert(tk.END, f"First 50 KMP indices: {kmp_matches[:50]}\n")
