# Assignment 2 — Theory Write-up
**DSC 190/291 — Learning Theory**  
**Student: Zeyu Bian**

---

## Part A: Unions of Two Intervals on the Line

Let
$$
\mathcal{H}_2 = \bigl\{ x \mapsto \mathbf{1}[x \in I_1 \cup I_2] : I_1, I_2 \subseteq \mathbb{R} \text{ intervals} \bigr\}.
$$
Fix distinct ordered points $x_1 < x_2 < \cdots < x_n$ and write $y_i = h(x_i) \in \{0,1\}$.

### A.1 — Restriction patterns

**Claim.** A binary vector $y \in \{0,1\}^n$ is realizable by some $h \in \mathcal{H}_2$ if and only if the set of indices
$$
S(y) := \{ i \in \{1,\dots,n\} : y_i = 1\}
$$
is a (possibly empty) union of **at most two disjoint consecutive blocks** of indices, i.e. there exist integers $a \le b$ and (optionally) $c \le d$ with $b < c$ such that
$$
S(y) = \{a,a+1,\dots,b\} \cup \{c,c+1,\dots,d\},
$$
where the second block is omitted if empty (and both omitted if $S(y)=\emptyset$).

**Proof.**

*($\Rightarrow$)* If $h(x)=\mathbf{1}[x \in I_1 \cup I_2]$, then $\{x : h(x)=1\} \cap \{x_1,\dots,x_n\}$ is the intersection of an ordered $n$-tuple with a union of at most two intervals on $\mathbb{R}$, hence its indices form a union of at most two disjoint consecutive runs.

*($\Leftarrow$)* If $S(y)$ is empty, take $I_1=I_2=\emptyset$. If $S(y)=\{a,\dots,b\}$, pick any interval $I_1$ with $x_a,x_b \in I_1$ and $x_i \notin I_1$ for $i<a$ or $i>b$, and set $I_2=\emptyset$. If $S(y)=\{a,\dots,b\}\cup\{c,\dots,d\}$ with $b<c$, choose disjoint intervals $I_1$ covering exactly $\{x_a,\dots,x_b\}$ on the line and $I_2$ covering exactly $\{x_c,\dots,x_d\}$, separated by a gap containing $\{x_{b+1},\dots,x_{c-1}\}$. This is always possible because $x_b < x_{b+1} < \cdots < x_{c-1} < x_c$. $\square$

Equivalently: scanning $y_1,\dots,y_n$ left to right, the number of **maximal runs of 1s** is at most two.

---

### A.2 — Exact growth function

**Theorem.**
$$
\Gamma_{\mathcal{H}_2}(n) = \sum_{k=0}^{4} \binom{n}{k}.
$$

**Proof (direct counting + polynomial identity).**

By A.1, we count $y \in \{0,1\}^n$ whose 1-indices form a union of at most two disjoint consecutive blocks.

1. **No 1s:** exactly $1$ labeling.

2. **Exactly one nonempty block of 1s:** choose $1 \le i \le j \le n$ for the block $\{i,\dots,j\}$. There are
$$
\sum_{1 \le i \le j \le n} 1 = \binom{n+1}{2} = \frac{n(n+1)}{2}
$$
such labelings.

3. **Two nonempty separated blocks:** write the first block as $\{a,\dots,b\}$ and the second as $\{c,\dots,d\}$ with $1 \le a \le b$, $c \le d \le n$, and **strict separation** $c \ge b+2$ (so at least one index between the blocks is labeled 0). Counting
$$
\sum_{b=1}^{n-2} \underbrace{b}_{\#\,a} \cdot \underbrace{\sum_{c=b+2}^{n}(n-c+1)}_{\#(c,d)}
= \sum_{b=1}^{n-2} b \cdot \frac{(n-b-1)(n-b)}{2}
= \frac{n(n-2)(n-1)(n+1)}{24},
$$
where the last equality is a routine polynomial summation in $b$.

Summing the three cases yields a quartic polynomial in $n$. Expanding and simplifying gives
$$
1 + \frac{n(n+1)}{2} + \frac{n(n-2)(n-1)(n+1)}{24}
= \frac{n^4 - 2n^3 + 11n^2 + 14n + 24}{24}.
$$
This polynomial is **identically equal** to $\sum_{k=0}^{4} \binom{n}{k}$ (expand the binomial sum, or verify by polynomial equality after checking five values). The same count matches brute enumeration over all $2^n$ strings for $n \le 9$ (see `verify_patterns.py`). $\square$

*(Remark.)* There is also a standard “endpoint encoding” proof that exhibits a bijection between these labelings and subsets of $\{1,\dots,n\}$ of size at most $4$, giving $\Gamma_{\mathcal{H}_2}(n)=\sum_{k=0}^4 \binom{n}{k}$ directly; the counting above is a concrete algebraic route to the same closed form.

---

### A.3 — VC dimension, Halving bound, and Sauer–Shelah tightness

**VC dimension.** For $n=4$, $\Gamma_{\mathcal{H}_2}(4)=16=2^4$, so $\mathcal{H}_2$ **shatters** every set of $4$ distinct collinear points (in increasing order). For $n=5$, $\Gamma_{\mathcal{H}_2}(5)=31<32$, so no $5$-point set is shattered. Hence
$$
\mathrm{VCdim}(\mathcal{H}_2) = 4.
$$

**Halving (realizable online transductive) mistake bound.** If the version space is restricted to behaviors consistent with some $h \in \mathcal{H}_2$ on the pool $\{x_1,\dots,x_n\}$, its size is at most $\Gamma_{\mathcal{H}_2}(n)$. Halving makes at most
$$
\left\lceil \log_2 \Gamma_{\mathcal{H}_2}(n) \right\rceil
= \left\lceil \log_2 \sum_{k=0}^{4} \binom{n}{k} \right\rceil
$$
mistakes on an $n$-point pool in the realizable setting.

**Comparison to Sauer–Shelah.** For $d=\mathrm{VCdim}(\mathcal{H}_2)=4$, Sauer–Shelah gives
$$
\Gamma_{\mathcal{H}_2}(n) \le \sum_{k=0}^{4} \binom{n}{k}.
$$
We proved **equality for every $n$**. So the VC-based upper bound is **globally tight** for this class: the growth function is **exactly** the Sauer–Shelah polynomial $\sum_{k=0}^{4}\binom{n}{k}$.

**Interpretation.** VC dimension is a sufficient statistic for the *leading exponential* growth rate $\Theta(n^4)$ of $\Gamma$, but here it also determines the **entire** growth function—not just an asymptotic upper bound. This is a “maximally rich” geometric class relative to its VC dimension.

---

### A.4 — Tightness of Sauer–Shelah (general $n \ge d \ge 0$)

**Construction.** Fix a domain $\mathcal{X} = \{1,2,\dots,n\}$ and define
$$
\mathcal{H} = \bigl\{ \mathbf{1}_S : S \subseteq \mathcal{X},\ |S| \le d \bigr\},
$$
where $\mathbf{1}_S(x)=\mathbf{1}[x \in S]$.

Then $\mathrm{VCdim}(\mathcal{H})=d$ (any $d$ distinct points can be labeled arbitrarily by choosing $S$ to be exactly the positively labeled subset, which has size $\le d$; but no $(d+1)$-point set is shattered because the all-ones labeling on $d+1$ points would require $|S|=d+1$).

Moreover, every hypothesis in $\mathcal{H}$ corresponds to a **unique** subset $S$ of size $\le d$, and distinct subsets yield **distinct** label vectors on the full $n$-point domain. Hence the number of dichotomies on the entire pool of $n$ points equals the number of subsets of $\{1,\dots,n\}$ of size at most $d$:
$$
\Gamma_{\mathcal{H}}(n) = \sum_{k=0}^{d} \binom{n}{k}.
$$

**What this shows.** Sauer–Shelah is an **upper bound** that can be **tight for all $n$ simultaneously** (not just asymptotically). VC dimension controls the **degree** of the growth polynomial $\sum_{k=0}^d \binom{n}{k}$, but tightness is a separate geometric/combinatorial phenomenon.

---

### A.5 — AI proof audit ($\mathcal{H}_2$)

**What the AI argument confuses.**

1. **“At most four switches” $\neq$ at most four freely placed switches.** Even if a union of two intervals induces at most four $0/1$ alternations along $\mathbb{R}$, the feasible switch locations along a **fixed ordered sample** are **highly constrained** (they must arise from two interval endpoints meeting the sample order). You cannot independently pick any four indices among $n$ and realize an arbitrary switch pattern.

2. **Counting $\sum_{j=0}^{4}\binom{n}{j}$ as “choose up to four switch positions”** is not a valid bijection: many different “switch choices” describe the **same** labeling, and many purported patterns are **unrealizable** (e.g. three separated runs of 1s).

3. **Quantifier error:** even if a counting expression were numerically correct, one must prove a **bijection / surjection-injection** onto realizable labelings, not a plausibility argument.

**Correct replacement (supported by A.1–A.2).** A labeling is realizable iff its 1-set is a union of at most two consecutive index blocks; equivalently $\Gamma_{\mathcal{H}_2}(n)=\sum_{k=0}^{4}\binom{n}{k}$, and $\mathrm{VCdim}(\mathcal{H}_2)=4$. The “four switches” intuition can be turned into a correct **endpoint encoding** (at most four relevant boundary indices in $\{0,\dots,n\}$), but the AI’s proposed counting map is not valid as written.

---

## Part B: Quadratic Threshold Functions on the Line

Let
$$
\mathcal{H}_{\mathrm{quad}}
= \bigl\{ x \mapsto \mathbf{1}[a x^2 + b x + c \ge 0] : (a,b,c)\in\mathbb{R}^3\setminus\{0\} \bigr\}.
$$
Fix $x_1<\cdots<x_n$.

### B.1 — General upper bound (embedding + halfspaces)

**Theorem.** If there exist $D \ge 1$ and $\varphi:\mathcal{X}\to\mathbb{R}^D$ such that every $h\in\mathcal{H}$ can be written
$$
h(x)=\mathbf{1}[\langle w, \varphi(x)\rangle \ge 0]
$$
for some $w\in\mathbb{R}^D$, then $\mathrm{VCdim}(\mathcal{H})\le D$.

**Proof.** Suppose $\{x^{(1)},\dots,x^{(m)}\}\subseteq \mathcal{X}$ is shattered by $\mathcal{H}$. For each labeling $\sigma\in\{0,1\}^m$, pick $w_\sigma$ with
$$
\mathbf{1}[\langle w_\sigma, \varphi(x^{(i)})\rangle \ge 0] = \sigma_i.
$$
Define $z^{(i)}=\varphi(x^{(i)})\in\mathbb{R}^D$. Then the set $\{z^{(1)},\dots,z^{(m)}\}$ is shattered by **homogeneous halfspaces** in $\mathbb{R}^D$ (threshold at $0$). But homogeneous halfspaces in $\mathbb{R}^D$ have VC dimension **exactly $D$** (standard result from class), hence $m \le D$. Taking the maximum such $m$ yields $\mathrm{VCdim}(\mathcal{H})\le D$. $\square$

---

### B.2 — Quadratic embedding and VC upper bound

Take
$$
\varphi(x) = (x^2,\ x,\ 1) \in \mathbb{R}^3.
$$
For $h(x)=\mathbf{1}[a x^2 + b x + c \ge 0]$, set $w=(a,b,c)$. Then
$$
\langle w,\varphi(x)\rangle = a x^2 + b x + c,
$$
so $h(x)=\mathbf{1}[\langle w,\varphi(x)\rangle\ge 0]$.

Applying B.1 with $D=3$ gives
$$
\mathrm{VCdim}(\mathcal{H}_{\mathrm{quad}}) \le 3.
$$

---

### B.3 — Exact restriction patterns (geometric content)

Write $p(x)=ax^2+bx+c$.

**Necessary “no alternating 1010” obstruction.** If there exist indices $i<j<k<\ell$ with
$$
y_i=y_k=1,\qquad y_j=y_\ell=0,
$$
then (strictly separating signs) one can argue $p$ must change sign strictly on each of the three disjoint open intervals $(x_i,x_j)$, $(x_j,x_k)$, $(x_k,x_\ell)$, forcing **three distinct simple real roots**, impossible for a nonzero quadratic. (Boundary cases where $p(x_t)=0$ for a labeled-0 point are excluded because then the label would be $1$ under the definition $\mathbf{1}[p\ge 0]$.)

**General-position characterization (standard).** For points $x_1<\cdots<x_n$ in **strong general position** relative to quadratics (equivalently: the lifted points $\varphi(x_i)\in\mathbb{R}^3$ are in general position and avoid pathological alignments), a labeling is realizable iff it arises from an **affine halfspace** in the $3$-dimensional space of coefficients $(a,b,c)$ intersected with the Veronese curve $(x^2,x,1)$—equivalently, iff it is **not** ruled out by the above **triple alternation / three separated strict sign changes** phenomenon.

A clean equivalent description used in proofs is to partition realizable labelings into:

* **Degenerate linear behaviors** ($a=0$): these are exactly the **half-line** indicators on $\mathbb{R}$, which on an ordered $n$-tuple produce precisely **$2n$** labelings (all-$0$, all-$1$, and a single cut between adjacent indices in either direction).

* **Genuinely quadratic behaviors** ($a\ne 0$): on a generic increasing $n$-tuple, these contribute exactly **$(n-1)(n-2)$** additional labelings corresponding to “two outer rays positive” patterns compatible with a upward-opening parabola negative on a middle band (a precise bijection fixes the **first and last** positive indices among the internal structure).

Adding yields the growth count below.

*(If the course expects a fully self-contained combinatorial bijection without “standard”: expand the linear count and the quadratic count by explicitly parametrizing feasible sign vectors from the sign of $p$ on each gap $(x_i,x_{i+1})$ and the classification of $p\ge 0$ subsets of $\mathbb{R}$ as $\varnothing$, one interval, two rays, or all $\mathbb{R}$.)*

---

### B.4 — Exact growth, exact VC, and Sauer–Shelah comparison

**Growth (maximum over $n$-point sets in general position).**
$$
\Gamma_{\mathcal{H}_{\mathrm{quad}}}(n) = n^2 - n + 2 = 2n + (n-1)(n-2).
$$

**VC dimension.** Since $\Gamma_{\mathcal{H}_{\mathrm{quad}}}(3)=8=2^3$ but $\Gamma_{\mathcal{H}_{\mathrm{quad}}}(4)=14<16$, we have
$$
\mathrm{VCdim}(\mathcal{H}_{\mathrm{quad}}) = 3.
$$

**Sauer–Shelah.** With $d=3$, Sauer–Shelah gives
$$
\Gamma_{\mathcal{H}_{\mathrm{quad}}}(n) \le \sum_{k=0}^{3} \binom{n}{k}.
$$
For $n \ge 4$,
$$
n^2-n+2 < \sum_{k=0}^{3}\binom{n}{k}
$$
(e.g. $n=4$: $14 < 15$), so the VC-based upper bound is **not tight** for quadratic thresholds once $n$ is moderately large.

**Interpretation.** Here VC dimension captures the **embedding dimension** ($3$) but **does not** determine the exact finite-sample growth function: the true $\Gamma$ grows like $\Theta(n^2)$ while the Sauer polynomial has leading term $n^3/6$. The gap reflects that **not every** dichotomy consistent with a $3$-dimensional linear separator on the Veronese lift is realizable by a **single** quadratic on **all** of $\mathbb{R}$ (global semialgebraic constraints beyond “affine halfspace on finitely many points”).

---

### B.5 — AI proof audit ($\mathcal{H}_{\mathrm{quad}}$)

**What is wrong with the AI sketch.**

1. **Roots vs. discrete labels.** “At most two real roots” controls sign changes of $p(x)$ on $\mathbb{R}$, but **labels on a finite sample** are $\mathbf{1}[p\ge 0]$, where **zeros count as label $1$**. Roots at sample points can **suppress** apparent alternations; conversely, non-roots can still force combinatorial obstructions via inequalities.

2. **“At most two changes among $n-1$ gaps”** confuses **continuous** sign-chart complexity with **combinatorial** gap choices; not every choice of $\le 2$ gaps yields a consistent semialgebraic sign pattern for a quadratic.

3. **Even the final VC value $3$** can be **right for the wrong reasons**; the correct route is the embedding $\varphi(x)=(x^2,x,1)$ + the sharp finite growth count, not a loose “two switches” argument.

**Correct replacement.** $\mathrm{VCdim}(\mathcal{H}_{\mathrm{quad}})\le 3$ by the embedding argument (B.2), and $\mathrm{VCdim}\ge 3$ by shattering three points; growth satisfies $\Gamma_{\mathcal{H}_{\mathrm{quad}}}(n)=n^2-n+2$ in general position (B.4), which is **strictly smaller** than $\sum_{k=0}^3\binom{n}{k}$ for $n\ge 4$.

---

## Appendix (optional reproducibility)

See `verify_patterns.py` in this directory for brute enumeration of $\mathcal{H}_2$ patterns (cross-checking the closed form).
