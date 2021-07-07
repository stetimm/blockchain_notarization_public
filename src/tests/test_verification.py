import os
import sys

import pytest
from web3 import Web3

sys.path.insert(0, os.path.abspath("src"))

from blockchain_config import INFURA_URL

sys.path.insert(0, os.path.abspath("src/notarization_code"))
from verification import verify_via_transaction


@pytest.fixture
def test_input():
    return {
        "web3_connection": Web3(Web3.HTTPProvider(INFURA_URL)),
        "tx_hash": "0xf0539dd9a25a7bf1758577ce6c7792a4002ac25624663bc528fab9a249df1800",
        "filepath_1": sys.path[1] + "/tests/test_data.csv",
        "filepath_2": sys.path[1] + "/tests/verification.py",
        "hash_1": "15679810d4ef3bcdb4a00608f36297c0dcc46697aa08fbd28e8c95178984c6a3",  # the correct hash of test_data.csv
        "hash_2": "0",
    }


def test_verification_wrong_tx_hash(test_input, capfd):
    """Test correct behavior if wrong tx_hash is specified."""
    # alter tx_hash from fixture:
    tx_hash = test_input["tx_hash"].replace("7", "3")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        verify_via_transaction(
            web3_connection=test_input["web3_connection"],
            tx_hash=tx_hash,
            filepath=test_input["filepath_1"],
        )
    out, err = capfd.readouterr()
    assert f"Could not find transaction with hash ({tx_hash})" in out
    assert pytest_wrapped_e.type == SystemExit


def test_verification_with_file_success(test_input):
    """Tests verification via file with a known transaction. Should succeed."""
    # hash of test_data.csv has been stored in the following transaction
    result = verify_via_transaction(
        web3_connection=test_input["web3_connection"],
        tx_hash=test_input["tx_hash"],
        filepath=test_input["filepath_1"],
    )
    assert result["verified"] == True


def test_verification_with_file_fail(test_input):
    """Tests verification via file with a known transaction. Should fail."""
    result = verify_via_transaction(
        web3_connection=test_input["web3_connection"],
        tx_hash=test_input["tx_hash"],
        hash_value=test_input["filepath_2"],
    )
    assert result["verified"] == False


def test_verification_with_hash_success(test_input):
    """Tests verification via hash with a known transaction. Should succeed."""
    result = verify_via_transaction(
        web3_connection=test_input["web3_connection"],
        tx_hash=test_input["tx_hash"],
        hash_value=test_input["hash_1"],
    )
    assert result["verified"] == True


def test_verification_with_hash_fail(test_input):
    """Tests verification via file with a known transaction. Should fail."""
    result = verify_via_transaction(
        web3_connection=test_input["web3_connection"],
        tx_hash=test_input["tx_hash"],
        hash_value=test_input["hash_2"],
    )
    assert result["verified"] == False
