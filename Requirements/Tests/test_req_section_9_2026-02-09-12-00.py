from ConnectionToHil.hil_modules import connect_hil, disconnect_hil, read_project_config, connect_to_veristand, check_if_already_connected
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait
from niveristand.legacy import NIVeriStand

import pytest
import json
import pathlib
import logging
# Removed asyncio in favor of niveristand.library.wait as per instructions

# tests

def test_hil_connects():
    ws, sys_addr = connect_hil()
    try:
        assert ws is not None, "Workspace is None"
        assert isinstance(sys_addr, str) and len(sys_addr) > 0, "System address is invalid"
        wait(3) # Replaced asyncio.run(asyncio.sleep(3))
    except Exception as e:
        print(e)

    ws = NIVeriStand.Workspace2(sys_addr)
    assert ws.GetSystemState()["state"] == 1


def test_thermal_system_requests_max_heating_during_max_defrost_activation():
    ws, sys_addr = connect_hil()
    hil_var = read_project_config()[3]

    # Pre-conditions (Assuming VehicleMode = 6 'Running' from template for Max Defrost activation)
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = 6
    wait(1) # Allow vehicle mode to settle

    # Trigger: Max Defrost is activated.
    # Step 1: Set MaxDefrostStatus to 1.
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostStatus"]).value = 1
    logging.debug("Waiting for 3 seconds...")
    wait(3)

    # Expected Outcome: CabHeatManStatus == 15
    assert ChannelReference(hil_var["CAN_IN"]["CabHeatManStatus"]).value == 15
    
    # Clean up: Deactivate Max Defrost Status
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostStatus"]).value = 0
    wait(1)


def test_hil_disconnects():
    sys_addr = read_project_config()[2]
    ws = NIVeriStand.Workspace2(sys_addr)
    disconnect_hil(ws, sys_addr)

    logging.debug("Asserting hil disconnected")
    assert ws.GetSystemState()["state"] == 0