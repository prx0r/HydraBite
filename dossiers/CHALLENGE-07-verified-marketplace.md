# Challenge: Verified-Statement Marketplace

## The hard truth

**Building a marketplace in a hackathon is ambitious.** Marketplaces need: supply (verified statements), demand (consumers), pricing (Certification Weight), trust (reputation), and liquidity (enough activity). You can't build all five in a day.

The Certification Weight formula (`certification × consensus × load × time`) is elegant but **untested.** Does it actually correlate with trustworthiness? Has anyone validated it against ground truth?

## The real question

Is this a hackathon product or a startup thesis?

If startup thesis: brilliant, raise money on it.
If hackathon product: too many moving parts.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [ClaimeAI](https://github.com/BharathxD/ClaimeAI) | 104 | LangGraph fact-checking | LOW-MED — different mechanism |
| [FIRE](https://github.com/mbzuai-nlp/fire) | 21 | Iterative fact-checking agent | LOW |
| [vero](https://github.com/himanshu931588-cmd/vero) | 6 | AI claim verification | LOW |
| [Credify](https://github.com/ParthTiwari-Coder/Credify) | 1 | Multimodal fact-checking | LOW |
| Fact-checking platforms (Full Fact, PolitiFact) | — | Human fact-checking | ADJACENT — different mechanism |

## Reusable from competitors

- ClaimeAI's LangGraph architecture
- FIRE's iterative verification pattern
- ClaimBuster's claim detection API

## Verdict

**The flywheel is real but the timeline is wrong.** Position as: "Long-term economic layer. Certification Weight as transferable trust asset." Not for this hackathon. The formula is worth publishing as a research contribution even without the marketplace.
