# Test Type: AUTOMATED
(Reason: Both `MaxDefrostStatus` and `AirRecirculationStatus` signals were found in the database.)

# Scenario: Max Defrost Activates, Recirculation Turns Off
**Description:** Verify that while Max Defrost is activated, the Thermal System uses outside air only by ensuring air recirculation is turned off.
**Pre-conditions:**
- Max Defrost is inactive.
- Air recirculation is active.
- Vehicle is in "Running" mode.
**Trigger:** Driver requests activation of Max Defrost.
**Steps:**
1. Set `MaxDefrostStatus` to 0.
2. Set `AirRecirculationStatus` to 1.
3. Set `MaxDefrostStatus` to 1.
**Expected Outcome:**
- `MaxDefrostStatus` == 1
- `AirRecirculationStatus` == 0