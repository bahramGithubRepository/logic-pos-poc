# Test Type: AUTOMATED
*(Reason: All required signals (MaxDefrostStatus, CabHeatManStatus) were found in the database.)*

# Scenario: Thermal System Requests Max Heating During Max Defrost Activation
**Description:** Verify that the Thermal System requests maximum heating when Max Defrost is activated.
**Pre-conditions:**
- Vehicle is in a state where Max Defrost can be activated (e.g., Running).
- Climate Control System is operational.
**Trigger:** Max Defrost is activated.
**Steps:**
1. Set `MaxDefrostStatus` to 1.
**Expected Outcome:**
- `CabHeatManStatus` == 15