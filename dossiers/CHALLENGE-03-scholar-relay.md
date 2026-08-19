# Challenge: Scholar Relay

## The hard truth

**Expert finding is a well-studied IR problem.** The academic community has published extensively on it. If the pitch is "find researchers who might know about X," you're competing with established methods.

The novel part — routing to humans for *verification* within an evidence workflow, not just recommendation — is genuinely different. But it's a **feature, not a product.**

## The real question

Does routing to experts actually happen after the proof obligation is emitted? If the answer is "email them and hope," the value is marginal. If the answer is "integrate with MyResearchFolio/ORCID to create a verifiable contribution record," the value compounds.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [CollabNext](https://github.com/beviah/CollabNext) | 4 | OpenAlex + Neo4j for research collaboration | MEDIUM-HIGH — very adjacent |
| [BibApp](https://github.com/BibApp/BibApp) | 41 | Campus expert finder | MEDIUM — older but established |
| [scholar-lab-radar](https://github.com/TaewoooPark/scholar-lab-radar) | 19 | Profile research labs via OpenAlex | LOW |
| [ExpertFinder4Projects](https://github.com/elloza/ExpertFinder4Projects) | 0 | Expert finding for projects (IAT 2025) | LOW — academic |
| OpenReview reviewer matching | — | Built into OpenReview | MEDIUM — but workflow-locked |

## Reusable from competitors

- CollabNext's Neo4j graph approach
- BibApp's expert profiling patterns
- OpenAlex Person/Organization API
- OpenReview's matcher as reference

## Verdict

**Not a standalone product.** Beautiful consequence of Research CI. Mention in one slide as "future extension." The integration with MyResearchFolio for contribution credit is the long-term play, but MyResearchFolio needs to mature first.
