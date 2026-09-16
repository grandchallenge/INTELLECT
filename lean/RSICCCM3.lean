import RSICCCM2Receipts

namespace RSICCC
namespace M3

open M1 M2

/-!
M3 adds a bounded proposer/evidence separation around the exact M2 transition
surface. Proposer-private state is deliberately absent from the authoritative
admission evidence. The executable lane independently checks the corresponding
content-addressed proposal and certificate identities.
-/

structure ProposerPrivateState where
  proposerId : String
  privateStateDigest : String

structure ProposalCommitment (t : FrozenTransition) where
  publicInputDigest : String
  proposalDigest : String
  transcriptDigest : String
  proposalDigestBound : proposalDigest = t.proposalDigest

/--
Authoritative M3 evidence is exactly the M2 checker certificate plus the M1
preservation result it discharges. There is no proposer identity or private
state field in this structure.
-/
structure IndependentAdmissionResult (t : FrozenTransition) : Prop where
  certificate : M2CheckerCertificate t
  preservation : AcceptedStepResult t.old.rep t.new.rep
    (m2Trust t) (m2Envelope t) true

/--
The evaluator consumes proposer-private state only as non-authoritative
metadata. The returned admission evidence is reconstructed solely from the
frozen transition and its checker certificate.
-/
def evaluateIndependent
    (_private : ProposerPrivateState)
    (t : FrozenTransition)
    (cert : M2CheckerCertificate t) :
    IndependentAdmissionResult t where
  certificate := cert
  preservation := m1ResultFromM2Certificate t cert

/--
For identical committed transition bytes and identical independent checker
certificate, changing proposer identity/private state cannot change the
admission/preservation result.
-/
theorem proposer_private_state_noninterference
    (p q : ProposerPrivateState)
    (t : FrozenTransition)
    (cert : M2CheckerCertificate t) :
    evaluateIndependent p t cert = evaluateIndependent q t cert := by
  rfl

/-- The authoritative certificate digest is likewise independent of proposer metadata. -/
def authoritativeCertificateDigest
    (_private : ProposerPrivateState)
    (certificateDigest : String) : String :=
  certificateDigest

theorem authoritative_certificate_digest_noninterference
    (p q : ProposerPrivateState)
    (certificateDigest : String) :
    authoritativeCertificateDigest p certificateDigest =
      authoritativeCertificateDigest q certificateDigest := by
  rfl

/-!
The bounded executable proposer regenerates the exact M2 accepted transitions
from the current public state. Therefore the already proved M2 composition
result is the preservation theorem for the M3 generated accepted path.
-/
theorem m3_generated_sequence_preservation :
    SequencePreservationResult s0 s5 m2Chain :=
  one_complete_guarded_replacement_sequence

/-! Cross-language identities independently replayed by Python CI. -/
def m3ObjectiveDigest : String :=
  "3926dc39cf05d5030a9da60e6680eb53eaf18f14e81e621210d95213248625a5"

def m3TranscriptChainDigest : String :=
  "295b815b1a14c4453da824d28c7e85309799678b737f274c795ebddd0704a008"

def m3IndependentCertificateChainDigest : String :=
  "7120c0be21626ab9a29b61a71f5a7837ea4c1cb163be54592d3f2f20d89411d8"

def m3FirstIndependentCertificateDigest : String :=
  "eea1542f8196516ee4c7e6dffe6115c1d8238b2515c9476cb30ed7d91daf9aca"

theorem m3_formal_object_is_frozen :
    formalObjectSHA256 =
      "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc" := rfl

end M3
end RSICCC
