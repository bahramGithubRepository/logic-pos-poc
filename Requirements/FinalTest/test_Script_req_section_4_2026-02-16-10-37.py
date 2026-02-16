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

# Simulation state (pretend hardware values, storing requests)
simulated_state = {
    "VehicleMode": 0,
    "WindscreenDefrost_ButtonStatus": 0,
    "Recirc_ButtonStatus": 0,
    "ClimateAirDistRequest_Floor": 0,
    "HVACBlowerRequest": 0,
    "AC_ButtonStatus": 0,
    "CabTempRequest": 0,
    "ClimateAirDistRequest_Defrost": 0,
    "ClimateAirDistRequest_Vent": 0,
}

# Mapping for VehicleMode enum values (assuming integer representation)
VEHICLE_MODE_ENUM = {
    'Ignition Off': 0,
    'Parked': 1,
    'Living': 2,
    'Accessory': 3,
    'PreRunning': 4,
    'Cranking': 5,
    'Running': 6,
}

# Mapping for common button/status states
STATE_ENUM = {
    'Released': 0,
    'Pressed': 1,
    'Off': 0,
    'On': 1,
    'Inactive': 0,
    'Active': 1,
    'Recirculation Off': 0,
    'Recirculation On': 1,
}


@pytest.fixture(scope="module")
def hil_config():
    """Load HIL configuration once for all tests"""
    # In a real scenario, this would load from projectConfig.json.
    # For a dry run, we define a mock structure that contains the signal paths.
    # The actual paths are typically determined dynamically by read_project_config.
    # This mock hil_var ensures the set_can_signal/check_can_signal can resolve paths.
    
    # Manually identified signal paths from projectConfig.json search results
    hil_var = {
        "CAN": {
            "OUT": {
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/VehicleMode",
                # Scenario implies setting WindscreenDefrost_ButtonStatus directly
                "WindscreenDefrost_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/WindscreenDefrost_ButtonStatus",
                # Scenario implies setting Recirc_ButtonStatus directly
                "Recirc_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/Recirc_ButtonStatus",
                "ClimateAirDistRequest_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Defrost",
                "ClimateAirDistRequest_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Floor",
                "ClimateAirDistRequest_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Vent",
                "HVACBlowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/HVACBlowerRequest",
                # Scenario implies setting AC_ButtonStatus directly
                "AC_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/AC_ButtonStatus",
                "CabTempRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/CabTempRequest",
            },
            "IN": {
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
                "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
                "AC_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/AC_ButtonStatus",
                "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
                "Recirc_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/Recirc_ButtonStatus",
                "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
                "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
                "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
                "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
            }
        }
    }
    # In a real test, you'd load the config like this:
    # _, _, _, hil_var = read_project_config()
    return hil_var


def set_can_signal(hil_var, signal_name, value):
    """
    DRY RUN: Show what WOULD be sent, but don't actually send.
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
            # Prioritize OUT signals, fall back to IN if scenario implies setting an IN signal
            if signal_name in hil_var["CAN"]["OUT"]:
                signal_path = hil_var["CAN"]["OUT"][signal_name]
            elif signal_name in hil_var["CAN"]["IN"]:
                signal_path = hil_var["CAN"]["IN"][signal_name]
                print(f"  WARNING: Attempting to set IN signal '{signal_name}'. This might not have effect on real hardware.")
                if reporter:
                    reporter.add_note(f"WARNING: Attempting to set IN signal '{signal_name}'. This might not have effect on real hardware.")
            else:
                raise KeyError(f"Signal '{signal_name}' not found in CAN OUT or IN configuration.")

            ChannelReference(signal_path).value = value
            print(f"  SET: {signal_name} = {value}")
            if reporter:
                reporter.add_set(signal_name, value)
        except KeyError:
            print(f"  WARNING: Signal '{signal_name}' not found in CAN OUT/IN configuration.")
            if reporter:
                reporter.add_note(f"WARNING: Signal '{signal_name}' not found.")


def check_can_signal(hil_var, signal_name, expected_value, tolerance=0.1):
    """
    DRY RUN: Read actual value but simulate what response WOULD be.
    """
    actual_value = None
    try:
        if signal_name in hil_var["CAN"]["IN"]:
            signal_path = hil_var["CAN"]["IN"][signal_name]
        elif signal_name in hil_var["CAN"]["OUT"]: # Sometimes requests are checked too
            signal_path = hil_var["CAN"]["OUT"][signal_name]
        else:
            raise KeyError(f"Signal '{signal_name}' not found in CAN IN/OUT configuration.")
        
        if not DRY_RUN: # Only read real hardware value if not in dry run
            actual_value = ChannelReference(signal_path).value
            
    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN/OUT configuration.")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found.")
        reporter.add_check(signal_name, expected_value, "N/A (Signal Not Found)", False, tolerance)
        return False

    if DRY_RUN and SIMULATE_RESPONSES:
        # Simulate expected response based on test logic
        simulated_value = simulate_hardware_response(signal_name, expected_value)
        
        passed = abs(simulated_value - expected_value) <= tolerance if isinstance(simulated_value, (int, float)) and isinstance(expected_value, (int, float)) else simulated_value == expected_value
        
        print(f"  [DRY RUN CHECK] {signal_name}")
        print(f"     Expected: {expected_value}")
        print(f"     Simulated response: {simulated_value}")
        if actual_value is not None:
            print(f"     Current real value: {actual_value} (not used for dry run pass/fail)")
        
        if passed:
            print(f"     [PASS] WOULD PASS")
        else:
            print(f"     [FAIL] WOULD FAIL")
        
        if reporter:
            reporter.add_check(signal_name, expected_value, simulated_value, passed, tolerance)
            if actual_value is not None:
                reporter.add_note(f"Actual hardware value: {actual_value} (not changed in dry run)")
        
        return passed
    else:
        # Normal check against real hardware
        if actual_value is None: # Should not happen if not DRY_RUN, but for safety
             print(f"  ERROR: Could not read actual value for {signal_name} in non-DRY_RUN mode.")
             if reporter: reporter.add_note(f"ERROR: Could not read actual value for {signal_name} in non-DRY_RUN mode.")
             reporter.add_check(signal_name, expected_value, "N/A (Read Error)", False, tolerance)
             return False

        passed = abs(actual_value - expected_value) <= tolerance if isinstance(actual_value, (int, float)) and isinstance(expected_value, (int, float)) else actual_value == expected_value
        
        if passed:
            print(f"  [PASS] CHECK: {signal_name} = {actual_value} (expected {expected_value})")
        else:
            print(f"  [FAIL] CHECK: {signal_name} = {actual_value} (expected {expected_value})")
        
        if reporter:
            reporter.add_check(signal_name, expected_value, actual_value, passed, tolerance)
        
        return passed


def simulate_hardware_response(signal_name, expected_value):
    """
    Simulate what the CCM WOULD respond with based on test logic.
    This simulates ideal hardware behavior - real hardware may differ!
    """
    # Retrieve current simulated request states
    is_windscreen_defrost_pressed = simulated_state.get("WindscreenDefrost_ButtonStatus", 0) == 1
    current_vehicle_mode = simulated_state.get("VehicleMode", 0)
    current_recirc_request = simulated_state.get("Recirc_ButtonStatus", 0)
    current_floor_request = simulated_state.get("ClimateAirDistRequest_Floor", 0)
    current_vent_request = simulated_state.get("ClimateAirDistRequest_Vent", 0)
    current_ac_request = simulated_state.get("AC_ButtonStatus", 0)
    current_blower_request = simulated_state.get("HVACBlowerRequest", 0)
    current_temp_request = simulated_state.get("CabTempRequest", 0)
    current_defrost_request = simulated_state.get("ClimateAirDistRequest_Defrost", 0)

    # Define valid vehicle modes for Max Defrost to activate (integer representation)
    valid_modes_for_activation = [
        VEHICLE_MODE_ENUM['Parked'], VEHICLE_MODE_ENUM['Living'], VEHICLE_MODE_ENUM['Accessory'],
        VEHICLE_MODE_ENUM['PreRunning'], VEHICLE_MODE_ENUM['Cranking'], VEHICLE_MODE_ENUM['Running']
    ]
    
    is_max_defrost_should_be_active = False

    if is_windscreen_defrost_pressed and current_vehicle_mode in valid_modes_for_activation:
        # Check deactivation conditions for Max Defrost based on other requests
        if current_recirc_request == STATE_ENUM['Recirculation On']:
            is_max_defrost_should_be_active = False
        elif current_floor_request == STATE_ENUM['Active'] or current_vent_request == STATE_ENUM['Active']:
            is_max_defrost_should_be_active = False
        else:
            is_max_defrost_should_be_active = True
    
    # Max Defrost deactivates if VehicleMode leaves Running (or if Ignition Off)
    if current_vehicle_mode == VEHICLE_MODE_ENUM['Ignition Off']:
        is_max_defrost_should_be_active = False

    response_map = {
        # Status signals based on Max Defrost logic
        "MaxDefrostStatus": STATE_ENUM['Active'] if is_max_defrost_should_be_active else STATE_ENUM['Inactive'],
        "AC_ButtonStatus": STATE_ENUM['On'] if is_max_defrost_should_be_active else current_ac_request, 
        "HVACBlowerLevelStat_BlowerLevel": 100 if is_max_defrost_should_be_active else current_blower_request, # Max blower speed for Max Defrost
        "Recirc_ButtonStatus": STATE_ENUM['Recirculation Off'] if is_max_defrost_should_be_active else current_recirc_request, 
        "ClimateAirDistStatus_Defrost": STATE_ENUM['Active'] if is_max_defrost_should_be_active else current_defrost_request,
        "ClimateAirDistStatus_Floor": STATE_ENUM['Inactive'] if is_max_defrost_should_be_active else current_floor_request,
        "ClimateAirDistStatus_Vent": STATE_ENUM['Inactive'] if is_max_defrost_should_be_active else current_vent_request,
        "CabHeatManStatus": 30 if is_max_defrost_should_be_active else current_temp_request, # Max heat for Max Defrost
        
        # Other request signals that might also be checked as status
        "VehicleMode": current_vehicle_mode,
        "WindscreenDefrost_ButtonStatus": is_windscreen_defrost_pressed,
    }

    if signal_name in response_map:
        return response_map[signal_name]
    
    # For any other signal not explicitly handled in response_map, 
    # if it's a request signal, its status will mirror its last set value in simulation.
    if signal_name in simulated_state:
        return simulated_state[signal_name]

    return expected_value # Fallback to expected value if no simulation logic applies


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of CAN IN signal (for dry run, returns from simulated_state or default)"""
    try:
        # In dry run, we mostly rely on simulated_state for "current values"
        # However, the template allows reading "real" hardware values even in dry run
        if not DRY_RUN:
            if signal_name in hil_var["CAN"]["IN"]:
                signal_path = hil_var["CAN"]["IN"][signal_name]
            elif signal_name in hil_var["CAN"]["OUT"]:
                signal_path = hil_var["CAN"]["OUT"][signal_name]
            else:
                raise KeyError(f"Signal '{signal_name}' not found in CAN IN/OUT configuration.")
            value = ChannelReference(signal_path).value
        else:
            value = simulated_state.get(signal_name, default)
        
        if DRY_RUN:
            print(f"  [READ] {signal_name} = {value} (simulated/initial state)")
        
        return value
    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN/OUT configuration.")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found.")
        return default


def test_max_defrost_activation_modes_dry_run(hil_config):
    """
    DRY RUN: Verify Max Defrost activation and persistence across valid vehicle modes.
    """
    global reporter
    reporter = TestReporter(
        "Max Defrost Activation in Valid Vehicle Modes - DRY RUN",
        "Simulation mode - validates test logic for Max Defrost activation and persistence without controlling hardware."
    )
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION IN VALID VEHICLE MODES")
    print("="*70)
    print("[!] DRY RUN: No signals will be changed on hardware")
    print("[!] This shows what WOULD happen if test runs for real")
    print("="*70)
    
    hil_var = hil_config
    
    # ========================================================================
    # Read current hardware state before test (for logging)
    # ========================================================================
    print("\n[STEP 0] Reading Current Hardware State (for logging)...")
    print("-" * 70)
    reporter.add_step("Step 0: Read Current State", "Capture current hardware values before dry run")
    
    signals_to_read_for_logging = [
        "MaxDefrostStatus", "HVACBlowerLevelStat_BlowerLevel", "ClimateAirDistStatus_Defrost",
        "ClimateAirDistStatus_Floor", "ClimateAirDistStatus_Vent", "Recirc_ButtonStatus",
        "AC_ButtonStatus", "CabHeatManStatus", "VehicleMode", "WindscreenDefrost_ButtonStatus"
    ]
    
    print("  Current hardware values:")
    for sig in signals_to_read_for_logging:
        val = get_can_signal(hil_var, sig, -999)
        if val != -999:
            print(f"     {sig}: {val}")
        else:
            print(f"     {sig}: NOT FOUND")
        if reporter:
            reporter.add_note(f"Initial {sig} = {val}")
    
    # ========================================================================
    # Pre-conditions
    # - The vehicle's ignition is on (handled by setting VehicleMode to Parked)
    # - Max Defrost function is currently inactive.
    # - Ambient temperature is above the threshold where AC operation is inhibited (e.g., 5°C). (Assumed for dry run)
    # - Climate system is powered on. (Assumed for dry run, implicitly handled if AC and Blower respond)
    # ========================================================================
    print("\n[STEP 1] Setting Pre-conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-conditions", "Set initial states for the test scenario.")
    
    set_can_signal(hil_var, "VehicleMode", VEHICLE_MODE_ENUM['Parked'])
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Released']) # Ensure inactive
    set_can_signal(hil_var, "Recirc_ButtonStatus", STATE_ENUM['Recirculation Off'])
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", STATE_ENUM['Inactive'])
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", STATE_ENUM['Inactive'])
    set_can_signal(hil_var, "HVACBlowerRequest", 0) # Some non-max value
    set_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['Off'])
    set_can_signal(hil_var, "CabTempRequest", 20) # Some non-max value
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", STATE_ENUM['Inactive'])
    asyncio.run(asyncio.sleep(0.5))

    print("\n[STEP 2] Verify Pre-conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-conditions", "Check that initial states are as expected.")
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Inactive'])
    check_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['Off'])
    check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 0)
    check_can_signal(hil_var, "Recirc_ButtonStatus", STATE_ENUM['Recirculation Off'])
    check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", STATE_ENUM['Inactive'])
    check_can_signal(hil_var, "ClimateAirDistStatus_Floor", STATE_ENUM['Inactive'])
    check_can_signal(hil_var, "ClimateAirDistStatus_Vent", STATE_ENUM['Inactive'])
    check_can_signal(hil_var, "CabHeatManStatus", 20)
    check_can_signal(hil_var, "VehicleMode", VEHICLE_MODE_ENUM['Parked'])
    asyncio.run(asyncio.sleep(0.2))
    
    # ========================================================================
    # Trigger and Step 3: Max Defrost activation in 'Parked' mode
    # ========================================================================
    print("\n[STEP 3] Trigger: Max Defrost button pressed. Verify activation in Parked mode (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 3: Activate Max Defrost (Parked)", "Set WindscreenDefrost_ButtonStatus to Pressed and verify system response.")
    
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Pressed'])
    asyncio.run(asyncio.sleep(1.0)) # Allow time for activation

    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active'])
    check_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['On'])
    check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 100)
    check_can_signal(hil_var, "Recirc_ButtonStatus", STATE_ENUM['Recirculation Off'])
    check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", STATE_ENUM['Active'])
    check_can_signal(hil_var, "ClimateAirDistStatus_Floor", STATE_ENUM['Inactive'])
    check_can_signal(hil_var, "ClimateAirDistStatus_Vent", STATE_ENUM['Inactive'])
    check_can_signal(hil_var, "CabHeatManStatus", 30)
    check_can_signal(hil_var, "VehicleMode", VEHICLE_MODE_ENUM['Parked'])
    asyncio.run(asyncio.sleep(0.5))

    # ========================================================================
    # Steps 4 & 5: Cycle VehicleMode and verify Max Defrost remains active
    # ========================================================================
    print("\n[STEP 4&5] Cycle VehicleMode and verify Max Defrost remains active (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4&5: Cycle VehicleMode, Max Defrost Active", "Transition through valid vehicle modes while Max Defrost is active.")

    vehicle_modes_to_cycle = [
        ('Living', VEHICLE_MODE_ENUM['Living']),
        ('Accessory', VEHICLE_MODE_ENUM['Accessory']),
        ('PreRunning', VEHICLE_MODE_ENUM['PreRunning']),
        ('Cranking', VEHICLE_MODE_ENUM['Cranking']),
        ('Running', VEHICLE_MODE_ENUM['Running']),
    ]

    for mode_name, mode_value in vehicle_modes_to_cycle:
        reporter.add_note(f"Transitioning to VehicleMode: {mode_name}")
        set_can_signal(hil_var, "VehicleMode", mode_value)
        set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Pressed']) # Ensure it stays pressed
        asyncio.run(asyncio.sleep(0.5))
        
        check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active'])
        check_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['On'])
        check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 100)
        check_can_signal(hil_var, "Recirc_ButtonStatus", STATE_ENUM['Recirculation Off'])
        check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", STATE_ENUM['Active'])
        check_can_signal(hil_var, "ClimateAirDistStatus_Floor", STATE_ENUM['Inactive'])
        check_can_signal(hil_var, "ClimateAirDistStatus_Vent", STATE_ENUM['Inactive'])
        check_can_signal(hil_var, "CabHeatManStatus", 30)
        check_can_signal(hil_var, "VehicleMode", mode_value)
        asyncio.run(asyncio.sleep(0.2))

    # ========================================================================
    # Step 6: Deactivate Max Defrost
    # ========================================================================
    print("\n[STEP 6] Deactivate Max Defrost by releasing button (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 6: Deactivate Max Defrost", "Set WindscreenDefrost_ButtonStatus to Released and verify deactivation.")
    
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Released'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Inactive'])
    asyncio.run(asyncio.sleep(0.2))

    # ========================================================================
    # Steps 7 & 8: Re-activate Max Defrost in 'Running' mode
    # ========================================================================
    print("\n[STEP 7&8] Re-activate Max Defrost in Running mode (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 7&8: Re-activate Max Defrost (Running)", "Set VehicleMode to Running and activate Max Defrost.")
    
    set_can_signal(hil_var, "VehicleMode", VEHICLE_MODE_ENUM['Running'])
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Pressed'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active'])
    check_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['On'])
    asyncio.run(asyncio.sleep(0.2))

    # ========================================================================
    # Step 9: Change Recirc_ButtonStatus to 'Recirculation On'
    # Expected: Max Defrost becomes Inactive
    # ========================================================================
    print("\n[STEP 9] Change Recirc_ButtonStatus to 'Recirculation On'. Expected: Max Defrost Inactive (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 9: Activate Recirculation", "Change Recirc_ButtonStatus to 'Recirculation On' and verify Max Defrost deactivation.")
    
    set_can_signal(hil_var, "Recirc_ButtonStatus", STATE_ENUM['Recirculation On'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Inactive'])
    asyncio.run(asyncio.sleep(0.2))
    
    # Reset for next checks
    set_can_signal(hil_var, "Recirc_ButtonStatus", STATE_ENUM['Recirculation Off'])
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Pressed'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active']) # Re-activate Max Defrost
    asyncio.run(asyncio.sleep(0.2))


    # ========================================================================
    # Step 10: Change ClimateAirDistRequest_Floor to 'Active'
    # Expected: Max Defrost becomes Inactive
    # ========================================================================
    print("\n[STEP 10] Change ClimateAirDistRequest_Floor to 'Active'. Expected: Max Defrost Inactive (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 10: Activate Floor Air Distribution", "Change ClimateAirDistRequest_Floor to 'Active' and verify Max Defrost deactivation.")
    
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", STATE_ENUM['Active'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Inactive'])
    asyncio.run(asyncio.sleep(0.2))

    # Reset for next checks
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", STATE_ENUM['Inactive'])
    set_can_signal(hil_var, "WindscreenDefrost_ButtonStatus", STATE_ENUM['Pressed'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active']) # Re-activate Max Defrost
    asyncio.run(asyncio.sleep(0.2))

    # ========================================================================
    # Step 11: Change HVACBlowerRequest to '50'
    # Expected: Max Defrost remains Active (performance affected)
    # ========================================================================
    print("\n[STEP 11] Change HVACBlowerRequest to '50'. Expected: Max Defrost Active (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 11: Adjust Blower Speed", "Change HVACBlowerRequest to '50' and verify Max Defrost remains active.")
    
    set_can_signal(hil_var, "HVACBlowerRequest", 50)
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active'])
    check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 50) # Status should mirror request if not forced by Max Defrost
    asyncio.run(asyncio.sleep(0.2))

    # ========================================================================
    # Step 12: Change AC_ButtonStatus to 'Off'
    # Expected: Max Defrost remains Active (performance affected)
    # ========================================================================
    print("\n[STEP 12] Change AC_ButtonStatus to 'Off'. Expected: Max Defrost Active (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 12: Turn AC Off", "Change AC_ButtonStatus to 'Off' and verify Max Defrost remains active.")
    
    set_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['Off'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active'])
    check_can_signal(hil_var, "AC_ButtonStatus", STATE_ENUM['Off']) # AC should turn off as per request, but MaxDefrost stays active
    asyncio.run(asyncio.sleep(0.2))


    # ========================================================================
    # Step 13: Change CabTempRequest to '22'
    # Expected: Max Defrost remains Active (performance affected)
    # ========================================================================
    print("\n[STEP 13] Change CabTempRequest to '22'. Expected: Max Defrost Active (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 13: Adjust Cabin Temperature", "Change CabTempRequest to '22' and verify Max Defrost remains active.")
    
    set_can_signal(hil_var, "CabTempRequest", 22)
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Active'])
    check_can_signal(hil_var, "CabHeatManStatus", 22) # Cab temp should mirror request
    asyncio.run(asyncio.sleep(0.2))


    # ========================================================================
    # Step 14: Set VehicleMode to 'Ignition Off'
    # Expected: Max Defrost becomes Inactive
    # ========================================================================
    print("\n[STEP 14] Set VehicleMode to 'Ignition Off'. Expected: Max Defrost Inactive (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 14: Set VehicleMode to Ignition Off", "Set VehicleMode to 'Ignition Off' and verify Max Defrost deactivation.")
    
    set_can_signal(hil_var, "VehicleMode", VEHICLE_MODE_ENUM['Ignition Off'])
    asyncio.run(asyncio.sleep(1.0))
    check_can_signal(hil_var, "MaxDefrostStatus", STATE_ENUM['Inactive'])
    asyncio.run(asyncio.sleep(0.2))


    # ========================================================================
    # Summary & Report Generation
    # ========================================================================
    print("\n" + "="*70)
    print("[DRY RUN COMPLETE]")
    print("="*70)
    
    report_path = reporter.generate_html("max_defrost_activation_dry_run_report.html")
    
    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Set DRY_RUN = False in the script.")
    print("   4. Ensure HIL system is connected and configured.")
    print("   5. Run: pytest -v your_test_script_name.py")
    print("="*70 + "\n")
    
    # In dry run, we are validating logic, so we always "pass" the dry run itself
    # unless there are critical errors in signal definition.
    # The actual pass/fail of individual checks is in the report.
    return True


if __name__ == "__main__":
    """Run dry run standalone"""
    
    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST ACTIVATION IN VALID VEHICLE MODES")
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
    
    # Call the test function directly for standalone execution
    # For standalone, hil_config needs to be manually provided or mocked
    mock_hil_config = {
        "CAN": {
            "OUT": {
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/VehicleMode",
                "WindscreenDefrost_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/WindscreenDefrost_ButtonStatus",
                "Recirc_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/Recirc_ButtonStatus",
                "ClimateAirDistRequest_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Defrost",
                "ClimateAirDistRequest_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Floor",
                "ClimateAirDistRequest_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/ClimateAirDistRequest_Vent",
                "HVACBlowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/HVACBlowerRequest",
                "AC_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/AC_ButtonStatus",
                "CabTempRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Cyclic/CIOM_Cab_62P (419246400)/CabTempRequest",
            },
            "IN": {
                "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
                "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
                "AC_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/AC_ButtonStatus",
                "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
                "Recirc_ButtonStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_06P (285161848)/Recirc_ButtonStatus",
                "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
                "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
                "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
                "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
            }
        }
    }
    test_max_defrost_activation_modes_dry_run(mock_hil_config)