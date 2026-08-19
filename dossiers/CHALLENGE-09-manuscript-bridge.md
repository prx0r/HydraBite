# Challenge: Manuscript Reality Bridge

## The hard truth

**The ontology extension is beautiful but the adapters don't exist.** To connect OpenAIRE publications to physical manuscripts, you need:
- IIIF adapter (for manuscript images)
- TEI-XML parser (for transcriptions)
- Archive.org/DLII adapter (for digitized manuscripts)
- A mapping between OpenAIRE's `Publication` and Pāṭala's `Work → Edition → Witness → Passage`

That's a lot of integration work for a hackathon.

## The real question

Is this a product or a research contribution?

If product: the adapter gap makes it impractical for now.
If research contribution: the ontology mapping is genuinely novel and publishable.

## The Sanskrit angle

Using Sanskrit manuscripts as the domain demo is powerful narratively — "which physical evidence ultimately underlies this scholarly claim?" is a compelling question. But it makes the hackathon submission niche. Judges who don't know Sanskrit may not appreciate the difficulty.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [IIIF-Crawler](https://github.com/Jean-Baptiste-Camps/IIIF-Crawler) | 9 | Crawl IIIF servers | LOW — just crawler |
| [DMMapp](https://github.com/SexyCodicology/DMMapp-Legacy) | 9 | Explore digitized manuscripts | LOW — discovery only |
| [iiif-manuscript-workbench](https://github.com/rsimon/iiif-manuscript-workbench) | 1 | IIIF manuscript analysis | LOW — viewing only |
| [GROBID](https://github.com/grobidOrg/grobid) | 5085 | PDF → structured data | ADJACENT — different format |
| TEI Consortium tools | — | TEI parsing ecosystem | REFERENCE — fragmented |

## Reusable from competitors

- IIIF-Crawler's crawl patterns
- GROBID's ML extraction approach
- TEI-to-RDF conversion patterns from digital humanities
- Mirador (IIIF viewer) for front-end

## Verdict

**Most distinctive domain demo but highest build risk.** The adapter gap is real. If you already had the TEI/IIIF adapters, this would be spectacular. Without them, it's a design doc.

Position as: "Future extension. Pāṭala was originally built for Sanskrit manuscript scholarship, where changing evidence and competing interpretations are unavoidable. This entry applies that same architecture to OpenAIRE."

One slide, one sentence, move on.
