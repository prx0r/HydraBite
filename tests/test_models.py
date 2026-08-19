import pytest
from hydrabite.models import Contract


def test_contract_renders_claim_templates_and_hash_is_stable():
    c = Contract(
        contract_id="x",
        description="x",
        requires_claim_templates=("user:{email}:exists",),
        produces_claim_templates=("sent:{email}",),
        allowed_verifier_ids=("v",),
    )
    args={"email":"a@example.test"}
    assert c.render_requires(args)==("user:a@example.test:exists",)
    assert c.render_produces(args)==("sent:a@example.test",)
    assert c.contract_hash == c.contract_hash


def test_contract_requires_verifier():
    with pytest.raises(ValueError):
        Contract(contract_id="x", description="x", allowed_verifier_ids=())
