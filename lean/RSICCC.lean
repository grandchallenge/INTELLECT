import Std

namespace RSICCC

/-- Frozen M0 formal-object identity. M1 may not change this digest. -/
def formalObjectSHA256 : String :=
  "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc"

def fixedContextId : String := "parity16-fixed-context-v1"
def fixedKernelId : String := "rsi-ccc-fixed-kernel-v1"

universe u v w

/-
A concrete adjacent-restriction presentation of objects of Set^(omega^op).
Because omega is a linear successor chain, arbitrary restrictions are generated
by repeated application of `res`.
-/
structure TreeObj where
  Obj : Nat → Type u
  res : (n : Nat) → Obj (n + 1) → Obj n

structure TreeHom (X Y : TreeObj.{u}) where
  app : (n : Nat) → X.Obj n → Y.Obj n
  natural : ∀ n x, Y.res n (app (n + 1) x) = app n (X.res n x)

namespace TreeHom

def id (X : TreeObj.{u}) : TreeHom X X where
  app := fun _ x => x
  natural := by
    intro n x
    rfl

def comp {X Y Z : TreeObj.{u}} (g : TreeHom Y Z) (f : TreeHom X Y) :
    TreeHom X Z where
  app := fun n x => g.app n (f.app n x)
  natural := by
    intro n x
    rw [g.natural n (f.app (n + 1) x), f.natural n x]

end TreeHom

def prodObj (X Y : TreeObj.{u}) : TreeObj.{u} where
  Obj := fun n => X.Obj n × Y.Obj n
  res := fun n p => (X.res n p.1, Y.res n p.2)

def fstHom (X Y : TreeObj.{u}) : TreeHom (prodObj X Y) X where
  app := fun _ p => p.1
  natural := by
    intro n p
    rfl

def sndHom (X Y : TreeObj.{u}) : TreeHom (prodObj X Y) Y where
  app := fun _ p => p.2
  natural := by
    intro n p
    rfl

def pairHom {W X Y : TreeObj.{u}} (f : TreeHom W X) (g : TreeHom W Y) :
    TreeHom W (prodObj X Y) where
  app := fun n w => (f.app n w, g.app n w)
  natural := by
    intro n w
    simp [prodObj, f.natural n w, g.natural n w]

theorem fst_pair {W X Y : TreeObj.{u}} (f : TreeHom W X) (g : TreeHom W Y)
    (n : Nat) (w : W.Obj n) :
    (fstHom X Y).app n ((pairHom f g).app n w) = f.app n w := rfl

theorem snd_pair {W X Y : TreeObj.{u}} (f : TreeHom W X) (g : TreeHom W Y)
    (n : Nat) (w : W.Obj n) :
    (sndHom X Y).app n ((pairHom f g).app n w) = g.app n w := rfl

/-- Underlying function-space evaluation. This is the local beta/eta sanity layer. -/
def evalFn {A : Type u} {B : Type v} : (A → B) × A → B :=
  fun p => p.1 p.2

def curryFn {X : Type u} {A : Type v} {B : Type w}
    (f : X × A → B) : X → A → B :=
  fun x a => f (x, a)

def uncurryFn {X : Type u} {A : Type v} {B : Type w}
    (g : X → A → B) : X × A → B :=
  fun p => g p.1 p.2

theorem eval_curry {X : Type u} {A : Type v} {B : Type w}
    (f : X × A → B) (x : X) (a : A) :
    evalFn (curryFn f x, a) = f (x, a) := rfl

theorem uncurry_curry {X : Type u} {A : Type v} {B : Type w}
    (f : X × A → B) :
    uncurryFn (curryFn f) = f := by
  funext p
  rfl

theorem curry_uncurry {X : Type u} {A : Type v} {B : Type w}
    (g : X → A → B) :
    curryFn (uncurryFn g) = g := by
  funext x a
  rfl

/--
Exact M1 obligation for the Kripke exponential in the frozen Set^(omega^op)
model. M1 must construct such a witness for the concrete `TreeObj` semantics;
the laws are named here so they cannot be silently weakened.
-/
structure KripkeExponentialContract (X A B : TreeObj.{u}) where
  Exp : TreeObj.{u}
  eval : TreeHom (prodObj Exp A) B
  curry : TreeHom (prodObj X A) B → TreeHom X Exp
  uncurry : TreeHom X Exp → TreeHom (prodObj X A) B
  beta : ∀ f n x a, eval.app n ((curry f).app n x, a) = f.app n (x, a)
  eta : ∀ g n x, (curry (uncurry g)).app n x = g.app n x

def laterObj (X : TreeObj.{u}) : Nat → Type u
  | 0 => PUnit
  | n + 1 => X.Obj n

def laterRes (X : TreeObj.{u}) :
    (n : Nat) → laterObj X (n + 1) → laterObj X n
  | 0 => fun _ => PUnit.unit
  | n + 1 => X.res n

def Later (X : TreeObj.{u}) : TreeObj.{u} where
  Obj := laterObj X
  res := laterRes X

def nextApp (X : TreeObj.{u}) : (n : Nat) → X.Obj n → (Later X).Obj n
  | 0 => fun _ => PUnit.unit
  | n + 1 => X.res n

def next (X : TreeObj.{u}) : TreeHom X (Later X) where
  app := nextApp X
  natural := by
    intro n x
    cases n <;> rfl

structure Global (X : TreeObj.{u}) where
  val : (n : Nat) → X.Obj n
  natural : ∀ n, X.res n (val (n + 1)) = val n

def mapGlobal {X Y : TreeObj.{u}} (f : TreeHom X Y) (x : Global X) :
    Global Y where
  val := fun n => f.app n (x.val n)
  natural := by
    intro n
    rw [f.natural n (x.val (n + 1)), x.natural n]

def constObj (α : Type u) : TreeObj.{u} where
  Obj := fun _ => α
  res := fun _ x => x

def constGlobal {α : Type u} (a : α) : Global (constObj α) where
  val := fun _ => a
  natural := by
    intro n
    rfl

/-- Stage-indexed guarded fixed-point candidate. -/
def gfixVal {X : TreeObj.{u}} (f : TreeHom (Later X) X) :
    (n : Nat) → X.Obj n
  | 0 => f.app 0 PUnit.unit
  | n + 1 => f.app (n + 1) (gfixVal f n)

theorem gfixVal_natural {X : TreeObj.{u}} (f : TreeHom (Later X) X) :
    ∀ n, X.res n (gfixVal f (n + 1)) = gfixVal f n := by
  intro n
  induction n with
  | zero =>
      simpa [gfixVal, Later, laterRes] using
        f.natural 0 (gfixVal f 0)
  | succ n ih =>
      simpa [gfixVal, Later, laterRes, ih] using
        f.natural (n + 1) (gfixVal f (n + 1))

def gfix {X : TreeObj.{u}} (f : TreeHom (Later X) X) : Global X where
  val := gfixVal f
  natural := gfixVal_natural f

theorem gfix_unfold_zero {X : TreeObj.{u}} (f : TreeHom (Later X) X) :
    (gfix f).val 0 = f.app 0 PUnit.unit := rfl

theorem gfix_unfold_succ {X : TreeObj.{u}} (f : TreeHom (Later X) X)
    (n : Nat) :
    (gfix f).val (n + 1) = f.app (n + 1) ((gfix f).val n) := rfl

/--
Productivity witness: stage n+1 of the fixed point is constructed from the
already available stage n value.
-/
theorem gfix_productive {X : TreeObj.{u}} (f : TreeHom (Later X) X)
    (n : Nat) :
    (gfix f).val (n + 1) = f.app (n + 1) ((gfix f).val n) :=
  gfix_unfold_succ f n

inductive Ty where
  | bool

def Denote : Ty → Type
  | .bool => Bool

inductive Term : Ty → Type
  | lit : Bool → Term .bool

abbrev Prog := Term

def quote {τ : Ty} (t : Term τ) : Prog τ := t

def evalTerm : {τ : Ty} → Term τ → Denote τ
  | .bool, .lit b => b

/-- Closed program evaluation is deliberately staged through `Later`. -/
def run {τ : Ty} (p : Prog τ) :
    Global (Later (constObj (Denote τ))) :=
  mapGlobal (next (constObj (Denote τ))) (constGlobal (evalTerm p))

theorem run_quote_adequacy {τ : Ty} (t : Term τ) :
    run (quote t) =
      mapGlobal (next (constObj (Denote τ))) (constGlobal (evalTerm t)) := rfl

structure RepProgram (α : Type u) (β : Type v) where
  run : α → Option β
  cost : Nat

def SemRefines {α : Type u} {β : Type v}
    (old new : RepProgram α β) : Prop :=
  ∀ x y, old.run x = some y → new.run x = some y

theorem semRefines_refl {α : Type u} {β : Type v}
    (p : RepProgram α β) : SemRefines p p := by
  intro x y h
  exact h

theorem semRefines_trans {α : Type u} {β : Type v}
    {p q r : RepProgram α β} :
    SemRefines p q → SemRefines q r → SemRefines p r := by
  intro hpq hqr x y h
  exact hqr x y (hpq x y h)

def QualityImproves {α : Type u} {β : Type v}
    (old new : RepProgram α β) : Prop :=
  new.cost < old.cost

def composeProgram {α : Type u} {β : Type v} {γ : Type w}
    (g : RepProgram β γ) (f : RepProgram α β) : RepProgram α γ where
  run := fun x =>
    match f.run x with
    | none => none
    | some y => g.run y
  cost := f.cost + g.cost

theorem compose_monotone {α : Type u} {β : Type v} {γ : Type w}
    {f₁ f₂ : RepProgram α β} {g₁ g₂ : RepProgram β γ}
    (hf : SemRefines f₁ f₂) (hg : SemRefines g₁ g₂) :
    SemRefines (composeProgram g₁ f₁) (composeProgram g₂ f₂) := by
  intro x z h
  cases hfx : f₁.run x with
  | none =>
      simp [composeProgram, hfx] at h
  | some y =>
      have hfxy : f₂.run x = some y := hf x y hfx
      have hgyz : g₁.run y = some z := by
        simpa [composeProgram, hfx] using h
      have hgzy : g₂.run y = some z := hg y z hgyz
      simpa [composeProgram, hfxy] using hgzy

def RawRefines {α : Type u} {β : Type v}
    (f g : α → Option β) : Prop :=
  ∀ x y, f x = some y → g x = some y

def BinaryRefines {α : Type u} {β : Type v} {γ : Type w}
    (f g : α → β → Option γ) : Prop :=
  ∀ a b y, f a b = some y → g a b = some y

def curryRun {α : Type u} {β : Type v} {γ : Type w}
    (f : α × β → Option γ) : α → β → Option γ :=
  fun a b => f (a, b)

theorem curry_refinement_compatible {α : Type u} {β : Type v} {γ : Type w}
    {f g : α × β → Option γ} (h : RawRefines f g) :
    BinaryRefines (curryRun f) (curryRun g) := by
  intro a b y hab
  exact h (a, b) y hab

def OptionRefines {β : Type v} (old new : Option β) : Prop :=
  ∀ y, old = some y → new = some y

theorem evaluation_refinement_compatible
    {α : Type u} {β : Type v} {γ : Type w}
    {f g : α → β → Option γ} (h : BinaryRefines f g)
    (a : α) (b : β) :
    OptionRefines (f a b) (g a b) := by
  exact h a b

structure TrustClaims where
  certificateValid : Prop
  contextIntegrity : Prop
  kernelFixed : Prop
  resourcesOK : Prop

structure BoundEnvelope where
  contextId : String
  kernelId : String

def BoundEnvelope.valid (e : BoundEnvelope) : Prop :=
  e.contextId = fixedContextId ∧ e.kernelId = fixedKernelId

structure AdmissionEvidence {α : Type u} {β : Type v}
    (old new : RepProgram α β) (trust : TrustClaims)
    (envelope : BoundEnvelope) where
  accepted : Bool
  semanticSoundness : accepted = true → SemRefines old new
  certificateSoundness : accepted = true → trust.certificateValid
  contextSoundness : accepted = true → trust.contextIntegrity
  kernelSoundness : accepted = true → trust.kernelFixed
  resourceSoundness : accepted = true → trust.resourcesOK
  bindingSoundness : accepted = true → envelope.valid

def admitProgram {α : Type u} {β : Type v}
    (old new : RepProgram α β) (accepted : Bool) : RepProgram α β :=
  if accepted then new else old

theorem rejected_step_stasis {α : Type u} {β : Type v}
    (old new : RepProgram α β) (accepted : Bool)
    (h : accepted = false) :
    admitProgram old new accepted = old := by
  simp [admitProgram, h]

def stageProgram {α : Type u} {β : Type v} (p : RepProgram α β) :
    Global (Later (constObj (RepProgram α β))) :=
  mapGlobal (next (constObj (RepProgram α β))) (constGlobal p)

theorem stageProgram_succ {α : Type u} {β : Type v}
    (p : RepProgram α β) (n : Nat) :
    (stageProgram p).val (n + 1) = p := rfl

structure AcceptedStepResult {α : Type u} {β : Type v}
    (old new : RepProgram α β) (trust : TrustClaims)
    (envelope : BoundEnvelope) (accepted : Bool) : Prop where
  admittedIsNew : admitProgram old new accepted = new
  semanticRefinement : SemRefines old new
  certificateValid : trust.certificateValid
  contextIntegrity : trust.contextIntegrity
  kernelFixed : trust.kernelFixed
  resourcesOK : trust.resourcesOK
  bindingValid : envelope.valid

/--
One mechanically checked guarded self-replacement step at the abstract checker
boundary. The theorem does not assume an oracle: every non-computable
obligation is visible in `AdmissionEvidence`.
-/
theorem one_guarded_replacement_step
    {α : Type u} {β : Type v}
    (old new : RepProgram α β)
    (trust : TrustClaims)
    (envelope : BoundEnvelope)
    (evidence : AdmissionEvidence old new trust envelope)
    (hAccepted : evidence.accepted = true) :
    AcceptedStepResult old new trust envelope evidence.accepted := by
  refine {
    admittedIsNew := ?_
    semanticRefinement := evidence.semanticSoundness hAccepted
    certificateValid := evidence.certificateSoundness hAccepted
    contextIntegrity := evidence.contextSoundness hAccepted
    kernelFixed := evidence.kernelSoundness hAccepted
    resourcesOK := evidence.resourceSoundness hAccepted
    bindingValid := evidence.bindingSoundness hAccepted
  }
  simp [admitProgram, hAccepted]

end RSICCC
