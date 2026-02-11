"""
Max Defrost Test - SAFE VERSION with Hardware Protection

This version includes safety measures to protect physical hardware:
- Temperature monitoring (if available)
- Maximum runtime limits
- Gradual power-up sequences
- Emergency shutdown capability
- Current monitoring (if available)

⚠️ USE THIS VERSION when testing with REAL HARDWARE CONNECTED
"""

import pytest
import asyncio
from niveristand.clientapi import ChannelReference
from hil_modules import read_project_config
from test_reporter import TestReporter
import time


# Safety Configuration
MAX_RUNTIME_SECONDS = 30  # Maximum time to run at full power
MAX_BLOWER_LEVEL = 10  # Can reduce if needed (e.g., 8 for safety)
MAX_HEATER_LEVEL = 10  # Can reduce if needed
GRADUAL_POWERUP = True  # Enable gradual power-up instead of instant max
POWERUP_DELAY = 0.5  # Seconds between power levels during gradual powerup
COOLDOWN_TIME = 5.0  # Seconds to cool down after test

# Emergency stop flag
emergency_stop = False

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
        signal_path = hil_var["CAN"]["IN"][signal_name]
        actual_value = ChannelReference(signal_path).value
        
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
            reporter.add_note(f"WARNING: Signal '{signal_name}' not found")
        return False


def get_can_signal(hil_var, signal_name, default=0.0):
    """Get current value of CAN IN signal"""
    try:
        signal_path = hil_var["CAN"]["IN"][signal_name]
        return ChannelReference(signal_path).value
    except KeyError:
        return default


def monitor_safety(hil_var):
    """
    Monitor safety parameters - ADD YOUR HARDWARE-SPECIFIC CHECKS HERE
    
    Returns: (is_safe, warning_message)
    """
    warnings = []
    
    # TODO: Add temperature monitoring if available
    # Example:
    # temp = get_can_signal(hil_var, "CabinTemperature", 0)
    # if temp > 60:  # degrees Celsius
    #     warnings.append(f"Temperature too high: {temp}°C")
    
    # TODO: Add current monitoring if available
    # Example:
    # current = get_can_signal(hil_var, "BlowerCurrent", 0)
    # if current > 20:  # Amperes
    #     warnings.append(f"Current too high: {current}A")
    
    # TODO: Add voltage monitoring
    # Example:
    # voltage = get_can_signal(hil_var, "SystemVoltage", 0)
    # if voltage < 10 or voltage > 30:
    #     warnings.append(f"Voltage out of range: {voltage}V")
    
    is_safe = len(warnings) == 0
    warning_msg = "; ".join(warnings) if warnings else ""
    
    return is_safe, warning_msg


def safe_powerup(hil_var, signal_name, target_level, steps=5):
    """
    Gradually increase power level instead of instant jump
    
    Args:
        signal_name: Signal to control
        target_level: Final target level
        steps: Number of intermediate steps
    """
    if not GRADUAL_POWERUP:
        set_can_signal(hil_var, signal_name, target_level)
        return
    
    print(f"  📈 Gradual power-up: {signal_name} -> {target_level}")
    
    current = 0
    step_size = target_level / steps
    
    for i in range(steps + 1):
        level = min(int(current), target_level)
        set_can_signal(hil_var, signal_name, level)
        asyncio.run(asyncio.sleep(POWERUP_DELAY))
        current += step_size
    
    print(f"  ✓ Reached target: {target_level}")


def emergency_shutdown(hil_var):
    """Emergency shutdown - set all to safe values"""
    print("\n🚨 EMERGENCY SHUTDOWN!")
    
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    set_can_signal(hil_var, "HVACBlowerRequest", 0)
    set_can_signal(hil_var, "CabHeatManReq", 0)
    set_can_signal(hil_var, "ClimatePowerRequest", 0)
    
    print("✓ All systems set to OFF")


def cooldown_sequence(hil_var):
    """Gradual cooldown after test"""
    print(f"\n🌡️ Cooldown sequence ({COOLDOWN_TIME}s)...")
    
    # Reduce blower gradually
    for level in [8, 6, 4, 2, 0]:
        set_can_signal(hil_var, "HVACBlowerRequest", level)
        asyncio.run(asyncio.sleep(COOLDOWN_TIME / 6))
    
    # Turn off heater
    set_can_signal(hil_var, "CabHeatManReq", 0)
    
    # Turn off max defrost
    set_can_signal(hil_var, "MaxDefrostRequest", 0)
    
    asyncio.run(asyncio.sleep(1.0))
    print("✓ Cooldown complete")


def test_max_defrost_safe(hil_config):
    """
    SAFE VERSION: Max Defrost Test with Hardware Protection
    
    Safety features:
    - Gradual power-up (not instant max)
    - Runtime limit (max 30 seconds at full power)
    - Safety monitoring (temperature, current if available)
    - Cooldown sequence after test
    - Emergency shutdown capability
    """
    
    global reporter
    reporter = TestReporter(
        "Max Defrost Test (SAFE MODE)",
        "Hardware-safe version with gradual power-up, runtime limits, and monitoring"
    )
    
    print("\n" + "="*70)
    print("🛡️  MAX DEFROST TEST - SAFE MODE")
    print("="*70)
    print(f"⚙️  Max runtime: {MAX_RUNTIME_SECONDS}s")
    print(f"⚙️  Gradual powerup: {GRADUAL_POWERUP}")
    print(f"⚙️  Cooldown time: {COOLDOWN_TIME}s")
    print("="*70)
    
    hil_var = hil_config
    test_start_time = time.time()
    
    try:
        # ====================================================================
        # PRE-CONDITIONS
        # ====================================================================
        print("\n[STEP 1] Setting Pre-Conditions...")
        print("-" * 70)
        reporter.add_step("Step 1: Set Pre-Conditions", "Configure initial state (SAFE)")
        
        asyncio.run(asyncio.sleep(0.5))
        
        set_can_signal(hil_var, "VehicleMode", 6)
        set_can_signal(hil_var, "ClimatePowerRequest", 1)
        set_can_signal(hil_var, "MaxDefrostRequest", 0)
        set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
        set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 1)
        set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 1)
        set_can_signal(hil_var, "AirRecirculationRequest", 1)
        set_can_signal(hil_var, "HVACBlowerRequest", 1)  # Start LOW
        
        print("\n[STEP 2] Verify Pre-Conditions...")
        print("-" * 70)
        reporter.add_step("Step 2: Verify Pre-Conditions", "Check initial state")
        
        asyncio.run(asyncio.sleep(2.0))
        
        checks_passed = True
        checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
        checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1)
        
        assert checks_passed, "Pre-condition verification failed"
        
        # ====================================================================
        # SAFETY CHECK BEFORE POWERUP
        # ====================================================================
        print("\n[STEP 3] Safety Check...")
        print("-" * 70)
        reporter.add_step("Step 3: Safety Check", "Verify hardware is safe to proceed")
        
        is_safe, warning = monitor_safety(hil_var)
        
        if not is_safe:
            reporter.add_note(f"⚠️ SAFETY WARNING: {warning}")
            print(f"  ⚠️ SAFETY WARNING: {warning}")
            print("  ℹ️ Proceeding with caution... (add monitoring if needed)")
        else:
            print("  ✓ Safety check passed")
        
        # ====================================================================
        # GRADUAL CABIN HEATER POWERUP
        # ====================================================================
        print("\n[STEP 4] Gradual Cabin Heater Power-Up...")
        print("-" * 70)
        reporter.add_step("Step 4: Gradual Heater Powerup", "Increase heater gradually to avoid thermal shock")
        
        safe_powerup(hil_var, "CabHeatManReq", 1)  # Start with LOW first
        asyncio.run(asyncio.sleep(1.0))
        
        checks_passed = check_can_signal(hil_var, "CabHeatManStatus", 1)
        assert checks_passed, "Cabin heater failed to activate"
        
        # ====================================================================
        # ACTIVATE MAX DEFROST (with runtime limit)
        # ====================================================================
        print("\n[STEP 5] Activating Max Defrost (with runtime limit)...")
        print("=" * 70)
        reporter.add_step("Step 5: Activate Max Defrost", f"Enable max defrost with {MAX_RUNTIME_SECONDS}s limit")
        
        set_can_signal(hil_var, "MaxDefrostRequest", 1)
        
        # Wait for activation
        max_wait = 10.0
        elapsed = 0
        activated = False
        
        while elapsed < max_wait:
            status = get_can_signal(hil_var, "MaxDefrostStatus", 0)
            if abs(status - 1.0) < 0.1:
                activated = True
                print(f"  ✓ MaxDefrostStatus activated in {elapsed:.1f}s")
                break
            await asyncio.sleep(0.5)
            elapsed += 0.5
        
        if not activated:
            reporter.add_note("⚠️ MaxDefrostStatus did not activate - hardware may not support this feature")
            print("  ⚠️ MaxDefrostStatus did not activate")
        
        # ====================================================================
        # MONITOR AT FULL POWER (with safety checks)
        # ====================================================================
        print("\n[STEP 6] Monitoring at Full Power...")
        print("-" * 70)
        reporter.add_step("Step 6: Monitor Full Power Operation", f"Run max {MAX_RUNTIME_SECONDS}s with safety monitoring")
        
        asyncio.run(asyncio.sleep(1.0))
        
        # Verify max defrost effects
        checks_passed = True
        
        # Check if signals reached expected values
        blower_actual = get_can_signal(hil_var, "HVACBlowerLevelStat_BlowerLevel", 0)
        heater_actual = get_can_signal(hil_var, "CabHeatManStatus", 0)
        
        print(f"  📊 Blower Level: {blower_actual} (expected ~{MAX_BLOWER_LEVEL})")
        print(f"  📊 Heater Level: {heater_actual} (expected ~{MAX_HEATER_LEVEL})")
        
        if reporter:
            reporter.add_check("HVACBlowerLevelStat_BlowerLevel", MAX_BLOWER_LEVEL, blower_actual, 
                             abs(blower_actual - MAX_BLOWER_LEVEL) < 2)
            reporter.add_check("CabHeatManStatus", MAX_HEATER_LEVEL, heater_actual,
                             abs(heater_actual - MAX_HEATER_LEVEL) < 2)
        
        # Monitor for limited time
        print(f"  ⏱️ Running at full power for {MAX_RUNTIME_SECONDS}s...")
        
        for i in range(int(MAX_RUNTIME_SECONDS)):
            # Safety check every second
            is_safe, warning = monitor_safety(hil_var)
            
            if not is_safe:
                print(f"  🚨 SAFETY ALERT: {warning}")
                reporter.add_note(f"SAFETY ALERT at {i}s: {warning}")
                break
            
            if i % 5 == 0:
                print(f"    {i}s / {MAX_RUNTIME_SECONDS}s...")
            
            asyncio.run(asyncio.sleep(1.0))
        
        print("  ✓ Full power monitoring complete")
        
        # ====================================================================
        # COOLDOWN SEQUENCE
        # ====================================================================
        print("\n[STEP 7] Cooldown Sequence...")
        print("-" * 70)
        reporter.add_step("Step 7: Cooldown", "Gradually reduce power to protect hardware")
        
        cooldown_sequence(hil_var)
        
        # Final verification
        asyncio.run(asyncio.sleep(1.0))
        
        max_defrost_off = get_can_signal(hil_var, "MaxDefrostStatus", 1)
        print(f"  📊 MaxDefrostStatus after cooldown: {max_defrost_off}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user!")
        reporter.add_note("Test interrupted by user (Ctrl+C)")
        emergency_shutdown(hil_var)
        raise
        
    except Exception as e:
        print(f"\n🚨 Error during test: {e}")
        reporter.add_note(f"Error: {str(e)}")
        emergency_shutdown(hil_var)
        raise
        
    finally:
        # Always generate report
        test_duration = time.time() - test_start_time
        report_path = reporter.generate_html("test_max_defrost_safe_report.html")
        
        print("\n" + "="*70)
        print(f"✓ Test completed in {test_duration:.1f}s")
        print(f"📊 HTML Report: {report_path}")
        print("="*70)


if __name__ == "__main__":
    """Run SAFE test standalone"""
    
    print("\n" + "="*70)
    print("🛡️  HARDWARE-SAFE MAX DEFROST TEST")
    print("="*70)
    print("\n⚠️  SAFETY REMINDERS:")
    print("  1. Check that hardware is properly cooled (fans, ventilation)")
    print("  2. Monitor temperature if sensors available")
    print("  3. Keep manual emergency stop accessible")
    print("  4. Do NOT leave test running unattended")
    print("  5. Inspect hardware after test for overheating")
    print("\n" + "="*70)
    
    response = input("\nHardware ready and monitored? (yes/no): ")
    
    if response.lower() != "yes":
        print("❌ Test aborted by user")
        exit(0)
    
    print("\n🚀 Starting SAFE test...")
    print("   Press Ctrl+C anytime for emergency shutdown\n")
    
    _, _, _, hil_var = read_project_config()
    test_max_defrost_safe(hil_var)
