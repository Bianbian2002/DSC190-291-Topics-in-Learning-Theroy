# Part C: AI Usage Report — Assignment 2
**DSC 190/291 — Learning Theory**  
**Student: Zeyu Bian**

---

## 1. Where AI was used

- **Part A ($\mathcal{H}_2$):** Used AI to sanity-check the “at most two runs of 1s” characterization against small-$n$ enumeration, and to typeset the growth-function proof cleanly.
- **Part B ($\mathcal{H}_{\mathrm{quad}}$):** Used AI to organize the embedding argument (Veronese lift) and to separate *necessary* obstructions (alternating patterns forcing too many roots) from a fully polished *sufficient* characterization of all realizable labelings.
- **Repository / build:** AI drafted `verify_patterns.py`, `build_pdfs.sh`, and the Pandoc pipeline to produce PDFs from Markdown.

---

## 2. Suggestions accepted

- **Growth function for $\mathcal{H}_2$:** AI proposed verifying $\Gamma_{\mathcal{H}_2}(n)=\sum_{k=0}^4 \binom{n}{k}$ by brute force for $n\le 11$ and matching it to the Sauer–Shelah polynomial; I kept this because it is an independent check on the closed form obtained by counting separated runs.
- **VC bound for $\mathcal{H}_{\mathrm{quad}}$:** The explicit feature map $\varphi(x)=(x^2,x,1)$ and the reduction to homogeneous halfspaces in $\mathbb{R}^3$ is standard; AI helped format the reduction as a short lemma.

---

## 3. Suggestions rejected or modified

- **Over-strong quadratic characterization:** Some drafts tried to equate realizability with a single simple forbidden subpattern (e.g. “no 1010 subsequence”). Subsequence avoidance is **not** equivalent to quadratic realizability on a fixed ordered tuple; I removed overly crisp claims not fully justified and replaced them with the correct *necessary* alternation obstruction plus a general-position growth statement.
- **Loose VC/growth language:** Any phrasing that implied “two switches among gaps” determines $\Gamma$ was rejected as it mirrors the flawed audit prompt in the homework.

---

## 4. How correctness was checked

- **Combinatorics:** Ran `python3 verify_patterns.py` to confirm the $\mathcal{H}_2$ brute counts match $\sum_{k=0}^4 \binom{n}{k}$ for $n\le 11$.
- **Proofs:** Manually re-derived the two-interval endpoint construction (Part A.1) and re-checked the Halving/Sauer comparison (equality for $\mathcal{H}_2$).
- **PDF build:** Recompiled Markdown with Pandoc + XeLaTeX and skimmed the PDF for broken math delimiters.

---

## 5. AI workflow updates

- Added `Assignment/hw2/build_pdfs.sh` so theory + this report compile to a single submission PDF with one command.
- (Optional) Extend root `CLAUDE.md` with an Assignment 2 pointer so future sessions default to the `hw2/` layout.
