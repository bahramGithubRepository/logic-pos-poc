# Test Type: AUTOMATED
(Reason: All required signals (MaxDefrostRequest, MaxDefrostStatus, CabHeatManStatus) were found in the database.)

# Scenario: Max Defrost Activates Max Heating Request
**Description:** Verify that when Max Defrost is activated, the Thermal System requests maximum heating.
**Pre-conditions:** Vehicle operating mode is "Running" or equivalent state where Max Defrost can be activated.
**Trigger:** Driver Experience System sends a request to activate Max Defrost.
**Steps:**
1. Set `MaxDefrostRequest` to '1' (Activate Max Defrost).
2. Monitor system signals for response.
**Expected Outcome:**
- `MaxDefrostStatus` == '1' (On)
- `CabHeatManStatus` == '15' (Maximum heating level)