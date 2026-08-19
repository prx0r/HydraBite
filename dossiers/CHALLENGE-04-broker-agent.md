# Challenge: Broker Agent

## The hard truth

**OpenAIRE's Broker already does the enrichment.** You're adding an evidence layer on top. That's useful but **not distinctive enough for a hackathon win.** The evidence bundle is the novel part, but judges may see "metadata enrichment" and move on.

The deeper problem: **who pays for the evidence gathering?** If each Broker event requires 5 API calls to cross-validate, the cost adds up. And if the evidence is just "ORCID confirmed this exists," that's not very compelling.

## When this actually wins

If you can show: "OpenAIRE suggested adding ORCID X to author Y. Our agent checked and found 3 supporting sources but 1 contradiction — the ORCID belongs to a different E. Richard Gold at a different institution." THAT is a story.

But building the contradiction-detection layer is non-trivial.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [bib-enricher](https://github.com/ivan-cardenas/bib-enricher) | 1 | Enrich .bib from Semantic Scholar/OpenAlex | LOW — just API wrapper |
| [GROBID](https://github.com/grobidOrg/grobid) | 5085 | ML extraction from PDFs | REFERENCE — different layer |
| [BibexPy](https://github.com/bcankara/BibexPy) | 18 | Bibliometric data integration | LOW |
| OpenAIRE Broker itself | — | The enrichment engine | THE PLATFORM — not competitor |

## Reusable from competitors

- bib-enricher's API integration patterns
- GROBID for PDF metadata extraction
- OpenAlex/Semantic Scholar as cross-validation sources

## Verdict

**Most immediately useful but least distinctive.** Good weekend build, unlikely to win. The evidence bundle idea is worth preserving for the Research CI submission — it's the same pattern (change detected → does it matter? → here's why).
