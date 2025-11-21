from datetime import datetime
import uuid
from .ingestion import ingest_data
from .blockchain import Blockchain
from .rules import AMLRules
from .reputation import ReputationSystem
from .alerts import AlertSystem
from .valuation import generate_synthetic_valuations, generate_suspicious_valuations

def generate_good_raw_transactions():
    return [
        {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now(), 'amount': 100, 'currency': 'USD', 'payment_method': 'credit_card', 'country': 'USA', 'sender_id': 'user_A', 'receiver_id': 'user_B', 'invoice_id': 'inv_1', 'invoice_date': datetime.now(), 'invoice_concept': 'Consulting services', 'invoice_provider': 'Provider Inc.'},
        {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now(), 'amount': 600, 'currency': 'USD', 'payment_method': 'wire', 'country': 'USA', 'sender_id': 'user_C', 'receiver_id': 'user_D', 'invoice_id': 'inv_2', 'invoice_date': datetime.now(), 'invoice_concept': 'Software license', 'invoice_provider': 'Software Corp.'},
    ]

def generate_suspicious_raw_transactions():
    return [
        # High-value transaction without valuation
        {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now(), 'amount': 1000, 'currency': 'USD', 'payment_method': 'cash', 'country': 'USA', 'sender_id': 'user_E', 'receiver_id': 'user_F', 'invoice_id': 'inv_3', 'invoice_date': datetime.now(), 'invoice_concept': 'Unspecified goods', 'invoice_provider': 'Anonymous Provider'},
        # Transaction with blacklisted entity
        {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now(), 'amount': 20, 'currency': 'USD', 'payment_method': 'credit_card', 'country': 'USA', 'sender_id': 'user_G', 'receiver_id': 'blacklisted_user', 'invoice_id': 'inv_4', 'invoice_date': datetime.now(), 'invoice_concept': 'Donation', 'invoice_provider': 'N/A'},
        # Splitting of funds to avoid valuation
        {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now(), 'amount': 499, 'currency': 'USD', 'payment_method': 'wire', 'country': 'USA', 'sender_id': 'user_H', 'receiver_id': 'user_I', 'invoice_id': 'inv_5', 'invoice_date': datetime.now(), 'invoice_concept': 'Consulting', 'invoice_provider': 'Consultants LLC'},
        {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now(), 'amount': 499, 'currency': 'USD', 'payment_method': 'wire', 'country': 'USA', 'sender_id': 'user_H', 'receiver_id': 'user_I', 'invoice_id': 'inv_6', 'invoice_date': datetime.now(), 'invoice_concept': 'Consulting', 'invoice_provider': 'Consultants LLC'},
    ]

def main():
    # 1. Setup
    blockchain = Blockchain()
    alert_system = AlertSystem()
    blacklisted_entities = {'blacklisted_user'}

    # 2. Generate and ingest data
    good_raw_data = generate_good_raw_transactions()
    suspicious_raw_data = generate_suspicious_raw_transactions()

    good_transactions, good_valuations, good_entities, good_invoices = ingest_data(good_raw_data)
    suspicious_transactions, suspicious_valuations, suspicious_entities, suspicious_invoices = ingest_data(suspicious_raw_data)

    # 3. Generate valuations
    good_valuations_data = generate_synthetic_valuations(good_transactions)
    suspicious_valuations_data = generate_suspicious_valuations(suspicious_transactions)

    # 4. Ingest valuations
    _, good_valuations, _, _ = ingest_data(good_valuations_data)
    _, suspicious_valuations, _, _ = ingest_data(suspicious_valuations_data)

    # 5. Add to blockchain
    blockchain.add_block(good_transactions, good_valuations)
    blockchain.add_block(suspicious_transactions, suspicious_valuations)

    # 5. Run AML and Reputation
    aml_rules = AMLRules(blockchain, blacklisted_entities)
    aml_alerts = aml_rules.check_all_transactions()

    reputation_system = ReputationSystem(blockchain, blacklisted_entities)
    reputation_scores = reputation_system.calculate_reputation()

    # 6. Generate Alerts
    for tx_id, alerts in aml_alerts.items():
        alert_system.generate_alert(tx_id, "AML Rule Violation", {'alerts': alerts})

    # 7. Print summary
    print("--- Blockchain Verification ---")
    print(f"Is chain valid? {blockchain.verify_chain()}")
    print(f"Number of blocks: {len(blockchain.chain)}")

    print("\n--- AML Alerts ---")
    for alert in alert_system.get_alerts():
        print(alert)

    print("\n--- Reputation Scores ---")
    print(reputation_scores)

if __name__ == "__main__":
    main()
