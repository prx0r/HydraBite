# Challenge: Research CI

## The hard truth

**Most researchers will not care about "semantic diffs of scholarly graphs."** That is infrastructure language. If that is the pitch, the project is likely a clever hackathon demo rather than a product.

The real problem underneath is **living systematic reviews and continually maintained evidence syntheses**. These teams rerun searches monthly, store successive batches, define explicit triggers for when new evidence matters, and struggle with deciding whether new information actually changes findings.

A real living review documented **30 search updates but only three review updates** — they explicitly describe needing rules for when new evidence changes outcomes.

## What someone actually gets

Not: "Nine OpenAIRE records changed."

Instead:

> **"Don't redo your entire review. This specific new evidence is the reason you need to look again."**

## Who cares most

| User | Care level | Why |
|------|-----------|-----|
| Living systematic review teams | **A lot** | Their entire job is maintaining conclusions against incoming evidence |
| Policy/guideline teams | **Even more** | Their output depends on fast-evolving evidence |
| Bibliometricians | Somewhat | OpenAIRE MONITOR already sells timely research intelligence |
| Research agents (future) | **Substantially** | Once an agent has 1,000 persistent analyses, manual checking is absurd |
| Normal researcher writing one paper | **Does not care** | They search, write, publish, move on |

## The 12 hard questions

1. **How often does OpenAIRE change in a way that changes a research conclusion rather than merely cleaning metadata?** If 99.9% of diffs are affiliation formatting, a generic watcher is useless. Need semantic-materiality filters.

2. **Why can't I just rerun my notebook?** If recomputation costs 30 seconds, this adds complexity. You win where the expensive part is human screening, evidence adjudication, extraction.

3. **Who creates `TrackedClaim.dependencies`?** If researchers manually annotate fifty claims and hundreds of dependencies, most won't bother. Need auto-generation with cheap validation.

4. **Can you distinguish "input changed" from "conclusion changed"?** A new study may not alter the meta-analysis. A corrected affiliation certainly won't. `STALE` cannot mean "something somewhere changed."

5. **Can you calculate impact rather than just alert?** "Seven papers appeared" is Google Scholar. "One of seven crosses your prespecified update trigger and changes effect direction" is valuable.

6. **Can you avoid alert fatigue?** If every update creates proof obligations, users disable it. High precision matters enormously.

7. **Is OpenAIRE the correct primary sensor?** For medicine: PubMed/Cochrane. For SE: Crossref/OpenAlex/GitHub. OpenAIRE is the hackathon adapter; architecture should be source-agnostic.

8. **What happens when the source doesn't provide historical versions?** Prospective snapshots work; retrospective history is incomplete.

9. **What exactly constitutes a "claim"?** Numeric meta-analysis results are tractable. "Theory A provides a better explanation" is much harder.

10. **Can you prove this saves work?** Evaluation: given 100 historical update cycles, can Pāṭala correctly identify the 10 that warranted re-analysis while letting researchers ignore the other 90?

11. **Does the user trust an automated "no update required"?** This is higher stakes than recommending papers. Need evidence trails, conservative uncertainty, human authority.

12. **Why switch from Covidence/EPPI/DistillerSR?** Don't. Integrate underneath those workflows.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [QuitStore](https://github.com/AKSW/QuitStore) | 114 | Quads in Git — version control for RDF | LOW — generic, not scholarly-specific |
| [LSR_Automation](https://github.com/L-ENA/LSR_Automation) | 3 | Evidence surveillance for living reviews | LOW — narrow scope |
| [OpenAlex API tutorials](https://github.com/ourresearch/openalex-api-tutorials) | 147 | OpenAlex (240M+ works) | REFERENCE — alternative data source |
| HUKA (paper) | — | Query provenance in dynamic KGs | PRIOR ART — academic only |
| TerminusDB | — | Git-like versioned database | ADJACENT — generic KG versioning |
| RDF Delta | — | RDF change propagation | ADJACENT — generic |

## Reusable from competitors

- QuitStore's quad-versioning approach for RDF
- OpenAlex as alternative/additional data source (free, 240M+ works)
- Crossref Event Data for change detection
- HUKA's provenance maintenance patterns

## Verdict

The mechanism is sound. The user segment is narrow but real (living review teams + policy + future agents). The biggest risk is **alert precision** — if most diffs are metadata noise, the product fails. The strongest version is:

> **"Register an evidence synthesis and its conclusions. Pāṭala continuously watches the evidence underneath it and tells you exactly when — and why — it deserves another look."**

The first experiment: take 20 historical living-review update cycles. Give Pāṭala the state before each. Can it distinguish updates where new evidence materially changed conclusions from those where researchers correctly left conclusions alone?

If yes: product. If no: elegant architecture solving the wrong layer.
