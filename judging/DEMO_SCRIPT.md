# Exact live demo script — ~2 minutes

## Before recording

```bash
./scripts/start_hydradb.sh
pip install -e '.[demo]'
uvicorn demo.app:app --port 8080
```

Also keep a terminal ready with:

```bash
iolaus prove-hydra
```

## Script

### 0:00–0:20 — frame
“Hydra already gives agents function routing. Iolaus solves one smaller problem: **when can an action result become trusted state?** This customer tool is deliberately adversarial.”

### 0:20–0:40 — lying tool
Click **Run lying tool**.

Say: “The tool returns `success=true`, but I configured it to write nothing. Notice Iolaus does not mark success; it says `SUCCEEDED_UNVERIFIED`.”

### 0:40–0:55 — verify
Click **Verify readback**.

Say: “A separate deterministic verifier reads the CRM. The record isn't there. FAIL receipt. No trusted claim.”

### 0:55–1:10 — prove consequence
Click **Try downstream action**.

Say: “Welcome email requires a verified customer. It is blocked before the email tool can run. This is the whole product.”

### 1:10–1:30 — good path
Click **Run honest + verify**.

Say: “Same contract, same verifier. This time readback finds the exact record. Iolaus signs the receipt and creates the verified claim.”

Click **Run verified downstream**.

Say: “Now the next action is allowed, and it must earn its own receipt.”

### 1:30–1:50 — prove Hydra
Terminal:

```bash
iolaus prove-hydra
```

Point at:
- `readyz: true`
- `metrics_marker: true`
- `roundtrip: true`
- `native_path: true`

Say: “The certificate requires Hydra's native `algo.MSpaths`. A Python mock doesn't count.”

### 1:50–2:05 — finish
“Hydra's routing benchmarks tell us whether the system chose and completed a plan. Iolaus adds the missing metric: **did false success become trusted state?** In our acceptance harness, that must stay at zero.”

Final screen:

> **No receipt → no trusted transition.**
