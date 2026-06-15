"""
Assignment 5, Part A.3 — Proper sparse 0-1 search vs. L1-regularized convex surrogate.

We compare:
  (i)  brute-force enumeration of k-sparse supports, fitting a halfspace per support
       via L2-regularized logistic regression and evaluating 0-1 agreement; reporting
       the best agreement across supports. The enumeration is exact; the per-support
       fit is an approximation (a convex surrogate inside a fixed-dimensional subproblem).
  (ii) L1-regularized logistic regression on the full d-dimensional problem, sweeping
       the regularization strength C and reporting the best 0-1 agreement attained.

Reports:
  - runtime scaling as d grows (k=3 fixed) and as k grows (d=20 fixed)
  - 0-1 agreement gap as a function of label-noise rate (d=20, k=3 fixed)

Produces runtime.png and agreement.png in the same directory.
"""

from __future__ import annotations
import itertools
import time
import warnings
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression

RNG = np.random.default_rng(0)
HERE = Path(__file__).resolve().parent


def make_data(n: int, d: int, k_true: int, noise: float, rng=RNG):
    """Synthetic data: plant a k_true-sparse weight vector, label by its sign, flip
    each label independently with probability `noise`."""
    X = rng.standard_normal((n, d))
    support = rng.choice(d, size=k_true, replace=False)
    w_star = np.zeros(d)
    w_star[support] = rng.choice([-1.0, 1.0], size=k_true)
    y = np.sign(X @ w_star)
    y[y == 0] = 1.0
    flip = rng.random(n) < noise
    y = np.where(flip, -y, y)
    return X, y.astype(float), w_star


def fit_halfspace_on_support(X_sub: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Fit a halfspace on the restricted-support feature matrix via L2-LR."""
    if X_sub.shape[1] == 0:
        return np.zeros(0)
    clf = LogisticRegression(
        penalty="l2", C=1e3, fit_intercept=False, solver="lbfgs", max_iter=2000
    )
    clf.fit(X_sub, y)
    return clf.coef_.ravel()


def empirical_agreement(w: np.ndarray, X: np.ndarray, y: np.ndarray) -> int:
    s = np.sign(X @ w)
    s[s == 0] = 1.0
    return int(np.sum(s == y))


def brute_force_sparse(X: np.ndarray, y: np.ndarray, k: int):
    """Enumerate all supports of size <= k, fit a halfspace on each, return best
    0-1 agreement and runtime."""
    n, d = X.shape
    t0 = time.perf_counter()
    best = -1
    best_w = np.zeros(d)
    for sz in range(1, k + 1):
        for T in itertools.combinations(range(d), sz):
            w_T = fit_halfspace_on_support(X[:, list(T)], y)
            w_full = np.zeros(d)
            w_full[list(T)] = w_T
            agree = empirical_agreement(w_full, X, y)
            if agree > best:
                best = agree
                best_w = w_full
    return best, best_w, time.perf_counter() - t0


def l1_surrogate(X: np.ndarray, y: np.ndarray):
    """L1-regularized logistic regression sweep; return best-agreement w and runtime."""
    t0 = time.perf_counter()
    best = -1
    best_w = np.zeros(X.shape[1])
    for C in (0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 50.0):
        clf = LogisticRegression(
            penalty="l1", C=C, fit_intercept=False, solver="liblinear", max_iter=2000
        )
        clf.fit(X, y)
        w = clf.coef_.ravel()
        agree = empirical_agreement(w, X, y)
        if agree > best:
            best = agree
            best_w = w
    return best, best_w, time.perf_counter() - t0


def runtime_scaling_d(ks=(3,), ds=(8, 10, 12, 14, 16, 18, 20), n=200, noise=0.05):
    rows = []
    for k in ks:
        for d in ds:
            X, y, _ = make_data(n, d, k, noise)
            _, _, t_bf = brute_force_sparse(X, y, k)
            _, _, t_l1 = l1_surrogate(X, y)
            rows.append((k, d, t_bf, t_l1))
            print(f"d={d:3d} k={k} brute={t_bf:6.2f}s   l1={t_l1:5.2f}s")
    return rows


def runtime_scaling_k(d=20, ks=(1, 2, 3, 4), n=200, noise=0.05):
    rows = []
    for k in ks:
        X, y, _ = make_data(n, d, k, noise)
        _, _, t_bf = brute_force_sparse(X, y, k)
        _, _, t_l1 = l1_surrogate(X, y)
        rows.append((k, d, t_bf, t_l1))
        print(f"d={d} k={k} brute={t_bf:6.2f}s   l1={t_l1:5.2f}s")
    return rows


def agreement_vs_noise(d=20, k=3, n=400, noises=(0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4)):
    rows = []
    for noise in noises:
        X, y, _ = make_data(n, d, k, noise)
        agree_bf, _, _ = brute_force_sparse(X, y, k)
        agree_l1, _, _ = l1_surrogate(X, y)
        rows.append((noise, agree_bf / n, agree_l1 / n))
        print(f"noise={noise:.2f}  brute={agree_bf}/{n}  l1={agree_l1}/{n}")
    return rows


def plot_runtime(rows_d, rows_k):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    ds = [r[1] for r in rows_d]
    bf = [r[2] for r in rows_d]
    l1 = [r[3] for r in rows_d]
    axes[0].plot(ds, bf, "o-", label="brute-force k-sparse")
    axes[0].plot(ds, l1, "s-", label="L1 surrogate (sweep)")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("d (k=3 fixed)")
    axes[0].set_ylabel("runtime (s, log scale)")
    axes[0].set_title("Runtime vs. d")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    ks = [r[0] for r in rows_k]
    bf = [r[2] for r in rows_k]
    l1 = [r[3] for r in rows_k]
    axes[1].plot(ks, bf, "o-", label="brute-force k-sparse")
    axes[1].plot(ks, l1, "s-", label="L1 surrogate (sweep)")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("k (d=20 fixed)")
    axes[1].set_ylabel("runtime (s, log scale)")
    axes[1].set_title("Runtime vs. k")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(HERE / "runtime.png", dpi=140)
    plt.close(fig)


def plot_agreement(rows):
    noises = [r[0] for r in rows]
    bf = [r[1] for r in rows]
    l1 = [r[2] for r in rows]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(noises, bf, "o-", label="brute-force k-sparse 0-1 best")
    ax.plot(noises, l1, "s-", label="L1 surrogate 0-1 best")
    ax.set_xlabel("label-noise rate")
    ax.set_ylabel("empirical agreement (fraction)")
    ax.set_title("0-1 agreement vs. noise (d=20, k=3, n=400)")
    ax.set_ylim(0.45, 1.02)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(HERE / "agreement.png", dpi=140)
    plt.close(fig)


def main():
    print("=== Runtime scaling in d ===")
    rows_d = runtime_scaling_d()
    print("=== Runtime scaling in k ===")
    rows_k = runtime_scaling_k()
    plot_runtime(rows_d, rows_k)
    print("=== Agreement vs. noise ===")
    rows_a = agreement_vs_noise()
    plot_agreement(rows_a)
    print("Wrote runtime.png and agreement.png")


if __name__ == "__main__":
    main()
