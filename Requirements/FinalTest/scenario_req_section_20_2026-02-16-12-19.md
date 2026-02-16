# Test Type: AUTOMATED
(Reason: Key signals for Max Defrost activation/deactivation, air distribution, blower speed, recirculation, AC, and vehicle mode are available in the database. The core functionality can be verified.)

# Scenario: Max Defrost Activation and User Deactivation
**Description:** Verify that the Max Defrost function activates correctly when requested by the user and deactivates when the user explicitly turns it off via the Max Defrost button.
**Pre-conditions:**
- Vehicle in 'Running' mode.
- Ambient temperature allows AC to be active (e.g., above 0°C).
- Climate control system is ON.
**Trigger:** Max Defrost button pressed by the user.
**Steps:**
1. Set `VehicleMode` to 'Running'.
2. Set `ClimatePowerRequest` to 'ON'.
3. Set `MaxDefrostRequest` to 'ACTIVE'.
4. Verify system response.
5. Set `MaxDefrostRequest` to 'INACTIVE' (user deactivates).
6. Verify system response after deactivation.
**Expected Outcome:**
- **Step 4 (After Activation):**
    - `MaxDefrostStatus` == 'ACTIVE'
    - `Recirc_ButtonStatus` == 'OFF' (Fresh air mode)
    - `AC_ButtonStatus` == 'ON' (AC activated)
    - `ClimateAirDistStatus_Defrost` == 'ACTIVE'
    - `ClimateAirDistStatus_Floor` == 'INACTIVE'
    - `ClimateAirDistStatus_Vent` == 'INACTIVE'
    - `HVACBlowerLevelStat_BlowerLevel` == 'MAXIMUM' (Highest possible)
- **Step 6 (After Deactivation):**
    - `MaxDefrostStatus` == 'INACTIVE'