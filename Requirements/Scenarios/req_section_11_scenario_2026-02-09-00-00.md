# Test Type: AUTOMATED
(Reason: Signals `MaxDefrostStatus` and `AirRecirculationStatus` are found in the database.)

# Scenario: Max Defrost Activation and Air Recirculation
**Description:** Verify that when Max Defrost is activated, the Thermal System uses 0% recirculation (outside air only).
**Pre-conditions:**
- Vehicle is in "Running" mode.
- Max Defrost is currently inactive (`MaxDefrostStatus = 0`).
- Air Recirculation is currently active (`AirRecirculationStatus = 1`).
**Trigger:** Max Defrost is activated.
**Steps:**
1. Set `MaxDefrostStatus` to 1 (On).
2. Observe the value of `AirRecirculationStatus`.
**Expected Outcome:**
- `MaxDefrostStatus` == 1
- `AirRecirculationStatus` == 0