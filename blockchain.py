import time
import hashlib
from uuid import uuid4
import requests

from flask import Flask, jsonify, url_for, request
from argparse import ArgumentParser


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

	@property
	def get_serialized_chain(self):
		return [vars(block) for block in self.chain]

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

	def mine_block(self, miner_address):
		# Sender "0" means that this node has mined a new block
		# For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
		self.create_new_transaction(
			sender="0",
			reciver=miner_address,
			amount=1,
		)

		last_block = self.get_last_block

		last_proof = last_block.proof
		proof = self.create_proof_of_work(last_proof)

		last_hash = last_block.get_block_hash
		block = self.create_new_block(proof, last_hash)

		return vars(block) # Return a native Dict type object

if __name__ == '__main__':

	app = Flask(__name__)

	parser = ArgumentParser()
	parser.add_argument('-H', '--host', default='127.0.0.1')
	parser.add_argument('-p', '--port', default=5000, type=int)
	args = parser.parse_args()

	blockcahin = BlockChain()

	node_address = uuid4().hex

	@app.route('/create-transaction',methods = ['POST'])
	def create_transaction():
		transaction_data = request.get_json()

		index = blockcahin.create_new_transaction(**transaction_data)

		response = {
			'message': 'Transaction has been submitted successfully',
			'block': index
		}

		return jsonify(response),201


	@app.route('/mine',methods = ['GET'])
	def mine():
		block = blockcahin.mine_block(node_address)

		response = {
			'message': 'Data mined successfully',
			'mined_block': block
		}

		return jsonify(response)

	@app.route('/full_chain',methods = ['GET'])
	def full_chain():
		response = {
			'blockchain': blockcahin.get_serialized_chain
		}

		return jsonify(response)

	app.run(host=args.host, port=args.port, debug=True)