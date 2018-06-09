import time
import hashlib


class Block:

	def __init__(self, index, proof, prev_hash, transaction):
		self.index = index
		self.proof = proof
		self.prev_hash = prev_hash
		self.transaction = transaction
		self.timestamp = time.time()


	@property
	def get_block_hash(self):
		block_string = '{}{}{}{}{}'.format(self.index, self.proof, self.prev_hash, self.transaction, self.timestamp)
		return hashlib.sha256(block_string.encode()).hexdigest()


class BlockChain:
	def __init__(self):
		self.chain = []
		self.current_node_transaction = []
		self.create_genesis_node()

	def create_genesis_node(self):
		pass

	def create_new_block(self):
		pass

	def create_new_transaction(self):
		pass

	@staticmethod
	def create_proof_of_work(self):
		pass

	@property
	def get_last_block(self):
		pass