import unittest
import time

# Assume the existence of a TestAutomationFramework with the following methods:
# - set_signal(signal_name, value): Sets the value of a signal.
# - get_signal(signal_name): Gets the current value of a signal.
# - check_condition(signal_name, expected_value, timeout): Checks if a signal reaches the expected value within a timeout.
# - start_test_case(name, description): Starts a new test case.
# - log_step(description): Logs a test step.

class TestMaxDefrostInitialState(unittest.TestCase):

    def setUp(self):
        """
        Initializes the TestAutomationFramework.
        This method is called before each test function.
        """
        self.framework = TestAutomationFramework()
        # It is assumed that the framework is connected to the vehicle/HIL setup.

    def test_max_defrost_activation_and_initial_state(self):
        """
        Test Name: Max Defrost Activation and Initial System State
        Description: Verifies that when Max Defrost is activated, the Thermal System correctly
                     commands all related components to their initial default states for
                     maximum defrost performance.
        """
        self.framework.start_test_case(
            name="Max Defrost Activation and Initial System State",
            description="Verifies the initial commanded state upon Max Defrost activation."
        )

        # --- Pre-conditions Setup ---
        # Citing: Test Scenario Description
        self.framework.log_step("Step 1: Establishing and verifying all pre-conditions.")

        # Set Vehicle power mode to Running
        self.framework.set_signal("DI_vehicleMode", 2) # Assuming 2 = Running

        # Set Ambient Temperature to 10°C to allow for A/C compressor activation
        self.framework.set_signal("AmbientTemp", 10)

        # Set Climate Control system to ON
        self.framework.set_signal("ClimatePowerRequest", 1)
        self.assertTrue(self.framework.check_condition("ClimatePowerStatus", 1, timeout=2), "Climate Control system should be ON")

        # Set initial climate settings
        self.framework.set_signal("MaxDefrostRequest", 0)
        self.framework.set_signal("AirRecirculationRequest", 1) # Recirculation On
        self.framework.set_signal("HVACBlowerRequest", 16) # Approx 50% (Range 0-31)
        self.framework.set_signal("CabHeatManReq_Driver", 22) # 22°C
        self.framework.set_signal("ACRequest", 0) # AC Off
        # Set Air Distribution to Vent Mode
        self.framework.set_signal("ClimateAirDistRequest_Vent", 15) # 100% Vent
        self.framework.set_signal("ClimateAirDistRequest_Defrost", 0)
        self.framework.set_signal("ClimateAirDistRequest_Floor", 0)

        # Verify initial states
        self.assertTrue(self.framework.check_condition("MaxDefrostStatus", 0, timeout=2), "MaxDefrostStatus should be 0 (Off)")
        self.assertTrue(self.framework.check_condition("AirRecirculationStatus", 1, timeout=2), "AirRecirculationStatus should be 1 (On)")
        self.assertTrue(self.framework.check_condition("ACStatus", 0, timeout=2), "ACStatus should be 0 (Off)")

        time.sleep(1) # Allow settings to stabilize

        # --- Trigger ---
        # Citing Requirement: Max Defrost Activation by Soft Button (ID: b66e5565-4ebf-4cbe-8820-70022dd5d737)
        self.framework.log_step("Step 2: Sending the Trigger command to activate Max Defrost.")
        self.framework.set_signal("MaxDefrostRequest", 1) # Press Max Defrost button

        # --- Verification ---
        # Citing: Expected Outcome from Test Scenario Description
        self.framework.log_step("Step 3: Monitoring the system's output signals for 5 seconds.")

        # Citing Requirement: Max Defrost Activation by Soft Button (ID: b66e5565-4ebf-4cbe-8820-70022dd5d737)
        self.assertTrue(self.framework.check_condition("MaxDefrostStatus", 1, timeout=5), "MaxDefrostStatus should be 1 (On)")

        # Citing Requirement: Max Defrost Activation - Manual Recirculation Off (ID: bd00fbe0-d890-4077-808e-8635c9ea3de6)
        self.assertTrue(self.framework.check_condition("AirRecirculationStatus", 0, timeout=5), "AirRecirculationStatus should be 0 (Off/Fresh Air)")

        # Citing Requirement: Max Defrost Activation - Blower Speed Setting (ID: 3a718b03-d7c5-4ad7-8b03-ed2c5ae1b8c9)
        # Note: Blower speed may ramp up, so we check the final state.
        self.assertTrue(self.framework.check_condition("HVACBlowerLevelStat_BlowerLevel", 31, timeout=5), "BlowerSpeedSetting should be 31 (100%)")

        # Citing Requirement: Max Defrost Activation - Maximum Heat Level Setting (ID: 77509225-072f-43a5-a4bf-68811dfe57ef)
        self.assertTrue(self.framework.check_condition("CabHeatStatus_Driver", 32, timeout=5), "TemperatureSetting should be 32°C (Max Heat)")

        # Citing Requirement: Max Defrost Activation - AC (ID: c436b2a7-2ca3-4a87-a3a2-a04f4765b867)
        self.assertTrue(self.framework.check_condition("ACStatus", 1, timeout=5), "AC_RequestStatus should be 1 (Enabled)")

        # Citing Requirement: Max Defrost Activation - Air Distribution Defrost Mode Setting (ID: 08d0345a-ac1c-4a0f-8332-e19e047ebc6c)
        # Verifies air distribution is 100% to Defrost, which corresponds to AirDist_Actuator_Rotation_Cmd = 0% in the scenario.
        self.assertTrue(self.framework.check_condition("ClimateAirDistStatus_Defrost", 15, timeout=5), "AirDist should be 100% Defrost")
        self.assertTrue(self.framework.check_condition("ClimateAirDistStatus_Floor", 0, timeout=5), "AirDist to Foot should be 0%")
        self.assertTrue(self.framework.check_condition("ClimateAirDistStatus_Vent", 0, timeout=5), "AirDist to Center Vent should be 0%")

        # Final physical state verification after a delay for actuators to move.
        self.framework.log_step("Step 4: Verifying physical flap positions after actuator movement.")
        time.sleep(3) # Wait for actuators to reach their final positions.
        
        # We verify the actuator position directly. As seen in the previous test, 0x00 position corresponds to 100% defrost.
        # This confirms "AirDist_Actuator_Rotation_Cmd = 0 (%)" and "Flap_Defrost_Position = 100 (%)".
        self.assertAlmostEqual(self.framework.get_signal("HVACAct1Stat_CurrentPos"), 0, delta=5, msg="Defrost Flap Position should be at 0 (100% Defrost)")


if __name__ == '__main__':
    unittest.main()


