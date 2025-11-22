"""
Demonstration script for the Financial Transaction Analysis System.

This script provides a clear, step-by-step demonstration of the system's capabilities,
focusing on the dynamic reputation system.
"""
from datetime import datetime
import uuid
import pandas as pd

# Import system components
from src.ingestion import ingest_data
from src.blockchain import Blockchain
from src.rules import AMLRules
from src.reputation import ReputationSystem, DEFAULT_REPUTATION_SCORE
from src.alerts import AlertSystem
from src.valuation import generate_synthetic_valuations

def print_header(title):
    """Prints a formatted header for each section of the demo."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def main():
    """Main function to run the demonstration."""
    print_header("System Initialization")

    # 1. Initialize all system components
    reputation_system = ReputationSystem()
    blockchain = Blockchain(reputation_system)
    alert_system = AlertSystem()
    blacklisted_entities = {'blacklisted_user'}
    aml_rules = AMLRules(blockchain, blacklisted_entities, reputation_system)

    print("Reputation System, Blockchain, and AML Rules Engine are ready.")
    print(f"Default reputation score for new entities: {DEFAULT_REPUTATION_SCORE}")

    # 2. Define a set of sample raw transactions
    raw_transactions = [
        # A standard, compliant transaction
        {'transaction_id': 'tx_good_1', 'timestamp': datetime.now(), 'amount': 100, 'currency': 'USD', 'payment_method': 'credit_card', 'country': 'USA', 'sender_id': 'user_A', 'receiver_id': 'user_B', 'invoice_id': 'inv_1'},
        # A high-value transaction that requires valuation
        {'transaction_id': 'tx_good_2', 'timestamp': datetime.now(), 'amount': 600, 'currency': 'USD', 'payment_method': 'wire', 'country': 'USA', 'sender_id': 'user_C', 'receiver_id': 'user_D', 'invoice_id': 'inv_2'},
        # A transaction involving a blacklisted entity (will trigger an AML alert)
        {'transaction_id': 'tx_bad_1', 'timestamp': datetime.now(), 'amount': 50, 'currency': 'USD', 'payment_method': 'cash', 'country': 'USA', 'sender_id': 'user_E', 'receiver_id': 'blacklisted_user', 'invoice_id': 'inv_3'},
        # A high-value transaction missing its required valuation (will trigger an AML alert)
        {'transaction_id': 'tx_bad_2', 'timestamp': datetime.now(), 'amount': 1200, 'currency': 'EUR', 'payment_method': 'wire', 'country': 'EU', 'sender_id': 'user_F', 'receiver_id': 'user_G', 'invoice_id': 'inv_4'},
    ]

    print("\nSample transactions have been defined.")

    # 3. Ingest and process the transactions
    transactions, _, _, _ = ingest_data(raw_transactions)

    # Generate valuations only for the transactions that require them
    valuations_data = generate_synthetic_valuations([tx for tx in transactions if tx.amount > 500 and tx.transaction_id != 'tx_bad_2'])
    _, valuations, _, _ = ingest_data(valuations_data)

    print("Transactions and valuations have been ingested and processed.")

    # 4. Add transactions to the blockchain
    print_header("Blockchain Processing")
    print("Adding transactions to the blockchain...")
    blockchain.add_block(transactions, valuations)
    print(f"Blockchain now has {len(blockchain.chain)} blocks.")

    last_block = blockchain.get_last_block()
    print("\n--- Reputations Snapshotted in Last Block ---")
    for tx in last_block.transactions:
        print(f"  Transaction {tx.transaction_id}:")
        print(f"    Sender ({tx.sender_id}): {tx.sender_reputation}")
        print(f"    Receiver ({tx.receiver_id}): {tx.receiver_reputation}")

    # 5. Run AML analysis
    print_header("AML and Reputation Analysis")
    print("Running AML checks on all transactions...")
    aml_alerts = aml_rules.check_all_transactions()

    if aml_alerts:
        print("\n--- Generated AML Alerts ---")
        alerts_list = []
        for tx_id, alerts in aml_alerts.items():
            for alert in alerts:
                print(f"  Alert for {tx_id}: {alert}")
                alerts_list.append({'transaction_id': tx_id, 'alert': alert})

        alerts_df = pd.DataFrame(alerts_list)
        alerts_df.to_csv('aml_alerts.csv', index=False)
        print("\nAML alerts have been saved to aml_alerts.csv")
    else:
        print("No AML alerts were generated.")

    # 6. Update reputations based on AML outcomes
    print("\nUpdating reputations based on AML alert outcomes...")
    reputation_system.update_reputations_from_alerts(transactions, aml_alerts)
    print("Reputations have been updated.")

    # 7. Display final reputation scores
    print_header("Final Reputation Scores")
    final_scores = reputation_system.get_all_reputations()

    scores_list = []
    print(f"{'Entity':<20} | {'Score':<10} | {'Change'}")
    print("-"*45)
    for entity, score in sorted(final_scores.items()):
        change = ""
        if score > DEFAULT_REPUTATION_SCORE:
            change = "Increased"
        elif score < DEFAULT_REPUTATION_SCORE:
            change = "Decreased"
        else:
            change = "Unchanged"
        print(f"{entity:<20} | {score:<10.2f} | {change}")
        scores_list.append({'entity': entity, 'score': score, 'change': change})

    scores_df = pd.DataFrame(scores_list)
    scores_df.to_csv('reputation_scores.csv', index=False)
    print("\nFinal reputation scores have been saved to reputation_scores.csv")

if __name__ == "__main__":
    main()
