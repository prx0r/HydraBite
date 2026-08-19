Yes. This is a major underused asset. The papers should become **a computable commentary layer over the primary-source graph**, not a pile of PDFs and not just embeddings for RAG.

The core transformation should be:

```text
PAPER
  ↓
SCHOLAR CONTRIBUTION PACKET
  ├─ questions answered
  ├─ claims made
  ├─ interpretations proposed
  ├─ primary passages interpreted
  ├─ evidence used
  ├─ arguments
  ├─ distinctions
  ├─ definitions / term senses
  ├─ objections to other scholars
  ├─ agreements / disagreements
  ├─ comparisons
  ├─ quotations
  ├─ uncertainty / qualifications
  ├─ citations and their roles
  └─ open questions
```

There is strong precedent for this. ORKG exists specifically to turn document-bound scholarship into machine-actionable research contributions that can be queried and compared; work built on ORKG represents contributions as structured units instead of document summaries. ([arXiv][1]) A 2025 paper goes directly toward your intuition by extracting a paper's central content as question-answer pairs, and the 2026 SocraticKG pipeline uses self-contained QA pairs as an intermediate representation before extracting and canonicalizing graph triples. ([arXiv][2])

But for Pāṭala, **QA is only one projection of a richer scholarly object**.

# The actual ontology I would use

A paper like Ratié on Pratyabhijñā should generate objects roughly like:

```yaml
ScholarlyWork:
  id: WORK-ratie-2011-x
  title:
  authors:
    - SCHOLAR-ratie
  doi:
  openalex_id:
  semantic_scholar_id:
  year:
  rights:
  source_file:
```

OpenAlex already gives us a large external scholarly graph connecting works, authors, institutions, topics and citations, while Semantic Scholar exposes papers, authors, citations, references and embeddings. They should be external identity/enrichment layers, not replace our own canonical objects. ([OpenAlex][3])

Then extract:

```yaml
ScholarPosition:
  id: POS-00491
  scholar_id: SCHOLAR-ratie
  work_id: WORK-ratie-2011-x

  proposition:
    "..."

  type:
    INTERPRETATION

  about:
    - CONCEPT-recognition
    - PASSAGE-ipk-x
    - ARGUMENT-14

  modality:
    asserted | probable | tentative | rejected

  source_span:
    page: 52
    paragraph: 3

  evidence_used:
    - PASSAGE-ipvv-x
    - WORK-torella-x

  confidence:
    extraction: .94

  review_state:
    MACHINE_EXTRACTED
```

This distinction is essential:

```text
PRIMARY SOURCE SAYS X
```

is not the same object as:

```text
RATIÉ INTERPRETS SOURCE AS X
```

which is not the same as:

```text
PĀṬALA CURRENTLY ACCEPTS X
```

You can now preserve the entire scholarly debate.

---

# Think of the secondary literature as a giant **commentarial graph**

You've already got:

```text
SANSKRIT
  ↓
translation
  ↓
proposition
  ↓
argument
```

Now add:

```text
                         PRIMARY PASSAGE
                               │
            ┌──────────────────┼──────────────────┐
            ↓                  ↓                  ↓
       Scholar A           Scholar B          Scholar C
     interprets X        interprets Y        qualifies X
            │                  │                  │
            └──────────────────┼──────────────────┘
                               ↓
                         Debate / Crux
                               ↓
                      Pāṭala adjudication
```

This turns thousands of secondary papers into a **live history of interpretation**.

And it means an answer can say:

> The primary text establishes A. Ratié reads this as B. Torella instead emphasizes C. The point on which they diverge is D.

Every clause can resolve downward to the exact relevant scholarly object.

That is much better than generic RAG.

---

# Yes: extract **questions each scholar answers**

I think this should be mandatory.

Every significant contribution should generate one or more canonical questions:

```yaml
Question:
  id: Q-119

  canonical:
    "What does recognition add if the self is already present?"

ScholarAnswer:
  question_id: Q-119
  scholar_id: SCHOLAR-x
  work_id: WORK-x

  answer_proposition_ids:
    - PROP-81
    - PROP-82

  evidence_ids:
    - PASSAGE-77

  source_span_ids:
    - SPAN-881
```

Then another paper:

```text
Q-119
 ├── Scholar A answer
 ├── Scholar B answer
 ├── Scholar C answer
 └── Pāṭala synthesis
```

Now a consumer asks naturally:

> Why is recognition necessary?

You don't perform fuzzy document RAG and hope.

Resolve:

```text
user utterance
   ↓
Q-119
   ↓
answer graph
   ↓
primary evidence
+ scholar positions
+ debate state
   ↓
personalized rendering
```

This is massive.

---

# SocraticKG is particularly useful here

Its current pipeline is essentially:

```text
document
   ↓
5W1H self-contained questions/answers
   ↓
atomic triples
   ↓
entity/relation canonicalization
```

and it argues that QA as an intermediate representation surfaces causal and procedural information that direct text-to-triple extraction can miss. ([GitHub][4])

I would copy that mechanism but replace generic 5W1H with **Pāṭala scholarly competency questions**.

For every substantive section, ask automatically:

```text
What question is the author answering?

What does the author claim?

What primary source is being interpreted?

What reading is proposed?

What evidence supports it?

Which previous scholar is being agreed with?

Which scholar is being challenged?

What distinction does the argument depend on?

What alternative interpretation is rejected?

What remains uncertain?

What follows if the interpretation is correct?
```

Then extract graph objects from the answers.

This is much safer than:

> Convert this 45-page humanities article straight into triples.

---

# Papers should generate many object types, not one “summary”

This is where I think Pāṭala can be much better than existing scientific KGs.

SciClaim demonstrates that fine-grained scientific claims benefit from representing qualifications and relation attributes rather than merely extracting naked entity-relation-entity triples. ([arXiv][5]) Scholarly argument-mining work likewise separates argumentative units from their support/attack relations, and full-text scholarly argument mining remains difficult enough that we should keep extraction claims reviewable rather than treating model output as truth. ([ACL Anthology][6])

For humanities/scholarship, I'd extract roughly these semantic categories in one `ScholarContributionPacket`:

| Object              | Example use                                    |
| ------------------- | ---------------------------------------------- |
| **Question**        | What problem is this passage/paper addressing? |
| **Claim**           | Scholar asserts X                              |
| **Interpretation**  | Passage P should be read as X                  |
| **Definition**      | Scholar uses *vimarśa* in sense S              |
| **Distinction**     | X must be distinguished from Y                 |
| **Argument**        | P1 + P2 → C                                    |
| **EvidenceUse**     | Passage P supports claim C                     |
| **Objection**       | Scholar attacks another position               |
| **Reply**           | Scholar answers objection O                    |
| **Agreement**       | A explicitly follows B                         |
| **Disagreement**    | A rejects B on crux C                          |
| **Qualification**   | X only under condition Y                       |
| **Comparison**      | Śaiva X compared to Buddhist Y                 |
| **CitationUse**     | Why this cited work appears here               |
| **ResearchGap**     | Author says question remains unresolved        |
| **Quote**           | Exact authorized/limited source wording        |
| **PedagogicalSeed** | Particularly explanatory distinction/example   |
| **MediaSeed**       | Strong mystery, dispute, example or reversal   |

Citation-intent modeling is useful here because a citation is not merely an edge `A CITES B`; existing work classifies functions such as background, method use and comparison. ([arXiv][7])

For us, citation roles should become more philosophical:

```text
CITES_AS_SUPPORT
CITES_AS_OPPONENT
CITES_AS_PRECEDENT
CITES_FOR_TRANSLATION
CITES_FOR_TEXTUAL_READING
CITES_FOR_DEFINITION
CITES_AS_PARALLEL
CITES_AS_COUNTEREXAMPLE
CITES_FOR_HISTORICAL_CONTEXT
```

That makes the scholarly citation network substantially more meaningful.

---

# Then the paper becomes **answerable**

Suppose Pāṭala ingests 300 papers concerning recognition.

We can ask graph queries like:

```text
Which scholars explicitly distinguish
recognition from memory?
```

or:

```text
Which scholars interpret IPK 1.1.2?

Show:
  interpretation
  supporting evidence
  disagreements
  chronology
```

or:

```text
What are all proposed explanations for
why recognition is necessary?

Group by underlying answer.
```

That last one is especially powerful.

Perhaps 87 passages from 31 papers collapse into five canonical positions.

```text
QUESTION:
Why is recognition necessary?

POSITION A
Because recognition removes non-recognition.

POSITION B
Because latent identity is not phenomenally manifest.

POSITION C
Because reflexive articulation is constitutive.

...
```

And every position preserves:

```text
authors
works
source spans
primary evidence
supporters
opponents
dates
```

You've turned an impossible literature review into a structured debate.

---

# This makes the consumer-question system even stronger

Before we were saying:

```text
CONSUMERS
→ questions
→ research gaps
```

Now:

```text
consumer question
       ↓
canonical Question
       ↓
existing scholarly answer graph?
       │
      YES
       ↓
render answer

      NO / PARTIAL
       ↓
search secondary corpus
       ↓
extract relevant ScholarPositions
       ↓
possibly resolve gap
```

So **your secondary corpus becomes a reservoir waiting to be activated by user questions**.

A consumer might ask something nobody at Pāṭala thought to structure explicitly.

The research agent discovers that three scholars already addressed it indirectly.

It creates:

```text
new Question
new answer associations
new debate relationships
```

The consumer has caused old scholarship to become newly structured.

That is another compounding mechanism.

---

# Scholar attribution can be much richer than citations

Yes, give the scholar credit whenever their contribution materially appears.

I would create a first-class:

```yaml
AttributionEvent:
  id:
  scholar_id:
  work_id:
  contribution_id:

  use_type:
    DIRECT_QUOTE
    PARAPHRASED_POSITION
    EVIDENCE_SOURCE
    INTERPRETIVE_DEPENDENCY
    CONTRASTED_POSITION
    PEDAGOGICAL_SOURCE

  output:
    answer | essay | lesson | video | benchmark

  output_id:

  public:
    true

  timestamp:
```

Then a scholar's Pāṭala page eventually shows:

```text
Alexis Sanderson

PĀṬALA CONTRIBUTION IMPACT

Works represented             43
Positions represented        281
Primary passages linked      712
Consumer answers informed  84,212
Lessons informed              146
Essays informed                38
Videos informed                17
Research questions resolved    24
```

That is an entirely new type of scholarly impact metric.

Not:

> paper has 421 citations.

But:

> **this specific intellectual contribution has been used to help 84,000 people understand something.**

That connects beautifully to the scholar-economics vision.

---

# You could even credit **specific intellectual contributions**

Scholar reputation should not be one number.

Example:

```text
Scholar X

KNOWN FOR

Recognition / memory distinction
  → 18 downstream explainers

Reading of IPVV 1.3.7
  → 7 downstream arguments

Interpretation of pratibimba
  → 12 comparisons
```

It's almost an **intellectual contribution graph**.

This is much more interesting than Google Scholar.

OpenAlex gives us author/work identities and citation structure; ORCID provides persistent researcher identities and can represent contributor roles, while CRediT provides a standardized 14-role taxonomy for contributions. ([OpenAlex][8])

Pāṭala can build a more domain-specific layer above those standards.

---

# And scholar credit can feed payments

Eventually:

```text
Revenue
  ↓
scholarly attribution graph
  ↓
transparent contribution accounting
```

I wouldn't do naïve Spotify-style per-word royalty accounting.

But you can have things like:

```text
commissioned review
expert adjudication
new translation
licensed commentary
course contribution
live Q&A
```

and attach downstream impact.

If a scholar explicitly contributes material to Pāṭala under an agreed license, derivative uses could even carry agreed revenue-sharing rules.

That is much cleaner than trying to infer payment rights from random published papers.

---

# Important distinction: **credit is not permission**

This is where we need to design carefully.

Having a PDF from Academia.edu does **not** automatically mean Pāṭala can republish its wording.

Attribution and copyright are different things.

For each paper I would ingest:

```yaml
RightsState:
  copyright_holder:
  source_url:
  license:
  oa_status:

  internal_analysis:
    allowed_or_review_needed

  public_quote:
    allowed_extent

  public_fulltext:
    yes/no

  derivative_permission:
    yes/no/unknown
```

The U.S. Copyright Office explicitly notes that limited quotation for criticism, teaching, scholarship and research can sometimes qualify as fair use, but there is no fixed safe word count or percentage; fair use is case-specific and includes factors such as amount used and market effect. ([U.S. Copyright Office][9])

So architecturally:

```text
INTERNAL EXTRACTION
        ≠
PUBLIC REPUBLICATION
```

This is essential.

For copyrighted secondary papers, public outputs should usually prefer:

```text
structured propositions
+
our own synthesis
+
citation
+
small justified quotation where appropriate
```

rather than reproducing substantial source prose.

And for scholar-submitted/licensed material, we can permit more.

---

# Exact wording should be a special object

Never let the AI accidentally blur:

```text
Scholar actually wrote this
```

and:

```text
Pāṭala paraphrased their position.
```

Have:

```yaml
Quote:
  text:
  work_id:
  scholar_id:
  source_span_id:
  page:
  exact: true

  rights_basis:
  license | permission | limited_quotation

  max_public_use:
```

Then generated answers have tokens like:

```text
[QUOTE:Q881]
```

that only a rendering service authorized for that quote can expand.

Everything else becomes:

```yaml
Paraphrase:
  proposition_ids: [...]
  attribution:
    scholar_id:
  generated_by:
  fidelity_status:
```

This makes provenance extraordinarily clean.

---

# The AI-writing idea needs one adjustment

You said:

> once we have it all in data format we like we can easily use AI to write similar

Yes in the sense of **writing new Pāṭala essays from the structured intellectual material**.

I would specifically *not* train it to mimic a living scholar's distinctive prose style.

The much stronger product is:

```text
Sanderson evidence
+ Ratié interpretation
+ Torella disagreement
+ primary texts
+ Pāṭala argument graph
+ consumer question data
        ↓
PĀṬALA HOUSE STYLE
        ↓
new explainer / essay / lesson / script
```

The scholarly corpus supplies **knowledge, argument patterns, distinctions, citations and intellectual structure**, not prose imitation.

That's cleaner academically and gives Pāṭala its own recognizable editorial voice.

---

# A paper can generate essays automatically at several levels

Suppose one 40-page article yields:

```text
18 important questions
31 claims
11 interpretations
8 primary-source links
6 distinctions
4 objections
2 significant disagreements
1 large thesis
```

That could automatically feed:

```text
1 deep scholar-oriented paper summary

3 concept explainers

4 "scholars disagree" essays

8 answers to canonical questions

6 interactive learning exercises

10 short video concepts

2 long-form documentary sections

1 scholar profile update

several benchmark cases
```

But all of them derive from the same structured packet.

So:

```text
PAPER
 ↓
ScholarContributionPacket
 ↓
       ┌────────┬────────┬────────┬────────┐
       ↓        ↓        ↓        ↓        ↓
      ASK      READ     LEARN    ESSAY    VIDEO
```

**Research once; render repeatedly** becomes much stronger.

---

# The essay should itself remain a graph projection

Don't save:

```text
essay.md
```

as the deepest canonical object.

Save:

```yaml
Synthesis:
  question_id:
  thesis:
  proposition_ids:
  evidence_use_ids:
  scholar_position_ids:
  objection_ids:
  crux_ids:
  uncertainty:
  review_state:
```

Then `essay.md` is one renderer.

So later:

```text
same synthesis
→ beginner essay
→ scholarly essay
→ 18-minute video
→ interactive argument
→ AI answer
```

No intellectual drift between formats.

---

# There's a particularly useful existing idea from ORKG

ORKG represents the research contribution rather than just the publication and supports comparing contributions across papers. ([arXiv][10])

Its scientific schemas often revolve around categories such as:

```text
ResearchProblem
Approach
Method
Results
Dataset
```

For Pāṭala humanities scholarship I'd make the equivalent:

```text
ResearchQuestion
TextualObject
ScholarPosition
Interpretation
EvidenceUse
Argument
Distinction
TermSense
OpponentPosition
Crux
HistoricalClaim
Conclusion
OpenQuestion
```

That's essentially **ORKG for intellectual history and textual philosophy**, with much deeper source provenance.

---

# And the newest technical mechanism I would seriously test is SocraticKG

Full project:

`https://github.com/LABA-SNU/SocraticKG`

Paper:

`https://arxiv.org/abs/2601.10003`

It specifically uses QA generation as a structured intermediate layer before graph extraction and then canonicalizes synonymous entities/relations. ([GitHub][4])

For our use I'd change:

```text
5W1H
```

into:

```text
PĀṬALA SCHOLAR INTERROGATOR

What question is answered?
What position is advanced?
What primary passage is interpreted?
What does this reading depend upon?
What alternative is rejected?
What evidence is given?
Who is being followed?
Who is being corrected?
Where is the author uncertain?
What downstream proposition follows?
```

That could be extraordinarily effective on your Academia corpus.

---

# The paper-ingestion pipeline I would actually build

```text
PDF
 │
 ▼
0. RIGHTS + IDENTITY
   DOI / OpenAlex / author / ORCID / license
 │
 ▼
1. STRUCTURE
   headings / pages / paragraphs / footnotes / bibliography
 │
 ▼
2. SCHOLARLY INTERROGATION
   section → canonical QA candidates
 │
 ▼
3. ATOMIC EXTRACTION
   claims / interpretations / evidence / definitions /
   objections / distinctions / citations
 │
 ▼
4. ARGUMENT RECONSTRUCTION
   premise / conclusion / support / attack / qualify
 │
 ▼
5. PRIMARY-SOURCE ALIGNMENT
   resolve Sanskrit/text references → Pāṭala IDs
 │
 ▼
6. SCHOLAR ALIGNMENT
   resolve citations → Work + Scholar IDs
 │
 ▼
7. CANONICALIZATION
   merge equivalent questions / concepts / positions
 │
 ▼
8. ADVERSARIAL PASS
   check overstatement / polarity / attribution /
   source support / alternative reading
 │
 ▼
9. SCHOLAR CONTRIBUTION PACKET
 │
 ├─ QuestionAnswers
 ├─ Positions
 ├─ Arguments
 ├─ TermSenses
 ├─ EvidenceUses
 ├─ Quotes
 ├─ Debates
 └─ ResearchGaps
 │
 ▼
10. GRAPH PROPOSAL
     MACHINE_PROPOSED
 │
 ▼
11. PĀṬALA SURFACES
     Ask / Read / Learn / Scholar / Media
```

Full-text scholarly argument mining research strongly suggests the decomposition matters: identifying argumentative discourse units and extracting relations between them are distinct difficult tasks, rather than one reliable one-shot operation. ([ACL Anthology][11])

---

# The really big compounding loop

Now combine this with the consumer system:

```text
1,000 PAPERS
      ↓
20,000 scholarly Questions
80,000 ScholarPositions
40,000 EvidenceUses
      ↓
CONSUMER APP
      ↓
users ask 500,000 questions
      ↓
map to existing scholarly Questions
      │
      ├── answer exists → render
      │
      └── answer missing
             ↓
      search paper corpus
             ↓
      recover latent answer
             ↓
      new structured objects
             ↓
      graph expands
```

Then:

```text
unanswered user demand
       ↓
tells us what papers to ingest more deeply

paper extraction
       ↓
improves consumer answers

consumer questions
       ↓
reveal hidden relationships between papers

scholars review
       ↓
canonicalize the best answers

canonical answers
       ↓
essays / videos / learning

those bring more users
       ↓
more questions
```

That is an extremely strong system.

The Academia corpus isn't simply “training material.”

**It is dormant structured scholarship.**

The job is to turn every paper into thousands of addressable intellectual atoms while preserving exactly **who said what, where, why, on what evidence, against whom, with what degree of certainty, and with what downstream uses**.

Once you have that, a Pāṭala answer isn't “the AI says...”.

It becomes:

```text
The primary source says A.

Scholar X interprets A as B.
Scholar Y objects because C.
Scholar Z proposes D.

The disagreement turns on crux E.

Here is the evidence for each.

Pāṭala's current synthesis is F,
with confidence/review status G.
```

And the same graph object can generate the answer, essay, lesson, video, scholar credit and future research task without losing provenance.

That secondary-scholarship layer may be the thing that turns the existing Pāṭala source graph into a genuinely **living intellectual tradition**, rather than just an unusually good digital edition.

[1]: https://arxiv.org/abs/2206.01439?utm_source=chatgpt.com "Open Research Knowledge Graph:A System Walkthrough"
[2]: https://arxiv.org/abs/2507.13827?utm_source=chatgpt.com "Question-Answer Extraction from Scientific Articles Using Knowledge Graphs and Large Language Models"
[3]: https://developers.openalex.org/?utm_source=chatgpt.com "Overview - OpenAlex Developers"
[4]: https://github.com/LABA-SNU/SocraticKG?utm_source=chatgpt.com "GitHub - LABA-SNU/SocraticKG: SocraticKG: Knowledge Graph Construction via QA-Driven Fact Extraction · GitHub"
[5]: https://arxiv.org/abs/2109.10453?utm_source=chatgpt.com "Extracting Fine-Grained Knowledge Graphs of Scientific Claims: Dataset and Transformer-Based Results"
[6]: https://aclanthology.org/2021.sdp-1.7/?utm_source=chatgpt.com "Argument Mining for Scholarly Document Processing: Taking Stock and Looking Ahead - ACL Anthology"
[7]: https://arxiv.org/abs/1904.01608?utm_source=chatgpt.com "Structural Scaffolds for Citation Intent Classification in Scientific Publications"
[8]: https://developers.openalex.org/api-reference/authors?utm_source=chatgpt.com "Authors Overview - OpenAlex Developers"
[9]: https://www.copyright.gov/fair-use/more-info.html?utm_source=chatgpt.com "More Information on Fair Use | U.S. Copyright Office"
[10]: https://arxiv.org/abs/2006.01747?utm_source=chatgpt.com "Generate FAIR Literature Surveys with Scholarly Knowledge Graphs"
[11]: https://aclanthology.org/2022.wiesp-1.7/?utm_source=chatgpt.com "Full-Text Argumentation Mining on Scientific Publications - ACL Anthology"
