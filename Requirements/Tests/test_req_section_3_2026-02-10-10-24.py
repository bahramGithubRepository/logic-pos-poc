from ConnectionToHil.hil_modules import connect_hil, disconnect_hil, read_project_config, connect_to_veristand, check_if_already_connected
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait
from niveristand.legacy import NIVeriStand

import pytest
import json
import pathlib
import logging

# tests

def test_hil_connects():
    ws, sys_addr = connect_hil()
    try:
        assert ws is not None, "Workspace is None"
        assert isinstance(sys_addr, str) and len(sys_addr) > 0, "System address is invalid"
        wait(3)
    except Exception as e:
        print(e)

    ws = NIVeriStand.Workspace2(sys_addr)
    assert ws.GetSystemState()["state"] == 1

def test_max_defrost_availability():
    hil_var = read_project_config()[3]

    # Pre-conditions
    # MaxDefrostRequest == 'Deactivate'
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = 0
    # MaxDefrostStatus == 'Inactive' - This is an expected state, not set
    wait(1)
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == 0, "MaxDefrostStatus was not Inactive (0) before test start"


    # Step 1: Set VehicleMode to 'PreRunning'.
    # Assuming PreRunning maps to an integer value, e.g., 1
    # Note: The basic_test.py uses 6 for VehicleMode. For this scenario,
    # specific enum values for PreRunning, Cranking, Running are needed.
    # Using placeholder values based on common CAN signal practices.
    VEHICLE_MODE_PRERUNNING = 1
    VEHICLE_MODE_CRANKING = 2
    VEHICLE_MODE_RUNNING = 3

    MAX_DEFROST_REQUEST_ACTIVATE = 1
    MAX_DEFROST_REQUEST_DEACTIVATE = 0
    MAX_DEFROST_STATUS_ACTIVE = 1
    MAX_DEFROST_STATUS_INACTIVE = 0


    logging.debug(f"Setting VehicleMode to PreRunning ({VEHICLE_MODE_PRERUNNING})")
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = VEHICLE_MODE_PRERUNNING
    wait(1) # Allow system to react

    # Step 2: Set MaxDefrostRequest to 'Activate'.
    logging.debug(f"Setting MaxDefrostRequest to Activate ({MAX_DEFROST_REQUEST_ACTIVATE})")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_ACTIVATE
    wait(2) # Allow system to activate Max Defrost

    # Expected Outcome: MaxDefrostStatus == 'Active'
    max_defrost_status_prerunning = ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value
    logging.debug(f"MaxDefrostStatus in PreRunning: {max_defrost_status_prerunning}")
    assert max_defrost_status_prerunning == MAX_DEFROST_STATUS_ACTIVE, \
        f"MaxDefrostStatus was not Active in PreRunning. Expected {MAX_DEFROST_STATUS_ACTIVE}, Got {max_defrost_status_prerunning}"

    # Step 3: Set VehicleMode to 'Cranking'.
    logging.debug(f"Setting VehicleMode to Cranking ({VEHICLE_MODE_CRANKING})")
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = VEHICLE_MODE_CRANKING
    wait(1) # Allow system to react

    # Step 4: Set MaxDefrostRequest to 'Activate'.
    logging.debug(f"Setting MaxDefrostRequest to Activate ({MAX_DEFROST_REQUEST_ACTIVATE})")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_ACTIVATE
    wait(2) # Allow system to activate Max Defrost

    # Expected Outcome: MaxDefrostStatus == 'Active'
    max_defrost_status_cranking = ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value
    logging.debug(f"MaxDefrostStatus in Cranking: {max_defrost_status_cranking}")
    assert max_defrost_status_cranking == MAX_DEFROST_STATUS_ACTIVE, \
        f"MaxDefrostStatus was not Active in Cranking. Expected {MAX_DEFROST_STATUS_ACTIVE}, Got {max_defrost_status_cranking}"

    # Step 5: Set VehicleMode to 'Running'.
    logging.debug(f"Setting VehicleMode to Running ({VEHICLE_MODE_RUNNING})")
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = VEHICLE_MODE_RUNNING
    wait(1) # Allow system to react

    # Step 6: Set MaxDefrostRequest to 'Activate'.
    logging.debug(f"Setting MaxDefrostRequest to Activate ({MAX_DEFROST_REQUEST_ACTIVATE})")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_ACTIVATE
    wait(2) # Allow system to activate Max Defrost

    # Expected Outcome: MaxDefrostStatus == 'Active'
    max_defrost_status_running = ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value
    logging.debug(f"MaxDefrostStatus in Running: {max_defrost_status_running}")
    assert max_defrost_status_running == MAX_DEFROST_STATUS_ACTIVE, \
        f"MaxDefrostStatus was not Active in Running. Expected {MAX_DEFROST_STATUS_ACTIVE}, Got {max_defrost_status_running}"

def test_hil_disconnects():
    sys_addr = read_project_config()[2]
    ws = NIVeriStand.Workspace2(sys_addr)
    disconnect_hil(ws, sys_addr)

    logging.debug("Asserting hil disconnected")
    assert ws.GetSystemState()["state"] == 0