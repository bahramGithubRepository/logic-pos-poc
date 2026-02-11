# Test Type: AUTOMATED
*(Reason: Both `MaxDefrostStatus` and `CabHeatManStatus` signals were found in the database, allowing for automated verification of the requirement.)*

# Scenario: Max Defrost Activates Max Heating
**Description:** Verify that the Thermal System requests maximum heating when Max Defrost is activated.
**Pre-conditions:**
The vehicle is in a Running state, allowing for Max Defrost activation and full thermal system functionality.
**Trigger:**
The `MaxDefrostStatus` signal is set to `1` (On).
**Steps:**
1. Set the vehicle operating mode to 'Running'.
2. Set `MaxDefrostStatus` to `1`.
**Expected Outcome:**
- `MaxDefrostStatus` == `1`
- `CabHeatManStatus` == `15`