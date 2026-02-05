from ConnectionToHil.hil_modules import connect_hil, disconnect_hil, read_project_config, connect_to_veristand, check_if_already_connected
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait
from niveristand.legacy import NIVeriStand

import pytest
import json
import pathlib
import logging
import asyncio


# tests

def test_hil_connects():
    ws, sys_addr = connect_hil()
    try:
        assert ws is not None, "Workspace is None"
        assert isinstance(sys_addr, str) and len(sys_addr) > 0, "System address is invalid"
        asyncio.run(asyncio.sleep(3))
    except Exception as e:
        print(e)

    ws = NIVeriStand.Workspace2(sys_addr)
    assert ws.GetSystemState()["state"] == 1


def test_basic_can_communication():
    hil_var = read_project_config()[3]

    ChannelReference(hil_var["CAN_OUT"]["VehicleMode"]).value = 6
    ChannelReference(hil_var["CAN_OUT"]["ClimatePowerRequest"]).value = 1
    ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"]).value = 0
    ChannelReference(hil_var["CAN_OUT"]["ClimateAirDistRequest_Defrost"]).value = 0
    ChannelReference(hil_var["CAN_OUT"]["ClimateAirDistRequest_Floor"]).value = 1
    ChannelReference(hil_var["CAN_OUT"]["ClimateAirDistRequest_Vent"]).value = 1
    ChannelReference(hil_var["CAN_OUT"]["AirRecirculationRequest"]).value = 1
    ChannelReference(hil_var["CAN_OUT"]["HVACBlowerRequest"]).value = 1

    logging.debug("Waiting for 3 seconds...")
    asyncio.run(asyncio.sleep(3))

    assert ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"]).value == 0
    assert ChannelReference(hil_var["CAN_IN"]["HVACBlowerLevelStat_BlowerLevel"]).value == 1
    assert ChannelReference(hil_var["CAN_IN"]["ClimateAirDistStatus_Defrost"]).value == 0
    assert ChannelReference(hil_var["CAN_IN"]["ClimateAirDistStatus_Floor"]).value == 1
    assert ChannelReference(hil_var["CAN_IN"]["ClimateAirDistStatus_Vent"]).value == 1
    assert ChannelReference(hil_var["CAN_IN"]["AirRecirculationStatus"]).value == 1
    assert ChannelReference(hil_var["CAN_IN"]["ClimatePowerStatus"]).value == 1


def test_basic_lin_communication():
    hil_var = read_project_config()[3]

    ChannelReference(hil_var["LIN28"]["OUT"]["EAC_InvrtTemp"]).value = 81

    logging.debug("Waiting for 3 seconds...")
    asyncio.run(asyncio.sleep(3))
    assert ChannelReference(hil_var["CAN_IN"]["ChlrVlvPsnRqst"]).value >= 138
    assert ChannelReference(hil_var["CAN_IN"]["ChlrVlvPsnRqst"]).value <= 139


def test_hil_disconnects():
    sys_addr = read_project_config()[2]
    ws = NIVeriStand.Workspace2(sys_addr)
    disconnect_hil(ws, sys_addr)

    logging.debug("Asserting hil disconnected")
    assert ws.GetSystemState()["state"] == 0


# @pytest.fixture(scope="session")
# def config_dict():
#     logging.debug("Running config_dict")
#     cfg_path = pathlib.Path("projectConfig.json")
#     if not cfg_path.exists():
#         pytest.skip("Configuration file projectConfig.json not found")
#     try:
#         data = json.loads(cfg_path.read_text(encoding='utf-8'))
#     except json.JSONDecodeError as e:
#         pytest.skip(f"Configuration file projectConfig.json is not a valid JSON: {e}")

#     needed = ["projectpath", "Systemadress", "variables"]
#     for k in needed:
#         if k not in data:
#             pytest.skip(f"Configuration file projectConfig.json is missing required key: {k}")
#     if "CAN" not in hil_var:
# CAN.skip("Configuration file projectConfig.json is missing required key: variables->CAN")

#     return data

# @pytest.fixture(scope="session")
# def hil_session():
    # logging.debug("Running hil_session")

    # try:
    #     ws, sys_addr = connect_hil()
    # except Exception as e:
    #     pytest.skip(f"Failed to initialize HIL (connect_hil): {e}")

    # if ws is None or sys_addr is None:
    #     pytest.skip("Failed to initialize HIL (ws or sys_addr is None)")

    # wait(0.1)  # Allow some time for the system to stabilize

    # yield ws, sys_addr  # Provide the workspace and system address to tests

    # try:
    #     disconnect_hil(ws, sys_addr)
    # except Exception as e:
    #     print(f"Failed to disconnect HIL (disconnect_hil): {e}")
