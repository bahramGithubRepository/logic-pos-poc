# Test Type: AUTOMATED
*(Reason: All relevant signals (MaxDefrostStatus, AirRecirculationRequest, AirRecirculationStatus, MaxDefrostRequest) required by the system requirement are found in the database. The system requirement explicitly states to "keep Max Defrost active" during manual recirculation activation/deactivation, overriding general rules about recirculation deactivating Max Defrost from the technical context for this specific scenario.)*

# Scenario: Manual Recirculation Activation/Deactivation during Active Max Defrost
**Description:** Verify that when Max Defrost is active, the system correctly activates and deactivates manual recirculation as requested by the Driver Experience system, while ensuring Max Defrost remains active.
**Pre-conditions:**
- Max Defrost is active (`MaxDefrostRequest` was previously set to 1, and `MaxDefrostStatus` is 1).
- Air recirculation is initially disabled (`AirRecirculationRequest` is 1 or 0, `AirRecirculationStatus` is 0).
**Trigger:** Driver Experience system requests activation/deactivation of Manual recirculation.
**Steps:**
1.  Set `MaxDefrostRequest = 1` to ensure Max Defrost is active.
2.  Request manual recirculation activation: Set `AirRecirculationRequest = 2` (Enable).
3.  Request manual recirculation deactivation: Set `AirRecirculationRequest = 1` (Disable).

**Expected Outcome:**
- **After Step 1 (Pre-condition setup and verification):**
    - `MaxDefrostStatus == 1`
    - `AirRecirculationStatus == 0`
- **After Step 2 (Manual recirculation activation):**
    - `MaxDefrostStatus == 1`
    - `AirRecirculationStatus == 1`
- **After Step 3 (Manual recirculation deactivation):**
    - `MaxDefrostStatus == 1`
    - `AirRecirculationStatus == 0`