import pytest
from src.models import Transaction
from src.valuation import generate_synthetic_valuations
from datetime import datetime

def test_generate_synthetic_valuations():
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=600, currency="USD", payment_method="wire", country="USA", sender_id="a", receiver_id="b", invoice_id="inv1")
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now(), amount=100, currency="USD", payment_method="cc", country="USA", sender_id="c", receiver_id="d", invoice_id="inv2")

    valuations = generate_synthetic_valuations([tx1, tx2])

    assert len(valuations) == 1
    assert valuations[0]['transaction_id'] == 'tx1'
    assert tx1.valuation_id is not None
    assert tx2.valuation_id is None
