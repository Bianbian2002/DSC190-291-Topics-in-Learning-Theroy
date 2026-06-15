"""
Assignment 7, Part D — FixedBoost margin experiment.

Implements FixedBoost from scratch on the sign matrix A, compares the
normalized ell_1 margin trajectory against the LP-optimal margin for two
instances (large-margin and small-margin).
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)
RNG = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Sign matrix construction
# ---------------------------------------------------------------------------

def build_sign_matrix(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Build A in {-1,+1}^{n x 2d} with columns for x_j and -x_j.
    A_{ig} = y_i * g(x_i)."""
    n, d = X.shape
    G_pos = X * y[:, None]
    G_neg = -X * y[:, None]
    A = np.hstack([G_pos, G_neg])
    return A


# ---------------------------------------------------------------------------
# FixedBoost
# ---------------------------------------------------------------------------

def fixedboost(A: np.ndarray, eta: float, T: int):
    """Run FixedBoost on sign matrix A with fixed step size eta for T rounds.
    Returns per-round metrics."""
    n, num_g = A.shape
    w = np.zeros(num_g)
    scores = np.zeros(n)  # cumulative: scores_i = sum_t eta * A_{i, g_t}
    D = np.ones(n) / n

    margins = []
    l1_norms = []

    for t in range(T):
        corr = D @ A
        g_t = int(np.argmax(corr))

        w[g_t] += eta
        scores += eta * A[:, g_t]

        log_D = -scores
        log_D -= log_D.max()
        D = np.exp(log_D)
        D /= D.sum()

        l1 = np.sum(np.abs(w))
        margin = scores.min() / l1 if l1 > 0 else 0.0
        margins.append(margin)
        l1_norms.append(l1)

    return w, np.array(margins), np.array(l1_norms)


# ---------------------------------------------------------------------------
# Optimal margin via LP
# ---------------------------------------------------------------------------

def optimal_margin_lp(A: np.ndarray) -> float:
    """Solve max gamma s.t. Ap >= gamma*1, p >= 0, 1^T p = 1.

    Rewrite as: min -gamma
      s.t. A p - gamma 1 >= 0  =>  [-A | 1] [p; gamma] <= 0 (ub form)
           1^T p = 1
           p >= 0, gamma free
    """
    n, num_g = A.shape
    c = np.zeros(num_g + 1)
    c[-1] = -1.0  # minimize -gamma

    A_ub = np.hstack([-A, np.ones((n, 1))])
    b_ub = np.zeros(n)

    A_eq = np.zeros((1, num_g + 1))
    A_eq[0, :num_g] = 1.0
    b_eq = np.array([1.0])

    bounds = [(0, None)] * num_g + [(None, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method='highs')
    if res.success:
        return -res.fun
    return 0.0


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------

def make_large_margin_instance(n=100, d=10, rng=RNG):
    """Labels y = sign(x_1 + x_2 + x_3) — majority of 3 coordinates.
    No single coordinate achieves margin 1 (each has correlation ~1/2 with y
    for ties broken), but the optimal combination has margin ~1/3.
    Filter out ties (sum = 0 impossible for 3 binary vars)."""
    X = rng.choice([-1.0, 1.0], size=(n, d))
    y = np.sign(X[:, 0] + X[:, 1] + X[:, 2])
    return X, y


def make_small_margin_instance(n=100, d=10, rng=RNG):
    """Labels depend on sign(sum of first 7 coords): each coordinate has
    weak individual correlation with y, so optimal margin is small."""
    Xs, ys = [], []
    k = 7
    while len(Xs) < n:
        batch = rng.choice([-1.0, 1.0], size=(n * 3, d))
        raw = batch[:, :k].sum(axis=1)
        keep = raw != 0
        Xs.append(batch[keep])
        ys.append(np.sign(raw[keep]))
    X = np.vstack(Xs)[:n]
    y = np.concatenate(ys)[:n]
    return X, y


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_margin_trajectory(margins, opt_margin, title, filename):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    rounds = np.arange(1, len(margins) + 1)
    ax.plot(rounds, margins, label="FixedBoost normalized margin", color="tab:blue")
    ax.axhline(opt_margin, color="tab:red", linestyle="--",
               label=f"LP-optimal margin = {opt_margin:.4f}")
    ax.set_xlabel("Round $t$")
    ax.set_ylabel("Normalized $\\ell_1$ margin")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / filename, dpi=140)
    plt.close(fig)


def plot_eta_sensitivity(A, opt_margin, etas, T, title, filename):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for eta in etas:
        _, margins, _ = fixedboost(A, eta=eta, T=T)
        ax.plot(np.arange(1, T + 1), margins, label=f"$\\eta={eta}$")
    ax.axhline(opt_margin, color="tab:red", linestyle="--",
               label=f"LP-optimal = {opt_margin:.4f}")
    ax.set_xlabel("Round $t$")
    ax.set_ylabel("Normalized $\\ell_1$ margin")
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / filename, dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Part D: FixedBoost Margin Experiment")
    print("=" * 60)

    # --- Large-margin instance ---
    X_large, y_large = make_large_margin_instance(n=50, d=10)
    A_large = build_sign_matrix(X_large, y_large)
    opt_large = optimal_margin_lp(A_large)
    print(f"\n[Large-margin instance] n={len(y_large)}, d=10, |G|={A_large.shape[1]}")
    print(f"  LP-optimal margin: {opt_large:.4f}")

    eta_large = 0.1
    T_large = 500
    w_large, margins_large, l1_large = fixedboost(A_large, eta=eta_large, T=T_large)
    print(f"  FixedBoost (eta={eta_large}, T={T_large}):")
    print(f"    Final margin: {margins_large[-1]:.4f}")
    print(f"    Max margin:   {margins_large.max():.4f} at round {margins_large.argmax()+1}")
    print(f"    Final ||w||_1: {l1_large[-1]:.2f}")

    plot_margin_trajectory(margins_large, opt_large,
                           f"Large-margin instance ($\\eta={eta_large}$, n={len(y_large)}, d=10)",
                           "margin_large.png")

    # --- Small-margin instance ---
    X_small, y_small = make_small_margin_instance(n=50, d=10)
    A_small = build_sign_matrix(X_small, y_small)
    opt_small = optimal_margin_lp(A_small)
    print(f"\n[Small-margin instance] n={len(y_small)}, d=10, |G|={A_small.shape[1]}")
    print(f"  LP-optimal margin: {opt_small:.4f}")

    eta_small = 0.05
    T_small = 2000
    w_small, margins_small, l1_small = fixedboost(A_small, eta=eta_small, T=T_small)
    print(f"  FixedBoost (eta={eta_small}, T={T_small}):")
    print(f"    Final margin: {margins_small[-1]:.4f}")
    print(f"    Max margin:   {margins_small.max():.4f} at round {margins_small.argmax()+1}")
    print(f"    Final ||w||_1: {l1_small[-1]:.2f}")

    plot_margin_trajectory(margins_small, opt_small,
                           f"Small-margin instance ($\\eta={eta_small}$, n={len(y_small)}, d=10)",
                           "margin_small.png")

    # --- Step-size sensitivity (on large-margin instance) ---
    plot_eta_sensitivity(A_large, opt_large,
                         etas=[0.01, 0.05, 0.1, 0.5, 1.0],
                         T=500,
                         title="Step-size sensitivity (large-margin instance)",
                         filename="eta_sensitivity.png")

    print(f"\nWrote figures to {FIG}")


if __name__ == "__main__":
    main()
