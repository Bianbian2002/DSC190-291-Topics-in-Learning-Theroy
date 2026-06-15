# Part C — AI Usage Report

**DSC 190/291 — Assignment 6**
**Student: Zeyu Bian**

## 1. Where I used AI

- **A.1 Hölder step.** I wrote the margin-inequality–take-expectation step myself,
  then asked AI to double-check that $\ell_1/\ell_\infty$ Hölder is exactly what's
  needed (and not $\ell_2/\ell_2$). AI confirmed and helped me write the bound in the
  cleanest form via $|\mathbb{E}_Q[y\varphi_j]|$ rather than the signed quantity.
- **A.3 hard construction.** This is the most AI-assisted part. The handout's hint
  describes three column families ("base / pair-flip / carry") and the weighted-sum
  constraint, but I wanted to be sure the carry-column construction actually gives
  $q$-weighted sum $1$ for *every* $p$. I wrote out the cases by hand on paper,
  then asked AI to verify the algebra. We caught one off-by-one in my initial
  carry column for $p=1$.
- **B.1 case split.** I had the "constant halfspace for small $p$, averaging for large $p$"
  outline from the hint. AI helped me find the right form of the inequality
  $\sum_i q_i\le(k-1)(1-p)$ via union bound on $\{h_i(x)=-1\}$ events, and then
  algebraically reduce $(k-1)(1-p)/k$ to $\le 1/2 - 1/(2k^2)$ for the boundary case.
- **A.4 experiment.** I wrote the AdaBoost loop and the data generators. AI suggested
  the right diagnostics to log (edge per round, support size, $\ell_1$-normalized
  margin), and helped track down a bug where I was computing the edge under the
  *uniform* sample distribution instead of the current $D$.

## 2. AI suggestions I accepted (and why)

- **"Take expectation of the margin inequality" framing for A.1.** AI suggested
  writing the proof as: (i) margin $\Rightarrow$ $\mathbb{E}_Q$ of the inner product
  $\ge 1$, (ii) Hölder. I accepted because this makes the
  $1\le\|w^\star\|_1\cdot\max_j|\mathbb{E}_Q[y\varphi_j]|$ identity a *one-line*
  derivation rather than a multi-step manipulation.
- **Edge formulation $L_D(b)=(1-\sum_i D_iy_ib(x_i))/2$.** AI proposed deriving the
  $O(nd)$ weak learner by reducing weighted error to a signed correlation, so the
  algorithm is "compute $c_j=\sum_i D_iy_i\varphi_j(x_i)$ for each $j$, return
  $b_{\arg\max|c_j|,\mathrm{sign}(c_j)}$." This is the cleanest expression of the
  weak learner.
- **$\|w^\star\|_1\ge Z$ argument in A.3.** Instead of trying to compute $\Phi^{-1}\mathbf{1}$
  in closed form, AI suggested using the A.1 contrapositive: best coordinate edge
  $\le 1/\|w^\star\|_1$ and best coordinate edge equals $1/Z$, so $\|w^\star\|_1\ge Z$.
  Then $\|w^\star\|_\infty\ge \|w^\star\|_1/s = 2^{\Omega(s)}$. Much cleaner than a
  direct matrix-inverse computation.
- **B.1 boundary algebra.** AI suggested writing
  $(k-1)(1-p)/k \le 1/2-1/(2k)+1/(2k^2)-1/(2k^3)$ and using $k\ge 2$ for the final
  step. I accepted; it makes the inequality verifiable line-by-line.
- **B.3 sample bound $\widetilde O(k^4 d/\varepsilon)$.** AI walked through the
  $T=O(k^4\log n)$ rounds × VC dim $\widetilde O(Td)$ × realizable rate $1/\varepsilon$
  composition. I verified each step.

## 3. AI suggestions I rejected or substantially modified

- **A.3: AI's first carry-column proposal.** AI initially gave a carry column with
  $\Phi_{(r,+),(p,-)}=+1$ for $r<p$ (which would give $\sum_{r<p}q_r\cdot 0=0$ instead
  of $-(2^p-2)$). I caught it by computing the weighted sum for $p=2$: the proposed
  column gave a sum of $-1+0+2^2 = 3\ne 1$. I rewrote the carry to use $(-,-)$ for
  $r<p$.
- **A.3: AI tried to invoke a Hadamard-style lower bound.** AI suggested skipping the
  explicit construction and quoting "any $\pm 1$ matrix with all column-sums equal to
  $1$ under exponential weights has a $2^{\Omega(s)}$ inverse." I rejected because
  the construction is part of the problem; the existence claim has to be made
  concrete.
- **B.1: AI's first attempt used $L_\mathcal{D}(h_i)\le (1-p)$ directly.** This is a
  trivial bound that doesn't beat $1/2$ when $p<1/2$. I corrected by introducing the
  union-bound step $\sum_i\Pr[y=-1,h_i=-1]\ge\Pr[y=-1]$ to get the factor $(k-1)/k$.
- **B.2: AI wanted $\varepsilon_0=1/(2k^2)$.** This would give the weak learner
  edge $0$ in the boundary case. I changed to $\varepsilon_0=1/(4k^2)$, giving edge
  $\gamma=1/(4k^2)>0$. The factor of $4$ matters: B.3's round count becomes
  $T=O(k^4\log n)$ instead of "undefined."
- **B.4: AI mixed up uSVP and RSAT regimes.** AI's first draft applied uSVP to
  $k=\omega(1)$ and RSAT to $k=d^r$. I corrected: uSVP gives hardness for
  polynomially-large $k=d^r$; RSAT gives hardness for any $\omega(1)$ size including
  sub-polynomial.

## 4. How I verified correctness

- **A.1.** Verified Hölder by considering the extremal case where all mass of $w^\star$
  concentrates on one coordinate ($w^\star=Be_{j^\star}$): then the coordinate
  predictor on that coordinate has edge $\ge 1/(\|w^\star\|_1)=1/B$, matching the bound.
- **A.2 round count.** Verified $T=O(s^2 B^2\log n)$ matches Schapire–Singer's
  $T=O(\log n/\gamma^2)$ with $\gamma=1/(2sB)$.
- **A.3 column-sum identity.** Verified in `experiment.py` line
  `assert np.allclose(sums, 1.0)` — the $7\times 7$ matrix actually does satisfy
  $\Phi^\top q=\mathbf{1}$ as constructed.
- **A.3 $\|w^\star\|_\infty$ size.** Computed by `np.linalg.solve(Phi, np.ones(s))`
  and confirmed $\|w^\star\|_\infty=9=2^{m}+1$, comfortably $2^{\Omega(s)}$ for $m=3$,
  matching the lower bound from A.1.
- **A.4.** Verified the AdaBoost loop on the easy distribution against a one-line
  sanity check: training error reaches $0$ in $O(\log n/\gamma^2)$ rounds, support
  matches the planted support, $\ell_1$-margin is close to the optimum $1/\|w^\star\|_1$.
- **B.1.** Verified the case split numerically for $k=2,3,4$: I computed
  $(k-1)/k\cdot(1/2+1/(2k^2))$ explicitly and confirmed it's $\le 1/2-1/(2k^2)$ in
  every case.
- **B.2/B.3 polynomial-time bookkeeping.** Wrote down the chain:
  $\varepsilon_0=1/(4k^2)\Rightarrow\gamma=1/(4k^2)\Rightarrow T=8k^4\ln n\Rightarrow$
  $\mathrm{VCdim}=\widetilde O(Td)=\widetilde O(k^4 d)\Rightarrow n=\widetilde O(k^4 d/\varepsilon)$.
  All polynomial in $d$ when $k\le d^c$.
- **B.4 contradiction direction.** Verified by contrapositive: hardness fact
  $+$ implication $\Rightarrow$ negation of "halfspaces are agnostically PAC learnable."

## AI workflow updates (5 most recent changes)

1. **"Compute the constants in case-split inequalities" rule.** Both A.3 (carry-column
   sum) and B.1 (the $(k-1)(1-p)/k\le 1/2-1/(2k^2)$ reduction) had off-by-one /
   sign-flip bugs from AI on the first try. I now require that any case-split inequality
   in a proof comes with an explicit numerical check at the boundary value
   ($p=1/2-1/(2k^2)$ here) before I write it down.
2. **"Use the contrapositive of part 1 rather than reproving" rule for A.3.** Rather
   than computing $\Phi^{-1}\mathbf{1}$ directly to bound $\|w^\star\|_\infty$, the
   cleaner argument is: A.1 says the best edge is $\le 1/\|w^\star\|_1$, and we
   constructed $\Phi$ so the best edge is $1/Z$, so $\|w^\star\|_1\ge Z$. I added a
   note to my workflow: "for tightness results, see if the upper-bound theorem can be
   contrapositive'd into a matching lower bound."
3. **"AdaBoost diagnostics" checklist.** Whenever I implement boosting, I now log a
   fixed five metrics per round: train 0-1 error, exponential loss, observed edge,
   support size, $\ell_1$-normalized margin. This caught the "edge computed under
   uniform $D$" bug in A.4: my first run had edge $\approx 0.4$ in every round, which
   is impossible on the hard distribution with $1/Z\approx 0.067$.
4. **"Distinguish weak / strong PAC learnability assumptions" prompt.** B.2/B.3 ask for
   the agnostic learner $\to$ realizable learner direction. I now ask AI explicitly to
   state which type of PAC learner is hypothesized and which is concluded, to avoid
   the easy slip "if X is realizable then Y is agnostic" (the directions matter).
5. **"Get the hardness regime right" check.** I now read out loud "uSVP gives X-size
   hardness; RSAT gives Y-size hardness" before applying either, since AI mixed them
   up in B.4's first draft. Reading conjectures out loud is a low-tech but effective
   defense against AI's overconfidence on cryptographic-assumption names.

I did not use AI to fabricate any reference; the standard AdaBoost training-error
analysis (Schapire–Freund), Hölder, and the boosted-class VC bound (Schapire et al.
1998) are all results I have read.
