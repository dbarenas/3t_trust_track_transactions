from typing import List, Dict, Set
from datetime import timedelta
from .models import Transaction, AssetValuation
from .blockchain import Blockchain

class AMLRules:
    def __init__(self, blockchain: Blockchain, blacklisted_entities: Set[str]):
        self.blockchain = blockchain
        self.blacklisted_entities = blacklisted_entities

    def check_transaction(self, transaction: Transaction) -> List[str]:
        """Checks a single transaction against AML rules."""
        alerts = []

        # Rule 1: High-value transaction without valuation
        if transaction.amount > 500:
            if not transaction.valuation_id:
                alerts.append(f"High-value transaction {transaction.transaction_id} is missing valuation.")
            else:
                valuation = self.blockchain.find_valuation(transaction.valuation_id)
                if not valuation:
                    alerts.append(f"Valuation {transaction.valuation_id} for transaction {transaction.transaction_id} not found in blockchain.")
                elif abs(valuation.valuation_amount - transaction.amount) / transaction.amount > 0.2:
                    alerts.append(f"Valuation amount for {transaction.transaction_id} is not reasonable.")

        # Rule 2: Transaction with blacklisted entity
        if transaction.sender_id in self.blacklisted_entities or transaction.receiver_id in self.blacklisted_entities:
            alerts.append(f"Transaction {transaction.transaction_id} involves a blacklisted entity.")

        return alerts

    def check_transaction_splitting(self, threshold=500, time_window_hours=24) -> List[str]:
        """Detects transaction splitting (Fraccionamiento)."""
        alerts = []
        transactions_by_party: Dict[Tuple[str, str], List[Transaction]] = {}

        # Group transactions by sender-receiver pair
        for block in self.blockchain.chain:
            for tx in block.transactions:
                pair = tuple(sorted((tx.sender_id, tx.receiver_id)))
                if pair not in transactions_by_party:
                    transactions_by_party[pair] = []
                transactions_by_party[pair].append(tx)

        # Check for splitting
        for pair, transactions in transactions_by_party.items():
            if len(transactions) > 1:
                transactions.sort(key=lambda tx: tx.timestamp)
                for i in range(len(transactions) - 1):
                    time_diff = transactions[i+1].timestamp - transactions[i].timestamp
                    if time_diff <= timedelta(hours=time_window_hours):
                        total_amount = transactions[i].amount + transactions[i+1].amount
                        if total_amount > threshold:
                            alerts.append(f"Transaction splitting detected between {pair[0]} and {pair[1]}.")
        return alerts

    def check_all_transactions(self) -> Dict[str, List[str]]:
        """Checks all transactions in the blockchain against AML rules."""
        all_alerts = {}
        for block in self.blockchain.chain:
            for tx in block.transactions:
                alerts = self.check_transaction(tx)
                if alerts:
                    all_alerts[tx.transaction_id] = alerts

        splitting_alerts = self.check_transaction_splitting()
        if splitting_alerts:
            all_alerts["splitting"] = splitting_alerts

        circular_flow_alerts = self.check_circular_flows()
        if circular_flow_alerts:
            all_alerts["circular_flows"] = circular_flow_alerts

        return all_alerts

    def check_circular_flows(self) -> List[str]:
        """Detects circular fund flows (e.g., A -> B -> C -> A)."""
        alerts = []
        graph: Dict[str, List[str]] = {}

        # Build transaction graph
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender_id not in graph:
                    graph[tx.sender_id] = []
                graph[tx.sender_id].append(tx.receiver_id)

        # Detect cycles
        for start_node in graph:
            path = [start_node]
            visited = {start_node}

            # DFS to find cycles
            stack = [(start_node, iter(graph.get(start_node, [])))]
            while stack:
                parent, children = stack[-1]
                try:
                    child = next(children)
                    if child in visited:
                        if child == start_node:
                            alerts.append(f"Circular flow detected: {' -> '.join(path)} -> {child}")
                    else:
                        visited.add(child)
                        path.append(child)
                        stack.append((child, iter(graph.get(child, []))))
                except StopIteration:
                    path.pop()
                    visited.remove(parent)
                    stack.pop()
        return alerts
