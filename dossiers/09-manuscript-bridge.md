# Dossier 9: Manuscript Reality Bridge

**Status:** Most distinctive domain demo, high risk
**Score:** 6.2/10
**Category:** Extend OpenAIRE's ontology to manuscript scholarship

---

## TL;DR

OpenAIRE connects publications, datasets, software, persons, organizations, projects. Manuscript scholarship adds: physical object → witness → image → transcription → edition → passage → translation → claim. Pāṭala bridges these ontologies.

---

## The Problem

Scholars studying Sanskrit manuscripts need to trace:
- A scholarly claim → which passage → which edition → which manuscript → which physical object
- OpenAIRE has the publication layer but not the manuscript layer
- No existing system bridges published scholarship to physical manuscript evidence

---

## The Product

```
OpenAIRE scholarly world
          │
          │ cites / studies
          ▼
      Publication
          │
          ▼
    Pāṭala resolver
          │
          ▼
        Work
      /      \
 edition    manuscript
              │
           archive
              │
        physical witness

QUERY: "Which physical evidence ultimately underlies this scholarly claim?"
```

---

## Reusable

- Atlas (Work, Edition, Witness, EText, Translation) from openpatalanew
- 13 adapters (GRETIL, PANDiT, Archive.org, etc.)
- Resolver R0-R5 from openpatalaproject/patala/resolver.py
- Collation concepts from fuck-off/lib

## New code needed (~400 lines)

Ontology bridge + IIIF adapter + TEI-XML adapter.

---

## Why this is ninth

The coolest domain demo — "which physical manuscript underlies this claim?" is a powerful question. But it requires adapters that don't exist yet (IIIF, TEI-XML) and the Sanskrit-specific ontology is niche. Better as "future extension" in the Research CI submission.
