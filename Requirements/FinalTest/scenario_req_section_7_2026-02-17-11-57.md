# Test Type: AUTOMATED
*(Reason: Core trigger 'MaxDefrostRequest' and blower speed status signal 'HVACBlowerLevelStat_BlowerLevel' are found in the database.)*

# Scenario: Activation of Max Defrost and Blower Speed to Maximum
**Description:** Verify that when Max Defrost is activated, the thermal system sets the blower speed to its maximum level.
**Pre-conditions:**
- Vehicle in Running mode.
- Max Defrost is not active.
**Trigger:** MaxDefrostRequest = 1 (On)
**Steps:**
1. Set `MaxDefrostRequest` to 0.
2. Set `MaxDefrostRequest` to 1.
3. Wait for the system to ramp up the blower speed to the requested level.
**Expected Outcome:**
- MaxDefrostRequest == 1
- MaxDefrostStatus == 1 (Note: Signal missing from DB; manual verification required)
- HVACBlowerLevelStat_BlowerLevel == 31