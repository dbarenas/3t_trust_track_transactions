"""
Demonstration script for the 3T (Traceability, Transparency, and Trust) system.
"""

import json
import hashlib
from web3 import Web3
from pymerkle.tree import MerkleTree
from web3.exceptions import ContractLogicError

# --- 1. Web3 Configuration ---
RPC_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
try:
    w3.eth.default_account = w3.eth.accounts[0]
    OWNER = w3.eth.default_account
except IndexError:
    print("No accounts found. Please ensure a local blockchain is running.")
    exit()


# --- Contract Configuration ---
MERKLE_REGISTRY_ADDR = "0xYourMerkleRegistryHere"
ENTITY_REGISTRY_ADDR = "0xYourEntityRegistryHere"

with open("BlockMerkleRegistry_ABI.json", "r") as f:
    MERKLE_REGISTRY_ABI = json.load(f)

with open("EntityRegistry_ABI.json", "r") as f:
    ENTITY_REGISTRY_ABI = json.load(f)

merkle_registry = w3.eth.contract(address=MERKLE_REGISTRY_ADDR, abi=MERKLE_REGISTRY_ABI)
entity_registry = w3.eth.contract(address=ENTITY_REGISTRY_ADDR, abi=ENTITY_REGISTRY_ABI)

# --- 2. Off-chain Functions ---
def make_merkle_root(transactions):
    """Calculates the Merkle root for a list of transactions."""
    tree = MerkleTree(hash_type="sha256")
    for tx in transactions:
        tree.update(str(tx).encode())
    return tree.root.value

def get_tx_proof(transactions, tx_index):
    """Generates a Merkle proof for a specific transaction."""
    tree = MerkleTree(hash_type="sha256")
    leaves = [str(tx).encode() for tx in transactions]
    for leaf in leaves:
        tree.update(leaf)

    leaf_data_to_prove = leaves[tx_index]
    leaf_hash = hashlib.sha256(b'\x00' + leaf_data_to_prove).digest()

    proof_obj = tree.prove(leaf_data_to_prove)

    formatted_proof = [lemma.value for lemma in proof_obj.lemmas]

    return leaf_hash, formatted_proof

# --- 3. On-chain Functions ---
def registerEntity(entity_id):
    """Registers a new entity in the EntityRegistry contract."""
    try:
        tx_hash = entity_registry.functions.registerEntity(entity_id).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"  - Successfully registered entity: {entity_id}")
    except Exception as e:
        print(f"  - Could not register entity {entity_id}: {e}")


def updateReputation(entity_id, new_reputation):
    """Updates the reputation of an entity in the EntityRegistry contract."""
    try:
        tx_hash = entity_registry.functions.updateReputation(entity_id, new_reputation).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"  - Successfully updated reputation for {entity_id}")
    except Exception as e:
        print(f"  - Could not update reputation for {entity_id}: {e}")

def getReputation(entity_id):
    """Gets the reputation of an entity from the EntityRegistry contract."""
    try:
        return entity_registry.functions.getReputation(entity_id).call()
    except Exception as e:
        print(f"  - Could not get reputation for {entity_id}: {e}")
        return 0

def commitBlock(merkle_root):
    """Commits a new block to the BlockMerkleRegistry contract."""
    try:
        tx_hash = merkle_registry.functions.commitBlock(merkle_root).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("  - Successfully committed block to the registry.")
    except Exception as e:
        print(f"  - Could not commit block: {e}")

def verifyLeafInBlock(block_number, leaf, proof):
    """Verifies a transaction's inclusion in a block."""
    try:
        return merkle_registry.functions.verifyLeafInBlock(block_number, leaf, proof).call()
    except ContractLogicError as e:
        print(f"  - Verification failed: {e}")
        return False
    except Exception as e:
        print(f"  - An unexpected error occurred during verification: {e}")
        return False

# --- 4. 3T Demo Flow ---
def run_demo_3T():
    """Main function to run the demonstration."""
    print("--- Running 3T Demo ---")

    # Create entities
    entities = ["A", "B", "C", "D"]
    for entity in entities:
        print(f"Registering entity: {entity}")
        registerEntity(entity)

    # Process a block of transactions
    transactions = [
        {"entity": "A", "amount": 120, "country": "ES"},
        {"entity": "B", "amount": 950, "country": "US"},
        {"entity": "C", "amount": 30, "country": "CO"},
        {"entity": "D", "amount": 450, "country": "DE"},
    ]

    # Calculate Merkle Root
    merkle_root = make_merkle_root(transactions)
    print(f"\nCalculated Merkle Root: {merkle_root.hex()}")

    # Register block on-chain
    print("Registering block on-chain...")
    commitBlock(merkle_root)

    # Apply AML logic
    print("\nApplying AML logic and updating reputations...")
    for tx in transactions:
        if tx["amount"] >= 500:
            print(f"  - Flagged transaction from {tx['entity']} for high amount. Decreasing reputation.")
            current_reputation = getReputation(tx['entity'])
            updateReputation(tx['entity'], current_reputation - 10)

    # Print final reputation
    print("\nFinal reputations:")
    for entity in entities:
        reputation = getReputation(entity)
        print(f"  - {entity}: {reputation}")


    # Generate and verify Merkle proof for transaction 1 (B)
    print("\nGenerating Merkle proof for transaction 1 (B)...")
    leaf, proof = get_tx_proof(transactions, 1)
    print(f"  - Leaf: {leaf.hex()}")
    print(f"  - Proof: {[p.hex() for p in proof]}")

    print("\nVerifying transaction in the contract...")
    is_valid = verifyLeafInBlock(0, leaf, proof)
    print(f"  - Verification result: {is_valid}")


# --- 5. Executable ---
if __name__ == "__main__":
    run_demo_3T()
