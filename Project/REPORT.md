# Formalizing the Sauer–Shelah Lemma in Lean 4

**Author:** Zeyu Bian · DSC 190/291, Learning Theory · Spring 2026
**Artifact:** `Project/Project/SauerShelah.lean` (237 lines, builds against mathlib, no `sorry`).

This report has three parts, in the order we approach the theorem formalization:

1. **The proof on paper** — a precise, self-contained natural-language proof.
2. **The formalization** — how each step of the paper proof becomes Lean code *from scratch*
   (we do not invoke mathlib's Sauer–Shelah results).
3. **Verification** — how a human (or machine) confirms the Lean artifact really proves the
   claimed theorem and nothing weaker.
---

## 0. Statement

Let $X$ be a finite ground set with $|X| = n$. A **concept class** is a family
$\mathcal{A} \subseteq 2^{X}$ of subsets of $X$ (each concept identified with the set of
points it labels $1$).

For $S \subseteq X$, we say $\mathcal{A}$ **shatters** $S$ if every subset $U \subseteq S$ is
realized as a trace:
$$\mathcal{A} \text{ shatters } S \quad:\Longleftrightarrow\quad \forall\, U \subseteq S,\ \exists\, A \in \mathcal{A},\ A \cap S = U .$$
Equivalently, the $2^{|S|}$ possible labelings of $S$ all occur among members of $\mathcal{A}$.

The **VC dimension** of $\mathcal{A}$ is the size of the largest shattered set,
$d = \mathrm{VCdim}(\mathcal{A}) = \max\{\,|S| : \mathcal{A}\text{ shatters }S\,\}$.

We aim to formalize the following lemma in Lean4.

> **Sauer–Shelah Lemma.** $\displaystyle |\mathcal{A}| \;\le\; \sum_{k=0}^{d} \binom{n}{k}.$

---

## 1. The proof on paper

The proof factors into two independent inequalities:
$$|\mathcal{A}| \;\overset{(\mathrm{I})}{\le}\; \#\{\text{sets shattered by } \mathcal{A}\} \;\overset{(\mathrm{II})}{\le}\; \sum_{k=0}^{d}\binom{n}{k}.$$
Write $\mathrm{Tr}(\mathcal{A}) = \{S \subseteq X : \mathcal{A}\text{ shatters }S\}$ for the set of
shattered sets (the "trace family").

### (I) Pajor's lemma: $|\mathcal{A}| \le |\mathrm{Tr}(\mathcal{A})|$

*A family shatters at least as many sets as it has members.* Proof by induction on the ground
set $X$.

**Base case $X = \varnothing$.** Every member of $\mathcal{A}$ is $\subseteq \varnothing$, so
$\mathcal{A} \subseteq \{\varnothing\}$, giving $|\mathcal{A}| \in \{0,1\}$. If
$\mathcal{A} = \varnothing$ then $0 \le |\mathrm{Tr}|$ trivially. If
$\mathcal{A} = \{\varnothing\}$ then $\mathcal{A}$ shatters $\varnothing$ (the only subset of
$\varnothing$ is $\varnothing = \varnothing \cap \varnothing$), so $|\mathrm{Tr}| \ge 1$. Either
way $|\mathcal{A}| \le |\mathrm{Tr}(\mathcal{A})|$.

**Inductive step $X = X' \sqcup \{a\}$** (with $a \notin X'$). Split and project on $a$. Define
three families over the smaller ground set $X'$:

- $\mathcal{A}_a = \{A \in \mathcal{A} : a \in A\}$, the members containing $a$;
- $M = \{A \setminus \{a\} : A \in \mathcal{A}_a\}$, those members with $a$ deleted;
- $\mathcal{A}_{\bar a} = \{A \in \mathcal{A} : a \notin A\}$, the members avoiding $a$.

Set $P = M \cup \mathcal{A}_{\bar a}$ and $Q = M \cap \mathcal{A}_{\bar a}$. All of
$P, Q$ are families of subsets of $X'$.

**Counting identity $|\mathcal{A}| = |P| + |Q|$.** Deleting $a$ is injective on $\mathcal{A}_a$
(each such $A$ equals $\{a\}\cup(A\setminus\{a\})$), so $|M| = |\mathcal{A}_a|$. Splitting
$\mathcal{A}$ by whether $a$ is present gives
$|\mathcal{A}| = |\mathcal{A}_a| + |\mathcal{A}_{\bar a}| = |M| + |\mathcal{A}_{\bar a}|$.
Inclusion–exclusion on $M, \mathcal{A}_{\bar a}$ gives
$|P| + |Q| = |M \cup \mathcal{A}_{\bar a}| + |M \cap \mathcal{A}_{\bar a}| = |M| + |\mathcal{A}_{\bar a}|$.
Hence $|\mathcal{A}| = |P| + |Q|$. *(Combinatorially: a set $B \subseteq X'$ is counted once in
$P$ if exactly one of $B,\ \{a\}\cup B$ lies in $\mathcal{A}$, and once more in $Q$ if both do —
exactly matching how the two preimages $B$ and $\{a\}\cup B$ contribute to $|\mathcal{A}|$.)*

**Transferring shattered sets.** Two claims relate traces over $X'$ to traces over $X$:

- **(A)** If $P$ shatters $S \subseteq X'$, then $\mathcal{A}$ shatters $S$.
  *Reason:* given $U \subseteq S$, $P$ supplies $B$ with $B \cap S = U$. If $B \in
  \mathcal{A}_{\bar a}\subseteq\mathcal{A}$, take $A = B$. If $B \in M$, then $\{a\}\cup B \in
  \mathcal{A}$ and, since $a \notin S$, $(\{a\}\cup B) \cap S = B \cap S = U$.
- **(B)** If $Q$ shatters $S \subseteq X'$, then $\mathcal{A}$ shatters $\{a\}\cup S$.
  *Reason:* take $U \subseteq \{a\}\cup S$.
  *If $a \notin U$:* $U \subseteq S$; $Q\subseteq\mathcal{A}_{\bar a}$ gives $B \in \mathcal{A}$,
  $a\notin B$, $B\cap S = U$, and then $B \cap (\{a\}\cup S) = B\cap S = U$.
  *If $a \in U$:* let $U' = U\setminus\{a\}\subseteq S$; $Q$ gives $B$ with $B\cap S = U'$ and,
  since $B\in M$, $\{a\}\cup B \in \mathcal{A}$; then
  $(\{a\}\cup B)\cap(\{a\}\cup S) = \{a\}\cup(B\cap S) = \{a\}\cup U' = U$.

**Putting it together.** By (A), $\mathrm{Tr}_{X'}(P) \subseteq \mathrm{Tr}_X(\mathcal{A})$. By
(B), $\{\,\{a\}\cup S : S \in \mathrm{Tr}_{X'}(Q)\,\} \subseteq \mathrm{Tr}_X(\mathcal{A})$. The
first collection consists of sets avoiding $a$; the second of sets containing $a$ — so they are
**disjoint**, and $S \mapsto \{a\}\cup S$ is injective on $\mathrm{Tr}_{X'}(Q)$ (those sets avoid
$a$). Therefore
$$|\mathrm{Tr}_X(\mathcal{A})| \ge |\mathrm{Tr}_{X'}(P)| + |\mathrm{Tr}_{X'}(Q)| \overset{\text{IH}}{\ge} |P| + |Q| = |\mathcal{A}|. \qquad\blacksquare$$

### (II) Counting: $|\mathrm{Tr}(\mathcal{A})| \le \sum_{k=0}^{d}\binom{n}{k}$

Every shattered set $S$ has $|S| \le d$ by definition of $d$, and $S \subseteq X$. Thus
$\mathrm{Tr}(\mathcal{A})$ is contained in the family of subsets of $X$ of size at most $d$, of
which there are exactly $\sum_{k=0}^{d}\binom{n}{k}$. Monotonicity of cardinality finishes it.

Combining (I) and (II) gives the lemma. $\blacksquare$

---

## 2. The formalization (from scratch)

File: `Project/Project/SauerShelah.lean`, namespace `SauerShelah`. Ground type `α` with
`[DecidableEq α]`; the ground set is an explicit `X : Finset α` (this is what makes induction on
$X$ possible — mathlib's `shatterer` is ground-set-free and is *not* used).

### Definitions (mirroring §0)

```lean
def Shatters (F : Finset (Finset α)) (T : Finset α) : Prop :=
  ∀ U ⊆ T, ∃ A ∈ F, A ∩ T = U                       -- "F shatters T"

def traces (X : Finset α) (F : Finset (Finset α)) : Finset (Finset α) :=
  X.powerset.filter (Shatters F)                     -- Tr_X(F), as a Finset

def vcDim (𝒜 : Finset (Finset α)) : ℕ := (traces univ 𝒜).sup Finset.card   -- d
```

`Shatters` is given a `DecidablePred` instance (quantifying `U` over `T.powerset`) so that
`traces` can be a `Finset` via `filter`. `mem_traces` unfolds membership to
`S ⊆ X ∧ Shatters F S`.

### Mapping paper → Lean

| Paper step | Lean name / tactic |
|---|---|
| (I) Pajor's lemma | `theorem pajor`, `induction X using Finset.induction` |
| Base case bookkeeping | `Finset.subset_singleton_iff`, explicit `traces ∅ {∅} = {∅}` |
| $\mathcal{A}_a,\ \mathcal{A}_{\bar a},\ M,\ P,\ Q$ | `set Fa, Fn, M, P, Q with …` |
| $|M| = |\mathcal{A}_a|$ (delete-$a$ injective) | `card_image_of_injOn` + `insert_erase` |
| $|\mathcal{A}| = |M|+|\mathcal{A}_{\bar a}|$ | `card_filter_add_card_filter_not` |
| $|\mathcal{A}| = |P|+|Q|$ | `card_union_add_card_inter` |
| Claim (A) | `claimA`, using `insert_inter_of_notMem` |
| Claim (B) | `claimB`, cases on `a ∈ U`, `insert_inter_of_mem` / `inter_insert_of_notMem`, `insert_erase` |
| disjoint + injective glue | `disjoint_left`, `card_image_of_injOn`, `card_union_of_disjoint` |
| final chain | a `calc` ending in `card_le_card (union_subset claimA claimB)` |
| (II) counting | `card_traces_le_sum`: `card_le_card` into `(Iic d).biUnion (powersetCard · univ)`, then `card_biUnion_le`, `card_powersetCard` |
| $\sum_{k\le d}$ vs `range (d+1)` | `Nat.range_succ_eq_Iic` |
| final theorem | `card_le_sum_choose := (pajor univ 𝒜 …).trans (card_traces_le_sum 𝒜)` |

The Lean proof is a *faithful transcription*: every `have` in `pajor` corresponds to a sentence
in §1, and the file's comments name the mathematical fact at each step. Only general-purpose
`Finset`/`powersetCard` lemmas are used — **no** `Finset.shatterer`,
`card_le_card_shatterer`, or `card_shatterer_le_sum_vcDim`.


## 3. Verification — convincing a human (and the kernel)

A proof that *compiles* can still be the wrong theorem. The following checks, all reproducible,
establish that the artifact proves exactly the Sauer–Shelah lemma of §0. Build first:

```bash
cd Project
lake exe cache get      # fetch mathlib (first time only)
lake build              # compiles SauerShelah.lean; the kernel checks every proof
```

**V1 — Read the statement.** The conclusion of `card_le_sum_choose` is literally
`𝒜.card ≤ ∑ k ∈ Finset.range (vcDim 𝒜 + 1), (Fintype.card α).choose k`, i.e.
$|\mathcal{A}| \le \sum_{k=0}^{d}\binom{n}{k}$. There is **no extra hypothesis** on `𝒜`: it
holds for *every* finite class, so the statement cannot be vacuously true.

**V2 — The definitions are the intended ones.** `Shatters F T` is *verbatim*
$\forall U \subseteq T,\ \exists A \in F,\ A \cap T = U$ (the §0 definition), and `vcDim` is the
`sup` of cardinalities of shattered sets — the largest shattered set. Nothing is hidden behind a
nonstandard definition. A grader compares these three `def`s against §0 directly.

**V3 — No cheats.** No `sorry`/`admit` appears:
```bash
grep -rn 'sorry\|admit' Project/Project/      # empty
```
and the kernel-level axiom trace of the main theorem is the standard mathlib base only:
```lean
#print axioms SauerShelah.card_le_sum_choose
-- 'SauerShelah.card_le_sum_choose' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `sorryAx`, no stray `axiom`, no `Lean.ofReduceBool` (so the theorem does **not** lean on
`native_decide`). This line is printed on every build.

**V4 — Non-vacuous, tight test instances** (these `example`s are checked by the compiler):
- Empty class `∅` over `Fin 5`: the bound applies (degenerate `0 ≤ …`).
- Full powerset over `Fin 4`: `vcDim = 4` is confirmed by computation
  (`example : vcDim ((univ : Finset (Fin 4)).powerset) = 4 := by native_decide`), catching any
  `vcDim` that silently computes the wrong number. Here the bound is
  $2^4 = 16 \le \sum_{k=0}^{4}\binom{4}{k} = 16$ — **equality**, so the lemma is tight and the
  inequality is not slack-by-construction.

**V5 — Independence.** A reviewer can confirm the reproof claim mechanically: the file never
imports mathlib's Sauer–Shelah / compression modules, so it *cannot* be silently leaning on
them. (The strings `card_le_card_shatterer` etc. appear only in the header comment that states
this very fact.)
```bash
grep -n '^import' Project/Project/SauerShelah.lean
# → Finset.Powerset, Fintype.Powerset, Interval.Finset.Nat, BigOperators only;
#   no Combinatorics.SetFamily.Shatter and no .Compression.Down
```

Passing V1–V5 means: the right statement (V1–V2), genuinely proved (V3), neither vacuous nor
loose (V4), and from scratch (V5).

---

## Files

```
Project/
├── REPORT.md                  ← this document
├── CLAUDE.md                  ← project guidance (proof presentation + validation policy)
├── lean-toolchain             ← Lean v4.30.0
├── lakefile.toml              ← mathlib v4.30.0 dependency
├── Project.lean               ← root import
└── Project/SauerShelah.lean   ← definitions, Pajor induction, counting, theorem, tests
```
