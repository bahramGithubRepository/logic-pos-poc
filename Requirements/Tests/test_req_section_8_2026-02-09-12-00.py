from ConnectionToHil.hil_modules import connect_hil, disconnect_hil, read_project_config, connect_to_veristand, check_if_already_connected
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait
from niveristand.legacy import NIVeriStand

import pytest
import json
import pathlib
import logging
import time


# tests

def test_max_defrost_air_distribution():
    ws, sys_addr = connect_hil()
    hil_var = read_project_config()[3]

    # Pre-conditions
    # Vehicle is in "Running" mode. (Assuming 6 is the enum for "Running" based on basic_test.py)
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = 6
    # Max Defrost is currently deactivated
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = 0
    logging.debug("Setting pre-conditions: VehicleMode=Running, MaxDefrostRequest=0")
    wait(1) # Allow system to settle

    # Assert initial state
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == 0, \
        "Pre-condition failed: MaxDefrostStatus is not 0."
    assert ChannelReference(hil_var["CAN_IN"]["ClimateAirDistStatus_Defrost"]).value == 0, \
        "Pre-condition failed: ClimateAirDistStatus_Defrost is not 0."

    # Trigger: Activate Max Defrost
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = 1
    logging.debug("Trigger: MaxDefrostRequest set to 1 (Activate Max Defrost).")

    # Wait for system response
    logging.debug("Waiting for 3 seconds for system to react...")
    wait(3)

    # Expected Outcome
    # MaxDefrostStatus == 1
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == 1, \
        "Expected Outcome failed: MaxDefrostStatus is not 1 after activation."
    # ClimateAirDistStatus_Defrost == 1
    assert ChannelReference(hil_var["CAN_IN"]["ClimateAirDistStatus_Defrost"]).value == 1, \
        "Expected Outcome failed: ClimateAirDistStatus_Defrost is not 1 after Max Defrost activation."

    # Cleanup: Deactivate Max Defrost to return to a known state
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = 0
    logging.debug("Cleanup: MaxDefrostRequest set to 0 (Deactivate Max Defrost).")
    wait(1) # Allow system to settle

    # Note: disconnect_hil is handled by a separate test_hil_disconnects function
    # or a pytest fixture in the template, so it's not included here.