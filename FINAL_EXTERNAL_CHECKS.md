# External checks before clicking Submit

The code artifact is self-contained; these are the only account/publication tasks that cannot be completed inside the build environment.

## MCP trace (completed)

A real Alien/OpenAIRE MCP interaction is included at `artifacts/alien_mcp_trace.live.json` (11 tool calls, 5 OpenAIRE IDs, synthetic:false). A synthetic example remains at `artifacts/alien_mcp_trace.example.json` for offline testing.

## Public-link check

Open every link in section 4 of `SUBMISSION_FINAL.md` in a private/incognito browser. Do not add a video/demo/Zenodo URL until it is genuinely public.

## Optional high-value additions

- Record `VIDEO_SCRIPT.md` as a <3 minute walkthrough and add the public URL.
- Create a Zenodo release using `.zenodo.json`, then add the DOI.
- Tag the exact GitHub commit used for submission.
