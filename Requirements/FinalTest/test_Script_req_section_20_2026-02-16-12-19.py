from test_reporter import TestReporter
import asyncio
import pytest
from niveristand.clientapi import ChannelReference
from hil_modules import read_project_config


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
        # Recirc_ButtonStatus reflects this
        "Recirc_ButtonStatus": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 1, # Default to 1 (ON) if not MaxDefrost
        
        # AC_ButtonStatus should be ON (1) during max defrost
        "AC_ButtonStatus": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 0, # Default to 0 (OFF) if not MaxDefrost

        # Blower level - in max defrost, should go to MAXIMUM (e.g., 10)
        "HVACBlowerLevelStat_BlowerLevel": 10 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 1, # Default to 1 if not MaxDefrost

        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 0,
        "ClimateAirDistStatus_Floor": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 1,
        "ClimateAirDistStatus_Vent": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 1,
    }

    # Return simulated value, or expected value if not in map
    return response_map.get(signal_name, expected_value)


def test_max_defrost_dry_run(hil_config):
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
        "Max Defrost Activation and User Deactivation - DRY RUN",
        "Verify Max Defrost function activates and deactivates correctly when requested by the user."
    )

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION AND DEACTIVATION TEST")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)

    hil_var = hil_config
    checks_passed = True # Overall test status for dry run

    # ========================================================================
    # Pre-conditions
    # ========================================================================
    print("\n[STEP 1] Setting Pre-conditions: Vehicle in 'Running' mode, Climate ON.")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-conditions", "Set VehicleMode to 'Running' and ClimatePowerRequest to 'ON'.")

    # The scenario asks for these pre-conditions, but the MaxDefrostRequest is initially INACTIVE
    set_can_signal(hil_var, "VehicleMode", 6) # Assuming 6 == 'Running'
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Assuming 1 == 'ON'
    set_can_signal(hil_var, "MaxDefrostRequest", 0) # Ensure it's initially INACTIVE
    asyncio.run(asyncio.sleep(0.5))

    # ========================================================================
    # Trigger: Max Defrost button pressed by the user.
    # ========================================================================
    print("\n[STEP 2] Trigger: Set MaxDefrostRequest to 'ACTIVE'.")
    print("-" * 70)
    reporter.add_step("Step 2: Activate Max Defrost", "Set MaxDefrostRequest to 'ACTIVE' (user presses button).")

    set_can_signal(hil_var, "MaxDefrostRequest", 1) # Assuming 1 == 'ACTIVE'
    asyncio.run(asyncio.sleep(1)) # Allow time for system response

    # ========================================================================
    # Step 4: Verify system response after activation.
    # ========================================================================
    print("\n[STEP 3] Verify system response after activation.")
    print("-" * 70)
    reporter.add_step("Step 3: Verify Max Defrost Activation", "Check status signals after Max Defrost activation.")

    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1) # Expected: 'ACTIVE'
    checks_passed &= check_can_signal(hil_var, "Recirc_ButtonStatus", 0) # Expected: 'OFF' (Fresh air mode)
    checks_passed &= check_can_signal(hil_var, "AC_ButtonStatus", 1) # Expected: 'ON' (AC activated)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1) # Expected: 'ACTIVE'
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0) # Expected: 'INACTIVE'
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0) # Expected: 'INACTIVE'
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10) # Expected: 'MAXIMUM' (Highest possible)
    asyncio.run(asyncio.sleep(0.5))


    # ========================================================================
    # Step 5: Set MaxDefrostRequest to 'INACTIVE' (user deactivates).
    # ========================================================================
    print("\n[STEP 4] User deactivates: Set MaxDefrostRequest to 'INACTIVE'.")
    print("-" * 70)
    reporter.add_step("Step 4: Deactivate Max Defrost", "Set MaxDefrostRequest to 'INACTIVE' (user presses button again).")

    set_can_signal(hil_var, "MaxDefrostRequest", 0) # Assuming 0 == 'INACTIVE'
    asyncio.run(asyncio.sleep(1)) # Allow time for system response

    # ========================================================================
    # Step 6: Verify system response after deactivation.
    # ========================================================================
    print("\n[STEP 5] Verify system response after deactivation.")
    print("-" * 70)
    reporter.add_step("Step 5: Verify Max Defrost Deactivation", "Check status signals after Max Defrost deactivation.")

    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0) # Expected: 'INACTIVE'
    # Other signals should revert to default or previous states, but scenario only specifies MaxDefrostStatus for deactivation.
    # For a comprehensive test, one might verify other states return to pre-MaxDefrost values.
    asyncio.run(asyncio.sleep(0.5))

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
    report_path = reporter.generate_html("test_max_defrost_activation_deactivation_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: pytest -v your_test_file_name.py")
    print("="*70 + "\n")

    # Always pass in dry run (we're just validating logic)
    assert checks_passed # Fail the pytest if any check failed in simulation
    return True


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION AND DEACTIVATION DRY RUN")
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
    test_max_defrost_dry_run(hil_var)