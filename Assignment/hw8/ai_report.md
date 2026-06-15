# Part D — AI Usage Report

**DSC 190/291 — Assignment 8**
**Student: Zeyu Bian**

## D.1 Where I used AI

This assignment is entirely theoretical (Parts A–C are proofs; there is no experiment or code component), so AI played the role of a *proof collaborator and LaTeX/exposition assistant*, not a code debugger. Concretely I used AI to:

- **Stress-test the proof skeleton** I had drafted on paper for A.1–A.4 (the validation oracle inequality and its adaptive-tuning consequence), checking that each "$\le$" was justified and that I had not silently swapped $n_T$ and $n_V$.
- **Check algebra** in the optimizations: the AM–GM balancing of $\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n_T}$ (A.3), the $c+1/c$ discretization constant, the $n_T=n_V=n/2$ simplification (A.4), the $\lambda$ choice in B.4/B.5, and the Cauchy–Schwarz step in C.3.
- **Improve exposition**, turning my margin notes into clean markdown with consistent notation.

## D.2 Suggestions I accepted

1. **The "expectation of the max" route for A.1.** I initially planned a high-probability bound (union bound + Hoeffding tail, then integrate). AI suggested going directly through the subgaussian maximal inequality $\mathbb E\max\le\sigma\sqrt{2\log(2K)}$ with $\sigma^2=1/(4n_V)$, which lands *exactly* on the target constant $2\sqrt{\log(2K)/(2n_V)}$ in expectation without a failure-probability term. I accepted it because it is both shorter and matches the stated bound's constant exactly; I verified $\sigma^2=1/(4n_V)$ from Hoeffding's lemma myself.

2. **Decoupling B.3 from the stability bound B.2.** My first attempt at B.3 bounded the generalization gap of $\tilde w_S$ using the B.2 stability constant directly, which produced an *extra* $2G\sqrt{2\eta/(\lambda\alpha)}$ term — too large to match the claim. AI pointed out the cleaner decomposition: bound $L_{\mathcal D}(\tilde w_S)\le L_{\mathcal D}(w_S)+G\|\tilde w_S-w_S\|$ using Lipschitzness of the *true* risk, then apply the exact-RERM bound to $w_S$. This gives exactly the single $G\sqrt{2\eta/(\lambda\alpha)}$ term. I accepted after re-deriving it.

## D.3 Suggestions I rejected or substantially modified

1. **Wrong strong-convexity constant.** AI at one point asserted that the regularized objective $F_S=L_S+\lambda\Psi$ is "$\alpha$-strongly convex." It is $\lambda\alpha$-strongly convex (the $\lambda$ multiplies $\Psi$). This matters in B.1: the correct bound is $\|\tilde w_S-w_S\|\le\sqrt{2\eta/(\lambda\alpha)}$, and dropping the $\lambda$ would have given the wrong dependence. I corrected it.

2. **Off-by-constant in B.5.** A draft treated the constraint $\|u\|_2\le B$ as $\Psi(u)\le B^2$, but $\Psi(u)=\tfrac12\|u\|_2^2\le\tfrac12B^2$. I redid the $\lambda$-optimization with the correct $\tfrac12B^2$, yielding $\lambda=\frac{2R}{B\sqrt n}$ and the leading term $\frac{2RB}{\sqrt n}$ (rather than an inflated constant).

3. **Over-claiming on the "price of tuning."** AI initially described the adaptivity cost as "$\sqrt{\log(B_{\max}/B_{\min})/n}$." That is the cost if $K\propto B_{\max}/B_{\min}$, but the dyadic grid has $K=O(\log(B_{\max}/B_{\min}))$, so the validation term is the *doubly*-logarithmic $\sqrt{\log\log(B_{\max}/B_{\min})/n}$. I corrected the write-up in A.4.

## D.4 How I verified correctness

Since the deliverables are proofs, verification was step-level:

- **Constant tracking.** For every boxed bound I checked that the target constant emerges, not just the rate: the $2\sqrt{\log(2K)/(2n_V)}$ in A.1, the $\frac52\sqrt2$ in A.3 (from $\max_{c\in[1/2,2]}(c+1/c)=5/2$), the collapse $\frac52\sqrt2\cdot\sqrt2=5$ in A.4, and $(2\sqrt2+1)$ in B.4.
- **Limit/sanity checks.** As $\eta\to0$, B.1–B.5 reduce to the exact-RERM statements; B.4's condition $\eta=O(n^{-3/2})$ is below the statistical $n^{-1/2}$ scale, as expected. In C.3, the optimal $q_j\propto r_j/b_j$ I verified by plugging back in to confirm both Cauchy–Schwarz factors equal $\sum_j b_jr_j$.
- **Independence bookkeeping.** The crux of A.2 is that $h_\lambda=A_\lambda(T)$ is independent of $V$ given $T$; I made sure the conditioning order (condition on $T$, apply A.1 over $V$, then $\mathbb E_T$) was airtight before trusting the oracle inequality.

## D.5 Updates to my AI workflow (5 most recent)

1. **Added a "constant audit" pass to my proof checklist.** After the B.3/B.5 constant slips, I now make a final pass that re-derives every boxed constant independently of the AI's text. *Why:* AI errors in these problems are almost always constant/factor errors, not structural ones.

2. **Added a "strong-convexity parameter" reminder to `CLAUDE.md`'s notes section.** A standing note: regularized objectives carry the $\lambda$ into the strong-convexity modulus ($\lambda\alpha$, not $\alpha$). *Why:* this exact mistake recurred and is easy to miss.

3. **Standardized the train/validation split notation prompt.** I now state $n_T,n_V$ (and which sample each quantity uses) explicitly in the prompt before asking for help. *Why:* AI mixed up $n_T$ and $n_V$ in an early A.2 draft.

4. **"Reduce to known limit" verification habit.** I added a step that checks every approximate/perturbed bound against its exact ($\eta\to0$) special case. *Why:* it instantly caught the spurious extra stability term in B.3.

5. **Kept the `build_pdfs.sh` pandoc pipeline from HW7** unchanged (theory + ai_report → combined `hw8_writeup.pdf`), since it has been reliable. *Why:* a stable, scripted build removes a class of last-minute formatting errors before submission.

I used AI for proof-checking, algebra verification, and exposition only; the proof strategies and all final corrections are my own.
