# Test Type: AUTOMATED
(Reason: All required signals (MaxDefrostStatus, AirRecirculationStatus) were found in the database.)

# Scenario: Max Defrost Deactivates Manual Recirculation
**Description:** Verify that when Max Defrost is activated while manual recirculation is active, the manual recirculation is deactivated.
**Pre-conditions:**
- Vehicle in a mode allowing Max Defrost activation (e.g., Running, PreRunning, Crank for ICE, or Parked, Living, Accessory, Crank, PreRunning, Running for BEV).
- Manual recirculation is active.
**Trigger:** Max Defrost is activated.
**Steps:**
1. Ensure the vehicle is in a valid mode for Max Defrost activation.
2. Activate manual recirculation.
3. Activate Max Defrost.
**Expected Outcome:**
- MaxDefrostStatus == 1 (On)
- AirRecirculationStatus == 0 (Disabled)