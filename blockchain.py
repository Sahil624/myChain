#!/usr/bin/python

import time
import hashlib
from uuid import uuid4
import requests
import os

from flask import Flask, jsonify, url_for, request
from argparse import ArgumentParser

app = Flask(__name__)

class Block:

	def __init__(self, index, proof, previous_hash, transactions):
		self.index = index # index of block in blockchain
		self.proof = proof # A number made after successful mining process. Block will be created using this proof
		self.previous_hash = previous_hash # Hash of previous block. maintaing the chain
		self.transactions = transactions # dictionary of all the transactions queued
		self.timestamp = time.time() # Current timestamp. when  block is created


	# Create a hash of this block for refering 
	@property
	def get_block_hash(self):
		
		"""
			This hash makes the blockchain secure. Present hash is calculated using previous hash.
			If any attacker changes the block whole chain is broken.
		"""
		
		block_string = '{}{}{}{}{}'.format(self.index, self.proof, self.previous_hash, self.transactions, self.timestamp)
		return hashlib.sha256(block_string.encode()).hexdigest()


class BlockChain:
	
	def __init__(self):
		"""
			When a instance of blockchain is created :- 
			1) The chain is initialed to empty list.
			2) There are no transactions in blockchain.
			3) A genesis block (First block of chain ) is created.
		"""
		self.chain = []
		self.current_node_transactions = []
		self.create_genesis_node()

	# First block of chain with proof and previous hash 0
	def create_genesis_node(self):
		self.create_new_block(proof = 0, previous_hash = 0)

	@property
	def get_serialized_chain(self):
		"""
			returns serialized chain
		"""
		return [vars(block) for block in self.chain]

	def create_new_block(self, proof, previous_hash):
		
		"""
			Create new block
		"""
		
		block = Block(
				index=len(self.chain), # index is length of chain + 1
				proof=proof, 
				previous_hash=previous_hash, # Pending transactions are assigned to new Node
				transactions=self.current_node_transactions
			)

		self.chain.append(block) # New Block is appened to the chain 
		self.current_node_transactions = [] # As transaction are assigned to new block. So, current txns are reseted

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
		"""
			Proof of work algorithm 
		"""
		while (proof + prev_proof) % 7 != 0:
			proof += 1

		return proof

	@property
	def get_last_block(self):
		"""
			return last block of the chain
		"""
		return self.chain[-1]

	def mine_block(self, miner_address):
		"""
		 Sender "0" means that this node has mined a new block
		 For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
		"""
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


blockchain = BlockChain()

# Create unique address of current node
node_address = uuid4().hex

# Dummy index function
@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/create-transaction',methods = ['POST'])
def create_transaction():
	transaction_data = request.get_json()

	index = blockchain.create_new_transaction(**transaction_data)

	response = {
		'message': 'Transaction has been submitted successfully',
		'block': index
	}

	return jsonify(response),201


@app.route('/mine',methods = ['GET'])
def mine():
	block = blockchain.mine_block(node_address)

	response = {
		'message': 'Data mined successfully',
		'mined_block': block
	}

	return jsonify(response)

@app.route('/full_chain',methods = ['GET'])
def full_chain():
	response = {
		'blockchain': blockchain.get_serialized_chain
	}

	return jsonify(response)

if __name__ == '__main__':

	parser = ArgumentParser()
	parser.add_argument('-H', '--host', default='127.0.0.1')
	parser.add_argument('-p', '--port', default=5000, type=int)
	args = parser.parse_args()

	port = os.getenv('PORT', args.port)
	host = os.getenv('IP', args.host)

	app.run(host=os.environ['IP'],port=int(os.environ['PORT']),debug = True)