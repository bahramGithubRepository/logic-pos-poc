# Test Type: AUTOMATED
*(Reason: Core trigger signal `MaxDefrostRequest` and all relevant control signals (`ACRequest`, `CabTempRequest`, `AirRecirculationRequest`, `ClimateAirDistRequest_Defrost`, `HVACBlowerRequest`) are present in the database. Output status `MaxDefrostStatus` is also available for verification.)*

# Scenario: Max Defrost Activation via Driver Experience System Request
**Description:** Verify that the Thermal System correctly activates Max Defrost mode when requested by the Driver Experience System, leading to appropriate settings for air distribution, AC, heating, recirculation, and blower speed to achieve maximum defrosting performance.
**Pre-conditions:**
- The vehicle is in a mode that allows Max Defrost activation (e.g., 'Running').
**Trigger:** The Driver Experience System requests Max Defrost activation.
**Steps:**
1. Set `VehicleMode` to 'Running'.
2. Set `MaxDefrostRequest` to 1 (On).
**Expected Outcome:**
- `MaxDefrostStatus` == 1 (On)
- `ACRequest` == 1 (On)
- `CabTempRequest` == Max (Maximum temperature setting)
- `AirRecirculationRequest` == 0 (Off/Fresh Air)
- `ClimateAirDistRequest_Defrost` == 1 (On)
- `ClimateAirDistRequest_Floor` == 0 (Off)
- `ClimateAirDistRequest_Vent` == 0 (Off)
- `HVACBlowerRequest` == Max (Highest blower speed setting)
- `Flap_Defrost` == 100% (Open) (Note: Signal missing from DB; manual verification required)
- `Flap_Foot` == 0% (Closed) (Note: Signal missing from DB; manual verification required)
- `Flap_Center_Vent` == 0% (Closed) (Note: Signal missing from DB; manual verification required)