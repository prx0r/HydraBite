# Dossier 2: Pāṭala Crux

**Status:** Secondary product, already built
**Score:** 8.6/10
**Category:** Verification primitive — find the minimal load-bearing premise

---

## TL;DR

Given a structured argument, Pāṭala Crux identifies the minimum premise whose removal causes the conclusion to fail. It simulates rejection/retraction and computes the exact epistemic blast radius.

---

## The Problem

Current AI review systems (CMU Paper Reviewer, Peerispect, ReviewGrounder) do:
- Claim extraction from papers
- Literature search for supporting/contradicting evidence
- Classification: supported/contradicted/undetermined

What they DON'T do:
- Formally model argument dependency structure
- Perturb premises systematically
- Identify which premise is the CRUX (minimum load-bearing set)
- Simulate "what if this premise is rejected?" and compute downstream impact

OpenReview handles workflow (submission → review → rebuttal → decision) but has no formal argument model.

---

## The Product

### Input

Structured argument:

```json
{
  "premises": [
    {"id": "P1", "text": "X is a Sanskrit text"},
    {"id": "P2", "text": "X dates to the 10th century"},
    {"id": "P3", "text": "Y is a commentary on X"}
  ],
  "inferences": [
    {"id": "I1", "from": ["P1", "P2", "P3"], "to": "C1"}
  ],
  "conclusions": [
    {"id": "C1", "text": "Y reflects 10th-century interpretive traditions"}
  ]
}
```

### Processing

```
perturbation analysis:
  remove P1 → C1 fails (no subject)
  remove P2 → C1 survives (still a commentary, just undated)
  remove P3 → C1 fails (no commentary relationship)

CRUX = {P1, P3}

minimal load-bearing set: 2 of 3 premises
```

### Output

```json
{
  "crux": {
    "type": "MINIMAL_DIVERGENCE",
    "load_bearing_premises": ["P1", "P3"],
    "non_bearing": ["P2"],
    "resolution_question": "Is the identification of X and the commentary relationship independently established?"
  },
  "simulated_rejection": {
    "rejected": "P1",
    "affected": ["I1", "C1"],
    "unaffected": [],
    "blast_radius": 2
  },
  "downstream": {
    "claims_affected": ["C1"],
    "proof_obligations": ["PO-1: Establish subject identification of X"]
  }
}
```

### CLI

```bash
# Find crux of an argument
patala crux argument.json

# Simulate rejection of a premise
patala simulate --reject P1 --from argument.json

# Output:
# P1          REJECTED
# I1          NEED_REVIEW
# C1          NEED_REVIEW
# 7 unrelated claims remain valid.
```

---

## Reusable from existing code

| Component | Source |
|-----------|--------|
| Crux engine | `fuck-off/lib/epistemic.py` (perturbation logic) |
| Review reducer | `fuck-off/lib/review.py` (state machine) |
| Blast-radius | `fuck-off/lib/staleness.py` (dependency walking) |
| Typed edges | GROUNDS, USES_AS_PREMISE, USES_AS_WARRANT |

## New code needed (~100 lines)

Thin CLI wrapper + JSON I/O around existing kernels.

---

## Why this is strong but second

The perturbation-based crux detection is genuinely unusual. But extracting argument structure from unstructured papers is the hard part, and that's where current systems struggle. For a hackathon, Research CI is safer because OpenAIRE already gives structured data.
