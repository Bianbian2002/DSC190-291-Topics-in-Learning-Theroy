# Part E — AI Usage Report

**DSC 190/291 — Assignment 7**
**Student: Zeyu Bian**

## E.1 Existing workflow (3 pts)

I used the same AI-assisted workflow as in previous assignments, with a few refinements:

- **Theory-then-verify pattern.** For each proof (A.1, A.2, B.1–B.3, C.1–C.4), I first worked through the proof structure on paper, identifying the key steps (e.g., "use Cauchy–Schwarz after pulling out the sup" for A.1, "decompose $w = w_\parallel + w_\perp$" for A.2). I then asked Claude to help me write the proof in clean LaTeX-flavored markdown, and verified each step.

- **Experiment checklist from HW6.** I carried over the "five diagnostics per round" checklist from HW6 (train error, loss, edge, support, margin) and adapted it for FixedBoost. The main adaptation: FixedBoost has a fixed step size, so $\|w_t\|_1 = t\eta$ is deterministic — I tracked it anyway as a sanity check.

- **LP verification workflow.** For Part D, I used the pattern: (1) formulate the optimization mathematically, (2) implement it using `scipy.optimize.linprog`, (3) verify on a small hand-computable example before running on the real instances.

## E.2 Skill development (3 pts)

I developed a **"margin-bound proof" skill** — a reusable template for deriving generalization bounds via Rademacher complexity and margin arguments. The template:

1. Identify the function class and its parameterization (e.g., $\ell_1$ ball, kernel ball).
2. Bound the empirical Rademacher complexity (via finite-class reduction + Massart, or via norm bounds).
3. Apply the Lipschitz composition lemma to convert from the linear predictor class to the loss class.
4. Apply the uniform convergence theorem (Rademacher $\to$ generalization gap).
5. If the goal is 0/1 error, use a surrogate (ramp loss) and note the calibration step.

This template was used in A.1, B.2, B.3, and C.1, covering four of the assignment's proofs. The template helps avoid a common AI failure mode: jumping directly to the final bound without establishing the intermediate steps that connect the function class to the generalization guarantee.

## E.3 Verification (4 pts)

**Plausible failure modes and how I checked:**

1. **Wrong direction in inequalities (proofs).** AI sometimes flips $\le$ and $\ge$ in chain inequalities, especially in Jensen and Cauchy–Schwarz applications. For A.1, I verified by checking the extreme case: if $\varphi(x_i) = e_i$ (orthonormal), then $K(x_i,x_i)=1$, $\sum K(x_i,x_i)=n$, and $\hat{\mathcal{R}}_S = B/\sqrt{n}$ by direct computation, matching the bound with equality (up to Jensen).

2. **Incorrect LP formulation (Part D).** I verified the LP optimal margin on a tiny $2\times 4$ instance where the answer is computable by hand: $A = [[1,1,-1,-1],[1,-1,1,-1]]$, optimal $p=(0.5,0,0.5,0)$, margin $= 1$. The LP solver returned $1.0$.

3. **FixedBoost implementation bugs.** The most likely bug is in the reweighting step (using raw scores vs. cumulative scores, or forgetting to normalize). I verified by checking that on a trivially separable instance (one coordinate perfectly predicts $y$), FixedBoost converges to margin $1.0$ and concentrates all weight on that coordinate.

4. **Convex-hull identity (B.1).** AI initially wrote "the sup over a compact convex set equals the sup over its extreme points" without noting this only holds for *linear* objectives. I added the explicit argument that $\Phi(h) = \frac{1}{n}\sum_i \sigma_i h(x_i)$ is linear in $h$.

5. **Minimax theorem application (C.3).** The factor of $\frac{1}{2}$ between edge and margin is easy to drop. I traced the definitions: edge $= \frac{1}{2}\sum D_i A_{ig}$, while margin $= \min_i \sum p_g A_{ig} = \min_D D^\top A p$. The minimax value is $\min_D \max_g D^\top A_{\cdot g}$, which equals $2 \gamma^*_{\text{WL}}$ (not $\gamma^*_{\text{WL}}$). I verified on the $2\times 4$ example above.

6. **Plot correctness.** I visually checked that the FixedBoost margin trajectory is monotonically non-decreasing (it should be, modulo oscillations from the fixed step size) and that it stays below the LP-optimal line. Both hold in the generated plots.
