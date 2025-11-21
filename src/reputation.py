from typing import Dict, List
from datetime import datetime
from .models import Reputation, Transaction

DEFAULT_REPUTATION_SCORE = 0.5
REPUTATION_DECREASE_RATE = 0.1
REPUTATION_INCREASE_RATE = 0.05

class ReputationSystem:
    """Manages the reputation of entities."""

    def __init__(self):
        self.reputations: Dict[str, Reputation] = {}

    def get_reputation(self, entity_id: str) -> float:
        """
        Retrieves the reputation score for a given entity.
        Returns a default score if the entity is not found.
        """
        if entity_id in self.reputations:
            return self.reputations[entity_id].score
        return DEFAULT_REPUTATION_SCORE

    def update_reputation(self, entity_id: str, new_score: float, reason: str):
        """
        Updates the reputation score of an entity.
        """
        if not (0.0 <= new_score <= 1.0):
            raise ValueError("Reputation score must be between 0.0 and 1.0.")

        reputation_record = Reputation(
            entity_id=entity_id,
            score=new_score,
            timestamp=datetime.now(),
            reason=reason
        )
        self.reputations[entity_id] = reputation_record

    def update_reputations_from_alerts(self, transactions: List[Transaction], aml_alerts: Dict[str, List[str]]):
        """
        Updates entity reputations based on AML alert outcomes for a set of transactions.
        """
        for tx in transactions:
            current_sender_score = self.get_reputation(tx.sender_id)
            current_receiver_score = self.get_reputation(tx.receiver_id)

            if tx.transaction_id in aml_alerts:
                # Decrease reputation for flagged transactions
                new_sender_score = max(0.0, current_sender_score - REPUTATION_DECREASE_RATE)
                new_receiver_score = max(0.0, current_receiver_score - REPUTATION_DECREASE_RATE)
                reason = f"Transaction {tx.transaction_id} flagged in AML check."
            else:
                # Increase reputation for clean transactions
                new_sender_score = min(1.0, current_sender_score + REPUTATION_INCREASE_RATE)
                new_receiver_score = min(1.0, current_receiver_score + REPUTATION_INCREASE_RATE)
                reason = f"Successful transaction {tx.transaction_id}."

            self.update_reputation(tx.sender_id, new_sender_score, reason)
            self.update_reputation(tx.receiver_id, new_receiver_score, reason)

    def get_all_reputations(self) -> Dict[str, float]:
        """Returns all current reputation scores."""
        return {entity_id: rep.score for entity_id, rep in self.reputations.items()}
