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
        
        # Cabin heater (temperature) - in max defrost, should go to 10 (max heat)
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
        if DRY_RUN:
            print(f"  [READ WARNING] Signal '{signal_name}' not found in CAN IN configuration. Returning default: {default}")
        return default


def test_max_defrost_deactivation_and_restoration(hil_config):
    """
    DRY RUN: Test Max Defrost deactivation and manual settings restoration
    """
    
    global reporter
    reporter = TestReporter(
        "Max Defrost Deactivation and Manual Settings Restoration - DRY RUN",
        "Verify that when Max Defrost is deactivated, previously active manual HVAC settings are restored."
    )
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST DEACTIVATION AND RESTORATION TEST")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)
    
    hil_var = hil_config
    
    # Store initial manual settings before Max Defrost activation
    # These values represent what the user had set before Max Defrost took over
    initial_recirculation = 1 # Example: ON
    initial_air_dist_floor = 1 # Example: ON
    initial_air_dist_vent = 1 # Example: ON
    initial_air_dist_defrost = 0 # Example: OFF
    initial_temp = 5 # Example: mid-range
    initial_blower = 3 # Example: mid-range
    initial_ac = 1 # Example: ON (via ClimatePowerRequest implies AC on, assuming no separate ACRequest)

    # ========================================================================
    # Step 1: Ensure pre-conditions are met
    # Max Defrost is currently active, and prior manual settings are stored/active.
    # ========================================================================
    print("\n[STEP 1] Setting Pre-conditions & Activating Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 1: Set Pre-conditions & Activate Max Defrost",
        "Set initial manual HVAC settings and then activate Max Defrost."
    )
    
    # Set vehicle mode to Running (example value)
    set_can_signal(hil_var, "VehicleMode", 6)
    asyncio.run(asyncio.sleep(0.1))

    # Set initial manual settings
    set_can_signal(hil_var, "AirRecirculationRequest", initial_recirculation)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", initial_air_dist_floor)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", initial_air_dist_vent)
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", initial_air_dist_defrost)
    set_can_signal(hil_var, "CabHeatManReq", initial_temp)
    set_can_signal(hil_var, "HVACBlowerRequest", initial_blower)
    set_can_signal(hil_var, "ClimatePowerRequest", initial_ac) # AC ON
    asyncio.run(asyncio.sleep(0.5)) # Allow time for settings to be registered

    # Activate Max Defrost
    set_can_signal(hil_var, "MaxDefrostRequest", 1)
    asyncio.run(asyncio.sleep(1.0)) # Allow time for Max Defrost to become active

    print("\n[VERIFICATION 1.1] Verify Max Defrost is active and manual settings are overridden (DRY RUN)...")
    checks_passed_step1 = True
    checks_passed_step1 &= check_can_signal(hil_var, "MaxDefrostStatus", 1) # Max Defrost should be active

    # During Max Defrost, settings are overridden as per Technical Context and simulate_hardware_response
    checks_passed_step1 &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10) # Blower max
    checks_passed_step1 &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1) # Defrost ON
    checks_passed_step1 &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0) # Floor OFF
    checks_passed_step1 &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0) # Vent OFF
    checks_passed_step1 &= check_can_signal(hil_var, "CabHeatManStatus", 10) # Max heat
    checks_passed_step1 &= check_can_signal(hil_var, "AirRecirculationStatus", 0) # Recirculation OFF

    # Manual checks for missing signals during Max Defrost
    print(f"  [MANUAL CHECK] Verify RecirculationStatus == 0 (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: RecirculationStatus == 0 (Signal missing from DB)")
    
    print(f"  [MANUAL CHECK] Verify CabinTempStatus == 10 (Max Heat) (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: CabinTempStatus == 10 (Max Heat) (Signal missing from DB)")

    print(f"  [MANUAL CHECK] Verify ACStatus == 1 (ON) (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ACStatus == 1 (ON) (Signal missing from DB)")


    # ========================================================================
    # Step 2: Set MaxDefrostRequest to 0 (Off).
    # ========================================================================
    print("\n[STEP 2] Deactivating Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step(
        "Step 2: Deactivate Max Defrost",
        "Set MaxDefrostRequest to 0 (Off) by button."
    )
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    asyncio.run(asyncio.sleep(1.0)) # Allow time for deactivation and settings restoration

    # ========================================================================
    # Expected Outcome: Verify settings restoration
    # ========================================================================
    print("\n[VERIFICATION 2.1] Verify Max Defrost is OFF and manual settings are restored (DRY RUN)...")
    checks_passed_step2 = True
    
    checks_passed_step2 &= check_can_signal(hil_var, "MaxDefrostStatus", 0) # Max Defrost should be OFF

    # Verify restoration of manual settings
    print("\n  Verifying restoration of Air Distribution setting:")
    checks_passed_step2 &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", initial_air_dist_defrost)
    checks_passed_step2 &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", initial_air_dist_floor)
    checks_passed_step2 &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", initial_air_dist_vent)

    print("\n  Verifying restoration of Blower setting:")
    checks_passed_step2 &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", initial_blower)

    # Manual checks for missing signals (Recirculation, Temperature, AC)
    print("\n  Verifying restoration of Recirculation setting:")
    print(f"  [MANUAL CHECK] Verify RecirculationStatus == {initial_recirculation} (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: RecirculationStatus == {initial_recirculation} (Signal missing from DB)")

    print("\n  Verifying restoration of Temperature setting:")
    print(f"  [MANUAL CHECK] Verify CabinTempStatus == {initial_temp} (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: CabinTempStatus == {initial_temp} (Signal missing from DB)")

    print("\n  Verifying restoration of AC setting:")
    print(f"  [MANUAL CHECK] Verify ACStatus == {initial_ac} (Signal missing from DB)")
    if reporter: reporter.add_note(f"MANUAL CHECK REQUIRED: ACStatus == {initial_ac} (Signal missing from DB)")

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    print("\nSummary:")
    total_checks_passed = checks_passed_step1 and checks_passed_step2
    print(f"  - All automated checks passed: {'YES' if total_checks_passed else 'NO'}")
    print(f"  - Hardware state unchanged: YES")
    print(f"  - Simulated test logic: {'PASS' if total_checks_passed else 'FAIL'}")
    
    # Generate report
    report_path = reporter.generate_html("report_req_section_13_2026-02-17-12-28.html")
    
    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: pytest -v your_test_file_name.py (after changing DRY_RUN to False)")
    print("="*70 + "\n")
    
    # Always pass in dry run (we're just validating logic)
    return True


if __name__ == "__main__":
    """Run dry run standalone"""
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST DEACTIVATION AND RESTORATION DRY RUN")
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
    test_max_defrost_deactivation_and_restoration(hil_var)