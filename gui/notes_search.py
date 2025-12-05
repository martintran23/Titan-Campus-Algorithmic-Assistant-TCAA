import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import PyPDF2
from docx import Document

from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp
from algorithms.kmp import kmp_search

# Theme colors (light blue accent)
BG = "#f6fbff"
PANEL = "#eaf4ff"
ACCENT = "#6fa8ff"
TEXT = "#1b1b1b"

class NotesSearch(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="Card.TFrame")
        self.text_data = ""
        self._setup_style()
        self._create_layout()

    def _setup_style(self):
        style = ttk.Style()
        style.configure("Card.TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background=BG)
        style.configure("Small.TLabel", background=BG)

    def _create_layout(self):
        ttk.Label(self, text="Notes Search Engine", style="Title.TLabel").grid(
            row=0, column=0, columnspan=6, sticky="w", padx=12, pady=10
        )

        # Load + pattern row
        ttk.Button(self, text="Load Document", command=self.load_file).grid(
            row=1, column=0, padx=8, pady=6, sticky="w"
        )

        ttk.Label(self, text="Document:").grid(row=1, column=1, sticky="e")
        self.doc_label = ttk.Label(self, text="(none)", style="Small.TLabel")
        self.doc_label.grid(row=1, column=2, sticky="w")

        ttk.Label(self, text="Pattern:").grid(row=2, column=0, sticky="e", padx=8, pady=6)
        self.pattern_entry = ttk.Entry(self, width=36)
        self.pattern_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=4, pady=6)

        # Algorithm radio buttons
        self.alg_var = tk.StringVar(value="all")
        alg_frame = ttk.Frame(self)
        alg_frame.grid(row=3, column=0, columnspan=6, sticky="w", padx=8)

        ttk.Radiobutton(alg_frame, text="Naive", variable=self.alg_var, value="naive").pack(side="left", padx=6)
        ttk.Radiobutton(alg_frame, text="Rabin–Karp", variable=self.alg_var, value="rk").pack(side="left", padx=6)
        ttk.Radiobutton(alg_frame, text="KMP", variable=self.alg_var, value="kmp").pack(side="left", padx=6)
        ttk.Radiobutton(alg_frame, text="All (compare)", variable=self.alg_var, value="all").pack(side="left", padx=6)

        ttk.Button(self, text="Search", style="Accent.TButton", command=self.run_search).grid(
            row=2, column=3, padx=8, pady=6
        )

        # ===============================
        # TWO BOXES: PREVIEW + OUTPUT
        # ===============================

        # Left panel — document preview
        preview_frame = ttk.Frame(self)
        preview_frame.grid(row=4, column=0, columnspan=3, padx=12, pady=10, sticky="nsew")

        ttk.Label(preview_frame, text="Document Preview", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.preview = tk.Text(preview_frame, height=25, width=60, wrap="word")
        self.preview.pack(side="left", fill="both", expand=True)

        preview_scroll = ttk.Scrollbar(preview_frame, command=self.preview.yview)
        preview_scroll.pack(side="right", fill="y")
        self.preview.config(yscrollcommand=preview_scroll.set)

        # Right panel — search output
        output_frame = ttk.Frame(self)
        output_frame.grid(row=4, column=3, columnspan=3, padx=12, pady=10, sticky="nsew")

        ttk.Label(output_frame, text="Search Results", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.output = tk.Text(output_frame, height=25, width=60, wrap="word")
        self.output.pack(side="left", fill="both", expand=True)

        output_scroll = ttk.Scrollbar(output_frame, command=self.output.yview)
        output_scroll.pack(side="right", fill="y")
        self.output.config(yscrollcommand=output_scroll.set)

        # Allow resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

    # -----------------------------
    # LOAD FILE
    # -----------------------------
    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text", "*.txt"), ("PDF", "*.pdf"), ("Word", "*.docx")]
        )
        if not path:
            return

        doc_label = path.split("/")[-1].split("\\")[-1]
        self.doc_label.config(text=doc_label)

        data = ""
        try:
            if path.lower().endswith(".txt"):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    data = f.read()

            elif path.lower().endswith(".pdf"):
                reader = PyPDF2.PdfReader(path)
                parts = []
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        parts.append(txt)
                data = "\n".join(parts)

            elif path.lower().endswith(".docx"):
                doc = Document(path)
                data = "\n".join([p.text for p in doc.paragraphs])

        except Exception as e:
            messagebox.showerror("File error", f"Unable to load file:\n{e}")
            return

        self.text_data = data

        # Show full text in preview box
        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, data)

        # Clear output
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"Loaded: {doc_label}\nCharacters: {len(data)}")

    # -----------------------------
    # SEARCH
    # -----------------------------
    def run_search(self):
        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showerror("Input error", "Please enter a pattern.")
            return

        choice = self.alg_var.get()

        # Clear output
        self.output.delete("1.0", tk.END)

        # -----------------------
        # Single Algorithms
        # -----------------------
        if choice == "naive":
            t0 = time.time()
            matches = naive_search(self.text_data, pattern)
            t = time.time() - t0

            self.output.insert(tk.END, "=== Naive Search ===\n\n")
            self.output.insert(tk.END, f"Matches: {matches}\n")
            self.output.insert(tk.END, f"Count: {len(matches)} | Time: {t:.6f} s\n")
            return

        if choice == "rk":
            t0 = time.time()
            matches = rabin_karp(self.text_data, pattern)
            t = time.time() - t0

            self.output.insert(tk.END, "=== Rabin–Karp Search ===\n\n")
            self.output.insert(tk.END, f"Matches: {matches}\n")
            self.output.insert(tk.END, f"Count: {len(matches)} | Time: {t:.6f} s\n")
            return

        if choice == "kmp":
            t0 = time.time()
            matches = kmp_search(self.text_data, pattern)
            t = time.time() - t0

            self.output.insert(tk.END, "=== KMP Search ===\n\n")
            self.output.insert(tk.END, f"Matches: {matches}\n")
            self.output.insert(tk.END, f"Count: {len(matches)} | Time: {t:.6f} s\n")
            return

        # -----------------------
        # ALL — Comparison Mode
        # -----------------------
        if choice == "all":
            self.output.insert(tk.END, "=== Comparison Mode ===\n\n")

            # Naive
            t0 = time.time()
            naive_matches = naive_search(self.text_data, pattern)
            t_naive = time.time() - t0

            self.output.insert(tk.END, "► Naive Search\n")
            self.output.insert(tk.END, f"Matches: {len(naive_matches)}\n")
            self.output.insert(tk.END, f"Time: {t_naive:.6f} s\n")
            self.output.insert(tk.END, f"Sample: {naive_matches[:50]}\n\n")

            # Rabin–Karp
            t1 = time.time()
            rk_matches = rabin_karp(self.text_data, pattern)
            t_rk = time.time() - t1

            self.output.insert(tk.END, "► Rabin–Karp Search\n")
            self.output.insert(tk.END, f"Matches: {len(rk_matches)}\n")
            self.output.insert(tk.END, f"Time: {t_rk:.6f} s\n")
            self.output.insert(tk.END, f"Sample: {rk_matches[:50]}\n\n")

            # KMP
            t2 = time.time()
            kmp_matches = kmp_search(self.text_data, pattern)
            t_kmp = time.time() - t2

            self.output.insert(tk.END, "► KMP Search\n")
            self.output.insert(tk.END, f"Matches: {len(kmp_matches)}\n")
            self.output.insert(tk.END, f"Time: {t_kmp:.6f} s\n")
            self.output.insert(tk.END, f"Sample: {kmp_matches[:50]}\n\n")
