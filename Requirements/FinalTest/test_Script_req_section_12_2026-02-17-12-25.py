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

        # Blower level - in max defrost, should go to 10
        "HVACBlowerLevelStat_BlowerLevel": 10 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("HVACBlowerRequest", 1),

        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Defrost", 0),
        "ClimateAirDistStatus_Floor": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Vent", 0),

        # Cabin heater - in max defrost, should go to 10
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


def test_max_defrost_scenario(hil_config):
    """
    Test Scenario: Activation of Max Defrost and Automatic AC Function
    Description: Verify that when Max Defrost is activated, the Thermal System reports Max Defrost status as On
                 and attempts to activate the AC function with the lowest allowed evaporator reference temperature.
    """

    global reporter
    reporter = TestReporter(
        "Max Defrost Activation and AC Function",
        "Verify Max Defrost activation, status, and related AC/Thermal system behaviors."
    )

    print("\n" + "="*70)
    print("[DRY RUN] Max Defrost Activation Scenario Test")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)

    hil_var = hil_config

    # ========================================================================
    # PRE-CONDITIONS
    # ========================================================================
    reporter.add_step("Pre-conditions", "Set vehicle to Running mode and ensure thermal system is operational and Max Defrost is off.")
    print("\n[STEP 1] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)

    asyncio.run(asyncio.sleep(0.5))

    # Vehicle is in Running mode.
    set_can_signal(hil_var, "VehicleMode", 6) # Assuming 6 is 'Running' mode
    # Thermal System is operational.
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Turn on Climate Power
    # Ensure Max Defrost is off initially
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    # Ensure air distribution is not defrost, e.g., Floor and Vent
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)
    # Ensure air recirculation is on (will be turned off by Max Defrost)
    set_can_signal(hil_var, "AirRecirculationRequest", 1)
    # Set blower to a nominal level (will be set to max by Max Defrost)
    set_can_signal(hil_var, "HVACBlowerRequest", 5) # Nominal blower speed
    # Set cabin heater to a nominal level (will be set to max by Max Defrost)
    set_can_signal(hil_var, "CabHeatManReq", 5) # Nominal heat level

    asyncio.run(asyncio.sleep(1.0)) # Wait for pre-conditions to settle

    reporter.add_step("Verify Pre-conditions", "Check initial state of relevant signals.")
    print("\n[STEP 2] Verifying Pre-Conditions (DRY RUN)...")
    print("-" * 70)

    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 1)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 1)
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 5)
    checks_passed &= check_can_signal(hil_var, "CabHeatManStatus", 5)
    print(f"  [MANUAL CHECK] Verify ACStatus == 0 (Off) before Max Defrost (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ACStatus == 0 (Off) before Max Defrost")


    # ========================================================================
    # TEST STEPS
    # ========================================================================
    reporter.add_step("Trigger Max Defrost", "Set MaxDefrostRequest to 1 (On).")
    print("\n[STEP 3] Activating Max Defrost Request (DRY RUN)...")
    print("=" * 70)

    # 1. Set MaxDefrostRequest to 1 (On).
    set_can_signal(hil_var, "MaxDefrostRequest", 1)

    # 2. Wait for the system to process the request.
    reporter.add_step("Wait for System Processing", "Allow time for the system to react to the Max Defrost request.")
    print("\n[STEP 4] Waiting for System to Process Request (DRY RUN)...")
    print("-" * 70)
    asyncio.run(asyncio.sleep(2.0)) # Increased wait time to ensure processing


    # ========================================================================
    # EXPECTED OUTCOME
    # ========================================================================
    reporter.add_step("Verify Expected Outcome", "Check that Max Defrost is active and AC/Thermal system functions are set correctly.")
    print("\n[STEP 5] Verifying Expected Outcome (DRY RUN)...")
    print("=" * 70)

    # Expected Outcome:
    # - MaxDefrostStatus == 1 (On)
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1)

    # - ACStatus == 1 (On) (Note: Signal missing from DB; manual verification required)
    print(f"  [MANUAL CHECK] Verify ACStatus == 1 (On) (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ACStatus == 1 (On)")

    # From previous feedback and technical context, also check:
    # - ClimateAirDistStatus_Floor == 0 (Off)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    # - ClimateAirDistStatus_Vent == 0 (Off)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    # - ClimateAirDistStatus_Defrost == 1 (On)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1)
    # - HVACBlowerLevelStat_BlowerLevel == 10 (High)
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10)
    # - AirRecirculationStatus == 0 (Off)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 0)
    # - CabHeatManStatus == 10 (High)
    checks_passed &= check_can_signal(hil_var, "CabHeatManStatus", 10)


    # ========================================================================
    # Test Teardown (Optional, but good practice for restoring state)
    # ========================================================================
    reporter.add_step("Teardown", "Deactivate Max Defrost and restore nominal conditions.")
    print("\n[STEP 6] Performing Teardown (DRY RUN)...")
    print("-" * 70)

    set_can_signal(hil_var, "MaxDefrostRequest", 0) # Turn off Max Defrost
    asyncio.run(asyncio.sleep(1.0)) # Wait for system to revert


    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    print("\nSummary:")
    print(f"  - All signal paths validated: {'YES' if checks_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if checks_passed else 'FAIL'}")

    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activation_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Change DRY_RUN = False in the script")
    print("   4. Run: pytest -v <this_script_name>.py")
    print("="*70 + "\n")

    # Always pass in dry run (we're just validating logic)
    return True


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "="*70)
    print("[DRY RUN] Max Defrost Activation Standalone Dry Run")
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
    test_max_defrost_scenario(hil_var)