# Judge demo — 90–120 seconds

The demo is deliberately split into **AI discovery** and **deterministic verification**. This directly demonstrates why both the official OpenAIRE MCP and Pāṭala are useful.

## 0–20s — Use the official OpenAIRE MCP

In the Alien Open Science Plugin, ask a bounded question such as:

> “Find recent research software related to agentic AI and show the structured OpenAIRE records you used.”

Show that the agent is grounded in OpenAIRE rather than generic web search. Preserve one credential-redacted MCP tool trace and import/bind it to the corresponding Pāṭala analysis.

**If recording before a live Alien trace is committed:** state clearly that the package's bundled trace is synthetic and only tests the trace protocol.

## 20–35s — The continuity problem

> “The MCP gives an excellent answer today. But OpenAIRE keeps improving. What happens to this stored conclusion after its evidence changes?”

Switch to Pāṭala:

```bash
patala-ci --workspace /tmp/patala-demo demo
```

The offline fixture uses OpenAIRE-shaped normalized objects and also exercises the MCP trace/binding path with `synthetic:true`.

## 35–55s — A material upstream change

Baseline:

```text
3 software outputs
2 dataset relations
claim: dataset linkage >= 60%
baseline = 2 / 3 = 66.7% → supported
```

Current state:

```text
+ 1 software output
- 1 dataset relation
~ 1 unrelated title normalization
```

Pāṭala emits a semantic diff rather than a raw JSON diff.

## 55–75s — Impact, not alert spam

Show the impact report. The key point is not that “something changed”; it is that only claims with an explicit dependency path are affected. The unrelated title normalization does not stale a relation-only claim.

> “OpenAIRE tells us the Graph changed. Pāṭala tells us which conclusion that change touched.”

## 75–95s — Proof obligation + receipt

Two computable claims are automatically recomputed:

```text
dataset linkage: 1/4 = 25% → UNSUPPORTED
open access:      3/4 = 75% → VERIFIED_CURRENT
```

A relation-specific manual claim remains open for review. Every resolution is bound to a frozen plan and produces a receipt.

## 95–110s — Integrity

```bash
patala-ci --workspace /tmp/patala-demo verify-ledger
```

Mention the adversarial suite:

```text
source outage ≠ zero results
partial relation source ≠ relation deletion
cosmetic change ≠ material impact
agent says “fixed” ≠ proven resolution
```

## 110–120s — Close

> **“OpenAIRE and Alien make trustworthy research intelligence available to AI agents. Pāṭala makes the conclusions those agents keep continuously verifiable.”**

Pilot extension: a Graph release/Broker notification triggers targeted refresh of persistent Alien/OpenAIRE agent memories rather than blind full recomputation.
