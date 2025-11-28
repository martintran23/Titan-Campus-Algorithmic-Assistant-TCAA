# Titan Campus Algorithmic Assistant (TCAA)
CPSC 335 – Algorithm Engineering
Instructor: Dr. Shah

## 📌 Overview
The Titan Campus Algorithmic Assistant (TCAA) is a fully interactive Python GUI application that demonstrates algorithm engineering concepts learned throughout CPSC 335. The application includes modules for graph algorithms, greedy scheduling, dynamic programming, string-pattern matching, and algorithm analysis.

This project serves as the final assignment for the course and integrates both theoretical and practical algorithmic design.

---

## ✅ Features / Modules

### 1. **Campus Navigator (Graphs)**
Implements:
- Breadth-First Search (BFS)
- Depth-First Search (DFS) + connectivity check
- Dijkstra’s shortest path (heap-based)
- Prim’s Minimum Spanning Tree (MST)

Users can:
- Select start and end buildings
- View paths, distances, traversal orders, and MST edges

---

### 2. **Study Planner (Greedy + Dynamic Programming)**
Implements:
- Greedy Task Scheduling (value/time priority)
- Optimal Task Selection using 0/1 Knapsack (Dynamic Programming)

Users can:
- Add tasks (name, duration, value)
- Enter available time
- Compare Greedy vs DP results

---

### 3. **Notes Search Engine (String Matching)**
Supports:
- Naive search
- Rabin-Karp
- Knuth-Morris-Pratt (KMP)
- Algorithm comparison mode

Users can upload:
- PDF files
- DOCX files
- TXT files

Outputs:
- Match indices
- Timing comparison
- Algorithm performance differences

---

### 4. **Algorithm Info / About Tab**
Includes:
- Time complexities (Big-O)
- Explanation of P vs NP
- Algorithm summaries

---

## 🛠️ Technologies Used
- **Python 3.x**
- **Tkinter** (GUI)
- **PyPDF2** (PDF parsing)
- **python-docx** (DOCX parsing)
- Standard libraries: `heapq`, `collections`, `time`, `math`

*No external algorithm libraries (NetworkX, Pandas, etc.) were used.*
