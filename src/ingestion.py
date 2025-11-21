from typing import List, Dict, Any, Tuple
import pandas as pd
from .cleaning import clean_data
from .models import Transaction, AssetValuation, Entity, Invoice

def ingest_data(raw_data: List[Dict[str, Any]]) -> Tuple[List[Transaction], List[AssetValuation], List[Entity], List[Invoice]]:
    """
    Ingests raw data, cleans it, and converts it into domain objects.
    """
    cleaned_df = clean_data(raw_data)

    transactions: List[Transaction] = []
    valuations: List[AssetValuation] = []
    entities: Dict[str, Entity] = {}
    invoices: List[Invoice] = []

    for _, row in cleaned_df.iterrows():
        if 'sender_id' in row:
            # Create Transaction object
            transaction = Transaction(
                transaction_id=row['transaction_id'],
                timestamp=row['timestamp'],
                amount=row['amount'],
                currency=row['currency'],
                payment_method=row['payment_method'],
                country=row['country'],
                sender_id=row['sender_id'],
                receiver_id=row['receiver_id'],
                invoice_id=row['invoice_id'],
                valuation_id=row.get('valuation_id')
            )
            transactions.append(transaction)

        # Create AssetValuation object if valuation data is present
        if pd.notna(row.get('valuation_id')) and 'third_party_id' in row:
             valuation = AssetValuation(
                 valuation_id=row['valuation_id'],
                 transaction_id=row['transaction_id'],
                 third_party_id=row['third_party_id'],
                 valuation_amount=row['valuation_amount'],
                 currency=row['currency'],
                 timestamp=row['timestamp'],
                 signature=row['signature']
             )
             valuations.append(valuation)

        if 'sender_id' in row:
            # Create Entity objects
            for entity_id in [row['sender_id'], row['receiver_id']]:
                if entity_id not in entities:
                    entities[entity_id] = Entity(entity_id=entity_id, name=entity_id, type='person')

            # Create Invoice object
            if 'invoice_date' in row:
                invoice = Invoice(
                    invoice_id=row['invoice_id'],
                    date=row['invoice_date'],
                    amount=row['amount'],
                    concept=row['invoice_concept'],
                    provider=row['invoice_provider']
                )
                invoices.append(invoice)

    return transactions, valuations, list(entities.values()), invoices
