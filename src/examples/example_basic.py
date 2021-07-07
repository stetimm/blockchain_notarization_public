""" Proof-of-Concept example with infura. """
# importing all necessary packages
import os
import sys

# importing all required modules
sys.path.insert(0, os.path.abspath("src/notarization_code"))

from utils import (
    calculate_hash_of_file_via_path,
    create_transaction_etherscan_link,
    establish_infura_connection,
)
from notarization import create_notarization_transaction
from notarization import send_transaction
from verification import verify_via_transaction

# importing infura_url from blockchain_config (needs to be added manually)
sys.path.insert(0, os.path.abspath("src"))
from blockchain_config import INFURA_URL

# Establish web3 connection via infura
web3_connection = establish_infura_connection(INFURA_URL)


def notarization(web3_connection):
    """
    Notarization in this particular example, uses command line inputs.
    """
    account = input("Please enter the address of the account: ")
    private_key = input("Please enter the private key of the account: ")
    file_path = input("Please enter the full path of the file you want to notarize: ")
    string_to_save = calculate_hash_of_file_via_path(file_path)
    tx = create_notarization_transaction(
        web3_connection=web3_connection,
        account=account,
        string_to_save=string_to_save,
    )
    tx_hash = send_transaction(
        web3_connection=web3_connection, transaction=tx, private_key=private_key
    )["tx_hash"]
    print(
        "You can look up your transaction under the following Etherscan link: \n",
        create_transaction_etherscan_link(tx_hash, "ropsten"),
    )


def verification(web3_connection):
    """
    Verification in this particular example, uses command line inputs.
    """
    file_path = input("Please enter the full path of the file you want to verify: ")
    tx_hash = input("Please enter the corresponding transaction hash: ")
    result = verify_via_transaction(
        web3_connection=web3_connection, tx_hash=tx_hash, filepath=file_path
    )
    if result["verified"] == True:
        print(
            "Congratulations - The file is verified. The contents of this file have not been changed since it was notarized with this timestamp (time is in UTC, one hour behind Germany): ",
            result["timestamp"],
        )
    else:
        print(
            "Unfortunately, the file does not match what was notarized with the following timestamp (time is in UTC, one hour behind Germany): ",
            result["timestamp"],
        )


# While loop that manages command line interaction, quite rudimentary, but this is just an example...
while True:
    choice = input("Do you want to notarize [1] or verify [2] a file? ")
    if choice == "1":
        notarization(web3_connection)
        break
    elif choice == "2":
        verification(web3_connection)
        break
    else:
        print("Invalid input. Please input either 1 or 2.")
