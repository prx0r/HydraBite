# MONITOR CI Benchmark

**Proof that Pāṭala can predict which OpenAIRE-derived research intelligence indicators are affected by Graph changes.**

## What this proves

Instead of saying "OpenAIRE changed, rerun everything," we demonstrate:

> "OpenAIRE changed X things. N of your K research-intelligence outputs provably don't depend on any of those changes. The M that do are exactly these, for these reasons."

## Indicators tracked

Based on [OpenAIRE MONITOR indicators](https://monitor.openaire.eu/support/research-institution-indicators.html):

| ID | Indicator | Depends on |
|----|-----------|------------|
| I1 | Software production count | query: type=software |
| I2 | Software linked to publications | ScholeXplorer: IsRelatedTo/Cites (pub↔sw) |
| I3 | Publications with ORCID | authorships.author.id (ORCID scheme) |
| I4 | Grant-supported publications | projects/funding relations |
| I5 | Open-access share | bestAccessRight |
| I6 | Dataset production count | query: type=dataset |
| I7 | Publications with DOI | pids (scheme=doi) |
| I8 | Peer-reviewed share | isPeerReviewed |
| I9 | Publication count (total) | query: type=publication |
| I10 | Datasets with PID | pids on type=dataset |
| I11 | International collaboration | countries (multiple per product) |
| I12 | Open-source software share | accessRight on type=software |

## How to run

```bash
cd /root/hackathon1
python3 evaluation/monitor_ci/run.py
```

## Metrics

- **Impact precision**: of predicted affected, how many actually changed?
- **Impact recall**: of actually changed, how many did we predict?
- **Recompute avoidance**: what % of indicators were correctly left alone?
- **False stale rate**: predicted affected but value unchanged
