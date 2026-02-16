# Test Type: AUTOMATED
(Reason: All critical signals for requesting, controlling, and monitoring Max Defrost and its associated functions (air distribution, blower, heating, AC, recirculation) have been found in the database or strong functional equivalents have been identified. Specifically, `MaxDefrostRequest` is available to trigger the activation, `LIN_WindscreenDefrostInd_cmd`, `MaxDefrostStatus`, and `WindscreenDefrost_ButtonStatus` (as an equivalent to `LIN_WindscreenDefrost_ButtonSt`) are available for verification. Control signals for air distribution (`ClimateAirDistRequest_Defrost`, `ClimateAirDistRequest_Floor`, `ClimateAirDistRequest_Vent`), blower (`HVACBlowerRequest`), and cabin temperature (`CabTempRequest`) are also present. The expected states of AC and Recirculation can be verified via `AC_ButtonStatus` and `Recirc_ButtonStatus` status signals, assuming the Thermal System internally manages these based on the `MaxDefrostRequest`.)

# Scenario: Max Defrost Activation by Thermal System Request
**Description:** Verify that the Thermal System correctly activates Max Defrost when requested, setting the appropriate indicator signals and internal climate control parameters (AC, recirculation, air distribution, blower speed, heating).
**Pre-conditions:**
-   `MaxDefrostStatus` == 0 (Max Defrost is inactive)
-   `VehicleMode` == 3 (Running, for ICE/BEV)
-   `LIN_WindscreenDefrostInd_cmd` == 0 (Max Defrost LED off)
-   `WindscreenDefrost_ButtonStatus` == 0 (Max Defrost button not pushed)
-   `AC_ButtonStatus` == 0 (AC off)
-   `Recirc_ButtonStatus` == 0 (Recirculation off)
-   `ClimateAirDistRequest_Defrost` == 0 (Air distribution not in defrost mode)
**Trigger:**
-   Set `MaxDefrostRequest` to 1 (Thermal System requests Max Defrost activation).
**Steps:**
1.  Set `VehicleMode` to 3 (Running).
2.  Ensure `MaxDefrostStatus` is 0.
3.  Set `MaxDefrostRequest` to 1.
4.  Wait for system to process the request (e.g., 500 ms).
**Expected Outcome:**
-   `LIN_WindscreenDefrostInd_cmd` == 1 (ON (LED activated))
-   `MaxDefrostStatus` == 1 (Enabled)
-   `WindscreenDefrost_ButtonStatus` == 1 (Pushed)
-   `ClimateAirDistRequest_Defrost` == 100 (Air distribution fully to defrost)
-   `ClimateAirDistRequest_Floor` == 0 (Floor distribution off)
-   `ClimateAirDistRequest_Vent` == 0 (Vent distribution off)
-   `AC_ButtonStatus` == 1 (AC enabled by system)
-   `Recirc_ButtonStatus` == 0 (Recirculation off / Fresh air intake enabled by system)
-   `HVACBlowerRequest` == [Max_Blower_Speed_Value] (Blower speed set to highest possible)
-   `CabTempRequest` == [Max_Heating_Temperature_Value] (Heating set to highest possible)