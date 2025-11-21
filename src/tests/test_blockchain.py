import pytest
from src.blockchain import Blockchain
from src.models import Transaction, AssetValuation
from datetime import datetime

@pytest.fixture
def blockchain():
    return Blockchain()

def test_genesis_block(blockchain: Blockchain):
    assert len(blockchain.chain) == 1
    genesis_block = blockchain.get_last_block()
    assert genesis_block.index == 0
    assert genesis_block.previous_hash == "0"

def test_add_block(blockchain: Blockchain):
    tx = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=100, currency="USD", payment_method="cc", country="USA", sender_id="a", receiver_id="b", invoice_id="inv1")
    blockchain.add_block([tx], [])
    assert len(blockchain.chain) == 2
    last_block = blockchain.get_last_block()
    assert last_block.index == 1
    assert last_block.transactions[0].transaction_id == "tx1"

def test_chain_verification(blockchain: Blockchain):
    tx1 = Transaction(transaction_id="tx1", timestamp=datetime.now(), amount=100, currency="USD", payment_method="cc", country="USA", sender_id="a", receiver_id="b", invoice_id="inv1")
    blockchain.add_block([tx1], [])
    tx2 = Transaction(transaction_id="tx2", timestamp=datetime.now(), amount=200, currency="USD", payment_method="cc", country="USA", sender_id="c", receiver_id="d", invoice_id="inv2")
    blockchain.add_block([tx2], [])

    assert blockchain.verify_chain() is True

    # Tamper with the chain
    blockchain.chain[1].transactions[0].amount = 999
    assert blockchain.verify_chain() is False
