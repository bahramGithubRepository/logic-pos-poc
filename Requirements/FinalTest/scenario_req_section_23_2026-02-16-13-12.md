# Test Type: AUTOMATED
(Reason: All required signals, including `VehicleMode`, `MaxDefrostRequest`, `MaxDefrostStatus`, `ClimateAirDistStatus_Defrost`, `ClimateAirDistStatus_Floor`, and `ClimateAirDistStatus_Vent`, were found in the database. Input signals like `MaxDefrostRequest` and `VehicleMode` can be set, and output signals like `MaxDefrostStatus` and `ClimateAirDistStatus` can be monitored to verify the behavior.)

# Scenario: Max Defrost Activation Maintained After Vehicle Mode Change
**Description:** Verify that Max Defrost activation is maintained when the vehicle mode transitions from Pre-Running to Running.
**Pre-conditions:**
- The Thermal System is initialized and operational.
- Vehicle is in "Pre-Running" mode. (`VehicleMode` = 'PreRunning')
- Max Defrost is not active. (`MaxDefrostStatus` = 0)
**Trigger:**
- Max Defrost is activated while the vehicle is in "Pre-Running" mode.
- Vehicle mode is subsequently changed from "Pre-Running" to "Running".
**Steps:**
1. Set `VehicleMode` to 'PreRunning'.
2. Set `MaxDefrostRequest` to 'Activate' (1).
3. Wait for the system to process the Max Defrost activation.
4. Set `VehicleMode` to 'Running'.
5. Wait for the system to stabilize after the vehicle mode change.
**Expected Outcome:**
- `MaxDefrostStatus` == 1 (On)
- `ClimateAirDistStatus_Defrost` == 100 (Flap_Defrost 100% Open)
- `ClimateAirDistStatus_Floor` == 0 (Flap_Foot 0% Closed)
- `ClimateAirDistStatus_Vent` == 0 (Flap_Center_Vent 0% Closed)