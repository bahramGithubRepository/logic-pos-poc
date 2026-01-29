import unittest
import time

# Mocked vehicle bus for demonstration purposes.
# In a real environment, this would be an interface to the vehicle's CAN bus.
class VehicleBus:
    def __init__(self):
        self._signals = {
            "ClimatePowerRequest": 0,
            "MaxDefrostRequest": 0,
            "MaxDefrostStatus": 0,
            "CabHeatManStatus": 5, # Default to a mid-range value
            "HVACBlowerLevelStat_BlowerLevel": 10, # Default to a mid-range value
            "ACStatus": 0,
            "AirRecirculationStatus": 1, # Default to recirculation on
            "ClimateAirDistStatus_Defrost": 0,
            "ClimateAirDistStatus_Floor": 15, # Default to floor
            "ClimateAirDistStatus_Vent": 0,
        }

    def set(self, signal, value):
        print(f"BUS.SET: {signal} = {value}")
        self._signals[signal] = value
        # Simulate ECU response to the trigger
        if signal == "MaxDefrostRequest" and value == 1:
            self._activate_max_defrost()

    def get(self, signal):
        value = self._signals.get(signal, 0)
        print(f"BUS.GET: {signal} -> {value}")
        return value

    def _activate_max_defrost(self):
        """Simulates the Thermal System's response to MaxDefrostRequest."""
        time.sleep(0.1) # Simulate processing delay
        self._signals["MaxDefrostStatus"] = 1
        self._signals["CabHeatManStatus"] = 15 # Max heat
        self._signals["HVACBlowerLevelStat_BlowerLevel"] = 31 # Max blower speed
        self._signals["ACStatus"] = 1 # AC On
        self._signals["AirRecirculationStatus"] = 0 # Fresh air
        self._signals["ClimateAirDistStatus_Defrost"] = 15 # 100% to defrost
        self._signals["ClimateAirDistStatus_Floor"] = 0
        self._signals["ClimateAirDistStatus_Vent"] = 0

# Mocked environment setup functions
def set_vehicle_mode(mode):
    print(f"ENV.SET: VehicleMode = {mode}")

def set_ambient_temp(temp):
    print(f"ENV.SET: AmbientTemp = {temp}°C")

vehicle_bus = VehicleBus()

class TestMaxDefrost(unittest.TestCase):

    def setUp(self):
        """
        Establishes the preconditions for the test case based on the scenario.
        """
        print("\n--- Setting Up Preconditions ---")
        # Precondition: VehicleMode = Running
        # Context from Tech Report EMD_MaxDefrost.pdf (ID: 53bcab3c-8910-4cf2-a6e1-a02971fc5ed2),
        # which states 'Running' is a valid mode for Max Defrost activation.
        set_vehicle_mode('Running')

        # Precondition: AmbientTemp = 15 degC
        # Context from Tech Report EMD_MaxDefrost.pdf, A/C activation is required
        # for dehumidification and is disabled in low ambient temperatures. 15°C ensures it can activate.
        set_ambient_temp(15)

        # Precondition: ClimateCtrlOn = 1 (On)
        # Signal 'ClimatePowerRequest' found in tech report (ID: ccb2dd6c-9b2f-49f0-b1fa-0047154732bf).
        vehicle_bus.set('ClimatePowerRequest', 1)

        # Precondition: MaxDefrostStatus = 0 (Off)
        # This is ensured by setting the request signal to 0 and verifying the status.
        vehicle_bus.set('MaxDefrostRequest', 0)
        
        # Allow a brief moment for the system to stabilize in its initial state.
        time.sleep(0.5)
        self.assertEqual(vehicle_bus.get('MaxDefrostStatus'), 0)
        print("--- Preconditions Met ---")


    def test_max_defrost_activation_and_verification(self):
        """
        This test verifies that when Max Defrost is activated, the Thermal System
        correctly commands all related outputs to their expected states as defined
        in the requirements.
        """
        # Trigger: Activate Max Defrost via the HMI request.
        # Requirement ID for activation request: f6d257d1-17d8-47b3-ab64-e8bcd14959cc.
        # The user's 'HMI_MaxDefrostRequest' maps to the CAN signal 'MaxDefrostRequest'.
        print("\n--- Applying Trigger: Activating Max Defrost ---")
        vehicle_bus.set('MaxDefrostRequest', 1)

        # Wait 500ms for the Thermal System to process the request as per the test scenario.
        time.sleep(0.5)

        # --- Verification Step ---
        print("\n--- Verifying System Outputs ---")

        # Expected Outcome 1: MaxDefrostStatus = 1 (On)
        # Requirement ID: c436b2a7-2ca3-4a87-a3a2-a04f4765b867
        # Signal Name: MaxDefrostStatus
        max_defrost_status = vehicle_bus.get('MaxDefrostStatus')
        self.assertEqual(max_defrost_status, 1, f"FAIL: MaxDefrostStatus - Expected 1 (On), Got {max_defrost_status}")
        print(f"PASS: MaxDefrostStatus is {max_defrost_status} (On)")

        # Expected Outcome 2: CabHeatManStatus = Max (mapped to 15)
        # Requirement ID: 77509225-072f-43a5-a4bf-68811dfe57ef
        # Signal Name: CabHeatManStatus, where the database indicates a max value of 15.
        cab_heat_status = vehicle_bus.get('CabHeatManStatus')
        self.assertEqual(cab_heat_status, 15, f"FAIL: CabHeatManStatus - Expected 15 (Max), Got {cab_heat_status}")
        print(f"PASS: CabHeatManStatus is {cab_heat_status} (Max)")

        # Expected Outcome 3: BlowerSpeedRequest = 100% (mapped to 31)
        # Requirement ID: c436b2a7-2ca3-4a87-a3a2-a04f4765b867
        # Signal Name: HVACBlowerLevelStat_BlowerLevel, where the database indicates a max value of 31 for 100%.
        blower_speed_status = vehicle_bus.get('HVACBlowerLevelStat_BlowerLevel')
        self.assertEqual(blower_speed_status, 31, f"FAIL: Blower Speed - Expected 31 (100%), Got {blower_speed_status}")
        print(f"PASS: Blower Speed is {blower_speed_status} (100%)")

        # Expected Outcome 4: AC_Request = 1 (On)
        # Requirement ID: c436b2a7-2ca3-4a87-a3a2-a04f4765b867
        # Signal Name: ACStatus. This is the feedback signal for the AC state.
        ac_status = vehicle_bus.get('ACStatus')
        self.assertEqual(ac_status, 1, f"FAIL: ACStatus - Expected 1 (On), Got {ac_status}")
        print(f"PASS: ACStatus is {ac_status} (On)")

        # Expected Outcome 5: RecirculationRequest = 0 (Fresh Air)
        # Requirement ID: c436b2a7-2ca3-4a87-a3a2-a04f4765b867
        # Signal Name: AirRecirculationStatus, where 0 corresponds to Fresh Air.
        recirc_status = vehicle_bus.get('AirRecirculationStatus')
        self.assertEqual(recirc_status, 0, f"FAIL: AirRecirculationStatus - Expected 0 (Fresh Air), Got {recirc_status}")
        print(f"PASS: AirRecirculationStatus is {recirc_status} (Fresh Air)")

        # Expected Outcome 6: Air Distribution Flaps set to 100% Defrost
        # Requirement ID: 08d0345a-ac1c-4a0f-8332-e19e047ebc6c
        # The flap positions are verified by checking the three distribution status signals.
        # Max value of 15 corresponds to 100% airflow.
        air_dist_defrost = vehicle_bus.get('ClimateAirDistStatus_Defrost')
        air_dist_floor = vehicle_bus.get('ClimateAirDistStatus_Floor')
        air_dist_vent = vehicle_bus.get('ClimateAirDistStatus_Vent')

        self.assertEqual(air_dist_defrost, 15, f"FAIL: Defrost Flap - Expected 15 (100%), Got {air_dist_defrost}")
        print(f"PASS: Defrost Flap Status is {air_dist_defrost} (100%)")
        self.assertEqual(air_dist_floor, 0, f"FAIL: Foot Flap - Expected 0 (Closed), Got {air_dist_floor}")
        print(f"PASS: Foot Flap Status is {air_dist_floor} (Closed)")
        self.assertEqual(air_dist_vent, 0, f"FAIL: Center Vent Flap - Expected 0 (Closed), Got {air_dist_vent}")
        print(f"PASS: Center Vent Flap Status is {air_dist_vent} (Closed)")

    def tearDown(self):
        """
        Cleans up the state after the test is complete.
        """
        print("\n--- Tearing Down Test ---")
        # Deactivate Max Defrost to return the system to a neutral state.
        vehicle_bus.set('MaxDefrostRequest', 0)
        time.sleep(0.5)
        self.assertEqual(vehicle_bus.get('MaxDefrostStatus'), 0)
        print("--- Teardown Complete ---")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
