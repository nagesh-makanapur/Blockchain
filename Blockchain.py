import hashlib
import time
import json

class Block:
    """Represents a single block in the blockchain."""
    
    def __init__(self, index, transactions, previous_hash):
        self.index = index  # Position of the block in the chain
        self.timestamp = time.time()  # Time of creation
        self.transactions = transactions  # List of transactions
        self.previous_hash = previous_hash  # Hash of the previous block
        self.nonce = 0  # Random number for mining
        self.hash = self.calculate_hash()  # Calculate the hash of the block
    
    def calculate_hash(self):
        """Calculates and returns the SHA-256 hash of the block."""
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)  # Sorting keys for consistency
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Performs Proof of Work by finding a hash with leading zeros."""
        while self.hash[:difficulty] != "0" * difficulty:  # Check for leading zeros
            self.nonce += 1  # Increment nonce to change hash
            self.hash = self.calculate_hash()

class Blockchain:
    """A simple Blockchain implementation."""
    
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]  # Start with the genesis block
        self.difficulty = difficulty  # Difficulty level for mining
    
    def create_genesis_block(self):
        """Creates the first block (Genesis Block)."""
        return Block(0, "Genesis Block", "0")  # Genesis block has no previous hash
    
    def add_block(self, transactions):
        """Adds a new block to the blockchain after mining."""
        previous_block = self.chain[-1]  # Get the last block
        new_block = Block(len(self.chain), transactions, previous_block.hash)
        new_block.mine_block(self.difficulty)  # Mine the new block
        self.chain.append(new_block)  # Append the new block to the chain
    
    def is_chain_valid(self):
        """Checks if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Validate hash integrity
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Validate chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def print_blockchain(self):
        """Prints all blocks in the blockchain."""
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("-" * 40)

if __name__ == "__main__":
    # Initialize Blockchain
    blockchain = Blockchain()
    
    # Add Blocks
    blockchain.add_block(["Alice pays Bob 10 BTC", "Bob pays Charlie 5 BTC"])
    blockchain.add_block(["Charlie pays Dave 2 BTC", "Dave pays Alice 1 BTC"])
    
    # Print Blockchain
    blockchain.print_blockchain()
    
    # Validate Blockchain
    print("Blockchain Validity before tampering:", blockchain.is_chain_valid())
    
    # Tampering Test
    blockchain.chain[1].transactions = ["Alice pays Bob 100 BTC"]  # Modify transaction
    
    print("Blockchain Validity after tampering:", blockchain.is_chain_valid())