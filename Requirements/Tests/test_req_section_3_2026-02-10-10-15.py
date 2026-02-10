from ConnectionToHil.hil_modules import connect_hil, disconnect_hil, read_project_config
from niveristand.clientapi import ChannelReference
from niveristand.library import wait

import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Constants for VehicleMode
VEHICLE_MODE_PRERUNNING = 2
VEHICLE_MODE_CRANKING = 3
VEHICLE_MODE_RUNNING = 4

# Constants for MaxDefrostRequest/Status
MAX_DEFROST_REQUEST_ON = 1
MAX_DEFROST_REQUEST_OFF = 0
MAX_DEFROST_STATUS_ACTIVE = 1
MAX_DEFROST_STATUS_INACTIVE = 0

@pytest.fixture(scope="module")
def hil_setup():
    ws, sys_addr = connect_hil()
    hil_var = read_project_config()[3]
    yield ws, sys_addr, hil_var
    disconnect_hil(ws, sys_addr)

def test_max_defrost_availability_in_valid_vehicle_modes(hil_setup):
    ws, sys_addr, hil_var = hil_setup

    logging.info("Starting test: Max Defrost Function Availability in Valid Vehicle Modes")

    # Pre-conditions
    # MaxDefrostRequest should be 0
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_OFF
    # VehicleMode should be a neutral state (e.g., Parked or Off - assuming 0 for now as it's not specified)
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = 0
    wait(1) # Allow signals to settle

    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_INACTIVE, "Pre-condition failed: MaxDefrostStatus is not 0"
    logging.info("Pre-conditions met: MaxDefrostRequest and MaxDefrostStatus are 0.")

    # Test for PreRunning mode
    logging.info(f"Setting VehicleMode to PreRunning ({VEHICLE_MODE_PRERUNNING}).")
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = VEHICLE_MODE_PRERUNNING
    wait(2) # Wait for mode transition

    logging.info(f"Setting MaxDefrostRequest to ON ({MAX_DEFROST_REQUEST_ON}).")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_ON
    wait(3) # Wait for Max Defrost to activate

    logging.info(f"Checking MaxDefrostStatus for PreRunning mode. Expected: {MAX_DEFROST_STATUS_ACTIVE}, Actual: {ChannelReference(hil_var['CAN_IN']['MaxDefrostStatus']).value}")
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_ACTIVE, "MaxDefrostStatus did not activate in PreRunning mode."
    logging.info("Max Defrost activated successfully in PreRunning mode.")

    logging.info(f"Setting MaxDefrostRequest to OFF ({MAX_DEFROST_REQUEST_OFF}).")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_OFF
    wait(2)
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_INACTIVE, "MaxDefrostStatus did not deactivate after request in PreRunning mode."


    # Test for Cranking mode
    logging.info(f"Setting VehicleMode to Cranking ({VEHICLE_MODE_CRANKING}).")
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = VEHICLE_MODE_CRANKING
    wait(2) # Wait for mode transition

    logging.info(f"Setting MaxDefrostRequest to ON ({MAX_DEFROST_REQUEST_ON}).")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_ON
    wait(3) # Wait for Max Defrost to activate

    logging.info(f"Checking MaxDefrostStatus for Cranking mode. Expected: {MAX_DEFROST_STATUS_ACTIVE}, Actual: {ChannelReference(hil_var['CAN_IN']['MaxDefrostStatus']).value}")
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_ACTIVE, "MaxDefrostStatus did not activate in Cranking mode."
    logging.info("Max Defrost activated successfully in Cranking mode.")

    logging.info(f"Setting MaxDefrostRequest to OFF ({MAX_DEFROST_REQUEST_OFF}).")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_OFF
    wait(2)
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_INACTIVE, "MaxDefrostStatus did not deactivate after request in Cranking mode."


    # Test for Running mode
    logging.info(f"Setting VehicleMode to Running ({VEHICLE_MODE_RUNNING}).")
    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = VEHICLE_MODE_RUNNING
    wait(2) # Wait for mode transition

    logging.info(f"Setting MaxDefrostRequest to ON ({MAX_DEFROST_REQUEST_ON}).")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_ON
    wait(3) # Wait for Max Defrost to activate

    logging.info(f"Checking MaxDefrostStatus for Running mode. Expected: {MAX_DEFROST_STATUS_ACTIVE}, Actual: {ChannelReference(hil_var['CAN_IN']['MaxDefrostStatus']).value}")
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_ACTIVE, "MaxDefrostStatus did not activate in Running mode."
    logging.info("Max Defrost activated successfully in Running mode.")

    logging.info(f"Setting MaxDefrostRequest to OFF ({MAX_DEFROST_REQUEST_OFF}).")
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = MAX_DEFROST_REQUEST_OFF
    wait(2)
    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == MAX_DEFROST_STATUS_INACTIVE, "MaxDefrostStatus did not deactivate after request in Running mode."

    logging.info("Test completed successfully: Max Defrost function is available in all specified vehicle modes.")