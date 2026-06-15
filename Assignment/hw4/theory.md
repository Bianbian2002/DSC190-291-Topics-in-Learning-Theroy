# Assignment 4 — Write-up
**DSC 190/291 — Learning Theory**
**Student: Zeyu Bian**

---

# Part A — Sparse Linear Predictors and Model Selection

Throughout, $\mathcal{X} = \mathbb{R}^d$, $\mathcal{Y} = \{-1,+1\}$,
$\mathcal{H}_k = \{x\mapsto \mathrm{sign}(\langle w,x\rangle) : \|w\|_0\le k\}$,
$\mathcal{H} = \bigcup_{k=1}^d \mathcal{H}_k$, and $S\sim\mathcal{D}^n$.

## A.1 VC dimension through supports

For a fixed support $I\subseteq[d]$ with $|I|=k$, write
$$\mathcal{H}_I \;=\; \{x\mapsto\mathrm{sign}(\langle w,x\rangle) : \mathrm{supp}(w)\subseteq I\}.$$
The map $w\mapsto w|_I$ identifies $\mathcal{H}_I$ with the class of homogeneous halfspaces
in $\mathbb{R}^k$, applied to the coordinates of $x$ indexed by $I$. Homogeneous halfspaces
in $\mathbb{R}^k$ have VC dimension $k$, so by Sauer–Shelah
$$\Gamma_{\mathcal{H}_I}(n) \;\le\; \left(\tfrac{en}{k}\right)^{k}\qquad (n\ge k).$$
Since $\mathcal{H}_k = \bigcup_{|I|=k}\mathcal{H}_I$, a union bound on dichotomies gives
$$\Gamma_{\mathcal{H}_k}(n) \;\le\; \binom{d}{k}\left(\tfrac{en}{k}\right)^k
\;\le\; \left(\tfrac{ed}{k}\right)^{k}\!\left(\tfrac{en}{k}\right)^{k}
\;=\; \left(\tfrac{e^2 dn}{k^2}\right)^{k}.$$
If $\mathrm{VCdim}(\mathcal{H}_k)=m$, then $2^m\le\Gamma_{\mathcal{H}_k}(m)\le(e^2 dm/k^2)^k$,
so $m \le k\log_2(e^2 dm/k^2)$. A standard lemma (e.g. Shalev-Shwartz–Ben-David, Lemma A.2)
converts $m\le k\log_2(am/k)$ into $m \le 2k\log_2(2ak/k) = O(k\log(ed/k))$. Hence
$$\boxed{\;\mathrm{VCdim}(\mathcal{H}_k) \;=\; O\!\big(k\log(ed/k)\big).\;}$$

**Lower-bound sanity check.** $\mathcal{H}_k$ contains $\mathcal{H}_I$ for any single $I$, and
$\mathrm{VCdim}(\mathcal{H}_I)=k$; so $\mathrm{VCdim}(\mathcal{H}_k)\ge k$. The upper bound is tight up
to the $\log(ed/k)$ factor, which is the price of choosing the support.

## A.2 Penalty-based SRM

**Class-level SRM theorem (from lecture).** Let $\mathcal{H}=\bigcup_{k=1}^d\mathcal{H}_k$ with
$p_k>0,\ \sum_k p_k\le 1$. Suppose for each $k$ there is a uniform-convergence rate
$\varepsilon_k(n,\delta)$ such that, with probability $\ge 1-\delta$ over $S$,
$\sup_{h\in\mathcal{H}_k}|L_S(h)-L_\mathcal{D}(h)|\le \varepsilon_k(n,\delta)$. Define
$\mathrm{pen}(k,n,\delta)=\varepsilon_k(n,p_k\delta)$ and
$\hat h\in\arg\min_{k,h\in\mathcal{H}_k}\{L_S(h)+\mathrm{pen}(k,n,\delta)\}$. Then with
probability $\ge 1-\delta$,
$$L_\mathcal{D}(\hat h) \;\le\; \inf_{k,\ h\in\mathcal{H}_k}\bigl\{L_\mathcal{D}(h) + 2\,\mathrm{pen}(k,n,\delta)\bigr\}.$$

**Instantiation for $\mathcal{H}_k$.** By A.1, $\mathrm{VCdim}(\mathcal{H}_k)=d_k=O(k\log(ed/k))$.
The VC uniform-convergence theorem (e.g. Vapnik–Chervonenkis / Massart) gives
$$\varepsilon_k(n,\delta) \;\le\; C_0\sqrt{\frac{d_k + \log(1/\delta)}{n}}
\;\le\; C_1\sqrt{\frac{k\log(ed/k) + \log(1/\delta)}{n}}.$$
Apply with confidence parameter $p_k\delta$:
$$\mathrm{pen}(k,n,\delta) \;\le\; C\sqrt{\frac{k\log(ed/k) + \log(1/p_k) + \log(1/\delta)}{n}}.$$
By the SRM theorem, with probability $\ge 1-\delta$,
$$\boxed{\;L_\mathcal{D}(\hat h)\;\le\;\inf_{1\le k\le d,\ h\in\mathcal{H}_k}\!\left\{
L_\mathcal{D}(h) + C\sqrt{\dfrac{k\log(ed/k) + \log(1/p_k) + \log(1/\delta)}{n}}\right\}.\;}$$

**Interpretation of each term.**

- $k\log(ed/k)$ is the **support cost**: it is the VC dimension of $\mathcal{H}_k$, and it
  pays for uniform convergence *within* the level $k$ — i.e. for the freedom to choose
  which $k$ coordinates carry weight and which halfspace to put on them.
- $\log(1/p_k)$ is the **sparsity-level cost**: it is the price of the union bound
  across the $d$ sparsity levels. With $p_k\propto 1/k^2$ we have
  $\log(1/p_k)=2\log k + O(1)$, much smaller than $\log(d)$ for the levels we actually
  care about.
- $\log(1/\delta)$ is the usual confidence cost.

## A.3 Comparison with dense halfspaces

Suppose $w^*$ with $\|w^*\|_0\le s$ and $L_\mathcal{D}(w^*)\le\eta$. Plugging
$h=$ this $w^*$ and $k=s$ into the SRM bound and forcing the penalty $\le\varepsilon$:
$$n \;\ge\; C\,\frac{s\log(ed/s) + \log(1/p_s) + \log(1/\delta)}{\varepsilon^2}
\;=\; O\!\left(\frac{s\log(ed/s) + \log(1/\delta)}{\varepsilon^2}\right)$$
(using $p_s\propto 1/s^2$, so $\log(1/p_s)=O(\log s)$, absorbed into $\log(ed/s)$).

Dense halfspaces in $\mathbb{R}^d$ have VC dimension $d$, so the corresponding sample
complexity is
$$n_{\mathrm{dense}} \;=\; O\!\left(\frac{d + \log(1/\delta)}{\varepsilon^2}\right).$$

**When sparse is smaller.** Sparse beats dense when $s\log(ed/s)\ll d$, i.e. roughly when
$s = o(d/\log d)$. For $s=d$ the bounds are identical up to a $\log$ factor; for
$s=\Theta(\log d)$ the sparse bound is exponentially better in $d$.

## A.4 Validation as model selection

Split $S$ evenly into $S_1$ (training, size $m=n/2$) and $S_2$ (validation, size $m$).
Define
$$w_k\in\arg\min_{\|w\|_0\le k}L_{S_1}(w),\qquad
\hat k\in\arg\min_{1\le k\le d}L_{S_2}(w_k).$$

**Step 1 (validation step).** Condition on $S_1$. The list $w_1,\dots,w_d$ is then a
*fixed* (i.e. $S_2$-independent) set of $d$ classifiers. Apply Hoeffding plus a union
bound over these $d$ candidates on the independent sample $S_2$ of size $m=n/2$: with
probability $\ge 1-\delta/2$, for all $k\in\{1,\dots,d\}$,
$$\bigl|L_{S_2}(w_k)-L_\mathcal{D}(w_k)\bigr| \;\le\; \sqrt{\frac{\log(4d/\delta)}{2m}}
\;\le\; C_2\sqrt{\frac{\log(d/\delta)}{n}}.$$
Therefore, on this event,
$$L_\mathcal{D}(w_{\hat k}) \;\le\; L_{S_2}(w_{\hat k}) + C_2\sqrt{\tfrac{\log(d/\delta)}{n}}
\;\le\; L_{S_2}(w_k) + C_2\sqrt{\tfrac{\log(d/\delta)}{n}}\quad\forall k,$$
and combining the two Hoeffding inequalities,
$$L_\mathcal{D}(w_{\hat k}) \;\le\; \min_{1\le k\le d} L_\mathcal{D}(w_k) + 2C_2\sqrt{\tfrac{\log(d/\delta)}{n}}. \quad (\star)$$

**Step 2 (training step).** For each fixed $k$, $w_k$ minimizes empirical risk over
$\mathcal{H}_k$ on $S_1$. By the VC uniform-convergence bound applied to $\mathcal{H}_k$ with
confidence $\delta/(2d)$ and sample size $m=n/2$, plus a union bound over $k$, with
probability $\ge 1-\delta/2$, for every $k$ and every $w$ with $\|w\|_0\le k$,
$$L_\mathcal{D}(w_k) \;\le\; L_\mathcal{D}(w) + C_3\sqrt{\frac{k\log(ed/k) + \log(d/\delta)}{n}}. \quad (\star\star)$$

**Combine.** Union bound the two events. With probability $\ge 1-\delta$, taking the
infimum over $k$ and $w$ in $(\star)$ via $(\star\star)$,
$$\boxed{\;L_\mathcal{D}(w_{\hat k}) \;\le\; \inf_{1\le k\le d,\ \|w\|_0\le k}\!\left\{
L_\mathcal{D}(w) + C\sqrt{\dfrac{k\log(ed/k) + \log(d/\delta)}{n}}\right\}.\;}$$

**Comparison with penalty SRM.**

| | Penalty-SRM | Validation |
|---|---|---|
| Sample used to *fit* candidates | all $n$ | $n/2$ |
| Sample used to *choose* $k$ | the same $n$ | a separate, independent $n/2$ |
| Complexity term for support | $k\log(ed/k)$ | $k\log(ed/k)$ |
| Complexity term for choosing $k$ | $\log(1/p_k)\!=\!O(\log k)$ | $\log d$ |

Validation pays a constant factor of $\sim 2$ in $n$ (the split) and replaces the
prior-dependent $\log(1/p_k)$ by $\log d$. In exchange, the validation step is purely
finite-class and never invokes the (in general computationally hard) penalty.

## A.5 Computation

**Brute-force algorithm (realizable case).** Enumerate every support
$I\subseteq[d]$ with $|I|=k$. For each $I$, solve the homogeneous-halfspace feasibility
problem
$$\text{find } w\in\mathbb{R}^I:\quad y_i\langle w, x_i|_I\rangle \ge 0\quad (i=1,\dots,n)$$
(strict-inequality / margin form, e.g. by LP or Perceptron). This is solvable in
$\mathrm{poly}(k,n)$ time. If any support yields a feasible $w$, output it; the realizable
assumption guarantees at least one such $I$ exists.

**Runtime.** $\binom{d}{k}\cdot \mathrm{poly}(k,n) \le (ed/k)^k\cdot\mathrm{poly}(k,n)$.
This is polynomial in $d$ iff $k=O(1)$ (a constant). For $k=\Theta(\log d)$ already, it
is $d^{\Theta(\log d)}$, superpolynomial.

**Statistical vs computational complexity.** Part A.3 shows that
$n=\widetilde O(s/\varepsilon^2)$ samples suffice to learn an $s$-sparse halfspace, with
*no* explicit dependence on $d$ beyond a log. But the brute-force algorithm needs
$d^s$ time. So small sample complexity does not buy small runtime: choosing the support
is a combinatorial problem whose decision version (PAC-learning sparse halfspaces under
adversarial noise) is NP-hard in general. This is exactly the Week 4 picture — VC theory
says "the information is in the sample"; computation says "extracting it can still be
hard."

---

# Part B — PAC-Bayes for Thresholds

$\mathcal{X}_N=\{1,\dots,N\}$, $\mathcal{Y}=\{0,1\}$,
$\mathcal{H}_N=\{h_t : t\in\{1,\dots,N{+}1\}\}$ with $h_t(x)=\mathbf{1}[x\ge t]$.

## B.1 VC dimension and point-posterior PAC-Bayes

**VCdim $=1$.** A single point $x_0$ is shattered: $h_{x_0}(x_0)=1$ and
$h_{x_0+1}(x_0)=0$ (taking $h_{N+1}$ if $x_0=N$). For *any* two points $x_1<x_2$, the
labeling $(y_1,y_2)=(1,0)$ is unachievable: $h_t(x_1)=1\Rightarrow t\le x_1<x_2\Rightarrow
h_t(x_2)=1\ne 0$. Hence $\mathrm{VCdim}(\mathcal{H}_N)=1$.

**KL for a point posterior.** $P$ uniform on $N+1$ thresholds, $Q_S=\delta_{h_{\hat t}}$:
$$\mathrm{KL}(Q_S\Vert P) \;=\; \log\frac{1}{P(h_{\hat t})} \;=\; \log(N+1).$$

**PAC-Bayes bound.** In the realizable setting, $L_S(Q_S)=L_S(h_{\hat t})=0$, so
$$L_\mathcal{D}(\delta_{h_{\hat t}}) \;\le\; \sqrt{\frac{\log(N+1) + \log(2n/\delta)}{2(n-1)}}.$$

**Why the $\log(N+1)$.** A VC realizable bound for thresholds gives the much sharper
$O(\log(1/\delta)/n)$ rate with *no* $\log N$. The $\log(N+1)$ in PAC-Bayes is the
$\mathrm{KL}$ of a point mass against a uniform prior over $N+1$ atoms: the prior is
fixed before seeing the data and is forced to spread its mass across all candidate
thresholds, so concentrating onto the empirical winner costs $\log(N+1)$ nats of KL.
This is a property of the *certificate* (specifically: of using a point posterior with a
prior that is uniform over an $N$-dependent set), not of the underlying learning problem.

## B.2 Version-space posterior

**Version space.** If $y_i=0$, consistency requires $h_t(x_i)=0$, i.e. $x_i<t$, i.e.
$t>x_i$. Hence $t>a(S):=\max_{i:y_i=0}x_i$ (with $a(S)=0$ if no negatives). If $y_i=1$,
consistency requires $x_i\ge t$, i.e. $t\le x_i$. Hence $t\le b(S):=\min_{i:y_i=1}x_i$
(with $b(S)=N{+}1$ if no positives). So
$$V(S) \;=\; \{t : a(S) < t \le b(S)\},\qquad |V(S)|=b(S)-a(S).$$
This set is nonempty in the realizable case since the true threshold lies in it.

**KL of $Q_V$.** $Q_V$ uniform on $V(S)$, $P$ uniform on $N+1$ thresholds, so
$$\mathrm{KL}(Q_V\Vert P) \;=\; \sum_{t\in V}\frac{1}{|V|}\log\frac{1/|V|}{1/(N+1)}
\;=\; \log\!\frac{N+1}{|V(S)|}.$$

**Empirical risk.** For every $t\in V(S)$, $h_t$ is consistent with $S$, so $L_S(h_t)=0$;
therefore $L_S(Q_V)=\mathbb{E}_{t\sim Q_V}L_S(h_t)=0$.

**Why $Q_V$ can beat the point posterior.** Both achieve $L_S=0$, but
$\mathrm{KL}(Q_V\Vert P)=\log(N+1)-\log|V(S)|$, smaller than $\log(N+1)$ by exactly
$\log|V(S)|$. When the version space is large (typical for small $n$), this gives a
genuinely tighter PAC-Bayes certificate.

## B.3 Spreading helps KL, but can hurt true risk

**True risk of $Q_W$.** The marginal of $\mathcal{D}$ on $\mathcal{X}_N$ is uniform and labels come
from $h_\tau$. For any $t$,
$$L_\mathcal{D}(h_t) = \Pr_x\bigl[h_t(x)\ne h_\tau(x)\bigr] = \frac{|\{x\in[N] : (x\ge t)\oplus(x\ge\tau)\}|}{N} = \frac{|t-\tau|}{N},$$
since the disagreement set is the integer interval between $\min(t,\tau)$ and
$\max(t,\tau)-1$, of size $|t-\tau|$. Hence
$$\boxed{\;L_\mathcal{D}(Q_W) \;=\; \mathbb{E}_{t\sim Q_W}L_\mathcal{D}(h_t)
\;=\; \frac{1}{N|W|}\sum_{t\in W}|t-\tau|.\;}$$

**Concrete example.** Take $N=20$, $\tau=11$, and a one-point sample
$S=((1,0))$. Then $a(S)=1$, $b(S)=N{+}1=21$, so
$V(S)=\{2,3,\dots,21\}$ with $|V(S)|=20$ — large.

- $\mathrm{KL}(\delta_{h_\tau}\Vert P)=\log 21\approx 3.04$.
- $\mathrm{KL}(Q_{V(S)}\Vert P)=\log\frac{21}{20}\approx 0.0488$.
  So $\mathrm{KL}(Q_V\Vert P)<\mathrm{KL}(\delta_{h_\tau}\Vert P)$.
- $L_\mathcal{D}(\delta_{h_\tau})=0$ ($h_\tau$ is the true labeller).
- $L_\mathcal{D}(Q_V)=\frac{1}{20\cdot 20}\sum_{t=2}^{21}|t-11|
   = \frac{1}{400}\bigl(\sum_{j=1}^{9}j + 0 + \sum_{j=1}^{10}j\bigr)
   = \frac{45+0+55}{400}=\frac{100}{400}=0.25$.
  So $L_\mathcal{D}(Q_V)>L_\mathcal{D}(\delta_{h_\tau})$.

**No contradiction with PAC-Bayes.** PAC-Bayes gives an *upper* bound on $L_\mathcal{D}(Q)$,
not a monotone equivalence: a smaller KL produces a smaller *bound*, but smaller bound
does not imply smaller actual risk. Both certificates correctly upper-bound their
respective $L_\mathcal{D}$ values; spreading the posterior across the version space gives a
tighter *certificate* even when it gives a *worse* posterior, because the posterior is
chosen to make $\mathrm{KL}+L_S$ small, not $L_\mathcal{D}$ small (which the learner does not
see).

## B.4 Every fixed prior can be attacked

**Pigeonhole.** $P$ is a probability distribution, so
$\sum_{\tau=2}^{N}P(h_\tau)\le 1$. Since this is a sum of $N-1$ nonnegative terms, at
least one satisfies
$$P(h_\tau)\;\le\;\frac{1}{N-1}\qquad\text{for some } \tau\in\{2,\dots,N\}. \quad (\dagger)$$
Fix this $\tau$.

**$\mathcal{D}_\tau$ is realizable.** Under $\mathcal{D}_\tau$, $\Pr[(x,y)=(\tau{-}1,0)]=
\Pr[(x,y)=(\tau,1)]=1/2$. Both points are correctly labelled by $h_\tau$:
$h_\tau(\tau-1)=0$, $h_\tau(\tau)=1$. So $L_\mathcal{D}(h_\tau)=0$.

**Both support points appear.** For $S\sim\mathcal{D}_\tau^n$, let $A$ = event that some
$x_i=\tau-1$ and some $x_j=\tau$. Then
$$\Pr[A^c] \;\le\; \Pr[\text{all }x_i=\tau-1] + \Pr[\text{all }x_i=\tau]
\;=\; 2\cdot (1/2)^n \;=\; 2^{1-n},$$
so $\Pr[A]\ge 1-2^{1-n}$.

**Version space collapses to $\{\tau\}$.** On $A$, $a(S)=\tau-1$ (the only label-0 value
in the support) and $b(S)=\tau$ (the only label-1 value), so by B.2,
$V(S)=\{t:\tau-1<t\le\tau\}=\{\tau\}$.

**Forced posterior.** Any posterior $Q$ with $L_S(Q)=0$ is supported on $V(S)=\{\tau\}$,
hence $Q=\delta_{h_\tau}$. Then
$$\mathrm{KL}(Q\Vert P) \;=\; \log\frac{1}{P(h_\tau)} \;\stackrel{(\dagger)}{\ge}\; \log(N-1).$$

**What this does/does not show.**

- *Does show:* For any fixed prior $P$ over $\mathcal{H}_N$, there exists a realizable
  distribution on which every zero-empirical-error PAC-Bayes certificate must incur
  $\mathrm{KL}\ge \log(N-1)$. So the *bound* it produces is at least
  $\sqrt{(\log(N-1)+\log(2n/\delta))/(2(n-1)\,)}$. This is a $\log N$ lower bound on the
  PAC-Bayes *certificate*.
- *Does not show:* A lower bound on the sample complexity of *learning* thresholds.
  ERM on thresholds achieves $L_\mathcal{D}(\hat h)=O(\log(1/\delta)/n)$ uniformly in $N$
  (VC dimension $1$). The certificate is loose; the learner is fine. The slack lives
  in the choice to (a) use a *fixed* prior chosen before seeing the data and (b)
  insist on a *zero-empirical-error* posterior. Either relaxing the
  $L_S(Q)=0$ requirement (KL-bound trades off against empirical risk) or allowing a
  data-dependent prior (e.g. localized PAC-Bayes) can sidestep the bound.
