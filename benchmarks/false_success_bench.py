"""Failure-oriented acceptance benchmark for Iolaus.

This is intentionally NOT a broad performance benchmark. It measures the one
failure mode Iolaus claims to solve: a tool reports success while its declared
world-state postcondition is false.

Requires a live HydraDB OSS node and writes every case as real graph state.
"""
from __future__ import annotations

import argparse
import json
import secrets
from pathlib import Path

from iolaus import IolausEngine, HydraClient, ReceiptSigner
from demo.scenario import CREATE_CUSTOMER, crm_verifier
from demo.workspace import DemoWorkspace

CASES = (
    "honest", "silent_failure", "wrong_record", "honest",
    "silent_failure", "honest", "wrong_record", "honest",
    "silent_failure", "wrong_record", "honest", "silent_failure",
)


def run(output: Path, workspace_path: Path) -> dict:
    hydra=HydraClient.from_env()
    proof=hydra.native_probe()
    if not proof.passed:
        raise RuntimeError(f"HydraDB native probe failed: {proof}")
    ws=DemoWorkspace(workspace_path); ws.reset()
    engine=IolausEngine(hydra,ReceiptSigner.generate("iolaus.benchmark"))
    verifier=crm_verifier(ws)
    records=[]
    naive_false_commits=0
    hb_false_commits=0
    semantic_failures=0
    true_positive=0
    expected_success=0

    for idx,mode in enumerate(CASES):
        email=f"bench-{idx}-{secrets.token_hex(3)}@example.test"
        args={"email":email,"name":"Bench","mode":mode}
        pending=engine.execute(CREATE_CUSTOMER,ws.create_customer_tool,args,executor="benchmark")
        # Naive baseline commits whenever the tool's own response says success.
        naive_commit=bool((pending.output or {}).get("success"))
        world_ok=ws.customer(email) is not None
        if naive_commit and not world_ok: naive_false_commits += 1
        if not world_ok: semantic_failures += 1
        else: expected_success += 1

        result=engine.verify(CREATE_CUSTOMER,pending,verifier)
        hb_commit=result.status.value=="VERIFIED"
        if hb_commit and not world_ok: hb_false_commits += 1
        if hb_commit and world_ok: true_positive += 1
        claim=f"crm.customer:{email}:exists"
        graph_claim=hydra.has_verified_claim(claim)
        if graph_claim != hb_commit:
            raise AssertionError((mode,email,hb_commit,graph_claim))
        records.append({
            "case":idx,"mode":mode,"tool_reported_success":naive_commit,"world_postcondition":world_ok,
            "naive_commit":naive_commit,"iolaus_status":result.status.value,"iolaus_commit":hb_commit,
            "graph_claim":graph_claim,"receipt_hash":result.receipt.receipt_hash if result.receipt else None,
        })

    metrics={
        "schema":"iolaus.false-success-bench.v1",
        "cases":len(CASES),
        "semantic_failures":semantic_failures,
        "expected_successes":expected_success,
        "naive_false_success_commits":naive_false_commits,
        "iolaus_false_success_commits":hb_false_commits,
        "naive_false_success_commit_rate":naive_false_commits/max(1,semantic_failures),
        "iolaus_false_success_commit_rate":hb_false_commits/max(1,semantic_failures),
        "iolaus_true_positive_rate":true_positive/max(1,expected_success),
        "hydra_native_proof":proof.model_dump(mode="json"),
        "records":records,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(metrics,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if hb_false_commits != 0 or true_positive != expected_success:
        raise AssertionError(metrics)
    return metrics


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--out",default="validation/false-success-bench.json"); p.add_argument("--workspace",default=".runs/bench-workspace.sqlite")
    a=p.parse_args(); m=run(Path(a.out),Path(a.workspace)); print(json.dumps(m,indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
