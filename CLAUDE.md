# CLAUDE.md — DSC 190/291: Learning Theory

## Course Context

**Course:** DSC 190/291: Learning Theory through Formal Proof and Proof Presentation  
**Institution:** UCSD, Spring 2026  
**Student:** Zeyu Bian  
**AI Policy:** AI assistance is explicitly allowed and expected for coding, debugging, designing experiments, explaining concepts, and writing. Every submission must include a Part D AI usage report.

## How to Help

- Help with all parts of every assignment: theory proofs, Python implementation, experiment design, and writing.
- For theory problems, provide rigorous mathematical proofs with clear step-by-step reasoning. Use LaTeX-style math notation in markdown.
- For coding tasks, write clean Python. Assignments live in `hw<N>/` subdirectories.
- For experiments, help design clear plots and concise discussion connecting empirical results back to the theoretical bounds.

## Repository Structure

```
DSC190-291-Topics-in-Learning-Theroy/
├── CLAUDE.md          ← this file
├── READ.md
└── Assignment/
    ├── hw_1.pdf
    ├── hw1/           ← code, plots, and report for Assignment 1
    ├── hw_2.pdf       ← handout for Assignment 2
    └── hw2/           ← write-up, AI report, `build_pdfs.sh`, optional checks
```

## Assignment 1 (Due: April 10, 2026)

**Parts:**
- **A (10 pts):** Repo setup (done via this CLAUDE.md)
- **B (40 pts):** Theory — ∆-separated threshold-realizable sequences
  - B.1: Design grid G ⊆ [0,1], prove consistency, derive O(log(1/∆)) mistake bound via Halving
  - B.2: Feature map φ:[0,1]→ℝᵈ, show margin ≥ c∆, derive O(1/∆²) bound via Perceptron theorem
  - B.3: Compare and interpret the two bounds
  - B.4 (optional): Audit a flawed AI proof
- **C (35 pts):** Implement Perceptron in Python, run experiments on mistake bound vs γ, dimension independence, behavior as γ→0
- **D (15 pts):** AI usage report (~half page)

**Submission:** Single PDF on Gradescope + code pushed to GitHub repo.

**PDF build:** Run `./Assignment/hw1/build_pdfs.sh` to produce `theory.pdf`, `discussion.pdf`, `ai_report.pdf`, and one combined **`hw1_writeup.pdf`** (theory + discussion + AI report in that order).

## Assignment 2 (Due: April 17, 2026)

**Parts:**
- **A (40 pts):** Unions of two intervals on $\mathbb{R}$ — restriction patterns, exact growth $\Gamma_{\mathcal{H}_2}(n)$, VC dimension + Halving vs Sauer–Shelah, tightness example, AI audit.
- **B (45 pts):** Quadratic thresholds — embedding bound $\mathrm{VCdim}\le 3$, explicit $\varphi$, exact patterns/growth/VC, Sauer comparison, AI audit.
- **C (15 pts):** AI usage report (include workflow updates).

**Artifacts:** `Assignment/hw2/theory.md`, `ai_report.md`, `verify_patterns.py`, `build_pdfs.sh`. Run `./Assignment/hw2/build_pdfs.sh` to produce `theory.pdf`, `ai_report.pdf`, and combined `hw2_writeup.pdf`.

## Coding Conventions

- Python for all implementations
- Use `numpy` for numerical work, `matplotlib` for plots
- Keep code in `hw<N>/` with a self-contained script or notebook
- Plots should have labeled axes, titles, and legends

## Notes for Claude

- The student understands the material and wants rigorous, correct proofs — don't oversimplify.
- Always explain the key insight behind each proof step, not just the mechanics.
- When writing the AI usage report, be honest and specific about what AI contributed.
- Flag any step where the proof requires a non-trivial lemma so the student can verify they understand it.
