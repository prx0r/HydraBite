#!/usr/bin/env python3
"""End-to-end demo of Pāṭala Research CI.

Run: python3 demo.py

This demonstrates the full TRACK → CLAIM → VERIFY → OBLIGE flow
against the live OpenAIRE V3 API.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from patala_research_ci.openaire import OpenAIREClient, SourceStatus
from patala_research_ci.tracked import TrackedAnalysis, TrackedClaim, Dependency, DepKind
from patala_research_ci.diff import compute_diff
from patala_research_ci.impact import analyze_impact
from patala_research_ci.obligations import generate_obligations
from patala_research_ci.ledger import ResearchCILedger

DATA_DIR = Path(__file__).parent / "demo_data"


def banner(text):
    print(f"\n{'═' * 60}")
    print(f"  {text}")
    print(f"{'═' * 60}\n")


def step(num, text):
    print(f"\n{'─' * 40}")
    print(f"  STEP {num}: {text}")
    print(f"{'─' * 40}\n")


def main():
    banner("PāṭALA RESEARCH CI — End-to-End Demo")

    # Clean slate
    import shutil
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True)

    ledger = ResearchCILedger(DATA_DIR / "ledger")
    client = OpenAIREClient()

    # ─── STEP 1: Track an analysis ───
    step(1, "TRACK — Register analysis against OpenAIRE")

    print("Querying OpenAIRE V3 for open access software...")
    records, status = client.fetch_records(
        entity_type="research-products",
        search="open access software",
        page_size=10,
        max_pages=1,
    )

    if status != SourceStatus.OK:
        print(f"Source unavailable: {status}")
        return

    print(f"Found {len(records)} records")

    analysis = TrackedAnalysis.create(
        analysis_id="demo:open-software",
        title="Open research software in AI",
        query={"search": "open access software", "entity": "research-products"},
        records=records,
        version="11.3.0",
    )

    # Save
    analysis_file = DATA_DIR / "analyses" / "demo:open-software.json"
    analysis_file.parent.mkdir(parents=True, exist_ok=True)
    with open(analysis_file, "w") as f:
        json.dump(analysis.to_dict(), f, indent=2, default=str)

    ledger.record_track("demo:open-software", analysis.query,
                        len(records), analysis.snapshot_digest)

    print(f"  TrackedAnalysis: demo:open-software")
    print(f"  Records: {len(records)}")
    print(f"  Digest: {analysis.snapshot_digest[:40]}...")

    # ─── STEP 2: Add claims ───
    step(2, "CLAIM — Attach conclusions with dependencies")

    claims = [
        TrackedClaim(
            claim_id="claim:software-exists",
            text="Open access software products exist in OpenAIRE",
            dependencies=[
                Dependency(kind=DepKind.ENTITY, ref=records[0].id if records else "none"),
            ],
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        ),
        TrackedClaim(
            claim_id="claim:dataset-linkage",
            text="Most sampled outputs have linked datasets",
            dependencies=[
                Dependency(kind=DepKind.RELATION,
                           source=records[0].id if records else "none",
                           predicate="IsRelatedTo",
                           target="doi:10.1234/dataset"),
            ],
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        ),
        TrackedClaim(
            claim_id="claim:unrelated",
            text="This claim has no dependencies on tracked records",
            dependencies=[],
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        ),
    ]

    claims_dir = DATA_DIR / "claims"
    claims_dir.mkdir(parents=True, exist_ok=True)
    for claim in claims:
        with open(claims_dir / f"{claim.claim_id}.json", "w") as f:
            json.dump(claim.to_dict(), f, indent=2)
        analysis.claims.append(claim.claim_id)
        print(f"  {claim.claim_id}: {claim.text}")
        print(f"    deps: {len(claim.dependencies)}")

    with open(analysis_file, "w") as f:
        json.dump(analysis.to_dict(), f, indent=2, default=str)

    # ─── STEP 3: Verify against current state ───
    step(3, "VERIFY — Detect changes and assess impact")

    print("Fetching current OpenAIRE state...")
    new_records, status = client.fetch_records(
        entity_type="research-products",
        search="open access software",
        page_size=10,
        max_pages=1,
    )
    client.close()

    if status != SourceStatus.OK:
        print(f"Source unavailable: {status}")
        return

    old_snapshot = analysis.snapshots.get(list(analysis.snapshots.keys())[-1], {})
    new_snapshot = {r.id: r.to_dict() for r in new_records}

    diff = compute_diff(old_snapshot, new_snapshot)

    print(f"  Old records:     {len(old_snapshot)}")
    print(f"  New records:     {len(new_snapshot)}")
    print(f"  Added:           {diff.added_count}")
    print(f"  Removed:         {diff.removed_count}")
    print(f"  Changed:         {diff.changed_count}")
    print(f"  Material changes: {diff.material_change_count}")

    # ─── STEP 4: Impact analysis ───
    step(4, "IMPACT — Match changes against claim dependencies")

    report = analyze_impact("demo:open-software", claims, diff)

    for impact in report.claim_impacts:
        icon = {"SOURCE_CHANGED": "⚠️", "RECOMPUTE": "🔄",
                "HUMAN_REVIEW": "👤"}.get(impact.status.value, "?")
        print(f"  {impact.claim_id:25s} {icon} {impact.status.value}")
        print(f"  {'':25s}   {impact.reason}")

    print(f"\n  Summary:")
    print(f"    Unaffected: {len(report.unaffected)}")
    print(f"    Recompute:  {len(report.recompute)}")
    print(f"    Human:      {len(report.human_review)}")

    # ─── STEP 5: Proof obligations ───
    step(5, "OBLIGE — Emit proof obligations with frozen acceptance")

    obligations = generate_obligations(report)

    if obligations:
        for po in obligations:
            print(f"  {po.id}  →  {po.claim_id}")
            print(f"    Reason:   {po.reason}")
            print(f"    Action:   {po.recommended_action}")
            print(f"    Class:    {po.resolution_class}")
            print(f"    Acceptance hash: {po.acceptance_hash[:32]}...")
            print(f"    Frozen criteria: {json.dumps(po.acceptance, indent=6)}")
            print()

        # Save obligations
        obs_dir = DATA_DIR / "obligations"
        obs_dir.mkdir(parents=True, exist_ok=True)
        for po in obligations:
            with open(obs_dir / f"{po.id}.json", "w") as f:
                json.dump(po.to_dict(), f, indent=2)
            ledger.record_obligation(po.to_dict())
    else:
        print("  No obligations — all claims CURRENT")

    # ─── STEP 6: Event log ───
    step(6, "LEDGER — Append-only event history")

    events = ledger.log(limit=10)
    for ev in events:
        print(f"  {ev.get('recorded_at', '?')}  {ev.get('event_type', '?')}")

    # ─── Done ───
    banner("DEMO COMPLETE")
    print("Files written to: demo_data/")
    print("  analyses/demo:open-software.json")
    print("  claims/*.json")
    print("  obligations/*.json")
    print("  ledger/events.jsonl")
    print()
    print("Next steps:")
    print("  python3 -m patala_research_ci.cli list")
    print("  python3 -m patala_research_ci.cli log")


if __name__ == "__main__":
    main()
