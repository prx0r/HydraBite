# Mechanisms reused and adapted

## From QDW

### Frozen verification plans

QDW's verification plan is a versioned immutable specification of required checks. Research CI adapts this into `ResolutionPlan`: once a proof obligation exists, its success criteria are content-hashed rather than silently mutable.

### Receipts rather than declarations

QDW records exact verification runs, command/artifact evidence and hashes. Research CI creates `VerificationReceipt` bound to old/new snapshot digests and claim dependencies.

### Typed negative states

QDW distinguishes `PROVEN`, `UNVERIFIED`, `BLOCKED`, `FAIL` rather than “looks good.” Research CI similarly separates `CURRENT`, `RECOMPUTE_REQUIRED`, `HUMAN_REVIEW_REQUIRED`, `BLOCKED`, `VERIFIED_CURRENT`, `UNSUPPORTED`.

### Source failure invariant

QDW's `SOURCE FAILURE != ZERO RESULTS` is carried across verbatim as a system invariant.

### Adversarial acceptance

The release test philosophy is adapted from QDW's verification ladder: prove failure behavior, not only happy-path behavior.

## From Pāṭala/Wiggly

- observations are not automatically truth;
- exact upstream evidence state is preserved;
- semantic state is append-only rather than overwritten;
- structured canonical hashing;
- explicit dependency/staleness propagation;
- machine computation and human authority are separable;
- unresolved questions become explicit obligations.

## From OpenAIRE's contract tests

- record before;
- replay the same request after;
- normalize before comparison;
- exclude transport/volatile values;
- compare exact identity where appropriate;
- keep before/after fixtures inspectable.

## From ScholeXplorer/Scholix

Use typed scholarly relations (`Cites`, `HasPart`, `IsNewVersionOf`, etc.) as dependency objects rather than flattening everything to generic strings.

## From RO-Crate

Make the complete verification object portable: analysis, snapshots, claims, diffs, obligations, plans, receipts and ledger can be exported as a crate-style ZIP with machine-readable metadata.

## From in-toto

The conceptual pattern is `plan/layout → exact inputs/materials → checks/steps → evidence/attestation`. Research CI applies this to scholarly re-verification, without claiming in-toto schema compatibility.

## What is intentionally *not* reused

- TerminusDB as the storage layer: excellent versioned graph prior art, but unnecessary dependency for a small portable hackathon reference implementation.
- QDW's factory/marketplace/federation systems: irrelevant to the product boundary.
- Pāṭala's full manuscript/translation ontology: valuable origin story and future vertical, not needed for this OpenAIRE entry.
