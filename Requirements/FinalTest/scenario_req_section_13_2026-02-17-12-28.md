# Test Type: AUTOMATED
(Reason: Core trigger signal 'MaxDefrostRequest' is available in the database. Output status signals for air distribution and blower level are also available. Output status signals for recirculation, temperature, and AC settings are not directly found and will require manual verification.)

# Scenario: Max Defrost Deactivation and Manual Settings Restoration
**Description:** Verify that when Max Defrost is deactivated by button, previously active manual HVAC settings (Recirculation, Air distribution, Temperature, Blower, AC) are restored to their values before Max Defrost activation, given that these manual settings were active and not changed during Max Defrost operation.

**Pre-conditions:**
*   Vehicle is in a mode where Max Defrost can be active (e.g., Running).
*   Initial manual settings are configured and active (e.g., Recirculation ON, Floor/Vent distribution, specific Temperature, specific Blower level, AC ON).
*   Max Defrost is currently active.

**Trigger:** Driver Experience System requests deactivation of Max Defrost by button.

**Steps:**
1.  Ensure pre-conditions are met: Max Defrost is active, and prior manual settings are stored/active.
2.  Set `MaxDefrostRequest` to 0 (Off).

**Expected Outcome:**
- `MaxDefrostStatus` == 0 (Off)
- Restore Recirculation setting:
    - `RecirculationStatus` == [Value before Max Defrost] (Note: Signal missing from DB; manual verification required)
- Restore Air distribution setting:
    - `ClimateAirDistStatus_Defrost` == [Value before Max Defrost]
    - `ClimateAirDistStatus_Floor` == [Value before Max Defrost]
    - `ClimateAirDistStatus_Vent` == [Value before Max Defrost]
- Restore Temperature setting:
    - `CabinTempStatus` == [Value before Max Defrost] (Note: Signal missing from DB; manual verification required)
- Restore Blower setting:
    - `HVACBlowerLevelStat_BlowerLevel` == [Value before Max Defrost]
- Restore AC setting:
    - `ACStatus` == [Value before Max Defrost] (Note: Signal missing from DB; manual verification required)