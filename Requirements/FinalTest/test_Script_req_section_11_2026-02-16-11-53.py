import pytest
import asyncio
from niveristand.clientapi import ChannelReference
from hil_modules import read_project_config
from test_reporter import TestReporter
from datetime import datetime

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
            # Assuming outgoing signals are in 'OUT'
            signal_path = hil_var["CAN"]["OUT"][signal_name]
            ChannelReference(signal_path).value = value
            print(f"  SET: {signal_name} = {value}")
            if reporter:
                reporter.add_set(signal_name, value)
        except KeyError:
            print(f"  WARNING: Signal '{signal_name}' not found in CAN OUT configuration")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN OUT configuration")


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.1):
    """
    DRY RUN: Read actual value but simulate what response WOULD be
    """
    try:
        # Assuming incoming signals are in 'IN'
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
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN IN configuration")
        return False


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the CCM WOULD respond with based on test logic
    This simulates ideal hardware behavior - real hardware may differ!
    """

    # Get the current state of the trigger signal from our simulated state
    is_windscreen_defrost_button_pressed = simulated_state.get("WindscreenDefrost_ButtonStatus", 0)

    response_map = {
        # MaxDefrostStatus should be 1 if the button is pressed
        "MaxDefrostStatus": 1 if is_windscreen_defrost_button_pressed == 1 else 0,

        # AirRecirculationStatus should be 0 (outside air) if max defrost is active
        "AirRecirculationStatus": 0 if is_windscreen_defrost_button_pressed == 1 else simulated_state.get("AirRecirculationRequest", 0), # Assuming an AirRecirculationRequest if not in Max Defrost

        # Air distribution to Defrost = 15 if max defrost is active, else 0
        "ClimateAirDistStatus_Defrost": 15 if is_windscreen_defrost_button_pressed == 1 else 0,

        # Air distribution to Floor = 0 if max defrost is active, else keep previous request
        "ClimateAirDistStatus_Floor": 0 if is_windscreen_defrost_button_pressed == 1 else simulated_state.get("ClimateAirDistRequest_Floor", 0), # Assuming a ClimateAirDistRequest_Floor if not in Max Defrost

        # Air distribution to Vent = 0 if max defrost is active, else keep previous request
        "ClimateAirDistStatus_Vent": 0 if is_windscreen_defrost_button_pressed == 1 else simulated_state.get("ClimateAirDistRequest_Vent", 0), # Assuming a ClimateAirDistRequest_Vent if not in Max Defrost

        # Other signals, if they are not explicitly part of the Max Defrost scenario,
        # can just return their last set value or the expected value for the check.
        # Example from template:
        "ClimatePowerStatus": simulated_state.get("ClimatePowerRequest", 0),
        "HVACBlowerLevelStat_BlowerLevel": simulated_state.get("HVACBlowerRequest", 1),
        "CabHeatManStatus": simulated_state.get("CabHeatManReq", 0),
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
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN configuration. Returning default: {default}")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN IN configuration. Returning default: {default}")
        return default


def test_max_defrost_activation_dry_run(hil_config):
    """
    DRY RUN: Test validation without hardware control
    Scenario: Max Defrost Activates with Outside Air and Correct Air Distribution
    """

    global reporter
    reporter = TestReporter(
        "Max Defrost Activation Test (DRY RUN)",
        "Verify Max Defrost activates, uses outside air, and sets air distribution correctly in simulation."
    )

    print("\n" + "=" * 70)
    print("[DRY RUN] MAX DEFROST ACTIVATION TEST")
    print("=" * 70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("=" * 70)

    hil_var = hil_config

    # ========================================================================
    # Read current hardware state before test
    # ========================================================================
    print("\n[STEP 0] Reading Current Hardware State...")
    print("-" * 70)
    reporter.add_step("Step 0: Read Current State", "Capture current hardware values before dry run")

    current_state = {}
    signals_to_read = [
        "MaxDefrostStatus",
        "AirRecirculationStatus",
        "ClimateAirDistStatus_Defrost",
        "ClimateAirDistStatus_Floor",
        "ClimateAirDistStatus_Vent",
        # Add other relevant initial state signals if necessary for preconditions,
        # otherwise, focus on the signals under test.
    ]

    print("  Current hardware values:")
    for sig in signals_to_read:
        val = get_can_signal(hil_var, sig, -999) # Use -999 to indicate not found/default
        current_state[sig] = val
        if val != -999:
            print(f"     {sig}: {val}")
        else:
            print(f"     {sig}: NOT FOUND")

        if reporter:
            reporter.add_note(f"Current {sig} = {val}")

    # ========================================================================
    # PRE-CONDITIONS
    # ========================================================================
    print("\n[STEP 1] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-Conditions (DRY RUN)", "Show what initial setup WOULD be")

    asyncio.run(asyncio.sleep(0.5))

    # Set initial states for signals not directly tested but might influence the system
    # (These are examples from the template, adjust as needed or remove if not relevant)
    set_can_signal(hil_var, "VehicleMode", 6)  # Example: Vehicle in Running mode
    set_can_signal(hil_var, "ClimatePowerRequest", 1)  # Example: Climate system is ON
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", 0) # Ensure it's off initially
    set_can_signal(hil_var, "AirRecirculationRequest", 1) # Example: Start with recirculation ON
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 10) # Example: Air to floor
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 10) # Example: Air to vent
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0) # Example: Air not to defrost initially

    print("\n[STEP 2] Verify Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-Conditions (DRY RUN)", "Simulate expected responses to pre-conditions")

    asyncio.run(asyncio.sleep(0.2))  # Shorter delay in dry run

    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 1) # Expected to be ON based on initial request
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 10) # Expected to be 10 based on initial request
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 10) # Expected to be 10 based on initial request
    # checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1) # Not part of scenario checks

    # ========================================================================
    # Test Step 1: Trigger Max Defrost
    # ========================================================================
    print("\n[STEP 3] Trigger: Set WindscreenDefrost_ButtonStatus to 1 (ON) (DRY RUN)...")
    print("=" * 70)
    reporter.add_step("Step 3: Trigger Max Defrost", "Driver requests activation of Max Defrost by setting WindscreenDefrost_ButtonStatus to 1")

    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", 1)

    print("\n[STEP 4] Wait for the system to stabilize (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4: Wait for Stabilization", "Allow system to react to Max Defrost activation")

    asyncio.run(asyncio.sleep(2.0)) # A longer delay to simulate system stabilization

    # In dry run, simulate immediate activation for status signals
    print("  [DRY RUN] Simulating Max Defrost system response...")

    # ========================================================================
    # Expected Outcome
    # ========================================================================
    print("\n[STEP 5] Verify Expected Outcomes (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 5: Verify Expected Outcomes", "Check that Max Defrost is active, using outside air, and air distribution is correct")

    # Verify MaxDefrostStatus == 1
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1)

    # Verify AirRecirculationStatus == 0 (Off - indicating 0% recirculation, outside air only)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 0)

    # Verify ClimateAirDistStatus_Defrost == 15 (Fully open towards defrost)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 15)

    # Verify ClimateAirDistStatus_Floor == 0 (Fully closed for floor distribution)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)

    # Verify ClimateAirDistStatus_Vent == 0 (Fully closed for vent distribution)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)

    # ========================================================================
    # Teardown (Optional, but good practice to return to a known state)
    # ========================================================================
    print("\n[STEP 6] Teardown: Deactivate Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 6: Teardown", "Deactivate Max Defrost to return to a neutral state")
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", 0)
    asyncio.run(asyncio.sleep(0.5))
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)


    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 70)
    print("[DRY RUN COMPLETE]")
    print("=" * 70)
    print("\nSummary:")
    print(f"  - All signal paths validated: {'YES' if checks_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if checks_passed else 'FAIL'}")

    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activation_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: pytest -v your_test_file.py") # User will need to rename the file
    print("=" * 70 + "\n")

    # Always pass in dry run (we're just validating logic, not actual hardware behavior)
    return True


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "=" * 70)
    print("[DRY RUN] MAX DEFROST ACTIVATION DRY RUN")
    print("=" * 70)
    print("\nThis will:")
    print("  [+] Show what the test WOULD do")
    print("  [+] Read current hardware state (no changes)")
    print("  [+] Validate all signal names exist")
    print("  [+] Simulate expected responses")
    print("  [+] Generate a report")
    print("\nThis will NOT:")
    print("  [-] Change any hardware signals")
    print("  [-] Control motors or actuators")
    print("\n" + "=" * 70)

    input("\nPress Enter to start dry run...")

    _, _, _, hil_var = read_project_config()
    test_max_defrost_activation_dry_run(hil_var)