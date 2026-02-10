# Test Type: AUTOMATED
(Reason: The `VehicleMode` signal and `MaxDefrostRequest` and `MaxDefrostStatus` signals, which indicate the availability and activation of the Max Defrost function, are present in the database.)

# Scenario: Max Defrost Availability in PreRunning, Cranking, and Running Vehicle Modes
**Description:** Verify that the Max Defrost function is available for activation when the vehicle is in the specified valid vehicle modes: PreRunning, Cranking, and Running.
**Pre-conditions:**
- The vehicle system is operational.
- Max Defrost is currently inactive.
- `MaxDefrostRequest` == 'Deactivate'
- `MaxDefrostStatus` == 'Inactive'
**Trigger:** Change in `VehicleMode` followed by a request to activate Max Defrost.
**Steps:**
1. Set `VehicleMode` to 'PreRunning'.
2. Set `MaxDefrostRequest` to 'Activate'.
3. Set `VehicleMode` to 'Cranking'.
4. Set `MaxDefrostRequest` to 'Activate'.
5. Set `VehicleMode` to 'Running'.
6. Set `MaxDefrostRequest` to 'Activate'.
**Expected Outcome:**
- When `VehicleMode` == 'PreRunning' AND `MaxDefrostRequest` == 'Activate', then `MaxDefrostStatus` == 'Active'.
- When `VehicleMode` == 'Cranking' AND `MaxDefrostRequest` == 'Activate', then `MaxDefrostStatus` == 'Active'.
- When `VehicleMode` == 'Running' AND `MaxDefrostRequest` == 'Activate', then `MaxDefrostStatus` == 'Active'.