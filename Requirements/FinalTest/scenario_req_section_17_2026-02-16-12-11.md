# Test Type: AUTOMATED
*(Reason: All required signals (MaxDefrostStatus, CabHeatManReq, CabHeatManStatus) were found in the database.)*

# Scenario: Max Defrost Heat Level Change
**Description:** Verify that when Max Defrost is active and the Driver Experience System has changed the Heat Level setting (Except to LO/MIN), the Thermal System shall change Heat Level setting accordingly, keep Max Defrost active and store Heat Level setting.
**Pre-conditions:**
- Max Defrost is active.
- Vehicle is in 'Running' mode.
**Trigger:**
- Driver Experience System changes the `CabHeatManReq` signal to a value other than 'LO' or 'MIN'.
**Steps:**
1.  Ensure the system is in a state where Max Defrost is active.
2.  Set `CabHeatManReq` = 5 (assuming 0-15 range, 5 is an intermediate heat level, not LO/MIN).
3.  Wait for a sufficient period for the system to process the change.
**Expected Outcome:**
- `MaxDefrostStatus` == 1 (On)
- `CabHeatManStatus` == 5