# Assignment 8 — Write-up
**DSC 190/291 — Learning Theory**
**Student: Zeyu Bian**

---

# Part A — Choosing Regularization by Validation

Throughout, $\ell(w,z)\in[0,1]$ is convex and $G$-Lipschitz in $w$ w.r.t. $\|\cdot\|$, $\Psi\ge0$ is $\alpha$-strongly convex w.r.t. $\|\cdot\|$, the training sample $T$ (size $n_T$) and validation sample $V$ (size $n_V$) are independent i.i.d. draws, $L_S(w)=\frac1{|S|}\sum_{z\in S}\ell(w,z)$, and $L_{\mathcal D}(w)=\mathbb E_z\ell(w,z)$.

## A.1 Validation selection for a finite random candidate set (10 pts)

**Claim.** Conditioning on predictors $h_1,\dots,h_K$ independent of $V$, with $\hat k\in\arg\min_{k\in[K]}L_V(h_k)$,
$$\mathbb E_V\,L_{\mathcal D}(h_{\hat k})\;\le\;\min_{k\in[K]}L_{\mathcal D}(h_k)+2\sqrt{\frac{\log(2K)}{2n_V}}.$$

**Proof.** Condition on the $h_k$'s; they are fixed functions independent of $V$. For each $k$,
$$L_V(h_k)=\frac1{n_V}\sum_{z\in V}\ell(h_k,z)$$
is an average of $n_V$ i.i.d. $[0,1]$-valued terms with mean $L_{\mathcal D}(h_k)$.

**Step 1: a uniform deviation bound in expectation.** Define
$$\Delta:=\max_{k\in[K]}\bigl|L_V(h_k)-L_{\mathcal D}(h_k)\bigr|.$$
By Hoeffding's lemma, each centered term $\ell(h_k,z)-L_{\mathcal D}(h_k)\in[-1,1]$-ish (a shifted $[0,1]$ variable) has MGF bounded by $e^{s^2/8}$. Independence across $z\in V$ gives, for the centered average $X_k:=L_V(h_k)-L_{\mathcal D}(h_k)$,
$$\mathbb E\,e^{sX_k}=\prod_{z\in V}\mathbb E\,e^{(s/n_V)(\ell(h_k,z)-L_{\mathcal D}(h_k))}\le\Bigl(e^{(s/n_V)^2/8}\Bigr)^{n_V}=e^{s^2/(8n_V)},$$
so each $X_k$ (and each $-X_k$) is $\sigma$-subgaussian with $\sigma^2=\tfrac1{4n_V}$. The $2K$ variables $\{\pm X_k\}$ are subgaussian, so by the standard maximal inequality: for any $s>0$,
$$e^{s\,\mathbb E\Delta}\le\mathbb E\,e^{s\Delta}=\mathbb E\max_{k,\pm}e^{\pm sX_k}\le\sum_{k,\pm}\mathbb E\,e^{\pm sX_k}\le 2K\,e^{s^2\sigma^2/2},$$
hence $\mathbb E\Delta\le\frac{\log(2K)}{s}+\frac{s\sigma^2}{2}$. Optimizing at $s=\sqrt{2\log(2K)}/\sigma$ gives
$$\mathbb E_V\,\Delta\;\le\;\sigma\sqrt{2\log(2K)}=\sqrt{\tfrac1{4n_V}}\,\sqrt{2\log(2K)}=\sqrt{\frac{\log(2K)}{2n_V}}.$$

**Step 2: the selection argument.** Let $k^\star\in\arg\min_k L_{\mathcal D}(h_k)$. Then
$$L_{\mathcal D}(h_{\hat k})\;\overset{(i)}{\le}\;L_V(h_{\hat k})+\Delta\;\overset{(ii)}{\le}\;L_V(h_{k^\star})+\Delta\;\overset{(iii)}{\le}\;L_{\mathcal D}(h_{k^\star})+2\Delta,$$
where (i) and (iii) use $|L_V(h_k)-L_{\mathcal D}(h_k)|\le\Delta$, and (ii) uses that $\hat k$ minimizes $L_V$. Taking $\mathbb E_V$ and Step 1:
$$\mathbb E_V\,L_{\mathcal D}(h_{\hat k})\le L_{\mathcal D}(h_{k^\star})+2\,\mathbb E_V\Delta\le\min_{k\in[K]}L_{\mathcal D}(h_k)+2\sqrt{\frac{\log(2K)}{2n_V}}.\qquad\square$$

**Key insight.** Because the $h_k$ are independent of $V$, the validation loss is an *unbiased* risk estimate for each; the only cost of picking the best is the $\sqrt{\log K}$ entropy of a union bound over $K$ fixed candidates, not the internal complexity of any $h_k$.

---

## A.2 Oracle inequality over a grid (10 pts)

**Claim.**
$$\mathbb E\,L_{\mathcal D}(h_{\hat\lambda})\;\le\;\min_{\lambda\in\Lambda}\inf_{u\in\mathcal W}\Bigl\{L_{\mathcal D}(u)+\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n_T}\Bigr\}+2\sqrt{\frac{\log(2K)}{2n_V}}.$$

**Proof.** *Apply A.1 conditionally on $T$.* Given $T$, the $K$ predictors $h_\lambda=A_\lambda(T)$ ($\lambda\in\Lambda$) are deterministic functions of $T$, hence independent of $V$. A.1 (with the candidate set $\{h_\lambda\}_{\lambda\in\Lambda}$, $K$ of them) gives
$$\mathbb E_V\bigl[L_{\mathcal D}(h_{\hat\lambda})\mid T\bigr]\le\min_{\lambda\in\Lambda}L_{\mathcal D}(h_\lambda)+2\sqrt{\frac{\log(2K)}{2n_V}}.$$
Take $\mathbb E_T$ and use $\mathbb E_T\min_\lambda(\cdot)\le\min_\lambda\mathbb E_T(\cdot)$:
$$\mathbb E\,L_{\mathcal D}(h_{\hat\lambda})\le\min_{\lambda\in\Lambda}\mathbb E_T\,L_{\mathcal D}(A_\lambda(T))+2\sqrt{\frac{\log(2K)}{2n_V}}.\tag{$\ast$}$$

*Week-8 exact-RERM bound.* Fix $\lambda$ and write $w_S=A_\lambda(S)$, the exact minimizer of $F_S(w)=L_S(w)+\lambda\Psi(w)$ (which is $\lambda\alpha$-strongly convex). The movement bound $\|w_S-w_{S'}\|\le\frac{2G}{\lambda\alpha n_T}$ (one-example change) plus $G$-Lipschitz $\ell$ give uniform stability $\beta=\frac{2G^2}{\lambda\alpha n_T}$, so $\mathbb E_T[L_{\mathcal D}(w_T)-L_T(w_T)]\le\beta$. Also, for any fixed $u$,
$$\mathbb E_T\,L_T(w_T)\le\mathbb E_T\bigl[L_T(w_T)+\lambda\Psi(w_T)\bigr]=\mathbb E_T\,F_T(w_T)\le\mathbb E_T\,F_T(u)=L_{\mathcal D}(u)+\lambda\Psi(u),$$
using $\Psi\ge0$, then that $w_T$ minimizes $F_T$, then $\mathbb E_T L_T(u)=L_{\mathcal D}(u)$. Adding,
$$\mathbb E_T\,L_{\mathcal D}(A_\lambda(T))\le L_{\mathcal D}(u)+\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n_T}\qquad\text{for every }u\in\mathcal W.$$
Taking $\inf_u$ then $\min_\lambda$ and substituting into $(\ast)$ proves the claim. $\square$

**Why the validation term is $\sqrt{\log K/n_V}$.** Selecting $\hat\lambda$ is exactly the finite-class selection of A.1 with $K$ candidates that are frozen once $T$ is fixed. The validation set certifies each candidate by an unbiased $n_V$-sample average; controlling the worst of $K$ such averages costs a union bound, contributing $\sqrt{\log K}$ (entropy) times $1/\sqrt{n_V}$ (concentration). It is independent of how complex each RERM rule is, because validation never re-uses $T$.

---

## A.3 Adapting to an unknown comparator scale (12 pts)

For a comparator $u$, set $a=\Psi(u)$ and $\lambda_{\mathrm{opt}}(a)=\sqrt{\tfrac{2G^2}{\alpha a n_T}}$.

**Optimizing the two-term expression.** Define $g(\lambda)=\lambda a+\frac{2G^2}{\lambda\alpha n_T}$. By AM–GM,
$$g(\lambda)\ge2\sqrt{\lambda a\cdot\frac{2G^2}{\lambda\alpha n_T}}=2\sqrt{\frac{2G^2a}{\alpha n_T}}=2G\sqrt{\frac{2a}{\alpha n_T}},$$
with equality iff $\lambda a=\frac{2G^2}{\lambda\alpha n_T}$, i.e. $\lambda=\lambda_{\mathrm{opt}}(a)$. Moreover at the optimum both summands equal the same value
$$M:=\lambda_{\mathrm{opt}}(a)\,a=\frac{2G^2}{\lambda_{\mathrm{opt}}(a)\,\alpha n_T}=G\sqrt{\frac{2a}{\alpha n_T}}.$$

**The factor-2 discretization.** Since $B_{\min}^2\le a=\Psi(u)\le B_{\max}^2$, the grid property gives a $\lambda\in\Lambda$ with $\tfrac12\lambda_{\mathrm{opt}}(a)\le\lambda\le2\lambda_{\mathrm{opt}}(a)$; write $\lambda=c\,\lambda_{\mathrm{opt}}(a)$ with $c\in[\tfrac12,2]$. Then
$$g(\lambda)=c\,\lambda_{\mathrm{opt}}(a)\,a+\frac1c\cdot\frac{2G^2}{\lambda_{\mathrm{opt}}(a)\,\alpha n_T}=\Bigl(c+\tfrac1c\Bigr)M.$$
On $[\tfrac12,2]$ the convex map $c\mapsto c+\tfrac1c$ is maximized at the endpoints, where it equals $\tfrac52$. Hence
$$g(\lambda)\le\tfrac52 M=\tfrac52\,G\sqrt{\frac{2a}{\alpha n_T}}=\frac{5\sqrt2}{2}\,G\sqrt{\frac{\Psi(u)}{\alpha n_T}}.$$

**Conclusion.** For this $\lambda$ and this $u$, the A.2 bracketed term is
$$L_{\mathcal D}(u)+\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n_T}=L_{\mathcal D}(u)+g(\lambda)\le L_{\mathcal D}(u)+\frac{5\sqrt2}{2}\,G\sqrt{\frac{\Psi(u)}{\alpha n_T}}.$$
Since A.2 takes the $\min$ over $\lambda\in\Lambda$ and $\inf$ over comparators, it is bounded by this particular choice, so for every $u$ with $B_{\min}^2\le\Psi(u)\le B_{\max}^2$,
$$\boxed{\;\mathbb E\,L_{\mathcal D}(h_{\hat\lambda})\le L_{\mathcal D}(u)+\frac{5\sqrt2}{2}\,G\sqrt{\frac{\Psi(u)}{\alpha n_T}}+2\sqrt{\frac{\log(2K)}{2n_V}}.\;}\qquad\square$$

The constant inflated from the oracle value $2\sqrt2$ (achievable only if the grid hit $\lambda_{\mathrm{opt}}(a)$ exactly) to $\tfrac52\sqrt2$ — the worst case of the factor-2 mismatch $c+1/c$.

---

## A.4 A dyadic grid and the price of tuning (8 pts)

**Construction.** Write $C:=G\sqrt{2/(\alpha n_T)}$, so $\lambda_{\mathrm{opt}}(a)=C/\sqrt a$. As $a$ ranges over $[B_{\min}^2,B_{\max}^2]$, $\lambda_{\mathrm{opt}}(a)$ ranges continuously over
$$[\lambda_{\min},\lambda_{\max}]=\Bigl[\tfrac{C}{B_{\max}},\,\tfrac{C}{B_{\min}}\Bigr].$$
Take the dyadic grid
$$\Lambda=\Bigl\{\lambda_i=\tfrac{C}{B_{\max}}\cdot 2^{\,i}:\;i=0,1,\dots,K-1\Bigr\},\qquad K=\Bigl\lceil\log_2\tfrac{B_{\max}}{B_{\min}}\Bigr\rceil+1.$$
Consecutive points differ by a factor $2$, and the largest is $\lambda_{K-1}=\frac{C}{B_{\max}}2^{K-1}\ge\frac{C}{B_{\max}}\cdot\frac{B_{\max}}{B_{\min}}=\lambda_{\max}$, so $[\lambda_{\min},\lambda_{\max}]\subseteq[\lambda_0,\lambda_{K-1}]$. Any target $t=\lambda_{\mathrm{opt}}(a)$ lies in some $[\lambda_i,\lambda_{i+1}]=[\lambda_i,2\lambda_i]$, giving $\lambda_i\in[t/2,t]\subseteq[t/2,2t]$ — exactly the A.3 property. Thus
$$K=\Bigl\lceil\log_2\tfrac{B_{\max}}{B_{\min}}\Bigr\rceil+1=O\!\Bigl(\log\tfrac{B_{\max}}{B_{\min}}\Bigr).$$

**Equal split $n_T=n_V=n/2$.** Substituting into A.3, with $\sqrt{\Psi(u)/(\alpha n/2)}=\sqrt{2\Psi(u)/(\alpha n)}$:
$$\frac{5\sqrt2}{2}\,G\sqrt{\frac{2\Psi(u)}{\alpha n}}=5\,G\sqrt{\frac{\Psi(u)}{\alpha n}},\qquad 2\sqrt{\frac{\log(2K)}{2\cdot n/2}}=2\sqrt{\frac{\log(2K)}{n}},$$
so
$$\boxed{\;\mathbb E\,L_{\mathcal D}(h_{\hat\lambda})\le L_{\mathcal D}(u)+\underbrace{5\,G\sqrt{\frac{\Psi(u)}{\alpha n}}}_{\text{RERM learning}}+\underbrace{2\sqrt{\frac{\log(2K)}{n}}}_{\text{validation selection}}.\;}$$

**Reading the terms.**
- **RERM learning term** $5G\sqrt{\Psi(u)/(\alpha n)}=\Theta(1/\sqrt n)$: the statistical cost of fitting the regularized rule on $T$.
- **Validation-selection term** $2\sqrt{\log(2K)/n}$: the cost of choosing among the $K$ trained rules on $V$.
- **Price of not knowing $\Psi(u)$.** Since $K=O(\log(B_{\max}/B_{\min}))$, the validation term is $O\!\bigl(\sqrt{\log\log(B_{\max}/B_{\min})/n}\bigr)$ — only *doubly* logarithmic in the unknown scale range. Additionally, the learning constant inflated from $2\sqrt2\approx2.83$ (known scale) to $5$. So adaptivity costs a tiny $\sqrt{\log\log}$ additive term plus a modest constant factor, while retaining the optimal $1/\sqrt n$ rate.

---

# Part B — Approximate RERM and Optimization Error

Setup: $\ell$ convex and $G$-Lipschitz w.r.t. $\|\cdot\|$, $\Psi\ge0$ $\alpha$-strongly convex; $F_S(w)=L_S(w)+\lambda\Psi(w)$, exact minimizer $w_S$, and the algorithm returns $\tilde w_S$ with $F_S(\tilde w_S)\le F_S(w_S)+\eta$. Given: movement bound $\|w_S-w_{S'}\|\le\frac{2G}{\lambda\alpha n}$.

## B.1 Approximate minimizers are close to exact minimizers (7 pts)

**Claim.** $\;\|\tilde w_S-w_S\|\le\sqrt{2\eta/(\lambda\alpha)}$ for every $S$.

**Proof.** $F_S$ is $\lambda\alpha$-strongly convex. For $\mu$-strongly convex $F$ with minimizer $w^\star$ over the convex set $\mathcal W$, there is a subgradient $g\in\partial F(w^\star)$ with $\langle g,w-w^\star\rangle\ge0$ for all $w\in\mathcal W$ (first-order optimality), so
$$F(w)\ge F(w^\star)+\langle g,w-w^\star\rangle+\tfrac\mu2\|w-w^\star\|^2\ge F(w^\star)+\tfrac\mu2\|w-w^\star\|^2.$$
With $\mu=\lambda\alpha$, $w^\star=w_S$, $w=\tilde w_S$:
$$F_S(w_S)+\frac{\lambda\alpha}2\|\tilde w_S-w_S\|^2\le F_S(\tilde w_S)\le F_S(w_S)+\eta\;\Rightarrow\;\frac{\lambda\alpha}2\|\tilde w_S-w_S\|^2\le\eta,$$
i.e. $\|\tilde w_S-w_S\|\le\sqrt{2\eta/(\lambda\alpha)}$. $\square$

## B.2 Stability of approximate RERM (8 pts)

**Claim.** If $S,S'$ differ in one example, then $|\ell(\tilde w_S,z)-\ell(\tilde w_{S'},z)|\le\frac{2G^2}{\lambda\alpha n}+2G\sqrt{2\eta/(\lambda\alpha)}$.

**Proof.** Triangle inequality and B.1 (twice) plus the movement bound:
$$\|\tilde w_S-\tilde w_{S'}\|\le\|\tilde w_S-w_S\|+\|w_S-w_{S'}\|+\|w_{S'}-\tilde w_{S'}\|\le\frac{2G}{\lambda\alpha n}+2\sqrt{\frac{2\eta}{\lambda\alpha}}.$$
Applying $G$-Lipschitzness of $\ell$,
$$|\ell(\tilde w_S,z)-\ell(\tilde w_{S'},z)|\le G\|\tilde w_S-\tilde w_{S'}\|\le\frac{2G^2}{\lambda\alpha n}+2G\sqrt{\frac{2\eta}{\lambda\alpha}}.\qquad\square$$

## B.3 Learning guarantee with optimization error (8 pts)

**Claim.** $\;\mathbb E_S\,L_{\mathcal D}(\tilde w_S)\le L_{\mathcal D}(u)+\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n}+G\sqrt{2\eta/(\lambda\alpha)}$ for every $u\in\mathcal W$.

**Proof.** $L_{\mathcal D}$ is $G$-Lipschitz (an average of $G$-Lipschitz $\ell(\cdot,z)$), so by B.1,
$$L_{\mathcal D}(\tilde w_S)\le L_{\mathcal D}(w_S)+G\|\tilde w_S-w_S\|\le L_{\mathcal D}(w_S)+G\sqrt{\frac{2\eta}{\lambda\alpha}}.$$
Take $\mathbb E_S$ and apply the exact-RERM bound from A.2 (valid for the exact minimizer $w_S$ with $n$ samples), $\mathbb E_S L_{\mathcal D}(w_S)\le L_{\mathcal D}(u)+\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n}$:
$$\mathbb E_S\,L_{\mathcal D}(\tilde w_S)\le L_{\mathcal D}(u)+\lambda\Psi(u)+\frac{2G^2}{\lambda\alpha n}+G\sqrt{\frac{2\eta}{\lambda\alpha}}.\qquad\square$$
The optimization error enters *additively* and only at the slow $\sqrt\eta$ rate, through the true-risk Lipschitz gap to the exact minimizer — the stability result B.2 is what makes the exact-RERM term legitimate.

## B.4 How accurate must the optimizer be? (7 pts)

Compete with all $u$ with $\Psi(u)\le B^2$ using $\lambda=\sqrt{2G^2/(\alpha B^2 n)}=\frac{G\sqrt2}{B\sqrt{\alpha n}}$.

The two RERM terms balance: $\lambda B^2=\frac{2G^2}{\lambda\alpha n}=GB\sqrt{2/(\alpha n)}$, summing to $2\sqrt2\,\frac{GB}{\sqrt{\alpha n}}$. Hence
$$\mathbb E_S\,L_{\mathcal D}(\tilde w_S)\le L_{\mathcal D}(u)+2\sqrt2\,\frac{GB}{\sqrt{\alpha n}}+G\sqrt{\frac{2\eta}{\lambda\alpha}}.$$

**Sufficient condition.** $G\sqrt{2\eta/(\lambda\alpha)}\le\frac{GB}{\sqrt{\alpha n}}\iff\frac{2\eta}{\lambda\alpha}\le\frac{B^2}{\alpha n}\iff\eta\le\frac{\lambda B^2}{2n}$. Substituting $\lambda$:
$$\boxed{\;\eta\le\frac{\lambda B^2}{2n}=\frac{GB}{\sqrt{2\alpha}\,n^{3/2}}=O\!\Bigl(\frac{GB}{\sqrt\alpha\,n^{3/2}}\Bigr).\;}$$

**Resulting excess risk.** Under this condition,
$$\mathbb E_S\,L_{\mathcal D}(\tilde w_S)-L_{\mathcal D}(u)\le2\sqrt2\,\frac{GB}{\sqrt{\alpha n}}+\frac{GB}{\sqrt{\alpha n}}=(2\sqrt2+1)\frac{GB}{\sqrt{\alpha n}}=O\!\Bigl(\frac{GB}{\sqrt{\alpha n}}\Bigr).$$
So an optimizer accurate to $\eta=O(n^{-3/2})$ leaves the statistical $1/\sqrt n$ rate intact: optimization error is essentially free.

## B.5 Soft-margin linear classification (5 pts)

Here $\ell(w,(x,y))=(1-y\langle w,x\rangle)_+$ with $\|x\|_2\le R$, and $\Psi(w)=\tfrac12\|w\|_2^2$, so $\|\cdot\|=\|\cdot\|_2$, $\alpha=1$. The hinge is $1$-Lipschitz in $t=y\langle w,x\rangle$ and $|y\langle w-w',x\rangle|\le R\|w-w'\|_2$, so $G=R$. For $\|u\|_2\le B$ we have $\Psi(u)=\tfrac12\|u\|_2^2\le\tfrac12B^2$.

Specializing B.3 and minimizing $\frac\lambda2B^2+\frac{2R^2}{\lambda n}$ over $\lambda$ gives $\lambda=\frac{2R}{B\sqrt n}$ with balanced value $\frac{2RB}{\sqrt n}$, and the optimization term becomes $R\sqrt{2\eta/\lambda}=\sqrt{RB\eta}\,n^{1/4}$:
$$\boxed{\;\mathbb E_S\,L_{\mathcal D}(\tilde w_S)\le L_{\mathcal D}(u)+\frac{2RB}{\sqrt n}+n^{1/4}\sqrt{RB\,\eta}.\;}$$

**Optimization-error condition.** $n^{1/4}\sqrt{RB\eta}\le\frac{RB}{\sqrt n}\iff\sqrt n\,RB\,\eta\le\frac{R^2B^2}{n}\iff\eta\le\frac{RB}{n^{3/2}}$. Under $\eta\le RB/n^{3/2}$ the excess risk is at most $\frac{3RB}{\sqrt n}$ — again the optimization term is a lower-order $O(n^{-3/2})$ requirement and the statistical rate $RB/\sqrt n$ is preserved.

---

# Part C — A Weighted Euclidean Geometry

Linear prediction with scalar loss convex and $g$-Lipschitz in the prediction. $\mathcal C_b=\{w:|w_j|\le b_j\}$, $|\varphi_j(x)|\le r_j$, $Q=\mathrm{diag}(q_1,\dots,q_d)$ with $q_j>0$, $\|w\|_Q=\sqrt{w^\top Qw}$, $\Psi_Q(w)=\tfrac12w^\top Qw$ ($1$-strongly convex w.r.t. $\|\cdot\|_Q$).

## C.1 Geometry quantities (5 pts)

**Dual norm.** $\|v\|_{Q,*}=\sup_{\|w\|_Q\le1}\langle v,w\rangle$. Substituting $u=Q^{1/2}w$ (so $\|w\|_Q=\|u\|_2$, $w=Q^{-1/2}u$),
$$\|v\|_{Q,*}=\sup_{\|u\|_2\le1}\langle Q^{-1/2}v,u\rangle=\|Q^{-1/2}v\|_2=\sqrt{v^\top Q^{-1}v}=\sqrt{\textstyle\sum_j v_j^2/q_j}.$$
Hence
$$\|\varphi(x)\|_{Q,*}^2=\sum_{j=1}^d\frac{\varphi_j(x)^2}{q_j}\le\sum_{j=1}^d\frac{r_j^2}{q_j}.$$
**Domain radius.** $\displaystyle\sup_{w\in\mathcal C_b}\Psi_Q(w)=\sup_{|w_j|\le b_j}\frac12\sum_j q_jw_j^2=\frac12\sum_{j=1}^d q_jb_j^2$, each term maximized at $w_j=\pm b_j$. $\square$

## C.2 Fixed $Q$ (5 pts)

As a function of $w$, the loss is $G$-Lipschitz w.r.t. $\|\cdot\|_Q$ with
$$|\ell(w)-\ell(w')|\le g\,|\langle w-w',\varphi(x)\rangle|\le g\,\|w-w'\|_Q\,\|\varphi(x)\|_{Q,*}\le \underbrace{g\sqrt{\textstyle\sum_j r_j^2/q_j}}_{=:G}\,\|w-w'\|_Q,$$
by Cauchy–Schwarz in the $\|\cdot\|_Q/\|\cdot\|_{Q,*}$ duality. The Week-8 theorem ($\alpha=1$) with comparators restricted to $\mathcal C_b$ (so $\Psi_Q(w)\le P:=\tfrac12\sum_j q_jb_j^2$) gives
$$\mathbb E\,L_{\mathcal D}(A_\lambda(S))\le\inf_{w\in\mathcal C_b}L_{\mathcal D}(w)+\lambda P+\frac{2G^2}{\lambda n}.$$
Minimizing over $\lambda$ (AM–GM): $\min_\lambda\bigl(\lambda P+\frac{2G^2}{\lambda n}\bigr)=2\sqrt{2G^2P/n}=2G\sqrt{2P/n}$. With $G^2=g^2\sum_j r_j^2/q_j$ and $2P=\sum_j q_jb_j^2$,
$$2G\sqrt{\tfrac{2P}{n}}=\frac{2g}{\sqrt n}\sqrt{\Bigl(\textstyle\sum_j r_j^2/q_j\Bigr)\Bigl(\sum_j q_jb_j^2\Bigr)}.$$
Therefore
$$\boxed{\;\mathbb E\,L_{\mathcal D}(A_\lambda(S))\le\inf_{w\in\mathcal C_b}L_{\mathcal D}(w)+\frac{2g}{\sqrt n}\sqrt{\Bigl(\sum_{j=1}^d q_jb_j^2\Bigr)\Bigl(\sum_{j=1}^d\frac{r_j^2}{q_j}\Bigr)}.\;}\qquad\square$$

## C.3 Best diagonal geometry (5 pts)

Minimize $\Phi(q)=\bigl(\sum_j q_jb_j^2\bigr)\bigl(\sum_j r_j^2/q_j\bigr)$ over $q_j>0$. By Cauchy–Schwarz,
$$\Bigl(\sum_j q_jb_j^2\Bigr)\Bigl(\sum_j \tfrac{r_j^2}{q_j}\Bigr)\ge\Bigl(\sum_j\sqrt{q_jb_j^2}\cdot\sqrt{\tfrac{r_j^2}{q_j}}\Bigr)^2=\Bigl(\sum_{j=1}^d b_jr_j\Bigr)^2,$$
with equality iff $q_jb_j^2\propto r_j^2/q_j$, i.e. $q_j\propto r_j/b_j$. (Check $q_j=r_j/b_j$: both factors equal $\sum_j b_jr_j$.) Hence $\min_q\sqrt{\Phi(q)}=\sum_j b_jr_j$, and the best excess term is
$$\boxed{\;\frac{2g}{\sqrt n}\sum_{j=1}^d b_jr_j.\;}$$
The optimal geometry rescales each coordinate by $q_j\propto r_j/b_j$, replacing the product of $\ell_2$-type norms by the dimension-adapted $\ell_1$-type sum $\sum_j b_jr_j$. $\square$
