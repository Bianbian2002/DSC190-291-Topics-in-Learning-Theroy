# Part C — AI Usage Report

**DSC 190/291 — Assignment 4**
**Student: Zeyu Bian**

## 1. Where I used AI

I used Claude Code in four roles on this assignment:

- **Part A.1 (VC dimension via supports) — proof structure.** I asked AI to confirm the
  cleanest way to pass from $\Gamma_{\mathcal{H}_k}(n)\le (e^2 dn/k^2)^k$ to the
  $O(k\log(ed/k))$ VC bound — specifically, which form of the "if $m\le k\log(am/k)$ then
  $m=O(k\log a)$" lemma to cite. I then verified the constants by hand.
- **Part A.2 (SRM oracle inequality) — bookkeeping of the three statistical costs.**
  AI helped me lay out the table separating *support cost* $k\log(ed/k)$, *level cost*
  $\log(1/p_k)$, and *confidence cost* $\log(1/\delta)$, and made me state the
  class-level SRM theorem cleanly before plugging things in. The actual instantiation
  (each $p_k\delta$ confidence parameter, the $2\cdot\mathrm{pen}$ factor) I wrote and checked
  myself.
- **Part A.4 (Validation oracle bound) — independence argument.** I asked AI to be a
  hostile reader on my proof that conditioning on $S_1$ makes the candidate list
  $\{w_1,\dots,w_d\}$ data-independent of $S_2$. This caught the place where I had
  originally tried to use a single uniform-convergence bound on $\mathcal{H}$ instead of
  the much sharper finite-class Hoeffding-with-union-bound on $d$ fixed candidates.
- **Part B (PAC-Bayes for thresholds) — example construction.** For B.3 I sketched the
  $(N=20,\tau=11,S=((1,0)))$ example by hand, then asked AI to double-check the arithmetic
  $\sum_{t=2}^{21}|t-11|=100$ and the resulting $L_\mathcal{D}(Q_V)=0.25$.

## 2. AI suggestions I accepted (and why)

- **The product form $\binom{d}{k}(en/k)^k\le(e^2 dn/k^2)^k$ for A.1.** AI suggested
  writing the growth-function bound in this "two factors of the same shape" form so the
  log-linear fixed-point lemma applies immediately. I accepted because it cleans up
  the algebra and produces the bound with the right constants.
- **Confidence rescaling $\delta\to p_k\delta$ in A.2.** AI's framing — "each level pays
  $\log(1/p_k)$ because the union bound assigns confidence $p_k\delta$ to level $k$" —
  is exactly the right way to explain the level cost in one sentence. I accepted and
  put it in the interpretation paragraph.
- **Validation comparison table in A.4.** AI suggested a four-row table comparing
  penalty-SRM and validation (sample used to fit; sample used to choose; support cost;
  level cost). I accepted because it makes the trade-off explicit and answers the
  "what is paid for the separation?" question directly.
- **Distinguish certificate vs learning in B.4.** AI insisted I add a final paragraph
  separating "PAC-Bayes lower-bounds the certificate" from "this is not a sample
  complexity lower bound." This is the actual point of the problem; without it the
  conclusion reads as a paradox.

## 3. AI suggestions I rejected or substantially modified

- **A.1 lower-bound claim.** AI's first draft asserted
  $\mathrm{VCdim}(\mathcal{H}_k)\ge k\log(d/k)$ without proof and tried to use it as a
  "matching lower bound." This is true but nontrivial; I demoted the claim to a
  sanity-check observation that $\mathrm{VCdim}(\mathcal{H}_k)\ge k$ (which is immediate
  from $\mathcal{H}_I\subseteq\mathcal{H}_k$) and dropped the unproved matching claim.
- **A.4 single-step union bound.** AI's first attempt at the validation bound tried
  to run *one* uniform-convergence statement over $\bigcup_k\mathcal{H}_k$ on $S_2$. This
  is wrong: $S_2$ only sees the *finite* list $w_1,\dots,w_d$, not all of $\mathcal{H}$;
  using the full uniform-convergence bound would gives a worse rate
  ($\sqrt{d/n}$ via VC) instead of the correct $\sqrt{\log d/n}$. I rewrote to make
  the conditioning on $S_1$ explicit and use Hoeffding on $d$ fixed candidates.
- **B.3 example.** AI's first proposed counterexample had $|V(S)|$ small and the KL
  inequality went the wrong way. I rewrote with $S=((1,0))$, which leaves
  $V(S)=\{2,\dots,N+1\}$ (i.e. all but one threshold), making the KL inequality strict
  and the risk inequality strict.
- **B.4 "$\tau\in\{1,\dots,N+1\}$" claim.** AI's first proof of the pigeonhole step
  used the pigeonhole over all $N+1$ thresholds to get $P(h_\tau)\le 1/(N+1)$, then
  tried to construct $\mathcal{D}_\tau$ using $x=\tau-1, x=\tau$. But this construction
  fails for $\tau=1$ (no $x=0$) and $\tau=N+1$ (no $x=N+1$). I rewrote to restrict
  $\tau\in\{2,\dots,N\}$ and get the slightly weaker $P(h_\tau)\le 1/(N-1)$, matching
  the assignment's $\log(N-1)$ bound.

## 4. How I verified correctness

- **A.1 VC bound.** Verified the algebra step-by-step:
  $\binom{d}{k}\le (ed/k)^k$ (standard, true for $1\le k\le d$); Sauer–Shelah for
  $\mathcal{H}_I$ at $n\ge k$; the log-linear inversion lemma applied to
  $m\le k\log_2(e^2 dm/k^2)$. Cross-checked against Shalev-Shwartz–Ben-David Lemma A.2.
- **A.2 SRM theorem.** Cross-checked the statement of the class-level SRM theorem and
  the $2\cdot\mathrm{pen}$ factor against SSBD §7.2. Verified the chain
  $\varepsilon_k(n,\delta)\to\mathrm{pen}(k,n,\delta)=\varepsilon_k(n,p_k\delta)$ produces
  the boxed bound by direct substitution.
- **A.3 sample complexity.** Verified $s\log(ed/s) + 2\log s = O(s\log(ed/s))$ for
  $s\le d$ so absorbing $\log(1/p_s)$ into the leading term is legitimate. Verified
  the boundary $s\log(d/s)\le d$ algebraically: equivalent to $\log(d/s)\le d/s$, true
  for $d/s\ge 1$ (which is given since $s\le d$).
- **A.4 validation bound.** Verified the two-step argument $(\star)+(\star\star)$
  gives the stated bound by writing out the two events explicitly and applying the
  union bound at $\delta/2+\delta/2=\delta$. Cross-checked the finite-class step
  against SSBD §11.2.
- **A.5 runtime.** Verified $(ed/k)^k$ is the upper bound on $\binom{d}{k}$ I used;
  noted polynomial-in-$d$ regime via $k=O(1)$ and superpolynomial regime via
  $k=\log d$ by direct exponentiation.
- **B.1 VC=1.** Verified by hand the impossibility of the $(1,0)$ pattern on
  $x_1<x_2$ from the definition $h_t(x)=\mathbf{1}[x\ge t]$.
- **B.2 version space.** Verified $a(S)<t\le b(S)$ from the two consistency
  conditions $\{y_i=0\Rightarrow t>x_i\}$ and $\{y_i=1\Rightarrow t\le x_i\}$. Checked
  the edge cases (no negatives: $a(S)=0$ gives $V=\{1,\dots,b(S)\}$; no positives:
  $b(S)=N{+}1$ gives $V=\{a(S){+}1,\dots,N{+}1\}$).
- **B.3 arithmetic.** Computed
  $\sum_{t=2}^{21}|t-11|=\sum_{j=1}^{9}j + 0 + \sum_{j=1}^{10}j = 45+55 = 100$
  by hand; verified $L_\mathcal{D}(Q_V)=100/400=0.25$ matches the formula.
- **B.4 failure probability.** Verified
  $\Pr[A^c]=\Pr[\text{all }(\tau-1)]+\Pr[\text{all }\tau]=2\cdot 2^{-n}=2^{1-n}$ by
  enumerating the support of $\mathcal{D}_\tau^n$.

## AI workflow updates (5 most recent changes)

1. **"Pigeonhole over the right set" rule.** AI tends to apply pigeonhole over the
   full set ($\{1,\dots,N{+}1\}$ here), then build a construction that only works for
   *interior* indices. I now check, after any pigeonhole step, whether my downstream
   construction has edge cases. This caught the $\tau\in\{1,N{+}1\}$ issue in B.4.
2. **"Finite-class vs uniform-convergence" prompt.** Before applying uniform
   convergence over a hypothesis class, I now explicitly ask "is this set fixed
   independently of the sample I'm evaluating on?" If yes, prefer Hoeffding+union over
   the (finite) set; if no, pay the VC complexity. This fixed the A.4 validation proof.
3. **Concrete-example-first protocol for PAC-Bayes/KL gaps.** Whenever AI claims an
   inequality between two information-theoretic quantities (e.g. "KL of $Q_V$ is much
   smaller than KL of $\delta$"), I require a worked numerical example before trusting
   it. This is how the B.3 example got written.
4. **Costs-table convention.** I added a rule that every oracle inequality I write
   must come with a row-by-row explanation of each term in the complexity penalty
   (support cost, level cost, confidence cost, validation overhead). This produced the
   interpretation paragraph in A.2 and the comparison table in A.4.
5. **"Reject unproved matching lower bounds."** AI is willing to assert
   $\mathrm{VCdim}\ge \dots$ matching the upper bound without proof. I now demand either
   a proof or a citation; if neither, I demote the claim to a weaker sanity check (in
   A.1: $\mathcal{H}_I\subseteq\mathcal{H}_k\Rightarrow\mathrm{VCdim}\ge k$).

I did not use AI to fabricate any reference; every cited result (SSBD Lemma A.2,
SSBD §7.2, §11.2) is one I located and read.
