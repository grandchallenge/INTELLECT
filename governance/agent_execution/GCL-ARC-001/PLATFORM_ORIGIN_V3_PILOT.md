# GCL-ARC-001 V3 — Authenticated execution-origin pilot (source stage)

Issue: grandchallenge/INTELLECT#126. Exact pilot subject: MATH-PROGRAMME PR #2710, head `b380e583ca2c997c07a4b7f15cbf97728006a79e` and canonical five-file material digest `b6b353decee67953b74c984a1c8856c3ea56debbae0599f759564f13bbe214b4`.

**Source scope:** Preserve the *actual* GitHub-hosted Actions runner witness from run #38988609732, attempt 1, artifact ID 12084032389, with protected witness Git blob `4f1114a841e1adc5039c518ab6a55eeec9e80509` and SHA-256 `e9a6cc3f140a3ab1befdf5500c4779a10873b32886b7c69a785bb05b2d6198ab`. It contains the three original runner-produced outputs, commands, and hash digests. A later independent readback of this run using MATH-PROGRAMME protected `ci/paar_execution_origin.py` returned `PASS_BOUNDED_PLATFORM_ORIGIN_REPLAY`; the contemporaneous external GitHub workflow/run/job/artifact records are not manufactured by this dossier.

The dedicated `GCL_AGENT_PLATFORM_ORIGIN_DOSSIER_V3` is a *new*, acyclic source artifact. It cites the earlier protected V2 source but does **not** change that original V2 dossier or receipt. It does not assert original October 15 CHAD execution provenance, separate human identities, hardware attestation, mathematical certification or estate-wide integrity. Its offline checker only reconciles local bytes; authentic external runner identity **must** be verified via GitHub's API by the downstream consumer.

## Next governed transactions

1. Protected source PR for this V3 dossier and captured witness, independent nonauthor **native GitHub APPROVED review on exact head**, protected CI and merge; no self-review.
2. Separate subsequent protected INTELLECT V3 receipt PR referencing the reviewed *source* PR head, source dossier Git blob, witness Git blob, GitHub run/attempt/artifact identity, and explicit limits. No circular self-reference.
3. A new MATH-PROGRAMME V3 consumer must retrieve the protected INTELLECT source dossier, source PR and native review, the separate protected receipt, and GitHub original run/job/artifact records. It must cross-check the run-scoped witness SHA-256, all three stdout/stderr digests, exact commands and reviewed subject, and reject absent/expired/tampered/spoofed/dismissed/stale evidence; it must not rely solely on the source dossier's assertion that the runner was authentic. Retain older V1/V2 labels honestly.
4. End-to-end live positive and hostile replay through the protected consumer and independent exact-head reviewer acceptance, then narrow PAAR-C #2708 disposition. GCL-PAAR-001 #2705 stays open for estate-wide evidence.

Run source byte tests with `python3 -m unittest -q governance/agent_execution/GCL-ARC-001/test_platform_origin_v3.py`. On a live authenticated MATH-PROGRAMME environment, run `python3 ci/paar_execution_origin.py verify-live --run-id 38988609732` to recheck original platform run. The provider's artifact can expire after 90 days; the durable witness copy does **not** guarantee indefinite availability of the authentic GitHub run/artifact API.
