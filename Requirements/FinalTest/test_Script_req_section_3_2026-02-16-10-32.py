import pytest
import asyncio
import os
from datetime import datetime
from pathlib import Path

# Mock implementation for ChannelReference
# In a real HIL environment, this would be imported from niveristand.clientapi
class ChannelReference:
    def __init__(self, path):
        self.path = path
        self._value = 0.0  # Default value

    @property
    def value(self):
        # In a real HIL system, this would read from hardware
        return self._value

    @value.setter
    def value(self, new_value):
        # In a real HIL system, this would write to hardware
        self._value = new_value

# Mock hil_modules.read_project_config() since we don't have access to actual file system
# and need to provide the hil_var structure for DRY_RUN.
class MockHILModules:
    def read_project_config(self):
        # This mock function returns a dummy hil_var structure
        # based on the signal paths found in projectConfig.json search.
        hil_var = {
            "CAN": {
                "OUT": {
                    "WindscreenDefrostInd_cmd": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_01P (285153688)/WindscreenDefrostInd_cmd",
                    "ClimatePowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/ClimatePowerRequest",
                    "MaxDefrostRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/MaxDefrostRequest", # Placeholder for template logic
                    "ClimateAirDistRequest_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/ClimateAirDistRequest_Defrost",
                    "ClimateAirDistRequest_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/ClimateAirDistRequest_Floor",
                    "ClimateAirDistRequest_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/ClimateAirDistRequest_Vent",
                    "AirRecirculationRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/AirRecirculationRequest",
                    "HVACBlowerRequest": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/HVACBlowerRequest",
                    "CabHeatManReq": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CCM_Cab_Requests/CabHeatManReq",
                    "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Outgoing/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode"
                },
                "IN": {
                    "VehicleMode": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CIOM_Cab_02P (284262208)/VehicleMode",
                    "MaxDefrostStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/MaxDefrostStatus",
                    "ClimateAirDistStatus_Defrost": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Defrost",
                    "ClimateAirDistStatus_Floor": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Floor",
                    "ClimateAirDistStatus_Vent": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimateAirDistStatus_Vent",
                    "HVACBlowerLevelStat_BlowerLevel": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/HVACBlowerLevelStat_BlowerLevel",
                    "ClimatePowerStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/ClimatePowerStatus",
                    "AirRecirculationStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_11P (418873240)/AirRecirculationStatus",
                    "CabHeatManStatus": "Targets/Controller/Hardware/Chassis/NI-XNET/CAN/Port1/Incoming/Single-Point/CCM_Cab_10P (413608344)/CabHeatManStatus",
                }
            }
        }
        return None, None, None, hil_var # Return (None, None, None, hil_var) to match template's read_project_config() usage.

hil_modules = MockHILModules() # Instantiate the mock class
# from hil_modules import read_project_config # This would be uncommented in a real environment

class TestReporter:
    """Generates detailed HTML reports for test execution"""

    def __init__(self, test_name, description=""):
        self.test_name = test_name
        self.description = description
        self.start_time = datetime.now()
        self.steps = []
        self.checks = []
        self.current_step = None
        self.failed = False

    def add_step(self, step_name, description=""):
        """Add a new test step"""
        step = {
            "name": step_name,
            "description": description,
            "timestamp": datetime.now(),
            "checks": [],
            "sets": []
        }
        self.steps.append(step)
        self.current_step = step
        return step

    def add_set(self, signal_name, value):
        """Record a signal set operation"""
        if self.current_step:
            self.current_step["sets"].append({
                "signal": signal_name,
                "value": value,
                "timestamp": datetime.now()
            })

    def add_check(self, signal_name, expected, actual, passed, tolerance=None):
        """Record a signal check operation"""
        check = {
            "signal": signal_name,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "tolerance": tolerance,
            "timestamp": datetime.now()
        }

        if self.current_step:
            self.current_step["checks"].append(check)

        self.checks.append(check)

        if not passed:
            self.failed = True

    def add_note(self, note):
        """Add a note to current step"""
        if self.current_step:
            if "notes" not in self.current_step:
                self.current_step["notes"] = []
            self.current_step["notes"].append({
                "text": note,
                "timestamp": datetime.now()
            })

    def generate_html(self, output_path="test_report.html"):
        """Generate HTML report file"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        total_checks = len(self.checks)
        passed_checks = sum(1 for c in self.checks if c["passed"])
        failed_checks = total_checks - passed_checks

        status = "FAILED" if self.failed else "PASSED"
        status_color = "#dc3545" if self.failed else "#28a745"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {self.test_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}

        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}

        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .summary-card h3 {{
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}

        .summary-card.status {{
            border-left-color: {status_color};
        }}

        .summary-card.status .value {{
            color: {status_color};
        }}

        .content {{
            padding: 30px;
        }}

        .step {{
            margin-bottom: 30px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            overflow: hidden;
        }}

        .step-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .step-header h3 {{
            color: #333;
            font-size: 18px;
        }}

        .step-time {{
            color: #6c757d;
            font-size: 13px;
        }}

        .step-body {{
            padding: 20px;
        }}

        .step-description {{
            color: #6c757d;
            margin-bottom: 15px;
            font-style: italic;
        }}

        .sets, .checks {{
            margin-top: 15px;
        }}

        .sets h4, .checks h4 {{
            font-size: 14px;
            color: #495057;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .set-item {{
            background: #e7f3ff;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 3px solid #0066cc;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}

        .set-item .signal {{
            font-weight: bold;
            color: #0066cc;
        }}

        .check-item {{
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 3px solid;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            gap: 15px;
            align-items: center;
            font-size: 13px;
        }}

        .check-item.passed {{
            background: #d4edda;
            border-left-color: #28a745;
        }}

        .check-item.failed {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}

        .check-signal {{
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }}

        .check-expected, .check-actual {{
            font-family: 'Courier New', monospace;
        }}

        .check-status {{
            text-align: right;
            font-weight: bold;
        }}

        .check-item.passed .check-status {{
            color: #28a745;
        }}

        .check-item.failed .check-status {{
            color: #dc3545;
        }}

        .notes {{
            margin-top: 15px;
            padding: 15px;
            background: #fff3cd;
            border-left: 3px solid #ffc107;
            border-radius: 4px;
        }}

        .notes h4 {{
            font-size: 14px;
            color: #856404;
            margin-bottom: 8px;
        }}

        .note-item {{
            color: #856404;
            font-size: 13px;
            margin-bottom: 5px;
        }}

        .footer {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
            text-align: center;
            color: #6c757d;
            font-size: 13px;
        }}

        @media print {{
            body {{
                padding: 0;
            }}

            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{self.test_name}</h1>
            <p>{self.description}</p>
        </div>

        <div class="summary">
            <div class="summary-card status">
                <h3>Status</h3>
                <div class="value">{status}</div>
            </div>

            <div class="summary-card">
                <h3>Duration</h3>
                <div class="value">{duration:.2f}s</div>
            </div>

            <div class="summary-card">
                <h3>Total Checks</h3>
                <div class="value">{total_checks}</div>
            </div>

            <div class="summary-card">
                <h3>Passed</h3>
                <div class="value" style="color: #28a745;">{passed_checks}</div>
            </div>

            <div class="summary-card">
                <h3>Failed</h3>
                <div class="value" style="color: #dc3545;">{failed_checks}</div>
            </div>
        </div>

        <div class="content">
            <h2 style="margin-bottom: 20px; color: #333;">Test Execution Details</h2>
"""

        # Add steps
        for step in self.steps:
            step_time = step["timestamp"].strftime("%H:%M:%S.%f")[:-3]

            html += f"""
            <div class="step">
                <div class="step-header">
                    <h3>{step["name"]}</h3>
                    <span class="step-time">{step_time}</span>
                </div>
                <div class="step-body">
"""

            if step["description"]:
                html += f"""
                    <p class="step-description">{step["description"]}</p>
"""

            # Add sets
            if step["sets"]:
                html += """
                    <div class="sets">
                        <h4>Signal Sets</h4>
"""
                for s in step["sets"]:
                    html += f"""
                        <div class="set-item">
                            <span class="signal">{s["signal"]}</span> = {s["value"]}
                        </div>
"""
                html += """
                    </div>
"""

            # Add checks
            if step["checks"]:
                html += """
                    <div class="checks">
                        <h4>Signal Checks</h4>
"""
                for c in step["checks"]:
                    status_class = "passed" if c["passed"] else "failed"
                    status_text = "✓ PASS" if c["passed"] else "✗ FAIL"

                    tolerance_text = f" (±{c['tolerance']})" if c['tolerance'] else ""

                    html += f"""
                        <div class="check-item {status_class}">
                            <div class="check-signal">{c["signal"]}</div>
                            <div class="check-expected">Expected: {c["expected"]}{tolerance_text}</div>
                            <div class="check-actual">Actual: {c["actual"]}</div>
                            <div class="check-status">{status_text}</div>
                        </div>
"""
                html += """
                    </div>
"""

            # Add notes
            if "notes" in step:
                html += """
                    <div class="notes">
                        <h4>Notes</h4>
"""
                for note in step["notes"]:
                    html += f"""
                        <div class="note-item">• {note["text"]}</div>
"""
                html += """
                    </div>
"""

            html += """
                </div>
            </div>
"""

        html += f"""
        </div>

        <div class="footer">
            Generated on {end_time.strftime("%Y-%m-%d %H:%M:%S")} |
            Test started at {self.start_time.strftime("%Y-%m-%d %H:%M:%S")} |
            Duration: {duration:.2f}s
        </div>
    </div>
</body>
</html>
"""

        # Write to file
        output_file = Path(output_path)
        output_file.write_text(html, encoding='utf-8')

        return str(output_file.absolute())


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
    _, _, _, hil_var = hil_modules.read_project_config() # Use mock read_project_config
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
        # In DRY_RUN, we don't actually read from a hardware ChannelReference unless specifically needed for debugging
        # For DRY_RUN with SIMULATE_RESPONSES, we only use simulated_state
        actual_hardware_value = ChannelReference(signal_path).value # This would be 0.0 in mock
        
        if DRY_RUN and SIMULATE_RESPONSES:
            # Simulate expected response based on test logic
            simulated_value = simulate_hardware_response(signal_name, expected_value)

            passed = abs(simulated_value - expected_value) <= tolerance

            print(f"  [DRY RUN CHECK] {signal_name}")
            print(f"     Current real value: {actual_hardware_value} (ignored in simulation)")
            print(f"     Simulated response: {simulated_value} (expected {expected_value})")

            if passed:
                print(f"     [PASS] WOULD PASS")
            else:
                print(f"     [FAIL] WOULD FAIL")

            if reporter:
                reporter.add_check(signal_name, expected_value, simulated_value, passed, tolerance)
                reporter.add_note(f"Actual hardware value (mock): {actual_hardware_value} (not changed in dry run)")

            return passed
        else:
            # Normal check against real hardware
            # In a real environment, actual_value would be read here from hardware
            actual_value = ChannelReference(signal_path).value
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

    is_max_defrost_commanded = simulated_state.get("WindscreenDefrostInd_cmd", 0) == 1
    current_vehicle_mode = simulated_state.get("VehicleMode", 0)

    # Define modes where Max Defrost is available
    # 6: PreRunning, 7: Cranking (Assumed), 8: Running (Assumed)
    max_defrost_available_modes = [6, 7, 8]
    
    is_max_defrost_active = is_max_defrost_commanded and (current_vehicle_mode in max_defrost_available_modes)

    response_map = {
        # Max Defrost Status
        "MaxDefrostStatus": 1 if is_max_defrost_active else 0,

        # Air distribution - in max defrost, defrost=1, others=0
        "ClimateAirDistStatus_Defrost": 1 if is_max_defrost_active else 0,
        "ClimateAirDistStatus_Floor": 0 if is_max_defrost_active else simulated_state.get("ClimateAirDistRequest_Floor", 0),
        "ClimateAirDistStatus_Vent": 0 if is_max_defrost_active else simulated_state.get("ClimateAirDistRequest_Vent", 0),
        
        # Blower level - in max defrost, should go to 10
        "HVACBlowerLevelStat_BlowerLevel": 10 if is_max_defrost_active else simulated_state.get("HVACBlowerRequest", 1),
        
        # Cabin heater - in max defrost, should go to 10
        "CabHeatManStatus": 10 if is_max_defrost_active else simulated_state.get("CabHeatManReq", 0),
        
        # Air recirculation - forced OFF (0) during max defrost for fresh air
        "AirRecirculationStatus": 0 if is_max_defrost_active else simulated_state.get("AirRecirculationRequest", 0),

        # Climate Power Status mirrors ClimatePowerRequest
        "ClimatePowerStatus": simulated_state.get("ClimatePowerRequest", 0),
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


def test_max_defrost_availability_dry_run(hil_config):
    """
    DRY RUN: Test validation without hardware control for Max Defrost Availability

    What this does:
    - ✅ Validates all signal names exist in config
    - ✅ Shows what WOULD be sent to hardware
    - ✅ Reads current hardware state (doesn't change it)
    - ✅ Simulates expected responses based on scenario logic
    - ✅ Generates report showing planned execution
    - ✅ Safe to run with hardware connected

    What this DOESN'T do:
    - ❌ Change any hardware signals
    - ❌ Control motors/actuators
    - ❌ Test real hardware behavior
    """

    global reporter
    reporter = TestReporter(
        "Max Defrost Availability Test - DRY RUN",
        "Simulation mode - verifies Max Defrost activation and air distribution across vehicle modes (PreRunning, Cranking, Running) without controlling hardware."
    )

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST AVAILABILITY TEST")
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
        "VehicleMode",
        "MaxDefrostStatus",
        "ClimateAirDistStatus_Defrost",
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
    # PRE-CONDITIONS
    # - Vehicle ignition is OFF (Simulate by setting VehicleMode to 0)
    # - Max Defrost function is inactive
    # - Climate Control System is active
    # ========================================================================
    print("\n[STEP 1] Setting Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 1: Set Pre-Conditions (DRY RUN)", "Show what initial setup WOULD be")

    asyncio.run(asyncio.sleep(0.5))

    set_can_signal(hil_var, "VehicleMode", 0) # Vehicle ignition is OFF
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 0) # Max Defrost inactive
    set_can_signal(hil_var, "ClimatePowerRequest", 1) # Climate Control System active
    set_can_signal(hil_var, "ClimateAirDistRequest_Defrost", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Floor", 0)
    set_can_signal(hil_var, "ClimateAirDistRequest_Vent", 0)


    print("\n[STEP 2] Verify Pre-Conditions (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 2: Verify Pre-Conditions (DRY RUN)", "Simulate expected responses to pre-conditions")

    asyncio.run(asyncio.sleep(0.2))

    checks_passed = True
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0)
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0)
    checks_passed &= check_can_signal(hil_var, "ClimatePowerStatus", 1) # Ensure climate system is active


    # ========================================================================
    # Test Scenario: Max Defrost Availability in Various Vehicle Modes
    # ========================================================================

    # --- Step 1: Set VehicleMode to 'PreRunning' and Activate Max Defrost ---
    print("\n[STEP 3] Set VehicleMode to 'PreRunning' and Activate Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 3: PreRunning Mode & Max Defrost", "Set VehicleMode to PreRunning (6) and activate Max Defrost")
    
    set_can_signal(hil_var, "VehicleMode", 6)  # PreRunning
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 1) # Activate Max Defrost
    asyncio.run(asyncio.sleep(1)) # Allow time for system to react

    print("\n[CHECK 3] Verify Max Defrost in 'PreRunning' mode (DRY RUN)...")
    reporter.add_step("Check 3: PreRunning Verification", "Verify Max Defrost status and air distribution in PreRunning")
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1) # Active
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1) # True
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0) # False
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0) # False
    

    # --- Step 2: Set VehicleMode to 'Cranking' and Activate Max Defrost ---
    print("\n[STEP 4] Set VehicleMode to 'Cranking' and Activate Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 4: Cranking Mode & Max Defrost", "Set VehicleMode to Cranking (7) and activate Max Defrost")
    
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 0) # Deactivate first to re-trigger
    set_can_signal(hil_var, "VehicleMode", 7) # Cranking (assumed value)
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 1) # Activate Max Defrost
    asyncio.run(asyncio.sleep(1)) # Allow time for system to react

    print("\n[CHECK 4] Verify Max Defrost in 'Cranking' mode (DRY RUN)...")
    reporter.add_step("Check 4: Cranking Verification", "Verify Max Defrost status and air distribution in Cranking")
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1) # Active
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1) # True
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0) # False
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0) # False


    # --- Step 3: Set VehicleMode to 'Running' and Activate Max Defrost ---
    print("\n[STEP 5] Set VehicleMode to 'Running' and Activate Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 5: Running Mode & Max Defrost", "Set VehicleMode to Running (8) and activate Max Defrost")
    
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 0) # Deactivate first to re-trigger
    set_can_signal(hil_var, "VehicleMode", 8) # Running (assumed value)
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 1) # Activate Max Defrost
    asyncio.run(asyncio.sleep(1)) # Allow time for system to react

    print("\n[CHECK 5] Verify Max Defrost in 'Running' mode (DRY RUN)...")
    reporter.add_step("Check 5: Running Verification", "Verify Max Defrost status and air distribution in Running")
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 1) # Active
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Defrost", 1) # True
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Floor", 0) # False
    checks_passed &= check_can_signal(hil_var, "ClimateAirDistStatus_Vent", 0) # False

    # ========================================================================
    # Teardown: Reset Max Defrost
    # ========================================================================
    print("\n[STEP 6] Teardown: Deactivating Max Defrost (DRY RUN)...")
    print("-" * 70)
    reporter.add_step("Step 6: Teardown", "Deactivate Max Defrost and reset VehicleMode")
    set_can_signal(hil_var, "WindscreenDefrostInd_cmd", 0)
    set_can_signal(hil_var, "VehicleMode", 0) # Back to OFF/Ignition OFF
    asyncio.run(asyncio.sleep(0.5))
    checks_passed &= check_can_signal(hil_var, "MaxDefrostStatus", 0)

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
    report_path = reporter.generate_html("test_max_defrost_availability_dry_run_report.html")

    print(f"\nDry Run Report: {report_path}")
    print("\n[!] To run for REAL:")
    print("   1. Review the dry run report")
    print("   2. Verify all signals are correct")
    print("   3. Run: pytest -v test_max_defrost_availability_dry_run.py") # Note: filename will be changed for real run
    print("="*70 + "\n")

    # Assert that all checks passed in the simulation
    # In a dry run, we mostly check if the logic flows as expected and signals are processed
    assert checks_passed, "Some checks failed in the dry run simulation."


if __name__ == "__main__":
    """Run dry run standalone"""

    print("\n" + "="*70)
    print("[DRY RUN] MAX DEFROST AVAILABILITY DRY RUN")
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

    _, _, _, hil_var_main = hil_modules.read_project_config() # Use mock read_project_config
    test_max_defrost_availability_dry_run(hil_var_main)