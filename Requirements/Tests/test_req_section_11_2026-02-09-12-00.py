import pytest
import time
import os
import json
from niveristand.clientapi.realtimesystemmanager import RealTimeSystemManager
from niveristand.clientapi.dotnetinterop import dotnet_interop as ni_dot_net
from niveristand.errors import RunError, TimeoutError
from NationalInstruments.VeriStand.SystemStorage import ChannelReference, Alarm, SystemAlarm
from NationalInstruments.VeriStand.SystemStorage.DataLogger import DataLogger
from NationalInstruments.VeriStand.SystemStorage.Models import AlarmProperties
from NationalInstruments.VeriStand.SystemStorage.Models import AlarmCategory

# Function to connect to HIL
def connect_hil():
    rts = RealTimeSystemManager()
    sys_addr = 'localhost'
    ws = rts.GetWorkspace(sys_addr)
    ws.Connect()
    return ws, sys_addr

# Function to read project config
def read_project_config():
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'projectConfig.json')
    with open(config_path, 'r') as f:
        # Per instruction: load config hil_var = read_project_config()[3]
        # This implies read_project_config returns a list/tuple where the actual config is at index 3.
        # In a real scenario, this function would likely just return the loaded JSON dictionary.
        loaded_config = json.load(f)
        return [None, None, None, loaded_config]

class TestMaxDefrostActivatesOutsideAirOnly:
    def setup_method(self):
        self.ws, self.sys_addr = connect_hil()
        self.hil_var = read_project_config()[3]

    def teardown_method(self):
        if hasattr(self, 'ws') and self.ws.IsConnected:
            self.ws.Disconnect()

    def test_max_defrost_activates_outside_air_only(self):
        # 1. Set the vehicle operating mode to 'Running'.
        # Assuming 'Running' corresponds to a specific integer value, e.g., 1.
        # Signal path for VehicleMode (input to ECU from HIL)
        ChannelReference(self.hil_var["CAN_OUT"]["VehicleMode"]).value = 1
        time.sleep(0.5) # Allow time for the system to process the mode change

        # 2. Set the signal `MaxDefrostStatus` to 1 (On) to activate Max Defrost.
        # Signal path for MaxDefrostStatus (input to ECU from HIL)
        ChannelReference(self.hil_var["CAN_OUT"]["MaxDefrostStatus"]).value = 1
        time.sleep(2) # Wait for Max Defrost to activate and thermal system to react

        # 3. Observe the `AirRecirculationStatus` signal.
        # Signal path for AirRecirculationStatus (output from ECU to HIL)
        current_max_defrost_status = ChannelReference(self.hil_var["CAN_OUT"]["MaxDefrostStatus"]).value
        current_air_recirculation_status = ChannelReference(self.hil_var["CAN_IN"]["AirRecirculationStatus"]).value

        # Expected Outcome:
        # - `MaxDefrostStatus` == 1
        # - `AirRecirculationStatus` == 0
        assert current_max_defrost_status == 1, (
            f"Expected MaxDefrostStatus to be 1, but got {current_max_defrost_status}"
        )
        assert current_air_recirculation_status == 0, (
            f"Expected AirRecirculationStatus to be 0 (outside air only), but got {current_air_recirculation_status}"
        )