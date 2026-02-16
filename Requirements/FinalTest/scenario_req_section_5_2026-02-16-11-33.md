# Test Type: AUTOMATED
(Reason: Both `MaxDefrostRequest` and `MaxDefrostStatus` signals were found in the database.)

# Scenario: Max Defrost Activation
**Description:** Verify that the Thermal System activates Max Defrost mode when requested by the Driver Experience System, and reports the correct status.
**Pre-conditions:**
- Vehicle in Running mode.
- Max Defrost is currently inactive.
**Trigger:** Driver Experience System requests Max Defrost activation.
**Steps:**
1. Set `MaxDefrostRequest` to 1.
**Expected Outcome:**
- `MaxDefrostStatus` == 1