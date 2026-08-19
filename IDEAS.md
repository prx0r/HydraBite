# Ideas Board — OpenAIRE AI Hackathon

## Constraints
- Deadline: **Aug 20, 2026** (23:59 CET)
- 12-week hackathon, "Powered by Alien Intelligence"
- Must use OpenAIRE Graph data
- Categories: Explore & Narrate, Build, Analyse, Wildcard

---

## Idea 1: Open Science Citation Network Explorer (Explore & Narrate)
**What:** Interactive visualization of citation networks + dataset links via ScholeXplorer
**Stack:** Python (httpx), D3.js or pyvis, OpenAIRE V4 API + ScholeXplorer API
**Why:** Nobody has a good visual explorer of dataset→publication citation chains
**MVP:**
1. Pick a dataset from OpenAIRE
2. Fetch all linked publications via ScholeXplorer
3. Fetch those publications' citations
4. Render as interactive graph

---

## Idea 2: Open Access Compliance Checker (Build)
**What:** Given a list of DOIs, check if each meets EU Open Access mandates (Plan S, Horizon Europe)
**Stack:** Python CLI + API wrapper
**Why:** Funders need this, researchers need this, nobody has a clean tool
**MVP:**
1. Accept DOIs or ORCID
2. Fetch research products from V4 API
3. Check: is it OA? Which route (gold/hybrid/green)? Embargo period?
4. Output compliance report (JSON + human-readable)

---

## Idea 3: Research Product Deduplication (Analyse)
**What:** Find duplicate records across sources (Crossref vs PubMed vs DataCite)
**Stack:** Python, fuzzy matching, OpenAIRE dedup data
**Why:** OpenAIRE already deduplicates but the logic is opaque — we can surface it
**MVP:**
1. Query same DOI from multiple sources
2. Compare metadata fields
3. Show where conflicts/duplicates exist
4. Confidence score for "same entity"

---

## Idea 4: Funding Landscape Map (Wildcard)
**What:** Map EU funding → projects → publications → impact
**Stack:** Python, OpenAIRE V4 (projects + research-products), mapping viz
**Why:** Taxpayers want to know what their money produced
**MVP:**
1. Query Horizon 2020 projects
2. Fetch linked publications
3. Show: funding amount → papers → citations → OA status
4. Aggregate by country/institution/topic

---

## Idea 5: SDG Research Tracker (Wildcard)
**What:** How much research is being done on UN Sustainable Development Goals?
**Stack:** Python, V4 API with SDG filters
**Why:** Policy makers need this, nobody tracks it well
**MVP:**
1. Filter by SDG subjects (e.g. "SDG 13: Climate Action")
2. Aggregate by year, country, institution
3. Show trends and gaps
4. Compare across SDGs

---

## Next Steps
- [ ] Pick one idea
- [ ] Prototype the API calls
- [ ] Build the minimum viable thing
- [ ] Write the submission narrative
