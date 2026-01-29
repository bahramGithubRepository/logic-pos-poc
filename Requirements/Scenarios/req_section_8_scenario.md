# Scenario: Max Defrost Activation Commands Full Defrost Air Distribution and Associated Thermal Settings
**Description:** This test verifies that upon activating Max Defrost, the Thermal System correctly commands all relevant actuators to their target states for maximum defrost performance. This includes setting air distribution to 100% defrost, maximizing blower speed and heat, enabling the AC compressor, and ensuring fresh air intake. The test also verifies that the low-level actuator commands are sent immediately to achieve the state as fast as possible.
**Pre-conditions:**
*   `Vehicle_Mode` = Running
*   `Ambient_Temperature` > 5°C (to allow AC activation)
*   `ClimateCtrlStatus` = On
*   `MaxDefrostStatus` = 0 (Off)
*   `ClimateAirDistStatus` = 3 (Foot)
*   `BlowerSpeedCmd` = 50%
*   `RecirculationCmd` = 1 (Recirculation On)
*   `AC_CompressorCmd` = 0 (Off)
*   `TemperatureCmd_DriverSide` = 22°C
**Trigger:**
The user activates Max Defrost via the HMI.
*   `DriverExperience_HMI_MaxDefrost_Request` = 1 (Pressed)
**Steps:**
1.  Establish all pre-conditions.
2.  Send the trigger signal `DriverExperience_HMI_MaxDefrost_Request` = 1.
3.  Monitor the system's output signals for the expected state changes.
**Expected Outcome:**
The system shall immediately issue commands to all relevant actuators and update its state. The following signals must be verified:
*   `MaxDefrostStatus` = 1 (On)
*   `ClimateAirDistStatus` = 1 (Defrost)
*   `HVACAct1Cmd_ConfigMode` = 2 (MoveToTarget)
*   `HVACAct1Cmd_InitPOS` = 0x00 (Position for 100% Defrost)
*   `HVACAct2Cmd_ConfigMode` = 2 (MoveToTarget)
*   `HVACAct2Cmd_InitPOS` = 0x00 (Position for 100% Fresh Air)
*   `HVACAct3Cmd_ConfigMode` = 2 (MoveToTarget)
*   `HVACAct3Cmd_InitPOS` = 0xFF (Position for 100% Heat)
*   `BlowerSpeedCmd` = 100%
*   `RecirculationCmd` = 0 (Fresh Air)
*   `AC_CompressorCmd` = 1 (On)
*   `TemperatureCmd_DriverSide` = 32°C (Max Heat)
*   `TemperatureCmd_PassengerSide` = 32°C (Max Heat)
*   `Flap_Defrost_Position` = 100%
*   `Flap_Foot_Position` = 0%
*   `Flap_Center_Vent_Position` = 0%