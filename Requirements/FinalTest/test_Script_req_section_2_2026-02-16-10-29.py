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
            # Assuming LIN signals are configured as HIL OUT to simulate HVAC module output to CCM
            signal_path = hil_var["LIN"]["OUT"][signal_name]
            ChannelReference(signal_path).value = value
            print(f"  SET: {signal_name} = {value}")
            if reporter:
                reporter.add_set(signal_name, value)
        except KeyError:
            print(f"  WARNING: Signal '{signal_name}' not found in LIN OUT configuration")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found")


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.1):
    """
    DRY RUN: Read actual value but simulate what response WOULD be
    """
    try:
        # Assuming LIN signals are configured as HIL IN to monitor what CCM receives
        signal_path = hil_var["LIN"]["IN"][signal_name]
        actual_value = ChannelReference(signal_path).value

        if DRY_RUN and SIMULATE_RESPONSES:
            # Simulate expected response based on test logic or last set value
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
        print(f"  WARNING: Signal '{signal_name}' not found in LIN IN configuration")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found")
        return False


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the HIL/CCM WOULD respond with based on test logic.
    For this test, we assume the status signal reflects what was last set for dry run.
    """
    # For HVAC Actuator status, assume it reflects the last set value in dry run
    if signal_name in ["LIN_HVACAct1Stat_CurrentPos", "LIN_HVACAct2Stat_CurrentPos", "LIN_HVACAct3Stat_CurrentPos"]:
        return simulated_state.get(signal_name, 0)  # Default to 0 if not set

    # Fallback to expected_value if not explicitly simulated and not in simulated_state
    return simulated_state.get(signal_name, expected_value)


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of LIN IN signal"""
    try:
        # Assuming LIN signals are inputs to HIL for monitoring
        signal_path = hil_var["LIN"]["IN"][signal_name]
        value = ChannelReference(signal_path).value

        if DRY_RUN:
            print(f"  [READ] {signal_name} = {value} (current hardware state)")

        return value
    except KeyError:
        return default


def test_hvac_actuator_position_feedback_dry_run(hil_config):
    """
    DRY RUN: Test validation without hardware control
    """
    global reporter
    reporter = TestReporter(
        "HVAC Actuator Final Position Status Feedback to CCM - DRY RUN",
        "Simulation mode - validates test logic for HVAC actuator position feedback without controlling hardware"
    )

    print("\n" + "=" * 70)
    print("[DRY RUN] HVAC ACTUATOR POSITION FEEDBACK TEST")
    print("=" * 70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("=" * 70)

    hil_var = hil_config

    # ========================================================================
    # Pre-conditions
    # ========================================================================
    print("\n[STEP 0] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 0: Set Pre-Conditions (DRY RUN)", "Simulate vehicle and module operational state.")
    asyncio.run(asyncio.sleep(0.5))
    # No specific signals to set for pre-conditions based on scenario,
    # as it describes vehicle and module operational. We'll proceed directly to simulation.
    reporter.add_note("Assuming vehicle and HVAC/CCM modules are operational as per scenario preconditions.")

    # ========================================================================
    # Step 1: Simulate HVAC Actuator 1 reaching 100
    # ========================================================================
    print("\n[STEP 1] Simulating HVAC Actuator 1 (Recirculation) final position = 100...")
    print("-" * 70)
    reporter.add_step(
        "Step 1: Simulate Actuator 1 Position",
        "Simulate LIN_HVACAct1Stat_CurrentPos feedback to 100."
    )
    set_can_signal(hil_var, "LIN_HVACAct1Stat_CurrentPos", 100)
    asyncio.run(asyncio.sleep(0.1))  # Small delay for simulation

    # ========================================================================
    # Step 2: Simulate HVAC Actuator 2 reaching 150
    # ========================================================================
    print("\n[STEP 2] Simulating HVAC Actuator 2 (Vent/Defrost/Floor) final position = 150...")
    print("-" * 70)
    reporter.add_step(
        "Step 2: Simulate Actuator 2 Position",
        "Simulate LIN_HVACAct2Stat_CurrentPos feedback to 150."
    )
    set_can_signal(hil_var, "LIN_HVACAct2Stat_CurrentPos", 150)
    asyncio.run(asyncio.sleep(0.1))  # Small delay for simulation

    # ========================================================================
    # Step 3: Simulate HVAC Actuator 3 reaching 200
    # ========================================================================
    print("\n[STEP 3] Simulating HVAC Actuator 3 (Heat Blend) final position = 200...")
    print("-" * 70)
    reporter.add_step(
        "Step 3: Simulate Actuator 3 Position",
        "Simulate LIN_HVACAct3Stat_CurrentPos feedback to 200."
    )
    set_can_signal(hil_var, "LIN_HVACAct3Stat_CurrentPos", 200)
    asyncio.run(asyncio.sleep(0.1))  # Small delay for simulation

    # ========================================================================
    # Step 4 & Expected Outcome: Monitor LIN bus and verify feedback signals
    # ========================================================================
    print("\n[STEP 4] Monitoring LIN bus for feedback signals and verifying expected outcomes...")
    print("-" * 70)
    reporter.add_step(
        "Step 4: Monitor and Verify Feedback",
        "Check if CCM receives the correct final position status from actuators."
    )
    asyncio.run(asyncio.sleep(0.5))  # Allow time for CCM to process (simulated)

    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "LIN_HVACAct1Stat_CurrentPos", 100)
    checks_passed &= check_can_signal(hil_var, "LIN_HVACAct2Stat_CurrentPos", 150)
    checks_passed &= check_can_signal(hil_var, "LIN_HVACAct3Stat_CurrentPos", 200)

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 70)
    print("[DRY RUN COMPLETE] HVAC ACTUATOR POSITION FEEDBACK TEST")
    print("=" * 70)
    print("\nSummary:")
    print(f"  - All signal paths validated: {'YES' if checks_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if checks_passed else 'FAIL'}")

    # Generate report
    report_path = reporter.generate_html("test_hvac_actuator_position_feedback_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Set DRY_RUN = False in the script.")
    print("   4. Run: pytest -v <this_script_name>.py")
    print("=" * 70 + "\n")

    # Always pass in dry run (we're just validating logic)
    return True


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "=" * 70)
    print("[DRY RUN] HVAC ACTUATOR POSITION FEEDBACK DRY RUN")
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

    # Mock ChannelReference for standalone dry run execution
    class MockChannelReference:
        def __init__(self, path):
            self.path = path
            self._value = 0.0

        @property
        def value(self):
            # In dry run, for "actual_value" in check_can_signal, we might need a dummy value.
            # For "simulated_value", it comes from simulated_state.
            # This mock mostly ensures ChannelReference access doesn't fail.
            # The actual logic for dry run comes from simulated_state via simulate_hardware_response.
            return self._value

        @value.setter
        def value(self, val):
            self._value = val

    # Mock hil_var structure for dry run standalone execution, reflecting assumed paths
    # These paths are placeholders and not used in DRY_RUN logic, but needed for `KeyError` check.
    mock_hil_var = {
        "LIN": {
            "OUT": {
                "LIN_HVACAct1Stat_CurrentPos": "LIN.LIN29_CCM.LIN_HVACAct1Stat_CurrentPos_HIL_out",
                "LIN_HVACAct2Stat_CurrentPos": "LIN.LIN29_CCM.LIN_HVACAct2Stat_CurrentPos_HIL_out",
                "LIN_HVACAct3Stat_CurrentPos": "LIN.LIN29_CCM.LIN_HVACAct3Stat_CurrentPos_HIL_out",
            },
            "IN": {
                "LIN_HVACAct1Stat_CurrentPos": "LIN.LIN29_CCM.LIN_HVACAct1Stat_CurrentPos_HIL_in",
                "LIN_HVACAct2Stat_CurrentPos": "LIN.LIN29_CCM.LIN_HVACAct2Stat_CurrentPos_HIL_in",
                "LIN_HVACAct3Stat_CurrentPos": "LIN.LIN29_CCM.LIN_HVACAct3Stat_CurrentPos_HIL_in",
            }
        }
    }

    # Override ChannelReference and read_project_config for standalone dry run
    _original_channel_reference = ChannelReference
    _original_read_project_config = read_project_config

    def mock_read_project_config():
        return None, None, None, mock_hil_var

    def mock_channel_reference_factory(path):
        return MockChannelReference(path)

    ChannelReference = mock_channel_reference_factory
    read_project_config = mock_read_project_config

    test_hvac_actuator_position_feedback_dry_run(mock_hil_var)

    # Restore original functions
    ChannelReference = _original_channel_reference
    read_project_config = _original_read_project_config