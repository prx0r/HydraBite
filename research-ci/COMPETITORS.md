# Competitors & Threats

## What already exists

| System | What it does | Threat |
|--------|-------------|--------|
| QuitStore | RDF version control (Git for quads) | LOW — generic, not scholarly-specific |
| TerminusDB | Versioned database | ADJACENT — generic KG versioning |
| RDF Delta | RDF change propagation | ADJACENT — generic |
| HUKA | Query provenance in dynamic KGs | PRIOR ART — academic only |
| OpenAIRE contract tests | API regression testing | ADJACENT — different layer |
| LSR_Automation | Living review surveillance | LOW — narrow scope |
| Crossref Event Data | Change detection | REFERENCE — data source |

## What does NOT exist

Nobody does: OpenAIRE analysis → explicit claim dependency → change → epistemic impact → proof obligation end-to-end.

Related prior art exists at each layer but the integrated loop is novel.

## Reusable from competitors

- QuitStore's quad-versioning approach
- OpenAlex as alternative data source (free, 240M+ works)
- HUKA's provenance maintenance patterns
- Hypothesis (Python) for property-based testing patterns

## What NOT to claim

Don't say:
- "Nobody has Git for knowledge graphs" (QuitStore, TerminusDB)
- "Nobody tracks graph changes" (OpenAIRE changelog, RDF Delta)
- "Nobody does query provenance" (HUKA)

Do say:
- "Nobody does end-to-end analysis → dependency → change → impact → obligation"
