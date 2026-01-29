# Scenario: Max Defrost Activation and Initial System State
**Description:** This test verifies that when Max Defrost is activated, the Thermal System correctly commands all related components to their initial default states for maximum defrost performance. This includes setting air recirculation to OFF (fresh air), commanding the blower and temperature to their maximum settings, enabling the A/C compressor for dehumidification, and directing all airflow to the defrost vents by commanding the appropriate actuator positions. This test validates the initial commanded state; subsequent user adjustments to blower speed, temperature, or A/C status are permitted during Max Defrost operation as per system design, but are not covered in this specific test case.
**Pre-conditions:**
1.  Vehicle power mode is **Running**.
2.  The Climate Control system is **ON**.
3.  Ambient temperature is **10°C** (to allow for A/C compressor activation).
4.  Initial climate settings are:
    *   `MaxDefrostStatus` = 0 (Off)
    *   `AirRecirculationStatus` = 1 (On)
    *   `BlowerSpeedSetting` = 50 (%)
    *   `TemperatureSetting` = 22 (°C)
    *   `AC_RequestStatus` = 0 (Off)
    *   `AirDist_Actuator_Rotation_Cmd` = 60 (%) (Vent Mode)

**Trigger:**
The system receives a request to activate Max Defrost.
`HMI_MaxDefrost_Request` = 1 (Pressed)

**Steps:**
1.  Verify the system is in the state defined by the Pre-conditions.
2.  Send the Trigger command to activate Max Defrost.
3.  Monitor the system's output signals for 5 seconds.

**Expected Outcome:**
The system shall immediately command the following states upon Max Defrost activation:
*   `MaxDefrostStatus` = 1 (On)
*   `AirRecirculationStatus` = 0 (Off)
*   `BlowerSpeedSetting` = 100 (%)
*   `TemperatureSetting` = 32 (°C)
*   `AC_RequestStatus` = 1 (Enabled)
*   `AirDist_Actuator_Rotation_Cmd` = 0 (%)
*   `Flap_Defrost_Position` = 100 (%)
*   `Flap_Foot_Position` = 0 (%)
*   `Flap_Center_Vent_Position` = 0 (%)