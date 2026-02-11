# Test Type: AUTOMATED
(Reason: The signal `MaxDefrostStatus` was found directly. A functionally equivalent signal `ClimateAirDistStatus_Defrost` was found to verify the air distribution to defrost, which is crucial for the requirement.)

# Scenario: Max Defrost Air Distribution Verification
**Description:** Verify that when Max Defrost is activated, the Thermal System sets the air distribution to defrost-only mode (100% air to Defrost and Side Defrost).
**Pre-conditions:**
- Vehicle is in "Running" mode.
- Max Defrost is not active.
- `MaxDefrostStatus` == 0
- `ClimateAirDistStatus_Defrost` == 0 (or equivalent 'Off' state)
**Trigger:**
Set `MaxDefrostStatus` to 1 (On)
**Steps:**
1. Set vehicle mode to "Running".
2. Set `MaxDefrostStatus` to 1.
3. Wait for 5 seconds to allow the system to reach the commanded air distribution.
**Expected Outcome:**
- `MaxDefrostStatus` == 1
- `ClimateAirDistStatus_Defrost` == 1