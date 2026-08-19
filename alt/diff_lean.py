"""Alternative: semantic diff — works on raw record lists.

From neverbrokeagain-research-ci — simpler, fewer abstractions.
"""

from dataclasses import dataclass, field


MATERIALITY = {
    "orcid": "identity", "doi": "identity", "openaire_id": "identity",
    "title": "metadata", "abstract": "metadata", "publication_date": "metadata",
    "access": "availability", "oa_status": "availability",
    "citation": "relation", "projects": "relation", "organizations": "relation",
}


@dataclass
class SemanticDiff:
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    changed: list[dict] = field(default_factory=list)
    unchanged: int = 0


def classify(field: str) -> str:
    for key, mat in MATERIALITY.items():
        if key in field.lower():
            return mat
    return "metadata"


def diff(old: list[dict], new: list[dict]) -> SemanticDiff:
    """Compute diff between two lists of records."""
    old_m = {r["id"]: r for r in old}
    new_m = {r["id"]: r for r in new}
    added = [r["id"] for r in new if r["id"] not in old_m]
    removed = [r["id"] for r in old if r["id"] not in new_m]
    changed = []
    for rid in old_m:
        if rid not in new_m:
            continue
        for f in set(list(old_m[rid].keys()) + list(new_m[rid].keys())):
            if old_m[rid].get(f) != new_m[rid].get(f):
                changed.append({
                    "id": rid, "field": f,
                    "old": old_m[rid].get(f), "new": new_m[rid].get(f),
                    "materiality": classify(f),
                })
    return SemanticDiff(
        added=added, removed=removed, changed=changed,
        unchanged=len(old_m) - len(removed),
    )
