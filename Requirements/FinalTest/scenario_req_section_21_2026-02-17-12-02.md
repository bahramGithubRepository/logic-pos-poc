# Test Type: AUTOMATED
(Reason: All core trigger and most secondary verification signals (`MaxDefrostRequest`, `MaxDefrostStatus`, `Recirc_ButtonStatus`, `AC_ButtonStatus`, `CabTempRequest`, `HVACBlowerRequest`, `ClimateAirDistRequest_Defrost`, `ClimateAirDistRequest_Floor`, `ClimateAirDistRequest_Vent`, `HVACBlowerLevelStat_BlowerLevel`) are available in the database.)

# Scenario: Max Defrost Activation and Settings Verification
**Description:** Verify that when Max Defrost is requested, the Thermal system correctly sets recirculation to fresh air, air distribution to defrost only, AC to on, temperature to maximum, and blower speed to maximum.
**Pre-conditions:**
*   `VehicleMode` is set to "Running".
*   `MaxDefrostRequest` is 0 (Off).
*   Climate control is in a default state (e.g., `AC_ButtonStatus` = 0, `Recirc_ButtonStatus` = 0, `HVACBlowerRequest` at a nominal level, `CabTempRequest` at a nominal temperature, air distribution not solely defrost).
**Trigger:** Set `MaxDefrostRequest` to 1 (On).
**Steps:**
1.  Set `VehicleMode` to "Running".
2.  Set `MaxDefrostRequest` to 0.
3.  Set `Recirc_ButtonStatus` to 0 (Fresh air).
4.  Set `AC_ButtonStatus` to 0 (AC off).
5.  Set `CabTempRequest` to 22.0 (nominal temperature).
6.  Set `HVACBlowerRequest` to 50 (nominal level).
7.  Set `ClimateAirDistRequest_Defrost` to 0.
8.  Set `ClimateAirDistRequest_Floor` to 1.
9.  Set `ClimateAirDistRequest_Vent` to 1.
10. Set `MaxDefrostRequest` to 1.
**Expected Outcome:**
- `MaxDefrostStatus` == 1
- `Recirc_ButtonStatus` == 0
- `ClimateAirDistRequest_Defrost` == 1
- `ClimateAirDistRequest_Floor` == 0
- `ClimateAirDistRequest_Vent` == 0
- `AC_ButtonStatus` == 1
- `CabTempRequest` == 30.0 (Max Temperature Value, assuming 30.0 for this system)
- `HVACBlowerRequest` == 100 (Max Blower Speed Value, assuming 100% for this system)
- `HVACBlowerLevelStat_BlowerLevel` == 100 (Max Blower Speed Value, assuming 100% for this system)