import RSICCC

namespace RSICCC
namespace M1

universe u

/-!
Concrete M1 closure for the frozen `Set^(omega^op)` target.

The exponential is represented at stage `n` by a compatible family of maps
through stages `0..n`. Restriction drops the newest stage. This is the standard
Kripke/presheaf exponential specialized to the successor-chain presentation
used by `TreeObj`.
-/

def ExpRaw (A B : TreeObj.{u}) : Nat → Type u
  | 0 => A.Obj 0 → B.Obj 0
  | n + 1 => (A.Obj (n + 1) → B.Obj (n + 1)) × ExpRaw A B n

namespace ExpRaw

def app (A B : TreeObj.{u}) :
    (n : Nat) → ExpRaw A B n → A.Obj n → B.Obj n
  | 0, f, a => f a
  | _ + 1, f, a => f.1 a

end ExpRaw

def ExpCompatible (A B : TreeObj.{u}) :
    (n : Nat) → ExpRaw A B n → Prop
  | 0, _ => True
  | n + 1, f =>
      ExpCompatible A B n f.2 ∧
        ∀ a, B.res n (f.1 a) = ExpRaw.app A B n f.2 (A.res n a)

abbrev ExpStage (A B : TreeObj.{u}) (n : Nat) :=
  { f : ExpRaw A B n // ExpCompatible A B n f }

def expRes (A B : TreeObj.{u}) (n : Nat) :
    ExpStage A B (n + 1) → ExpStage A B n
  | ⟨f, h⟩ => ⟨f.2, h.1⟩

def kripkeExpObj (A B : TreeObj.{u}) : TreeObj.{u} where
  Obj := ExpStage A B
  res := expRes A B

def expApply (A B : TreeObj.{u}) (n : Nat)
    (f : ExpStage A B n) (a : A.Obj n) : B.Obj n :=
  ExpRaw.app A B n f.1 a

def curryRaw {X A B : TreeObj.{u}}
    (f : TreeHom (prodObj X A) B) :
    (n : Nat) → X.Obj n → ExpRaw A B n
  | 0, x => fun a => f.app 0 (x, a)
  | n + 1, x =>
      (fun a => f.app (n + 1) (x, a), curryRaw f n (X.res n x))

theorem curryRaw_app {X A B : TreeObj.{u}}
    (f : TreeHom (prodObj X A) B)
    (n : Nat) (x : X.Obj n) (a : A.Obj n) :
    ExpRaw.app A B n (curryRaw f n x) a = f.app n (x, a) := by
  cases n <;> rfl

theorem curryRaw_compatible {X A B : TreeObj.{u}}
    (f : TreeHom (prodObj X A) B) :
    ∀ n x, ExpCompatible A B n (curryRaw f n x) := by
  intro n
  induction n with
  | zero =>
      intro x
      trivial
  | succ n ih =>
      intro x
      constructor
      · exact ih (X.res n x)
      · intro a
        calc
          B.res n (f.app (n + 1) (x, a)) =
              f.app n (X.res n x, A.res n a) := by
                simpa [prodObj] using f.natural n (x, a)
          _ = ExpRaw.app A B n
                (curryRaw f n (X.res n x)) (A.res n a) :=
              (curryRaw_app f n (X.res n x) (A.res n a)).symm

def expEval (A B : TreeObj.{u}) :
    TreeHom (prodObj (kripkeExpObj A B) A) B where
  app := fun n p => expApply A B n p.1 p.2
  natural := by
    intro n p
    change
      B.res n (ExpRaw.app A B (n + 1) p.1.1 p.2) =
        ExpRaw.app A B n p.1.1.2 (A.res n p.2)
    exact p.1.2.2 p.2

def expCurry {X A B : TreeObj.{u}}
    (f : TreeHom (prodObj X A) B) :
    TreeHom X (kripkeExpObj A B) where
  app := fun n x => ⟨curryRaw f n x, curryRaw_compatible f n x⟩
  natural := by
    intro n x
    apply Subtype.ext
    rfl

def expUncurry {X A B : TreeObj.{u}}
    (g : TreeHom X (kripkeExpObj A B)) :
    TreeHom (prodObj X A) B :=
  TreeHom.comp (expEval A B)
    (pairHom (TreeHom.comp g (fstHom X A)) (sndHom X A))

theorem exp_beta {X A B : TreeObj.{u}}
    (f : TreeHom (prodObj X A) B)
    (n : Nat) (x : X.Obj n) (a : A.Obj n) :
    (expEval A B).app n ((expCurry f).app n x, a) =
      f.app n (x, a) := by
  simpa [expEval, expApply, expCurry] using curryRaw_app f n x a

theorem exp_eta {X A B : TreeObj.{u}}
    (g : TreeHom X (kripkeExpObj A B)) :
    ∀ n x, (expCurry (expUncurry g)).app n x = g.app n x := by
  intro n
  induction n with
  | zero =>
      intro x
      apply Subtype.ext
      funext a
      rfl
  | succ n ih =>
      intro x
      apply Subtype.ext
      apply Prod.ext
      · funext a
        rfl
      · have hprev :
            (expCurry (expUncurry g)).app n (X.res n x) =
              expRes A B n (g.app (n + 1) x) := by
          calc
            (expCurry (expUncurry g)).app n (X.res n x) =
                g.app n (X.res n x) := ih (X.res n x)
            _ = expRes A B n (g.app (n + 1) x) :=
                (g.natural n x).symm
        simpa [expCurry, curryRaw, expRes] using congrArg Subtype.val hprev

def kripkeExponential (X A B : TreeObj.{u}) :
    KripkeExponentialContract X A B where
  Exp := kripkeExpObj A B
  eval := expEval A B
  curry := expCurry
  uncurry := expUncurry
  beta := exp_beta
  eta := exp_eta

theorem concrete_kripke_exponential_exists (X A B : TreeObj.{u}) :
    Nonempty (KripkeExponentialContract X A B) :=
  ⟨kripkeExponential X A B⟩

/-! Typed reflection is now connected to the concrete exponential layer. -/

def progObj (τ : Ty) : TreeObj := constObj (Prog τ)

def denObj (τ : Ty) : TreeObj := constObj (Denote τ)

def runHom (τ : Ty) : TreeHom (progObj τ) (Later (denObj τ)) where
  app := fun n p => (run p).val n
  natural := by
    intro n p
    exact (run p).natural n

def terminalObj : TreeObj := constObj PUnit

def runProductHom (τ : Ty) :
    TreeHom (prodObj terminalObj (progObj τ)) (Later (denObj τ)) :=
  TreeHom.comp (runHom τ) (sndHom terminalObj (progObj τ))

def typedRunContract (τ : Ty) :
    KripkeExponentialContract terminalObj (progObj τ) (Later (denObj τ)) :=
  kripkeExponential terminalObj (progObj τ) (Later (denObj τ))

def runCurried (τ : Ty) : TreeHom terminalObj (typedRunContract τ).Exp :=
  (typedRunContract τ).curry (runProductHom τ)

theorem typed_run_exponential_beta (τ : Ty) (n : Nat) (p : Prog τ) :
    (typedRunContract τ).eval.app n
      ((runCurried τ).app n PUnit.unit, p) =
        (runHom τ).app n p := by
  simpa [runProductHom] using
    (typedRunContract τ).beta (runProductHom τ) n PUnit.unit p

theorem typed_quote_run_exponential_adequacy
    (τ : Ty) (t : Term τ) (n : Nat) :
    (typedRunContract τ).eval.app n
      ((runCurried τ).app n PUnit.unit, quote t) =
        (run (quote t)).val n := by
  simpa [runHom] using typed_run_exponential_beta τ n (quote t)

/-!
Exact admitted refinement domain and frozen parity-checker certificate layer.
This mirrors the finite checker predicates while leaving cryptographic byte
binding to the already content-addressed Python/manifest evidence.
-/

abbrev ParityInput := Fin 16

def parityAnswer (x : ParityInput) : Bool := x.val % 2 == 0

def parityBaseline : RepProgram ParityInput Bool where
  run := fun x => if x.val < 4 then some (parityAnswer x) else none
  cost := 40

def parityCapability : RepProgram ParityInput Bool where
  run := fun x => some (parityAnswer x)
  cost := 40

def parityOptimized : RepProgram ParityInput Bool where
  run := fun x => some (parityAnswer x)
  cost := 10

def ParitySafe (p : RepProgram ParityInput Bool) : Prop :=
  ∀ x y, p.run x = some y → y = parityAnswer x

def StrictCapability {α : Type u} {β : Type u}
    (old new : RepProgram α β) : Prop :=
  ∃ x, old.run x = none ∧ ∃ y, new.run x = some y

def SameAnswers {α : Type u} {β : Type u}
    (old new : RepProgram α β) : Prop :=
  ∀ x, old.run x = new.run x

inductive ImprovementMode where
  | capabilityExtension
  | semanticsPreservingOptimization
  deriving DecidableEq

def ModeImproves {α : Type u} {β : Type u}
    (mode : ImprovementMode) (old new : RepProgram α β) : Prop :=
  match mode with
  | .capabilityExtension => StrictCapability old new
  | .semanticsPreservingOptimization =>
      SameAnswers old new ∧ QualityImproves old new

theorem parityCapability_safe : ParitySafe parityCapability := by
  intro x y h
  simpa [parityCapability] using h.symm

theorem parityBaseline_refines_capability :
    SemRefines parityBaseline parityCapability := by
  intro x y h
  by_cases hx : x.val < 4
  · simpa [parityBaseline, parityCapability, hx] using h
  · simp [parityBaseline, hx] at h

def parityWitness : ParityInput := ⟨4, by decide⟩

theorem parityCapability_is_strict_extension :
    StrictCapability parityBaseline parityCapability := by
  refine ⟨parityWitness, ?_, ?_⟩
  · rfl
  · exact ⟨parityAnswer parityWitness, rfl⟩

theorem parityCapability_refines_optimized :
    SemRefines parityCapability parityOptimized := by
  intro x y h
  simpa [parityCapability, parityOptimized] using h

theorem parityOptimization_same_answers :
    SameAnswers parityCapability parityOptimized := by
  intro x
  rfl

theorem parityOptimization_quality :
    QualityImproves parityCapability parityOptimized := by
  show (10 : Nat) < 40
  decide

structure FrozenCandidate where
  candidateId : String
  digest : String
  contextId : String
  kernelId : String
  rep : RepProgram ParityInput Bool

def baselineDigest : String :=
  "8b00933f5ccf3d497f12b4d11ea547bede001afc95508548b097ad5d593d677c"

def capabilityDigest : String :=
  "4e3496acb09a7356e5d85f4e8fbf713a05c31cdf16c02cfc07829068ea26135c"

def optimizedDigest : String :=
  "2a9f139d25726a857cab5a5d10bad6313d18813f64f2daa9998c32d10d1adc13"

def admittedDigest (candidateId : String) : Option String :=
  if candidateId = "baseline" then some baselineDigest
  else if candidateId = "capability-extension" then some capabilityDigest
  else if candidateId = "optimized-equivalent" then some optimizedDigest
  else none

def CandidateBound (c : FrozenCandidate) : Prop :=
  c.contextId = fixedContextId ∧
  c.kernelId = fixedKernelId ∧
  admittedDigest c.candidateId = some c.digest

def frozenBaseline : FrozenCandidate where
  candidateId := "baseline"
  digest := baselineDigest
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityBaseline

def frozenCapability : FrozenCandidate where
  candidateId := "capability-extension"
  digest := capabilityDigest
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityCapability

def frozenOptimized : FrozenCandidate where
  candidateId := "optimized-equivalent"
  digest := optimizedDigest
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityOptimized

structure FrozenTransition where
  old : FrozenCandidate
  new : FrozenCandidate
  mode : ImprovementMode
  baseDigest : String
  candidateDigest : String
  proposalDigest : String
  serializedBytes : Nat

def capabilityTransition : FrozenTransition where
  old := frozenBaseline
  new := frozenCapability
  mode := .capabilityExtension
  baseDigest := baselineDigest
  candidateDigest := capabilityDigest
  proposalDigest :=
    "83ad17c3e367fcc026c276672073d71bf0e2dc301edfed194c8efb73c1afda12"
  serializedBytes := 527

def optimizationTransition : FrozenTransition where
  old := frozenCapability
  new := frozenOptimized
  mode := .semanticsPreservingOptimization
  baseDigest := capabilityDigest
  candidateDigest := optimizedDigest
  proposalDigest :=
    "a37dfe285c727cc414ec3805954d91552cb96fa1a4157eebb634bd35ca13e5be"
  serializedBytes := 540

structure FrozenCheckerCertificate (t : FrozenTransition) : Prop where
  baseIdentity : t.baseDigest = t.old.digest
  candidateIdentity : t.candidateDigest = t.new.digest
  baseBound : CandidateBound t.old
  candidateBound : CandidateBound t.new
  serializedBound : t.serializedBytes ≤ 4096
  declaredCostBound : t.new.rep.cost ≤ 10000
  safeNew : ParitySafe t.new.rep
  semanticRefinement : SemRefines t.old.rep t.new.rep
  strictProgress : ModeImproves t.mode t.old.rep t.new.rep

def capabilityCertificate : FrozenCheckerCertificate capabilityTransition where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := by decide
  candidateBound := by decide
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := parityCapability_safe
  semanticRefinement := parityBaseline_refines_capability
  strictProgress := parityCapability_is_strict_extension

def optimizationCertificate : FrozenCheckerCertificate optimizationTransition where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := by decide
  candidateBound := by decide
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := parityCapability_safe
  semanticRefinement := parityCapability_refines_optimized
  strictProgress := ⟨parityOptimization_same_answers, parityOptimization_quality⟩

def transitionEnvelope (t : FrozenTransition) : BoundEnvelope where
  contextId := t.new.contextId
  kernelId := t.new.kernelId

def transitionTrust (t : FrozenTransition) : TrustClaims where
  certificateValid := FrozenCheckerCertificate t
  contextIntegrity := t.new.contextId = fixedContextId
  kernelFixed := t.new.kernelId = fixedKernelId
  resourcesOK := t.serializedBytes ≤ 4096 ∧ t.new.rep.cost ≤ 10000

def evidenceFromCertificate (t : FrozenTransition)
    (cert : FrozenCheckerCertificate t) :
    AdmissionEvidence t.old.rep t.new.rep (transitionTrust t)
      (transitionEnvelope t) where
  accepted := true
  semanticSoundness := fun _ => cert.semanticRefinement
  certificateSoundness := fun _ => cert
  contextSoundness := fun _ => cert.candidateBound.1
  kernelSoundness := fun _ => cert.candidateBound.2.1
  resourceSoundness := fun _ => ⟨cert.serializedBound, cert.declaredCostBound⟩
  bindingSoundness := fun _ =>
    ⟨cert.candidateBound.1, cert.candidateBound.2.1⟩

structure CompleteGuardedStepResult (t : FrozenTransition) : Prop where
  abstractPreservation :
    AcceptedStepResult t.old.rep t.new.rep (transitionTrust t)
      (transitionEnvelope t) true
  checkerCertificate : FrozenCheckerCertificate t
  strictProgress : ModeImproves t.mode t.old.rep t.new.rep
  guardedStage :
    ∀ n, (stageProgram (admitProgram t.old.rep t.new.rep true)).val (n + 1) =
      t.new.rep
  formalObjectBound :
    formalObjectSHA256 =
      "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc"

theorem completeStepFromCertificate (t : FrozenTransition)
    (cert : FrozenCheckerCertificate t) : CompleteGuardedStepResult t := by
  let evidence := evidenceFromCertificate t cert
  have preserved :
      AcceptedStepResult t.old.rep t.new.rep (transitionTrust t)
        (transitionEnvelope t) true :=
    one_guarded_replacement_step t.old.rep t.new.rep
      (transitionTrust t) (transitionEnvelope t) evidence rfl
  refine {
    abstractPreservation := preserved
    checkerCertificate := cert
    strictProgress := cert.strictProgress
    guardedStage := ?_
    formalObjectBound := rfl
  }
  intro n
  simpa [admitProgram] using stageProgram_succ t.new.rep n

/-- Exact bounded capability-extension replacement admitted by the frozen checker semantics. -/
theorem one_complete_guarded_capability_replacement :
    CompleteGuardedStepResult capabilityTransition :=
  completeStepFromCertificate capabilityTransition capabilityCertificate

/-- Exact semantics-preserving lower-cost replacement; this discharges the quality branch. -/
theorem one_complete_guarded_optimization_replacement :
    CompleteGuardedStepResult optimizationTransition :=
  completeStepFromCertificate optimizationTransition optimizationCertificate

end M1
end RSICCC
