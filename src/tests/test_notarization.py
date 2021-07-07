import os
import sys

import pytest
from web3 import Web3

sys.path.insert(0, os.path.abspath("src"))

from blockchain_config import INFURA_URL

sys.path.insert(0, os.path.abspath("src/notarization_code"))
from notarization import (
    AccountBalanceInsufficient,
    create_notarization_transaction,
    send_transaction,
)


@pytest.fixture
def connection_and_account_data():
    return {
        "web3_connection": Web3(Web3.HTTPProvider(INFURA_URL)),
        "account": "0x417a7f57bfb638906ccF7c52B5a8A9B6259d21Cd",
    }


def test_insufficient_balance(connection_and_account_data):
    """
    Tests if insufficient account balance triggers custom exception.
    This is tested by using a ridiculously high required balance.
    """
    with pytest.raises(AccountBalanceInsufficient):
        create_notarization_transaction(
            web3_connection=connection_and_account_data["web3_connection"],
            account=connection_and_account_data["account"],
            string_to_save="Test",
            gas_limit=200000,
            gas_price=Web3.toWei(1000, "ether"),  # this is suuuper high.
        )


def test_create_notarization_transaction_sufficient_balance(
    connection_and_account_data,
):
    """
    Ensures that no error is triggered when balance is sufficient.
    """
    tx = create_notarization_transaction(
        web3_connection=connection_and_account_data["web3_connection"],
        account=connection_and_account_data["account"],
        string_to_save="Test",
        gas_limit=0,
        gas_price=0,  # this should always pass, balance >= 0 always holds.
    )
    web3_connection = connection_and_account_data["web3_connection"]
    nonce = web3_connection.eth.getTransactionCount(
        connection_and_account_data["account"]
    )
    expected_tx = {
        "nonce": nonce,
        "to": connection_and_account_data["account"],
        "value": 0,
        "gas": 0,
        "gasPrice": 0,
        "data": Web3.toHex(text="Test"),
    }
    assert tx == expected_tx


def test_send_transaction_incorrect_private_key(connection_and_account_data, capfd):
    """
    Test behavior of send_transaction function if wrong private key is provided.
    """
    # create transaction
    tx = create_notarization_transaction(
        web3_connection=connection_and_account_data["web3_connection"],
        account=connection_and_account_data["account"],
        string_to_save="Test",
    )
    # wrong private key
    pk_wrong = "4f45b03c17892bd0ebfbc4f9ffbbfce86d641ccf30b2e9261854b5c83f00b206"

    # we want to test 2 things - if a system exit occurs and if the right message is displayed.
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        send_transaction(
            web3_connection=connection_and_account_data["web3_connection"],
            transaction=tx,
            private_key=pk_wrong,
        )
    out, err = capfd.readouterr()
    assert out == "The private key you specified is incorrect. Execution aborted.\n"
    assert pytest_wrapped_e.type == SystemExit


def test_send_transaction_invalid_private_key(connection_and_account_data, capfd):
    """
    Test behavior of send_transaction function if invalid private key is (non-hex bytes).
    """
    # create transaction
    tx = create_notarization_transaction(
        web3_connection=connection_and_account_data["web3_connection"],
        account=connection_and_account_data["account"],
        string_to_save="Test",
    )
    # invalid private key (added X to it)
    pk_wrong = "4f45b03c17892bX0asdebfbc4f9ffbbfce86d641ccf30b2e9261854b5c83f00b206"

    # we want to test 2 things - if a system exit occurs and if the right message is displayed.
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        send_transaction(
            web3_connection=connection_and_account_data["web3_connection"],
            transaction=tx,
            private_key=pk_wrong,
        )
    out, err = capfd.readouterr()
    assert "It may only contain [0-9a-fA-F] characters." in out
    assert pytest_wrapped_e.type == SystemExit


def test_send_transaction_short_private_key(connection_and_account_data, capfd):
    """
    Test behavior of send_transaction function if too short private key is provided.
    """
    # create transaction
    tx = create_notarization_transaction(
        web3_connection=connection_and_account_data["web3_connection"],
        account=connection_and_account_data["account"],
        string_to_save="Test",
    )
    # wrong private key
    pk_wrong = "a"

    # we want to test 2 things - if a system exit occurs and if the right message is displayed.
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        send_transaction(
            web3_connection=connection_and_account_data["web3_connection"],
            transaction=tx,
            private_key=pk_wrong,
        )
    out, err = capfd.readouterr()
    assert "The private key must be exactly 32 bytes long" in out
    assert pytest_wrapped_e.type == SystemExit
