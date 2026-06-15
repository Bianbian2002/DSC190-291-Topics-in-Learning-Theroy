# CLAUDE.md — Lean Formalization: Sauer–Shelah Lemma

## Goal

Formalize and **machine-check** the Sauer–Shelah lemma in Lean 4 (with mathlib), and
deliver a proof that is (a) complete (no `sorry`/`axiom` cheats) and (b) demonstrably the
statement we actually mean. This subproject lives entirely under `Project/`.

**The mathematical target.** For a finite ground set `α` and a concept class
`𝒜 : Finset (Finset α)` with VC dimension `d`,
```
|𝒜| ≤ Σ_{i=0}^{d} C(n, i),   where n = |α|.
```
Each concept is identified with the subset of points it labels `1`. `d` = size of the
largest set *shattered* by `𝒜`.

## Project Layout

```
Project/
├── CLAUDE.md            ← this file
├── lean-toolchain       ← pins Lean (leanprover/lean4:v4.30.0)
├── lakefile.toml        ← requires mathlib @ matching tag
├── Project.lean         ← root; imports all modules
└── Project/
    └── SauerShelah.lean ← the statement + proof
```

## Toolchain & Build

- Lean is installed via `elan`; toolchain is pinned in `lean-toolchain`.
- **The Lean version in `lean-toolchain` MUST match the mathlib `rev` in `lakefile.toml`.**
  A mismatch is the #1 cause of a broken build. If you bump one, bump the other.
- First-time setup (downloads prebuilt mathlib, ~minutes, do NOT compile mathlib from source):
  ```bash
  cd Project
  lake exe cache get      # fetch mathlib oleans — REQUIRED, never skip
  lake build              # builds our code against cached mathlib
  ```
- If `cache get` reports misses / `lake build` starts compiling mathlib itself, **stop**:
  the toolchain and the mathlib tag are out of sync. Fix the pin instead of waiting hours.

## Reuse Before Reprove (check mathlib FIRST)

Mathlib already has a Sauer–Shelah development in
`Mathlib/Combinatorics/SetFamily/Shatter.lean`. Before writing any proof:

1. Locate the installed source and read it:
   ```bash
   find Project/.lake/packages/mathlib -name 'Shatter.lean'
   grep -rn 'Shatter\|shatterer\|vcDim\|SauerShelah' Project/.lake/packages/mathlib/Mathlib/Combinatorics/SetFamily/
   ```
2. Confirm the real names/signatures with `#check` in the file (e.g. `Finset.Shatters`,
   `Finset.shatterer`, `Finset.card_le_card_shatterer`). **Names in `SauerShelah.lean`
   marked `-- VERIFY` are from memory and may be wrong — never trust a lemma name you have
   not `#check`ed against the installed mathlib.**
3. Decide and record (in a comment at the top of `SauerShelah.lean`) which path we take:
   - **(A) Wrap**: if mathlib already proves the exact bound, our job is to state *our*
     `card_le_sum_choose` and derive it in a few lines from the library lemma. The value is
     the precise statement + the bridge, not re-deriving the combinatorics.
   - **(B) Reprove**: if mathlib only has pieces (shatterer, `card_le_card_shatterer`) but
     not the binomial-sum bound, build the missing step (the classic
     shifting / down-compression argument bounding `|shatterer|`).
   Pick (A) if available; only do (B) for the genuinely missing part.

**CURRENT STATE: Path (B), fully self-contained.** `SauerShelah.lean` does NOT cite
mathlib's `card_le_card_shatterer` or `card_shatterer_le_sum_vcDim`. It defines its own
`Shatters`/`traces`/`vcDim` over an explicit ground `Finset` and proves the lemma from
scratch via **Pajor's double-counting induction on the ground set** (`SauerShelah.pajor`),
plus an elementary counting bound (`SauerShelah.card_traces_le_sum`). Only general-purpose
`Finset`/`powersetCard` lemmas are used. The wrapper proof of Path (A) is kept in the git
history / can be restored if a short version is ever wanted for comparison.

The proof skeleton (keep these names in sync with the file):
* `mem_traces`              — unfolds `S ∈ traces X F`
* `pajor`                   — `#F ≤ #(traces X F)`, induction on the ground set `X`
* `card_traces_le_sum`      — `#(traces univ 𝒜) ≤ ∑_{k≤d} C(n,k)`, pure counting
* `card_le_sum_choose`      — the course-form theorem, `pajor.trans card_traces_le_sum`

## How to Present the Proof

Write for a human reader who knows learning theory but not Lean. The file is the artifact.

- **State the theorem in the form the course uses** (`|𝒜| ≤ Σ C(n,i)`), not only in
  mathlib's internal `shatterer`-cardinality form. The grader must recognize Sauer–Shelah
  on sight without decoding library internals.
- **Top-of-file docstring**: plain-English statement, the meaning of every symbol
  (`𝒜`, shatter, VC dim, `n`, `d`), and which path (A/B) we took and why.
- **Definitions must be faithful.** `Shatters s` must mean *all* `2^{|s|}` labelings are
  realized (`∀ t ⊆ s, ∃ u ∈ 𝒜, s ∩ u = t`). VC dim = `sup` of cards of shattered sets.
  A wrong definition makes a `sorry`-free proof worthless — see Validation.
- **Structure the proof in named, commented steps** mirroring the math: (1) `|𝒜| ≤
  |shatterer 𝒜|`; (2) every member of `shatterer 𝒜` has card `≤ d`; (3) count sets of
  card `≤ d` in an `n`-set `= Σ_{i≤d} C(n,i)`. One `have` per step, each with a one-line
  comment saying *what* it establishes and *why*.
- **Flag every non-trivial lemma** (e.g. the down-shift / compression lemma, or
  `card_powersetCard`-style counting) with a comment naming the mathematical fact, so the
  student can confirm they understand it — not just that Lean accepted it.
- Prefer readable structured tactics (`have`, `calc`, `refine`) over an opaque
  `simp`/`omega`/`aesop` one-liner for the main steps. Automation is fine for arithmetic
  side-goals; the skeleton of the argument should be legible.

## Validation — "is it indeed what we need?"

A green checkmark is necessary, not sufficient. A proof can compile and still prove the
wrong (or a vacuous) thing. Run ALL of these before declaring done:

1. **No cheats.** The build must have zero `sorry`. Verify mechanically:
   ```bash
   grep -rn 'sorry\|admit' Project/Project/        # must be empty
   lake build 2>&1 | grep -i 'sorry\|warning'      # no sorry warnings
   ```
2. **No hidden axioms / no fake hypotheses.** After the theorem:
   ```lean
   #print axioms SauerShelah.card_le_sum_choose
   ```
   Expect only the standard `[propext, Classical.choice, Quot.sound]`. Anything else (a
   stray `axiom`, an `Inhabited` smuggling, etc.) is a red flag. Also confirm the theorem
   has **no unused/false hypothesis** that would make it vacuously true — it should hold for
   *every* `𝒜`, including `𝒜 = ∅`, the full powerset, and singletons.
3. **The statement is the real one.** Sanity-check with concrete instances so the
   inequality is non-vacuous and tight where expected:
   - `𝒜 = ∅`  → bound holds trivially (`0 ≤ …`).
   - `𝒜 = univ.powerset` over `Fin n` → `d = n` and bound becomes `2^n ≤ Σ_{i≤n} C(n,i) = 2^n` (equality). Add this as a `example`/`#eval`-checked corollary.
   - A class with `d = 1` on `Fin n` → bound is `≤ 1 + n`. Confirm the definition of `vcDim`
     returns `1`, not `0` or `n`, on such a class (`#eval` / `decide`).
   These instance checks are what catch a definition that compiles but means the wrong thing.
4. **Definitions match mathlib's intent.** If we reuse `Finset.shatterer`, prove (or cite)
   the unfolding lemma showing our `vcDim`/shatter agrees with `∀ t ⊆ s, ∃ u ∈ 𝒜, s ∩ u = t`.
   Don't assume — `#check` and unfold it once in a comment.
5. **It builds from clean.** `rm -rf Project/.lake/build/lib/Project && lake build` succeeds.

Treat 1–5 as a checklist to paste into the final report. "It compiles" alone is not a result.

## Workflow for Claude

- Use the IDE diagnostics / `lake build` after each meaningful edit; fix errors before
  adding new content. Don't accumulate many broken `have`s.
- When stuck on a lemma name, `grep` the installed mathlib and `#check` — do not guess.
- Keep `sorry` only as a temporary scaffold while building; track remaining ones and remove
  them all before any "done" claim. A file with `sorry` is incomplete, full stop.
- Match mathlib style: `Finset` API, `open Finset`, namespaced theorems, docstrings on
  every public declaration.
- This is coursework: explain the *insight* of each step, flag every non-trivial lemma, and
  be honest in the eventual AI-usage report about what the assistant contributed.
```
