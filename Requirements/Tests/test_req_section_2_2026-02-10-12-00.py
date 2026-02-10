import pytest
import time
from niveristand.clientapi import realtimesequence as rtseq
from niveristand.clientapi import realtimestims as rtstims
from niveristand.clientapi import ChannelReference
from niveristand.clientapi import Workspace
from systemtests.core.decorators import sut_wait_until_true
from systemtests.core.utils import connect_hil, disconnect_hil, get_channel_value, set_channel_value, wait, read_project_config

@pytest.fixture(scope="module")
def hil_fixture():
    ws, sys_addr = connect_hil()
    hil_var = read_project_config()[3]
    yield hil_var
    disconnect_hil(ws)

@rtseq.RealTimeSequence
def test_hvac_actuator_final_position_status_feedback(hil_var):
    # Step 1: Command the HVAC Recirculation actuator to move to a new position.
    ChannelReference(hil_var["LIN_29_CCM"]["HVACAct1Cmd_ParamPosMode"]).value = 100
    wait(1)

    # Step 2: Command the HVAC Vent/Defrost/Floor actuator to move to a new position.
    ChannelReference(hil_var["LIN_29_CCM"]["HVACAct2Cmd_ParamPosMode"]).value = 150
    wait(1)

    # Step 3: Command the HVAC Heat Blend actuator to move to a new position.
    ChannelReference(hil_var["LIN_29_CCM"]["HVACAct3Cmd_ParamPosMode"]).value = 200
    wait(1)

    # Expected Outcome:
    # - LIN_HVACAct1Stat_CurrentPos == 100
    # - LIN_HVACAct2Stat_CurrentPos == 150
    # - LIN_HVACAct3Stat_CurrentPos == 200
    assert ChannelReference(hil_var["LIN_29_CCM"]["LIN_HVACAct1Stat_CurrentPos"]).value == 100
    assert ChannelReference(hil_var["LIN_29_CCM"]["LIN_HVACAct2Stat_CurrentPos"]).value == 150
    assert ChannelReference(hil_var["LIN_29_CCM"]["LIN_HVACAct3Stat_CurrentPos"]).value == 200