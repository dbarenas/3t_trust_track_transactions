import pytest
from src.blockchain import Blockchain
from src.models import Transaction
from src.rules import AMLRules
from src.reputation import ReputationSystem
from datetime import datetime, timedelta

@pytest.fixture
def reputation_system():
    return ReputationSystem()

@pytest.fixture
def blockchain_with_tx(reputation_system):
    bc = Blockchain(reputation_system)
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=600, currency="USD", payment_method="wire", country="USA", sender_id="a", receiver_id="b", invoice_id="inv1")
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now(), amount=100, currency="USD", payment_method="cc", country="USA", sender_id="c", receiver_id="blacklisted", invoice_id="inv2")
    bc.add_block([tx1, tx2], [])
    return bc

def test_high_value_transaction_rule(blockchain_with_tx: Blockchain, reputation_system: ReputationSystem):
    rules = AMLRules(blockchain_with_tx, set(), reputation_system)
    alerts = rules.check_all_transactions()
    assert "tx1" in alerts
    assert "High-value transaction tx1 is missing valuation." in alerts["tx1"]

def test_blacklisted_entity_rule(blockchain_with_tx: Blockchain, reputation_system: ReputationSystem):
    rules = AMLRules(blockchain_with_tx, {"blacklisted"}, reputation_system)
    alerts = rules.check_all_transactions()
    assert "tx2" in alerts
    assert "Transaction tx2 involves a blacklisted entity." in alerts["tx2"]

def test_low_reputation_rule(reputation_system: ReputationSystem):
    reputation_system.update_reputation("low_rep_sender", 0.1, "Suspicious activity")
    bc = Blockchain(reputation_system)
    tx = Transaction(transaction_id="tx_low_rep", timestamp=datetime.now(), amount=100, currency="USD", payment_method="wire", country="USA", sender_id="low_rep_sender", receiver_id="normal_user", invoice_id="inv_low_rep")
    bc.add_block([tx], [])

    rules = AMLRules(bc, set(), reputation_system)
    alerts = rules.check_all_transactions()

    assert "tx_low_rep" in alerts
    assert "Sender low_rep_sender has a low reputation score." in alerts["tx_low_rep"]

def test_transaction_splitting_rule(reputation_system: ReputationSystem):
    bc = Blockchain(reputation_system)
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=400, currency="USD", payment_method="wire", country="USA", sender_id="H", receiver_id="I", invoice_id="inv5")
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now() + timedelta(hours=1), amount=400, currency="USD", payment_method="wire", country="USA", sender_id="H", receiver_id="I", invoice_id="inv6")
    bc.add_block([tx1, tx2], [])
    rules = AMLRules(bc, set(), reputation_system)
    alerts = rules.check_all_transactions()
    assert "splitting" in alerts
    assert "Transaction splitting detected between H and I." in alerts["splitting"]

def test_circular_flow_rule(reputation_system: ReputationSystem):
    bc = Blockchain(reputation_system)
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=100, currency="USD", payment_method="wire", country="USA", sender_id="A", receiver_id="B", invoice_id="inv1")
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now(), amount=100, currency="USD", payment_method="wire", country="USA", sender_id="B", receiver_id="C", invoice_id="inv2")
    tx3 = Transaction(transaction_id="tx3", timestamp=datetime.now(), amount=100, currency="USD", payment_method="wire", country="USA", sender_id="C", receiver_id="A", invoice_id="inv3")
    bc.add_block([tx1, tx2, tx3], [])
    rules = AMLRules(bc, set(), reputation_system)
    alerts = rules.check_all_transactions()
    assert "circular_flows" in alerts
    assert "Circular flow detected: A -> B -> C -> A" in alerts["circular_flows"]
