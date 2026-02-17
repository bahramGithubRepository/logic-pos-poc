# Test Type: AUTOMATED
(Reason: The core trigger signal `MaxDefrostRequest` is available in the database. The `MaxDefrostStatus` signal is also found. Although `ACStatus` is missing, the test can still be automated with a manual verification note for the missing signal.)

# Scenario: Activation of Max Defrost and Automatic AC Function
**Description:** Verify that when Max Defrost is activated, the Thermal System reports Max Defrost status as On and attempts to activate the AC function with the lowest allowed evaporator reference temperature.
**Pre-conditions:**
- Vehicle is in Running mode.
- Thermal System is operational.
- Ambient temperature allows AC activation.
**Trigger:** Driver activates Max Defrost.
**Steps:**
1. Set `MaxDefrostRequest` to `1` (On).
2. Wait for the system to process the request.
**Expected Outcome:**
- `MaxDefrostStatus` == `1` (On)
- `ACStatus` == `1` (On) (Note: Signal missing from DB; manual verification required)