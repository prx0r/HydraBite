# Challenge: Pāṭala Crux

## The hard truth

**Argument mining is a mature NLP subfield.** ACL/EMNLP have published hundreds of papers on it. If the pitch is "we extract argument structure," you're competing with established labs.

The genuinely novel part — perturbation analysis to find load-bearing premises — is interesting but **depends entirely on having good argument structure in the first place.** And extracting that from unstructured papers is exactly where current systems struggle.

## The real question

Is perturbation-based crux detection actually useful, or is it an intellectually satisfying mechanism looking for a problem?

Arguments for:
- A 2026 position paper argues AI peer review should be "verification-first and adversarial" — validates the design philosophy
- No existing tool does counterfactual stress-testing of argumentative reasoning chains
- The "minimal load-bearing premise-set" framing is genuinely different from "find contrary evidence"

Arguments against:
- Extracting argument structure from papers is the hard part, and that's where everyone struggles
- For structured/formal arguments (math, logic), this is well-studied
- For informal scholarly arguments, the representation is ambiguous
- Demo risk: if the argument extraction is weak, the crux analysis looks trivial

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [Marseille](https://github.com/vene/marseille) | 66 | Argument structure mining with LSTM | MEDIUM — mature but old (2018) |
| [DebateSum](https://github.com/Hellisotherpeople/DebateSum) | 55 | Debate summarization + argument mining | LOW — different domain |
| [mining-legal-arguments](https://github.com/trusthlt/mining-legal-arguments) | 80 | Legal argument mining | LOW — domain-specific |
| [neural_end2end_am](https://github.com/UKPLab/acl2017-neural_end2end_am) | 59 | Neural argument mining (ACL 2017) | MEDIUM — foundational |
| [Argdown](https://github.com/christianvoigt/argdown) | — | Structured argumentation framework | REFERENCE — representation format |
| Peerispect | — | Claim verification in peer review | ADJACENT — different mechanism |

## Reusable from competitors

- Marseille for argument structure detection
- Argdown for argument representation
- ACL argument mining datasets for evaluation
- DebateSum's preprocessing pipeline

## Verdict

The perturbation mechanism is novel. But the dependency on argument extraction makes it a **bad hackathon standalone** — too much glue risk. Better as a stretch feature for Research CI, where the "arguments" are structured TrackedClaims with explicit dependencies (which the user provides).

The strongest version: **don't extract arguments from papers. Let users define structured arguments, then perturb them.** That's a tool, not an NLP system.
