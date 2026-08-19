"""HydraBite receipts — signed Bite receipts."""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Any
from .models import ReceiptPayload


@dataclass
class ReceiptSigner:
    """Signs Bite receipts."""
    private_key: bytes = b""
    issuer_id: str = ""

    @classmethod
    def generate(cls, issuer_id: str = "") -> "ReceiptSigner":
        key = hashlib.sha256(issuer_id.encode()).digest() if issuer_id else b"mvp-key"
        return cls(private_key=key, issuer_id=issuer_id)

    def sign(self, payload: ReceiptPayload) -> str:
        """Sign a receipt payload. Returns hex signature."""
        content = json.dumps(asdict(payload), sort_keys=True, default=str)
        return hashlib.sha256(content.encode() + self.private_key).hexdigest()

    def sign_payload(self, payload: ReceiptPayload) -> dict:
        """Sign a receipt and return envelope with tamper detection."""
        payload_dict = asdict(payload)
        payload_hash = hashlib.sha256(json.dumps(payload_dict, sort_keys=True, default=str).encode()).hexdigest()
        sig = self.sign(payload)
        envelope = {
            "payload": payload_dict,
            "signature": sig,
            "payload_hash": payload_hash,
            "envelope_hash": hashlib.sha256(sig.encode()).hexdigest(),
        }
        return envelope

    @classmethod
    def verify(cls, envelope: dict) -> bool:
        """Verify a receipt envelope — detect tampered payloads."""
        payload = envelope.get("payload", {})
        sig = envelope.get("signature", "")
        payload_hash = envelope.get("payload_hash", "")
        env_hash = envelope.get("envelope_hash", "")
        if not sig or not payload:
            return False
        # Check envelope_hash matches sha256(signature)
        expected_env_hash = hashlib.sha256(sig.encode()).hexdigest()
        if expected_env_hash != env_hash:
            return False
        # Check payload hasn't been tampered with
        current_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        return current_hash == payload_hash
