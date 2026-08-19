# Responsible data use, rights and provenance

## OpenAIRE Graph

OpenAIRE documents the Graph/API metadata as reusable under **CC BY 4.0**, with attribution required. Pāṭala therefore:

- identifies OpenAIRE as the source in snapshots, traces and documentation;
- retains source/API version and request/query provenance where available;
- does not imply endorsement by OpenAIRE;
- treats derived/exported metadata bundles as CC BY 4.0 unless a more permissive source-specific licence is known;
- does not redistribute article full text as part of the reference implementation.

Recommended acknowledgement/citation is documented by OpenAIRE at:
- https://graph.openaire.eu/docs/apis/terms/
- https://graph.openaire.eu/docs/bulk-access/downloads/full-graph/

## Alien Intelligence / OpenAIRE MCP

The MCP integration stores **tool-call provenance**, not credentials. The trace sanitizer redacts common credential fields such as tokens, authorization headers, cookies and passwords before persistence. Users should never paste secrets into trace notes or free-text fields.

The reference artifact does not bundle proprietary Alien code or authentication material.

## Personal data

The tool is designed around scholarly metadata already exposed by OpenAIRE (for example public authorship/person records and identifiers). It does not scrape private contact details, infer sensitive traits, or create behavioural profiles. A deployment should still apply its institution's lawful-basis, retention and access-control policies when processing identifiable people at scale.

## Source-health safeguards

The following are hard safety invariants:

```text
SOURCE FAILURE != ZERO RESULTS
PARTIAL RELATION SOURCE != RELATION DELETION
MISSING FIELD != FALSE
UPSTREAM CHANGE != CONCLUSION FALSITY
```

A failed or partial OpenAIRE/ScholeXplorer fetch blocks or narrows verification rather than manufacturing mass deletions.

## Included fixtures and outputs

- `fixtures/demo/*`: synthetic OpenAIRE-shaped demonstration data, released CC0-1.0 for reuse.
- `artifacts/alien_mcp_trace.example.json`: synthetic example only, CC0-1.0; not evidence of a live Alien session.
- submission prose/docs: CC BY 4.0.
- source code: MIT.
