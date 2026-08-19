# IDEAS1.md — OpenAIRE Hackathon Strategy (Word-for-Word Analysis)

*2026-08-19*

---

## The Core Insight

After going through the OpenAIRE org, docs, current strategy, Broker, IIS, AffRo, contract tests, ScholeXplorer, MyResearchFolio, and their existing case studies, the opportunity is **not** "build another cool thing using the OpenAIRE Graph."

OpenAIRE already has a surprisingly complete research-intelligence stack:

```text
INGEST / INTEROPERABILITY
Guidelines · crosswalks · validators

            ↓

IDENTITY / CLEANING
AffRo · ROR · deduplication

            ↓

INFERENCE
IIS
citations · projects · datasets · software · affiliations
classification · similarity

            ↓

LINK EXCHANGE
Scholix / ScholeXplorer

            ↓

CHANGE / ENRICHMENT
Broker

            ↓

GRAPH
OpenAIRE Graph

            ↓

APPLICATIONS
Explore · Monitor · MyResearchFolio · Alien MCP
OPIX · Linknovate · national dashboards
```

IIS is particularly serious infrastructure: it ingests their information space, executes modular processing workflows, and feeds inferred relationships back into the Graph. Its actual workflow has switches for project-reference extraction, dataset-reference extraction, research initiatives, software URLs, citation matching, document similarity/classification and affiliation matching.

So **don't compete with that layer**.

The interesting place is immediately above it.

---

## The missing layer: `inference → obligation → judgment → history`

OpenAIRE can infer:

```text
paper P
  └── fundedBy → project X

author A
  └── affiliatedWith → institution Y

publication P
  └── uses → dataset D
```

What your architecture asks is different:

```text
WHY?

how was it inferred?
what evidence supports it?
did another source corroborate it?
has anyone challenged it?
has a human adjudicated it?
what did the graph believe last month?
what remains unresolved?
what physical evidence would settle it?
who is qualified to settle it?
```

That is basically **Wiggly's native data model already**. Its current architecture explicitly separates permanent identity/artifacts/observations/assertions/provenance/adjudication/history from active AI intelligence, with qualified state producing questions and proof obligations.

That is the seam I'd attack.

---

## The product: Pāṭala Research Protocol

### A proof-obligation and human-adjudication layer for AI-native scholarship.

Not Sanskrit software.

Not an OpenAIRE frontend.

A generic protocol demonstrated on **the unusually difficult case of Sanskrit manuscript scholarship**.

```text
                   OPENAIRE
                      │
         papers · people · projects
         datasets · organisations
                      │
                      ▼
               AI / IIS / MCP
                      │
            inferred knowledge
                      │
                      ▼
               PĀṬALA PROTOCOL
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
     PROVEN       UNCERTAIN       CONFLICTED
                                      │
                           ┌──────────┴──────────┐
                           ▼                     ▼
                    MACHINE TASK           HUMAN TASK
                           │                     │
                           ▼                     ▼
                    more evidence       qualified scholar
                           │                     │
                           └──────────┬──────────┘
                                      ▼
                                ADJUDICATION
                                      │
                               evidence + reason
                                      │
                                      ▼
                              APPEND-ONLY EVENT
                                      │
                                      ▼
                              QUALIFIED STATE
```

This takes OpenAIRE's "research intelligence as public infrastructure" position extremely literally. Their current strategy says research intelligence should be open, inspectable, governable and trustworthy, and specifically ties this to responsible research assessment and AI-ready scholarly reuse.

And Pāṭala's scholar vision already says almost exactly what the human component should be: AI handles search/alignment/candidate generation/evidence gathering; human experts perform the scarce judgment.

That is much more distinctive than another research assistant.

---

## The six strong products

| Product                          | OpenAIRE primitive               | Your primitive                    | Potential                        |
| -------------------------------- | -------------------------------- | --------------------------------- | -------------------------------- |
| **1. Scholar Relay**             | Graph + Person + MyResearchFolio | Pāṭala cruxes/adjudication        | **Best hackathon story**         |
| **2. GraphGit**                  | Graph API + contract tests       | append-only Pāṭala state          | **Very novel infra**             |
| **3. Broker Agent**              | OpenAIRE Broker                  | GitGoblin/QDW verification        | **Most immediately useful**      |
| **4. OpenScience CI**            | IIS/AffRo/API                    | QDW evaluator/red-team            | **Best dev tool**                |
| **5. Manuscript Reality Bridge** | publications/persons/projects    | Pāṭala manuscripts                | **Most distinctive domain demo** |
| **6. Contribution Ledger**       | MyResearchFolio                  | scholar events/CRediT-style roles | **Strategic longer-term**        |

---

## 1. Scholar Relay

OpenAIRE now has first-class researcher profiles and is building **MyResearchFolio** specifically to recognise contributions beyond papers—data, software, mentoring, leadership, community work and narrative evidence. Future plans explicitly include agents automatically discovering and organising contributions.

Your extension is:

> **What if agents discover not merely contributions, but the scholarly work that still needs humans?**

Example:

```text
Agent researching Tantrāloka

↓ gathers everything machine-accessible

OpenAIRE
Crossref
PANDiT
GRETIL
OpenAlex
published scholarship

↓

CRUX DETECTED

Witness A gives reading X
Edition B prints reading Y
Scholar C argues interpretation Z

machine confidence insufficient

↓

SCHOLAR RELAY

question:
Which reading is philologically preferable?

evidence packet:
  passages
  witnesses
  bibliography
  competing readings
  model arguments

expertise required:
  Sanskrit
  Kashmir Śaivism
  manuscript criticism

↓

OpenAIRE Person Graph

↓

plausible relevant researchers

↓

human adjudication

↓

citable contribution
```

This directly uses OpenAIRE's human network as part of an AI workflow.

---

## 2. GraphGit

This came from discovering their new API contract-test repository.

OpenAIRE itself recently built a record/replay system where it snapshots API results before a storage change, runs the same requests afterwards, and compares structural equivalence, identifier overlap and exact single-record values.

You can generalize that from:

> "Did the API break?"

to:

> **"How did scientific knowledge change?"**

Imagine:

```bash
graphgit log doi:10.xxx/foo
```

returns:

```text
2026-08

author affiliation changed
  UNKNOWN
  → ROR:03yrm5c26

funding relation added
  → Horizon Europe project X
  source: inferred

dataset relation removed
  previous confidence: .71

ORCID added
  source: ORCID/OpenAIRE

software relation added
  source: full-text extraction
```

And:

```bash
graphgit diff graph:11.2 graph:11.3 --topic "agent memory"
```

returns:

```text
+ 84 publications
+ 11 datasets
+ 17 software objects

+ 23 funding links
-  4 relations invalidated

5 organisations merged
7 authors resolved to ORCID

3 previous conclusions no longer supported
```

This is basically **Git for scholarly knowledge graphs**.

And Pāṭala already has **2,181 append-only events and a state digest** in the current repo.

---

## 3. Broker Agent

The OpenAIRE Broker already emits enrichment events when OpenAIRE knows something a repository doesn't—for example missing PIDs, project links, ORCID associations, OA versions, subjects, abstracts, publication dates, datasets and software links. Its public API exposes subscriptions and scrollable notification feeds.

You could build:

### **Broker Proof Agent**

```text
OpenAIRE Broker event

"Add ORCID X to author Y"

             ↓

        Proof Agent

             ↓

Crossref
ORCID
OpenAlex
ROR
institution
coauthors
publication history

             ↓

evidence bundle

      /              \
high confidence      ambiguous
      │                 │
      ▼                 ▼
AUTO-PROPOSE         HUMAN REVIEW
```

Crucially, **do not silently mutate repositories**.

Produce a PR-like review bundle.

---

## 4. OpenScience CI

OpenAIRE spends serious engineering effort avoiding false relationships. One IIS change tightened affiliation matching because even apparently strong fuzzy similarities could generate false positives; they tested the change against millions of relations and manually inspected samples.

Build:

### **OpenScience CI**

Property-based and adversarial testing for scholarly graphs.

```text
Graph / repository / CRIS
          ↓
    invariant suite
          ↓
 ┌────────┼────────┐
 ▼        ▼        ▼
identity relation provenance
 ▼        ▼        ▼
tests    tests     tests
          ↓
       QDW
   generates adversarial cases
          ↓
      regression corpus
```

Examples:

```text
same surname + different country

same organisation alias +
different ROR

paper has DOI in Crossref
but another DOI in repository

dataset relation exists
but cited DOI resolves elsewhere

grant relation inferred
but publication predates project

author ORCID conflicts
with known affiliation timeline
```

---

## 5. Manuscript Reality Bridge

This is where Sanskrit becomes the hackathon's visual centerpiece.

OpenAIRE already connects:

```text
publication
dataset
software
person
organisation
project
```

But manuscript scholarship has another ontology:

```text
PHYSICAL OBJECT
    ↓
MANUSCRIPT WITNESS
    ↓
DIGITAL IMAGE
    ↓
TRANSCRIPTION
    ↓
EDITION
    ↓
PASSAGE
    ↓
TRANSLATION
    ↓
CLAIM
    ↓
SCHOLARSHIP
```

So build an extension:

```text
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
```

---

## 6. Contribution Ledger

More strategic than hackathon-ready.

Your scholar model says a researcher might have:

```text
83 cruxes adjudicated
27 alternative readings
14 argument reconstructions
6 counterexamples
```

and treats those as meaningful contributions rather than invisible labor.

Define a generic:

```yaml
ScholarlyContributionEvent:
  contributor:
  role:
  object:
  activity:
  evidence:
  decision:
  timestamp:
  provenance:
  citation:
```

Possible activities:

```text
DATA_CURATION
VALIDATION
ADJUDICATION
TRANSCRIPTION
ENTITY_RESOLUTION
REPRODUCTION
COUNTEREXAMPLE
ONTOLOGY_CURRATION
EVIDENCE_ACQUISITION
```

Now Scholar Relay tasks turn automatically into research-assessment evidence.

---

## Things NOT to build

**Don't build generic OpenAIRE MCP/RAG.** Alien has already done it.

**Don't build generic "emerging research radar."** OPIX already does this.

**Don't build organisation dedupe.** AffRo and OpenOrgs cover this.

**Don't build another research dashboard.** MONITOR and national monitors exist.

**Don't build generic researcher profiles.** MyResearchFolio is already a major direction.

**Don't build basic metadata enrichment.** Broker already does this at production scale.

---

## What I'd submit tomorrow

Combine **three** of the ideas into one coherent entry:

### **Pāṭala — Proof Obligations for Open Science**

Tagline: **AI can find the literature. Pāṭala tracks what still needs to be proven.**

Demo:

```text
1. Ask a real Sanskrit research question.

2. OpenAIRE finds:
   papers
   researchers
   organisations
   related scholarship.

3. Pāṭala resolves the modern scholarship
   against a primary manuscript/text graph.

4. Agent builds an EvidencePacket.

5. One claim cannot be established.

6. Pāṭala emits:

   PROOF OBLIGATION #17

   type: EXPERT_ADJUDICATION
   reason: conflicting readings
   evidence: [...]
   skills: Sanskrit / Śaiva textual criticism

7. OpenAIRE Person graph suggests
   relevant expertise.

8. Human decision is recorded.

9. Pāṭala ledger updates.

10. GraphGit shows:

    + claim corroborated
    + contributor credited
    + state digest changed
```

## The killer longer-term architecture

Eventually GitGoblin becomes **ScholarGoblin**:

```text
OpenAIRE Graph update
Broker event
new Crossref record
new paper
new dataset
new manuscript digitisation
new GitHub research software release
            │
            ▼
         GitGoblin
      detects change
            │
            ▼
          Pāṭala
   identifies affected claims
            │
            ▼
       proof obligations
            │
       ┌────┴─────┐
       ▼          ▼
      QDW       scholar
       │          │
 experiment    judgment
       │          │
       └────┬─────┘
            ▼
       evidence event
            ▼
   new qualified knowledge
```

That is essentially **continuous integration for human knowledge**.
