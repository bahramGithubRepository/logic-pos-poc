# Test Type: AUTOMATED
*(Reason: The signals `MaxDefrostStatus` and `ClimateAirDistStatus_Defrost` were found in the database, allowing for automated verification of the system behavior.)*

# Scenario: Max Defrost Air Distribution to Defrost Only Mode
**Description:** Verify that when Max Defrost is activated, the Thermal System correctly sets the air distribution to defrost only mode.
**Pre-conditions:**
- Vehicle is in "Running" mode.
- Max Defrost is currently deactivated (`MaxDefrostStatus == 0`).
**Trigger:**
- Activate Max Defrost via driver input.
**Steps:**
1. Set `MaxDefrostStatus` to `1`.
**Expected Outcome:**
- `MaxDefrostStatus == 1`
- `ClimateAirDistStatus_Defrost == 1`