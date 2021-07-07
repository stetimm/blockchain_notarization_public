import os
import sys

import pytest
from web3 import Web3

sys.path.insert(0, os.path.abspath("src"))
from blockchain_config import INFURA_URL

sys.path.insert(0, os.path.abspath("src/notarization_code"))
from utils import (
    calculate_hash_of_file_via_path,
    establish_infura_connection,
    NoInfuraConnection,
)


@pytest.fixture
def connection_and_account_data():
    return {
        "infura_url": INFURA_URL,
        "account": "0x417a7f57bfb638906ccF7c52B5a8A9B6259d21Cd",
    }


def test_invalid_infura_url(connection_and_account_data):
    """
    Test if you can establish connection with valid infura url.
    """
    with pytest.raises(NoInfuraConnection):
        establish_infura_connection(
            connection_and_account_data["infura_url"] + "x"
        )  # invalid URL


def test_calculate_hash_of_file_via_path():
    """
    Compares SHA256 checksum of test_data.csv calculated externally to the hash calculated by my function.
    """
    path = sys.path[1] + "/tests/test_data.csv"
    calculated_hash = calculate_hash_of_file_via_path(path)
    assert (
        calculated_hash
        == "15679810d4ef3bcdb4a00608f36297c0dcc46697aa08fbd28e8c95178984c6a3"
    )


def test_file_does_not_exist():
    """
    Checks if system exit occurs if file does not exist (desired behavior).
    """
    path = sys.path[1] + "/bs.csv"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        calculate_hash_of_file_via_path(path)
    assert pytest_wrapped_e.type == SystemExit
