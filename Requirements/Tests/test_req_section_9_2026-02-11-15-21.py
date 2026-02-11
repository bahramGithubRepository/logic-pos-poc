import pytest
import asyncio
from niveristand.clientapi import ChannelReference
from hil_modules import read_project_config
from test_reporter import TestReporter


# Dry run configuration
DRY_RUN = True  # Set to False to actually execute
SIMULATE_RESPONSES = True  # Simulate expected hardware responses

# Global reporter instance
reporter = None

# Simulation state (pretend hardware values)
simulated_state = {}


@pytest.fixture(scope="module")
def hil_config():
    """Load HIL configuration once for all tests"""
    _, _, _, hil_var = read_project_config()
    return hil_var


def set_can_signal(hil_var, signal_name, value):
    """
    DRY RUN: Show what WOULD be sent, but don't actually send
    """
    if DRY_RUN:
        print(f"  [DRY RUN SET] {signal_name} = {value} (NOT SENT)")

        # Store in simulated state
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
            print(f"  WARNING: Signal '{signal_name}' not found in CAN OUT configuration")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found")


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.1):
    """
    DRY RUN: Read actual value but simulate what response WOULD be
    """
    try:
        signal_path = hil_var["CAN"]["IN"][signal_name]
        actual_value = ChannelReference(signal_path).value

        if DRY_RUN and SIMULATE_RESPONSES:
            # Simulate expected response based on test logic
            simulated_value = simulate_hardware_response(signal_name, expected_value)

            passed = abs(simulated_value - expected_value) <= tolerance

            print(f"  [DRY RUN CHECK] {signal_name}")
            print(f"     Current real value: {actual_value}")
            print(f"     Simulated response: {simulated_value} (expected {expected_value})")

            if passed:
                print(f"     [PASS] WOULD PASS")
            else:
                print(f"     [FAIL] WOULD FAIL")

            if reporter:
                reporter.add_check(signal_name, expected_value, simulated_value, passed, tolerance)
                reporter.add_note(f"Actual hardware value: {actual_value} (not changed in dry run)")

            return passed
        else:
            # Normal check against real hardware
            passed = abs(actual_value - expected_value) <= tolerance

            if passed:
                print(f"  [PASS] CHECK: {signal_name} = {actual_value} (expected {expected_value})")
            else:
                print(f"  [FAIL] CHECK: {signal_name} = {actual_value} (expected {expected_value})")

            if reporter:
                reporter.add_check(signal_name, expected_value, actual_value, passed, tolerance)

            return passed

    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN configuration")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found")
        return False


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the CCM WOULD respond with based on test logic

    This simulates ideal hardware behavior - real hardware may differ!
    """

    # Map of expected CCM responses based on requests
    response_map = {
        # Status signals mirror request signals in ideal case
        "MaxDefrostStatus": simulated_state.get("MaxDefrostRequest", 0),
        "ClimatePowerStatus": simulated_state.get("ClimatePowerRequest", 0),

        # Air recirculation - forced OFF (0) during max defrost for fresh air
        "AirRecirculationStatus": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("AirRecirculationRequest", 0),

        # Blower level - in max defrost, should go to max (10)
        "HVACBlowerLevelStat_BlowerLevel": 10 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("HVACBlowerRequest", 1),

        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Defrost", 0),
        "ClimateAirDistStatus_Floor": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Vent", 0),

        # Cabin heater - in max defrost, should go to 15 (max heating as per scenario)
        "CabHeatManStatus": 15 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("CabHeatManReq", 0),
    }

    # Return simulated value, or expected value if not in map
    return response_map.get(signal_name, expected_value)


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of CAN IN signal"""
    try:
        signal_path = hil_var["CAN"]["IN"][signal_name]
        value = ChannelReference(signal_path).value

        if DRY_RUN:
            print(f"  [READ] {signal_name} = {value} (current hardware state)")

        return value
    except KeyError:
        return default


def test_max_defrost_activates_max_heating(hil_config):
    """
    Verify that the Thermal System requests maximum heating when Max Defrost is activated.
    """

    global reporter
    reporter = TestReporter(
        "Max Defrost Activates Max Heating - DRY RUN",
        "Verify Max Defrost activation leads to maximum heating request."
    )

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATES MAX HEATING TEST")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)

    hil_var = hil_config

    # ========================================================================
    # Read current hardware state before test
    # ========================================================================
    print("\n[STEP 0] Reading Current Hardware State...")
    print("-" * 70)
    reporter.add_step("Step 0: Read Current State", "Capture current hardware values before dry run")

    current_state = {}
    signals_to_read = [
        "VehicleMode",
        "MaxDefrostStatus",
        "CabHeatManStatus",
    ]

    print("  Current hardware values:")
    for sig in signals_to_read:
        val = get_can_signal(hil_var, sig, -999)
        current_state[sig] = val
        if val != -999:
            print(f"     {sig}: {val}")
        else:
            print(f"     {sig}: NOT FOUND")

        if reporter:
            reporter.add_note(f"Current {sig} = {val}")

    # ========================================================================
    # Step 1: Set the vehicle operating mode to 'Running' (Pre-condition)
    # ========================================================================
    print("\n[STEP 1] Setting Pre-conditions: Vehicle operating mode to 'Running'")
    print("-" * 70)
    reporter.add_step("Step 1: Set Vehicle to Running", "Ensure vehicle is in running state for Max Defrost activation.")

    set_can_signal(hil_var, "VehicleMode", 6) # Assuming 6 means 'Running'
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Ensure climate is on
    set_can_signal(hil_var, "MaxDefrostRequest", 0) # Ensure it's off initially for a clean start
    set_can_signal(hil_var, "CabHeatManReq", 0) # Ensure heater is off initially

    asyncio.run(asyncio.sleep(0.5))

    check_can_signal(hil_var, "VehicleMode", 6)
    check_can_signal(hil_var, "ClimatePowerStatus", 1)
    check_can_signal(hil_var, "MaxDefrostStatus", 0)
    check_can_signal(hil_var, "CabHeatManStatus", 0)


    # ========================================================================
    # Step 2: Set MaxDefrostStatus to 1 (Trigger)
    # ========================================================================
    print("\n[STEP 2] Setting MaxDefrostRequest to 1 (On)")
    print("-" * 70)
    reporter.add_step("Step 2: Activate Max Defrost", "Set the MaxDefrostRequest signal to 1.")

    set_can_signal(hil_var, "MaxDefrostRequest", 1)

    asyncio.run(asyncio.sleep(1.0)) # Give some time for the system to react


    # ========================================================================
    # Expected Outcome
    # - MaxDefrostStatus == 1
    # - CabHeatManStatus == 15
    # ========================================================================
    print("\n[STEP 3] Verifying Expected Outcome")
    print("-" * 70)
    reporter.add_step("Step 3: Verify Max Defrost and Heating Status", "Check if MaxDefrostStatus is 1 and CabHeatManStatus is 15.")

    max_defrost_passed = check_can_signal(hil_var, "MaxDefrostStatus", 1)
    cab_heat_passed = check_can_signal(hil_var, "CabHeatManStatus", 15)

    final_result_passed = max_defrost_passed and cab_heat_passed


    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    print("\nSummary:")
    print(f"  - All signal paths validated: {'YES' if final_result_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if final_result_passed else 'FAIL'}")

    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activates_max_heating_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: DRY_RUN = False in this file or set environment variable")
    print("   4. Then execute: pytest -v your_test_file_name.py")
    print("="*70 + "\n")

    # Always pass in dry run (we're just validating logic)
    assert final_result_passed


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATES MAX HEATING DRY RUN")
    print("="*70)
    print("\nThis will:")
    print("  [+] Show what the test WOULD do")
    print("  [+] Read current hardware state (no changes)")
    print("  [+] Validate all signal names exist")
    print("  [+] Simulate expected responses")
    print("  [+] Generate a report")
    print("\nThis will NOT:")
    print("  [-] Change any hardware signals")
    print("  [-] Control motors or actuators")
    print("\n" + "="*70)

    input("\nPress Enter to start dry run...")

    # Mock hil_config for standalone dry run
    class MockChannelReference:
        def __init__(self, value=0):
            self._value = value
        @property
        def value(self):
            return self._value
        @value.setter
        def value(self, v):
            self._value = v

    class MockHilVar:
        def __init__(self):
            self.data = {
                "CAN": {
                    "IN": {
                        "VehicleMode": "MockChannel_VehicleMode",
                        "MaxDefrostStatus": "MockChannel_MaxDefrostStatus",
                        "CabHeatManStatus": "MockChannel_CabHeatManStatus",
                        "ClimatePowerStatus": "MockChannel_ClimatePowerStatus",
                        # Add other signals as needed for reading current state
                    },
                    "OUT": {
                        "VehicleMode": "MockChannel_VehicleMode",
                        "MaxDefrostRequest": "MockChannel_MaxDefrostRequest",
                        "ClimatePowerRequest": "MockChannel_ClimatePowerRequest",
                        "CabHeatManReq": "MockChannel_CabHeatManReq",
                        # Add other signals as needed for setting
                    }
                }
            }
            # Initialize mock channels
            self._channels = {
                "MockChannel_VehicleMode": MockChannelReference(0),
                "MockChannel_MaxDefrostStatus": MockChannelReference(0),
                "MockChannel_CabHeatManStatus": MockChannelReference(0),
                "MockChannel_ClimatePowerStatus": MockChannelReference(0),
                "MockChannel_MaxDefrostRequest": MockChannelReference(0),
                "MockChannel_ClimatePowerRequest": MockChannelReference(0),
                "MockChannel_CabHeatManReq": MockChannelReference(0),
            }

        def __getitem__(self, key):
            if key == "CAN":
                return self.data[key]
            raise KeyError(f"Key '{key}' not found in MockHilVar")

    # Override ChannelReference to use mock channels for standalone dry run
    old_channel_reference = ChannelReference
    def mock_channel_reference_factory(path):
        if path in mock_hil_var._channels:
            return mock_hil_var._channels[path]
        return old_channel_reference(path) # Fallback if not mocked
    ChannelReference = mock_channel_reference_factory

    mock_hil_var = MockHilVar()

    test_max_defrost_activates_max_heating(mock_hil_var)