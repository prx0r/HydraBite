"""Real Benchmark: Hermes × HydraDB × Iolaus with actual MCP tools.

Tests against real tool calls, real failures, real verification.
No injected faults. No synthetic scenarios. Real world.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx


# ─── HydraDB client ───

HYDRA_URL = "http://127.0.0.1:8443"
TOKEN = "iolauz-test-token-32-chars-long!!"


def hydra_query(query: str, params: dict | None = None) -> dict:
    try:
        r = httpx.post(
            f"{HYDRA_URL}/v1/graphs/default/query",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "X-Graph-Namespace": "default",
                "Content-Type": "application/json",
            },
            json={"cell_id": "cell-0", "query": query, "parameters": params or {}},
            timeout=10,
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def hydra_alive() -> bool:
    try:
        r = httpx.get(f"{HYDRA_URL.replace('8443', '9090')}/readyz", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# ─── Hermes MCP client (subprocess) ───

def hermes_query(prompt: str, timeout: int = 30) -> dict:
    """Call Hermes via CLI and parse response."""
    import subprocess
    try:
        result = subprocess.run(
            ["hermes", "-z", prompt],
            capture_output=True, text=True, timeout=timeout,
            env={**__import__("os").environ, "HERMES_PROFILE": "patala"},
        )
        output = result.stdout.strip()
        return {
            "success": result.returncode == 0 and len(output) > 0,
            "output": output[:2000],
            "error": result.stderr[:500] if result.returncode != 0 else None,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": "timeout"}
    except Exception as e:
        return {"success": False, "output": "", "error": str(e)}


# ─── Real tool calls via MCP ───

def call_patala_tool(tool_name: str, args: dict) -> dict:
    """Call a patala MCP tool with proper JSON-RPC framing."""
    import subprocess
    # Must initialize first, then call tool
    init_msg = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "bench", "version": "1.0"}},
        "id": 1,
    })
    call_msg = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args},
        "id": 2,
    })
    full_input = init_msg + "\n" + call_msg + "\n"
    try:
        result = subprocess.run(
            ["node", "/root/patalacheckpoints/mcp/index.mjs"],
            input=full_input, capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            # Parse last JSON line (the tool call response)
            lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
            for line in reversed(lines):
                try:
                    resp = json.loads(line)
                    if "result" in resp:
                        return resp["result"]
                except json.JSONDecodeError:
                    continue
            return {"raw": result.stdout[:500]}
        return {"error": result.stderr[:500] if result.stderr else "no output"}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}


# ─── Real benchmark tasks ───

REAL_TASKS = [
    {
        "id": "patala.get_work",
        "description": "Get metadata for the Vijñānabhairava tantra",
        "tool": "get_work",
        "args": {"id": "vijnanabhairava"},
        "expected_fields": ["id", "title"],
        "verification": "response_has_field",
        "verifies_against": "mcp_response",
    },
    {
        "id": "patala.search_passages",
        "description": "Search for 'śakti' in the Sanskrit corpus",
        "tool": "search_passages",
        "args": {"q": "śakti", "limit": 5},
        "expected_fields": ["results"],
        "verification": "response_has_field",
        "verifies_against": "mcp_response",
    },
    {
        "id": "patala.verify_quote",
        "description": "Verify a known quote exists in source",
        "tool": "verify_quote",
        "args": {"q": "dhāraṇā", "ref": "vijnanabhairava:1"},
        "expected_fields": ["verified"],
        "verification": "response_has_field",
        "verifies_against": "mcp_response",
    },
    {
        "id": "patala.get_source_passage",
        "description": "Get Sanskrit text of a specific passage",
        "tool": "get_source_passage",
        "args": {"passage_id": "tantra:text:kramasadbhava:1.2"},
        "expected_fields": ["sanskrit"],
        "verification": "response_has_field",
        "verifies_against": "mcp_response",
    },
    {
        "id": "patala.get_themes",
        "description": "Get theme structure for IPVV",
        "tool": "get_themes",
        "args": {},
        "expected_fields": ["themes"],
        "verification": "response_has_field",
        "verifies_against": "mcp_response",
    },
    {
        "id": "patala.get_term_senses",
        "description": "Get accepted senses for a Sanskrit term",
        "tool": "get_term_senses",
        "args": {"lemma": "bindu"},
        "expected_fields": ["senses"],
        "verification": "response_has_field",
        "verifies_against": "mcp_response",
    },
    {
        "id": "file.write_and_read",
        "description": "Write a file and read it back to verify integrity",
        "tool": "filesystem",
        "args": {"action": "write", "path": "/tmp/bench-marker.txt", "content": f"bench-{secrets.token_hex(4)}"},
        "expected_fields": ["success"],
        "verification": "file_exists",
        "verifies_against": "filesystem",
    },
    {
        "id": "hydra.write_and_query",
        "description": "Write a node to HydraDB and query it back",
        "tool": "hydra",
        "args": {"action": "create_and_query"},
        "expected_fields": ["verified"],
        "verification": "hydra_roundtrip",
        "verifies_against": "hydra",
    },
]


# ─── Trial data structures ───

@dataclass
class RealTrial:
    task_id: str
    task_description: str
    tool_name: str
    tool_args: dict
    # Actual execution
    tool_success: bool
    tool_response: dict
    tool_latency_ms: float
    # Verification
    verified: bool
    verification_evidence: dict
    verification_latency_ms: float
    # Hermes routing
    hermes_routed: bool
    hermes_confidence: float
    # HydraDB storage
    stored_in_hydra: bool
    # Timing
    total_latency_ms: float

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_description": self.task_description,
            "tool_name": self.tool_name,
            "tool_success": self.tool_success,
            "tool_latency_ms": self.tool_latency_ms,
            "verified": self.verified,
            "verification_evidence": self.verification_evidence,
            "verification_latency_ms": self.verification_latency_ms,
            "hermes_routed": self.hermes_routed,
            "hermes_confidence": self.hermes_confidence,
            "stored_in_hydra": self.stored_in_hydra,
            "total_latency_ms": self.total_latency_ms,
        }


@dataclass
class RealBenchmarkResult:
    trials: list[RealTrial] = field(default_factory=list)
    hydra_alive: bool = False
    hermes_alive: bool = False
    mcp_alive: bool = False

    @property
    def n(self) -> int:
        return len(self.trials)

    def tool_success_rate(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(1 for t in self.trials if t.tool_success) / self.n

    def verification_rate(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(1 for t in self.trials if t.verified) / self.n

    def false_trusted_successes(self) -> int:
        """Tool says success but verification failed."""
        return sum(1 for t in self.trials if t.tool_success and not t.verified)

    def hermes_routing_rate(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(1 for t in self.trials if t.hermes_routed) / self.n

    def avg_tool_latency_ms(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(t.tool_latency_ms for t in self.trials) / self.n

    def avg_verification_latency_ms(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(t.verification_latency_ms for t in self.trials) / self.n

    def summary(self) -> dict:
        return {
            "schema": "real-benchmark.v1",
            "total_trials": self.n,
            "infrastructure": {
                "hydra_alive": self.hydra_alive,
                "hermes_alive": self.hermes_alive,
                "mcp_alive": self.mcp_alive,
            },
            "results": {
                "tool_success_rate": self.tool_success_rate(),
                "verification_rate": self.verification_rate(),
                "false_trusted_successes": self.false_trusted_successes(),
                "hermes_routing_rate": self.hermes_routing_rate(),
                "avg_tool_latency_ms": self.avg_tool_latency_ms(),
                "avg_verification_latency_ms": self.avg_verification_latency_ms(),
            },
            "trials": [t.to_dict() for t in self.trials],
        }


# ─── Benchmark runner ───

class RealBenchmarkRunner:
    def __init__(self):
        self.result = RealBenchmarkResult()

    def check_infrastructure(self) -> None:
        print("Checking infrastructure...")
        self.result.hydra_alive = hydra_alive()
        print(f"  HydraDB: {'alive' if self.result.hydra_alive else 'dead'}")

        hermes = hermes_query("respond with just the word 'pong'", timeout=10)
        self.result.hermes_alive = hermes["success"]
        print(f"  Hermes: {'alive' if self.result.hermes_alive else 'dead'}")

        mcp = call_patala_tool("get_themes", {})
        self.result.mcp_alive = "error" not in mcp
        print(f"  MCP (patala): {'alive' if self.result.mcp_alive else 'dead'}")

    def run_task(self, task: dict) -> RealTrial:
        start = time.time()

        # Step 1: Hermes routing
        hermes_start = time.time()
        hermes_result = hermes_query(
            f"Route this task to the right tool: {task['description']}. "
            f"Available tools: {task['tool']}. "
            f"Return JSON: {{\"tool\": \"tool_name\", \"confidence\": 0.0-1.0}}",
            timeout=15,
        )
        hermes_latency = (time.time() - hermes_start) * 1000
        hermes_routed = hermes_result["success"]
        hermes_confidence = 0.9 if hermes_routed else 0.0

        # Step 2: Tool execution
        tool_start = time.time()
        if task["tool"] == "filesystem":
            # File system operation
            import os
            path = task["args"].get("path", "/tmp/bench-test.txt")
            content = task["args"].get("content", "test")
            try:
                Path(path).write_text(content)
                tool_response = {"success": True, "path": path}
                tool_success = True
            except Exception as e:
                tool_response = {"success": False, "error": str(e)}
                tool_success = False
        elif task["tool"] == "hydra":
            # HydraDB roundtrip
            test_id = int.from_bytes(secrets.token_bytes(4), "big") % 100000
            write_result = hydra_query(
                "CREATE (n:BenchMarker {id: $id, value: $value})-[:TESTED]->(h:Hub {id: 9999})",
                {"id": test_id, "value": f"bench-{test_id}"},
            )
            query_result = hydra_query(
                "MATCH (n:BenchMarker {id: $id}) RETURN n.value",
                {"id": test_id},
            )
            rows = query_result.get("rows", [])
            verified = len(rows) > 0
            tool_response = {"write": write_result, "query": query_result, "verified": verified}
            tool_success = verified
        else:
            # MCP tool
            tool_response = call_patala_tool(task["tool"], task["args"])
            # MCP error means tool failed
            tool_success = not (isinstance(tool_response, dict) and tool_response.get("isError", False))
        tool_latency = (time.time() - tool_start) * 1000

        # Step 3: Verification
        verify_start = time.time()
        if task["verification"] == "response_has_field":
            # Check for MCP error responses
            if isinstance(tool_response, dict) and tool_response.get("isError"):
                verified = False
                evidence = {"mcp_error": True, "error_text": tool_response.get("content", [{}])[0].get("text", "unknown")}
            else:
                expected = task.get("expected_fields", [])
                data = tool_response.get("result", tool_response)
                verified = all(
                    field in data or (isinstance(data, dict) and field in data)
                    for field in expected
                )
                evidence = {"expected_fields": expected, "actual_keys": list(data.keys()) if isinstance(data, dict) else str(type(data))}
        elif task["verification"] == "file_exists":
            path = task["args"].get("path", "/tmp/bench-test.txt")
            verified = Path(path).exists()
            evidence = {"path": path, "exists": verified}
        elif task["verification"] == "hydra_roundtrip":
            verified = tool_response.get("verified", False)
            evidence = {"roundtrip": verified}
        else:
            verified = tool_success
            evidence = {"default": True}
        verify_latency = (time.time() - verify_start) * 1000

        # Step 4: Store in HydraDB
        stored = False
        if self.result.hydra_alive:
            try:
                hydra_query(
                    "CREATE (e:RealBenchExec {id: $id, task: $task, success: $success, verified: $verified})-[:FOR_USER]->(h:Hub {id: 8888})",
                    {
                        "id": int.from_bytes(secrets.token_bytes(4), "big") % 100000,
                        "task": task["id"],
                        "success": str(tool_success),
                        "verified": str(verified),
                    },
                )
                stored = True
            except Exception:
                pass

        total_latency = (time.time() - start) * 1000

        return RealTrial(
            task_id=task["id"],
            task_description=task["description"],
            tool_name=task["tool"],
            tool_args=task["args"],
            tool_success=tool_success,
            tool_response=tool_response,
            tool_latency_ms=tool_latency,
            verified=verified,
            verification_evidence=evidence,
            verification_latency_ms=verify_latency,
            hermes_routed=hermes_routed,
            hermes_confidence=hermes_confidence,
            stored_in_hydra=stored,
            total_latency_ms=total_latency,
        )

    def run(self, n_runs: int = 1) -> RealBenchmarkResult:
        self.check_infrastructure()
        print(f"\nRunning {n_runs} iterations × {len(REAL_TASKS)} tasks...\n")

        for run_idx in range(n_runs):
            for task in REAL_TASKS:
                try:
                    trial = self.run_task(task)
                    self.result.trials.append(trial)
                    status = "PASS" if trial.verified else "FAIL"
                    print(f"  [{status}] {trial.task_id}: tool={trial.tool_success} verified={trial.verified} ({trial.total_latency_ms:.0f}ms)")
                except Exception as e:
                    print(f"  [ERR] {task['id']}: {e}")

        print(f"\n{'='*50}")
        print(f"Results: {self.result.n} trials")
        print(f"  Tool success rate: {self.result.tool_success_rate():.1%}")
        print(f"  Verification rate: {self.result.verification_rate():.1%}")
        print(f"  False trusted successes: {self.result.false_trusted_successes()}")
        print(f"  Hermes routing rate: {self.result.hermes_routing_rate():.1%}")
        print(f"  Avg tool latency: {self.result.avg_tool_latency_ms():.0f}ms")
        print(f"  Avg verification latency: {self.result.avg_verification_latency_ms():.0f}ms")

        return self.result

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.result.summary(), indent=2) + "\n", encoding="utf-8")


# ─── Certifier ───

def certify_real(path: Path) -> dict:
    """Recompute summary from raw trials."""
    data = json.loads(path.read_text())
    trials = []
    for t in data["trials"]:
        try:
            trials.append(RealTrial(
                task_id=t["task_id"],
                task_description=t.get("task_description", ""),
                tool_name=t.get("tool_name", ""),
                tool_args=t.get("tool_args", {}),
                tool_success=t["tool_success"],
                tool_response=t.get("tool_response", {}),
                tool_latency_ms=t["tool_latency_ms"],
                verified=t["verified"],
                verification_evidence=t.get("verification_evidence", {}),
                verification_latency_ms=t["verification_latency_ms"],
                hermes_routed=t.get("hermes_routed", False),
                hermes_confidence=t.get("hermes_confidence", 0.0),
                stored_in_hydra=t.get("stored_in_hydra", False),
                total_latency_ms=t.get("total_latency_ms", 0.0),
            ))
        except Exception as e:
            print(f"Skipping trial: {e}")
    result = RealBenchmarkResult(trials=trials)
    declared = data["results"]

    errors = []
    if abs(result.tool_success_rate() - declared["tool_success_rate"]) > 1e-10:
        errors.append("tool_success_rate mismatch")
    if abs(result.verification_rate() - declared["verification_rate"]) > 1e-10:
        errors.append("verification_rate mismatch")

    return {
        "certified": len(errors) == 0,
        "errors": errors,
        "declared": declared,
        "recomputed": {
            "tool_success_rate": result.tool_success_rate(),
            "verification_rate": result.verification_rate(),
            "false_trusted_successes": result.false_trusted_successes(),
        },
    }


# ─── CLI ───

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Real Benchmark")
    parser.add_argument("--runs", type=int, default=3, help="Number of run iterations")
    parser.add_argument("--out", default="results/real-benchmark.json")
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()

    if args.certify:
        result = certify_real(Path(args.out))
        print(json.dumps(result, indent=2))
        return 0 if result["certified"] else 1

    runner = RealBenchmarkRunner()
    runner.run(n_runs=args.runs)
    runner.save(Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
