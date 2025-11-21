from typing import List, Optional
from datetime import datetime
import hashlib
import json
from .models import Block, Transaction, AssetValuation

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the very first block in the chain."""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now(),
            transactions=[],
            valuations=[],
            previous_hash="0"
        )
        genesis_block.hash = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        """Returns the last block in the chain."""
        return self.chain[-1]

    def add_block(self, transactions: List[Transaction], valuations: List[AssetValuation]) -> Block:
        """Adds a new block to the blockchain."""
        previous_block = self.get_last_block()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=datetime.now(),
            transactions=transactions,
            valuations=valuations,
            previous_hash=previous_block.hash
        )
        new_block.hash = self.calculate_hash(new_block)
        self.chain.append(new_block)
        return new_block

    def calculate_hash(self, block: Block) -> str:
        """Calculates the hash of a block."""
        block_dict = block.dict(exclude={'hash'})
        block_dict['transactions'] = [tx.dict() for tx in block.transactions]
        block_dict['valuations'] = [v.dict() for v in block.valuations]

        block_string = json.dumps(block_dict, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def verify_chain(self) -> bool:
        """Verifies the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def find_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Finds a transaction by its ID in the blockchain."""
        for block in self.chain:
            for tx in block.transactions:
                if tx.transaction_id == transaction_id:
                    return tx
        return None

    def find_valuation(self, valuation_id: str) -> Optional[AssetValuation]:
        """Finds a valuation by its ID in the blockchain."""
        for block in self.chain:
            for v in block.valuations:
                if v.valuation_id == valuation_id:
                    return v
        return None
