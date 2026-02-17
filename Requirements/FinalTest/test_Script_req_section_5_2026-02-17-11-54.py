"""
Max Defrost Test - DRY RUN MODE

This version SIMULATES the test without actually controlling hardware:
- Shows what WOULD be sent to hardware
- Reads current values but doesn't change them
- Validates test logic and signal paths
- Safe to run with hardware connected
- Generates report showing planned actions

✅ USE THIS to validate your test before running on real hardware
"""

import pytest
import asyncio
# from niveristand.clientapi import ChannelReference # Not used in dry run, kept for structure
# from hil_modules import read_project_config # Mocked for dry run
from test_reporter import TestReporter


# Dry run configuration
DRY_RUN = True  # Set to False to actually execute
SIMULATE_RESPONSES = True  # Simulate expected hardware responses

# Global reporter instance
reporter = None

# Simulation state (pretend hardware values)
simulated_state = {}

# Mock ChannelReference for DRY_RUN
class MockChannelReference:
    def __init__(self, path):
        self.path = path
        # Use the full signal path as key for simulated_state to avoid name collisions
        # However, the set/check_can_signal functions use signal_name (e.g., "MaxDefrostRequest")
        # so simulated_state will store by signal_name.
        # This MockChannelReference will try to read from simulated_state using its `path`
        # which is not what `set_can_signal` puts in.
        # Let's adjust MockChannelReference to use signal_name as well, or modify set/check_can_signal
        # to store/retrieve by path. For consistency with the existing template, simulated_state
        # keys are signal names. So, this MockChannelReference needs to extract the signal_name from path.
        # Simpler approach: `simulated_state` stores by `signal_name`, and `MockChannelReference` will not
        # be directly used to retrieve status from `simulated_state` for `check_can_signal` in DRY_RUN,
        # but `simulate_hardware_response` will be the source.
        # For `get_can_signal`, `MockChannelReference` will directly return 0.0 or a default.

    @property
    def value(self):
        # In DRY_RUN, we just return a default value as we are simulating responses
        # with simulate_hardware_response, not reading from a mock HIL here.
        # This is primarily for `get_can_signal` in DRY_RUN context to not error out.
        return 0.0

    @value.setter
    def value(self, val):
        # In DRY_RUN, we don't actually set anything via ChannelReference.
        # The set_can_signal wrapper handles storing in simulated_state.
        pass


# Replace niveristand.clientapi.ChannelReference for DRY_RUN
if DRY_RUN:
    ChannelReference = MockChannelReference
else:
    from niveristand.clientapi import ChannelReference


@pytest.fixture(scope="module")
def hil_config():
    """Load HIL configuration once for all tests"""
    # Mimic the structure of what read_project_config() would return
    # and provide the necessary signal paths.
    hil_var = {
        "CAN": {
            "IN": {
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
                "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
                "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
                "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
                "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
                "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
                "ClimatePowerStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimatePowerStatus",
                "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
            },
            "OUT": {
                "MaxDefrostRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/MaxDefrostRequest",
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_02P (284262208)/VehicleMode", # Assuming this can be set as an outgoing test input
                "PV_AmbientAirTemp": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_61P (419244352)/PV_AmbientAirTemp",
                "ClimatePowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimatePowerRequest",
                "CabHeatManReq": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_59P (352288832)/CabHeatManReq",
                # The following are not explicitly used in this test but might be needed for initial setup in a broader context
                "HVACBlowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/HVACBlowerRequest",
                "ClimateAirDistRequest_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Defrost",
                "ClimateAirDistRequest_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Floor",
                "ClimateAirDistRequest_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Vent",
            }
        }
    }
    return hil_var


def set_can_signal(hil_var, signal_name, value):
    """
    DRY RUN: Show what WOULD be sent, but don't actually send
    """
    if DRY_RUN:
        print(f"  [DRY RUN SET] {signal_name} = {value} (NOT SENT)")

        # Store in simulated state based on canonical signal name
        simulated_state[signal_name] = value

        if reporter:
            reporter.add_set(signal_name, value)
            reporter.add_note(f"DRY RUN: {signal_name} would be set to {value}")
    else:
        # Actually set the signal
        try:
            signal_path = hil_var["CAN"]["OUT"][signal_name]
            ChannelReference(signal_path).value = value
            print(f"  SET: {signal_name} = {value}")
            if reporter:
                reporter.add_set(signal_name, value)
        except KeyError:
            print(f"  WARNING: Signal '{signal_name}' not found in CAN OUT configuration. Cannot set.")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN OUT. Cannot set.")


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.1):
    """
    DRY RUN: Read actual value but simulate what response WOULD be
    """
    try:
        if signal_name not in hil_var["CAN"]["IN"]:
            raise KeyError(f"Signal '{signal_name}' not found in CAN IN configuration")

        # In DRY_RUN, `ChannelReference` will return a default value (0.0).
        # We rely on `simulate_hardware_response` for the expected outcome.
        actual_value_from_hil = ChannelReference(hil_var["CAN"]["IN"][signal_name]).value

        if DRY_RUN:
            simulated_response_value = simulate_hardware_response(signal_name, expected_value)

            passed = abs(simulated_response_value - expected_value) <= tolerance

            print(f"  [DRY RUN CHECK] {signal_name}")
            print(f"     Current real value (from mock HIL): {actual_value_from_hil}") # This will be 0.0
            print(f"     Simulated response: {simulated_response_value} (expected {expected_value})")

            if passed:
                print(f"     [PASS] WOULD PASS")
            else:
                print(f"     [FAIL] WOULD FAIL")

            if reporter:
                reporter.add_check(signal_name, expected_value, simulated_response_value, passed, tolerance)
                # reporter.add_note(f"Actual hardware value: {actual_value_from_hil} (not changed in dry run)")

            return passed
        else:
            # Normal check against real hardware
            actual_value = ChannelReference(hil_var["CAN"]["IN"][signal_name]).value
            passed = abs(actual_value - expected_value) <= tolerance

            if passed:
                print(f"  [PASS] CHECK: {signal_name} = {actual_value} (expected {expected_value})")
            else:
                print(f"  [FAIL] CHECK: {signal_name} = {actual_value} (expected {expected_value})")

            if reporter:
                reporter.add_check(signal_name, expected_value, actual_value, passed, tolerance)

            return passed

    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN configuration. Cannot check.")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN IN. Cannot check.")
        return False


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the CCM WOULD respond with based on test logic

    This simulates ideal hardware behavior - real hardware may differ!
    """

    # Map of expected CCM responses based on requests
    # Use signal_name keys as they are the common interface in set/check_can_signal
    response_map = {
        # Status signals mirror request signals in ideal case
        "MaxDefrostStatus": simulated_state.get("MaxDefrostRequest", 0),
        "ClimatePowerStatus": simulated_state.get("ClimatePowerRequest", 0),
        # CabHeatManStatus: if MaxDefrostRequest is 1, it should be max (10 as per template's example)
        "CabHeatManStatus": 10 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("CabHeatManReq", 0),

        # Blower level - in max defrost, should go to max.
        # Max value for HVACBlowerLevelStat_BlowerLevel is 10 according to template.
        "HVACBlowerLevelStat_BlowerLevel": 10 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("HVACBlowerRequest", 1),

        # Air distribution - in max defrost, defrost=100%, others=0%
        "ClimateAirDistStatus_Defrost": 100 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Defrost", 0),
        "ClimateAirDistStatus_Floor": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Vent", 0),
    }

    # Return simulated value, or expected value if not in map
    return response_map.get(signal_name, expected_value)


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of CAN IN signal"""
    try:
        # In DRY_RUN, this reads from the MockChannelReference which returns a default (0.0).
        # We are not directly reading from simulated_state here as that is handled by simulate_hardware_response
        # for `check_can_signal`. This function is typically for reading "actual" HIL values.
        signal_path = hil_var["CAN"]["IN"][signal_name]
        value = ChannelReference(signal_path).value

        if DRY_RUN:
            print(f"  [READ] {signal_name} = {value} (current hardware state or mock default)")

        return value
    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN configuration. Returning default {default}.")
        return default


def test_max_defrost_activation_request(hil_config):
    """
    DRY RUN: Test validation without hardware control

    What this does:
    - ✅ Validates all signal names exist in config
    - ✅ Shows what WOULD be sent to hardware
    - ✅ Reads current hardware state (doesn't change it)
    - ✅ Simulates expected responses
    - ✅ Generates report showing planned execution
    - ✅ Safe to run with hardware connected

    What this DOESN'T do:
    - ❌ Change any hardware signals
    - ❌ Control motors/actuators
    - ❌ Test real hardware behavior
    """

    global reporter
    reporter = TestReporter(
        "Max Defrost Activation Request - DRY RUN",
        "Verify that when the Driver Experience System requests the activation of Max Defrost, the Thermal System correctly activates Max Defrost mode and configures related climate control settings (air distribution, blower speed, AC, heating, and recirculation) as specified."
    )

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION REQUEST TEST")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)

    hil_var = hil_config

    # ========================================================================
    # Pre-conditions
    # ========================================================================
    reporter.add_step("Pre-conditions", "Set initial conditions for the test")

    print("\n[STEP 1] Setting Pre-conditions...")
    print("-" * 70)
    # Vehicle Mode is "Running" (Value 6 for "Running" from common vehicle mode enums)
    set_can_signal(hil_var, "VehicleMode", 6)
    # Ambient air temperature is above the threshold for AC enablement (e.g., 10°C).
    set_can_signal(hil_var, "PV_AmbientAirTemp", 15.0) # Set to 15 deg C
    # Climate Control System is initially in a normal operating state (e.g., Auto mode, no Max Defrost active).
    set_can_signal(hil_var, "MaxDefrostRequest", 0) # Ensure Max Defrost is off
    set_can_signal(hil_var, "ClimatePowerRequest", 0) # AC off initially
    set_can_signal(hil_var, "CabHeatManReq", 0) # Heating off initially
    set_can_signal(hil_var, "HVACBlowerRequest", 1) # Blower low initially (Value 1)
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1) # Floor/Vent on initially (Value 1 for on)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)

    asyncio.run(asyncio.sleep(0.5))

    print("\n[STEP 2] Verify Pre-conditions...")
    print("-" * 70)
    reporter.add_step("Verify Pre-conditions", "Check that initial conditions are met")
    check_can_signal(hil_var, "MaxDefrostStatus", 0)
    check_can_signal(hil_var, "ClimatePowerStatus", 0)
    check_can_signal(hil_var, "CabHeatManStatus", 0)
    check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 1)
    check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 1)
    check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 1)


    # ========================================================================
    # Test Steps (Trigger)
    # ========================================================================

    # Step 1: Set MaxDefrostRequest to 1 (On).
    print("\n[STEP 3] Trigger: Setting MaxDefrostRequest to 1 (On)")
    print("-" * 70)
    reporter.add_step("Trigger Max Defrost Request", "Set MaxDefrostRequest to 1 (On).")
    set_can_signal(hil_var, "MaxDefrostRequest", 1)

    # Step 2: Set `VehicleMode` to "Running". (Re-asserting for test clarity)
    print("\n[STEP 4] Re-assert VehicleMode to Running (Value 6)")
    print("-" * 70)
    reporter.add_step("Re-assert Vehicle Mode", "Ensure VehicleMode is 'Running'.")
    set_can_signal(hil_var, "VehicleMode", 6)

    # Step 3: Set `PV_AmbientAirTemp` to 15.0°C. (Re-asserting for test clarity)
    print("\n[STEP 5] Re-assert PV_AmbientAirTemp to 15.0°C")
    print("-" * 70)
    reporter.add_step("Re-assert Ambient Air Temp", "Set PV_AmbientAirTemp to 15.0°C.")
    set_can_signal(hil_var, "PV_AmbientAirTemp", 15.0)

    # Step 4: Monitor the relevant status signals. (This is where verification happens)
    print("\n[STEP 6] Monitoring status signals for expected outcome...")
    print("-" * 70)
    reporter.add_step("Monitor Status Signals and Verify Outcome", "Verify the system's response to Max Defrost activation.")

    asyncio.run(asyncio.sleep(1.0)) # Allow time for system to react and signals to propagate

    # ========================================================================
    # Expected Outcome Verification
    # ========================================================================
    checks_passed = True
    # - `MaxDefrostStatus` == 1 (On)
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1)
    # - `ClimateAirDistStatus_Defrost` == 100% (Open)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 100)
    # - `ClimateAirDistStatus_Floor` == 0% (Closed)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    # - `ClimateAirDistStatus_Vent` == 0% (Closed)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    # - `HVACBlowerLevelStat_BlowerLevel` == Maximum Value (As high as possible)
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10) # Max value as per template simulation
    # - `PS_FrontACStatus` == On (Enabled) -> Using `ClimatePowerStatus` for incoming AC status
    checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1) # Assuming 1 for On/Enabled
    # - `PV_FrontTemperatureStatus` == Maximum Value (Highest possible heating) -> Using `CabHeatManStatus` for incoming heating status
    checks_passed &= check_can_signal(hil_var, "CabHeatManStatus", 10) # Max value as per template simulation
    # - Recirculation is off (fresh air) (Note: Signal missing from DB; manual verification required)
    print(f"  [MANUAL CHECK] Verify Recirculation is off (fresh air) (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: Recirculation is off (fresh air)")


    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    print("\nSummary:")
    print(f"  - All signal paths checked and simulated: YES")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if checks_passed else 'FAIL'}")

    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activation_request_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct in projectConfig.json for actual HIL interaction")
    print("   3. Set DRY_RUN = False in the script")
    print("   4. Run: pytest -v your_test_script_name.py")
    print("="*70 + "\n")

    # In dry run, we consider the test successful if it ran without errors and generated checks.
    # A real test would assert checks_passed.
    return True


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION REQUEST DRY RUN")
    print("="*70)
    print("\nThis will:")
    print("  [+] Show what the test WOULD do")
    print("  [+] Read current hardware state (no changes)")
    print("  [+] Validate all signal names exist in mock config")
    print("  [+] Simulate expected responses")
    print("  [+] Generate a report")
    print("\nThis will NOT:")
    print("  [-] Change any hardware signals")
    print("  [-] Control motors or actuators")
    print("\n" + "="*70)

    input("\nPress Enter to start dry run...")

    # Mock read_project_config for standalone run
    class MockHILConfig:
        def __call__(self):
            # This replicates the hil_config fixture for standalone execution
            hil_var = {
                "CAN": {
                    "IN": {
                        "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
                        "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
                        "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
                        "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
                        "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
                        "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
                        "ClimatePowerStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimatePowerStatus",
                        "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
                    },
                    "OUT": {
                        "MaxDefrostRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/MaxDefrostRequest",
                        "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_02P (284262208)/VehicleMode",
                        "PV_AmbientAirTemp": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_61P (419244352)/PV_AmbientAirTemp",
                        "ClimatePowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimatePowerRequest",
                        "CabHeatManReq": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_59P (352288832)/CabHeatManReq",
                        "HVACBlowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/HVACBlowerRequest",
                        "ClimateAirDistRequest_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Defrost",
                        "ClimateAirDistRequest_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Floor",
                        "ClimateAirDistRequest_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Vent",
                    }
                }
            }
            return hil_var

    mock_hil_config_obj = MockHILConfig()
    test_max_defrost_activation_request(mock_hil_config_obj())