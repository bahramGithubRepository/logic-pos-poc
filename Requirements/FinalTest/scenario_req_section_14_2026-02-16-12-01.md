# Test Type: AUTOMATED
*(Reason: All required signals for setting and verifying HVAC functions and vehicle mode, including `AirRecirculationRequest`, `ClimateAirDistRequest_Defrost`, `ClimateAirDistRequest_Floor`, `ClimateAirDistRequest_Vent`, `CabTempRequest`, `HVACBlowerRequest`, `AC_ButtonStatus`, `MaxDefrostRequest`, `MaxDefrostStatus`, and `VehicleMode`, have been found in the database. `AirRecirculationRequest` is used for Recirculation setting, and `AC_ButtonStatus` is used to simulate AC activation/deactivation.)*

# Scenario: Max Defrost Deactivation and Settings Restoration on Vehicle Mode Change
**Description:** Verify that when Max Defrost is active and manual HVAC settings were active prior to Max Defrost, if the vehicle mode leaves "Running", the Thermal System deactivates Max Defrost and restores the previously active manual settings for recirculation, air distribution, temperature, blower, and AC.
**Pre-conditions:**
- `VehicleMode` == 3 (Running)
- `MaxDefrostRequest` == 0 (Off)
- `MaxDefrostStatus` == 0 (Off)
- `AirRecirculationRequest` == 0 (Fresh Air, manual setting)
- `ClimateAirDistRequest_Defrost` == 0
- `ClimateAirDistRequest_Floor` == 1
- `ClimateAirDistRequest_Vent` == 0 (Manual Floor distribution)
- `CabTempRequest` == 22.0 (Manual Temperature setting)
- `HVACBlowerRequest` == 30.0 (Manual Blower setting)
- `AC_ButtonStatus` == 1 (AC On, manual setting)

**Trigger:** `VehicleMode` changes from 3 (Running) to 0 (Ignition Off).

**Steps:**
1. Set `AirRecirculationRequest` to 0 (Fresh Air).
2. Set `ClimateAirDistRequest_Defrost` to 0.
3. Set `ClimateAirDistRequest_Floor` to 1.
4. Set `ClimateAirDistRequest_Vent` to 0.
5. Set `CabTempRequest` to 22.0.
6. Set `HVACBlowerRequest` to 30.0.
7. Set `AC_ButtonStatus` to 1.
8. Set `VehicleMode` to 3 (Running).
9. Set `MaxDefrostRequest` to 1 (On).
10. Wait for 5 seconds to allow Max Defrost to activate and override settings.
11. Set `VehicleMode` to 0 (Ignition Off).
12. Wait for 5 seconds to allow deactivation and restoration.

**Expected Outcome:**
- `MaxDefrostStatus` == 0 (Off)
- `AirRecirculationRequest` == 0 (Fresh Air, restored to pre-Max Defrost value)
- `ClimateAirDistRequest_Defrost` == 0 (Restored to pre-Max Defrost value)
- `ClimateAirDistRequest_Floor` == 1 (Restored to pre-Max Defrost value)
- `ClimateAirDistRequest_Vent` == 0 (Restored to pre-Max Defrost value)
- `CabTempRequest` == 22.0 (Restored to pre-Max Defrost value)
- `HVACBlowerRequest` == 30.0 (Restored to pre-Max Defrost value)
- `AC_ButtonStatus` == 1 (Restored to pre-Max Defrost value)