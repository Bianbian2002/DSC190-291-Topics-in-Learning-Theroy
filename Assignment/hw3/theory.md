# Assignment 3 — Write-up
**DSC 190/291 — Learning Theory**
**Student: Zeyu Bian**

---

# Part A — A Mini-Course on Concentration Inequalities

This mini-course develops the four concentration inequalities used (without proof) in the
Week 3 derivation of the i.i.d. growth-function ERM guarantee:

- Hoeffding's inequality,
- Hoeffding's inequality for sampling without replacement,
- McDiarmid's bounded-differences inequality,
- Bernstein's inequality.

The exposition is self-contained: every result we cite is proved here. We close by gluing
the pieces together to give a full proof of the Week 3 ERM bound.

## A.1 The concept of concentration

**What concentrates.** A *concentration inequality* is a quantitative statement that some
random quantity $Z$ — typically a function $Z = f(X_1,\dots,X_n)$ of many independent
inputs — is, with high probability, very close to a deterministic value (usually its mean
$\mathbb{E} Z$, sometimes its median). Concretely, we want bounds of the form
$$
\Pr\bigl(\,|Z - \mathbb{E}Z|\ge t\,\bigr)\;\le\;2\exp\!\bigl(-c\, t^2 / v\bigr),
$$
where $v$ is some "scale" parameter (a sum of squared ranges, a variance proxy, etc.).
The quadratic-in-$t$ exponent is what we mean by *sub-Gaussian* tails.

**Why we should expect this.** The intuition is the Law of Large Numbers turned
quantitative. For $S_n = \frac{1}{n}\sum_{i=1}^n X_i$ with i.i.d. bounded $X_i$, the variance
of $S_n$ is $\sigma^2 / n$, so the standard deviation is $O(1/\sqrt n)$ — much smaller than
the range of an individual $X_i$. The CLT says the *shape* of the fluctuations is Gaussian
in the limit; concentration inequalities give *non-asymptotic* Gaussian-like tails for finite
$n$. The phenomenon extends beyond sums to any function of $X_1,\dots,X_n$ that depends only
mildly on each coordinate (this is the content of McDiarmid's inequality).

**Concrete example.** Toss a fair coin $n$ times and let $S_n$ be the number of heads.
Markov's inequality on $|S_n - n/2|$ gives no useful bound. Chebyshev's inequality, using
$\mathrm{Var}(S_n) = n/4$, gives
$\Pr(|S_n - n/2|\ge t\sqrt n) \le 1/(4t^2)$ — polynomial decay only. Hoeffding's inequality
(proved below) gives the much sharper
$\Pr(|S_n - n/2|\ge t\sqrt n) \le 2\exp(-2 t^2)$ — exponential in $t^2$. For $n=10000$ and
$t=3$, Chebyshev says "$\le 0.028$"; Hoeffding says "$\le 2.5\cdot 10^{-8}$". This gap is
typical and is why concentration inequalities are the right tool for learning theory:
generalization guarantees need failure probability $\delta \to 0$, not just $\delta \le 0.5$.

The intuition behind concentration is *averaging cancels independent noise.* Independence
prevents the deviations from one coordinate piling up systematically with the deviations
from another; bounded influence of each coordinate prevents any single coordinate from
dominating; together, they force the whole quantity to look like its mean.

## A.2 The common technique: the MGF / Chernoff method

The proofs of Hoeffding, Bernstein, and (with a martingale twist) McDiarmid all share one
backbone: **bound the moment generating function, then optimize via Chernoff.**

### A.2.1 The Chernoff template

Let $Z$ be any real random variable and $\lambda > 0$. By Markov's inequality applied to
the non-negative random variable $e^{\lambda Z}$,
$$
\Pr(Z \ge t)
= \Pr\bigl(e^{\lambda Z} \ge e^{\lambda t}\bigr)
\;\le\; e^{-\lambda t}\,\mathbb{E} e^{\lambda Z}.
\tag{Chernoff}
$$
Optimizing over $\lambda > 0$,
$$
\Pr(Z \ge t) \;\le\; \exp\!\Bigl(-\sup_{\lambda > 0}\bigl[\lambda t - \log \mathbb{E} e^{\lambda Z}\bigr]\Bigr).
$$
The function $\psi_Z(\lambda) := \log \mathbb{E} e^{\lambda Z}$ is the *cumulant generating
function* (CGF), and the supremum above is the Legendre dual $\psi_Z^*(t)$.

**The job, then, is to upper bound $\psi_Z(\lambda)$.** The bigger your upper bound on
$\psi_Z$, the smaller the dual $\psi_Z^*$, and the worse the concentration. For sums of
independent variables this is easy: independence converts the MGF of a sum into a product,
hence the CGF of a sum into a sum of CGFs:
$$
Z = \sum_{i=1}^n X_i \;\implies\; \psi_Z(\lambda) = \sum_{i=1}^n \psi_{X_i}(\lambda).
$$
So we only need to bound the CGF of each individual $X_i$. Two standard routes:

- **Hoeffding's lemma**: bounded random variables have $\psi_X(\lambda) \le \lambda^2(b-a)^2/8$.
  This gives sub-Gaussian tails depending only on the *range* of $X$.
- **Bernstein's lemma**: variance-aware bound that yields tighter tails when
  $\mathrm{Var}(X) \ll (b-a)^2$.

### A.2.2 The bounded-differences variant (preview of McDiarmid)

For functions $Z = f(X_1,\dots,X_n)$ that are not literal sums, independence still helps,
but we need a martingale decomposition. Let $\mathcal{F}_k = \sigma(X_1,\dots,X_k)$ and
$D_k := \mathbb{E}[Z\mid\mathcal{F}_k] - \mathbb{E}[Z\mid\mathcal{F}_{k-1}]$. Then
$$
Z - \mathbb{E} Z = \sum_{k=1}^n D_k,
$$
and $(D_k)$ is a martingale difference sequence. If we can bound the conditional MGF of
each $D_k$ by a sub-Gaussian term, the same Chernoff machinery goes through. Section A.4.3
makes this precise.

## A.3 Statements, assumptions, and consequences

In all four statements, $X_1, \dots, X_n$ are independent (with one exception, noted) and
$t > 0$.

### A.3.1 Hoeffding's inequality

**Theorem (Hoeffding, 1963).** Let $X_1,\dots,X_n$ be independent with $X_i \in [a_i, b_i]$
almost surely. Let $S = \sum_{i=1}^n X_i$. Then
$$
\Pr\!\bigl(S - \mathbb{E} S \ge t\bigr)\;\le\;\exp\!\Bigl(-\tfrac{2 t^2}{\sum_{i=1}^n (b_i-a_i)^2}\Bigr),
$$
and the same bound for the lower tail; a union bound gives the two-sided version with a
factor of 2. *Assumption:* boundedness and independence. No assumption on means or variances.

For the i.i.d. mean $\bar X = \frac{1}{n}\sum X_i$ with $X_i \in [a,b]$:
$$
\Pr\!\bigl(|\bar X - \mathbb{E} \bar X| \ge \varepsilon\bigr)
\;\le\;2 \exp\!\Bigl(-\tfrac{2 n \varepsilon^2}{(b-a)^2}\Bigr).
$$

### A.3.2 Hoeffding's inequality for sampling without replacement

**Theorem (Hoeffding, 1963; Serfling, 1974).** Let $\mathcal{C} = \{c_1,\dots,c_N\}\subset[a,b]$
be a finite population with mean $\mu = \frac1N\sum c_i$. Draw $X_1,\dots,X_n$ uniformly
*without replacement* from $\mathcal{C}$, $n\le N$. Then
$$
\Pr\!\Bigl(\tfrac{1}{n}\sum_{i=1}^n X_i - \mu \ge \varepsilon\Bigr)
\;\le\;\exp\!\Bigl(-\tfrac{2 n \varepsilon^2}{(b-a)^2}\Bigr).
$$
*Assumption:* uniform sampling without replacement from a bounded population. **No
independence**: the $X_i$ are exchangeable but dependent. Strikingly, the bound is
*at least as good* as the with-replacement Hoeffding bound — sampling without replacement
concentrates *more*, because exhausting the population reduces variability. This is what
the Week 3 proof needs at the symmetrization step (a ghost sample is drawn without
replacement from a fixed pool).

### A.3.3 McDiarmid's inequality (bounded differences)

**Theorem (McDiarmid, 1989).** Let $X_1,\dots,X_n$ be independent random variables on
spaces $\mathcal{X}_1,\dots,\mathcal{X}_n$, and let $f:\prod\mathcal{X}_i\to\mathbb{R}$
satisfy the *bounded-differences* property: there exist constants $c_1,\dots,c_n\ge 0$ such that
for every $i$ and every $x_1,\dots,x_n,x_i'$,
$$
\bigl|f(x_1,\dots,x_i,\dots,x_n) - f(x_1,\dots,x_i',\dots,x_n)\bigr|\;\le\;c_i.
$$
Then
$$
\Pr\!\bigl(f(X) - \mathbb{E} f(X) \ge t\bigr)\;\le\;\exp\!\Bigl(-\tfrac{2 t^2}{\sum_{i=1}^n c_i^2}\Bigr).
$$

*Assumption:* independence + bounded coordinate-wise influence. No structural assumption on
$f$ (no convexity, no Lipschitz in any norm beyond the discrete bounded-differences
condition). When $f(x) = \sum_i x_i / n$ and $x_i\in[a,b]$, $c_i = (b-a)/n$, and we recover
Hoeffding (up to the factor of $n$ in the rescaling). McDiarmid's strength is that it
applies to any bounded-influence function; in learning theory, this is what controls the
uniform deviation $\sup_{h\in\mathcal{H}}\lvert L_\mathcal{D}(h) - L_n(h)\rvert$.

### A.3.4 Bernstein's inequality

**Theorem (Bernstein).** Let $X_1,\dots,X_n$ be independent with $\mathbb{E} X_i = 0$,
$|X_i|\le M$ a.s., and $\sum_i \mathbb{E} X_i^2 \le v$. Then for all $t\ge 0$,
$$
\Pr\!\Bigl(\sum_{i=1}^n X_i \ge t\Bigr)
\;\le\;\exp\!\Bigl(-\tfrac{t^2}{2(v + Mt/3)}\Bigr).
$$
Equivalently, with probability at least $1-\delta$,
$$
\sum X_i \le \sqrt{2 v \log(1/\delta)} + \tfrac{2M}{3}\log(1/\delta).
$$

*Assumption:* independence, boundedness, and a variance bound $v$. **What Bernstein
exploits beyond Hoeffding:** the *variance* of each $X_i$, not just its range. When
$\mathrm{Var}(X_i)$ is much smaller than $M^2$ (rare events, low-probability indicators,
Bernoulli with $p$ small), the bound is dramatically sharper: in the small-deviation regime
$t \ll v/M$ Bernstein gives Gaussian tails with the *true* variance proxy $v$ rather than
the loose proxy $nM^2$ that Hoeffding uses.

### A.3.5 Side-by-side comparison

| Inequality | Quantity | Assumption | Tail at level $t$ |
|---|---|---|---|
| Hoeffding | $\sum (X_i-\mathbb{E} X_i)$, indep. | $X_i\in[a_i,b_i]$ | $\exp(-2 t^2/\sum (b_i-a_i)^2)$ |
| Hoeffding (w/o replacement) | $\sum X_i - n\mu$ from finite pop. | $c_i\in[a,b]$, sampled w/o repl. | $\exp(-2 t^2/(n(b-a)^2))$ |
| McDiarmid | $f(X)-\mathbb{E} f(X)$ | indep. + bdd. diffs. $c_i$ | $\exp(-2 t^2/\sum c_i^2)$ |
| Bernstein | $\sum X_i$, indep., zero-mean | $|X_i|\le M$, var $\le v$ | $\exp(-t^2/(2v + 2Mt/3))$ |

The first three are *purely sub-Gaussian*: their exponent is quadratic in $t$ with a scale
that uses only ranges/diameters. Bernstein is *sub-exponential beyond a threshold*: in the
small-$t$ regime it beats Hoeffding by replacing $\sum(b_i-a_i)^2/4$ with the typically much
smaller $v$; in the large-$t$ regime ($t\gtrsim v/M$) it transitions to a slower
$\exp(-3t/(2M))$ tail, which is the price for the variance-aware constant.

## A.4 Proofs

### A.4.1 Hoeffding's lemma and Hoeffding's inequality

**Lemma (Hoeffding's lemma).** If $X\in[a,b]$ a.s. and $\mathbb{E} X = 0$, then for all
$\lambda\in\mathbb{R}$,
$$
\mathbb{E} e^{\lambda X}\;\le\;\exp\!\Bigl(\tfrac{\lambda^2 (b-a)^2}{8}\Bigr).
$$

*Proof.* By convexity of $x\mapsto e^{\lambda x}$, for $x\in[a,b]$,
$$
e^{\lambda x} \le \tfrac{b-x}{b-a} e^{\lambda a} + \tfrac{x-a}{b-a} e^{\lambda b}.
$$
Taking expectations and using $\mathbb{E} X = 0$,
$$
\mathbb{E} e^{\lambda X} \le \tfrac{b}{b-a} e^{\lambda a} - \tfrac{a}{b-a} e^{\lambda b}
= e^{\phi(\lambda)},
$$
where, setting $p = -a/(b-a)\in[0,1]$ and $u = \lambda(b-a)$,
$$
\phi(\lambda) = -p u + \log\!\bigl(1-p+p e^{u}\bigr).
$$
Direct computation gives $\phi(0)=\phi'(0)=0$ and
$\phi''(u) = \frac{p(1-p) e^{u}}{(1-p+p e^{u})^2}\le\frac14$ (since the function
$q(1-q)$ with $q = p e^u/(1-p+p e^u)\in[0,1]$ is at most $1/4$). Taylor's theorem gives
$\phi(\lambda)\le \lambda^2(b-a)^2/8$. $\square$

**Hoeffding's inequality (proof).** WLOG centering each $X_i$ (replace $X_i$ by $X_i-\mathbb{E} X_i\in[a_i-\mathbb{E} X_i,b_i-\mathbb{E} X_i]$, an interval of length $b_i-a_i$). Let
$Z = \sum (X_i-\mathbb{E} X_i)$. By independence and Hoeffding's lemma,
$$
\mathbb{E} e^{\lambda Z} = \prod_i \mathbb{E} e^{\lambda(X_i-\mathbb{E} X_i)}
\le \prod_i e^{\lambda^2 (b_i-a_i)^2/8}
= e^{\lambda^2 V / 8}, \quad V:=\sum (b_i-a_i)^2.
$$
By Chernoff, $\Pr(Z\ge t)\le \exp(-\lambda t + \lambda^2 V/8)$, minimized at
$\lambda^\star = 4t/V$, giving $\exp(-2t^2/V)$. $\square$

### A.4.2 Hoeffding without replacement

We prove the result via Hoeffding's elegant *coupling reduction* to the i.i.d. case:
sampling without replacement is dominated, in the convex order on partial sums, by
sampling with replacement.

**Lemma (Hoeffding 1963, Theorem 4).** Let $\mathcal{C}=\{c_1,\dots,c_N\}\subset[a,b]$,
$\mu = \frac1N\sum c_i$. Let $X_1,\dots,X_n$ be a uniform sample *without* replacement from
$\mathcal{C}$, and $Y_1,\dots,Y_n$ a uniform sample *with* replacement. Then for any
continuous convex $\varphi:\mathbb{R}\to\mathbb{R}$,
$$
\mathbb{E}\,\varphi\!\Bigl(\sum_{i=1}^n X_i\Bigr)
\;\le\;\mathbb{E}\,\varphi\!\Bigl(\sum_{i=1}^n Y_i\Bigr).
$$

*Proof sketch (the key idea).* Condition on the unordered set
$T = \{X_1,\dots,X_n\}$; then $\sum X_i = \sum_{c\in T} c$ is determined. Conditional on the
*multiset* $T_Y = \{Y_1,\dots,Y_n\}$, the same is true. A direct combinatorial argument
shows that the distribution of $\sum X_i$ is a *mixture of permutations* of size-$n$
subsets, while $\sum Y_i$ is a richer mixture also including multisets with repeats; the
multiset distribution majorizes the set distribution in the convex order. (Hoeffding 1963,
Theorem 4; the modern slick proof is via a double-stochastic representation, see
Boucheron–Lugosi–Massart 2013, §6.1.) $\square$

Taking $\varphi(s) = e^{\lambda(s - n\mu)}$ (convex), the lemma gives
$$
\mathbb{E} e^{\lambda(\sum X_i - n\mu)} \le \mathbb{E} e^{\lambda(\sum Y_i - n\mu)}
\le e^{\lambda^2 n(b-a)^2/8}
$$
by the standard Hoeffding lemma applied to the i.i.d. variables $Y_i$. Then Chernoff gives
the same bound as the i.i.d. case:
$$
\Pr\!\Bigl(\tfrac1n\sum X_i - \mu \ge \varepsilon\Bigr)\le e^{-2 n \varepsilon^2 / (b-a)^2}. \qquad\square
$$

(Serfling 1974 sharpens this with a $1 - (n-1)/N$ "finite-population correction" factor; we
do not need that strengthening for the ERM proof.)

### A.4.3 McDiarmid via the martingale method

Fix $f$ with bounded differences $c_1,\dots,c_n$. Let $\mathcal{F}_k = \sigma(X_1,\dots,X_k)$,
$\mathcal{F}_0 = \{\emptyset, \Omega\}$, and define the Doob martingale
$$
M_k := \mathbb{E}[f(X)\mid\mathcal{F}_k], \qquad D_k := M_k - M_{k-1}.
$$
Then $f(X) - \mathbb{E} f(X) = \sum_{k=1}^n D_k$, and $(D_k)$ is a martingale difference
sequence.

**Key bound on each $D_k$.** Conditional on $\mathcal{F}_{k-1}$, define for $x\in\mathcal{X}_k$,
$$
g(x) := \mathbb{E}[f(X) \mid X_1,\dots,X_{k-1}, X_k = x].
$$
Then $D_k = g(X_k) - \mathbb{E}_{X_k} g(X_k)$ (where the expectation is over $X_k$,
holding $\mathcal{F}_{k-1}$ fixed; this uses independence of $X_k$ from $\mathcal{F}_{k-1}$).
By the bounded-differences property, swapping the $k$-th coordinate changes $f$ by at most
$c_k$, so by averaging over $X_{k+1},\dots,X_n$, we have
$\sup g - \inf g \le c_k$. In particular, $D_k$ conditional on $\mathcal{F}_{k-1}$ is a
zero-mean random variable supported in an interval of length $\le c_k$.

**Conditional Hoeffding lemma.** Apply Hoeffding's lemma to $D_k\mid\mathcal{F}_{k-1}$:
$$
\mathbb{E}[e^{\lambda D_k}\mid\mathcal{F}_{k-1}]\;\le\;e^{\lambda^2 c_k^2 / 8}.
$$

**Telescoping the MGF.** By the tower property,
$$
\mathbb{E} e^{\lambda \sum_{k=1}^n D_k}
= \mathbb{E}\Bigl[e^{\lambda \sum_{k=1}^{n-1} D_k}\,\mathbb{E}[e^{\lambda D_n}\mid\mathcal{F}_{n-1}]\Bigr]
\le e^{\lambda^2 c_n^2/8}\,\mathbb{E} e^{\lambda \sum_{k=1}^{n-1} D_k}.
$$
Iterating: $\mathbb{E} e^{\lambda(f - \mathbb{E} f)} \le \exp\!\bigl(\lambda^2 \sum c_k^2 / 8\bigr)$.
Chernoff with $\lambda^\star = 4t/\sum c_k^2$ gives the McDiarmid bound. $\square$

### A.4.4 Bernstein's inequality

**Lemma (Bernstein's MGF bound).** If $X$ is a real random variable with $\mathbb{E} X = 0$,
$|X|\le M$ a.s., and $\mathbb{E} X^2 \le \sigma^2$, then for any $\lambda \in (0, 3/M)$,
$$
\mathbb{E} e^{\lambda X}\;\le\;\exp\!\Bigl(\tfrac{\lambda^2 \sigma^2 / 2}{1 - \lambda M / 3}\Bigr).
$$

*Proof.* Expand
$$
e^{\lambda X} = 1 + \lambda X + \sum_{k\ge 2}\tfrac{\lambda^k X^k}{k!}.
$$
Take expectation; the linear term vanishes. For $k\ge 2$, $|X^k|\le M^{k-2} X^2$, so
$\mathbb{E} X^k \le M^{k-2}\sigma^2$. Hence
$$
\mathbb{E} e^{\lambda X}
\le 1 + \sigma^2 \sum_{k\ge 2}\tfrac{\lambda^k M^{k-2}}{k!}
= 1 + \tfrac{\sigma^2}{M^2}\bigl(e^{\lambda M} - 1 - \lambda M\bigr).
$$
Using $\sum_{k\ge 2} u^k / k! \le \frac{u^2/2}{1 - u/3}$ for $u\in[0,3)$ (an elementary
calculus estimate: $k!\ge 2\cdot 3^{k-2}$ for $k\ge 2$),
$$
\tfrac{\sigma^2}{M^2}(e^{\lambda M} - 1 - \lambda M)
\le \tfrac{\sigma^2 \lambda^2 / 2}{1 - \lambda M / 3}.
$$
Apply $1 + u\le e^u$. $\square$

**Bernstein's inequality (proof).** With $X_i$ as in the theorem and
$Z = \sum X_i$, by independence and the lemma,
$$
\log \mathbb{E} e^{\lambda Z} \le \tfrac{\lambda^2 v / 2}{1 - \lambda M/3}, \qquad \lambda\in(0,3/M).
$$
Chernoff: $\Pr(Z\ge t)\le \exp\!\bigl(-\lambda t + \tfrac{\lambda^2 v/2}{1-\lambda M/3}\bigr)$.
The optimal $\lambda^\star = t/(v + Mt/3)$ lies in $(0, 3/M)$ and yields
$\exp(-t^2/(2v + 2Mt/3))$. $\square$

### A.4.5 The unifying template

Three of the four proofs follow the *same* three-step recipe:

1. **Bound a single-variable CGF**: $\psi_X(\lambda) \le \rho(\lambda)$ for some explicit $\rho$.
2. **Tensorize** by independence (or, for McDiarmid, by a martingale tower) to get
   $\psi_Z(\lambda) \le \sum_i \rho_i(\lambda)$.
3. **Optimize** via Chernoff: $\Pr(Z\ge t) \le \exp(-\sup_\lambda[\lambda t - \sum\rho_i(\lambda)])$.

The four inequalities differ only in step 1: Hoeffding uses range, Bernstein uses range +
variance, McDiarmid uses bounded differences (after a martingale step), and Hoeffding w/o
replacement reduces to the i.i.d. case via convex domination. This makes the four results
not four separate facts but four instantiations of *one* method — control the MGF, then
Chernoff.

```
                  Chernoff / Markov on exp(lambda * Z)
                              |
        +---------------------+--------------------+
        |                                          |
   sum of indep. X_i                          f(X), bdd. diffs.
        |                                          |
        +-- range only      --> Hoeffding lemma --> Hoeffding
        +-- + variance      --> Bernstein lemma --> Bernstein
        +-- w/o replacement --> convex domination --> Hoeffding-WoR
                                                    |
                       Doob martingale + cond. Hoeffding --> McDiarmid
```

## A.5 Connection to the Week 3 ERM proof

We now glue these inequalities together to prove the Week 3 i.i.d. ERM guarantee. Let
$\mathcal{H}$ be a hypothesis class with growth function $\Gamma_\mathcal{H}$, $0$-$1$ loss
$\ell(h, (x,y)) = \mathbf{1}[h(x)\ne y]\in[0,1]$, $\mathcal{D}$ a distribution,
$L_\mathcal{D}(h) = \mathbb{E}_{(x,y)\sim\mathcal{D}}\ell(h,(x,y))$,
$L_n(h) = \frac1n\sum_i \ell(h, (X_i,Y_i))$, and $\hat h\in\arg\min_h L_n(h)$.

**Goal.** With probability at least $1-\delta$ over $S\sim\mathcal{D}^n$,
$$
L_\mathcal{D}(\hat h) \le \inf_{h\in\mathcal{H}} L_\mathcal{D}(h)
+ O\!\left(\sqrt{\tfrac{\log\Gamma_\mathcal{H}(2n) + \log(1/\delta)}{n}}\right).
$$

The argument has four steps; each invokes one of our concentration tools.

**Step 1 (Reduction to uniform deviation).** Fix any $h^\star \in\arg\min_h L_\mathcal{D}(h)$.
By optimality of $\hat h$ on $L_n$,
$$
L_\mathcal{D}(\hat h) - L_\mathcal{D}(h^\star)
= \bigl[L_\mathcal{D}(\hat h) - L_n(\hat h)\bigr] + \bigl[L_n(\hat h) - L_n(h^\star)\bigr] + \bigl[L_n(h^\star) - L_\mathcal{D}(h^\star)\bigr].
$$
The middle bracket is $\le 0$. The third bracket is, by *Hoeffding* applied to the i.i.d.
bounded losses $\ell(h^\star, (X_i,Y_i))\in[0,1]$,
$\le \sqrt{\log(1/\delta) / (2n)}$ with prob. $\ge 1-\delta/2$. The first bracket is at
most $\Phi(S) := \sup_{h\in\mathcal{H}}\bigl(L_\mathcal{D}(h) - L_n(h)\bigr)$. So we need
to bound $\Phi$ in high probability.

**Step 2 (Concentration of $\Phi$ around its mean — McDiarmid).** Replacing one sample
$(X_i, Y_i)$ changes any $L_n(h)$ by at most $1/n$ (since losses lie in $[0,1]$), hence
$\Phi$ changes by at most $1/n$. McDiarmid with $c_i = 1/n$ gives
$$
\Pr\!\bigl(\Phi - \mathbb{E}\Phi \ge \varepsilon\bigr)
\le \exp(-2n\varepsilon^2),
$$
so with probability $\ge 1-\delta/2$, $\Phi \le \mathbb{E}\Phi + \sqrt{\log(2/\delta)/(2n)}$.

**Step 3 (Symmetrization — ghost sample, no independence needed for the ghost).** Let
$S' = (X_i', Y_i')_{i=1}^n$ be an independent ghost sample $\sim\mathcal{D}^n$. By Jensen,
$$
\mathbb{E}\Phi(S) = \mathbb{E}_S\sup_h\bigl(\mathbb{E}_{S'} L_n'(h) - L_n(h)\bigr)
\le \mathbb{E}_{S,S'}\sup_h\bigl(L_n'(h) - L_n(h)\bigr).
$$
Letting $\sigma_i\in\{\pm1\}$ be i.i.d. Rademacher and using that swapping
$(X_i,Y_i)\leftrightarrow(X_i',Y_i')$ preserves the distribution of the joint sample,
$$
\mathbb{E}\Phi(S) \le \mathbb{E}_{S,S',\sigma}\sup_{h\in\mathcal{H}}\tfrac1n\sum_{i=1}^n \sigma_i\bigl(\ell(h, Z_i') - \ell(h, Z_i)\bigr),
$$
where $Z_i = (X_i,Y_i)$.

**Step 4 (Massart's finite class lemma — Hoeffding on the loss vector).** Condition on
$S\cup S'$; this is a fixed pool of $2n$ points. As $h$ ranges over $\mathcal{H}$, the
restriction of $h$ to this pool takes at most $\Gamma_\mathcal{H}(2n)$ distinct values. So
the sup ranges over a set of at most $\Gamma_\mathcal{H}(2n)$ vectors $u^{(h)}\in[-1,1]^{2n}$.
For each fixed $u$, $\langle\sigma, u\rangle$ is a sum of $2n$ independent bounded variables;
by Hoeffding's lemma it is sub-Gaussian with parameter $\|u\|_2^2\le 2n$. Massart's lemma
(a standard consequence: max of $N$ sub-Gaussians is $\le\sqrt{2 v\log N}$) gives
$$
\mathbb{E}_\sigma \sup_h \tfrac1n\langle\sigma, u^{(h)}\rangle
\le \tfrac1n\sqrt{2\cdot 2n\cdot \log\Gamma_\mathcal{H}(2n)}
= 2\sqrt{\tfrac{\log\Gamma_\mathcal{H}(2n)}{n}}.
$$
Taking outer expectation, $\mathbb{E}\Phi(S)\le 2\sqrt{\log\Gamma_\mathcal{H}(2n)/n}$.

*(Why the without-replacement Hoeffding shows up.)* The "permutation" form of
symmetrization fixes the $2n$-pool $S\cup S'$ and resamples a size-$n$ subset uniformly
without replacement from it; the deviation of $L_n$ from the pool average is then a
without-replacement quantity, controlled by the WoR Hoeffding inequality of A.3.2. Either
form of symmetrization works; we use the Rademacher version above for definiteness, but
the WoR Hoeffding inequality is the natural tool if one writes the symmetrization as a
permutation argument (as in Vapnik–Chervonenkis 1971).

**Combining.** With probability $\ge 1-\delta$:
$$
L_\mathcal{D}(\hat h) - L_\mathcal{D}(h^\star)
\le \underbrace{2\sqrt{\tfrac{\log\Gamma_\mathcal{H}(2n)}{n}}}_{\mathbb{E}\Phi}
+ \underbrace{\sqrt{\tfrac{\log(2/\delta)}{2n}}}_{\Phi-\mathbb{E}\Phi}
+ \underbrace{\sqrt{\tfrac{\log(2/\delta)}{2n}}}_{L_n(h^\star)-L_\mathcal{D}(h^\star)}.
$$
This is exactly the bound stated:
$$
L_\mathcal{D}(\hat h)\le \inf_h L_\mathcal{D}(h) + O\!\left(\sqrt{\tfrac{\log\Gamma_\mathcal{H}(2n) + \log(1/\delta)}{n}}\right). \qquad\square
$$

**Bernstein's role.** Bernstein is not needed for this growth-function bound, but it is the
tool of choice for *fast-rate* refinements: when $L_\mathcal{D}(h^\star)$ is small (the
realizable / low-noise regime), the variance of $\ell(h, Z) - \ell(h^\star, Z)$ scales with
$L_\mathcal{D}(h)$ rather than with $1$, and Bernstein converts this into an
$O(1/n)$-type rate instead of $O(1/\sqrt n)$. We include it in the mini-course because every
serious learning-theory proof eventually needs it.

## A.6 References

1. W. Hoeffding. *Probability inequalities for sums of bounded random variables.* JASA 58
   (1963), 13–30. [Hoeffding's lemma, Theorems 1, 2, 4 — the with- and without-replacement
   inequalities.]
2. C. McDiarmid. *On the method of bounded differences.* In *Surveys in Combinatorics*, LMS
   Lecture Note Series 141, 1989, 148–188. [Theorem 3.1.]
3. S. Bernstein. *On a modification of Chebyshev's inequality and on the error in Laplace's
   formula.* (Original 1924; see Bennett 1962, or Boucheron–Lugosi–Massart §2.8.)
4. R. Serfling. *Probability inequalities for the sum in sampling without replacement.*
   Annals of Statistics 2 (1974), 39–48.
5. S. Boucheron, G. Lugosi, P. Massart. *Concentration Inequalities: A Nonasymptotic Theory
   of Independence.* Oxford UP, 2013. [Chapters 2, 3, 6 — the canonical modern reference.]
6. V. Vapnik, A. Chervonenkis. *On the uniform convergence of relative frequencies of events
   to their probabilities.* Theory Prob. Appl. 16 (1971), 264–280. [Original symmetrization
   + growth-function ERM bound.]
7. S. Shalev-Shwartz, S. Ben-David. *Understanding Machine Learning: From Theory to
   Algorithms.* Cambridge UP, 2014. [Chapters 4, 6, 28 — textbook proofs of Hoeffding,
   McDiarmid, the growth-function ERM bound, and the No-Free-Lunch theorem.]
8. M. Anthony, P. Bartlett. *Neural Network Learning: Theoretical Foundations.* Cambridge UP,
   1999. [Chapter 4 — symmetrization with ghost samples.]

---

# Part B — The No-Free-Lunch Theorem and the Fundamental Theorem

## B.1 Proof of the Week 3 NFL theorem

**Theorem (NFL, restated).** Let $A$ be any (possibly randomized) learning algorithm for
binary classification under the $0$-$1$ loss over a domain $\mathcal{X}$, and let $n$ be
any integer with $n < |\mathcal{X}|/2$. Then there exists a distribution $\mathcal{D}$ on
$\mathcal{X}\times\{0,1\}$ such that
(i) some $f^\star:\mathcal{X}\to\{0,1\}$ has $L_\mathcal{D}(f^\star) = 0$, and
(ii) $\Pr_{S\sim\mathcal{D}^n}\bigl(L_\mathcal{D}(A(S))\ge 1/8\bigr)\ge 1/7$.

**Quantifier reading.** The algorithm $A$ is given first (universal); the *adversary*
chooses both $\mathcal{D}$ and $f^\star$ second, knowing $A$. Inside the conclusion, $S$ is
random. So NFL is a *worst-case-over-the-distribution* statement — the adversary is
oblivious to $S$ but adaptive to $A$.

**Proof.** Fix a subset $C\subseteq\mathcal{X}$ with $|C| = 2n$ (possible since $|X|>2n$).
We will only consider distributions supported on $C\times\{0,1\}$ that are deterministic in
the label, i.e. of the form $\mathcal{D}_f$: $X\sim$ Uniform($C$) and $Y = f(X)$ for some
$f:C\to\{0,1\}$. Under $\mathcal{D}_f$ the realizability assumption (i) holds with $f^\star$
any extension of $f$ to $\mathcal{X}$, so it suffices to show that there exists such an $f$
making $A$ fail.

Let $\mathcal{F} = \{0,1\}^C$ (all $2^{2n}$ labelings of $C$). The averaging argument shows
that *expected* loss over a *uniform* choice of $f\in\mathcal{F}$ is at least $1/4$.

**Step 1 (Averaging over labelings).** Fix any $S = ((x_1,y_1),\dots,(x_n,y_n))\in(C\times\{0,1\})^n$
realizable by some $f\in\mathcal{F}$. Let $T = \{x_1,\dots,x_n\}$ (a multiset; we abuse
notation and let $|T|$ denote distinct elements). Set $C\setminus T \supseteq C \setminus
\{x_1,\dots,x_n\}$, which has cardinality $\ge 2n - n = n$. For any $f\in\mathcal{F}$,
$$
L_{\mathcal{D}_f}(A(S)) = \tfrac{1}{|C|}\sum_{x\in C} \mathbf{1}[A(S)(x)\ne f(x)]
\ge \tfrac{1}{2n}\sum_{x\in C\setminus T} \mathbf{1}[A(S)(x)\ne f(x)].
$$
Now do the averaging over a *random labeling* $f$ uniform on $\mathcal{F}$ — but only of
points in $C\setminus T$. The hypothesis $A(S)$ depends on $S$, hence on
$\{f(x_1),\dots,f(x_n)\}$, but is *independent* of $\{f(x): x\in C\setminus T\}$ when those
labels are drawn fresh and uniform. So for each $x\in C\setminus T$,
$\Pr_f[A(S)(x)\ne f(x)\mid S] = 1/2$ exactly. Therefore
$$
\mathbb{E}_f\!\left[\,L_{\mathcal{D}_f}(A(S))\,\big|\, S\right]
\ge \tfrac{1}{2n}\cdot |C\setminus T|\cdot \tfrac12 \ge \tfrac{1}{2n}\cdot n\cdot \tfrac12 = \tfrac14.
$$

For the averaging to make sense across both random $S$ and random $f$, we use the *coupled*
distribution: draw $f\sim$ Uniform($\mathcal{F}$), then $S\sim\mathcal{D}_f^n$. The above
inequality, taken in expectation over $S$, gives
$$
\mathbb{E}_f \mathbb{E}_{S\sim\mathcal{D}_f^n}\!\left[L_{\mathcal{D}_f}(A(S))\right] \ge \tfrac14.
$$
(Strictly: the inequality $\ge 1/4$ holds for every $S$, not just on average, so it holds in
expectation over $S$ pointwise in $f$, and then in expectation over $f$.)

**Step 2 (Probabilistic method — extract one bad $f$).** By averaging,
$$
\exists\, f^\star\in\mathcal{F}\text{ s.t. } \mathbb{E}_{S\sim\mathcal{D}_{f^\star}^n}\!\left[L_{\mathcal{D}_{f^\star}}(A(S))\right]\ge \tfrac14.
$$

**Step 3 (Markov in reverse).** Let $W := L_{\mathcal{D}_{f^\star}}(A(S))\in[0,1]$, with
$\mathbb{E} W \ge 1/4$. For any $a\in[0,1)$,
$$
\mathbb{E} W \le a\cdot\Pr(W < a) + 1\cdot\Pr(W\ge a) = a + (1-a)\Pr(W\ge a),
$$
i.e. $\Pr(W\ge a)\ge (\mathbb{E} W - a)/(1-a)$. Set $a = 1/8$: $\Pr(W\ge 1/8)\ge (1/4 - 1/8)/(7/8) = 1/7$. $\square$

## B.2 Application: closing the Fundamental Theorem

**Corollary (lower-bound direction).** If $\mathrm{VCdim}(\mathcal{H}) = \infty$, then
$\mathcal{H}$ is *not* PAC learnable.

*Proof.* Suppose $\mathcal{H}$ were PAC learnable, witnessed by $A$ and a sample-complexity
function $m_\mathcal{H}(\varepsilon,\delta)$: for every $\mathcal{D}$ realizable by
$\mathcal{H}$, with $n\ge m_\mathcal{H}(\varepsilon,\delta)$, $L_\mathcal{D}(A(S))\le\varepsilon$
w.p. $\ge 1-\delta$. Set $\varepsilon = 1/8$, $\delta = 1/7$, and let $n_0 := m_\mathcal{H}(1/8, 1/7)$.

Since $\mathrm{VCdim}(\mathcal{H}) = \infty$, $\mathcal{H}$ shatters some set $C$ of size
$|C| > 2n_0$. NFL on the domain $C$ produces a labeling $f^\star\in\{0,1\}^C$ — but because
$C$ is shattered, $f^\star$ is realized by some $h\in\mathcal{H}$, so the constructed
distribution is realizable by $\mathcal{H}$. NFL says $\Pr(L_\mathcal{D}(A(S))\ge 1/8)\ge 1/7$,
contradicting PAC learnability with these parameters. $\square$

**Concrete instance: the class of all finite subsets of $\mathbb{R}$.** Let
$\mathcal{H} = \{\mathbf{1}_F : F\subset\mathbb{R}\text{ finite}\}$.

*Claim.* $\mathrm{VCdim}(\mathcal{H}) = \infty$.

*Proof.* Pick any $n$ and any distinct points $x_1,\dots,x_n\in\mathbb{R}$. For any
$y\in\{0,1\}^n$, take $F = \{x_i: y_i=1\}$ — a finite set, hence in $\mathcal{H}$, that
realizes $y$. So every finite subset of $\mathbb{R}$ is shattered, and the VC dimension is
unbounded. $\square$

*Application of the corollary.* By the corollary, $\mathcal{H}$ is not PAC learnable. We
can also see this directly via NFL: for any $A$ and any $n$, choose $C = \{x_1,\dots,x_{2n}\}\subset\mathbb{R}$
with $|C| = 2n$. Every $f:C\to\{0,1\}$ is realized by some finite-subset hypothesis, so the
NFL distribution is in $\mathcal{H}$'s realizable family, and the NFL conclusion applies.

## B.3 Worked construction

**Setup.** Domain $\mathcal{X} = \{1,2,\dots,2n\}$ for $n = 5$ (so $|\mathcal{X}|=10>2n$ —
note: this requires $|\mathcal{X}|/2 > n$, here $5\not<5$, so I take $n=4$, $|\mathcal{X}|=10$).
Re-fix: $n=4$, $C = \mathcal{X} = \{1,\dots,10\}$, sample size $n=4 < 5 = |\mathcal{X}|/2$.

**Learner $A$.** *Constant-0* memorizer: $A(S)$ outputs the function $h_S$ defined by
$h_S(x) = y_i$ if $x = x_i$ for some seen $(x_i, y_i)\in S$, else $h_S(x) = 0$.

**Adversary's distribution.** Take $\mathcal{D}_{f^\star}$: $X\sim$ Uniform($\{1,\dots,10\}$),
$Y = f^\star(X)$, where $f^\star$ is the *all-ones* labeling: $f^\star\equiv 1$. Then
$f^\star\in\mathcal{H}_{\text{all funcs}}$ has $L_\mathcal{D}(f^\star) = 0$ (realizability holds).

**Calculating the failure probability.** With $S = ((X_1,1),\dots,(X_4,1))$, the seen set
$T = \{X_1,\dots,X_4\}\subseteq\{1,\dots,10\}$. The learner outputs $h_S$ which is $1$ on
$T$ and $0$ elsewhere. The population error is
$$
L_{\mathcal{D}_{f^\star}}(h_S) = \Pr_{X\sim\text{Unif}}[h_S(X)\ne 1] = \tfrac{|\{1,\dots,10\}\setminus T|}{10} = \tfrac{10 - |T|}{10}.
$$
Since the $X_i$ are i.i.d. uniform on a 10-point set,
$\mathbb{E}|T| = 10(1 - (9/10)^4) = 10(1 - 0.6561) = 3.439$, so
$\mathbb{E}[L_\mathcal{D}(h_S)] = (10-3.439)/10 = 0.6561$. In fact, with probability $1$ we
have $|T|\le 4$, so $L_\mathcal{D}(h_S)\ge 6/10 = 0.6\gg 1/8$ — *deterministically*.

So $A$ fails (loss $\ge 1/8$) with probability $1$, certainly $\ge 1/7$. $\square$

This concrete example illustrates the NFL mechanism: the learner has *no information* about
the $\ge n$ unseen points; whatever it outputs there can be flipped by the adversary's
choice of $f^\star$. Above, the adversary "flipped" all unseen labels to $1$ knowing the
learner defaults to $0$.

## B.4 Comparison: Week 1 NFL vs Week 3 NFL

| Feature | **Week 1 NFL (online / mistake-bound)** | **Week 3 NFL (statistical / PAC)** |
|---|---|---|
| Learning setting | Online learning over a finite domain $\mathcal{X}$, $|\mathcal{X}|=n$ | Statistical (PAC) learning, sample size $n$ |
| What the learner sees | An *adaptive* sequence of unlabeled queries $x_1,\dots,x_n$; predicts $\hat y_t$, then sees $f(x_t)$ | An i.i.d. sample $S\sim\mathcal{D}^n$ |
| Learner | Any deterministic online algorithm | Any (possibly randomized) batch algorithm |
| Adversary | **Adaptive**: chooses $(x_t, f(x_t))$ based on the learner's past predictions | **Oblivious**: fixes $\mathcal{D}$ and $f^\star$ before $S$ is drawn |
| Universal/existential | $\forall A$ deterministic, $\exists f, \exists$ ordering | $\forall A$, $\exists \mathcal{D}, f^\star$ |
| Conclusion | **Deterministic**: $A$ makes $n$ mistakes (i.e. all of them) | **Probabilistic**: $\Pr_S(L_\mathcal{D}\ge 1/8)\ge 1/7$ |
| Quantity controlled | Mistake count on a finite sequence | Population $0$-$1$ loss |
| Hypothesis class | Implicit: all functions $\mathcal{X}\to\{0,1\}$ | Implicit: same |
| Why it holds | At each step, the adversary picks $f(x_t)\ne\hat y_t$ — possible because both labels are still consistent with the past | At least $n$ of the $2n$ pool points are unseen; their labels are uniform random, so the learner is at chance there |

**What each version is telling us.**

- *Week 1* says: in the online, fully-adversarial, finite-domain setting, **no** algorithm
  beats trivial — even with no statistical noise, an adaptive teacher can force a mistake on
  every round. The lesson is that *online learning needs structural assumptions on the
  hypothesis class* (finite Littlestone dimension); without them, even a finite domain is
  hopeless.

- *Week 3* says: in the i.i.d. PAC setting, **no** algorithm beats trivial against a
  worst-case but oblivious distribution **when the hypothesis class is too rich**. The
  lesson is that *PAC learning needs structural assumptions on the hypothesis class*
  (finite VC dimension); without them, even with i.i.d. samples and a fixed-in-advance
  distribution, the learner cannot generalize to the unseen majority.

**Why both are called "No-Free-Lunch."** Both formalize the impossibility of
*assumption-free* learning: a learner that performs well on every problem (every labeling /
every distribution) cannot exist, because the universal quantification over targets gives
the adversary enough room to construct a counterexample tailored to $A$. The slogan "no
free lunch" is exactly: *you cannot learn without inductive bias.* The two versions differ
quantitatively (mistake counts vs population loss) and in the adversary's power (adaptive
sequencing vs distributional choice), but the *conceptual* message — without restrictions
on $\mathcal{H}$, learning is impossible — is the same. The PAC version is the one that
forces the introduction of VC dimension; the online version is the one that forces the
introduction of Littlestone dimension. Both versions thus motivate the central
combinatorial complexity measures of their respective theories.

## B.5 References

- Shalev-Shwartz & Ben-David, *Understanding Machine Learning*, §5 (No-Free-Lunch),
  §6 (Fundamental Theorem of PAC learning).
- Lecture notes for DSC 190/291, Weeks 1 and 3 (course material).
