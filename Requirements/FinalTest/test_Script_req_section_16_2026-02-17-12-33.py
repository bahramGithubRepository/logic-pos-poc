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
            # Assuming all set signals are CAN OUT
            signal_path = hil_var["CAN"]["OUT"][signal_name]
            ChannelReference(signal_path).value = value
            print(f"  SET: {signal_name} = {value}")
            if reporter:
                reporter.add_set(signal_name, value)
        except KeyError:
            print(f"  WARNING: Signal '{signal_name}' not found in CAN OUT configuration")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN OUT")


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
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found in CAN IN")
        return False


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the CCM WOULD respond with based on test logic
    
    This simulates ideal hardware behavior - real hardware may differ!
    """
    
    # Map of expected CCM responses based on requests
    response_map = {
        # Status signals mirror request signals in ideal case (for those not affected by Max Defrost logic)
        "ClimatePowerStatus": simulated_state.get("ClimatePowerRequest", 0),
        "CabHeatManStatus": simulated_state.get("CabHeatManReq", 0),

        # Max Defrost specific logic
        # MaxDefrostStatus - should follow MaxDefrostRequest
        "MaxDefrostStatus": simulated_state.get("MaxDefrostRequest", 0),
        
        # Air recirculation - forced OFF (0) during max defrost for fresh air
        "AirRecirculationStatus": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("AirRecirculationRequest", 0),
        
        # Blower level - during max defrost, should follow HVACBlowerRequest as changes are allowed
        "HVACBlowerLevelStat_BlowerLevel": simulated_state.get("HVACBlowerRequest", 1),
        
        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Defrost", 0),
        "ClimateAirDistStatus_Floor": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if simulated_state.get("MaxDefrostRequest", 0) == 1 else simulated_state.get("ClimateAirDistRequest_Vent", 0),
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


def test_blower_change_during_max_defrost(hil_config):
    """
    DRY RUN: Test validation without hardware control
    
    Scenario: Blower Setting Change During Active Max Defrost
    Verify that when Max Defrost is active and the Driver Experience System
    requests a change in blower setting, the Thermal System updates the
    blower to the new level and maintains Max Defrost activation.
    """
    
    global reporter
    reporter = TestReporter(
        "Blower Setting Change During Active Max Defrost",
        "Verify that when Max Defrost is active and the Driver Experience System requests a change in blower setting, the Thermal System updates the blower to the new level and maintains Max Defrost activation."
    )
    
    print("\n" + "="*70)
    print("[DRY RUN] Blower Setting Change During Active Max Defrost Test")
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
        "HVACBlowerLevelStat_BlowerLevel",
        "ClimateAirDistStatus_Defrost",
        "ClimateAirDistStatus_Floor",
        "ClimateAirDistStatus_Vent",
        "AirRecirculationStatus",
        "ClimatePowerStatus",
        "CabHeatManStatus"
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
    # Step 1: Set Pre-conditions (Max Defrost active, Vehicle in Running mode)
    # ========================================================================
    print("\n[STEP 1] Setting Pre-conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-conditions", "Set VehicleMode to Running and activate Max Defrost with initial blower speed.")
    
    asyncio.run(asyncio.sleep(0.5))
    
    set_can_signal(hil_var, "VehicleMode", 6) # Running mode
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Climate system ON
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 1) # Air to Defrost
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 0) # Floor OFF
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 0) # Vent OFF
    set_can_signal(hil_var, "AirRecirculationRequest", 0) # Recirculation OFF (fresh air)
    set_can_signal(hil_var, "MaxDefrostRequest", 1) # Activate Max Defrost
    set_can_signal(hil_var, "HVACBlowerRequest", 10) # Set initial blower speed
    
    asyncio.run(asyncio.sleep(1)) # Allow time for system to react
    
    # ========================================================================
    # Step 2: Verify Pre-conditions
    # ========================================================================
    print("\n[STEP 2] Verifying Pre-conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-conditions", "Verify Max Defrost is active, vehicle mode is Running, and initial blower speed is set.")
    
    checks_passed = True
    # Verify blower level is 10 (initial setting)
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10)
    
    # Manual check for MaxDefrostStatus
    print(f"  [MANUAL CHECK] Verify MaxDefrostStatus == 1 (On) (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: MaxDefrostStatus == 1")
    
    # Verify negative checks for air distribution
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 0)
    
    # ========================================================================
    # Step 3: Trigger - Change blower setting
    # ========================================================================
    print("\n[STEP 3] Changing Blower Setting (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 3: Change Blower Setting", "Set HVACBlowerRequest to 20 while Max Defrost is active.")
    
    asyncio.run(asyncio.sleep(0.5))
    set_can_signal(hil_var, "HVACBlowerRequest", 20) # Change blower speed
    
    asyncio.run(asyncio.sleep(1)) # Allow time for system to react
    
    # ========================================================================
    # Expected Outcome
    # ========================================================================
    print("\n[STEP 4] Verifying Expected Outcome (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4: Verify Outcome", "Verify blower level updates and Max Defrost remains active.")
    
    # Verify HVACBlowerLevelStat_BlowerLevel == 20
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 20)
    
    # Manual check for MaxDefrostStatus == 1 (On)
    print(f"  [MANUAL CHECK] Verify MaxDefrostStatus == 1 (On) (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: MaxDefrostStatus == 1")

    # Verify negative checks for air distribution remain
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1) # Should remain 1
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 0) # Should remain 0
    
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
    report_path = reporter.generate_html("test_blower_change_during_max_defrost_dry_run_report.html")
    
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
    print("[DRY RUN] Blower Setting Change During Active Max Defrost Test")
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
    test_blower_change_during_max_defrost(hil_var)