# Six-criterion adversarial scorecard

The hackathon scores every criterion 1–5 and can reject an entry for a single weak axis. This document therefore treats the rubric as a test suite rather than marketing.

| Criterion | Current evidence | Honest target | Main residual risk |
|---|---|---:|---|
| **1. AI MCP connector using OpenAIRE Graph** | Dual-MCP architecture; trace capture/redaction/digest/binding; companion MCP; 4 trace tests; official connector named as required AI discovery plane. **Live Alien trace captured** (11 tool calls, 5 OpenAIRE IDs, synthetic=false). Alien's existing features (auto-updates, audit trails, redaction) are explicitly acknowledged; Pāṭala's contribution is the downstream dependency/impact layer Alien does not have. | **5/5** | Live trace captured. |
| **2. Usefulness/value** | Persistent analyses/agents learn *which* conclusions require attention; target users and anti-alert-fatigue behavior are explicit. | **5/5** | Need judges to see the difference between a diff and downstream impact immediately. |
| **3. Originality** | Prior-art docs explicitly reject generic KG versioning and AI peer review; contribution is dependency impact + proof obligation + receipt. | **5/5** | Do not claim invention of provenance/versioning/MCP. |
| **4. Responsible data** | OpenAIRE attribution, CC-BY policy, no full-text redistribution, secret redaction, source health, synthetic/live labels, human-review state. | **5/5** | Never imply source absence means falsity. |
| **5. Reproducibility/interoperability** | Offline fixtures, schemas, tests, build certificate, tamper checks, CFF/CodeMeta/Zenodo, RO-Crate export, stable V3 default. | **5/5** | Public repo must match the final ZIP. |
| **6. Clarity** | One loop; 30-second README; exact form; 2-minute script; alternative ideas archived rather than foregrounded. | **5/5** | Avoid overloading demo with Sanskrit/QDW/marketplace history. |

## Shortlist blockers

Before submit, all must be true:

- [x] One real **Alien/OpenAIRE MCP** tool call has been captured/imported and the redacted trace is public.
- [ ] `SUBMISSION_FINAL.md` is public and no longer says MCP is “not applicable.”
- [ ] GitHub root has README, LICENSE, `CITATION.cff`, rights/FAIR docs and visible commit history.
- [ ] `python scripts/verify_release.py` reports `PROVEN` on the final commit/tree.
- [ ] Every public URL opens in a private browser window.
- [ ] OpenAIRE is attributed anywhere its metadata is redistributed.
- [ ] No API keys/tokens are in traces, docs, fixtures or history.
- [ ] The submitter personally confirms publication/voting/right-to-submit checkboxes.
