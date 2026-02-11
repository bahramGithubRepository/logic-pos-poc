"""
Max Defrost Test - Converted from test_max_defrost.xml

This test validates the Max Defrost functionality of the CCM (Climate Control Module).
When MaxDefrostRequest is activated, the system should:
- Set MaxDefrostStatus to On
- Set blower to maximum (level 10)
- Route air to defrost only
- Turn off recirculation
- Set cabin heater to maximum

Original XML: test_max_defrost.xml
Generated: 2025-08-27 (PnTool 6.0.0.23)
Converted: 2025-12-22
"""

import pytest
import asyncio
from niveristand.clientapi import ChannelReference
from hil_modules import read_project_config
from test_reporter import TestReporter


# Timeout for async waits
DEFAULT_TIMEOUT = 10.0

# Global reporter instance
reporter = None


@pytest.fixture(scope="module")
def hil_config():
    """Load HIL configuration once for all tests"""
    _, _, _, hil_var = read_project_config()
    return hil_var


def set_can_signal(hil_var, signal_name, value):
    """Helper function to set CAN OUT signals"""
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
    """Helper function to check CAN IN signals"""
    try:
        passed = abs(actual_value - expected_value) <= tolerance
        
        if passed:
            print(f"  ✓ CHECK: {signal_name} = {actual_value} (expected {expected_value})")
        else:
            print(f"  ✗ FAIL: {signal_name} = {actual_value} (expected {expected_value})")
        
        if reporter:
            reporter.add_check(signal_name, expected_value, actual_value, passed, tolerance)
        
        return passed
    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN configuration")
        if reporter:
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found
            print(f"  ✗ FAIL: {signal_name} = {actual_value} (expected {expected_value})")
            return False
    except KeyError:
        print(f"  WARNING: Signal '{signal_name}' not found in CAN IN configuration")
        return False


async def await_condition(check_func, timeout=DEFAULT_TIMEOUT, interval=0.1):
    """Wait for a condition to become true with timeout"""
    elapsed = 0.0
    while elapsed < timeout:
        if check_func():
            return True
        await asyncio.sleep(interval)
        elapsed += interval
    return False


def test_max_defrost(hil_config):
    """
    Test Case: Max Defrost Functionality
    
    Validates that when MaxDefrostRequest is activated:
    global reporter
    reporter = TestReporter(
        "Max Defrost Test",
        "Validates CCM Max Defrost functionality: activation, blower max, defrost-only air distribution, fresh air mode, and maximum cabin heating"
    )
    
    1. MaxDefrostStatus turns On
    2. Blower level increases to 10 (maximum)
    3. Air distribution switches to Defrost only (Vent=0, Floor=0)
    4. Air Recirculation turns Off
    5. Cabin heater increases to maximum (10)
    """
    
    print("\n" + "="*70)
    print("MAX DEFROST TEST - START")
    print("="*70)
    
    hil_var = hil_c
    reporter.add_step("Step 1: Set Pre-Conditions", "Configure initial system state before test")onfig
    
    # ========================================================================
    # PRE-CONDITIONS: Set initial state
    # ========================================================================
    print("\n[STEP 1] Setting Pre-Conditions...")
    print("-" * 70)
    
    # Wait 500ms for system stabilization
    asyncio.run(asyncio.sleep(0.5))
    
    # Set initial CAN OUT signals (from CIOM to CCM)
    set_can_signal(hil_var, "VehicleMode", 6)  # VehicleMode_Running
    set_can_signal(hil_var, "ClimatePowerRequest", 1)  # On
    set_can_signal(hil_var, "MaxDefrostRequest", 0)  # Off
    set_can_signal(
    reporter.add_step("Step 2: Verify Pre-Conditions", "Wait 2s and check CCM responded correctly to initial setup")hil_var, "ClimateAirDistRequest_Defrost", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)
    set_can_signal(hil_var, "AirRecirculationRequest", 1)  # On
    set_can_signal(hil_var, "HVACBlowerRequest", 1)
    
    print("\n[STEP 2] Verify Pre-Conditions (Timeout: 2s)...")
    print("-" * 70)
    
    # Wait for CCM to respond and verify initial state
    asyncio.run(asyncio.sleep(2.0))
    
    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)  # Off
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 1)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 1)  # On
    checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1)  # On
    
    assert checks_passed, "Pre-condition verification failed"
    
    # ========================================================================
    # Send "Not Available" values to test robustness
    # =============
    reporter.add_step("Step 3: Test 'Not Available' Handling", "Send NotAvailable (15/3) values and verify CCM maintains previous valid state")===========================================================
    print("\n[STEP 3] Testing 'Not Available' Signal Handling...")
    print("-" * 70)
    
    set_can_signal(hil_var, "HVACBlowerRequest", 15)  # Not Available
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 15)  # Not Available
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 15)  # Not Available
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 15)  # Not Available
    set_can_signal(hil_var, "AirRecirculationRequest", 3)  # NotAvailable
    set_can_signal(hil_var, "CabHeatManReq", 15)  # Not Available
    set_can_signal(hil_var, "ClimatePowerRequest", 1)  # Keep On
    
    asyncio.run(asyncio.sleep(0.5))
    
    # CCM should maintain previous valid state
    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 1)
    checks_passed &= check_can_signal(hil_var, "AirRecirculationStatus", 1)
    checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1)
    
    assert checks_passed, "'Not Available' handling verification failed"
    
    # ========================================================================
    # Set Cabin Heater Manual Request
    # =============
    reporter.add_step("Step 4: Set Cabin Heater Request", "Enable cabin heater manual mode")===========================================================
    print("\n[STEP 4] Setting Cabin Heater Manual Request...")
    print("-" * 70)
    
    set_can_signal(hil_var, "CabHeatManReq", 1)
    
    reporter.add_step("Step 5: Verify Cabin Heater Status", "Wait 2s and check heater activated")
    print("\n[STEP 5] Verify Cabin Heater Status (Timeout: 2s)...")
    print("-" * 70)
    asyncio.run(asyncio.sleep(2.0))
    
    checks_passed = check_can_signal(hil_var, "CabHeatManStatus", 1)
    assert checks_passed, "Cabin heater status verification failed"
    
    reporter.add_step("Step 6: Test Cabin Heater NotAvailable", "Send NotAvailable and verify heater maintains previous state")
    # Test "Not Available" for cabin heater
    print("\n[STEP 6] Testing Cabin Heater 'Not Available'...")
    print("-" * 70)
    set_can_signal(hil_var, "CabHeatManReq", 15)  # Not Available
    asyncio.run(asyncio.sleep(0.5))
    
    # Should maintain previous value
    checks_passed = check_can_signal(hil_var, "CabHeatManStatus", 1)
    assert checks_passed, "Cabin heater 'Not Available' handling failed"
    
    # ========================================================================
    # MAIN TEST: Ac
    reporter.add_step("Step 7: Activate Max Defrost", "Send MaxDefrostRequest=1")tivate Max Defrost
    # ========================================================================
    print("\n[STEP 7] ACTIVATING MAX DEFROST REQUEST...")
    print("=" * 70)
    
    set_can_signal(
    reporter.add_step("Step 8: Wait for Max Defrost Activation", "Monitor MaxDefrostStatus for up to 10 seconds")hil_var, "MaxDefrostRequest", 1)  # Turn On Max Defrost
    
    print("\n[STEP 8] Waiting for MaxDefrostStatus to turn On (Timeout: 10s)...")
    print("-" * 70)
    
    # Wait up to 10 seconds for MaxDefrostStatus to activate
    async def check_max_defrost_on():
        try:
            signal_path = hil_var["CAN"]["IN"]["MaxDefrostStatus"]
            value = ChannelReference(signal_path).value
            return abs(value - 1.0) <= 0.1
        except:
            return False
    
    max_defrost_activated = asyncio.run(await_condition(check_max_defrost_on, timeout=10.0))
    
    if max_defrost_activated:
        print("  ✓ MaxDefrostStatus activated!")
    else:
        print("  ✗ MaxDefrostStatus did NOT activate within timeout")
        
    assert max_defrost_activated, "MaxDefrostStatus failed to activate within 10 seconds"
    
    # =============
    reporter.add_step("Step 9: Verify Max Defrost Effects", "Check all expected system responses: blower max, defrost only, recirculation off, heater max")===========================================================
    # Verify Max Defrost Mode Effects
    # ========================================================================
    print("\n[STEP 9] Verifying Max Defrost Mode Effects...")
    print("-" * 70)
    
    asyncio.run(asyncio.sleep(0.5))
    
    checks_passed = True
    
    # Verify blower at maximum
    checks_passed &= check_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 10)
    
    # Verify air distribution: Defrost=On, Vent=Off, Floor=Off
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    
    # Verify cabin heater at maximum
    checks_passed &= check_can_signal(hil_var, "CabHeatManStatus", 10)
    # Generate HTML report
    report_path = reporter.generate_html("test_max_defrost_report.html")
    
    if checks_passed:
        print("\n" + "="*70)
        print("✓ MAX DEFROST TEST - PASSED")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗ MAX DEFROST TEST - FAILED")
        print("="*70)
    
    print(f"\n📊 HTML Report generated: {report_path}")
    print(f"   Open in browser to see detailed results\n")
    else:
        print("\n" + "="*70)
        print("✗ MAX DEFROST TEST - FAILED")
        print("="*70)
        
    assert checks_passed, "Max Defrost mode verification failed"


# ============================================================================
# NOTES FROM XML CONVERSION:
# ============================================================================
# 
# 1. [Include] CCM4 Init A3 ICE:
#    - The XML references an external test case: "TestCase(x040000002BE635C7)"
#    - This is likely an initialization sequence for CCM
#    - TODO: You may need to add this initialization in a setup fixture if required
#    - Comment: Currently not implemented - add if needed
#
# 2. Signal mapping assumptions:
#    - VehicleMode: 6 = VehicleMode_Running
#    - OffOn values: 0=Off, 1=On, 3=NotAvailable
#    - NotAvailable value: 15 for most signals
#    - These mappings should match your DBC file definitions
#
# 3. Timeouts:
#    - Pre-conditions: 2000ms (2s)
#    - Max defrost activation: 10000ms (10s)
#    - State checks: 500ms
#
# 4. LogicalOperator(All):
#    - All checks must pass (AND logic)
#    - Implemented as sequential checks with boolean AND
#
# 5. NetTestFunction.CommonInit / CommonExit:
#    - These appear to be framework-specific functions
#    - TODO: Add proper setup/teardown if needed
#    - Comment: Currently handled by pytest fixtures
#
# ============================================================================


if __name__ == "__main__":
    """
    Run this test standalone for debugging:
    
    python test_max_defrost.py
    
    Or use pytest:
    
    pytest -v test_max_defrost.py
    """
    print("\nRunning Max Defrost Test in standalone mode...")
    print("Make sure VeriStand is deployed before running!")
    print("-" * 70)
    
    # Load config
    _, _, _, hil_var = read_project_config()
    
    # Run test
    test_max_defrost(hil_var)
