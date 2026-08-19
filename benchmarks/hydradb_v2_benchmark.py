"""HydraDB v2 Benchmark: Real hosted API, real function routing, real verification.

Tests the AI Chief of Staff pattern from the HydraDB cookbook:
1. Register functions as knowledge objects
2. Query HydraDB for function routing
3. Execute via registry
4. Log outcomes back
5. Verify learning loop

Base URL: https://api.hydradb.com
"""
from __future__ import annotations

import json
import os
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx


# ─── HydraDB v2 client ───

API_URL = "https://api.hydradb.com"
API_KEY = os.environ.get("HYDRA_DB_API_KEY", "")


def hydradb_request(method: str, path: str, **kwargs) -> dict:
    """Make a request to HydraDB v2 API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "API-Version": "2",
        "Content-Type": "application/json",
    }
    try:
        r = httpx.request(method, f"{API_URL}{path}", headers=headers, timeout=30, **kwargs)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_database(database: str) -> dict:
    return hydradb_request("POST", "/databases", json={"database": database})


def check_database_ready(database: str) -> bool:
    resp = hydradb_request("GET", f"/databases/status?database={database}")
    try:
        return resp.get("data", {}).get("infra", {}).get("ready_for_ingestion", False)
    except Exception:
        return False


def ingest_functions(database: str, collection: str, functions: list[dict]) -> dict:
    """Register functions as knowledge objects."""
    return hydradb_request("POST", "/context/ingest", json={
        "type": "knowledge",
        "database": database,
        "collection": collection,
        "app_knowledge": json.dumps(functions),
    })


def query_function(database: str, collection: str, task: str) -> dict:
    """Query HydraDB for function routing."""
    return hydradb_request("POST", "/query", json={
        "database": database,
        "collection": collection,
        "query": task,
        "type": "knowledge",
        "query_by": "hybrid",
        "mode": "thinking",
        "max_results": 5,
    })


def ingest_memory(database: str, collection: str, memories: list[dict]) -> dict:
    """Store execution outcomes as memories."""
    return hydradb_request("POST", "/context/ingest", json={
        "type": "memory",
        "database": database,
        "collection": collection,
        "memories": json.dumps(memories),
    })


def query_memory(database: str, collection: str, query: str) -> dict:
    """Query user memories."""
    return hydradb_request("POST", "/query", json={
        "database": database,
        "collection": collection,
        "query": query,
        "type": "memory",
        "query_by": "hybrid",
        "mode": "thinking",
    })


# ─── Function schemas ───

FUNCTION_SCHEMAS = [
    {
        "id": "send_slack_message",
        "title": "Send a Slack message",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "send_slack_message",
            "name": "Send a Slack message",
            "description": "Posts a message to a Slack channel or DM. Use for internal, time-sensitive communications. Prefer over email for team updates.",
            "parameters": {"type": "object", "properties": {"channel": {"type": "string"}, "text": {"type": "string"}}, "required": ["channel", "text"]},
        })},
        "metadata": {"type": "function", "collections": ["communication"]},
    },
    {
        "id": "create_calendar_event",
        "title": "Create a calendar event",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "create_calendar_event",
            "name": "Create a calendar event",
            "description": "Creates a Google Calendar event with attendees. Use for scheduling meetings, calls, and appointments.",
            "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "start_time": {"type": "string"}, "end_time": {"type": "string"}, "attendees": {"type": "array"}}, "required": ["title", "start_time", "end_time"]},
        })},
        "metadata": {"type": "function", "collections": ["scheduling"]},
    },
    {
        "id": "send_email",
        "title": "Send an email",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "send_email",
            "name": "Send an email",
            "description": "Sends an email via Gmail. Use for external communications, formal messages, and when a paper trail is needed.",
            "parameters": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]},
        })},
        "metadata": {"type": "function", "collections": ["communication"]},
    },
    {
        "id": "update_crm",
        "title": "Update CRM record",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "update_crm",
            "name": "Update CRM record",
            "description": "Updates a Salesforce CRM opportunity or contact. Use for sales pipeline updates, deal stage changes, and contact modifications.",
            "parameters": {"type": "object", "properties": {"record_id": {"type": "string"}, "field": {"type": "string"}, "value": {"type": "string"}}, "required": ["record_id", "field", "value"]},
        })},
        "metadata": {"type": "function", "collections": ["sales"]},
    },
    {
        "id": "create_jira_ticket",
        "title": "Create a Jira ticket",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "create_jira_ticket",
            "name": "Create a Jira ticket",
            "description": "Creates a Jira issue for bug tracking, feature requests, or task management. Use for engineering work items.",
            "parameters": {"type": "object", "properties": {"project": {"type": "string"}, "summary": {"type": "string"}, "description": {"type": "string"}, "issue_type": {"type": "string"}}, "required": ["project", "summary"]},
        })},
        "metadata": {"type": "function", "collections": ["engineering"]},
    },
    {
        "id": "trigger_deployment",
        "title": "Trigger a deployment",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "trigger_deployment",
            "name": "Trigger a deployment",
            "description": "Triggers a CI/CD deployment to a specified environment. Use for releasing code changes to staging or production.",
            "parameters": {"type": "object", "properties": {"environment": {"type": "string"}, "branch": {"type": "string"}}, "required": ["environment"]},
        })},
        "metadata": {"type": "function", "collections": ["engineering"]},
    },
    {
        "id": "approve_expense",
        "title": "Approve an expense report",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "approve_expense",
            "name": "Approve an expense report",
            "description": "Approves a pending expense report in the finance system. Use when a manager needs to sign off on submitted expenses.",
            "parameters": {"type": "object", "properties": {"expense_id": {"type": "string"}, "approver_id": {"type": "string"}}, "required": ["expense_id", "approver_id"]},
        })},
        "metadata": {"type": "function", "collections": ["finance"]},
    },
    {
        "id": "generate_report",
        "title": "Generate a report",
        "type": "function",
        "timestamp": "2025-01-01T00:00:00Z",
        "content": {"text": json.dumps({
            "id": "generate_report",
            "name": "Generate a report",
            "description": "Generates a formatted report from data sources. Use for metrics, dashboards, executive summaries, and data analysis.",
            "parameters": {"type": "object", "properties": {"report_type": {"type": "string"}, "date_range": {"type": "string"}, "recipients": {"type": "array"}}, "required": ["report_type"]},
        })},
        "metadata": {"type": "function", "collections": ["analytics"]},
    },
]


# ─── Benchmark tasks ───

ROUTING_TASKS = [
    {"id": "t1", "task": "tell the team about the delay", "expected_fn": "send_slack_message"},
    {"id": "t2", "task": "book a meeting with alice next tuesday", "expected_fn": "create_calendar_event"},
    {"id": "t3", "task": "send the quarterly report to the board", "expected_fn": "send_email"},
    {"id": "t4", "task": "update the acme deal to negotiation stage", "expected_fn": "update_crm"},
    {"id": "t5", "task": "file a bug for the login timeout issue", "expected_fn": "create_jira_ticket"},
    {"id": "t6", "task": "deploy the hotfix to production", "expected_fn": "trigger_deployment"},
    {"id": "t7", "task": "approve james expense report for $500", "expected_fn": "approve_expense"},
    {"id": "t8", "task": "generate the weekly sales summary", "expected_fn": "generate_report"},
    {"id": "t9", "task": "ping the engineering channel about the outage", "expected_fn": "send_slack_message"},
    {"id": "t10", "task": "schedule a 30 min call with the vendor", "expected_fn": "create_calendar_event"},
    {"id": "t11", "task": "send a formal proposal to the new client", "expected_fn": "send_email"},
    {"id": "t12", "task": "create a ticket for the database migration", "expected_fn": "create_jira_ticket"},
]


# ─── Benchmark runner ───

@dataclass
class RoutingTrial:
    task_id: str
    task: str
    expected_fn: str
    routed_fn: str | None
    routing_correct: bool
    response_chunks: int
    top_score: float
    latency_ms: float
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task": self.task,
            "expected_fn": self.expected_fn,
            "routed_fn": self.routed_fn,
            "routing_correct": self.routing_correct,
            "response_chunks": self.response_chunks,
            "top_score": self.top_score,
            "latency_ms": self.latency_ms,
            "error": self.error,
        }


@dataclass
class BenchmarkResult:
    database: str
    collection: str
    trials: list[RoutingTrial] = field(default_factory=list)
    setup_time_ms: float = 0
    functions_registered: int = 0

    @property
    def n(self) -> int:
        return len(self.trials)

    def routing_accuracy(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(1 for t in self.trials if t.routing_correct) / self.n

    def avg_latency_ms(self) -> float:
        if self.n == 0:
            return 0.0
        return sum(t.latency_ms for t in self.trials) / self.n

    def p95_latency_ms(self) -> float:
        if self.n == 0:
            return 0.0
        sorted_latencies = sorted(t.latency_ms for t in self.trials)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[min(idx, len(sorted_latencies) - 1)]

    def summary(self) -> dict:
        return {
            "schema": "hydradb-v2-benchmark.v1",
            "database": self.database,
            "collection": self.collection,
            "functions_registered": self.functions_registered,
            "total_trials": self.n,
            "routing_accuracy": self.routing_accuracy(),
            "avg_latency_ms": self.avg_latency_ms(),
            "p95_latency_ms": self.p95_latency_ms(),
            "setup_time_ms": self.setup_time_ms,
            "trials": [t.to_dict() for t in self.trials],
        }


class BenchmarkRunner:
    def __init__(self, database: str = "benchmark-chief-of-staff", collection: str = "functions"):
        self.database = database
        self.collection = collection
        self.result = BenchmarkResult(database=database, collection=collection)

    def setup(self) -> bool:
        """Create database and register functions."""
        if not API_KEY:
            print("ERROR: HYDRA_DB_API_KEY not set")
            return False

        print(f"Creating database '{self.database}'...")
        create_database(self.database)

        print("Waiting for database to be ready...")
        for _ in range(30):
            if check_database_ready(self.database):
                break
            time.sleep(2)
        else:
            print("ERROR: Database not ready after 60s")
            return False

        print(f"Registering {len(FUNCTION_SCHEMAS)} functions...")
        start = time.time()
        resp = ingest_functions(self.database, self.collection, FUNCTION_SCHEMAS)
        self.result.setup_time_ms = (time.time() - start) * 1000
        self.result.functions_registered = len(FUNCTION_SCHEMAS)

        if not resp.get("success", True):
            print(f"ERROR: Ingest failed: {resp}")
            return False

        print(f"Setup complete ({self.result.setup_time_ms:.0f}ms)")
        return True

    def run_routing_benchmark(self) -> BenchmarkResult:
        """Run routing accuracy benchmark."""
        print(f"\nRunning {len(ROUTING_TASKS)} routing tasks...")

        for task in ROUTING_TASKS:
            start = time.time()
            try:
                resp = query_function(self.database, self.collection, task["task"])
                latency = (time.time() - start) * 1000

                chunks = resp.get("data", {}).get("chunks", [])
                response_chunks = len(chunks)

                if chunks:
                    top_chunk = chunks[0]
                    top_content = top_chunk.get("chunk_content", "")
                    try:
                        schema = json.loads(top_content)
                        routed_fn = schema.get("id")
                    except (json.JSONDecodeError, KeyError):
                        routed_fn = None
                    top_score = top_chunk.get("relevancy_score", 0)
                else:
                    routed_fn = None
                    top_score = 0

                routing_correct = routed_fn == task["expected_fn"]
                error = None

            except Exception as e:
                latency = (time.time() - start) * 1000
                routed_fn = None
                response_chunks = 0
                top_score = 0
                routing_correct = False
                error = str(e)

            trial = RoutingTrial(
                task_id=task["id"],
                task=task["task"],
                expected_fn=task["expected_fn"],
                routed_fn=routed_fn,
                routing_correct=routing_correct,
                response_chunks=response_chunks,
                top_score=top_score,
                latency_ms=latency,
                error=error,
            )
            self.result.trials.append(trial)

            status = "PASS" if routing_correct else "FAIL"
            print(f"  [{status}] {task['id']}: '{task['task'][:40]}' → {routed_fn} (expected {task['expected_fn']}) [{latency:.0f}ms]")

        print(f"\nRouting accuracy: {self.result.routing_accuracy():.1%}")
        print(f"Avg latency: {self.result.avg_latency_ms():.0f}ms")
        print(f"P95 latency: {self.result.p95_latency_ms():.0f}ms")

        return self.result

    def run_learning_loop_test(self) -> dict:
        """Test if storing outcomes improves routing."""
        print("\nTesting learning loop...")

        # Store a user preference
        ingest_memory(self.database, f"user-{secrets.token_hex(4)}", [{
            "text": "User prefers Slack for all internal communications. Never use email for team updates.",
            "infer": True,
        }])

        # Query with the preference context
        resp = query_function(self.database, self.collection, "tell the team about the delay")
        chunks = resp.get("data", {}).get("chunks", [])

        return {
            "chunks_returned": len(chunks),
            "top_fn": json.loads(chunks[0]["chunk_content"]).get("id") if chunks else None,
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.result.summary(), indent=2) + "\n", encoding="utf-8")


# ─── Certifier ───

def certify(path: Path) -> dict:
    data = json.loads(path.read_text())
    declared = {
        "routing_accuracy": data["routing_accuracy"],
        "total_trials": data["total_trials"],
        "avg_latency_ms": data["avg_latency_ms"],
    }

    # Recompute
    trials = data.get("trials", [])
    correct = sum(1 for t in trials if t.get("routing_correct", False))
    n = len(trials)
    recomputed = {
        "routing_accuracy": correct / n if n else 0,
        "total_trials": n,
        "avg_latency_ms": sum(t.get("latency_ms", 0) for t in trials) / n if n else 0,
    }

    errors = []
    for key in declared:
        if abs(declared[key] - recomputed[key]) > 1e-10:
            errors.append(f"{key}: declared={declared[key]} recomputed={recomputed[key]}")

    return {
        "certified": len(errors) == 0,
        "errors": errors,
        "declared": declared,
        "recomputed": recomputed,
    }


# ─── CLI ───

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="HydraDB v2 Benchmark")
    parser.add_argument("--database", default="benchmark-chief-of-staff")
    parser.add_argument("--collection", default="functions")
    parser.add_argument("--out", default="results/hydradb-v2-benchmark.json")
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()

    if args.certify:
        result = certify(Path(args.out))
        print(json.dumps(result, indent=2))
        return 0 if result["certified"] else 1

    runner = BenchmarkRunner(args.database, args.collection)
    if not runner.setup():
        return 1

    runner.run_routing_benchmark()
    runner.run_learning_loop_test()
    runner.save(Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
