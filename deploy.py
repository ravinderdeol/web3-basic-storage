# import the requied python packages
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

# load the dotenv function
load_dotenv()

# open the gradestorage file and save it in variable
# read the file and close it upon completion
with open("./GradeStorage.sol", "r") as file:
    grade_storage_file = file.read()

# install the solidity compiler version
install_solc("0.6.0")

# save the compiled code to a variable
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"GradeStorage.sol": {"content": grade_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# dump the compiled code into a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# save the bytecode in a variable
bytecode = compiled_sol["contracts"]["GradeStorage.sol"]["GradeStorage"]["evm"]["bytecode"]["object"]

# save the abi in a variable
abi = compiled_sol["contracts"]["GradeStorage.sol"]["GradeStorage"]["abi"]

# connect to a local chain in ganache
# change these details to connect to infura
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x4271c1B152BaAa9FC279338d16cFF9F5f2e5AC9F"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
GradeStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction count
nonce = w3.eth.getTransactionCount(my_address)

# build the deploy transaction for the contract
# the trans parameters get added to create a trans object
transaction = GradeStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce})

# sign the transaction with a private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("DEPLOYING CONTRACT ...")

# send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait for the block confirmations
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("DEPLOYED!")

# need the contract address and abi to work with a contract
grade_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call a view function in the smart contract
print(grade_storage.functions.readGrade().call())

print("UPDATING CONTRACT ...")

# nonce plus once can only be used for one transaction
store_transaction = grade_storage.functions.storeGrade(10).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1})

# sign the above transaction
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key)

# send the above transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("UPDATED!")

print(grade_storage.functions.readGrade().call())
