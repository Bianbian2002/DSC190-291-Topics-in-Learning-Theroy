# Part B: Theory Problems
**DSC 190/291 — Assignment 1**  
**Student: Zeyu Bian**

Throughout: $ \mathcal{X} = [0,1] $, $ \mathcal{Y} = \{-1,+1\} $, and $ h_\theta(x) = \mathrm{sign}(x - \theta) $ with the convention $ \mathrm{sign}(z) = +1 $ for $ z \geq 0 $ and $ \mathrm{sign}(z) = -1 $ for $ z < 0 $.

---

## B.1 — From Continuous Thresholds to a Finite Class

### Grid Construction

For $ \Delta \in (0, 1] $, define the uniform grid
$$
G = \left\{ \frac{k\Delta}{2} : k = 0, 1, \ldots, \left\lceil \frac{2}{\Delta} \right\rceil \right\} \cap [0,1].
$$
The spacing between consecutive points is $ \Delta/2 $, so every point in $[0,1]$ is within distance $ \Delta/2 $ of some grid point.

**Size of $ G $.**
$$
|G| = \left\lceil \frac{2}{\Delta} \right\rceil + 1 \;\leq\; \frac{2}{\Delta} + 2 \;=\; O\!\left(\frac{1}{\Delta}\right).
$$

### Consistency Proof

**Claim.** For every $\Delta$-separated threshold-realizable sequence $((x_t, y_t))_{t=1}^T$ with true threshold $\theta^* \in [0,1]$, there exists $\tilde\theta \in G$ such that $ h_{\tilde\theta}(x_t) = y_t $ for all $t$.

**Proof.** Since $G$ has spacing $\Delta/2$, there exists $\tilde\theta \in G$ with $ |\tilde\theta - \theta^*| \leq \Delta/2 $.

Fix any round $t$. By $\Delta$-separation, $ |x_t - \theta^*| \geq \Delta $. Consider two cases:

- **Case 1: $ x_t \geq \theta^* + \Delta $.** Then $ h_{\theta^*}(x_t) = +1 $. Since $ \tilde\theta \leq \theta^* + \Delta/2 \leq x_t - \Delta/2 < x_t $, we have $ h_{\tilde\theta}(x_t) = \mathrm{sign}(x_t - \tilde\theta) = +1 $. ✓

- **Case 2: $ x_t \leq \theta^* - \Delta $.** Then $ h_{\theta^*}(x_t) = -1 $. Since $ \tilde\theta \geq \theta^* - \Delta/2 \geq x_t + \Delta/2 > x_t $, we have $ h_{\tilde\theta}(x_t) = \mathrm{sign}(x_t - \tilde\theta) = -1 $. ✓

In both cases $ h_{\tilde\theta}(x_t) = h_{\theta^*}(x_t) = y_t $, so $ h_{\tilde\theta} $ is consistent with the entire sequence. $\square$

### Mistake Bound via Halving

The consistency proof shows every $\Delta$-separated threshold-realizable sequence is realizable by some hypothesis in the **finite** class
$$
\mathcal{H}_G = \{h_\theta : \theta \in G\}, \qquad |\mathcal{H}_G| = O(1/\Delta).
$$

**Halving Algorithm (explicit learner).** At each round $t$, let $V_t \subseteq \mathcal{H}_G$ be the version space (all hypotheses in $\mathcal{H}_G$ consistent with past examples). Predict the majority vote of $V_t$ on $x_t$.

**Halving Theorem.** If a mistake occurs, the version space strictly shrinks: at least half the current consistent hypotheses predict incorrectly, so $|V_{t+1}| \leq |V_t|/2$. Starting with $|V_1| = |\mathcal{H}_G|$, after $M$ mistakes, $|V| \geq 1$ implies
$$
1 \leq \frac{|\mathcal{H}_G|}{2^M} \implies M \leq \log_2 |\mathcal{H}_G|.
$$

**Mistake bound.**
$$
\boxed{M \leq \log_2 |\mathcal{H}_G| \leq \log_2\!\left(\frac{2}{\Delta} + 2\right) \leq \log_2\!\left(\frac{4}{\Delta}\right) = 2 + \log_2\!\frac{1}{\Delta} = O\!\left(\log\frac{1}{\Delta}\right).}
$$

---

## B.2 — A Positive Margin from Separation

### Feature Map and Unit Separator

Define $ \phi: [0,1] \to \mathbb{R}^2 $ by
$$
\phi(x) = (x,\, 1).
$$
For the true threshold $\theta^*$, define
$$
w^* = (1,\, -\theta^*) \in \mathbb{R}^2, \qquad u^* = \frac{w^*}{\|w^*\|} = \frac{(1, -\theta^*)}{\sqrt{1 + (\theta^*)^2}}.
$$
Then $ w^* \cdot \phi(x) = x - \theta^* $, so $ h_{\theta^*}(x) = \mathrm{sign}(w^* \cdot \phi(x)) = \mathrm{sign}(u^* \cdot \phi(x)) $.

### Norm Bound

$$
\|\phi(x)\| = \sqrt{x^2 + 1} \leq \sqrt{1 + 1} = \sqrt{2} =: R.
$$
(using $x \in [0,1]$, so $x^2 \leq 1$.)

### Margin Lower Bound

For any example $(x_t, y_t)$ in the $\Delta$-separated sequence, $ y_t = \mathrm{sign}(x_t - \theta^*) $, so $ y_t(x_t - \theta^*) = |x_t - \theta^*| \geq \Delta $. Also $\theta^* \in [0,1]$ implies $ \sqrt{1+(\theta^*)^2} \leq \sqrt{2} $. Therefore
$$
y_t \cdot (u^* \cdot \phi(x_t)) = \frac{y_t(x_t - \theta^*)}{\sqrt{1+(\theta^*)^2}} = \frac{|x_t - \theta^*|}{\sqrt{1+(\theta^*)^2}} \geq \frac{\Delta}{\sqrt{2}} =: \gamma.
$$
This establishes linear separability with margin
$$
\gamma \geq c\Delta, \qquad c = \frac{1}{\sqrt{2}}.
$$

### Mistake Bound via the Perceptron Theorem

**Perceptron Theorem.** If the sequence is linearly separable with unit vector $u^*$, margin $\gamma$, and $\|\phi(x_t)\| \leq R$ for all $t$, then the Perceptron algorithm makes at most $R^2/\gamma^2$ mistakes.

*Proof sketch (for completeness).* Let $M$ be the number of mistakes. Each mistake at round $t$ updates $w \leftarrow w + y_t \phi(x_t)$. Tracking:
- **Inner product:** $w_M \cdot u^* \geq M\gamma$ (each update adds $y_t(u^* \cdot \phi(x_t)) \geq \gamma$).
- **Squared norm:** $\|w_M\|^2 \leq MR^2$ (each update adds at most $R^2$, since on a mistake $y_t(w \cdot \phi(x_t)) \leq 0$).

By Cauchy–Schwarz: $ M\gamma \leq w_M \cdot u^* \leq \|w_M\| \leq R\sqrt{M} $, giving $ M \leq R^2/\gamma^2 $.

Applying to our setting:
$$
\boxed{M \leq \frac{R^2}{\gamma^2} \leq \frac{(\sqrt{2})^2}{(\Delta/\sqrt{2})^2} = \frac{2}{\Delta^2/2} = \frac{4}{\Delta^2} = O\!\left(\frac{1}{\Delta^2}\right).}
$$

---

## B.3 — Comparison and Interpretation

### No Contradiction with the Impossibility Theorem

The impossibility theorem from lecture states: for the class $\mathcal{H} = \{h_\theta : \theta \in [0,1]\}$ of all thresholds, no deterministic online learner can bound its number of mistakes on arbitrary threshold-realizable sequences. The proof constructs adversarial sequences by placing examples closer and closer to any learner's implicit "threshold estimate," exploiting the fact that the class is infinite and every point in $[0,1]$ can be the true threshold.

The $\Delta$-separation condition **rules out these adversarial sequences**. Any sequence with $|x_t - \theta^*| \geq \Delta$ for all $t$ cannot place examples in the "confusion zone" $(\theta^* - \Delta, \theta^* + \Delta)$ around the true threshold. This prevents the adversary from forcing an unlimited number of mistakes. There is therefore no contradiction: Part B.1 applies only to the restricted class of $\Delta$-separated sequences, not to the full class of threshold-realizable sequences.

### Comparison of the Two Bounds

| Method | Bound | Source |
|--------|-------|--------|
| Halving (B.1) | $O(\log(1/\Delta))$ | Hypothesis counting |
| Perceptron (B.2) | $O(1/\Delta^2)$ | Geometric margin |

For small $\Delta$, $ \log(1/\Delta) \ll 1/\Delta^2 $, so the Halving bound is dramatically tighter.

### Why the Bounds Scale Differently

The two arguments measure **different structural properties** of the problem.

**The Halving argument** exploits the *discrete* structure introduced by $\Delta$-separation. The separation condition collapses the infinite threshold class into a finite grid of size $O(1/\Delta)$. The Halving algorithm exploits this by maintaining a version space: each mistake eliminates at least half the remaining consistent hypotheses. The mistake count is bounded by the *logarithm* of the hypothesis class size — a purely combinatorial argument. The bound is tight for the Halving algorithm on this class.

**The Perceptron argument** exploits the *geometric* structure: the margin. The margin $\gamma = \Theta(\Delta)$ controls how well each update aligns the weight vector with the true separator. The bound $R^2/\gamma^2 = \Theta(1/\Delta^2)$ comes from comparing the linear growth of $w_M \cdot u^*$ (growing as $M\gamma$) to the square-root growth of $\|w_M\|$ (growing as $R\sqrt{M}$). Perceptron is a general-purpose algorithm that applies to any linearly separable data; it does *not* use the fact that the hypothesis class is finite.

In summary: the Halving bound is better because it uses both the problem structure (finite effective class) and an algorithm specifically designed to exploit it (majority vote over consistent hypotheses). Perceptron achieves a weaker bound because it leverages only the margin, ignoring the combinatorial structure.

---

## B.4 (Optional) — Auditing the AI Proof

### The AI Argument

> *Because every example is at least $\Delta$ away from the true threshold, continuous thresholds effectively form a class of size $O(1/\Delta)$. Therefore any online learner, including Perceptron, must make at most $O(\log(1/\Delta))$ mistakes on every $\Delta$-separated threshold-realizable sequence.*

### Two Mathematical Problems

**Problem 1: The hypothesis class is not of size $O(1/\Delta)$.**  
The claim "continuous thresholds effectively form a class of size $O(1/\Delta)$" is not a well-defined mathematical statement. The class $\mathcal{H} = \{h_\theta : \theta \in [0,1]\}$ is uncountably infinite regardless of any $\Delta$-separation assumption. What *is* true (and what Part B.1 establishes rigorously) is that one can construct a *finite cover* $\mathcal{H}_G$ of size $O(1/\Delta)$ such that every $\Delta$-separated sequence is realizable by some element of $\mathcal{H}_G$. But this finite cover is a proof artifact, not a property of $\mathcal{H}$ itself. Treating an informal concept ("effective size") as if it were a rigorous mathematical object without proving that the finite class is sufficient is a logical gap.

**Problem 2: The conclusion applies to all learners, including Perceptron — this is false.**  
The statement "any online learner, including Perceptron, must make at most $O(\log(1/\Delta))$ mistakes" is incorrect. The $O(\log(1/\Delta))$ bound is an upper bound for the *Halving algorithm* applied to *$\mathcal{H}_G$*. There is no general principle that says every learner achieves this bound. In fact, Part B.2 proves that Perceptron (under the feature map $\phi(x) = (x,1)$) achieves only $O(1/\Delta^2)$ mistakes — a factor of $1/\Delta$ worse. Perceptron does not exploit the finite structure of $\mathcal{H}_G$; it is oblivious to the combinatorial constraint and only uses the margin. Conflating "some algorithm achieves this bound" with "every algorithm, including Perceptron, achieves this bound" is a fundamental error in quantifier scope.

### Corrected Statement and Proof

**Theorem.** *For any $\Delta > 0$, there exists an explicit online learning algorithm that makes at most*
$$
\lfloor \log_2(2/\Delta) \rfloor + 1 = O(\log(1/\Delta))
$$
*mistakes on every $\Delta$-separated threshold-realizable sequence over $\mathcal{X} = [0,1]$.*

**Proof.** Construct the grid
$$
G = \left\{\frac{k\Delta}{2} : k = 0, 1, \ldots, \left\lceil \frac{2}{\Delta} \right\rceil\right\} \cap [0,1],
$$
with $|G| \leq 2/\Delta + 2$. By the consistency argument in Part B.1, every $\Delta$-separated threshold-realizable sequence is realizable by some $h_{\tilde\theta} \in \mathcal{H}_G$. Apply the Halving algorithm to $\mathcal{H}_G$: at each round, predict the majority vote of the current version space. By the Halving theorem, the number of mistakes satisfies
$$
M \leq \lfloor \log_2 |\mathcal{H}_G| \rfloor \leq \lfloor \log_2(2/\Delta + 2) \rfloor \leq \log_2(4/\Delta) = 2 + \log_2(1/\Delta) = O(\log(1/\Delta)).
$$

**Remark.** This bound does *not* apply to Perceptron. Under the feature map $\phi(x) = (x,1)$, Perceptron achieves the weaker bound $O(1/\Delta^2)$, as shown in Part B.2. $\square$
