from iolaus.models import VerifierClass
from iolaus.verifiers import CallableVerifier, JsonSchemaVerifier


def test_json_schema_verifier():
    v=JsonSchemaVerifier("schema", {"type":"object","required":["ok"],"properties":{"ok":{"type":"boolean"}}})
    assert v.verify(arguments={}, output={"ok":True}).passed
    assert not v.verify(arguments={}, output={"x":1}).passed


def test_callable_verifier_keeps_class():
    v=CallableVerifier("readback", VerifierClass.DETERMINISTIC_READBACK, lambda a,o:(o.get("ok") is True,"checked",{}))
    ev=v.verify(arguments={},output={"ok":True})
    assert ev.passed
    assert ev.verifier_class is VerifierClass.DETERMINISTIC_READBACK
