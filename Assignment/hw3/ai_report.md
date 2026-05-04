# Part C — AI Usage Report

**DSC 190/291 — Assignment 3**
**Student: Zeyu Bian**

## 1. Where I used AI

I used Claude Code throughout this assignment, in three roles:

- **Mini-course (Part A) — exposition + proof structure.** I drafted the section
  outline myself, then asked AI to help organize the four inequalities under one
  unifying template (the MGF / Chernoff method), refine the comparison table, and tighten
  the explanation of why sampling without replacement concentrates more strongly than i.i.d.
  sampling. AI also helped me check the algebra in the Bernstein MGF lemma (specifically,
  the bound $\sum_{k\ge 2} u^k/k!\le \tfrac{u^2/2}{1-u/3}$).
- **NFL theorem (Part B) — quantifier audit + worked example.** I asked AI to act as an
  adversarial reader on my proof: in particular, to flag the place where the averaging
  argument secretly assumes $A$ is independent of the labels of unseen points, and to push
  back on whether my $|T|$ vs $|C\setminus T|$ counting was tight enough. I also used AI
  to sanity-check the constants $1/4 \to 1/8 \to 1/7$ in the Markov-in-reverse step.
- **Mini-course connection (A.5) — gluing the proofs into the Week 3 ERM bound.** AI
  helped me identify *which* concentration inequality enters at each step
  (Hoeffding for fixed-$h$ tail, McDiarmid for the sup, WoR-Hoeffding/symmetrization for
  $\mathbb{E}\Phi$, Massart's lemma for the finite-class step), which I then verified
  against Shalev-Shwartz–Ben-David Ch. 4 and Boucheron–Lugosi–Massart Ch. 3.

## 2. AI suggestions I accepted (and why)

- **Unified-template framing.** AI suggested presenting the four inequalities as
  "MGF-bound + Chernoff + (independence | martingale tower)" with a small ASCII diagram.
  I accepted this because it makes the four-results-as-one-method point I wanted to emphasize
  in Section A.4.5. I verified the framing is faithful by tracing each individual proof.
- **Hoeffding's lemma proof via convexity.** AI suggested the Taylor-style proof of
  Hoeffding's lemma rather than the symmetrization-style one. I accepted because it
  generalizes cleanly to the conditional version needed for McDiarmid.
- **Probabilistic-method phrasing in NFL.** AI suggested making the order of operations
  explicit ("draw $f$ first, then $S\sim\mathcal{D}_f^n$") to avoid a quantifier slip I
  had in my draft. I accepted; the cleaner phrasing is in Section B.1, Step 1.

## 3. AI suggestions I rejected or substantially modified

- **Bernstein constant.** AI's first draft wrote the Bernstein bound with denominator
  $2(\sigma^2 + Mt/3)$ where I had $2(v + Mt/3)$. Both are valid for different conventions
  ($\sigma^2$ per-variable vs $v$ summed); AI was inconsistent across paragraphs. I
  rewrote to standardize on $v = \sum\mathbb{E} X_i^2$ and verified against
  Boucheron–Lugosi–Massart §2.8.
- **WoR Hoeffding "proof".** AI initially gave a one-line "by exchangeability" proof,
  which is not rigorous — exchangeability does not imply concentration. I replaced this
  with the convex-domination route (Hoeffding 1963 Theorem 4) and was explicit that this
  is a sketch citing the modern proof in BLM §6.1.
- **NFL with $|T|$ vs $|T|=n$.** AI's draft used $|T| = n$, which is only true if the
  $X_i$ are distinct. I rewrote to use $|C\setminus T|\ge n$ which holds always, and to
  note that the inequality is actually pointwise in $S$.
- **Week 1 vs Week 3 comparison.** AI's first draft framed Week 1 as a "stochastic" result.
  I corrected this: Week 1 is purely adversarial / deterministic, and the comparison table
  is the place to make this explicit.

## 4. How I verified correctness

- **Proofs (Hoeffding, Bernstein, McDiarmid).** I cross-checked every line against
  Boucheron–Lugosi–Massart 2013, Chapters 2 and 6. I re-derived the Bernstein MGF bound
  by hand (the elementary inequality $\sum_{k\ge 2} u^k/k!\le u^2/(2(1-u/3))$ uses
  $k!\ge 2\cdot 3^{k-2}$ for $k\ge 2$, which is true: $2!=2\ge 2$, $3!=6\ge 6$, and
  $k!/(k-1)! = k\ge 3$ for $k\ge 3$).
- **WoR Hoeffding.** I verified the convex-domination claim by checking the $n=2$, $N=3$
  case explicitly (without replacement assigns probability $1/3$ to each unordered pair,
  while with-replacement assigns $1/9$ to each ordered pair; the partial-sum distributions
  match the dominance claim).
- **NFL constants.** I re-derived the $1/4\to 1/8\to 1/7$ chain: $\mathbb{E} W \ge 1/4$,
  and Markov-in-reverse with threshold $1/8$ gives $\Pr(W\ge 1/8)\ge (1/4 - 1/8)/(1 - 1/8)
  = (1/8)/(7/8) = 1/7$.
- **Worked NFL example.** Computed by hand: with $|\mathcal{X}|=10$, $n=4$, all-ones
  target, constant-0 fallback, the population loss is exactly $(10-|T|)/10\ge 6/10$
  deterministically. No AI was used to "verify" this; I checked it by direct calculation.
- **Week 3 ERM end-to-end.** I cross-checked Step 1–4 against Shalev-Shwartz–Ben-David
  §6.4 (which uses the McDiarmid + symmetrization + Massart route) and confirmed the
  $O(\sqrt{(\log\Gamma_\mathcal{H}(2n) + \log(1/\delta))/n})$ rate matches the statement
  in the assignment.
- **Exposition.** I read the entire write-up out loud once to catch awkward phrasings AI
  introduced and to make sure each claim is mine.

## AI workflow updates (5 most recent changes)

1. **Pinned the unifying-template framing.** Added to my working notes that whenever I
   write about a family of related results (here: 4 concentration inequalities), I should
   first ask AI to propose a unifying template, then verify each result fits it. This
   produced Section A.4.5 in this assignment and would have improved my hw2 growth-function
   exposition.
2. **Adversarial-reader protocol for proofs.** I now ask AI to act as a hostile reader on
   any proof I draft (specifically: "find the place where the proof depends on an
   independence assumption I might not have stated, or a quantifier swap I might have made").
   This caught the $A$-vs-unseen-labels independence issue in NFL.
3. **Citation discipline.** I added a rule that for every concentration inequality I cite,
   I must include a *page-or-theorem-level* citation, not just a textbook name. Boucheron–
   Lugosi–Massart §2.8 (Bernstein), Theorem 6.1 (WoR), etc. This is reflected in
   Section A.6 above.
4. **Hand-checking algebraic constants.** AI is unreliable on small numerical constants
   (e.g. the $1/8$ in Bernstein's denominator, the $2$ vs $1$ in Hoeffding's exponent).
   I now compute these by hand whenever they appear, and only use AI to draft the
   surrounding argument. The Bernstein-constant inconsistency described in §3 above is
   the example that pushed me to add this rule.
5. **Worked-example requirement.** For any abstract impossibility result, I now require
   myself to construct a concrete instance and compute the failure probability by hand.
   The constant-0 learner / all-ones target example in Section B.3 is the result of this
   rule. It pushed me to spot that the worst-case probability is actually $1$, not the
   $1/7$ guaranteed by the theorem — which clarified for me what NFL actually buys.

I did not use AI to fabricate any reference; every citation in Section A.6 corresponds to
a source I have either read or located.
