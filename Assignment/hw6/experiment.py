"""
Assignment 6, Part A.4 — AdaBoost over coordinate stumps vs. L1-LR surrogate, on
an "easy" sparse-margin distribution and on the A.3 hard construction.

Reports for each distribution:
  - training error, exponential loss, observed edge, support size, normalized L1 margin
    over AdaBoost rounds
  - L1-LR comparison (final train error, support, margin)
Produces three figures in ./figures/.
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)
RNG = np.random.default_rng(0)


# -----------------------------------------------------------------------------
# Distributions
# -----------------------------------------------------------------------------
def easy_distribution(n=200, d=20, s=5, rng=RNG):
    """Random {-1,+1} features; planted s-sparse target w_star with entries in {-1,+1}.
    Keep examples with margin >= 1 (resample until n collected)."""
    support = rng.choice(d, size=s, replace=False)
    w_star = np.zeros(d)
    w_star[support] = rng.choice([-1.0, 1.0], size=s)
    Xs, ys = [], []
    while len(Xs) < n:
        x = rng.choice([-1.0, 1.0], size=d)
        y = 1 if np.dot(w_star, x) >= 1 else (-1 if np.dot(w_star, x) <= -1 else 0)
        if y == 0:
            continue
        Xs.append(x)
        ys.append(float(y))
    return np.array(Xs), np.array(ys), w_star


def hard_distribution(m=3):
    """A.3 construction with s = 2m+1 rows = 2m+1 cols. Returns features X in {±1}^{s×s},
    labels y = +1, and a probability vector q/Z over examples (the "natural" weighting)."""
    s = 2 * m + 1
    rows = [("0",)] + [(r, sgn) for r in range(1, m + 1) for sgn in ("+", "-")]
    # row -> index
    row_idx = {r: i for i, r in enumerate(rows)}
    cols = ["0"] + [(p, "+") for p in range(1, m + 1)] + [(p, "-") for p in range(1, m + 1)]

    def base_col():
        """+1 in row 0, +1 in (r,+), -1 in (r,-) for all r."""
        v = np.zeros(s)
        v[row_idx[("0",)]] = 1
        for r in range(1, m + 1):
            v[row_idx[(r, "+")]] = 1
            v[row_idx[(r, "-")]] = -1
        return v

    Phi = np.zeros((s, s))
    Phi[:, 0] = base_col()
    # Pair-flip columns (p,+): base with pair p flipped.
    for j, c in enumerate(cols[1 : m + 1], start=1):
        p, _ = c
        v = base_col()
        v[row_idx[(p, "+")]] = -1
        v[row_idx[(p, "-")]] = 1
        Phi[:, j] = v
    # Carry columns (p,-).
    for j, c in enumerate(cols[m + 1 :], start=m + 1):
        p, _ = c
        v = np.zeros(s)
        v[row_idx[("0",)]] = -1
        for r in range(1, m + 1):
            if r < p:
                v[row_idx[(r, "+")]] = -1
                v[row_idx[(r, "-")]] = -1
            elif r == p:
                v[row_idx[(r, "+")]] = 1
                v[row_idx[(r, "-")]] = 1
            else:
                v[row_idx[(r, "+")]] = 1
                v[row_idx[(r, "-")]] = -1
        Phi[:, j] = v

    # Verify columns sum to 1 under q.
    q = np.zeros(s)
    q[row_idx[("0",)]] = 1.0
    for r in range(1, m + 1):
        q[row_idx[(r, "+")]] = 2.0 ** (r - 1)
        q[row_idx[(r, "-")]] = 2.0 ** (r - 1)
    sums = Phi.T @ q  # shape (s,)
    assert np.allclose(sums, 1.0), f"column sums = {sums}"
    assert abs(np.linalg.det(Phi)) > 1e-9, "Phi not invertible"

    X = Phi
    y = np.ones(s)
    p = q / q.sum()
    return X, y, p, Phi


# -----------------------------------------------------------------------------
# AdaBoost over coordinate stumps b_{j,sigma}(x) = sigma * x[j]
# -----------------------------------------------------------------------------
def adaboost_stumps(X, y, T=200, sample_weights=None):
    """Run AdaBoost over coordinate stumps. Returns per-round metrics and a final
    weight vector w (sum of alpha_t * sigma_t * e_{j_t})."""
    n, d = X.shape
    D = np.ones(n) / n if sample_weights is None else sample_weights.copy()
    D = D / D.sum()
    w_total = np.zeros(d)
    F = np.zeros(n)  # current margin scores y * sum alpha_t b_t(x_i)
    hist = {
        "train_err": [],
        "exp_loss": [],
        "edge": [],
        "support_size": [],
        "norm_margin": [],
    }
    for t in range(T):
        # weighted correlations c_j = sum_i D_i y_i x_{i,j}
        c = (D * y) @ X  # shape (d,)
        j = int(np.argmax(np.abs(c)))
        sigma = float(np.sign(c[j])) or 1.0
        edge = float(abs(c[j]))  # = sum_i D_i y_i b(x_i)
        if edge < 1e-12:
            break
        # weighted error eps_t = (1 - edge)/2
        eps_t = (1 - edge) / 2.0
        alpha = 0.5 * np.log((1 - eps_t) / max(eps_t, 1e-12))
        b_vals = sigma * X[:, j]  # b_t(x_i)
        w_total[j] += alpha * sigma
        F = F + alpha * y * b_vals
        # update D
        D = D * np.exp(-alpha * y * b_vals)
        D = D / D.sum()

        train_err = np.mean(np.sign(F * 0 + (X @ w_total)) != y)
        exp_loss = np.mean(np.exp(-y * (X @ w_total)))
        l1 = np.sum(np.abs(w_total))
        norm_margin = (y * (X @ w_total)).min() / max(l1, 1e-12)
        hist["train_err"].append(float(train_err))
        hist["exp_loss"].append(float(exp_loss))
        hist["edge"].append(edge)
        hist["support_size"].append(int(np.sum(np.abs(w_total) > 1e-9)))
        hist["norm_margin"].append(float(norm_margin))
    return w_total, hist


def l1_logreg(X, y):
    if len(np.unique(y)) < 2:
        # Only one class — degenerate; return trivial "all +1" predictor stats.
        return {"train_err": float((y != 1).mean()), "support": 0,
                "norm_margin": 0.0, "l1": 0.0, "degenerate": True}
    best = (None, -1)
    for C in (0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 50.0):
        clf = LogisticRegression(
            penalty="l1", C=C, fit_intercept=False, solver="liblinear", max_iter=5000
        )
        clf.fit(X, y)
        w = clf.coef_.ravel()
        train_acc = np.mean(np.sign(X @ w) == y)
        if train_acc > best[1]:
            best = (w, train_acc)
    w = best[0]
    l1 = np.sum(np.abs(w))
    margin = (y * (X @ w)).min() / max(l1, 1e-12) if l1 > 0 else 0.0
    return {
        "train_err": 1 - best[1],
        "support": int(np.sum(np.abs(w) > 1e-6)),
        "norm_margin": float(margin),
        "l1": float(l1),
    }


# -----------------------------------------------------------------------------
# Run + plot
# -----------------------------------------------------------------------------
def run_easy():
    X, y, w_star = easy_distribution(n=200, d=20, s=5)
    w, hist = adaboost_stumps(X, y, T=80)
    lr = l1_logreg(X, y)
    print("=== Easy distribution (n=200, d=20, s=5) ===")
    print(f"  AdaBoost final: train_err={hist['train_err'][-1]:.3f}  "
          f"support={hist['support_size'][-1]}  "
          f"norm_margin={hist['norm_margin'][-1]:.4f}  rounds={len(hist['edge'])}")
    print(f"  L1-LR  : train_err={lr['train_err']:.3f}  support={lr['support']}  "
          f"norm_margin={lr['norm_margin']:.4f}")
    return hist, lr, ("easy", X.shape, np.sum(np.abs(w_star)))


def run_hard():
    X, y, p, Phi = hard_distribution(m=3)
    # AdaBoost on the (uniform-over-distinct-rows) sample, weighted by q/Z
    w, hist = adaboost_stumps(X, y, T=200, sample_weights=p)
    lr = l1_logreg(X, y)
    Z = (2 ** (3 + 1)) - 1
    print(f"=== Hard distribution (A.3, m=3, s=7, Z={Z}) ===")
    print(f"  AdaBoost final: train_err={hist['train_err'][-1]:.3f}  "
          f"support={hist['support_size'][-1]}  "
          f"norm_margin={hist['norm_margin'][-1]:.4f}  rounds={len(hist['edge'])}")
    print(f"  best edge over rounds  = {max(hist['edge']):.4f}  "
          f"(theoretical max 1/Z={1/Z:.4f})")
    print(f"  L1-LR  : train_err={lr['train_err']:.3f}  support={lr['support']}  "
          f"norm_margin={lr['norm_margin']:.4f}")
    w_star = np.linalg.solve(Phi, np.ones(Phi.shape[0]))
    print(f"  ||w*||_inf = {np.max(np.abs(w_star)):.3f}, ||w*||_1 = "
          f"{np.sum(np.abs(w_star)):.3f}")
    return hist, lr


def plot_three(easy, hard):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, hist, name in zip(axes, (easy, hard), ("easy", "hard")):
        ax.plot(hist["train_err"], label="train 0-1 error")
        ax.plot(hist["exp_loss"], label="exp loss")
        ax.set_yscale("log")
        ax.set_xlabel("round")
        ax.set_title(f"AdaBoost training: {name}")
        ax.grid(True, alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "training.png", dpi=140)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, hist, name in zip(axes, (easy, hard), ("easy", "hard")):
        ax.plot(hist["edge"], label="observed edge")
        ax.set_xlabel("round")
        ax.set_ylabel("edge = E_D[y b(x)]")
        ax.set_title(f"Weak-learner edge: {name}")
        ax.grid(True, alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "edge.png", dpi=140)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, hist, name in zip(axes, (easy, hard), ("easy", "hard")):
        ax.plot(hist["norm_margin"], label="L1-normalized margin", color="tab:green")
        ax2 = ax.twinx()
        ax2.plot(hist["support_size"], color="tab:red", label="support size")
        ax.set_xlabel("round")
        ax.set_ylabel("normalized margin", color="tab:green")
        ax2.set_ylabel("support size", color="tab:red")
        ax.set_title(f"Margin and support: {name}")
    fig.tight_layout()
    fig.savefig(FIG / "margin.png", dpi=140)
    plt.close(fig)


def main():
    easy_h, easy_lr, _ = run_easy()
    hard_h, hard_lr = run_hard()
    plot_three(easy_h, hard_h)
    print(f"Wrote figures to {FIG}")


if __name__ == "__main__":
    main()
