// Lean compiler output
// Module: Project.SauerShelah
// Imports: public import Init public meta import Init public import Mathlib.Data.Finset.Powerset public import Mathlib.Data.Fintype.Powerset public import Mathlib.Order.Interval.Finset.Nat public import Mathlib.Algebra.BigOperators.Group.Finset.Basic
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lp_mathlib_Multiset_ndinter___redArg(lean_object*, lean_object*, lean_object*);
uint8_t l_List_decidablePerm___redArg(lean_object*, lean_object*, lean_object*);
uint8_t lp_mathlib_Finset_decidableExistsAndFinset___redArg(lean_object*, lean_object*);
lean_object* lp_mathlib_Finset_powerset___redArg(lean_object*);
uint8_t lp_mathlib_Multiset_decidableDforallMultiset___redArg(lean_object*, lean_object*);
lean_object* lp_mathlib_Multiset_filter___redArg(lean_object*, lean_object*);
lean_object* lp_mathlib_Finset_card___boxed(lean_object*, lean_object*);
extern lean_object* lp_mathlib_instDistribLatticeNat;
lean_object* lp_mathlib_Finset_sup___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_traces___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_traces(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_Project_SauerShelah_vcDim___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_mathlib_Finset_card___boxed, .m_arity = 2, .m_num_fixed = 1, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))} };
static const lean_object* lp_Project_SauerShelah_vcDim___redArg___closed__0 = (const lean_object*)&lp_Project_SauerShelah_vcDim___redArg___closed__0_value;
LEAN_EXPORT lean_object* lp_Project_SauerShelah_vcDim___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_Project_SauerShelah_vcDim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__0(lean_object* v_inst_1_, lean_object* v_T_2_, lean_object* v_a_3_, lean_object* v_a_4_){
_start:
{
lean_object* v___x_5_; uint8_t v___x_6_; 
lean_inc_ref(v_inst_1_);
v___x_5_ = lp_mathlib_Multiset_ndinter___redArg(v_inst_1_, v_a_4_, v_T_2_);
v___x_6_ = l_List_decidablePerm___redArg(v_inst_1_, v___x_5_, v_a_3_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__0___boxed(lean_object* v_inst_7_, lean_object* v_T_8_, lean_object* v_a_9_, lean_object* v_a_10_){
_start:
{
uint8_t v_res_11_; lean_object* v_r_12_; 
v_res_11_ = lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__0(v_inst_7_, v_T_8_, v_a_9_, v_a_10_);
v_r_12_ = lean_box(v_res_11_);
return v_r_12_;
}
}
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__1(lean_object* v_inst_13_, lean_object* v_T_14_, lean_object* v_F_15_, lean_object* v_a_16_, lean_object* v_h_17_){
_start:
{
lean_object* v___f_18_; uint8_t v___x_19_; 
v___f_18_ = lean_alloc_closure((void*)(lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__0___boxed), 4, 3);
lean_closure_set(v___f_18_, 0, v_inst_13_);
lean_closure_set(v___f_18_, 1, v_T_14_);
lean_closure_set(v___f_18_, 2, v_a_16_);
v___x_19_ = lp_mathlib_Finset_decidableExistsAndFinset___redArg(v_F_15_, v___f_18_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__1___boxed(lean_object* v_inst_20_, lean_object* v_T_21_, lean_object* v_F_22_, lean_object* v_a_23_, lean_object* v_h_24_){
_start:
{
uint8_t v_res_25_; lean_object* v_r_26_; 
v_res_25_ = lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__1(v_inst_20_, v_T_21_, v_F_22_, v_a_23_, v_h_24_);
v_r_26_ = lean_box(v_res_25_);
return v_r_26_;
}
}
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg(lean_object* v_inst_27_, lean_object* v_F_28_, lean_object* v_T_29_){
_start:
{
lean_object* v___f_30_; lean_object* v___x_31_; uint8_t v___x_32_; 
lean_inc(v_T_29_);
v___f_30_ = lean_alloc_closure((void*)(lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___lam__1___boxed), 5, 3);
lean_closure_set(v___f_30_, 0, v_inst_27_);
lean_closure_set(v___f_30_, 1, v_T_29_);
lean_closure_set(v___f_30_, 2, v_F_28_);
v___x_31_ = lp_mathlib_Finset_powerset___redArg(v_T_29_);
v___x_32_ = lp_mathlib_Multiset_decidableDforallMultiset___redArg(v___x_31_, v___f_30_);
return v___x_32_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg___boxed(lean_object* v_inst_33_, lean_object* v_F_34_, lean_object* v_T_35_){
_start:
{
uint8_t v_res_36_; lean_object* v_r_37_; 
v_res_36_ = lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg(v_inst_33_, v_F_34_, v_T_35_);
v_r_37_ = lean_box(v_res_36_);
return v_r_37_;
}
}
LEAN_EXPORT uint8_t lp_Project_SauerShelah_instDecidablePredFinsetShatters(lean_object* v_00_u03b1_38_, lean_object* v_inst_39_, lean_object* v_F_40_, lean_object* v_T_41_){
_start:
{
uint8_t v___x_42_; 
v___x_42_ = lp_Project_SauerShelah_instDecidablePredFinsetShatters___redArg(v_inst_39_, v_F_40_, v_T_41_);
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_instDecidablePredFinsetShatters___boxed(lean_object* v_00_u03b1_43_, lean_object* v_inst_44_, lean_object* v_F_45_, lean_object* v_T_46_){
_start:
{
uint8_t v_res_47_; lean_object* v_r_48_; 
v_res_47_ = lp_Project_SauerShelah_instDecidablePredFinsetShatters(v_00_u03b1_43_, v_inst_44_, v_F_45_, v_T_46_);
v_r_48_ = lean_box(v_res_47_);
return v_r_48_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_traces___redArg(lean_object* v_inst_49_, lean_object* v_X_50_, lean_object* v_F_51_){
_start:
{
lean_object* v___x_52_; lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_52_ = lean_alloc_closure((void*)(lp_Project_SauerShelah_instDecidablePredFinsetShatters___boxed), 4, 3);
lean_closure_set(v___x_52_, 0, lean_box(0));
lean_closure_set(v___x_52_, 1, v_inst_49_);
lean_closure_set(v___x_52_, 2, v_F_51_);
v___x_53_ = lp_mathlib_Finset_powerset___redArg(v_X_50_);
v___x_54_ = lp_mathlib_Multiset_filter___redArg(v___x_52_, v___x_53_);
return v___x_54_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_traces(lean_object* v_00_u03b1_55_, lean_object* v_inst_56_, lean_object* v_X_57_, lean_object* v_F_58_){
_start:
{
lean_object* v___x_59_; 
v___x_59_ = lp_Project_SauerShelah_traces___redArg(v_inst_56_, v_X_57_, v_F_58_);
return v___x_59_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_vcDim___redArg(lean_object* v_inst_61_, lean_object* v_inst_62_, lean_object* v_00_U0001d49c_63_){
_start:
{
lean_object* v___x_64_; lean_object* v_toSemilatticeSup_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; 
v___x_64_ = lp_mathlib_instDistribLatticeNat;
v_toSemilatticeSup_65_ = lean_ctor_get(v___x_64_, 0);
v___x_66_ = lean_unsigned_to_nat(0u);
v___x_67_ = lp_Project_SauerShelah_traces___redArg(v_inst_61_, v_inst_62_, v_00_U0001d49c_63_);
v___x_68_ = ((lean_object*)(lp_Project_SauerShelah_vcDim___redArg___closed__0));
lean_inc_ref(v_toSemilatticeSup_65_);
v___x_69_ = lp_mathlib_Finset_sup___redArg(v_toSemilatticeSup_65_, v___x_66_, v___x_67_, v___x_68_);
return v___x_69_;
}
}
LEAN_EXPORT lean_object* lp_Project_SauerShelah_vcDim(lean_object* v_00_u03b1_70_, lean_object* v_inst_71_, lean_object* v_inst_72_, lean_object* v_00_U0001d49c_73_){
_start:
{
lean_object* v___x_74_; 
v___x_74_ = lp_Project_SauerShelah_vcDim___redArg(v_inst_71_, v_inst_72_, v_00_U0001d49c_73_);
return v___x_74_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Finset_Powerset(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Fintype_Powerset(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Order_Interval_Finset_Nat(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_BigOperators_Group_Finset_Basic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_Project_Project_SauerShelah(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Finset_Powerset(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Fintype_Powerset(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Order_Interval_Finset_Nat(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Algebra_BigOperators_Group_Finset_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
