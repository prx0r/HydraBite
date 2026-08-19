"""Iolaus hydra — HydraDB OSS HTTP/OpenCypher adapter."""
from __future__ import annotations
import hashlib
import httpx
from typing import Any


def stable_vertex_id(domain: str, identifier: str) -> int:
    """Deterministic positive 63-bit vertex ID."""
    h = hashlib.sha256(f"{domain}:{identifier}".encode()).hexdigest()
    return int(h[:16], 16) & 0x7FFFFFFFFFFFFFFF


class HydraClient:
    """Thin client for HydraDB OSS graph-node HTTP/OpenCypher."""

    def __init__(self, base_url: str = "http://127.0.0.1:7474", auth_token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.c = httpx.Client(timeout=30)

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.auth_token:
            h["Authorization"] = f"Bearer {self.auth_token}"
        return h

    def query(self, cypher: str, params: dict | None = None) -> list[dict]:
        """Execute a Cypher read query."""
        payload = {"statements": [{"text": cypher, "parameters": params or {}}]}
        r = self.c.post(
            f"{self.base_url}/db/data/transaction",
            json=payload,
            headers=self._headers(),
        )
        r.raise_for_status()
        return r.json().get("results", [{}])[0].get("data", [])

    def upsert_vertex(self, label: str, vertex_id: int, properties: dict) -> int:
        """Create or update a vertex."""
        cypher = f"MERGE (n:{label} {{vertex_id: $vid}}) SET n += $props RETURN n.vertex_id"
        self.query(cypher, {"vid": vertex_id, "props": properties})
        return vertex_id

    def merge_edge(self, src: int, rel_type: str, dst: int, **props) -> int:
        """Create or update an edge."""
        cypher = f"""
        MATCH (a {{vertex_id: $src}}), (b {{vertex_id: $dst}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        RETURN id(r)
        """
        result = self.query(cypher, {"src": src, "dst": dst, "props": props})
        return result[0].get("id", 0) if result else 0

    def has_verified_claim(self, claim_key: str) -> bool:
        """Check if a verified claim exists."""
        cypher = """
        MATCH (c:HBClaim {claim_key: $key})
              -[:VERIFIED_BY]->(r:HBReceipt {verdict: 'PASS'})
        RETURN c.claim_key LIMIT 1
        """
        result = self.query(cypher, {"key": claim_key})
        return len(result) > 0

    def ready(self) -> bool:
        """Check if HydraDB is ready."""
        try:
            r = self.c.get(f"{self.base_url}/readyz", headers=self._headers())
            return r.status_code == 200
        except Exception:
            return False
