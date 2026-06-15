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
