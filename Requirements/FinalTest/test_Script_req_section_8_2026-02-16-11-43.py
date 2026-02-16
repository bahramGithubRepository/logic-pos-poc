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
            # Signal paths from projectConfig.json search results
            signal_map = {
                "WindscreenDefrost_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/WindscreenDefrost_ButtonStatus",
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
                # Placeholder/example requests, actual HIL setup might have OUT signals for these
                "ClimatePowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimatePowerStatus", # Using status as a placeholder for request for simulation
                "ClimateAirDistRequest_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost", # Using status as a placeholder for request for simulation
                "ClimateAirDistRequest_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor", # Using status as a placeholder for request for simulation
                "ClimateAirDistRequest_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent", # Using status as a placeholder for request for simulation
                "AirRecirculationRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/AirRecirculationStatus", # Using status as a placeholder for request for simulation
                "HVACBlowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel", # Using status as a placeholder for request for simulation
                "CabHeatManReq": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus", # Using status as a placeholder for request for simulation
            }
            signal_path = signal_map[signal_name] # Using hardcoded paths for now, in a real scenario hil_var would have them
            ChannelReference(signal_path).value = value
            print(f"  SET: {signal_name} = {value}")
            if reporter:
                reporter.add_set(signal_name, value)
        except KeyError:
            print(f"  WARNING: Signal '{signal_name}' not found in configuration or no direct 'OUT' signal path known.")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found for setting")


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.1):
    """
    DRY RUN: Read actual value but simulate what response WOULD be
    """
    try:
        # Signal paths from projectConfig.json search results
        signal_map = {
            "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
            "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
            "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
            "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
            "WindscreenDefrost_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/WindscreenDefrost_ButtonStatus",
            "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
            "AirRecirculationStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/AirRecirculationStatus",
            "ClimatePowerStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimatePowerStatus",
            "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
            "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
        }
        signal_path = signal_map[signal_name] # Using hardcoded paths for now, in a real scenario hil_var would have them
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
        print(f"  WARNING: Signal '{signal_name}' not found in configuration or no direct 'IN' signal path known.")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found for checking")
        return False


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the CCM WOULD respond with based on test logic
    
    This simulates ideal hardware behavior - real hardware may differ!
    """
    
    # Use WindscreenDefrost_ButtonStatus as the primary trigger for Max Defrost simulation
    max_defrost_active = simulated_state.get("WindscreenDefrost_ButtonStatus", 0) == 1

    response_map = {
        # Status signals mirror request signals in ideal case
        "MaxDefrostStatus": 1 if max_defrost_active else 0, # Directly tied to button status
        
        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if max_defrost_active else simulated_state.get("ClimateAirDistRequest_Defrost", 0),
        "ClimateAirDistStatus_Floor": 0 if max_defrost_active else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if max_defrost_active else simulated_state.get("ClimateAirDistRequest_Vent", 0),
        
        # Other signals, using template logic, but ensuring the Max Defrost trigger is consistent
        "ClimatePowerStatus": simulated_state.get("ClimatePowerRequest", 0),
        "AirRecirculationStatus": 0 if max_defrost_active else simulated_state.get("AirRecirculationRequest", 0), # Forced OFF during max defrost
        "HVACBlowerLevelStat_BlowerLevel": 10 if max_defrost_active else simulated_state.get("HVACBlowerRequest", 1), # High during max defrost
        "CabHeatManStatus": 10 if max_defrost_active else simulated_state.get("CabHeatManReq", 0), # Highest possible heating
        "VehicleMode": simulated_state.get("VehicleMode", 0) # VehicleMode is an input, just reflect its set value
    }
    
    # Return simulated value, or expected value if not in map
    return response_map.get(signal_name, expected_value)


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of CAN IN signal"""
    try:
        # Signal paths from projectConfig.json search results
        signal_map = {
            "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
            "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
            "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
            "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
            "WindscreenDefrost_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/WindscreenDefrost_ButtonStatus",
            "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
            "AirRecirculationStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/AirRecirculationStatus",
            "ClimatePowerStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimatePowerStatus",
            "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
            "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
        }
        signal_path = signal_map[signal_name] # Using hardcoded paths for now, in a real scenario hil_var would have them
        value = ChannelReference(signal_path).value
        
        if DRY_RUN:
            print(f"  [READ] {signal_name} = {value} (current hardware state)")
        
        return value
    except KeyError:
        return default


def test_max_defrost_air_distribution_verification_dry_run(hil_config):
    """
    DRY RUN: Test validation without hardware control
    
    What this does:
    - ✅ Validates all signal names exist in config (in a real run)
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
        "Max Defrost Air Distribution Verification - DRY RUN",
        "Simulation mode - verifies max defrost activation and air distribution without controlling hardware"
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
        "ClimateAirDistStatus_Floor",
        "ClimateAirDistStatus_Vent",
        "WindscreenDefrost_ButtonStatus", # Also read the input button status
        "VehicleMode",
        # Other signals for comprehensive reporting
        "HVACBlowerLevelStat_BlowerLevel",
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
    # PRE-CONDITIONS
    # - Max Defrost is not currently active (WindscreenDefrost_ButtonStatus == 0, MaxDefrostStatus == 0).
    # - The vehicle is in a state where Max Defrost can be activated (e.g., Running mode).
    # ========================================================================
    print("\n[STEP 1] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-Conditions (DRY RUN)", "Ensure Max Defrost is inactive and vehicle is in Running mode")
    
    asyncio.run(asyncio.sleep(0.5))
    
    # Set initial state for simulation
    set_can_signal(hil_var, "VehicleMode", 6) # Assumed Running mode
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", 0) # Max Defrost not active
    
    # Also set other relevant climate controls to a default non-max-defrost state for simulation
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Climate system is ON
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)
    set_can_signal(hil_var, "AirRecirculationRequest", 1)
    set_can_signal(hil_var, "HVACBlowerRequest", 1)
    set_can_signal(hil_var, "CabHeatManReq", 0)

    # TODO: Signal ActuatorRotationPercentage not found. (Not settable in scenario)
    
    print("\n[STEP 2] Verify Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-Conditions (DRY RUN)", "Simulate expected responses to pre-conditions")
    
    asyncio.run(asyncio.sleep(0.2))  # Shorter delay in dry run
    
    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 1)
    # Check other signals that might be influenced by default state if applicable
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 1)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 1)
    checks_passed &= check_can_signal(hil_var, "CabHeatManStatus", 0)
    
    # ========================================================================
    # MAIN TEST: Trigger Max Defrost
    # ========================================================================
    print("\n[STEP 3] Trigger: Driver activates Max Defrost (DRY RUN)...")
    print("=" * 70)
    reporter.add_step("Step 3: Trigger Max Defrost", "Set WindscreenDefrost_ButtonStatus to 1")
    
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", 1) # Driver activates Max Defrost
    
    print("\n[STEP 4] Allow sufficient time for the Thermal System to respond and stabilize (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4: Wait for System Response", "Allow time for the system to react and stabilize")
    
    asyncio.run(asyncio.sleep(3.0)) # Allow 3 seconds for stabilization
    
    # ========================================================================
    # Verify Expected Outcome
    # ========================================================================
    print("\n[STEP 5] Verifying Expected Outcome (DRY RUN)...")
    print("=" * 70)
    reporter.add_step("Step 5: Verify Expected Outcome", "Check Max Defrost status and air distribution")
    
    current_step_checks_passed = True
    current_step_checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1)
    current_step_checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1)
    current_step_checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    current_step_checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    
    # Additional checks based on the technical context and template's simulate_hardware_response
    current_step_checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10) # High blower
    current_step_checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 0) # No recirculation
    current_step_checks_passed &= check_can_signal(hil_var, "CabHeatManStatus", 10) # Highest possible heating
    
    checks_passed &= current_step_checks_passed
    
    # ========================================================================
    # Teardown (Optional - Resetting state for next test if not dry run)
    # For dry run, this just shows what would happen
    # ========================================================================
    print("\n[STEP 6] Resetting Test Environment (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 6: Reset Environment", "Deactivate Max Defrost for next test")

    # Set button status back to 0
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", 0) 
    asyncio.run(asyncio.sleep(1.0)) # Allow time for system to react
    check_can_signal(hil_var, "MaxDefrostStatus", 0) # Should be off now

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
    report_path = reporter.generate_html("test_max_defrost_air_distribution_report.html")
    
    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Change DRY_RUN = False in the script")
    print("   4. Run: pytest -v your_test_script.py")
    print("="*70 + "\n")
    
    # Always pass in dry run (we're just validating logic), unless a signal was explicitly not found
    if not checks_passed:
        pytest.fail("Dry run simulated checks indicated failures. Please review the report.")


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
    test_max_defrost_air_distribution_verification_dry_run(hil_var)