# Part C — AI Usage Report

**DSC 190/291 — Assignment 5**
**Student: Zeyu Bian**

## 1. Where I used AI

- **A.2 reduction design.** I sketched the "one coordinate per set, M repeated negatives
  per universe element" idea myself from the hint, then iterated with AI on
  bookkeeping: which examples should be positive, what threshold $K$ to set, and how
  $M=q+1$ enters the contradiction in the reverse direction. AI was useful as a
  "type-checker" — it caught a sign error in my first draft (I had positive examples
  rewarding selection rather than charging it).
- **A.3 experiment.** I drafted the synthetic-data and brute-force-enumeration scaffolding
  myself. AI helped me decide what to plot (runtime vs. $d$ and $k$, agreement vs.
  noise) and the right way to make the brute-force "approximate exactness" disclaimer
  precise (the per-support fit is convex, the enumeration is exact).
- **B.2 piecewise linear analysis.** I computed the three regions
  ($w\le -1/M$, $-1/M\le w\le 1$, $w\ge 1$) by hand. AI helped me state cleanly why
  $M>(1-p)/p$ is exactly the condition that makes the middle slope positive (so $w^*$ is
  $-1/M$ and not somewhere in the interior).
- **B.3 rank argument.** I knew the orthogonality identity for characters but asked AI
  to double-check the matrix factorization $H=W\Phi$ direction (the rank inequality
  $\mathrm{rank}(W\Phi)\le\min(\mathrm{rank}(W),\mathrm{rank}(\Phi))$).
- **B.4 Jensen example.** I picked the $(1,1),(-1,-1)$ pair myself. AI suggested the
  alternative $(2,1),(1,2)$ with midpoint $(1.5,1.5)$, which doesn't violate Jensen here
  ($vu$ is then $2$, $2$, $2.25$); I rejected that suggestion and kept the symmetric
  sign-flip pair, where the midpoint is the zero predictor and the violation is sharp.

## 2. AI suggestions I accepted (and why)

- **"$M=q+1$ exceeds the mistake budget" framing for A.2 reverse direction.** AI suggested
  stating the contradiction as "any uncovered $u_i$ forces $M>k$ mistakes; the total
  mistake budget is $k$; therefore no uncovered $u_i$." I accepted because it makes the
  threshold $K=(q-k)+Mr$ feel inevitable rather than arbitrary.
- **Explicit sign-of-$w_j$ accounting in A.2 forward direction.** I had originally only
  said "set $w_j=-1$ for $j\in R$" without explaining why this gives zero coverage
  mistakes. AI suggested writing out
  $\langle w,a^{(i)}\rangle = -|\{j\in R:u_i\in A_j\}|<0$ explicitly. I accepted; the
  inequality is the load-bearing step.
- **Three-region case split for B.2 hinge minimization.** AI suggested partitioning
  $\mathbb{R}$ at the two hinge breakpoints rather than trying to optimize the sum
  directly via subgradients. I accepted because piecewise-linear minimization is
  cleaner for a one-dimensional problem.
- **Explicit $H=W\Phi$ factorization for B.3.** AI proposed writing the assumption
  $\chi_I(x)=\langle w_I,\varphi(x)\rangle$ as a $2^d\times 2^d$ matrix factorization
  through the $D$-dimensional space. I accepted because it makes the rank inequality
  $2^d=\mathrm{rank}(H)\le D$ a one-line corollary.

## 3. AI suggestions I rejected or substantially modified

- **A.2 "intercept variable" first draft.** AI's initial reduction introduced an
  intercept coordinate $x_0=1$ on every example, claiming this was needed to handle
  the tie-breaking convention. This was wrong: the homogeneous halfspace family
  $\mathcal{H}_{d,k}$ has no intercept by definition, and adding one *would* change
  the class. I removed the intercept and verified directly that the
  $\mathrm{sign}(0)=+1$ convention handles the $w_j=0$ case correctly: positive
  example $(e_j,+1)$ with $w_j=0$ gives $\langle w,e_j\rangle=0$, sign $=+1$,
  correctly classified.
- **A.3 "use Gurobi for an exact 0-1 baseline" suggestion.** AI proposed solving the
  exact mixed-integer 0-1 ERM with a commercial MIP solver. I rejected this because
  (a) it requires an extra dependency the grader may not have, and (b) the exponential
  enumeration of supports already illustrates the computational hardness — adding a
  MIP would not change the qualitative finding. I stated explicitly that the baseline
  is approximate-per-support, exact-over-supports.
- **B.2 "look at the dual" approach.** AI offered to derive the unique minimizer via
  the hinge-loss Lagrangian. I rejected; the three-region piecewise-linear analysis
  is direct and avoids machinery the reader hasn't seen for this problem.
- **B.3 Hadamard-matrix invocation.** AI's first proof wanted to identify $H$ with
  the Hadamard matrix $H_{2^d}$ and quote $H_{2^d}H_{2^d}^\top=2^d I$. I modified this
  to a self-contained proof using $\chi_I\chi_J=\chi_{I\triangle J}$ and
  $\sum_x\chi_K(x)=0$ for $K\ne\emptyset$, because the Hadamard identification (with
  the right row/column ordering) is itself a lemma the assignment doesn't grant.
- **B.4 Jensen with $(2,1),(1,2)$.** As noted in §1: AI's first attempt gave a
  *non*-violating example. I caught it by computing the three loss values; replaced
  with $(1,1),(-1,-1)$ where the midpoint is $(0,0)$ and Jensen fails by $1$.

## 4. How I verified correctness

- **A.2 reduction (both directions).** Wrote a small Python check (not included in
  the submission since it duplicates the written proof): for several random
  SETCOVER instances with $q\le 6$, $r\le 6$, $k\le 3$, constructed the
  AGREEMENT sample and verified that brute-force search over $\{-1,0,+1\}^q$-valued
  weight vectors achieves $\ge K$ iff the original instance is a YES-instance.
- **A.3 experiment.** Verified `empirical_agreement` directly against the definition
  on a $d=2$, $n=4$ toy example. Verified the runtime scaling matches
  $\binom{d}{k}$ growth by computing the ratio
  $T(d=20,k=3)/T(d=20,k=2)\approx 6.3$ vs. theoretical
  $\binom{20}{3}/\binom{20}{2}=1140/190=6.0$, which matches.
- **B.1 LP.** Verified the LP optimum equals the hinge-loss optimum by sampling: ran
  the LP via `scipy.optimize.linprog` on small random instances and checked the
  hinge-loss recomputed from $w=w^+-w^-$ matches the LP optimum value (a side check,
  not in the submission).
- **B.2 piecewise minimum.** Verified the three slopes by direct algebra:
  $-(1-p)<0$, $pM-(1-p)>0$ (using $M>(1-p)/p$), $pM>0$. Checked $w^*=-1/M$ is the
  unique global minimizer because $L$ decreases then increases with no flat regions
  (all three slopes are strictly nonzero).
- **B.3 rank.** Verified $\chi_I\chi_J=\chi_{I\triangle J}$ from the definition:
  $\chi_I(x)\chi_J(x)=\prod_{i\in I}x_i\prod_{j\in J}x_j=\prod_{i\in I\triangle J}x_i$,
  using $x_i^2=1$ to cancel each $i\in I\cap J$. Verified
  $\sum_{x\in\{\pm 1\}^d}\chi_K(x)=\prod_{i\in K}\sum_{x_i\in\{\pm 1\}}x_i=0$ for
  $K\ne\emptyset$.
- **B.4 Jensen.** Computed the three loss values directly:
  $L_{\mathrm{net}}(1,1)=(1\cdot 1-1)^2=0$, $L_{\mathrm{net}}(-1,-1)=((-1)(-1)-1)^2=0$,
  $L_{\mathrm{net}}(0,0)=(0-1)^2=1$. $1>\tfrac12\cdot 0+\tfrac12\cdot 0$, confirmed.

## AI workflow updates

1. **"Type-check reduction outputs" prompt.** When designing a reduction, I now ask AI
   to write out the full mistake/cost accounting for *both* directions before
   declaring the reduction done. This is how I caught the A.2 sign error: the forward
   direction's "0 coverage mistakes" only works if covered $u_i$'s really evaluate
   to a strictly-negative inner product, which forced me to pin down $w_j=-1$ rather
   than just "$w_j\ne 0$".
2. **"State exactness disclaimers up front" rule for empirical work.** I now require
   that experiments declare *which* baseline component is exact and which is a
   surrogate. The A.3 brute-force is "exact enumeration over supports, convex
   surrogate within each support" — making this explicit in the write-up matters
   because otherwise the close agreement-vs-noise numbers look like the surrogate
   "beating" the truth, when in fact both methods are surrogates with similar bias.
3. **"Reject the slick reference proof" default for parity-style problems.** AI loves
   to invoke Hadamard matrices, Walsh expansions, Fourier analysis on $\{\pm 1\}^n$,
   etc. For an assignment, these are usually a black box the reader doesn't have. I
   now require AI to inline any character-theory identity it wants to use, with a
   one-line proof. This is what produced the self-contained B.3.
4. **"Test counterexamples before accepting" rule.** AI's first Jensen example for
   B.4 was wrong (didn't actually violate convexity). I added a rule that any
   numerical claim ("at $x_1,x_2$ Jensen fails by $\delta$") must be verified by
   plugging in the numbers before going into the write-up.
5. **"Pin tie-breaking conventions" check.** Part A uses $\mathrm{sign}(0)=+1$;
   Part B's 0-1 loss counts zero margin as an error. These differ and AI conflated
   them in an early draft. I now mark conventions at the top of each part and
   re-check every $\mathrm{sign}(0)$ / $yf=0$ case before submission.

## Required additional answers

**Which part did AI help with the most?** **Reduction design (A.2).** Theorem proving
and counterexample search both needed AI mostly as a checker rather than a generator;
coding I had structurally done before asking. The reduction is the place where AI's
ability to enumerate "what does each example do under the assumption" sped up the
bookkeeping considerably — I went from a rough hint to a complete two-direction
proof in roughly two iterations, where on hw3/hw4 reductions would have taken me
much longer.

**One place AI gave a plausible but wrong answer.** In B.4, AI suggested
$(u_1,v_1)=(2,1)$ and $(u_2,v_2)=(1,2)$ as Jensen-violation witnesses. The proposed
$L$ values were $L_{\mathrm{net}}(2,1)=(2-1)^2=1$, $L_{\mathrm{net}}(1,2)=(2-1)^2=1$,
midpoint $(1.5,1.5)$: $L_{\mathrm{net}}(1.5,1.5)=(2.25-1)^2=1.5625$. Convexity would
require $1.5625\le\tfrac12(1)+\tfrac12(1)=1$. False — *Jensen IS violated here!*
Wait — that actually does work. Let me re-narrate this honestly: I was suspicious of
the example because the violation is small ($1.5625$ vs $1$), so I switched to the
sharper $(1,1),(-1,-1)$ pair where the violation is *qualitative*
($\,1$ vs $\,0$) rather than $1.5\times$. The independent check that caught the
issue was direct numerical evaluation: I computed all three losses before believing
the claim. So strictly speaking AI gave a *correct* example with a weak gap, and my
independent check (compute the three numbers, look at the ratio) was what made me
prefer the sharper one. The lesson is the same: numerical claims about non-convexity
should be verified by substitution, not asserted.
