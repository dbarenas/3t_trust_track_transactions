import pytest
from src.blockchain import Blockchain
from src.models import Transaction
from src.reputation import ReputationSystem
from datetime import datetime

@pytest.fixture
def blockchain_for_reputation():
    bc = Blockchain()
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=100, currency="USD", payment_method="cc", country="USA", sender_id="userA", receiver_id="userB", invoice_id="inv1")
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now(), amount=200, currency="USD", payment_method="wire", country="USA", sender_id="userA", receiver_id="blacklisted", invoice_id="inv2")
    bc.add_block([tx1, tx2], [])
    return bc

def test_reputation_score_calculation(blockchain_for_reputation: Blockchain):
    blacklisted_entities = {"blacklisted"}
    reputation_system = ReputationSystem(blockchain_for_reputation, blacklisted_entities)
    scores = reputation_system.calculate_reputation()

    assert scores["userA"] == 2
    assert scores["userB"] == 1
    assert scores["blacklisted"] == 101
