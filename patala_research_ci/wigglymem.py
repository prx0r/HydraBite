"""WigglyMem — Wiggly evidence graph on HydraDB storage backend."""
import json
from pathlib import Path
from typing import Any
from .hydradb import HydraDB

class WigglyMem:
    """Adapter: Wiggly evidence graph → HydraDB knowledge storage."""

    def __init__(self, hydradb: HydraDB):
        self.hydradb = hydradb

    def export_corpus(self, corpus_path: str) -> dict:
        """Export Wiggly corpus to HydraDB as knowledge sources."""
        corpus_dir = Path(corpus_path)
        exported = 0
        errors = 0

        for jsonl_file in corpus_dir.glob("*.jsonl"):
            try:
                with open(jsonl_file) as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line)
                            self._export_record(record)
                            exported += 1
            except Exception as e:
                errors += 1

        return {"exported": exported, "errors": errors}

    def _export_record(self, record: dict):
        """Export a single Wiggly record to HydraDB."""
        text = self._record_to_text(record)
        title = record.get("preferred_title", record.get("id", "unknown"))
        self.hydradb.ingest(text=text, title=title, is_markdown=True)

    def _record_to_text(self, record: dict) -> str:
        """Convert Wiggly record to ingestible text."""
        parts = [f"# {record.get('preferred_title', 'Unknown')}"]
        parts.append(f"\nID: {record.get('id', '')}")
        if record.get("preferred_author"):
            parts.append(f"Author: {record['preferred_author']}")
        if record.get("tradition"):
            parts.append(f"Tradition: {record['tradition']}")
        for ext_id in record.get("external_ids", []):
            parts.append(f"External ID: {ext_id.get('source', '')}:{ext_id.get('identifier', '')}")
        for assertion in record.get("assertions", []):
            parts.append(f"Assertion: {assertion.get('predicate', '')} {assertion.get('object', '')}")
        return "\n".join(parts)

    def query_evidence(self, question: str, mode: str = "fast") -> dict:
        """Query HydraDB for evidence supporting a question."""
        return self.hydradb.query(question, mode=mode)

    def verify_claim(self, claim_text: str, expected_evidence: list[str]) -> dict:
        """Verify a claim against HydraDB-stored evidence."""
        result = self.hydradb.query(f"Evidence for: {claim_text}", mode="thinking")
        answer = result.get("result", {}).get("content", "")

        supported = any(e.lower() in answer.lower() for e in expected_evidence)
        return {
            "claim": claim_text,
            "supported": supported,
            "evidence_found": answer[:200] if answer else "",
            "expected": expected_evidence,
        }
