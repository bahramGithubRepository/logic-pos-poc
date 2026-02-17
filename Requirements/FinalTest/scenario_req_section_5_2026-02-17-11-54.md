# Test Type: AUTOMATED
*(Reason: All core trigger and primary verification signals, `MaxDefrostRequest` and `MaxDefrostStatus`, are present in the database. Relevant secondary output signals for air distribution, blower level, AC status, and front temperature status are also found.)*

# Scenario: Max Defrost Activation Request
**Description:** Verify that when the Driver Experience System requests the activation of Max Defrost, the Thermal System correctly activates Max Defrost mode and configures related climate control settings (air distribution, blower speed, AC, heating, and recirculation) as specified.
**Pre-conditions:**
- Vehicle Mode is "Running".
- Ambient air temperature is above the threshold for AC enablement (e.g., 10°C).
- Climate Control System is initially in a normal operating state (e.g., Auto mode, no Max Defrost active).
**Trigger:** The Driver Experience System sends a request to activate Max Defrost.
**Steps:**
1. Set `MaxDefrostRequest` to 1 (On).
2. Set `VehicleMode` to "Running".
3. Set `PV_AmbientAirTemp` to 15.0°C (e.g., for AC enablement).
4. Monitor the relevant status signals.
**Expected Outcome:**
- `MaxDefrostStatus` == 1 (On)
- `ClimateAirDistStatus_Defrost` == 100% (Open)
- `ClimateAirDistStatus_Floor` == 0% (Closed)
- `ClimateAirDistStatus_Vent` == 0% (Closed)
- `HVACBlowerLevelStat_BlowerLevel` == Maximum Value (As high as possible)
- `PS_FrontACStatus` == On (Enabled)
- `PV_FrontTemperatureStatus` == Maximum Value (Highest possible heating)
- Recirculation is off (fresh air) (Note: Signal missing from DB; manual verification required)