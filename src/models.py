from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class Entity(BaseModel):
    """Represents a person or a company involved in transactions."""
    entity_id: str
    name: str
    type: str  # 'person' or 'company'
    risk_score: float = 0.0

class Invoice(BaseModel):
    """Represents an invoice related to a transaction."""
    invoice_id: str
    date: datetime
    amount: float
    concept: str
    provider: str

class AssetValuation(BaseModel):
    """Represents the valuation of an asset by a third party."""
    valuation_id: str
    transaction_id: str
    third_party_id: str
    valuation_amount: float
    currency: str
    timestamp: datetime
    signature: str  # Simulated signature
    metadata: Optional[Dict] = None

class Transaction(BaseModel):
    """Represents a single financial transaction."""
    transaction_id: str
    timestamp: datetime
    amount: float
    currency: str
    payment_method: str
    country: str
    sender_id: str
    receiver_id: str
    invoice_id: str
    valuation_id: Optional[str] = None

class ReputationRecord(BaseModel):
    """Represents a reputation score at a point in time."""
    entity_id: str
    score: float
    timestamp: datetime
    reason: str

class Block(BaseModel):
    """Represents a block in the blockchain."""
    index: int
    timestamp: datetime
    transactions: List[Transaction]
    valuations: List[AssetValuation]
    previous_hash: str
    hash: Optional[str] = None
