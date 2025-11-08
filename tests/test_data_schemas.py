import pytest
from pydantic import ValidationError
from routes.data.schemas import AlertCreate, AlertUpdate, AlertRead
import datetime as dt

def test_datacreate_valid():
    obj = AlertCreate(
        contract="NQ1!",
        trade_type="buy",
        quantity=1,
        price=100.0,
        secret_key="abc",
        timestamp=dt.datetime.now()
    )
    assert obj.contract == "NQ1!"
    assert obj.trade_type == "buy"
    assert obj.quantity == 1
    assert obj.price == 100.0

@pytest.mark.parametrize("field,value", [
    ("quantity", 0),
    ("price", 0.0),
])
def test_datacreate_invalid(field, value):
    kwargs = dict(contract="NQ1!", trade_type="buy", quantity=1, price=100.0)
    kwargs[field] = value
    with pytest.raises(ValidationError):
        AlertCreate(**kwargs)

def test_dataupdate_partial():
    obj = AlertUpdate(quantity=5)
    assert obj.quantity == 5
    assert obj.contract is None


def test_dataread_serialization():
    obj = AlertRead(
        id="507f1f77bcf86cd799439011",
        contract="NQ1!",
        trade_type="sell",
        quantity=2,
        price=200.0,
        secret_key=None,
        timestamp=None
    )
    data = obj.model_dump()
    assert data["id"] == "507f1f77bcf86cd799439011"
    assert data["contract"] == "NQ1!"

