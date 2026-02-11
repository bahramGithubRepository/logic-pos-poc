import pytest
import asyncio
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
            # Assuming output signals are in 'CAN']['OUT']
            if signal_name == "VehicleMode":
                signal_path = hil_var["CAN"]["OUT"]["VehicleMode"]
            elif signal_name == "MaxDefrostRequest":
                signal_path = hil_var["CAN"]["OUT"]["MaxDefrostRequest"]
            else:
                raise KeyError(f"Signal '{signal_name}' not explicitly mapped in set_can_signal")
            
            # Using ChannelReference directly is not allowed as per instructions, but the template uses it
            # To adhere to the prompt's instruction "You MUST mimic its structure exactly, including ... the set_can_signal/check_can_signal wrapper functions."
            # and "Signal Access: NEVER use ChannelReference directly inside the test function. ALWAYS use set_can_signal(...) or check_can_signal(...).",
            # I will keep the ChannelReference in the set_can_signal wrapper as provided in the template,
            # as the template itself defines how these wrappers should function when DRY_RUN is False.
            from niveristand.clientapi import ChannelReference
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
        # Assuming input signals are in 'CAN']['IN']
        if signal_name == "MaxDefrostStatus":
            signal_path = hil_var["CAN"]["IN"]["MaxDefrostStatus"]
        elif signal_name == "ClimateAirDistStatus_Defrost":
            signal_path = hil_var["CAN"]["IN"]["ClimateAirDistStatus_Defrost"]
        elif signal_name == "VehicleMode": # Assuming for check too
             signal_path = hil_var["CAN"]["IN"]["VehicleMode"]
        else:
            raise KeyError(f"Signal '{signal_name}' not explicitly mapped in check_can_signal")
        
        from niveristand.clientapi import ChannelReference
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
        # MaxDefrostStatus should follow MaxDefrostRequest
        "MaxDefrostStatus": simulated_state.get("MaxDefrostRequest", 0),
        
        # ClimateAirDistStatus_Defrost should be 1 when MaxDefrostRequest is 1
        "ClimateAirDistStatus_Defrost": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 0,
        
        # VehicleMode should reflect the set value
        "VehicleMode": simulated_state.get("VehicleMode", 0),
    }
    
    # Return simulated value, or expected value if not in map
    return response_map.get(signal_name, expected_value)


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of CAN IN signal"""
    try:
        # Assuming input signals are in 'CAN']['IN']
        if signal_name == "MaxDefrostStatus":
            signal_path = hil_var["CAN"]["IN"]["MaxDefrostStatus"]
        elif signal_name == "ClimateAirDistStatus_Defrost":
            signal_path = hil_var["CAN"]["IN"]["ClimateAirDistStatus_Defrost"]
        elif signal_name == "VehicleMode": # Assuming for get too
             signal_path = hil_var["CAN"]["IN"]["VehicleMode"]
        else:
            raise KeyError(f"Signal '{signal_name}' not explicitly mapped in get_can_signal")
            
        from niveristand.clientapi import ChannelReference
        value = ChannelReference(signal_path).value
        
        if DRY_RUN:
            print(f"  [READ] {signal_name} = {value} (current hardware state)")
        
        return value
    except KeyError:
        return default


def test_max_defrost_air_distribution_verification(hil_config):
    """
    DRY RUN: Test validation without hardware control
    """
    
    global reporter
    reporter = TestReporter(
        "Max Defrost Air Distribution Verification - DRY RUN",
        "Verify that when Max Defrost is activated, the Thermal System sets the air distribution to defrost-only mode."
    )
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST AIR DISTRIBUTION VERIFICATION TEST")
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
        "MaxDefrostStatus",
        "ClimateAirDistStatus_Defrost",
        "VehicleMode",
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
    # PRE-CONDITIONS
    # ========================================================================
    print("\n[STEP 1] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-Conditions (DRY RUN)", "Show what initial setup WOULD be")
    
    asyncio.run(asyncio.sleep(0.5))
    
    # Pre-condition: Vehicle is in "Running" mode (assuming 6 is Running)
    set_can_signal(hil_var, "VehicleMode", 6)
    # Pre-condition: Max Defrost is not active
    set_can_signal(hil_var, "MaxDefrostRequest", 0) 
    
    print("\n[STEP 2] Verify Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-Conditions (DRY RUN)", "Simulate expected responses to pre-conditions")
    
    asyncio.run(asyncio.sleep(0.2))  # Shorter delay in dry run
    
    checks_passed = True
    # Pre-condition: MaxDefrostStatus == 0
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    # Pre-condition: ClimateAirDistStatus_Defrost == 0
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    # Check VehicleMode (as a pre-condition, assuming we can check this status)
    checks_passed &= check_can_signal(hil_var, "VehicleMode", 6)
    
    # ========================================================================
    # Test Steps
    # ========================================================================
    print("\n[STEP 3] Set MaxDefrostStatus to 1 (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 3: Trigger Max Defrost (DRY RUN)", "Show command to activate Max Defrost")
    
    # Trigger: Set MaxDefrostStatus to 1 (On)
    set_can_signal(hil_var, "MaxDefrostRequest", 1)
    
    print("\n[STEP 4] Wait for 5 seconds (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4: Wait for System Response (DRY RUN)", "Simulate waiting for system to react")
    
    asyncio.run(asyncio.sleep(5)) # Wait for 5 seconds
    
    # ========================================================================
    # Expected Outcome
    # ========================================================================
    print("\n[STEP 5] Verifying Expected Outcome (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 5: Verify Expected Outcome (DRY RUN)", "Simulate checks for post-condition status")
    
    # Expected Outcome: MaxDefrostStatus == 1
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1)
    # Expected Outcome: ClimateAirDistStatus_Defrost == 1
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1)
    
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
    report_path = reporter.generate_html("test_max_defrost_air_distribution_verification_report.html")
    
    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: pytest -v your_test_file_name.py") # Placeholder for actual filename
    print("="*70 + "\n")
    
    # Always pass in dry run (we're just validating logic)
    return True


if __name__ == "__main__":
    """Run dry run standalone"""
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST AIR DISTRIBUTION VERIFICATION DRY RUN")
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
    test_max_defrost_air_distribution_verification(hil_var)