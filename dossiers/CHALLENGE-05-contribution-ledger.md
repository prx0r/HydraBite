# Challenge: Contribution Ledger

## The hard truth

**There's essentially zero open-source tooling for CRediT-based contribution tracking.** That's both the opportunity and the warning — if nobody built it, maybe nobody wants it.

The real barrier is adoption: researchers already struggle to fill in ORCID profiles. Asking them to log contribution events is a bigger ask. The only way this works is if it's **automatic** — contributions are recorded as a byproduct of using other tools (Research CI, Crux, Scholar Relay).

## When this wins

If every Pāṭala interaction (tracking an analysis, verifying a claim, adjudicating a crux) automatically produces a `ScholarlyContributionEvent` that feeds into MyResearchFolio, the ledger becomes invisible infrastructure that compounds value.

If it requires manual entry, it dies.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| None found | — | No open-source CRediT implementation | **WIDE OPEN** |
| DORA-Metrics | 2 | DevOps metrics (different domain) | IRRELEVANT |
| MyResearchFolio | — | OpenAIRE's researcher profile system | THE PLATFORM — integrate, don't compete |
| Altmetric | — | Tracks attention, not contributions | ADJACENT |
| SciCV (NIH) | — | Biosketch tool | ADJACENT |

## Verdict

**Strategic killer but not for this hackathon.** The automatic-contribution-as-byproduct framing is the right one. Long-term, this could be the economic flywheel (Certification Weight → marketplace). But it needs MyResearchFolio to mature and needs Pāṭala interactions to be the data source first.

Position as: "Every Pāṭala interaction produces a contribution event."
