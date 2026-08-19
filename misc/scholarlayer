Yes. After checking the existing standards, I would **not design Pāṭala Sources as a new ontology from scratch**. Most of the generic substrate already exists, but it is distributed across several standards. The high-value move is to define a **Pāṭala application profile** that composes them and adds only the epistemic objects none of them provide.

The closest overall answer is:

> **FaBiO/BIBFRAME for bibliographic identity + W3C Web Annotation for stable spans + PROV-O for derivation/provenance + CiTO for citation relations + RO-Crate for packaging + IIIF for page/image assets. Pāṭala owns SourceAssertion, CorroborationEvent, epistemic status and downstream dependency semantics.**

That is much better than inventing `Publication`, `Witness`, `Span`, etc. independently.

## 1. Bibliographic identity: FaBiO is remarkably close to what we just designed

**FaBiO** already distinguishes bibliographic objects using the FRBR-style hierarchy:

```text
Work
↓
Expression
↓
Manifestation
↓
Item
```

and explicitly models journal articles, books, chapters, critical editions, datasets, figures, tables, pages, web content, computer files, etc. It even explains the difference between a work's intellectual content, a version/realization, a digital/physical manifestation, and a particular file/item. 

That is extremely close to our:

```text
Publication
↓
Edition/version
↓
DocumentWitness
↓
local PDF
```

I would therefore **not invent our own conceptual hierarchy unnecessarily**.

For Pāṭala I'd simplify the internal API names, but map them explicitly:

```text
Pāṭala                  External alignment

BibliographicWork   ↔   fabio:Work
Expression          ↔   fabio:Expression
Manifestation       ↔   fabio:Manifestation
Witness / Item      ↔   fabio:Item
Publication type    ↔   FaBiO subclasses
```

BIBFRAME gives a similar library-oriented model of `Work → Instance → Item`, with Agents and Subjects. ([The Library of Congress][1])

### Which should Pāṭala prefer?

**FaBiO internally as the closer scholarly-publication vocabulary; BIBFRAME as an interoperability adapter.**

FaBiO is more naturally research/publication focused. BIBFRAME is excellent for library integration but its model is fundamentally cataloguing-oriented. 

---

# 2. Stable passages/spans: W3C Web Annotation basically solves this

This was the biggest pleasant surprise.

The **W3C Web Annotation Data Model** already gives exactly the robust locator pattern we were converging on. It supports a target resource plus multiple selectors, including:

* text quote;
* prefix/suffix context;
* character position;
* fragments;
* XPath/CSS for structured documents;
* ranges;
* state/version information;
* images and timed media. ([W3C][2])

Most importantly, the standard explicitly encourages **multiple selectors for the same segment** because one locator can fail while another survives. ([W3C][2])

So instead of inventing:

```json
{
  "page": 17,
  "char_start": 18422,
  "char_end": 19201,
  "text_hash": "..."
}
```

Pāṭala should conceptually use:

```text
SourceSpan
  source → Witness
  selectors:
    HumanPageSelector
    TextPositionSelector
    TextQuoteSelector
    PāṭalaHashSelector
```

For example:

```text
human:
page 173, §4

machine:
start=18422
end=19201

resilience:
exact="vimarśa ..."
prefix="..."
suffix="..."

integrity:
witness_sha256=...
span_sha256=...
```

The first three largely align with Web Annotation.

**The cryptographic witness/span hashes are a justified Pāṭala extension.**

That's a much better design.

---

# 3. Provenance: PROV-O already gives the generic derivation graph

PROV-O's primitives are:

```text
Entity
Activity
Agent
```

with relationships such as:

```text
wasDerivedFrom
used
wasGeneratedBy
wasAttributedTo
wasAssociatedWith
actedOnBehalfOf
```

and it supports qualified relations, roles and plans. ([W3C DVCS][3])

That maps beautifully to:

```text
PDF
   ↓ OCR Activity
OCR text
   ↓ assertion extraction
SourceAssertion

Agent = Hermes/model/editor/scholar
Plan  = Pāṭala skill/version
```

So again, don't invent generic provenance verbs like `DERIVED_FROM` with incompatible semantics.

Internally we can retain concise Pāṭala fields, but they should have an explicit PROV-O mapping.

This is consistent with the standards decision Agent 1 already reached.

---

# 4. Citation relationships: CiTO is considerably richer than generic `CITES`

We also shouldn't invent the entire citation-relation vocabulary.

**CiTO — Citation Typing Ontology** exists specifically to characterize citations, including factual and rhetorical citation relationships rather than merely “A cites B.” ([SPAR Ontologies][4])

This is relevant to the future distinction between:

```text
Ratié supports Sanderson
Ratié discusses Sanderson
Ratié critiques Sanderson
Ratié obtains a result from Sanderson
Ratié cites Sanderson as background
```

Pāṭala will still need its own epistemic relations such as:

```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
ALTERNATIVE_READING
CONTRADICTS_PROPOSITION
```

because those describe the relationship between a Pāṭala proposition and evidence.

But for **publication → publication citation semantics**, use CiTO rather than inventing another vocabulary.

---

# 5. Packaging hundreds of PDFs: RO-Crate is almost tailor-made

For the practical problem:

> “How do I turn the giant Sanderson/Ratié directory into a stable portable research corpus?”

**RO-Crate is probably the strongest existing piece to adopt.**

RO-Crate packages files and URI-addressable resources together with JSON-LD metadata describing people, organizations, software, provenance, licensing, context and relationships. It supports both contained files and external resources that cannot be redistributed. ([researchobject.org][5])

A crate can look conceptually like:

```text
sanderson-corpus/
├── ro-crate-metadata.json
├── PDFs/
├── extracted/
└── ...
```

with the metadata graph identifying every relevant resource and its relationships. RO-Crate explicitly accommodates file-level provenance and can coexist with fixity systems/checksums rather than pretending metadata alone is a full integrity manifest. ([researchobject.org][6])

This means we could produce something like:

```text
Pāṭala Scholar Corpus RO-Crate
```

for export/archive/interchange **without making RO-Crate Pāṭala's database**.

That distinction is important.

Use it as:

```text
package/export format
```

not:

```text
canonical epistemic ontology
```

---

# 6. Images/pages/manuscripts/assets: IIIF is the obvious existing standard

The moment you mentioned:

> figures, manuscript images, diagrams, education/media assets

we entered **IIIF territory**.

IIIF Presentation 3 models compound objects using:

```text
Manifest
↓
Canvas
↓
Annotations
↓
content resources
```

and can handle page views, images, OCR/transcriptions, commentary, text, audio/video, regions and rights metadata. ([IIIF][7])

Critically, IIIF uses Web Annotation underneath. A Canvas can have the page image as its rendered content while OCR/transcription can be attached separately as `supplementing` content. ([IIIF][7])

That's basically perfect for:

```text
Sanderson PDF page 17
├── page image
├── extracted/OCR text
├── highlighted scholarly span
├── Pāṭala assertion annotation
└── education/media asset
```

It also carries rights and attribution information. ([IIIF][7])

For ordinary machine-processing PDFs we don't need to force everything through a IIIF server immediately.

But **make the object model IIIF-compatible from the beginning.**

Especially for manuscripts and visual assets.

---

# 7. DataCite is useful for IDs/relationships, not the internal ontology

DataCite already supports persistent identifiers and a useful controlled relation set:

```text
IsVersionOf / HasVersion
IsDerivedFrom / IsSourceOf
IsPartOf / HasPart
Cites / IsCitedBy
Reviews / IsReviewedBy
IsTranslationOf / HasTranslation
IsIdenticalTo
...
```

([DataCite Metadata Schema][8])

That's useful for import/export and external identifier alignment.

It also supports identifiers such as DOI, ISBN, ARK, Handle, arXiv and others. ([DataCite Metadata Schema][9])

But DataCite is deliberately publication/resource metadata. It doesn't solve fine-grained source-span assertions or Pāṭala's epistemic graph.

So:

```text
DataCite = external metadata/PID profile
```

not canonical source ontology.

---

# 8. OpenAlex is extremely useful as enrichment, not authority

OpenAlex already has a large scholarly works graph with entities and relationships for scholarly documents, authors, sources, citations and locations. ([OpenAlex][10])

I would absolutely use it when ingesting something like:

```text
Ratié paper PDF
```

to propose:

```text
title
author
year
venue
DOI
related works
citation graph
```

But treat it as:

```text
metadata witness
```

rather than:

```text
Pāṭala canonical identity
```

Canonical identity should remain your stable `pt:*` identifier associated with external IDs.

That means a bibliographic object can have:

```text
pt:publication:...
DOI: ...
OpenAlex: W...
ISBN: ...
Zotero key: ...
```

without any external provider owning the identity.

---

# 9. Nanopublications fit `SourceAssertion` remarkably well — but later

Nanopublications have exactly three relevant layers:

```text
Assertion
Provenance of assertion
Publication info
```

and are individually addressable/citable knowledge graph objects. ([Nanopub][11])

That is an excellent eventual export representation for:

```text
SourceAssertion
CorroborationEvent
reviewed Proposition
```

But I would **not** build the internal system around RDF nanopubs right now.

Same doctrine:

```text
Pāṭala native object
↓
nanopub adapter
```

It's an interoperability/publishing boundary.

---

# 10. TEI still matters, but for textual editions rather than the universal registry

TEI provides durable identifiers, references/pointers, source responsibility and rich encoding for textual scholarship; its current P5 model includes explicit pointer/reference mechanisms and responsibility/source metadata. ([Text Encoding Initiative][12])

It remains highly relevant for:

```text
critical editions
Sanskrit source structure
manuscript transcription
apparatus
textual variants
```

But I would not make TEI the general article/PDF/source backend.

It's another specialized projection/adapter.

---

# So the answer is: use a **schema stack**

No single existing ontology does everything cleanly.

I would freeze this:

| Pāṭala requirement                | Reuse                                      |
| --------------------------------- | ------------------------------------------ |
| bibliographic conceptual identity | **FaBiO**                                  |
| library interoperability          | **BIBFRAME** adapter                       |
| DOI/ISBN/etc metadata             | **DataCite / Crossref/OpenAlex ingestion** |
| local/remote file packaging       | **RO-Crate**                               |
| provenance/derivation             | **PROV-O**                                 |
| exact source spans                | **W3C Web Annotation**                     |
| publication citation semantics    | **CiTO**                                   |
| images/pages/manuscripts          | **IIIF Presentation**                      |
| textual critical editions         | **TEI**                                    |
| atomic assertion publishing       | **Nanopublication** adapter                |
| evidence epistemology             | **Pāṭala native**                          |
| argument epistemology             | **Pāṭala native**                          |

This is far stronger than inventing all of it.

---

# What remains uniquely Pāṭala?

This is the key question.

After aggressively reusing standards, the native core becomes surprisingly small.

### `SourceAssertion`

Not merely:

> this text occurs at this location.

But:

> **this attributed actor commits to this structured proposition at this source span, with this extraction/reconstruction status.**

Web Annotation can point to the span.

PROV-O can say who/what produced the extraction.

FaBiO can identify the publication.

But Pāṭala owns the epistemic semantics.

### `EvidenceUse / CorroborationEvent`

```text
Pāṭala Proposition
       ↕
SourceAssertion
```

with:

```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
DIRECT_CONTRADICTION
ALTERNATIVE_READING
BACKGROUND_ONLY
NON_EQUIVALENT
```

plus:

```text
scope
modality
speaker
independence
defeaters
semantic alignment
```

None of the generic bibliographic standards should decide this.

### Review/authority state

```text
MACHINE_PROPOSED
ENGINEERING_VALIDATED
SCHOLARLY_CORROBORATED
```

separate from:

```text
NOT_REVIEWED
INDEPENDENT_REVIEWED
ADJUDICATED
```

Again Pāṭala-specific.

### Dependency consequences

The truly unique machinery remains:

```text
ScholarAssertion changes
↓
Corroboration changes
↓
Proposition status changes
↓
Argument ceiling changes
↓
Synthesis becomes stale
↓
Essay/education becomes stale
```

No bibliography schema gives you that.

---

# I would therefore revise our proposed source model

Instead of inventing:

```text
Publication
DocumentWitness
SourceSpan
SourceAssertion
Asset
```

as wholly Pāṭala-native concepts, do:

```text
pt:BibliographicWork
    profile of FaBiO Work/Expression/etc.

pt:Witness
    FaBiO Item/Manifestation
    + PROV provenance

pt:Span
    Web Annotation SpecificResource
    + selectors
    + Pāṭala integrity hashes

pt:Asset
    IIIF-compatible content resource

pt:SourceAssertion      ← genuinely Pāṭala
pt:CorroborationEvent   ← genuinely Pāṭala
```

That's a much better architectural boundary.

---

# The architecture becomes highly interoperable

```text
                         EXTERNAL STANDARDS

                   FaBiO / DataCite / OpenAlex
                              │
                              ▼
                    Bibliographic Identity
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
       Manifestation                       Agent
             │                              PROV
             ▼
          Witness
             │
      ┌──────┴──────┐
      ▼             ▼
Web Annotation     IIIF
    Span           Asset
      │
      ▼
════════════════ PĀṬALA BOUNDARY ════════════════
      │
      ▼
 SourceAssertion
      │
      ▼
 CorroborationEvent
      │
      ▼
  Proposition
      │
      ▼
   Argument
      │
      ▼
   Synthesis
      │
      ▼
Essay / Education / API
```

That is extremely clean.

---

## The one existing project I would investigate first in code is **RO-Crate**

Not because it replaces Pāṭala, but because it might save a *lot* of boring corpus packaging work.

Its current 1.3 spec is designed around JSON-LD, files, datasets and contextual entities; it is extensible with additional linked-data vocabularies rather than demanding one giant ontology. ([researchobject.org][13])

A prototype could literally take 5 Sanderson/Ratié files and emit:

```text
scholar-pilot/
  ro-crate-metadata.json
  sources/
  extracted/
```

then layer:

```text
FaBiO identities
PROV derivations
Web Annotation spans
Pāṭala SourceAssertions
```

into the same graph.

If that remains pleasant rather than fighting the specification, we have our packaging foundation.

### My recommendation

**Do not build `Pāṭala Sources` as an isolated custom schema.**

Build:

> **Pāṭala Source Evidence Profile v0**

composed from:

```text
FaBiO
+ PROV-O
+ Web Annotation
+ CiTO
+ RO-Crate
+ IIIF compatibility
────────────────────
+ very small Pāṭala epistemic extension
```

Then test it on **5–10 ugly real files**, not the whole corpus.

If that vertical works, we can package Sanderson, Ratié, Torella, Sanskrit editions, images and future neuroscience/Greek/Buddhist corpora through the same substrate while keeping the things that are actually unique to Pāṭala—**assertion interpretation, corroboration, authority, review and dependency propagation**—native.

That looks like the correct end-state.

[1]: https://www.loc.gov/bibframe/docs/bibframe2-model.html?utm_source=chatgpt.com "Overview of the BIBFRAME 2.0 Model (BIBFRAME - Bibliographic Framework Initiative, Library of Congress)"
[2]: https://www.w3.org/TR/annotation-model/?utm_source=chatgpt.com "Web Annotation Data Model"
[3]: https://dvcs.w3.org/hg/prov/raw-file/tip/ontology/Overview.html?utm_source=chatgpt.com "PROV-O: The PROV Ontology"
[4]: https://sparontologies.github.io/cito/2018-02-12/cito.html?utm_source=chatgpt.com "CiTO, the Citation Typing Ontology"
[5]: https://www.researchobject.org/ro-crate/specification/1.1/introduction.html?utm_source=chatgpt.com "Introduction | Research Object Crate (RO-Crate)"
[6]: https://www.researchobject.org/ro-crate/specification/1.0/index.html?utm_source=chatgpt.com "RO-Crate 1.0 | Research Object Crate (RO-Crate)"
[7]: https://iiif.io/api/presentation/3.0/?utm_source=chatgpt.com "Presentation API 3.0 — IIIF | International Image Interoperability Framework"
[8]: https://datacite-metadata-schema.readthedocs.io/en/4.7/properties/relatedidentifier/?utm_source=chatgpt.com "12. RelatedIdentifier — DataCite Metadata Schema 4.7 documentation"
[9]: https://datacite-metadata-schema.readthedocs.io/en/4.7/appendices/appendix-1/relatedIdentifierType/?utm_source=chatgpt.com "relatedIdentifierType — DataCite Metadata Schema 4.7 documentation"
[10]: https://developers.openalex.org/api-reference/works?utm_source=chatgpt.com "Works Overview - OpenAlex Developers"
[11]: https://nanopub.net/guidelines/working_draft/?utm_source=chatgpt.com "Nanopublication Guidelines"
[12]: https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-ptr.html?utm_source=chatgpt.com "TEI element ptr (pointer)"
[13]: https://www.researchobject.org/ro-crate/specification/1.3/metadata?utm_source=chatgpt.com "Metadata of the RO-Crate | Research Object Crate (RO-Crate)"
