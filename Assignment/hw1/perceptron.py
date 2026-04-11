"""
hw1/perceptron.py
DSC 190/291 — Assignment 1, Part C

Perceptron algorithm implementation and experiments.
Verifies the mistake bound M <= R^2 / gamma^2 from the Perceptron theorem.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUTDIR = Path(__file__).parent
N_TRIALS = 30    # repetitions per setting (average over random orderings)
N_EXAMPLES = 3000
RNG_BASE = 2026  # base seed for reproducibility


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Perceptron algorithm
# ─────────────────────────────────────────────────────────────────────────────

def perceptron(X: np.ndarray, y: np.ndarray) -> tuple[int, np.ndarray]:
    """
    Online Perceptron algorithm (mistake-driven update).

    Parameters
    ----------
    X : (T, d) array of examples
    y : (T,) array of labels in {-1, +1}

    Returns
    -------
    mistakes : int
        Total number of mistakes made.
    w : (d,) array
        Final weight vector.
    """
    T, d = X.shape
    w = np.zeros(d)
    mistakes = 0
    for xt, yt in zip(X, y):
        yhat = 1 if np.dot(w, xt) >= 0 else -1
        if yhat != yt:
            w = w + yt * xt
            mistakes += 1
    return mistakes, w


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Data generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_data(n: int, d: int, gamma: float, R: float = 1.0,
                  tight_margin: bool = False,
                  seed: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate n linearly separable examples in R^d with margin >= gamma.

    Construction (answering Question C.1):
    - True separator: u* = e_1 (first standard basis vector).
    - x_1 is drawn from [gamma, R] (sign randomly ±1).
    - If tight_margin=True, x_1 is drawn from [gamma, gamma + 0.05*(R-gamma)],
      keeping the margin close to gamma; this makes the 1/gamma^2 scaling
      visible cleanly in experiment 1.
    - Remaining coordinates x_2,...,x_d are drawn from a Gaussian and scaled
      so that ||x|| = R exactly.
    - Label: y = sign(x_1).

    This guarantees:
      - ||x|| = R  (norm bound)
      - y * (u* · x) = |x_1| >= gamma  (margin condition)
    Both R and gamma are independent of dimension d.

    Parameters
    ----------
    n            : number of examples
    d            : dimension (d >= 1)
    gamma        : margin parameter, 0 < gamma < R
    R            : norm of every example
    tight_margin : if True, draw |x_1| near gamma (margin ≈ gamma exactly)
    seed         : random seed for reproducibility
    """
    assert 0 < gamma < R, "Need 0 < gamma < R"
    rng = np.random.default_rng(seed)

    if tight_margin:
        # Draw |x_1| from [gamma, gamma + 5% of slack] to keep margin ≈ gamma
        slack = min(0.05 * (R - gamma), 0.02)
        x1_mag = rng.uniform(gamma, gamma + slack, size=n)
    else:
        # Draw |x_1| uniformly from [gamma, R]
        x1_mag = rng.uniform(gamma, R, size=n)

    # Assign labels uniformly at random
    labels = rng.choice([-1, 1], size=n)
    x1 = labels * x1_mag   # x_1 = ±|x_1|

    if d == 1:
        X = x1.reshape(-1, 1)
    else:
        # Remaining coordinates: Gaussian, then project onto sphere of radius
        # sqrt(R^2 - x_1^2) so that ||x|| = R.
        remainder_norm = np.sqrt(np.maximum(R**2 - x1_mag**2, 0.0))
        rest = rng.standard_normal((n, d - 1))
        norms = np.linalg.norm(rest, axis=1, keepdims=True)
        # Avoid division by zero when remainder_norm == 0
        norms = np.where(norms == 0, 1.0, norms)
        rest = rest / norms * remainder_norm[:, None]
        X = np.concatenate([x1[:, None], rest], axis=1)

    y = labels
    # Shuffle to avoid any ordering artifacts
    perm = rng.permutation(n)
    return X[perm], y[perm]


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Verification helpers (answering Question C.6)
# ─────────────────────────────────────────────────────────────────────────────

def verify_data(X: np.ndarray, y: np.ndarray, gamma: float, R: float,
                tol: float = 1e-8) -> None:
    """Assert that the dataset satisfies the margin and norm conditions."""
    u_star = np.zeros(X.shape[1])
    u_star[0] = 1.0

    margins = y * (X @ u_star)
    norms = np.linalg.norm(X, axis=1)

    assert np.all(margins >= gamma - tol), (
        f"Margin violation: min margin = {margins.min():.6f} < {gamma}"
    )
    assert np.all(np.abs(norms - R) <= tol), (
        f"Norm violation: max |||x||-R| = {np.abs(norms - R).max():.2e}"
    )


def verify_perceptron_bounds(X: np.ndarray, y: np.ndarray,
                             gamma: float, R: float) -> dict:
    """
    Run Perceptron and verify the inner-product / norm bounds from the proof.

    After M mistakes with updates w_{t+1} = w_t + y_t x_t:
      - w_M · u* >= M * gamma     (inner-product bound)
      - ||w_M||^2 <= M * R^2      (squared-norm bound)
    These two together imply M <= R^2/gamma^2.
    """
    T, d = X.shape
    w = np.zeros(d)
    u_star = np.zeros(d); u_star[0] = 1.0
    mistakes = 0

    for xt, yt in zip(X, y):
        yhat = 1 if np.dot(w, xt) >= 0 else -1
        if yhat != yt:
            w = w + yt * xt
            mistakes += 1

    if mistakes == 0:
        return {"mistakes": 0, "inner_prod_bound_satisfied": True,
                "norm_bound_satisfied": True}

    inner_prod = np.dot(w, u_star)
    norm_sq = np.dot(w, w)
    return {
        "mistakes": mistakes,
        "inner_prod": inner_prod,
        "inner_prod_lower_bound": mistakes * gamma,
        "inner_prod_bound_satisfied": inner_prod >= mistakes * gamma - 1e-8,
        "norm_sq": norm_sq,
        "norm_sq_upper_bound": mistakes * R**2,
        "norm_bound_satisfied": norm_sq <= mistakes * R**2 + 1e-8,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Experiments
# ─────────────────────────────────────────────────────────────────────────────

def exp1_mistakes_vs_gamma():
    """
    Experiment 1 — Mistakes vs γ (Question C.2 and C.3).

    Fix d = 5, R = 1. Vary gamma from 0.05 to 0.45.
    We use tight_margin=True so that |x_1| ≈ gamma for every example,
    keeping the effective margin close to gamma. This makes the 1/gamma^2
    scaling clearly visible in the log-log plot.
    Compare observed average mistakes to the theoretical bound R^2/gamma^2.
    The observed count is well below the worst-case bound (Question C.3).
    """
    print("Experiment 1: Mistakes vs γ ...")
    d, R = 5, 1.0
    gammas = np.linspace(0.05, 0.45, 22)

    avg_mistakes, std_mistakes = [], []
    for gamma in gammas:
        ms = []
        for trial in range(N_TRIALS):
            X, y = generate_data(N_EXAMPLES, d, gamma, R=R,
                                 tight_margin=True, seed=RNG_BASE + trial)
            m, _ = perceptron(X, y)
            ms.append(m)
        avg_mistakes.append(np.mean(ms))
        std_mistakes.append(np.std(ms))

    avg_mistakes = np.array(avg_mistakes)
    std_mistakes = np.array(std_mistakes)
    theoretical  = R**2 / gammas**2

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: mistakes vs gamma (linear scale)
    axes[0].fill_between(gammas,
                         avg_mistakes - std_mistakes,
                         avg_mistakes + std_mistakes,
                         alpha=0.25, label='±1 std')
    axes[0].plot(gammas, avg_mistakes, 'o-', label='Observed mistakes (mean)')
    axes[0].plot(gammas, theoretical, 'r--', label=r'Bound $R^2/\gamma^2$')
    axes[0].set_xlabel(r'$\gamma$', fontsize=13)
    axes[0].set_ylabel('Number of mistakes', fontsize=13)
    axes[0].set_title(r'Mistakes vs $\gamma$  ($d=5$, $R=1$)', fontsize=13)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Right: log-log plot vs 1/gamma^2
    inv_g2 = 1.0 / gammas**2
    coeffs = np.polyfit(np.log(inv_g2), np.log(avg_mistakes), 1)
    fit_line = np.exp(coeffs[1]) * inv_g2**coeffs[0]

    axes[1].loglog(inv_g2, avg_mistakes, 'o-', label='Observed mistakes')
    axes[1].loglog(inv_g2, theoretical, 'r--', label=r'Bound $R^2/\gamma^2$')
    axes[1].loglog(inv_g2, fit_line, 'k:', alpha=0.7,
                   label=f'Best-fit slope = {coeffs[0]:.2f}')
    axes[1].set_xlabel(r'$1/\gamma^2$', fontsize=13)
    axes[1].set_ylabel('Number of mistakes', fontsize=13)
    axes[1].set_title(r'Log–log: Mistakes vs $1/\gamma^2$', fontsize=13)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    out = OUTDIR / 'exp1_mistakes_vs_gamma.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved {out.name}")
    print(f"  Log-log slope: {coeffs[0]:.3f}  (expected ≈ 1.0)")
    print(f"  Theoretical bound vs observed at gamma=0.1: "
          f"{R**2/0.1**2:.0f} vs {avg_mistakes[np.argmin(np.abs(gammas-0.1))]:.1f}")


def exp2_dimension_independence():
    """
    Experiment 2 — Dimension independence (Question C.4).

    Fix gamma = 0.2, R = 1. Vary d from 1 to 500.
    The theoretical bound R^2/gamma^2 = 25 does not depend on d.
    We show observed mistakes stay roughly constant as d grows.
    """
    print("Experiment 2: Dimension independence ...")
    gamma, R = 0.2, 1.0
    dims = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    theoretical_bound = R**2 / gamma**2

    avg_mistakes = []
    for d in dims:
        ms = []
        for trial in range(N_TRIALS):
            X, y = generate_data(N_EXAMPLES, d, gamma, R=R,
                                 seed=RNG_BASE + trial)
            m, _ = perceptron(X, y)
            ms.append(m)
        avg_mistakes.append(np.mean(ms))
        print(f"  d={d:4d}: avg mistakes = {avg_mistakes[-1]:.1f}")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.semilogx(dims, avg_mistakes, 'o-', label='Observed mistakes (mean)')
    ax.axhline(theoretical_bound, color='r', linestyle='--',
               label=rf'Bound $R^2/\gamma^2 = {theoretical_bound:.0f}$')
    ax.set_xlabel('Dimension $d$  (log scale)', fontsize=13)
    ax.set_ylabel('Number of mistakes', fontsize=13)
    ax.set_title(r'Mistakes vs Dimension  ($\gamma=0.2$, $R=1$)', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out = OUTDIR / 'exp2_dimension.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved {out.name}")


def exp3_gamma_to_zero():
    """
    Experiment 3 — Behavior as gamma → 0 (Question C.5).

    Fix d = 2, R = 1. Vary gamma from 0.3 down to 0.005.
    As gamma → 0, examples can be arbitrarily close to the decision boundary.
    The bound R^2/gamma^2 → ∞, and observed mistakes grow rapidly.
    Connection to the threshold counterexample: with gamma = 0, examples can
    lie exactly at the threshold, and no finite mistake bound is possible.
    """
    print("Experiment 3: γ → 0 ...")
    d, R = 2, 1.0
    gammas = [0.30, 0.20, 0.15, 0.10, 0.07, 0.05, 0.03, 0.02, 0.01, 0.005]

    avg_mistakes = []
    for gamma in gammas:
        ms = []
        for trial in range(N_TRIALS):
            X, y = generate_data(N_EXAMPLES, d, gamma, R=R,
                                 seed=RNG_BASE + trial)
            m, _ = perceptron(X, y)
            ms.append(m)
        avg_mistakes.append(np.mean(ms))

    theoretical = R**2 / np.array(gammas)**2

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.loglog(gammas, avg_mistakes, 'o-', label='Observed mistakes')
    ax.loglog(gammas, theoretical, 'r--', label=r'Bound $R^2/\gamma^2$')
    ax.set_xlabel(r'$\gamma$  (log scale, decreasing →)', fontsize=13)
    ax.set_ylabel('Number of mistakes  (log scale)', fontsize=13)
    ax.set_title(r'Mistakes as $\gamma \to 0$  ($d=2$, $R=1$, $T=3000$)',
                 fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.invert_xaxis()

    plt.tight_layout()
    out = OUTDIR / 'exp3_gamma_to_zero.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved {out.name}")


def run_sanity_checks():
    """
    Sanity checks that catch subtle bugs (Question C.6).

    Check 1 — Correct sign convention: a sequence with a single obvious
    positive example should produce exactly one mistake when Perceptron starts
    from w=0 (since w·x = 0 predicts +1, so if the label is +1 it's correct).

    Check 2 — No spurious updates: on a run with zero mistakes the weight
    vector must remain all-zeros.

    Check 3 — Proof invariants: verify w_M · u* >= M*gamma and ||w_M||^2 <=
    M*R^2 after every run. A bug in the update rule (e.g., wrong sign, wrong
    scaling) would violate one of these.

    Check 4 — Determinism: same seed gives same results.
    """
    print("Sanity checks ...")

    # ── Check 1: sign convention at w=0 ──────────────────────────────────────
    # w=0 → predict +1 (dot product = 0 >= 0).
    # Example (+1, +1): no mistake. Example (-1, +1): mistake → update.
    X1 = np.array([[1.0, 0.0]])
    y1 = np.array([1])
    m1, w1 = perceptron(X1, y1)
    assert m1 == 0 and np.allclose(w1, 0), (
        "Check 1 failed: w=0 should predict +1 correctly for positive example."
    )

    X2 = np.array([[-1.0, 0.0]])
    y2 = np.array([-1])
    m2, w2 = perceptron(X2, y2)
    assert m2 == 1 and np.allclose(w2, [1.0, 0.0]), (
        f"Check 1b failed: expected 1 mistake and w=[1,0], got {m2}, {w2}."
    )
    print("  Check 1 (sign convention at w=0): PASSED")

    # ── Check 2: zero mistakes → w unchanged ─────────────────────────────────
    # All-positive data well separated from origin.
    rng = np.random.default_rng(0)
    X3 = rng.uniform(0.5, 1.0, (30, 4))
    y3 = np.ones(30, dtype=int)
    m3, w3 = perceptron(X3, y3)
    assert m3 == 0 and np.allclose(w3, 0), (
        "Check 2 failed: zero-mistake run should leave w = 0."
    )
    print("  Check 2 (no updates on zero-mistake run): PASSED")

    # ── Check 3: proof invariants ─────────────────────────────────────────────
    for gamma, d in [(0.3, 3), (0.15, 10), (0.05, 2)]:
        X4, y4 = generate_data(1000, d, gamma, R=1.0, tight_margin=False, seed=42)
        verify_data(X4, y4, gamma, R=1.0)
        result = verify_perceptron_bounds(X4, y4, gamma=gamma, R=1.0)
        assert result["inner_prod_bound_satisfied"], (
            f"Proof invariant (inner product) violated: {result}"
        )
        assert result["norm_bound_satisfied"], (
            f"Proof invariant (norm) violated: {result}"
        )
    print("  Check 3 (proof invariants w_M·u* >= M*gamma, ||w_M||^2 <= M*R^2): PASSED")

    # ── Check 4: determinism ──────────────────────────────────────────────────
    X5a, y5a = generate_data(200, 5, 0.2, tight_margin=False, seed=99)
    X5b, y5b = generate_data(200, 5, 0.2, tight_margin=False, seed=99)
    assert np.allclose(X5a, X5b) and np.array_equal(y5a, y5b), (
        "Check 4 failed: same seed should produce identical data."
    )
    print("  Check 4 (determinism): PASSED")

    print("All sanity checks passed.\n")


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    OUTDIR.mkdir(exist_ok=True)

    run_sanity_checks()
    exp1_mistakes_vs_gamma()
    exp2_dimension_independence()
    exp3_gamma_to_zero()

    print(f"\nAll experiments complete. Plots saved to: {OUTDIR}")
