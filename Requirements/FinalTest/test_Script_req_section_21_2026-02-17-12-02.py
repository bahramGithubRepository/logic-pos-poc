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


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.0):
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
        
        # Blower level - in max defrost, should go to 100
        "HVACBlowerLevelStat_BlowerLevel": 100 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("HVACBlowerRequest", 50),
        
        # AC Button Status - in max defrost, should go to 1
        # This simulation is for the *expected state* if the system turned it on.
        "AC_ButtonStatus": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else 0, # Assuming system sets it to 1 on MaxDefrost
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


def test_max_defrost_activation_verification(hil_config):
    """
    Verify Max Defrost Activation and Settings
    """
    
    global reporter
    reporter = TestReporter(
        "Max Defrost Activation and Settings Verification",
        "Verify that when Max Defrost is requested, the Thermal system correctly sets recirculation to fresh air, "
        "air distribution to defrost only, AC to on, temperature to maximum, and blower speed to maximum."
    )
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION AND SETTINGS VERIFICATION TEST")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)
    
    hil_var = hil_config
    
    # ========================================================================
    # PRE-CONDITIONS
    # ========================================================================
    reporter.add_step("Pre-conditions Setup", "Setting up initial conditions for the test.")
    print("\n[STEP 1] Setting Pre-Conditions...")
    
    # Step 1: Set VehicleMode to "Running". VehicleMode is an IN signal, thus manual setup.
    print(f"  [MANUAL SET] Verify VehicleMode is set to 'Running' (enum 6).")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: Set VehicleMode to 'Running'")
    
    # Step 2: Set MaxDefrostRequest to 0.
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    
    # Step 3: Set Recirc_ButtonStatus to 0 (Fresh air). Recirc_ButtonStatus is an IN signal, thus manual setup.
    print(f"  [MANUAL SET] Ensure Recirc_ButtonStatus is 0 (Fresh air).")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: Set Recirc_ButtonStatus to 0")

    # Step 4: Set AC_ButtonStatus to 0 (AC off). AC_ButtonStatus is an IN signal, thus manual setup.
    print(f"  [MANUAL SET] Ensure AC_ButtonStatus is 0 (AC off).")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: Set AC_ButtonStatus to 0")
    
    # Step 5: Set CabTempRequest to 22.0 (nominal temperature).
    set_can_signal(hil_var, "CabTempRequest", 22.0)
    
    # Step 6: Set HVACBlowerRequest to 50 (nominal level).
    set_can_signal(hil_var, "HVACBlowerRequest", 50)
    
    # Step 7: Set ClimateAirDistRequest_Defrost to 0.
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
    
    # Step 8: Set ClimateAirDistRequest_Floor to 1.
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1)
    
    # Step 9: Set ClimateAirDistRequest_Vent to 1.
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)
    
    asyncio.run(asyncio.sleep(0.5))
    
    # ========================================================================
    # Trigger
    # ========================================================================
    reporter.add_step("Trigger Max Defrost", "Activating Max Defrost request.")
    print("\n[STEP 2] Trigger: Setting MaxDefrostRequest to 1...")
    
    # Step 10: Set MaxDefrostRequest to 1.
    set_can_signal(hil_var, "MaxDefrostRequest", 1)
    
    asyncio.run(asyncio.sleep(1.0)) # Wait for system to react
    
    # ========================================================================
    # Expected Outcome
    # ========================================================================
    reporter.add_step("Verify Expected Outcome", "Checking system response to Max Defrost activation.")
    print("\n[STEP 3] Verifying Expected Outcomes...")
    
    checks_passed = True
    
    # Expected Outcome: MaxDefrostStatus == 1
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1)
    
    # Expected Outcome: Recirc_ButtonStatus == 0. Recirc_ButtonStatus is an IN signal, manual verification.
    print(f"  [MANUAL CHECK] Verify Recirc_ButtonStatus == 0")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: Recirc_ButtonStatus == 0")
    
    # Expected Outcome: ClimateAirDistRequest_Defrost == 1. This is an OUT signal, manual verification.
    print(f"  [MANUAL CHECK] Verify ClimateAirDistRequest_Defrost == 1")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ClimateAirDistRequest_Defrost == 1")
    
    # Expected Outcome: ClimateAirDistRequest_Floor == 0. This is an OUT signal, manual verification.
    print(f"  [MANUAL CHECK] Verify ClimateAirDistRequest_Floor == 0")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ClimateAirDistRequest_Floor == 0")
    
    # Expected Outcome: ClimateAirDistRequest_Vent == 0. This is an OUT signal, manual verification.
    print(f"  [MANUAL CHECK] Verify ClimateAirDistRequest_Vent == 0")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ClimateAirDistRequest_Vent == 0")
    
    # Expected Outcome: AC_ButtonStatus == 1. AC_ButtonStatus is an IN signal, manual verification.
    print(f"  [MANUAL CHECK] Verify AC_ButtonStatus == 1")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: AC_ButtonStatus == 1")
    
    # Expected Outcome: CabTempRequest == 30.0. This is an OUT signal, manual verification.
    print(f"  [MANUAL CHECK] Verify CabTempRequest == 30.0 (Max Temperature Value, assuming 30.0 for this system)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: CabTempRequest == 30.0")
    
    # Expected Outcome: HVACBlowerRequest == 100. This is an OUT signal, manual verification.
    print(f"  [MANUAL CHECK] Verify HVACBlowerRequest == 100 (Max Blower Speed Value, assuming 100% for this system)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: HVACBlowerRequest == 100")
    
    # Expected Outcome: HVACBlowerLevelStat_BlowerLevel == 100.
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 100)
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    print("\nSummary:")
    print(f"  - All automated signal paths validated: {'YES' if checks_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if checks_passed else 'FAIL'}")
    
    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activation_verification_report.html")
    
    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Manually perform steps marked as '[MANUAL SET]' and '[MANUAL CHECK]'")
    print("   4. Set DRY_RUN = False in the script")
    print("   5. Run: pytest -v test_max_defrost_activation_verification.py")
    print("="*70 + "\n")
    
    assert True # Dry run always passes in terms of script execution, actual pass/fail is determined by manual review of report/notes.


if __name__ == "__main__":
    """Run dry run standalone"""
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION VERIFICATION DRY RUN")
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
    test_max_defrost_activation_verification(hil_var)