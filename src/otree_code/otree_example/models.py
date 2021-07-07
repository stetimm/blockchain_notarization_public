import hashlib
import os
import sys

from otree.api import BaseConstants
from otree.api import BaseGroup
from otree.api import BasePlayer
from otree.api import BaseSubsession
from otree.api import Currency as c
from otree.api import currency_range
from otree.api import models
from otree.api import widgets

sys.path.insert(0, os.path.abspath("../notarization_code"))
from notarization import (
    create_notarization_transaction,
    send_transaction,
)
from utils import (
    create_transaction_etherscan_link,
    establish_infura_connection,
)

sys.path.insert(0, os.path.abspath(".."))
from blockchain_config import INFURA_URL, ACCOUNT, PK

author = "Stefan Timmermann"

doc = """
Simple multiple price list (MPL) style elicitation of an indifference point.
Code heavily inspired by MPL implementation of Felix Holzmeister: https://github.com/felixholzmeister/mpl
Holzmeister, F. (2017). oTree: Ready-Made Apps for Risk Preference Elicitation Methods, Journal of Behavioral and Experimental Finance 16, 33-38.
"""


class Constants(BaseConstants):
    name_in_url = "indiff_mpl"
    players_per_group = None
    payoff_charity = 150
    # self_payments = [n*5 for n in range(0, 31)] # the actual value
    self_payments = [n * 5 for n in range(0, 3)]  # the one used for testing
    decisions = ["decision_" + str(j) for j in self_payments]
    num_rounds = 1
    blockchain_notarization = True  # set to True to enable notarization


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:

            n = len(Constants.self_payments)
            for p in self.get_players():
                # create list corresponding to form_field variables including all decisions
                form_fields = ["decision_" + str(k) for k in Constants.self_payments]

                # create list of decisions
                p.participant.vars["mpl_decisions"] = form_fields

                # initiate list for decisions made
                p.participant.vars["mpl_decisions_made"] = [
                    None for j in range(1, n + 1)
                ]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # add model fields to class player

    for j in Constants.self_payments:
        # locals()['indiff_point_' + str(j)] = make_binary_choice_field(str(j))
        locals()["decision_" + str(j)] = models.StringField()
    del j  # do this because otherwise you get NonModelFieldAttr: Player has attribute "j", which is not a model field, and will therefore not be saved to the database.

    tx_hash = models.StringField()  # transaction hash of the placed transaction

    def notarize_player_input(self):
        """Function to notarize the input of the player.
        Try-except is there to ensure the app does not get stuck if there is an error when sending stuff to blockchain.
        """
        # the data the participant put in, as one list
        input_data = str(self.participant.vars["mpl_decisions_made"])
        # payload is the string to be saved in blockchain transaction
        payload = (
            "participant_code: "
            + str(self.participant.code)
            + " time_started: "
            + str(self.participant.time_started)
            + " decisions: "
            + input_data
        )
        # hash the payload
        payload_hash = str(hashlib.sha256(payload.encode()).hexdigest())
        try:
            tx_hash_to_store = notarize(" - ".join([payload, payload_hash]))
            self.tx_hash = tx_hash_to_store
        # if any exceptions are raised, just store the following as tx_hash:
        except:
            self.tx_hash = "Notarization failed. Please review logs."


# just giving this a shot
def notarize(string_to_save):
    """Function to do notarizatin within oTree app.

    Args:
        string_to_save (string): The string to save in the transaction. \n

    Returns:
        string: The tx_hash of the transaction where the hash has been saved. \n
    """

    web3_connection = establish_infura_connection(INFURA_URL)
    account = ACCOUNT
    private_key = PK
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
    return tx_hash
