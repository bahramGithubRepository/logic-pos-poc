# Test Type: AUTOMATED
(Reason: All necessary signals, `VehicleMode`, `MaxDefrostRequest` (mapped to `WindscreenDefrost_ButtonStatus`), `MaxDefrostStatus`, `AC_Status` (mapped to `AC_ButtonStatus`), `HVACBlowerRequest`, `Recirculation_Status` (mapped to `Recirc_ButtonStatus`), `ClimateAirDistRequest_Defrost`, `ClimateAirDistRequest_Floor`, `ClimateAirDistRequest_Vent`, and `CabTempRequest` were found in the database. Functional equivalents exist for controlling Max Defrost and related thermal system parameters.)

# Scenario: Max Defrost Activation in Valid Vehicle Modes
**Description:** Verify that the Max Defrost function can be activated and remains active when the vehicle is in valid operational modes (Parked, Living, Accessory, PreRunning, Cranking, Running) and the driver requests activation.
**Pre-conditions:**
- The vehicle's ignition is on.
- Max Defrost function is currently inactive.
- Ambient temperature is above the threshold where AC operation is inhibited (e.g., 5°C).
- Climate system is powered on.
**Trigger:**
- Max Defrost button is pressed by the driver.
**Steps:**
1. Set `VehicleMode` to 'Parked'.
2. Set `WindscreenDefrost_ButtonStatus` to 'Pressed' (1) to request Max Defrost activation.
3. Verify that Max Defrost activates.
4. Cycle `VehicleMode` through 'Living', 'Accessory', 'PreRunning', 'Cranking', and 'Running' while `WindscreenDefrost_ButtonStatus` remains 'Pressed'.
5. Verify that Max Defrost remains active during these transitions.
6. Set `WindscreenDefrost_ButtonStatus` to 'Released' (0) to deactivate Max Defrost.
7. Set `VehicleMode` to 'Running'.
8. Set `WindscreenDefrost_ButtonStatus` to 'Pressed' (1) to request Max Defrost activation.
9. Change `Recirc_ButtonStatus` to 'Recirculation On' (1).
10. Change `ClimateAirDistRequest_Floor` to 'Active' (1).
11. Change `HVACBlowerRequest` to '50' (mid-range speed).
12. Change `AC_ButtonStatus` to 'Off' (0).
13. Change `CabTempRequest` to '22' (lower temperature).
14. Set `VehicleMode` to 'Ignition Off'.
**Expected Outcome:**
- When `VehicleMode` is 'Parked' AND `WindscreenDefrost_ButtonStatus` is 'Pressed' (1):
    - `MaxDefrostStatus` == 'Active' (1)
    - `AC_ButtonStatus` == 'On' (1)
    - `HVACBlowerRequest` == '100' (Maximum speed)
    - `Recirc_ButtonStatus` == 'Off' (0)
    - `ClimateAirDistRequest_Defrost` == 'Active' (1)
    - `ClimateAirDistRequest_Floor` == 'Inactive' (0)
    - `ClimateAirDistRequest_Vent` == 'Inactive' (0)
    - `CabTempRequest` == '30' (Maximum heat)
- When `VehicleMode` transitions from 'Parked' to 'Living', 'Accessory', 'PreRunning', 'Cranking', and 'Running' AND `WindscreenDefrost_ButtonStatus` is 'Pressed' (1):
    - `MaxDefrostStatus` == 'Active' (1)
    - `AC_ButtonStatus` == 'On' (1)
    - `HVACBlowerRequest` == '100' (Maximum speed)
    - `Recirc_ButtonStatus` == 'Off' (0)
    - `ClimateAirDistRequest_Defrost` == 'Active' (1)
    - `ClimateAirDistRequest_Floor` == 'Inactive' (0)
    - `ClimateAirDistRequest_Vent` == 'Inactive' (0)
    - `CabTempRequest` == '30' (Maximum heat)
- When `WindscreenDefrost_ButtonStatus` is 'Released' (0):
    - `MaxDefrostStatus` == 'Inactive' (0)
- When `Recirc_ButtonStatus` is 'Recirculation On' (1) AND `MaxDefrostStatus` is 'Active':
    - `MaxDefrostStatus` == 'Inactive' (0)
- When `ClimateAirDistRequest_Floor` is 'Active' (1) AND `MaxDefrostStatus` is 'Active':
    - `MaxDefrostStatus` == 'Inactive' (0)
- When `HVACBlowerRequest` is '50' AND `MaxDefrostStatus` is 'Active' (this change is allowed but affects performance, so Max Defrost should remain active but with reduced performance as per requirement):
    - `MaxDefrostStatus` == 'Active' (1)
- When `AC_ButtonStatus` is 'Off' (0) AND `MaxDefrostStatus` is 'Active' (this change is allowed but affects performance):
    - `MaxDefrostStatus` == 'Active' (1)
- When `CabTempRequest` is '22' AND `MaxDefrostStatus` is 'Active' (this change is allowed but affects performance):
    - `MaxDefrostStatus` == 'Active' (1)
- When `VehicleMode` leaves 'Running' (e.g., to 'Ignition Off') AND `MaxDefrostStatus` is 'Active':
    - `MaxDefrostStatus` == 'Inactive' (0)