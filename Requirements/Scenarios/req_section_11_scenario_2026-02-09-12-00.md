# Test Type: AUTOMATED
(Reason: Both `MaxDefrostStatus` and `AirRecirculationStatus` signals were found in the database.)

# Scenario: Max Defrost Activates Outside Air Only
**Description:** Verify that when Max Defrost is activated, the Thermal System uses 0% recirculation (outside air only).
**Pre-conditions:**
- Vehicle is in a valid operational mode (e.g., Running).
- Thermal system is functional.
**Trigger:** Max Defrost is activated.
**Steps:**
1. Set the vehicle operating mode to 'Running'.
2. Set the signal `MaxDefrostStatus` to 1 (On) to activate Max Defrost.
3. Observe the `AirRecirculationStatus` signal.
**Expected Outcome:**
- `MaxDefrostStatus` == 1
- `AirRecirculationStatus` == 0