# Test Type: AUTOMATED
Reason: Core trigger signal `HVACBlowerRequest` and primary verification signal `HVACBlowerLevelStat_BlowerLevel` are found in the database. The `MaxDefrostStatus` signal is missing, but its verification can be handled manually.

# Scenario: Blower Setting Change During Active Max Defrost
**Description:** Verify that when Max Defrost is active and the Driver Experience System requests a change in blower setting, the Thermal System updates the blower to the new level and maintains Max Defrost activation.
**Pre-conditions:**
- Max Defrost is active.
- Vehicle is in "Running" mode.
**Trigger:** Driver Experience System changes the blower setting.
**Steps:**
1. Set the vehicle mode to "Running".
2. Ensure Max Defrost is active.
3. Set `HVACBlowerRequest` to 20 (assuming a valid blower speed level).
**Expected Outcome:**
- `HVACBlowerLevelStat_BlowerLevel` == 20
- `MaxDefrostStatus` == 1 (On) (Note: Signal missing from DB; manual verification required)