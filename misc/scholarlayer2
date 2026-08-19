Yes. The biggest thing I missed was that we were mixing **storage/interoperability standards** with **evaluation/benchmark infrastructure**. `TantraFact` belongs to a different plane entirely, and there are several other pieces worth adding.

The architecture should really have **four separate standards families**:

```text
1. IDENTIFY / PACKAGE SOURCES
2. ADDRESS / EXPOSE CONTENT
3. REPRESENT EVIDENCE + REASONING
4. TEST WHETHER THE SYSTEM ACTUALLY WORKS
```

The fourth one is where **TantraFact** belongs.

## TantraFact should absolutely remain in the architecture

Its closest precedents are **SciFact + FEVER**, with some ideas from FEVEROUS and MultiVerS.

SciFact's task is almost exactly the skeleton we want: given a claim, retrieve evidence from scholarly literature, classify the relation, and return exact rationale spans. Its labels are essentially support/refute plus evidence rationales. ([ACL Anthology][1])

FEVER adds the very important third outcome:

```text
SUPPORTS
REFUTES
NOT ENOUGH INFO
```

plus evidence sets. ([ACL Anthology][2])

That maps beautifully onto Pāṭala:

```text
SciFact / FEVER       TantraFact

SUPPORTS          →   SUPPORTED
REFUTES           →   REFUTED
NOT ENOUGH INFO   →   UNDERDETERMINED

evidence sentence →   exact SourceSpan
claim             →   Proposition
document          →   Publication/Witness
```

But **TantraFact should be considerably stricter** because philosophical claims have scope, attribution, modality and interpretive ambiguity that biomedical factual claims often do not.

I would eventually make each TantraFact example something like:

```json
{
  "claim_ref": "pt:prop:...",
  "claim": "...",

  "debate_frame": "...",

  "evidence": [
    {
      "span_ref": "pt:span:...",
      "role": "SUPPORT",
      "source_assertion_ref": "..."
    }
  ],

  "verdict": "UNDERDETERMINED",

  "defeaters": [
    "SCOPE_DIFFERENCE",
    "ATTRIBUTION_UNCERTAIN"
  ],

  "rationale_refs": ["..."],

  "gold_origin": "HUMAN_ADJUDICATED"
}
```

And crucially:

> **TantraFact should not be generated from the same machine-produced graph it evaluates.**

Otherwise we have circular evaluation again.

---

## FEVEROUS gives us another future extension

FEVEROUS expands verification beyond ordinary prose to evidence from structured material such as tables and lists, and evaluates both the verdict and evidence retrieval. ([ACL Anthology][3])

That becomes relevant once Pāṭala evidence includes:

```text
scholarly prose
tables
critical apparatus
manuscript metadata
argument graphs
figures
```

So I would design `EvidenceTarget` as polymorphic now:

```text
TextSpan
TableCell
FigureRegion
GraphNode
DataRecord
```

even if TantraFact v0 uses only text spans.

Do not implement multimodality yet.

Just don't make the schema text-only.

---

## MultiVerS is relevant later as a baseline, not architecture

MultiVerS performs scientific claim verification using full-document context while jointly predicting the verdict and rationale sentences. ([ACL Anthology][4])

That's a very useful model-design precedent for the eventual `scholar-corroborate` evaluator because our evidence often requires more than a single matching sentence.

But I would not adopt its architecture as Pāṭala's.

Use it as:

```text
baseline / comparison system
```

not epistemic machinery.

Same principle as xAIF/SEPIO.

---

# A major omission: CTS / DTS for primary-text identity

This might actually be more important than some of the bibliography standards we discussed.

**Canonical Text Services (CTS)** was explicitly designed to provide persistent, technology-independent identifiers for scholarly texts **and passages within texts**. Its identifier structure separates namespace, work hierarchy and passage citation. ([CITE Architecture][5])

For example conceptually:

```text
urn:cts:patala:abhinavagupta.ipvv.editionX:1.3.7
```

Pāṭala does not have to literally replace `pt:*` IDs with CTS URNs.

But its primary-text identity model should be **CTS-compatible**:

```text
TextGroup
→ Work
→ Edition / Translation
→ Passage
```

This is extremely relevant to:

```text
IPK
IPVV
Tantrāloka
commentaries
editions
translations
canonical passage references
```

It solves a different problem from Web Annotation.

### CTS vs Web Annotation

They're complementary:

```text
CTS
= what canonical textual passage is this?

Web Annotation selectors
= where exactly is this span in this particular digital witness?
```

That's powerful.

You could have:

```text
canonical:
IPVV 1.3.7

witness:
Torella edition PDF sha...

physical locator:
p. 83

digital locator:
characters 18392–18810

text integrity:
sha256...
```

That is a much stronger citation model.

---

## And DTS is the modern API layer for texts

The **Distributed Text Services (DTS)** specification defines interoperable APIs for collections of texts, navigation within texts, and retrieval of full or partial texts. Its 1.0 release candidate was published in 2025. ([Distributed Text Services][6])

That means Pāṭala's future public text API should probably be:

```text
internally:
pt:* IDs / canonical graph

externally:
DTS-compatible text retrieval
```

rather than inventing an entirely proprietary endpoint design.

That is especially appealing for the site and future scholarly integration.

So add:

```text
CTS-compatible identifiers
+
DTS-compatible text API
```

to our standards matrix.

---

# Another omission: JATS for modern scholarship ingestion

For journal articles, JATS is a mature standard specifically for preserving and exchanging article metadata, textual structure and graphical content. The current standard is JATS 1.4 / ANSI-NISO Z39.96-2024. ([NISO][7])

This matters because sometimes we will get:

```text
publisher XML / JATS
```

rather than:

```text
terrible PDF
↓
OCR
↓
guess section boundaries
```

If JATS exists, use it.

The ingestion hierarchy should therefore be something like:

```text
BEST
publisher JATS/XML
↓
structured HTML
↓
born-digital PDF
↓
OCR PDF
WORST
```

and the `DocumentWitness` records which representation generated the normalized text.

Again, don't convert everything to JATS ourselves.

Just **consume it losslessly when available**.

---

# Persistent people and organization identities were also missing

We shouldn't invent identities for scholars where global identifiers already exist.

**ORCID** provides persistent identifiers for researchers and their scholarly activities. ([ORCID][8])

**ROR** provides open persistent identifiers for research organizations and is explicitly designed to connect organizations to researchers and outputs. ([Research Organization Registry (ROR)][9])

So:

```text
pt:person:isabelle-ratie
  sameAs ORCID:...

pt:org:ephe
  sameAs ROR:...
```

Pāṭala still owns its internal ID because not every historical scholar/author has an ORCID.

But external IDs should be attached where available.

For historical actors:

```text
Abhinavagupta
Utpaladeva
Bhartṛhari
```

Wikidata/VIAF identifiers may eventually be useful as external crosswalks, though I wouldn't make them canonical.

---

# OpenCitations is worth adding to the citation layer

I mentioned CiTO as a relation vocabulary, but missed **OpenCitations Meta** as an actual open bibliographic/citation infrastructure.

OpenCitations Meta specifically tries to disambiguate publications represented by different identifiers, assigns its own identifiers where external PIDs are absent, and preserves provenance of its bibliographic metadata. ([arXiv][10])

That is extremely relevant to:

```text
same article
DOI
Academia PDF
Crossref record
local PDF
citation in another article
```

So enrichment priority probably becomes:

```text
Crossref / DataCite
OpenAlex
OpenCitations
ORCID
ROR
```

as **metadata witnesses**, not authorities.

---

# QASPER belongs in the education/research-question evaluation family

QASPER contains questions about full research papers, answers, and human-selected supporting evidence; it was specifically designed around information-seeking questions that require reasoning across scientific papers. ([arXiv][11])

That's not TantraFact.

It's closer to a future:

```text
PāṭalaQA
```

benchmark:

> Given this scholarly question, can the system answer it using the corpus and return the evidence that licenses the answer?

Potential benchmark families therefore become:

```text
TantraFact
claim → evidence → verdict

ArgumentBench
passage → propositions/inferences/abstention

PāṭalaQA
question → answer + evidence

CorroborationBench
proposition → scholarly support/conflict

CitationBench
claim → exact source + attribution
```

You don't need all of these now.

But the architecture should distinguish them.

---

# So the updated standards landscape is larger

Here's the corrected complete picture I would freeze:

| Problem                            | Standard/project to borrow    |
| ---------------------------------- | ----------------------------- |
| Bibliographic identity             | **FaBiO**                     |
| Library exchange                   | **BIBFRAME**                  |
| Research IDs                       | **DOI / DataCite / Crossref** |
| Scholar identity                   | **ORCID**                     |
| Institution identity               | **ROR**                       |
| Citation graph/enrichment          | **OpenCitations / OpenAlex**  |
| Corpus packaging                   | **RO-Crate**                  |
| Generic provenance                 | **PROV-O**                    |
| Fine-grained arbitrary spans       | **W3C Web Annotation**        |
| Canonical primary-text passages    | **CTS URNs**                  |
| Text collection/retrieval API      | **DTS**                       |
| Journal full text                  | **JATS**                      |
| Critical/textual editions          | **TEI**                       |
| Images/manuscripts/media           | **IIIF**                      |
| Citation semantics                 | **CiTO**                      |
| Atomic assertion publishing        | **Nanopublications**          |
| Argument interchange               | **xAIF**                      |
| Scientific evidence vocabulary     | **SEPIO**                     |
| Claim-verification benchmark       | **SciFact / FEVER**           |
| Structured/multimodal verification | **FEVEROUS**                  |
| Full-document verifier baseline    | **MultiVerS**                 |
| Document-grounded QA benchmark     | **QASPER**                    |
| Pāṭala-specific verification       | **TantraFact**                |

That's now much closer to complete.

---

# But there is an important simplification

We should **not implement 20 standards**.

They fall into three categories:

### Build compatibility into the schema now

```text
FaBiO-ish bibliographic identity
PROV-O provenance semantics
Web Annotation selectors
CTS-compatible textual identity
ORCID/ROR/external IDs
rights/licensing
```

These influence foundational object design.

### Adopt as adapters later

```text
RO-Crate
DTS
IIIF
TEI
JATS
CiTO
BIBFRAME
nanopub
xAIF
SEPIO
```

Do not burden v0 with runtime dependencies.

### Use as benchmark inspiration

```text
SciFact
FEVER
FEVEROUS
MultiVerS
QASPER
```

No ontology dependency at all.

---

# Where TantraFact belongs in the end-state

I'd now put it here:

```text
                         PĀṬALA

SOURCE SUBSTRATE
       ↓
primary text ───────── scholarship
       ↓                   ↓
L0/L2/L200/C1        SourceAssertions
       \                   /
        \                 /
          PROPOSITIONS
               ↓
           ARGUMENTS
               ↓
          SYNTHESES
               ↓
         ESSAY / EDUCATION


────────────────────────────────────
           EVALUATION PLANE
────────────────────────────────────

TantraFact
  proposition
  → retrieve evidence
  → exact rationale
  → support/refute/underdetermined

ArgumentBench
  passage
  → structured reasoning

PāṭalaQA
  question
  → grounded answer

CorroborationBench
  proposition
  → scholar evidence relation
```

This is important because **benchmarks sit outside the production graph**.

They test it.

They are not just more graph content.

---

## And I think there is one particularly valuable benchmark innovation

SciFact/FEVER mostly ask:

> Is claim C supported by source S?

Pāṭala can ask the harder question:

> **At what exact layer does support fail?**

For example:

```text
SOURCE EXISTS                   PASS
SPAN SUPPORTS PARAPHRASE        PASS
ATTRIBUTION CORRECT             PASS
SCOPE MATCH                     FAIL
INFERENCE WARRANT               UNRESOLVED
CONCLUSION                      UNDERDETERMINED
```

That gives a process benchmark rather than merely final-label accuracy.

That's a much more Pāṭala-native `TantraFact`.

It would evaluate **epistemic conservation** itself.

And that, rather than another general fact-check dataset, could eventually become a genuinely interesting research contribution.

[1]: https://aclanthology.org/2020.emnlp-main.609/?utm_source=chatgpt.com "Fact or Fiction: Verifying Scientific Claims - ACL Anthology"
[2]: https://aclanthology.org/N18-1074/?utm_source=chatgpt.com "FEVER: a Large-scale Dataset for Fact Extraction and VERification - ACL Anthology"
[3]: https://aclanthology.org/2021.fever-1.1/?utm_source=chatgpt.com "The Fact Extraction and VERification Over Unstructured and Structured information (FEVEROUS) Shared Task - ACL Anthology"
[4]: https://aclanthology.org/2022.findings-naacl.6/?utm_source=chatgpt.com "MultiVerS: Improving scientific claim verification with weak supervision and full-document context - ACL Anthology"
[5]: https://cite-architecture.github.io/ctsurn_spec/?utm_source=chatgpt.com "Canonical Text Services protocol specification"
[6]: https://distributed-text-services.github.io/specifications/?utm_source=chatgpt.com "Distributed Text Services (DTS) - Distributed Text Services"
[7]: https://www.niso.org/standards-committees/jats?utm_source=chatgpt.com "Standardized Markup for Journal Articles: Journal Article Tag Suite (JATS) | NISO website"
[8]: https://support.orcid.org/hc/en-us/articles/360006973993-What-is-ORCID?utm_source=chatgpt.com "What is ORCID? – ORCID"
[9]: https://ror.org/about/?utm_source=chatgpt.com "Research Organization Registry (ROR) | About"
[10]: https://arxiv.org/abs/2306.16191?utm_source=chatgpt.com "OpenCitations Meta"
[11]: https://arxiv.org/abs/2105.03011?utm_source=chatgpt.com "A Dataset of Information-Seeking Questions and Answers Anchored in Research Papers"
