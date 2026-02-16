# Test Type: AUTOMATED
(Reason: The critical input signal (`WindscreenDefrost_ButtonStatus`) and output status signals (`MaxDefrostStatus`, `ClimateAirDistStatus_Defrost`, `ClimateAirDistStatus_Floor`, `ClimateAirDistStatus_Vent`) required to verify the core requirement are available in the database. `ActuatorRotationPercentage` and `VehicleMode` were not found and are noted as 'To Be Verified' as they relate to the underlying mechanism and broader system context rather than the direct verification of air distribution status.)

# Scenario: Max Defrost Air Distribution Verification
**Description:** Verify that when Max Defrost is activated, the Thermal System sets the air distribution to defrost only mode (100% air to Defrost and Side Defrost).
**Pre-conditions:**
- The vehicle is in a state where Max Defrost can be activated. (e.g., Running mode - `VehicleMode` signal is not directly settable, assumed to be in a valid state for this test).
- Max Defrost is not currently active (`WindscreenDefrost_ButtonStatus` == 0, `MaxDefrostStatus` == 0).
**Trigger:** Driver activates Max Defrost.
**Steps:**
1. Set `WindscreenDefrost_ButtonStatus` to 1 (pressed).
2. Allow sufficient time for the Thermal System to respond and stabilize air distribution.
**Expected Outcome:**
- `MaxDefrostStatus` == 1
- `ClimateAirDistStatus_Defrost` == 1
- `ClimateAirDistStatus_Floor` == 0
- `ClimateAirDistStatus_Vent` == 0