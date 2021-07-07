""" Just some various simple functions that I need for the other parts of the notarization code.\n
Because I use infura I add an exception class ``NoInfuraConnection`` that allows me to report back nice error messages in case there is an issue.
This is used in the function ``establish_infura_connection`` which I use to connect to the ETH network via infura. \n
The function ``create_transaction_etherscan_link`` is just a handy tool for creating etherscan links based on tx_hashes. \n
The functions ``file_as_bytes``, ``calculate_hash_of_file_directly`` and ``calculate_hash_of_file_via_path`` are all for convenient hashing in other places. """
import hashlib
import sys

from web3 import Web3


class NoInfuraConnection(Exception):
    """Exception raised if web3 cannot connect via infura URL.

    Attributes:
        infura_url (string): The infura URL given.\n
        message (string): Explanation to user.
    """

    def __init__(
        self,
        infura_url,
        message="Not successfully connected to Ethereum (Test-)Network. Please check your internet connection and the infura URL.",
    ):
        self.infura_url = infura_url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Infura URL used: {self.infura_url}"


def file_as_bytes(file):
    """Reads file as binary.
    Args:
        file: File to read as binary

    Returns:
        binary file
    """
    with file:
        return file.read()


def calculate_hash_of_file_directly(file):
    """Calculate SHA256 checksum of binary file.
    IMPORTANT: File needs to be encoded as binary.
    Args:
        file (binary): Binary file

    Returns:
        calculated hash
    """

    return hashlib.sha256(file_as_bytes(file)).hexdigest()


def calculate_hash_of_file_via_path(path):
    """Read file in as binary and apply hash.
    Args:
        path (string): Path to the file that is to be hashed

    Returns:
        string: calculated hash
    """
    try:
        with open(path, "rb") as f:
            return calculate_hash_of_file_directly(f)
    except FileNotFoundError:
        print(
            f"No file exists under the specified path ({path}). Please make sure that you provide the full and correct path to the file."
        )
        sys.exit()


def create_transaction_etherscan_link(tx_hash, network):
    """Creates etherscan link for a transaction.
    Args:
        tx_hash (string): The transaction hash.\n
        networ (string): The network the transaction is on.

    Returns:
        url (string): The url for etherscan.
    """
    if network == "ropsten":
        url = "https://ropsten.etherscan.io/tx/" + tx_hash
    elif network == "goerli":
        url = "https://goerli.etherscan.io/tx/" + tx_hash
    elif network == "mainnet":
        url = "https://etherscan.io/tx/" + tx_hash
    else:
        # TODO: Exception needs to be thrown here
        pass

    return url


def establish_infura_connection(infura_url):
    """Establishes web3 connection via infura URL. Raises exception if URL is invalid.
    Args:
        infura_url (string): Infura URL to connect to network.

    Returns:
        web3_connection: A Web3 connection object that can be used in the following.
    """
    web3_connection = Web3(Web3.HTTPProvider(infura_url))
    if web3_connection.isConnected() == False:
        raise NoInfuraConnection(infura_url=infura_url)
    else:
        print("Successfully connected to Ethereum (Test-)Network. Can continue.")
        return web3_connection
