"""Alternative: canonical record normalization.

From neverbrokeagain-research-ci — simpler field extraction.
"""

import json
import hashlib


def normalize(record: dict) -> dict:
    """Extract stable fields for comparison."""
    return {
        "id": record.get("id", ""),
        "doi": record.get("doi", ""),
        "title": (record.get("mainTitle") or record.get("title", "")).strip(),
        "type": record.get("type", ""),
        "year": record.get("publicationYear"),
        "access": (record.get("bestAccessRight") or {}).get("label", ""),
        "citations": record.get("citationCount", 0),
        "is_peer_reviewed": record.get("isPeerReviewed"),
        "projects": sorted([p.get("id", "") for p in record.get("relProjects", [])]),
        "organizations": sorted([o.get("id", "") for o in record.get("relOrganizations", [])]),
        "relations": sorted([
            f"{r.get('source','')}:{r.get('predicate','')}:{r.get('target','')}"
            for r in record.get("relations", [])
        ]),
    }


def digest(records: list[dict]) -> str:
    """JCS-style deterministic digest."""
    canonical = json.dumps(
        sorted(records, key=lambda r: r.get("id", "")),
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    )
    return hashlib.sha512(canonical.encode()).hexdigest()
