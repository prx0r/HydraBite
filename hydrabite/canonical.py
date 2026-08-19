"""HydraBite canonical — hashing and identity."""
from __future__ import annotations
import hashlib
import json
import math
import struct


def sha256_hex(data: Any) -> str:
    """SHA-256 hex digest. Accepts str, bytes, or dict (canonicalized)."""
    if isinstance(data, (str, bytes)):
        raw = data.encode("utf-8") if isinstance(data, str) else data
    elif isinstance(data, dict):
        raw = canonical_bytes(data)
    else:
        raw = str(data).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(obj: Any) -> bytes:
    """Canonical byte representation for hashing."""
    if isinstance(obj, str):
        return obj.encode("utf-8")
    if isinstance(obj, bytes):
        return obj
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise ValueError(f"non-finite value: {obj}")
        return str(obj).encode("utf-8")
    if isinstance(obj, dict):
        # Check for non-finite values
        for v in obj.values():
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                raise ValueError(f"non-finite value: {v}")
        return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return str(obj).encode("utf-8")


def stable_vertex_id(domain: str, identifier: str) -> int:
    """Deterministic positive 63-bit vertex ID from domain + identifier."""
    h = sha256_hex(f"{domain}:{identifier}")
    # Take first 16 hex chars (64 bits), mask to 63 bits
    val = int(h[:16], 16) & 0x7FFFFFFFFFFFFFFF
    return val
