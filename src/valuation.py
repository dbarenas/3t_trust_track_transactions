from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Any
from .models import Transaction, AssetValuation

def generate_synthetic_valuations(transactions: List[Transaction]) -> List[Dict[str, Any]]:
    """
    Generates synthetic valuation data for transactions requiring it.
    """
    valuations_data = []
    for tx in transactions:
        if tx.amount > 500:
            valuation_id = str(uuid.uuid4())
            tx.valuation_id = valuation_id

            valuations_data.append({
                'valuation_id': valuation_id,
                'transaction_id': tx.transaction_id,
                'third_party_id': 'third_party_validator_A',
                'valuation_amount': tx.amount * 1.05, # 5% markup
                'currency': tx.currency,
                'timestamp': tx.timestamp,
                'signature': 'signed_by_third_party'
            })
    return valuations_data

def generate_suspicious_valuations(transactions: List[Transaction]) -> List[Dict[str, Any]]:
    """
    Generates synthetic suspicious valuation data.
    """
    valuations_data = []

    # Transaction > 500 without valuation
    tx_no_valuation = next((tx for tx in transactions if tx.amount > 500), None)

    # Transaction with fraudulent valuation (bad signature)
    tx_bad_signature = next((tx for tx in transactions if tx.amount > 500 and tx.transaction_id != tx_no_valuation.transaction_id), None)
    if tx_bad_signature:
        valuation_id = str(uuid.uuid4())
        tx_bad_signature.valuation_id = valuation_id
        valuations_data.append({
            'valuation_id': valuation_id,
            'transaction_id': tx_bad_signature.transaction_id,
            'third_party_id': 'third_party_validator_B',
            'valuation_amount': tx_bad_signature.amount * 1.10,
            'currency': tx_bad_signature.currency,
            'timestamp': tx_bad_signature.timestamp,
            'signature': 'tampered_signature'
        })

    return valuations_data
