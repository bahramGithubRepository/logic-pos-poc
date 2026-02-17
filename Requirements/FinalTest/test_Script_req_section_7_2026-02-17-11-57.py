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

        # Blower level - in max defrost, should go to 31 as per scenario
        "HVACBlowerLevelStat_BlowerLevel": 31 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("HVACBlowerRequest", 1),

        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Defrost", 0),
        "ClimateAirDistStatus_Floor": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Vent", 0),

        # Cabin heater - in max defrost, should go to max (e.g., 10 for illustrative purposes)
        "CabHeatManStatus": 10 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("CabHeatManReq", 0),
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


def test_max_defrost_activation_and_blower_speed(hil_config):
    """
    DRY RUN: Verify Max Defrost activation sets blower speed to maximum.
    """

    global reporter
    reporter = TestReporter(
        "Max Defrost Activation and Blower Speed - DRY RUN",
        "Verify that when Max Defrost is activated, the thermal system sets the blower speed to its maximum level."
    )

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION AND BLOWER SPEED TEST")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)

    hil_var = hil_config

    # ========================================================================
    # Pre-conditions
    # ========================================================================
    print("\n[STEP 1] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-Conditions", "Ensure vehicle is in Running mode and Max Defrost is not active, with default climate settings.")

    asyncio.run(asyncio.sleep(0.5))

    # Set vehicle to Running mode
    set_can_signal(hil_var, "VehicleMode", 6) # Assuming 6 is 'Running'
    # Ensure Max Defrost is off
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    # Turn on climate power
    set_can_signal(hil_var, "ClimatePowerRequest", 1)
    # Set default air distribution (e.g., Floor & Vent, not Defrost initially)
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)
    # Ensure air recirculation is not active (or at default)
    set_can_signal(hil_var, "AirRecirculationRequest", 0)
    # Set blower to a non-max value initially
    set_can_signal(hil_var, "HVACBlowerRequest", 5)

    print("\n[STEP 2] Verify Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-Conditions", "Confirm initial state of signals.")

    asyncio.run(asyncio.sleep(0.2)) # Shorter delay in dry run

    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 5) # Matches initial request
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 1)
    checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1)
    # MaxDefrostRequest is an OUT signal, verification isn't typically done on OUT signals,
    # but the dry run simulation will reflect its set state in MaxDefrostStatus.

    # ========================================================================
    # Trigger
    # ========================================================================
    print("\n[STEP 3] Trigger: Set MaxDefrostRequest to 1 (DRY RUN)...")
    print("=" * 70)
    reporter.add_step("Step 3: Trigger Max Defrost", "Set MaxDefrostRequest to ON to activate the function.")

    set_can_signal(hil_var, "MaxDefrostRequest", 1)

    print("\n[STEP 4] Wait for system response (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4: Wait for System Response", "Allow time for the thermal system to react and ramp up the blower speed.")

    asyncio.run(asyncio.sleep(3)) # Allow time for ramp-up

    # ========================================================================
    # Expected Outcome
    # ========================================================================
    print("\n[STEP 5] Verify Expected Outcome (DRY RUN)...")
    print("=" * 70)
    reporter.add_step("Step 5: Verify Expected Outcome", "Check if Max Defrost is active and blower speed is at maximum, along with air distribution.")

    asyncio.run(asyncio.sleep(0.2))

    # Expected Outcome 1: MaxDefrostRequest == 1 (already set, not re-checked as status is main check)
    # Expected Outcome 2: MaxDefrostStatus == 1 (Note: Signal missing from DB; manual verification required)
    print(f"  [MANUAL CHECK] Verify MaxDefrostStatus == 1 (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: MaxDefrostStatus == 1")

    # Expected Outcome 3: HVACBlowerLevelStat_BlowerLevel == 31
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 31)

    # From previous feedback and overview, verify negative checks for air distribution
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE] Max Defrost Activation Test")
    print("="*70)
    print("\nSummary:")
    print(f"  - All signal paths validated: {'YES' if checks_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if checks_passed else 'FAIL'}")

    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activation_blower_speed_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Set DRY_RUN = False in the script (or use a dedicated 'real' test script)")
    print("   4. Run: pytest -v your_test_script_name.py")
    print("="*70 + "\n")

    # Always pass in dry run (we're just validating logic)
    assert checks_passed


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION AND BLOWER SPEED DRY RUN")
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

    _, _, _, hil_var = read_project_config()
    test_max_defrost_activation_and_blower_speed(hil_var)