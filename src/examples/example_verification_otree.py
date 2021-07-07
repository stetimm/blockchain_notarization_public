""" Example to show how verification of an oTree generated file would work. \n
NOTE: This is currently fairly specific to the oTree example. Much is hard-coded.
The purpose is to illustrate the general principle. """
# importing all necessary packages
import hashlib
import os
import sys

import pandas as pd

# importing all required modules, files and config data
sys.path.insert(0, os.path.abspath("src/notarization_code"))
from verification import verify_via_transaction
from utils import establish_infura_connection

otree_raw_data = pd.read_csv(sys.path[1] + "/example_file_otree.csv")

sys.path.insert(0, os.path.abspath("src"))
from blockchain_config import INFURA_URL

# Establish web3 connection via infura
web3_connection = establish_infura_connection(INFURA_URL)

# minimal data cleaning
relevant_data = otree_raw_data.copy()
relevant_data.columns = relevant_data.columns.str.replace(".", "_")


def build_verification_string(
    data, participant_code_column, time_started_column, input_data_columns
):
    """
    Takes dataframe as input and calculates the payload string to check.
    """
    input_data_listed = data[input_data_columns].to_numpy().tolist()
    data["input_data_generated"] = input_data_listed
    data["input_data_generated"] = data["input_data_generated"].astype(str)
    data["verification_string_without_hash"] = (
        "participant_code: "
        + data[participant_code_column]
        + " time_started: "
        + data[time_started_column]
        + " decisions: "
        + data["input_data_generated"]
    )
    data["hashes"] = data.apply(
        lambda row: hashlib.sha256(
            row.verification_string_without_hash.encode()
        ).hexdigest(),
        axis=1,
    )
    data["verification_string"] = (
        data["verification_string_without_hash"] + " - " + data["hashes"]
    )
    return data["verification_string"]


# Step 1: Take the data and calculate the verification string as a new column.
relevant_data["verification_string"] = build_verification_string(
    data=relevant_data,
    participant_code_column="participant_code",
    time_started_column="participant_time_started",
    input_data_columns=["player_decision_0", "player_decision_5", "player_decision_10"],
)

# Step 2: Look up if the verification string matches what is saved in the transaction specified
relevant_data["verified"] = relevant_data.apply(
    lambda row: verify_via_transaction(
        web3_connection=web3_connection,
        tx_hash=row.player_tx_hash,
        hash_value=row.verification_string,
    )["verified"],
    axis=1,
)

# Show which rows have been verified.
print(relevant_data["verified"])
