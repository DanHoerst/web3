from solcx import compile_standard
from web3 import Web3

import json
import os

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file
            }
        },
        "settings": {
            "outputSelection": {
                "*" : {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("CHAIN_ENDPOINT")))
chain_id = os.getenv("CHAIN_ID")
my_address = os.getenv("WALLET_ADDRESS")
private_key = os.getenv("WALLET_PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction for nonce
nonce = w3.eth.getTransactionCount(my_address)

# Build, Sign and Send a transaction
transaction = SimpleStorage.constructor().buildTransaction({ "chainId": chain_id, "from": my_address, "nonce": nonce })
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Working with the contract, you always need
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1
    }
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)
print(simple_storage.functions.retrieve().call())
