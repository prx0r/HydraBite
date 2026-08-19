# Pāṭala Research CI — submission story

## The question

The OpenAIRE/Alien MCP gives AI agents direct access to authoritative scholarly metadata and relationships. That improves the quality and traceability of an answer **at the moment the answer is generated**. But OpenAIRE is continuously improved after that moment. If a research agent stores a conclusion for weeks or months, how does it know that a supporting record, relation or query result has changed?

**Pāṭala Research CI asks: can a stored research conclusion carry enough dependency information to know when it deserves to be checked again?**

## The journey

I first considered generic “Git for the OpenAIRE Graph”, an AI peer reviewer, a Broker agent, a living-review tool and a broader proof protocol. Prior-art review changed the direction. OpenAIRE already versions/releases its Graph; generic graph versioning exists; and AI peer review is crowded. The real seam is downstream of these systems.

The final build therefore combines two complementary paths:

```text
Official OpenAIRE MCP / Alien
       │ AI discovery + structured evidence
       ▼
redacted, hashed MCP trace
       │
OpenAIRE Graph V3
       │ canonical replayable snapshot
       ▼
TrackedClaim dependencies
       │
new Graph state
       ▼
SemanticDiff → ImpactReport → ProofObligation → VerificationReceipt
```

V3 is the stable/recommended deterministic plane; V4 remains optional/beta. ScholeXplorer supplies typed relations when available. Broker is a natural future trigger. A critical implementation lesson was that source health must itself be modeled: an API outage is not zero results, a partial relation source is not relation deletion, and an upstream change is not automatically a false conclusion.

I also adapted a mechanism from QDW: a proof obligation has a **frozen resolution plan**. A claim cannot return to current merely because an agent reports that it “fixed” the problem; a predefined check must produce verifiable evidence.

## The insight

The useful primitive is not “show me what changed in OpenAIRE.” It is:

> **show me which of my conclusions depended on what changed, and exactly what must be checked to trust them again.**

The deterministic demo begins with three software records, two dataset relationships and three downstream claims. The later snapshot adds a record, removes a dataset relationship and includes an unrelated cosmetic change. Pāṭala ignores the irrelevant change, targets only claims connected by explicit dependencies, recomputes the computable ones, leaves ambiguous work open for human review, and records hashed verification receipts. The adversarial suite also checks source failures, partial relation enrichment, ordering-only changes and tampering.

The MCP integration is intentionally explicit rather than hand-waved: Pāṭala can record a credential-redacted OpenAIRE/Alien MCP call, hash it and bind it to the deterministic analysis. The bundled MCP trace is clearly marked synthetic because a credentialed Alien session belongs to the participant account, not the offline release environment.

## What others can reuse

The artifact is designed as a set of small protocol objects rather than a monolithic app:

- OpenAIRE V3/V4/ScholeXplorer/Broker adapters with typed source health;
- a credential-redacting OpenAIRE MCP trace schema and trace-binding workflow;
- `TrackedAnalysis` and explicit entity/field/relation/query-membership dependencies;
- semantic diff and dependency-impact logic;
- machine-readable proof obligations;
- frozen resolution plans and verification receipts;
- a tamper-detecting append-only ledger;
- JSON Schemas, RO-Crate-compatible export, `CITATION.cff`, CodeMeta and Zenodo metadata;
- deterministic fixtures, unit/E2E/adversarial tests and a build certificate.

A team can reuse the verification protocol with other scholarly sources without replacing OpenAIRE. The longer-term OpenAIRE/Alien pilot is straightforward: let MCP-driven research agents keep persistent answers; use Graph/Broker changes as triggers; invalidate only memories whose evidence dependencies were touched; and measure how much recomputation is saved without missing material changes.

**OpenAIRE continuously validates research information. Pāṭala continuously validates what researchers and AI agents derived from it.**
