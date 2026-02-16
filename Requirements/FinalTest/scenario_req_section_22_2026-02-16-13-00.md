# Test Type: AUTOMATED
(Reason: All critical signals for the Max Defrost activation, climate power control, blower, temperature, AC, and air distribution requests, as well as their corresponding status signals, were found in the database. This allows for full automation of the test scenario.)

# Scenario: Verify Max Defrost Activation and Parameter Restoration after Climate System Power Cycle in Running Mode
**Description:** This test verifies that when the Climate System is powered ON, and the vehicle is in running mode, if Max Defrost was active when the Climate System was turned OFF during the same uninterrupted session, the Thermal System activates Max Defrost and restores the AC setting, Temperature setting, and Blower setting to their previously stored values.
**Pre-conditions:**
- `VehicleMode` == 3 (Running)
- `ClimatePowerRequest` == 2 (Enable)
- `ClimatePowerStatus` == 1 (Enabled)
- `MaxDefrostRequest` == 0 (Off)
- `MaxDefrostStatus` == 0 (Off)
- `ACRequest` == 0 (Off)
- `CabTempRequest` == 20.0 (initial temperature)
- `HVACBlowerRequest` == 0 (initial blower level)
**Trigger:** `ClimatePowerRequest` changes from 0 (Disable) to 2 (Enable) after a previous power cycle with Max Defrost active.
**Steps:**
1. Set `VehicleMode` to 3 (Running).
2. Set `ClimatePowerRequest` to 2 (Enable).
3. Wait until `ClimatePowerStatus` == 1 (Enabled).
4. Set `ACRequest` to 1 (On).
5. Set `CabTempRequest` to 22.0 (degrees Celsius).
6. Set `HVACBlowerRequest` to 5 (specific blower level).
7. Set `MaxDefrostRequest` to 1 (On).
8. Wait until `MaxDefrostStatus` == 1 (On).
9. Set `ClimatePowerRequest` to 0 (Disable).
10. Wait until `ClimatePowerStatus` == 0 (Disabled).
11. Set `ClimatePowerRequest` to 2 (Enable).
12. Wait until `ClimatePowerStatus` == 1 (Enabled).
**Expected Outcome:**
- `MaxDefrostStatus` == 1 (On)
- `ACRequest` == 1 (On)
- `CabTempRequest` == 22.0 (degrees Celsius)
- `HVACBlowerRequest` == 5
- `ClimateAirDistRequest_Defrost` == 1 (On)
- `ClimateAirDistRequest_Floor` == 0 (Off)
- `ClimateAirDistRequest_Vent` == 0 (Off)