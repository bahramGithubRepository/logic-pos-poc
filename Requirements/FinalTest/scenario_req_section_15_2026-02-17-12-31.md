# Test Type: AUTOMATED
*(Reason: `PS_MaxDefrostStatus` and `HVACBlowerLevelStat_BlowerLevel` signals were found in the database. `CabHeatManStatus` was not found and will require manual verification.)*

# Scenario: Max Defrost Deactivation upon Air Distribution Change
**Description:** Verify that when Max Defrost is active and the Driver Experience System changes the air distribution, the Thermal System deactivates Max Defrost, sets the blower level to maximum, and the temperature level to maximum.
**Pre-conditions:**
- Max Defrost is active.
- Driver Experience System is active.
**Trigger:** Driver Experience System changes air distribution from Defrost/Side Defrost to another mode (e.g., Floor or Vent).
**Steps:**
1. Ensure Max Defrost is active.
2. Change the air distribution from Defrost/Side Defrost to a different distribution mode (e.g., Floor or Vent) using the Driver Experience System.
**Expected Outcome:**
- `PS_MaxDefrostStatus` == 0 (Off)
- `HVACBlowerLevelStat_BlowerLevel` == 31 (Maximum Level)
- `CabHeatManStatus` == Maximum Level (Note: Signal missing from DB; manual verification required)