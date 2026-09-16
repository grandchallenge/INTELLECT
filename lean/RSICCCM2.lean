import RSICCCM1

namespace RSICCC
namespace M2

open M1

/-!
M2 proves closure under succession for the frozen M1 replacement boundary.
The fixed checker itself remains outside this Lean module; exact Python/Lean
identity is replayed by the content-binding tests.
-/

def parityPrefix (limit cost : Nat) : RepProgram ParityInput Bool where
  run := fun x => if x.val < limit then some (parityAnswer x) else none
  cost := cost

theorem parityPrefix_safe (limit cost : Nat) :
    ParitySafe (parityPrefix limit cost) := by
  intro x y h
  by_cases hx : x.val < limit
  · simpa [parityPrefix, hx] using h.symm
  · simp [parityPrefix, hx] at h

theorem parityPrefix_refines
    {oldLimit newLimit oldCost newCost : Nat}
    (hLimits : oldLimit ≤ newLimit) :
    SemRefines (parityPrefix oldLimit oldCost)
      (parityPrefix newLimit newCost) := by
  intro x y h
  by_cases hx : x.val < oldLimit
  · have hxNew : x.val < newLimit := Nat.lt_of_lt_of_le hx hLimits
    simpa [parityPrefix, hx, hxNew] using h
  · simp [parityPrefix, hx] at h

theorem parityPrefix_same_answers (limit oldCost newCost : Nat) :
    SameAnswers (parityPrefix limit oldCost) (parityPrefix limit newCost) := by
  intro x
  rfl

theorem parityPrefix_strict
    {oldLimit newLimit oldCost newCost : Nat}
    (hStrict : oldLimit < newLimit)
    (hBound : newLimit ≤ 16) :
    StrictCapability (parityPrefix oldLimit oldCost)
      (parityPrefix newLimit newCost) := by
  have hOldBound : oldLimit < 16 := Nat.lt_of_lt_of_le hStrict hBound
  let x : ParityInput := ⟨oldLimit, hOldBound⟩
  refine ⟨x, ?_, ?_⟩
  · simp [parityPrefix, x]
  · refine ⟨parityAnswer x, ?_⟩
    simp [parityPrefix, x, hStrict]

/-! Exact accepted candidate identities replayed from the frozen checker. -/

def s0 : FrozenCandidate where
  candidateId := "baseline"
  digest := "8b00933f5ccf3d497f12b4d11ea547bede001afc95508548b097ad5d593d677c"
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityPrefix 4 40

def s1 : FrozenCandidate where
  candidateId := "m2-capability-0-7"
  digest := "6d2f3dedffd06f9abfe3d767c3b0686d40c80bca9948b62ed2c9a2aa572852e5"
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityPrefix 8 40

def s2 : FrozenCandidate where
  candidateId := "m2-optimized-0-7"
  digest := "07b96e8d3d78f13772e3942cbfafeb00ed1a65ebd5cd0539b07458a1fc13d2cd"
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityPrefix 8 20

def s3 : FrozenCandidate where
  candidateId := "m2-capability-0-11"
  digest := "cd7fdccfda70687abb71a937505abbfd3c9e208015e37d3cea7818759328b3e8"
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityPrefix 12 20

def s4 : FrozenCandidate where
  candidateId := "m2-capability-0-15"
  digest := "101c289d2575c798dccc7ffc25faaeffc0fa3c18b7b98000e8a6cb02f204eabb"
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityPrefix 16 20

def s5 : FrozenCandidate where
  candidateId := "m2-optimized-0-15"
  digest := "4f0b7070b8e32d839f2d296bea9bb4ce3981aa0100e71605f4cf3dc45fe02b03"
  contextId := fixedContextId
  kernelId := fixedKernelId
  rep := parityPrefix 16 10

def m2AdmittedDigest (candidateId : String) : Option String :=
  if candidateId = "baseline" then some s0.digest
  else if candidateId = "m2-capability-0-7" then some s1.digest
  else if candidateId = "m2-optimized-0-7" then some s2.digest
  else if candidateId = "m2-capability-0-11" then some s3.digest
  else if candidateId = "m2-capability-0-15" then some s4.digest
  else if candidateId = "m2-optimized-0-15" then some s5.digest
  else none

def M2CandidateBound (c : FrozenCandidate) : Prop :=
  c.contextId = fixedContextId ∧
  c.kernelId = fixedKernelId ∧
  m2AdmittedDigest c.candidateId = some c.digest

theorem s0_bound : M2CandidateBound s0 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [m2AdmittedDigest, s0]

theorem s1_bound : M2CandidateBound s1 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [m2AdmittedDigest, s1]

theorem s2_bound : M2CandidateBound s2 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [m2AdmittedDigest, s2]

theorem s3_bound : M2CandidateBound s3 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [m2AdmittedDigest, s3]

theorem s4_bound : M2CandidateBound s4 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [m2AdmittedDigest, s4]

theorem s5_bound : M2CandidateBound s5 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [m2AdmittedDigest, s5]

/-! Exact accepted transition identities. -/

def t01 : FrozenTransition where
  old := s0
  new := s1
  mode := .capabilityExtension
  baseDigest := s0.digest
  candidateDigest := s1.digest
  proposalDigest := "c48b9eb1f664658e4e00e7192317b36be38e389804087c71d3f3bfc5afffe690"
  serializedBytes := 520

def t12 : FrozenTransition where
  old := s1
  new := s2
  mode := .semanticsPreservingOptimization
  baseDigest := s1.digest
  candidateDigest := s2.digest
  proposalDigest := "5d132973675d8e54fcd31a12c7b2b9ff4ce520aa52f7dd1da6750fc00652a30a"
  serializedBytes := 532

def t23 : FrozenTransition where
  old := s2
  new := s3
  mode := .capabilityExtension
  baseDigest := s2.digest
  candidateDigest := s3.digest
  proposalDigest := "e35745452befafd849fc7d83ff2cc630e8f93538733e9a72f8418058b7f715e4"
  serializedBytes := 523

def t34 : FrozenTransition where
  old := s3
  new := s4
  mode := .capabilityExtension
  baseDigest := s3.digest
  candidateDigest := s4.digest
  proposalDigest := "205aadc286496c225737d967fab9b07b7f83cf332da1000a1606abbdc543978c"
  serializedBytes := 525

def t45 : FrozenTransition where
  old := s4
  new := s5
  mode := .semanticsPreservingOptimization
  baseDigest := s4.digest
  candidateDigest := s5.digest
  proposalDigest := "a01b2d61440704a22dea5d3252c3bae1d3bf9820029de4667133d7339cba23f7"
  serializedBytes := 537

structure M2CheckerCertificate (t : FrozenTransition) : Prop where
  baseIdentity : t.baseDigest = t.old.digest
  candidateIdentity : t.candidateDigest = t.new.digest
  baseBound : M2CandidateBound t.old
  candidateBound : M2CandidateBound t.new
  serializedBound : t.serializedBytes ≤ 4096
  declaredCostBound : t.new.rep.cost ≤ 10000
  safeNew : ParitySafe t.new.rep
  semanticRefinement : SemRefines t.old.rep t.new.rep
  strictProgress : ModeImproves t.mode t.old.rep t.new.rep

theorem s0_safe : ParitySafe s0.rep := by
  simpa [s0] using parityPrefix_safe 4 40

theorem s1_safe : ParitySafe s1.rep := by
  simpa [s1] using parityPrefix_safe 8 40

theorem s2_safe : ParitySafe s2.rep := by
  simpa [s2] using parityPrefix_safe 8 20

theorem s3_safe : ParitySafe s3.rep := by
  simpa [s3] using parityPrefix_safe 12 20

theorem s4_safe : ParitySafe s4.rep := by
  simpa [s4] using parityPrefix_safe 16 20

theorem s5_safe : ParitySafe s5.rep := by
  simpa [s5] using parityPrefix_safe 16 10

theorem s0_refines_s1 : SemRefines s0.rep s1.rep := by
  simpa [s0, s1] using
    (parityPrefix_refines (oldLimit := 4) (newLimit := 8)
      (oldCost := 40) (newCost := 40) (by decide))

theorem s1_refines_s2 : SemRefines s1.rep s2.rep := by
  simpa [s1, s2] using
    (parityPrefix_refines (oldLimit := 8) (newLimit := 8)
      (oldCost := 40) (newCost := 20) (by decide))

theorem s2_refines_s3 : SemRefines s2.rep s3.rep := by
  simpa [s2, s3] using
    (parityPrefix_refines (oldLimit := 8) (newLimit := 12)
      (oldCost := 20) (newCost := 20) (by decide))

theorem s3_refines_s4 : SemRefines s3.rep s4.rep := by
  simpa [s3, s4] using
    (parityPrefix_refines (oldLimit := 12) (newLimit := 16)
      (oldCost := 20) (newCost := 20) (by decide))

theorem s4_refines_s5 : SemRefines s4.rep s5.rep := by
  simpa [s4, s5] using
    (parityPrefix_refines (oldLimit := 16) (newLimit := 16)
      (oldCost := 20) (newCost := 10) (by decide))

theorem s0_s1_strict : StrictCapability s0.rep s1.rep := by
  simpa [s0, s1] using
    (parityPrefix_strict (oldLimit := 4) (newLimit := 8)
      (oldCost := 40) (newCost := 40) (by decide) (by decide))

theorem s2_s3_strict : StrictCapability s2.rep s3.rep := by
  simpa [s2, s3] using
    (parityPrefix_strict (oldLimit := 8) (newLimit := 12)
      (oldCost := 20) (newCost := 20) (by decide) (by decide))

theorem s3_s4_strict : StrictCapability s3.rep s4.rep := by
  simpa [s3, s4] using
    (parityPrefix_strict (oldLimit := 12) (newLimit := 16)
      (oldCost := 20) (newCost := 20) (by decide) (by decide))

theorem s1_s2_quality :
    ModeImproves .semanticsPreservingOptimization s1.rep s2.rep := by
  constructor
  · simpa [s1, s2] using parityPrefix_same_answers 8 40 20
  · show (20 : Nat) < 40
    decide

theorem s4_s5_quality :
    ModeImproves .semanticsPreservingOptimization s4.rep s5.rep := by
  constructor
  · simpa [s4, s5] using parityPrefix_same_answers 16 20 10
  · show (10 : Nat) < 20
    decide

def c01 : M2CheckerCertificate t01 where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := s0_bound
  candidateBound := s1_bound
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := s1_safe
  semanticRefinement := s0_refines_s1
  strictProgress := s0_s1_strict

def c12 : M2CheckerCertificate t12 where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := s1_bound
  candidateBound := s2_bound
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := s2_safe
  semanticRefinement := s1_refines_s2
  strictProgress := s1_s2_quality

def c23 : M2CheckerCertificate t23 where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := s2_bound
  candidateBound := s3_bound
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := s3_safe
  semanticRefinement := s2_refines_s3
  strictProgress := s2_s3_strict

def c34 : M2CheckerCertificate t34 where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := s3_bound
  candidateBound := s4_bound
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := s4_safe
  semanticRefinement := s3_refines_s4
  strictProgress := s3_s4_strict

def c45 : M2CheckerCertificate t45 where
  baseIdentity := rfl
  candidateIdentity := rfl
  baseBound := s4_bound
  candidateBound := s5_bound
  serializedBound := by decide
  declaredCostBound := by decide
  safeNew := s5_safe
  semanticRefinement := s4_refines_s5
  strictProgress := s4_s5_quality

/-! Each M2 certificate is discharged through the exact M1 preservation theorem. -/

def m2Envelope (t : FrozenTransition) : BoundEnvelope where
  contextId := t.new.contextId
  kernelId := t.new.kernelId

def m2Trust (t : FrozenTransition) : TrustClaims where
  certificateValid := M2CheckerCertificate t
  contextIntegrity := t.new.contextId = fixedContextId
  kernelFixed := t.new.kernelId = fixedKernelId
  resourcesOK := t.serializedBytes ≤ 4096 ∧ t.new.rep.cost ≤ 10000

def evidenceFromM2Certificate (t : FrozenTransition)
    (cert : M2CheckerCertificate t) :
    AdmissionEvidence t.old.rep t.new.rep (m2Trust t) (m2Envelope t) where
  accepted := true
  semanticSoundness := fun _ => cert.semanticRefinement
  certificateSoundness := fun _ => cert
  contextSoundness := fun _ => cert.candidateBound.1
  kernelSoundness := fun _ => cert.candidateBound.2.1
  resourceSoundness := fun _ => ⟨cert.serializedBound, cert.declaredCostBound⟩
  bindingSoundness := fun _ => ⟨cert.candidateBound.1, cert.candidateBound.2.1⟩

def m1ResultFromM2Certificate (t : FrozenTransition)
    (cert : M2CheckerCertificate t) :
    AcceptedStepResult t.old.rep t.new.rep (m2Trust t) (m2Envelope t) true :=
  one_guarded_replacement_step t.old.rep t.new.rep
    (m2Trust t) (m2Envelope t) (evidenceFromM2Certificate t cert) rfl

/-!
A `CertifiedChain a b` is succession by construction: every next transition
starts from the exact candidate produced by the previous transition.
-/

inductive CertifiedChain : FrozenCandidate → FrozenCandidate → Type where
  | nil (c : FrozenCandidate) : CertifiedChain c c
  | cons (t : FrozenTransition)
      (cert : M2CheckerCertificate t)
      (m1 : AcceptedStepResult t.old.rep t.new.rep
        (m2Trust t) (m2Envelope t) true)
      {finish : FrozenCandidate}
      (tail : CertifiedChain t.new finish) :
      CertifiedChain t.old finish

namespace CertifiedChain

def length : {a b : FrozenCandidate} → CertifiedChain a b → Nat
  | _, _, .nil _ => 0
  | _, _, .cons _ _ _ tail => 1 + length tail

end CertifiedChain

theorem chain_semantic_refinement :
    {a b : FrozenCandidate} → CertifiedChain a b → SemRefines a.rep b.rep
  | _, _, .nil c => semRefines_refl c.rep
  | _, _, .cons _ _ m1 tail =>
      semRefines_trans m1.semanticRefinement (chain_semantic_refinement tail)

def Answered (p : RepProgram ParityInput Bool) (x : ParityInput) : Prop :=
  ∃ y, p.run x = some y

theorem semRefines_preserves_answered
    {old new : RepProgram ParityInput Bool}
    (h : SemRefines old new) :
    ∀ x, Answered old x → Answered new x := by
  intro x hx
  rcases hx with ⟨y, hy⟩
  exact ⟨y, h x y hy⟩

theorem chain_preserves_accumulated_obligations
    {a b : FrozenCandidate} (chain : CertifiedChain a b) :
    ∀ x, Answered a.rep x → Answered b.rep x :=
  semRefines_preserves_answered (chain_semantic_refinement chain)

theorem chain_final_bound :
    {a b : FrozenCandidate} →
    CertifiedChain a b → M2CandidateBound a → M2CandidateBound b
  | _, _, .nil _, h => h
  | _, _, .cons _ cert _ tail, _ => chain_final_bound tail cert.candidateBound

theorem chain_final_safe :
    {a b : FrozenCandidate} →
    CertifiedChain a b → ParitySafe a.rep → ParitySafe b.rep
  | _, _, .nil _, h => h
  | _, _, .cons _ cert _ tail, _ => chain_final_safe tail cert.safeNew

structure SequencePreservationResult
    (start finish : FrozenCandidate)
    (chain : CertifiedChain start finish) : Prop where
  semanticRefinement : SemRefines start.rep finish.rep
  obligationsPreserved : ∀ x, Answered start.rep x → Answered finish.rep x
  finalSafe : ParitySafe finish.rep
  startBound : M2CandidateBound start
  finalBound : M2CandidateBound finish
  finalContextFixed : finish.contextId = fixedContextId
  finalKernelFixed : finish.kernelId = fixedKernelId
  formalObjectBound :
    formalObjectSHA256 =
      "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc"

theorem certified_sequence_preservation
    {start finish : FrozenCandidate}
    (chain : CertifiedChain start finish)
    (startBound : M2CandidateBound start)
    (startSafe : ParitySafe start.rep) :
    SequencePreservationResult start finish chain := by
  have finalBound := chain_final_bound chain startBound
  exact {
    semanticRefinement := chain_semantic_refinement chain
    obligationsPreserved := chain_preserves_accumulated_obligations chain
    finalSafe := chain_final_safe chain startSafe
    startBound := startBound
    finalBound := finalBound
    finalContextFixed := finalBound.1
    finalKernelFixed := finalBound.2.1
    formalObjectBound := rfl
  }

def m2Chain : CertifiedChain s0 s5 :=
  .cons t01 c01 (m1ResultFromM2Certificate t01 c01)
    (.cons t12 c12 (m1ResultFromM2Certificate t12 c12)
      (.cons t23 c23 (m1ResultFromM2Certificate t23 c23)
        (.cons t34 c34 (m1ResultFromM2Certificate t34 c34)
          (.cons t45 c45 (m1ResultFromM2Certificate t45 c45)
            (.nil s5)))))

theorem m2_chain_has_five_accepted_steps : m2Chain.length = 5 := rfl

/-- The M2 milestone: M1 preservation composes across the exact five-step chain. -/
theorem one_complete_guarded_replacement_sequence :
    SequencePreservationResult s0 s5 m2Chain :=
  certified_sequence_preservation m2Chain s0_bound s0_safe

/-- Rejected events are stasis and therefore cannot advance the sequence state. -/
theorem rejected_event_stasis (old candidate : RepProgram ParityInput Bool) :
    admitProgram old candidate false = old := by
  exact rejected_step_stasis old candidate false rfl

/-! Cross-language constants independently replayed by Python CI. -/

def m2GenesisDigest : String :=
  "de941aa2dd670273052243d14f50448560b37950b49b4b5bfa5cd48cd961d4a6"

def m2EventChainDigest : String :=
  "47b2a9d249befeaada200e4163235324a2347502478b84f27aa3c4c778ef1da9"

end M2
end RSICCC
