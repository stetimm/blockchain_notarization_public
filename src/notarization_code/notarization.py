""" All Functions necessary for Notarization. The core pieces of the code are the function ``create_notarization_transaction`` and ``send_transaction``. \n
The former initializes the notarization to send, with the letter it is sent to the blockchain.
The ``account_balance_sufficient`` function is just a little piece of helper code to check if the balance of the account is sufficient to send the transaction.
Because the transaction is over 0 ETH sent from one account back to itself, the only cost is gas. Therefore, sufficient balance is determined by gas price and gas limit.
The exception class ``AccountBalanceInsufficient`` is there to give nice feedback in case the balance is insufficient.

"""
import binascii
import sys

from web3 import exceptions
from web3 import Web3


class AccountBalanceInsufficient(Exception):
    """Exception raised if account balance is insufficient to cover gas fees for this transaction.

    Attributes:
        balance (int): Balance the account has (causing the exception). \n
        min_amount (int): Minimum balance the account should have. \n
        message (string): Explanation to user.
    """

    def __init__(
        self,
        balance,
        min_amount,
        message="Account balance is not sufficient to cover gas fees for this transaction.",
    ):
        self.balance = balance
        self.min_amount = min_amount
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Current Balance: {self.balance} gwei, Required Balance: {self.min_amount} gwei."


def create_notarization_transaction(
    web3_connection,
    account,
    string_to_save,
    gas_limit=2000000,
    gas_price=50,
):
    """Creates the transaction to be sent to blockchain, but does not send it yet.

    The function will get the current nonce (number of transactions sent so far) for the specified account and build a dictionary that details the transaction to be signed and sent.

    The transaction will just sent 0 ETH from the specified account back to itself. In this transaction, the string_to_save will be stored.

    Args:
        web3_connection (Web3 object): The web3 connection, initialized via ' Web3(Web3.HTTPProvider( ))'\n
        account (string): The address of the account to be sent and received from.\n
        string_to_save (string): The string to save.\n
        gas_limit (int, optional): Gas limit, not focus of proof-of-concept implementation. Will be multiplied with gas price later (defaults to 2000000).\n
        gas_price (int, in gwei, optional): The gas price specified in transaction to be sent (defaults to 50).


    Returns:
        tx (dictionary): Details for the transaction to be sent. Can be signed and sent to Ethereum Blockchain.

    """
    # check if balance of account is sufficient to execute transaction
    check_balance = account_balance_sufficient(
        web3_connection=web3_connection,
        account=account,
        gas_limit=gas_limit,
        gas_price=gas_price,
    )

    if check_balance["sufficient"] == False:
        raise AccountBalanceInsufficient(
            balance=check_balance["balance"], min_amount=gas_limit * gas_price
        )
    else:
        # get nonce for account
        nonce = web3_connection.eth.getTransactionCount(account)

        # build transaction
        tx = {
            "nonce": nonce,
            "to": account,
            "value": Web3.toWei(0, "ether"),  # sending just 0
            "gas": gas_limit,
            "gasPrice": Web3.toWei(gas_price, "gwei"),
            "data": Web3.toHex(text=string_to_save),
        }
        return tx


def send_transaction(web3_connection, transaction, private_key, time_limit=120):
    """Signs a transaction with private key and sends it to the blockchain via the specified web3_connection.
    IMPORTANT: Signing requires private key, which needs to be treated carefully!

    Args:
        web3_connection (Web3 object): The web3 connection, initialized via ' Web3(Web3.HTTPProvider( ))'\n
        transaction (dictionary): A dictionary specifying the details of the transaction.\n
        private_key (string): The private key for the account specified in transaction.\n
        time_limit (int): Number of seconds to wait for confirmation of mining of transaction.\n

    Returns a dictionary containing:
        tx_hash (string): The transaction hash of the signed transaction.\n
        tx_receipt (only if successful, dictionary): The transaction receipt of a mined transaction.
    """

    # sign transaction, check for invalid private key
    try:
        signed_tx = web3_connection.eth.account.signTransaction(
            transaction, private_key
        )
    except binascii.Error:
        print(
            "The private key you specified is invalid. It may only contain [0-9a-fA-F] characters. Execution aborted."
        )
        sys.exit()
    except ValueError as e:
        if "exactly 32 bytes" in str(e):
            print(
                "The private key you specified is invalid.",
                str(e),
                "Execution aborted.",
            )
            sys.exit()
        else:
            raise
    # get transaction hash
    tx_hash = Web3.toHex(signed_tx[1])

    # send transaction, check for incorrect private key
    try:
        web3_connection.eth.sendRawTransaction(signed_tx.rawTransaction)
    except ValueError as e:
        # this is a weird error that is thrown when you have incorrect pk.
        # Provide better message.
        if "'code': -32000" in str(e):
            print("The private key you specified is incorrect. Execution aborted.")
            sys.exit()
        else:
            raise

    print(
        "Sending Transaction. Waiting for Confirmation. Time Limit: ",
        time_limit,
        " seconds.",
    )
    # wait for confirmation
    try:
        tx_receipt = web3_connection.eth.waitForTransactionReceipt(
            transaction_hash=tx_hash, timeout=time_limit
        )
        print("Transaction successfully sent! Transaction Hash: ", tx_hash)
        return {"tx_hash": tx_hash, "tx_receipt": tx_receipt}
    except:
        print(
            "Transaction has not been mined yet. Please check for the following Transaction Hash: ",
            tx_hash,
        )
        return {
            "tx_hash": tx_hash,
        }


def account_balance_sufficient(
    web3_connection, account, gas_limit=2000000, gas_price=50
):
    """Checks if an accounts balance is sufficient to send transaction given either a minimum amount or gas limit and gas price.

    Args:
        web3_connection (Web3 object): The web3 connection, initialized via ' Web3(Web3.HTTPProvider( ))'.\n
        account (string): The address of the account to check the balance of.\n
        gas_limit (int): The gas limit of the transaction to be sent (usually 2000000).\n
        gas_price (int, in gwei): The gas price specified in transaction to be sent (defaults to 50).

    Returns:
        dictionary: Contains bolean indicating whether balance is sufficient and the balance.
    """
    try:
        balance_wei = web3_connection.eth.getBalance(account)
        balance_gwei = Web3.fromWei(balance_wei, "gwei")
        min_amount = gas_limit * gas_price
        if balance_gwei >= min_amount:
            return {"sufficient": True, "balance": balance_gwei}
        else:
            return {"sufficient": False, "balance": balance_gwei}
    except exceptions.InvalidAddress:
        print(
            f"There is no account for the address you entered ({account}). Please double check."
        )
        sys.exit()
