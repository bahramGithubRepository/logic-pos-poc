# Test Type: AUTOMATED
(Reason: All necessary signals (`VehicleMode`, `MaxDefrostRequest`, `MaxDefrostStatus`) were found in the database, allowing for automated testing of Max Defrost function availability across specified vehicle modes.)

# Scenario: Max Defrost Availability in Valid Vehicle Modes
**Description:** Verify that the Max Defrost function is available for activation when the vehicle is in PreRunning, Cranking, or Running modes.
**Pre-conditions:**
- Vehicle is in a state where Max Defrost is currently inactive.
- `MaxDefrostRequest` == `FALSE`
- `MaxDefrostStatus` == `Inactive`
**Trigger:**
- Set `MaxDefrostRequest` to `TRUE`.
**Steps:**
1. Set `VehicleMode` to `PreRunning`.
2. Set `MaxDefrostRequest` to `TRUE`.
3. Set `MaxDefrostRequest` to `FALSE`.
4. Set `VehicleMode` to `Cranking`.
5. Set `MaxDefrostRequest` to `TRUE`.
6. Set `MaxDefrostRequest` to `FALSE`.
7. Set `VehicleMode` to `Running`.
8. Set `MaxDefrostRequest` to `TRUE`.
**Expected Outcome:**
- When `VehicleMode` == `PreRunning` and `MaxDefrostRequest` == `TRUE`, then `MaxDefrostStatus` == `Active`.
- When `VehicleMode` == `Cranking` and `MaxDefrostRequest` == `TRUE`, then `MaxDefrostStatus` == `Active`.
- When `VehicleMode` == `Running` and `MaxDefrostRequest` == `TRUE`, then `MaxDefrostStatus` == `Active`.