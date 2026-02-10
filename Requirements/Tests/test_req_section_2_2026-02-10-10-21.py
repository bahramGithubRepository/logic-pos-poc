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

def test_hvac_actuator_position_feedback():
    ws, sys_addr = connect_hil()
    try:
        assert ws is not None, "Workspace is None"
        assert isinstance(sys_addr, str) and len(sys_addr) > 0, "System address is invalid"
        # Removed asyncio.run(asyncio.sleep(3))
    except Exception as e:
        print(e)

    ws = NIVeriStand.Workspace2(sys_addr)
    assert ws.GetSystemState()["state"] == 1

    hil_var = read_project_config()[3]

    # Steps:
    # 1. Command LIN_HVACAct1Stat_CurrentPos (Recirculation actuator) to a specific position value, for example, 128.
    ChannelReference(hil_var["LIN29"]["OUT"]["LIN_HVACAct1Stat_CurrentPos"]).value = 128
    logging.debug("Commanded LIN_HVACAct1Stat_CurrentPos to 128")

    # 2. Command LIN_HVACAct2Stat_CurrentPos (Vent/Defrost/Floor actuator) to a specific position value, for example, 64.
    ChannelReference(hil_var["LIN29"]["OUT"]["LIN_HVACAct2Stat_CurrentPos"]).value = 64
    logging.debug("Commanded LIN_HVACAct2Stat_CurrentPos to 64")

    # 3. Command LIN_HVACAct3Stat_CurrentPos (Heat Blend actuator) to a specific position value, for example, 192.
    ChannelReference(hil_var["LIN29"]["OUT"]["LIN_HVACAct3Stat_CurrentPos"]).value = 192
    logging.debug("Commanded LIN_HVACAct3Stat_CurrentPos to 192")

    # 4. Monitor the feedback signals from the HVAC to the CCM.
    logging.debug("Waiting for 3 seconds to allow signals to propagate...")
    wait(3)

    # Expected Outcome:
    # - LIN_HVACAct1Stat_CurrentPos == 128
    assert ChannelReference(hil_var["LIN29"]["OUT"]["LIN_HVACAct1Stat_CurrentPos"]).value == 128
    logging.debug("Assertion passed: LIN_HVACAct1Stat_CurrentPos == 128")

    # - LIN_HVACAct2Stat_CurrentPos == 64
    assert ChannelReference(hil_var["LIN29"]["OUT"]["LIN_HVACAct2Stat_CurrentPos"]).value == 64
    logging.debug("Assertion passed: LIN_HVACAct2Stat_CurrentPos == 64")

    # - LIN_HVACAct3Stat_CurrentPos == 192
    assert ChannelReference(hil_var["LIN29"]["OUT"]["LIN_HVACAct3Stat_CurrentPos"]).value == 192
    logging.debug("Assertion passed: LIN_HVACAct3Stat_CurrentPos == 192")

    disconnect_hil(ws, sys_addr)
    logging.debug("Disconnected from HIL system.")