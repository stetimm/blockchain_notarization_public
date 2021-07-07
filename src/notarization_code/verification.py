""" The verification function. This is a relatively simple function that just "looks up" a transaction on the blockchain and compares the input_data of the transaction to
the hash of a file or a directly provided hash. """
import sys
from datetime import datetime

from utils import calculate_hash_of_file_via_path
from web3 import exceptions
from web3 import Web3


def verify_via_transaction(web3_connection, tx_hash, filepath="", hash_value=""):
    """Verifies that a specified file (or hash_value) matches the hash value in a specified transaction.

    Args:
        web3_connection (Web3 object): The web3 connection, initialized via ' Web3(Web3.HTTPProvider( ))'.\n
        tx_hash (string): The transaction hash for the transaction to look up.\n
        filepath (string): Path to the file that is to be verified.\n
        hash_value (string, optional): Instead of a filepath, the hash value to compare can be specified directly.\n

    Returns:
        result (dictionary): A dictionary specifying whether the file was verified and the timestamp of the block the transaction was mined in.
    """

    # get transaction
    try:
        fetched_tx = web3_connection.eth.getTransaction(tx_hash)
    except exceptions.TransactionNotFound:
        print(
            f"Could not find transaction with hash ({tx_hash}). Please double check if the hash is correct."
        )
        sys.exit()

    # get input string from transaction and convert from Hex to Text
    tx_string = Web3.toText(fetched_tx["input"])

    # get timestamp via block
    # fetched_block = web3_connection.eth.getBlock(fetched_tx["blockHash"])
    fetched_block = web3_connection.eth.get_block(fetched_tx["blockNumber"])
    mining_timestamp = fetched_block["timestamp"]
    timestamp_string = datetime.utcfromtimestamp(mining_timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # to actually verify we want to calculate hash of file here and compare with tx_string
    if filepath != "":
        validation = (
            True if tx_string == calculate_hash_of_file_via_path(filepath) else False
        )
    elif hash_value != "":
        validation = True if tx_string == hash_value else False

    result = {"timestamp": timestamp_string, "verified": validation}
    return result
