import pytest
from src.main import generate_good_raw_transactions, generate_suspicious_raw_transactions
from src.ingestion import ingest_data
from src.blockchain import Blockchain
from src.rules import AMLRules
from src.reputation import ReputationSystem

def test_full_pipeline():
    # 1. Setup
    blockchain = Blockchain()
    blacklisted_entities = {'blacklisted_user'}

    # 2. Ingest data
    raw_data = generate_good_raw_transactions() + generate_suspicious_raw_transactions()
    transactions, valuations, _, _ = ingest_data(raw_data)

    # 3. Add to blockchain
    blockchain.add_block(transactions, valuations)

    # 4. Run AML and Reputation
    aml_rules = AMLRules(blockchain, blacklisted_entities)
    aml_alerts = aml_rules.check_all_transactions()

    reputation_system = ReputationSystem(blockchain, blacklisted_entities)
    reputation_scores = reputation_system.calculate_reputation()

    # 5. Assertions
    assert len(blockchain.chain) == 2
    assert len(aml_alerts) > 0
    assert reputation_scores['blacklisted_user'] > 100
