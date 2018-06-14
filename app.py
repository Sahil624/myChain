from blockchain import BlockChain

from uuid import uuid4
import os
from flask import Flask, jsonify, url_for, request
from argparse import ArgumentParser

app = Flask(__name__)



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

	app.run(host=host,port=port,debug = True)