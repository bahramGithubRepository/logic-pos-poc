import pytest
import asyncio
from niveristand.clientapi import ChannelReference
from ConnectionToHil.hil_modules import connect_hil, read_project_config

# --------------------------------------------------------------------------
# FIXTURE: Handles HIL Connection for this specific test module
# --------------------------------------------------------------------------
@pytest.fixture(scope="module")
def hil_system():
    # 1. Connect to the HIL Rig
    ws, sys_addr = connect_hil()
    assert ws is not None, "Failed to connect to VeriStand"
    
    # 2. Get the Signal Map (Variables) from JSON
    project_path, calibration_file, sys_addr, hil_var = read_project_config()
    
    yield ws, hil_var  # Pass workspace and variables to the test
    
    # 3. Teardown: Disconnect is handled safely by hil_modules, 
    # but we can reset signals here if needed.

# --------------------------------------------------------------------------
# TEST CASE: Max Defrost Activation Logic
# --------------------------------------------------------------------------
def test_max_defrost_activation(hil_system):
    ws, hil_var = hil_system
    
    # --- STEP 1: SETUP (Pre-conditions) ---
    print("\n[Step 1] Setting Vehicle to RUNNING mode...")
    # Map abstract name "VehicleMode" to physical CAN signal
    veh_mode_sig = ChannelReference(hil_var["CAN_OUT"]["VehicleMode"])
    veh_mode_sig.value = 6  # Assuming 6 = Running (based on basic_test.py)
    
    # Ensure Defrost is currently OFF to start
    defrost_req_sig = ChannelReference(hil_var["CAN_OUT"]["MaxDefrostRequest"])
    defrost_req_sig.value = 0
    
    asyncio.run(asyncio.sleep(2)) # Wait for system to settle

    # --- STEP 2: TRIGGER (Action) ---
    print("[Step 2] Requesting Max Defrost (Request = 1)...")
    defrost_req_sig.value = 1
    
    # Wait for the HIL loop to process the logic (Simulating ECU reaction time)
    asyncio.run(asyncio.sleep(3))

    # --- STEP 3: VERIFY (Assertions) ---
    print("[Step 3] Verifying Feedback Signals...")
    
    # 3.1 Verify Status Feedback
    # We read the "CAN_IN" signal coming back from the ECU
    defrost_stat_sig = ChannelReference(hil_var["CAN_IN"]["MaxDefrostStatus"])
    curr_status = defrost_stat_sig.value
    assert curr_status == 1.0, f"Expected MaxDefrostStatus=1, but got {curr_status}"
    
    # 3.2 Verify Recirculation Logic (Requirement: 0% Recirculation)
    # Check logical status
    recirc_stat_sig = ChannelReference(hil_var["CAN_IN"]["AirRecirculationStatus"])
    curr_recirc = recirc_stat_sig.value
    assert curr_recirc == 0.0, f"Expected RecirculationStatus=0 (Fresh Air), got {curr_recirc}"
    
    # 3.3 Verify Physical Actuator Movement (HIL Specific)
    # We check the LIN Bus signal going to the physical motor
    # Actuator 1 is defined as "Recirculation" in the PDF
    act1_pos_sig = ChannelReference(hil_var["LIN"]["HVACAct1Cmd_FPOS"])
    curr_act1_pos = act1_pos_sig.value
    
    # Validating the requirement "0% Recirculation"
    # We allow a small tolerance (e.g. 0.0 to 1.0) because motors jitter
    assert 0.0 <= curr_act1_pos <= 1.0, f"Expected Actuator 1 (Recirc) to be at 0%, got {curr_act1_pos}%"

    print("SUCCESS: Max Defrost Logic Verified on HIL Hardware.")
