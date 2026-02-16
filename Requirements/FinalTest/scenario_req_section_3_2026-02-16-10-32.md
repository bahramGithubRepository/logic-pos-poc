# Test Type: AUTOMATED
(Reason: All necessary signals (`VehicleMode`, `WindscreenDefrostInd_cmd`, `MaxDefrostStatus`, `ClimateAirDistStatus_Defrost`, `ClimateAirDistStatus_Floor`, `ClimateAirDistStatus_Vent`) are available in the database to verify Max Defrost availability and air distribution according to the requirements.)

# Scenario: Max Defrost Availability in Various Vehicle Modes
**Description:** Verify that the Max Defrost function becomes available for activation when the vehicle is in PreRunning, Cranking, or Running modes, and that the air distribution is correctly set to Defrost/Side Defrost with Floor and Vent modes off.
**Pre-conditions:**
- Vehicle ignition is OFF.
- Max Defrost function is inactive.
- Climate Control System is active.
**Trigger:** Vehicle Mode changes to PreRunning, Cranking, or Running, followed by an activation request for Max Defrost.
**Steps:**
1. Set `VehicleMode` to 'PreRunning'.
2. Set `WindscreenDefrostInd_cmd` to '1' (Activate Max Defrost).
3. Set `VehicleMode` to 'Cranking'.
4. Set `WindscreenDefrostInd_cmd` to '1' (Activate Max Defrost).
5. Set `VehicleMode` to 'Running'.
6. Set `WindscreenDefrostInd_cmd` to '1' (Activate Max Defrost).

**Expected Outcome:**
- When `VehicleMode` == 'PreRunning' AND `WindscreenDefrostInd_cmd` == '1':
    - `MaxDefrostStatus` == 'Active'
    - `ClimateAirDistStatus_Defrost` == 'True'
    - `ClimateAirDistStatus_Floor` == 'False'
    - `ClimateAirDistStatus_Vent` == 'False'
- When `VehicleMode` == 'Cranking' AND `WindscreenDefrostInd_cmd` == '1':
    - `MaxDefrostStatus` == 'Active'
    - `ClimateAirDistStatus_Defrost` == 'True'
    - `ClimateAirDistStatus_Floor` == 'False'
    - `ClimateAirDistStatus_Vent` == 'False'
- When `VehicleMode` == 'Running' AND `WindscreenDefrostInd_cmd` == '1':
    - `MaxDefrostStatus` == 'Active'
    - `ClimateAirDistStatus_Defrost` == 'True'
    - `ClimateAirDistStatus_Floor` == 'False'
    - `ClimateAirDistStatus_Vent` == 'False'