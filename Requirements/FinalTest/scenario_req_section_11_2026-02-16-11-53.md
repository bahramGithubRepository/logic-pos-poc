# Test Type: AUTOMATED
(Reason: All required signals including `MaxDefrostStatus`, `AirRecirculationStatus`, `WindscreenDefrost_ButtonStatus` (as the activation trigger), and functional equivalents for flap positions (`ClimateAirDistStatus_Defrost`, `ClimateAirDistStatus_Floor`, `ClimateAirDistStatus_Vent`) were found in the database.)

# Scenario: Max Defrost Activates with Outside Air and Correct Air Distribution
**Description:** Verify that when Max Defrost is activated, the Thermal System uses only outside air (0% recirculation) and correctly sets the air distribution to direct airflow solely to the defrost vents.
**Pre-conditions:** The vehicle is in a valid operating mode for Max Defrost activation (e.g., Running).
**Trigger:** Driver requests activation of Max Defrost.
**Steps:**
1. Set `WindscreenDefrost_ButtonStatus` to `1` (ON).
2. Wait for the system to stabilize.
**Expected Outcome:**
- `MaxDefrostStatus` == `1` (On)
- `AirRecirculationStatus` == `0` (Off - indicating 0% recirculation, outside air only)
- `ClimateAirDistStatus_Defrost` == `15` (Fully open towards defrost, assuming 15 is max value)
- `ClimateAirDistStatus_Floor` == `0` (Fully closed for floor distribution, assuming 0 is min value)
- `ClimateAirDistStatus_Vent` == `0` (Fully closed for vent distribution, assuming 0 is min value)