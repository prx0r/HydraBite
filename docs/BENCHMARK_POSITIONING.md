# Benchmark positioning

HydraDB already publishes serious database/retrieval and function-routing evaluation. Iolaus should **not** submit another sprawling benchmark suite and should not imply its tiny harness competes with Hydra's benchmark work.

## Hydra's benchmark questions

Hydra's public benchmark material emphasizes graph/context retrieval quality and the difference between semantic similarity and decision-relevant graph context. The function-routing cookbook separately evaluates routing/plan behavior.

These are upstream questions:

```text
Did we retrieve the right context?
Did we select the right function?
Did the plan execute/complete?
```

Iolaus asks a downstream systems question:

```text
If execution reported success, was the declared effect actually true
before we committed it as trusted state?
```

## Why only 12 adversarial cases in the MVP

The benchmark is an executable invariant test, not a statistical claim about all agent systems. It intentionally creates controlled semantic failures for which ground truth is directly readable from the external demo database.

That makes every case auditable:

```text
requested email
→ tool return
→ external row state
→ verifier decision
→ Hydra receipt
→ Hydra claim existence
```

A larger benchmark would add volume without strengthening the core hackathon proof.

## Future evaluation

A serious follow-up could measure:
- false-success commit rate across real SaaS APIs;
- verifier coverage and cost;
- time-to-verification;
- recovery success after REJECTED transitions;
- routing quality when historical labels change from raw success to verified success;
- expected cost per verified terminal outcome.

Those are explicitly future work.
