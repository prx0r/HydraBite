import json
from iolaus.models import ReceiptPayload, VerifierClass
from iolaus.receipts import ReceiptSigner


def payload():
    return ReceiptPayload(
        receipt_id="bite_test",
        invocation_id="inv_test",
        contract_id="contract.test",
        contract_hash="a" * 64,
        input_hash="b" * 64,
        output_hash="c" * 64,
        evidence_hash="d" * 64,
        verifier_id="verifier.test",
        verifier_class=VerifierClass.DETERMINISTIC_TEST,
        verdict="PASS",
        issued_at="2026-08-19T00:00:00+00:00",
        issuer_id="issuer.test",
    )


def test_signed_receipt_roundtrip():
    signer = ReceiptSigner.generate("issuer.test")
    receipt = signer.sign_payload(payload())
    assert ReceiptSigner.verify(receipt)


def test_tamper_breaks_signature_or_envelope_hash():
    signer = ReceiptSigner.generate("issuer.test")
    receipt = signer.sign_payload(payload())
    # Tamper with the output_hash in the payload
    tampered = json.loads(json.dumps(receipt))
    tampered["payload"]["output_hash"] = "e" * 64
    assert not ReceiptSigner.verify(tampered)
