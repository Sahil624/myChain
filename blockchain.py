import time
import hashlib


class Block:

	def __init__(self, index, proof, previous_hash, transactions):
		self.index = index
		self.proof = proof
		self.previous_hash = previous_hash
		self.transactions = transactions
		self.timestamp = time.time()


	@property
	def get_block_hash(self):
		block_string = '{}{}{}{}{}'.format(self.index, self.proof, self.previous_hash, self.transactions, self.timestamp)
		return hashlib.sha256(block_string.encode()).hexdigest()


class BlockChain:
	def __init__(self):
		self.chain = []
		self.current_node_transactions = []
		self.create_genesis_node()

	def create_genesis_node(self):
		self.create_new_block(proof = 0, previous_hash = 0)

	def create_new_block(self, proof, previous_hash):
		block = Block(
				index=len(self.chain),
				proof=proof,
				previous_hash=previous_hash,
				transactions=self.current_node_transactions
			)

		self.chain.append(block)
		self.current_node_transactions = []

		return block

	def create_new_transaction(self ,sender ,reciver ,amount):
		self.current_node_transactions.append({
			'sender': sender,
			'reciver': reciver,
			'amount': amount
			})

		return self.get_last_block.index + 1

	@staticmethod
	def create_proof_of_work(prev_proof):
		proof = prev_proof + 1

		while (proof + prev_proof) % 7 != 0:
			proof += 1

		return proof

	@property
	def get_last_block(self):
		return self.chain[-1]