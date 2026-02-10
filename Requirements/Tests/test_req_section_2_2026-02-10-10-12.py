from ConnectionToHil.hil_modules import connect_hil, disconnect_hil, read_project_config, connect_to_veristand, check_if_already_connected
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait
from niveristand.legacy import NIVeriStand

import pytest
import json
import pathlib
import logging
# The original template used asyncio, but the instructions explicitly state "Do NOT use asyncio."
# So, we will use wait(sec) instead as per instructions.
# import asyncio


# tests

def test_verify_hvac_actuator_position_feedback_to_ccm():
    ws, sys_addr = connect_hil()
    try:
        assert ws is not None, "Workspace is None"
        assert isinstance(sys_addr, str) and len(sys_addr) > 0, "System address is invalid"
        wait(3) # Initial wait for system stabilization
    except Exception as e:
        print(e)

    ws = NIVeriStand.Workspace2(sys_addr)
    assert ws.GetSystemState()["state"] == 1

    hil_var = read_project_config()[3]

    # 1. Command the HVAC Recirculation Actuator (corresponding to HVACAct1) to its fully closed position.
    ChannelReference(hil_var["LIN29"]["OUT"]["HVACAct1Cmd_ConfigEmRun"]).value = 0
    logging.debug("Commanded HVACAct1 (Recirculation) to fully closed (0)")

    # 2. Allow sufficient time for the actuator to reach its commanded position and for the status signal to be updated.
    wait(3)

    # 3. Command the HVAC Vent/Defrost/Floor Actuator (corresponding to HVACAct2) to its fully open (defrost) position.
    ChannelReference(hil_var["LIN29"]["OUT"]["HVACAct2Cmd_ConfigEmRun"]).value = 255
    logging.debug("Commanded HVACAct2 (Vent/Defrost/Floor) to fully open/defrost (255)")

    # 4. Allow sufficient time for the actuator to reach its commanded position and for the status signal to be updated.
    wait(3)

    # 5. Command the HVAC Heat Blend Actuator (corresponding to HVACAct3) to a specific intermediate position, e.g., 50% open.
    ChannelReference(hil_var["LIN29"]["OUT"]["HVACAct3Cmd_ConfigEmRun"]).value = 128
    logging.debug("Commanded HVACAct3 (Heat Blend) to 50% open (128)")

    # 6. Allow sufficient time for the actuator to reach its commanded position and for the status signal to be updated.
    wait(3)

    # Expected Outcome:
    # - LIN_HVACAct1Stat_CurrentPos == 0 (fully closed for Recirculation)
    # - LIN_HVACAct2Stat_CurrentPos == 255 (fully open/defrost for Vent/Defrost/Floor)
    # - LIN_HVACAct3Stat_CurrentPos == 128 (approx. 50% open for Heat Blend)

    actual_hvac_act1_pos = ChannelReference(hil_var["LIN29"]["IN"]["LIN_HVACAct1Stat_CurrentPos"]).value
    actual_hvac_act2_pos = ChannelReference(hil_var["LIN29"]["IN"]["LIN_HVACAct2Stat_CurrentPos"]).value
    actual_hvac_act3_pos = ChannelReference(hil_var["LIN29"]["IN"]["LIN_HVACAct3Stat_CurrentPos"]).value

    logging.debug(f"LIN_HVACAct1Stat_CurrentPos: {actual_hvac_act1_pos}")
    logging.debug(f"LIN_HVACAct2Stat_CurrentPos: {actual_hvac_act2_pos}")
    logging.debug(f"LIN_HVACAct3Stat_CurrentPos: {actual_hvac_act3_pos}")

    assert actual_hvac_act1_pos == 0, f"Expected LIN_HVACAct1Stat_CurrentPos to be 0, but got {actual_hvac_act1_pos}"
    assert actual_hvac_act2_pos == 255, f"Expected LIN_HVACAct2Stat_CurrentPos to be 255, but got {actual_hvac_act2_pos}"
    assert actual_hvac_act3_pos == 128, f"Expected LIN_HVACAct3Stat_CurrentPos to be 128, but got {actual_hvac_act3_pos}"

    disconnect_hil(ws, sys_addr)