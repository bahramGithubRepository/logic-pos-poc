# Scenario: Max Defrost Activation and System State Verification
**Description:** This test verifies that when Max Defrost is activated, the Thermal System correctly commands maximum heating, maximum blower speed, fresh air intake, A/C activation, and sets the air distribution mode to full defrost by commanding the actuator to the correct position.
**Pre-conditions:**
*   `VehicleMode = Running`
*   `AmbientTemp = 15 degC` (To ensure A/C can be activated)
*   `ClimateCtrlOn = 1` (On)
*   `MaxDefrostStatus = 0` (Off)
**Trigger:** The driver activates the Max Defrost function via the HMI.
*   `HMI_MaxDefrostRequest = 1` (Pressed)
**Steps:**
1.  Establish the state defined in Pre-conditions.
2.  Apply the Trigger by setting `HMI_MaxDefrostRequest = 1`.
3.  Wait 500ms for the Thermal System to process the request.
4.  Verify that all related Thermal System outputs match the Expected Outcome.
**Expected Outcome:**
*   `MaxDefrostStatus = 1` (On)
*   `CabHeatManStatus = Max`
*   `BlowerSpeedRequest = 100%`
*   `AC_Request = 1` (On)
*   `RecirculationRequest = 0` (Fresh Air)
*   `AirDistActuatorCmd = 0%` (Command to Defrost position)
*   `Flap_Defrost = 100%` (Open)
*   `Flap_Foot = 0%` (Closed)
*   `Flap_Center_Vent = 0%` (Closed)