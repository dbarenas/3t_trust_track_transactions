import pytest
from src.reputation import ReputationSystem, DEFAULT_REPUTATION_SCORE
from src.models import Transaction
from datetime import datetime

@pytest.fixture
def reputation_system():
    return ReputationSystem()

def test_get_reputation_default(reputation_system: ReputationSystem):
    assert reputation_system.get_reputation("new_entity") == DEFAULT_REPUTATION_SCORE

def test_update_and_get_reputation(reputation_system: ReputationSystem):
    reputation_system.update_reputation("entity1", 0.9, "Good transaction history")
    assert reputation_system.get_reputation("entity1") == 0.9

def test_update_reputation_invalid_score(reputation_system: ReputationSystem):
    with pytest.raises(ValueError):
        reputation_system.update_reputation("entity2", 1.1, "Invalid score")
    with pytest.raises(ValueError):
        reputation_system.update_reputation("entity3", -0.1, "Invalid score")

def test_get_all_reputations(reputation_system: ReputationSystem):
    reputation_system.update_reputation("entity1", 0.9, "Good transaction history")
    reputation_system.update_reputation("entity2", 0.2, "Suspicious activity")
    scores = reputation_system.get_all_reputations()
    assert scores == {"entity1": 0.9, "entity2": 0.2}

def test_update_reputations_from_alerts(reputation_system: ReputationSystem):
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=100, currency="USD", payment_method="cc", country="USA", sender_id="sender1", receiver_id="receiver1", invoice_id="inv1")
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now(), amount=200, currency="USD", payment_method="cc", country="USA", sender_id="sender2", receiver_id="receiver2", invoice_id="inv2")
    transactions = [tx1, tx2]
    aml_alerts = {"tx2": ["Suspicious activity detected"]}

    reputation_system.update_reputations_from_alerts(transactions, aml_alerts)

    # sender1 and receiver1 should have increased reputation
    assert reputation_system.get_reputation("sender1") > DEFAULT_REPUTATION_SCORE
    assert reputation_system.get_reputation("receiver1") > DEFAULT_REPUTATION_SCORE

    # sender2 and receiver2 should have decreased reputation
    assert reputation_system.get_reputation("sender2") < DEFAULT_REPUTATION_SCORE
    assert reputation_system.get_reputation("receiver2") < DEFAULT_REPUTATION_SCORE
