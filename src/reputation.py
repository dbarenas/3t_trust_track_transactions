from typing import Dict, List, Set
from .models import Transaction, ReputationRecord
from .blockchain import Blockchain

class ReputationSystem:
    def __init__(self, blockchain: Blockchain, blacklisted_entities: Set[str]):
        self.blockchain = blockchain
        self.blacklisted_entities = blacklisted_entities
        self.reputation_scores: Dict[str, float] = {}

    def calculate_reputation(self) -> Dict[str, float]:
        """Calculates reputation scores for all entities in the blockchain."""
        entity_transactions: Dict[str, List[Transaction]] = {}

        # Aggregate transactions per entity
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender_id not in entity_transactions:
                    entity_transactions[tx.sender_id] = []
                entity_transactions[tx.sender_id].append(tx)

                if tx.receiver_id not in entity_transactions:
                    entity_transactions[tx.receiver_id] = []
                entity_transactions[tx.receiver_id].append(tx)

        # Calculate scores
        for entity_id, transactions in entity_transactions.items():
            score = 0.0
            if entity_id in self.blacklisted_entities:
                score += 100 # High penalty for being blacklisted

            # More complex scoring logic can be added here
            # For now, we just count transactions
            score += len(transactions)

            self.reputation_scores[entity_id] = score

        return self.reputation_scores
