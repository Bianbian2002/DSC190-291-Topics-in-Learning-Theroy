/-
# Sauer–Shelah Lemma — self-contained reproof (Path B)

We prove, from scratch, the Sauer–Shelah lemma in its concept-class form:

  For a finite ground set `α` and a concept class `𝒜 : Finset (Finset α)` with VC dimension
  `d`, writing `n = |α|`,
      `|𝒜| ≤ ∑_{k=0}^{d} C(n, k)`.

We do NOT cite mathlib's Sauer–Shelah results (`card_le_card_shatterer`,
`card_shatterer_le_sum_vcDim`) nor its compression library. We define our own
`Shatters` / `traces` / `vcDim` and prove everything with general-purpose `Finset` lemmas.

The argument is the classic **Pajor double-counting induction on the ground set**:
  1. `pajor`              : `#F ≤ #(traces X F)` — a family shatters at least `#F` sets.
  2. `card_traces_le_sum` : `#(traces univ 𝒜) ≤ ∑_{k≤d} C(n,k)` — counting sets of size `≤ d`.
  3. `card_le_sum_choose` : combine (1)+(2) with `X = univ`.

See REPORT.md for the natural-language proof this file mirrors.
-/
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.Powerset
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

open Finset

namespace SauerShelah

variable {α : Type*} [DecidableEq α]

/-! ## Definitions -/

/-- `F` **shatters** `T` if every subset `U ⊆ T` arises as `A ∩ T` for some member `A ∈ F`;
i.e. `F` realizes all `2^{|T|}` labelings on `T`. -/
def Shatters (F : Finset (Finset α)) (T : Finset α) : Prop :=
  ∀ U ⊆ T, ∃ A ∈ F, A ∩ T = U

instance (F : Finset (Finset α)) : DecidablePred (Shatters F) := fun T =>
  decidable_of_iff (∀ U ∈ T.powerset, ∃ A ∈ F, A ∩ T = U) (by
    simp only [mem_powerset, Shatters])

/-- The family of sets shattered by `F`, searched among subsets of the ground set `X`. -/
def traces (X : Finset α) (F : Finset (Finset α)) : Finset (Finset α) :=
  X.powerset.filter (Shatters F)

@[simp] lemma mem_traces {X : Finset α} {F : Finset (Finset α)} {S : Finset α} :
    S ∈ traces X F ↔ S ⊆ X ∧ Shatters F S := by
  simp only [traces, mem_filter, mem_powerset]

/-! ## Pajor's lemma: `#F ≤ #(traces X F)` -/

/-- **Pajor's lemma.** Any family `F` whose members lie in the ground set `X` shatters at
least `#F` distinct subsets of `X`. Proved by induction on `X`. -/
theorem pajor : ∀ (X : Finset α) (F : Finset (Finset α)), (∀ A ∈ F, A ⊆ X) →
    F.card ≤ (traces X F).card := by
  intro X
  induction X using Finset.induction with
  | empty =>
    -- Members must be `⊆ ∅`, hence `= ∅`, so `F ⊆ {∅}`. The shatterer is `{∅}` if `F` is
    -- nonempty and `∅` otherwise; either way `#F ≤ #(traces ∅ F)`.
    intro F hF
    have hF' : F ⊆ {∅} := by
      intro A hA; rw [mem_singleton, ← subset_empty]; exact hF A hA
    rcases Finset.subset_singleton_iff.1 hF' with h | h <;> subst h
    · simp
    · have : traces ∅ ({∅} : Finset (Finset α)) = {∅} := by
        ext S
        simp only [mem_traces, subset_empty, mem_singleton]
        constructor
        · rintro ⟨h, -⟩; exact h
        · rintro rfl
          refine ⟨rfl, fun U hU => ⟨∅, mem_singleton_self _, ?_⟩⟩
          rw [subset_empty.1 hU, inter_empty]
      rw [this]
  | @insert a X' ha ih =>
    intro F hF
    -- Split `F` according to whether a member contains `a`.
    set Fa := F.filter (fun A => a ∈ A) with hFa
    set Fn := F.filter (fun A => a ∉ A) with hFn
    -- `M`: members containing `a`, with `a` deleted.  `P = M ∪ Fn`, `Q = M ∩ Fn`.
    set M := Fa.image (fun A => A.erase a) with hM
    set P := M ∪ Fn with hP
    set Q := M ∩ Fn with hQ
    -- `erase a` is injective on `Fa` (those sets contain `a`), so `#M = #Fa`.
    have hMcard : M.card = Fa.card := by
      refine card_image_of_injOn ?_
      intro A hA B hB hAB
      have hAa : a ∈ A := (mem_filter.1 hA).2
      have hBa : a ∈ B := (mem_filter.1 hB).2
      rw [← insert_erase hAa, ← insert_erase hBa]
      exact congrArg (insert a) hAB
    -- `#F = #M + #Fn`  (split by membership of `a`, then transport `Fa` along the bijection).
    have hFcard : F.card = M.card + Fn.card := by
      rw [hMcard, hFa, hFn]
      exact (card_filter_add_card_filter_not (fun A => a ∈ A)).symm
    -- `#F = #P + #Q`  (inclusion–exclusion on `M, Fn`).
    have hFPQ : F.card = P.card + Q.card := by
      rw [hFcard, hP, hQ, ← card_union_add_card_inter]
    -- Members of `P` and `Q` lie in the smaller ground set `X'`.
    have hMsub : ∀ B ∈ M, a ∉ B ∧ insert a B ∈ F := by
      intro B hB
      rw [hM, mem_image] at hB
      obtain ⟨A, hA, rfl⟩ := hB
      have hAa : a ∈ A := (mem_filter.1 hA).2
      exact ⟨notMem_erase _ _, by rw [insert_erase hAa]; exact (mem_filter.1 hA).1⟩
    have hPsub : ∀ B ∈ P, B ⊆ X' := by
      intro B hB
      rw [hP, mem_union] at hB
      rcases hB with hB | hB
      · -- `B = A.erase a` with `A ⊆ insert a X'`
        rw [hM, mem_image] at hB
        obtain ⟨A, hA, rfl⟩ := hB
        intro x hx
        have hx' : x ∈ A ∧ x ≠ a := by rw [mem_erase] at hx; exact ⟨hx.2, hx.1⟩
        have : x ∈ insert a X' := hF A (mem_filter.1 hA).1 hx'.1
        rw [mem_insert] at this
        exact this.resolve_left hx'.2
      · -- `B ∈ F`, `a ∉ B`
        have hBF : B ∈ F := (mem_filter.1 hB).1
        have hBa : a ∉ B := (mem_filter.1 hB).2
        intro x hx
        have : x ∈ insert a X' := hF B hBF hx
        rw [mem_insert] at this
        exact this.resolve_left (fun h => hBa (h ▸ hx))
    have hQsub : ∀ B ∈ Q, B ⊆ X' := fun B hB => hPsub B (mem_union_left _ (mem_of_mem_inter_left hB))
    -- Induction hypotheses on `P` and `Q`.
    have ihP : P.card ≤ (traces X' P).card := ih P hPsub
    have ihQ : Q.card ≤ (traces X' Q).card := ih Q hQsub
    -- Claim A: a set shattered by `P` (inside `X'`) is shattered by `F` (inside `X`).
    have claimA : traces X' P ⊆ traces (insert a X') F := by
      intro S hS
      rw [mem_traces] at hS ⊢
      refine ⟨hS.1.trans (subset_insert _ _), fun U hU => ?_⟩
      obtain ⟨B, hBP, hBU⟩ := hS.2 U hU
      rw [hP, mem_union] at hBP
      have haS : a ∉ S := fun h => ha (hS.1 h)
      rcases hBP with hBM | hBn
      · obtain ⟨_, hins⟩ := hMsub B hBM
        exact ⟨insert a B, hins, by rw [insert_inter_of_notMem haS]; exact hBU⟩
      · exact ⟨B, (mem_filter.1 hBn).1, hBU⟩
    -- Claim B: a set `S` shattered by `Q` gives a shattered set `insert a S` for `F`.
    have claimB : (traces X' Q).image (insert a) ⊆ traces (insert a X') F := by
      intro T hT
      rw [mem_image] at hT
      obtain ⟨S, hS, rfl⟩ := hT
      rw [mem_traces] at hS ⊢
      have haS : a ∉ S := fun h => ha (hS.1 h)
      refine ⟨insert_subset (mem_insert_self _ _) (hS.1.trans (subset_insert _ _)), fun U hU => ?_⟩
      by_cases haU : a ∈ U
      · -- `U = insert a U'`, with `U' = U.erase a ⊆ S`; use a member containing `a`.
        have hU' : U.erase a ⊆ S := by
          intro x hx; rw [mem_erase] at hx
          have := hU hx.2; rw [mem_insert] at this; exact this.resolve_left hx.1
        obtain ⟨B, hBQ, hBU⟩ := hS.2 (U.erase a) hU'
        obtain ⟨hBa, hins⟩ := hMsub B (mem_of_mem_inter_left hBQ)
        refine ⟨insert a B, hins, ?_⟩
        rw [insert_inter_of_mem (mem_insert_self _ _), inter_insert_of_notMem hBa, hBU,
          insert_erase haU]
      · -- `a ∉ U`, so `U ⊆ S`; use a member not containing `a`.
        have hUS : U ⊆ S := by
          intro x hx; have := hU hx; rw [mem_insert] at this
          exact this.resolve_left (fun h => haU (h ▸ hx))
        obtain ⟨B, hBQ, hBU⟩ := hS.2 U hUS
        have hBn := mem_of_mem_inter_right hBQ
        have hBa : a ∉ B := (mem_filter.1 hBn).2
        exact ⟨B, (mem_filter.1 hBn).1, by rw [inter_insert_of_notMem hBa]; exact hBU⟩
    -- The two contributions are disjoint (one has sets avoiding `a`, the other all contain `a`).
    have hdisj : Disjoint (traces X' P) ((traces X' Q).image (insert a)) := by
      rw [disjoint_left]
      intro S hS hS'
      have haS : a ∉ S := fun h => ha ((mem_traces.1 hS).1 h)
      rw [mem_image] at hS'
      obtain ⟨_, _, rfl⟩ := hS'
      exact haS (mem_insert_self _ _)
    -- `insert a` is injective on `traces X' Q` (those sets avoid `a`).
    have hinjcard : ((traces X' Q).image (insert a)).card = (traces X' Q).card := by
      refine card_image_of_injOn ?_
      intro S hS T hT h
      have haS : a ∉ S := fun hx => ha ((mem_traces.1 hS).1 hx)
      have haT : a ∉ T := fun hx => ha ((mem_traces.1 hT).1 hx)
      rw [← erase_insert haS, ← erase_insert haT, h]
    -- Put it together.
    calc F.card = P.card + Q.card := hFPQ
      _ ≤ (traces X' P).card + (traces X' Q).card := Nat.add_le_add ihP ihQ
      _ = (traces X' P).card + ((traces X' Q).image (insert a)).card := by rw [hinjcard]
      _ = ((traces X' P) ∪ (traces X' Q).image (insert a)).card := (card_union_of_disjoint hdisj).symm
      _ ≤ (traces (insert a X') F).card := card_le_card (union_subset claimA claimB)

/-! ## VC dimension and the counting bound -/

variable [Fintype α]

/-- VC dimension of `𝒜`: the size of the largest set it shatters. -/
def vcDim (𝒜 : Finset (Finset α)) : ℕ := (traces univ 𝒜).sup Finset.card

/-- The number of shattered sets is at most the number of subsets of size `≤ d`. -/
theorem card_traces_le_sum (𝒜 : Finset (Finset α)) :
    (traces univ 𝒜).card ≤ ∑ k ∈ Finset.range (vcDim 𝒜 + 1), (Fintype.card α).choose k := by
  rw [Nat.range_succ_eq_Iic]
  calc (traces univ 𝒜).card
      ≤ ((Iic (vcDim 𝒜)).biUnion fun k => powersetCard k univ).card := by
        refine card_le_card fun S hS => ?_
        rw [mem_biUnion]
        refine ⟨S.card, mem_Iic.2 (le_sup hS), ?_⟩
        rw [mem_powersetCard_univ]
    _ ≤ ∑ k ∈ Iic (vcDim 𝒜), (powersetCard k (univ : Finset α)).card := card_biUnion_le
    _ = ∑ k ∈ Iic (vcDim 𝒜), (Fintype.card α).choose k := by
        simp_rw [card_powersetCard, card_univ]

/-! ## Sauer–Shelah lemma (course form) -/

/-- **Sauer–Shelah lemma.** A concept class `𝒜` over an `n`-point ground set has size at
most the sum of binomial coefficients up to its VC dimension `d`:
`|𝒜| ≤ ∑_{k=0}^{d} C(n, k)`. -/
theorem card_le_sum_choose (𝒜 : Finset (Finset α)) :
    𝒜.card ≤ ∑ k ∈ Finset.range (vcDim 𝒜 + 1), (Fintype.card α).choose k :=
  (pajor univ 𝒜 fun A _ => subset_univ A).trans (card_traces_le_sum 𝒜)

/-! ## Validation instances (see REPORT.md "Verification") -/

-- Empty class: trivial.
example : (∅ : Finset (Finset (Fin 5))).card
    ≤ ∑ k ∈ Finset.range (vcDim (∅ : Finset (Finset (Fin 5))) + 1), (5).choose k :=
  card_le_sum_choose _

-- Full powerset over `Fin 4` is fully shattered: `d = 4`, bound is `16 ≤ 16` (tight).
example : vcDim ((univ : Finset (Fin 4)).powerset) = 4 := by native_decide

example : ((univ : Finset (Fin 4)).powerset).card
    ≤ ∑ k ∈ Finset.range (vcDim ((univ : Finset (Fin 4)).powerset) + 1),
        (Fintype.card (Fin 4)).choose k :=
  card_le_sum_choose _

end SauerShelah

#print axioms SauerShelah.card_le_sum_choose
