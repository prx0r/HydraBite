# Public repository sync

The final ZIP is the verified release artifact. During final preparation the connected GitHub App could read `prx0r/hackathon1` but a contents write returned HTTP 403 (`Resource not accessible by integration`), so this package does **not** pretend that the hardened files were pushed.

Before submitting, sync this extracted release into the public `hackathon1` clone and commit it. The included helper preserves unrelated ideation/history files while replacing the judge-facing implementation and adding the FAIR/MCP material.

```bash
# From the extracted final release:
python scripts/sync_into_hackathon1.py /path/to/hackathon1

cd /path/to/hackathon1
python -m unittest discover -s tests -v
python scripts/verify_release.py

git add -A
git commit -m "Final OpenAIRE submission: Alien MCP + Research CI hardened release"
git push
```

Then verify in a private browser:

- repository root opens;
- `README.md` foregrounds the official Alien/OpenAIRE MCP;
- `SUBMISSION_FINAL.md` opens;
- `MCP_AGENT_WORKFLOW.md`, `DATA_AND_RIGHTS.md`, `FAIR.md`, and `CITATION.cff` open;
- the old statement `AI MCP connector: Not applicable` is gone.

## Strongly recommended criterion-1 action

Run one real query through the participant's official Alien/OpenAIRE MCP account, export a credential-redacted trace using `schemas/mcp-trace.schema.json`, set `synthetic: false`, import it into Pāṭala, and commit only the safe public trace. The bundled example remains explicitly synthetic.
