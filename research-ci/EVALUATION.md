# Evaluation

## The benchmark

Create a fixed benchmark:

```
25 tracked records
10 deliberately meaningful changes
10 irrelevant changes
5 ambiguous changes
```

## Metrics

```
diff detection recall
diff precision
impact classification accuracy
unaffected-claim precision
proof-obligation correctness
replay determinism
```

## Anti-alert-fatigue test

For known irrelevant changes:

> Does Pāṭala correctly leave unrelated claims CURRENT?

A system marking everything stale isn't useful. High precision on "no action required" is the most important metric.

## The real evaluation (stretch)

Take 20 historical living-review update cycles.

Give Pāṭala only the state before each update.

Can it distinguish updates where new evidence materially changed conclusions from those where researchers correctly left conclusions alone?

If yes: product.
If no: elegant architecture solving the wrong layer.

## Hard requirements

```
R1. Same snapshots + same deps → same ImpactReport
R2. Replay from scratch produces identical results
R3. Proof obligations identify exact triggering change
R4. Unaffected claims are verifiably unaffected
```
