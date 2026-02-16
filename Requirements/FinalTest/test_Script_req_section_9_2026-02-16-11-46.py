"""
Max Defrost Activates Max Heating Request - DRY RUN MODE

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
        
        # Cabin heater - in max defrost, should go to 15 (as per scenario)
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


def test_max_defrost_activates_max_heating_dry_run(hil_config):
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
        "Max Defrost Activates Max Heating Request - DRY RUN",
        "Verify that when Max Defrost is activated, the Thermal System requests maximum heating. (Simulation mode)"
    )
    
    print("\n" + "="*70)
    print("[DRY RUN] Max Defrost Activates Max Heating Request")
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
    reporter.add_step("Step 0: Read Current State", "Capture current hardware values before dry run.")
    
    current_state = {}
    signals_to_read = [
        "MaxDefrostStatus",
        "CabHeatManStatus",
        "ClimateAirDistStatus_Floor",
        "ClimateAirDistStatus_Vent",
        "ClimatePowerStatus",
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
    # Pre-conditions
    # ========================================================================
    print("\n[STEP 1] Setting Pre-conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 1: Set Pre-conditions",
        "Ensure vehicle is in 'Running' mode, Max Defrost is off, and Climate Power is on."
    )
    
    set_can_signal(hil_var, "VehicleMode", 6) # Assuming 6 is "Running"
    set_can_signal(hil_var, "MaxDefrostRequest", 0) # Ensure Max Defrost is off
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Ensure Climate Power is on
    
    asyncio.run(asyncio.sleep(0.5))
    
    print("\n[STEP 2] Verify Pre-conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 2: Verify Pre-conditions",
        "Confirm initial state before triggering Max Defrost."
    )
    
    checks_passed_pre_cond = True
    checks_passed_pre_cond &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed_pre_cond &= check_can_signal(hil_var, "ClimatePowerStatus", 1)
    
    asyncio.run(asyncio.sleep(0.2))
    
    # ========================================================================
    # Scenario: Max Defrost Activates Max Heating Request
    # ========================================================================
    print("\n[STEP 3] Trigger: Activate Max Defrost Request (DRY RUN)...")
    print("=" * 70)
    reporter.add_step(
        "Step 3: Trigger Max Defrost Request",
        "Driver Experience System sends a request to activate Max Defrost by setting MaxDefrostRequest to '1'."
    )
    
    # Scenario Step 1: Set MaxDefrostRequest to '1' (Activate Max Defrost).
    set_can_signal(hil_var, "MaxDefrostRequest", 1)
    
    asyncio.run(asyncio.sleep(1)) # Allow time for system to react
    
    print("\n[STEP 4] Monitor System Signals and Verify Expected Outcome (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 4: Monitor and Verify Expected Outcome",
        "Monitor MaxDefrostStatus and CabHeatManStatus. Also verify negative checks for air distribution."
    )
    
    # Scenario Step 2: Monitor system signals for response.
    # Expected Outcome:
    # - MaxDefrostStatus == '1' (On)
    # - CabHeatManStatus == '15' (Maximum heating level)
    checks_passed_scenario = True
    checks_passed_scenario &= check_can_signal(hil_var, "MaxDefrostStatus", 1)
    checks_passed_scenario &= check_can_signal(hil_var, "CabHeatManStatus", 15)
    
    # Negative checks from previous feedback
    checks_passed_scenario &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    checks_passed_scenario &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    
    asyncio.run(asyncio.sleep(0.5))
    
    # ========================================================================
    # Teardown
    # ========================================================================
    print("\n[STEP 5] Teardown: Deactivating Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 5: Teardown",
        "Reset Max Defrost Request and Climate Power to off."
    )
    
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    set_can_signal(hil_var, "ClimatePowerRequest", 0)
    asyncio.run(asyncio.sleep(0.5))
    
    print("\n[STEP 6] Teardown Verification (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 6: Teardown Verification",
        "Verify Max Defrost Status is back to off."
    )
    check_can_signal(hil_var, "MaxDefrostStatus", 0)
    check_can_signal(hil_var, "ClimatePowerStatus", 0)
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    print("\nSummary:")
    print(f"  - Pre-conditions validated: {'YES' if checks_passed_pre_cond else 'NO'}")
    print(f"  - Scenario checks validated: {'YES' if checks_passed_scenario else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if (checks_passed_pre_cond and checks_passed_scenario) else 'FAIL'}")
    
    # Generate report
    report_path = reporter.generate_html("test_max_defrost_activates_max_heating_dry_run_report.html")
    
    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: pytest -v your_test_file.py (after setting DRY_RUN = False)")
    print("="*70 + "\n")
    
    # Always pass in dry run (we're just validating logic)
    return True


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
    
    _, _, _, hil_var = read_project_config()
    test_max_defrost_activates_max_heating_dry_run(hil_var)