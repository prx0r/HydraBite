"""Alternative: CLI with rich tables.

From neverbrokeagain-research-ci — pretty output, fewer commands.
"""

import json
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from .openaire import OpenAIRE
from .normalize import normalize, digest
from .tracked import TrackedAnalysis, TrackedClaim
from .diff import diff
from .impact import impact
from .obligations import generate
from .ledger import Ledger


console = Console() if HAS_RICH else None
LEDGER = Ledger()


def _print(msg, style=None):
    if console:
        console.print(msg, style=style)
    else:
        print(msg)


def _table(title, columns, rows):
    if not HAS_RICH:
        print(f"\n{title}")
        for row in rows:
            print(f"  {row}")
        return
    t = Table(title=title)
    for col in columns:
        t.add_column(col)
    for row in rows:
        t.add_row(*[str(c) for c in row])
    console.print(t)


def cmd_track(args):
    api = OpenAIRE()
    query = dict(x.split("=", 1) for x in args.query.split("&") if "=" in x)
    results = api.products(**query)
    records = [normalize(r) for r in results]
    snap_digest = digest(records)
    analysis = TrackedAnalysis(
        analysis_id=f"analysis:{args.name}", title=args.name,
        source_version="11.3.0", query=query,
        result_ids=[r["id"] for r in records],
        snapshot_digest=snap_digest,
    )
    state = {"type": "track", "analysis": _ser(analysis), "record_count": len(records)}
    LEDGER.append(state)
    _print(f"[green]Tracked[/green] {len(records)} records, digest {snap_digest[:16]}...")


def cmd_verify(args):
    entries = LEDGER.entries()
    track_events = [e for e in entries if e["type"] == "track"]
    if not track_events:
        _print("[red]No tracked analyses found.[/red]")
        return

    latest = track_events[-1]
    a = latest["analysis"]
    _print(f"[cyan]Verifying {a['analysis_id']}[/cyan]")

    api = OpenAIRE()
    results = api.products(**a.get("query", {}))
    new_records = [normalize(r) for r in results]
    old_digest = a["snapshot_digest"]
    new_digest = digest(new_records)

    if old_digest == new_digest:
        _print("[green]No changes detected.[/green]")
        return

    d = diff(a.get("result_ids", []), [r["id"] for r in new_records])
    claims = [TrackedClaim(**c) for c in a.get("claims", [])]
    imp = impact(d, claims)
    obs = generate(imp)

    _table("Semantic Diff", ["Type", "Count"], [
        ["Added", str(len(d.added))],
        ["Removed", str(len(d.removed))],
        ["Changed", str(len(d.changed))],
        ["Unchanged", str(d.unchanged)],
    ])

    for cid in imp["recompute"]:
        _print(f"  [yellow]RECOMPUTE[/yellow] {cid}")
    for cid in imp["unaffected"]:
        _print(f"  [green]CURRENT[/green] {cid}")
    for ob in obs:
        _print(f"  [red]PROOF OBLIGATION[/red] {ob.claim_id}: {ob.reason}")

    LEDGER.append({
        "type": "verify", "analysis_id": a["analysis_id"],
        "diff_summary": {"added": len(d.added), "removed": len(d.removed)},
        "impact": imp, "obligations": len(obs),
    })


def cmd_log(args):
    for e in LEDGER.entries():
        t = e.get("timestamp", "?")
        tp = e["type"]
        if tp == "track":
            _print(f"  {t} TRACK {e['analysis']['analysis_id']} ({e['record_count']} records)")
        elif tp == "verify":
            _print(f"  {t} VERIFY {e['analysis_id']} ({e['diff_summary']})")


def _ser(obj):
    from dataclasses import asdict
    return asdict(obj)


def main():
    import argparse
    p = argparse.ArgumentParser(prog="patala", description="Research CI for OpenAIRE")
    sub = p.add_subparsers(dest="command")

    t = sub.add_parser("track")
    t.add_argument("--name", required=True)
    t.add_argument("--query", required=True)

    v = sub.add_parser("verify")
    v.add_argument("analysis")

    l = sub.add_parser("log")

    args = p.parse_args()
    if args.command == "track":
        cmd_track(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "log":
        cmd_log(args)
    else:
        p.print_help()
