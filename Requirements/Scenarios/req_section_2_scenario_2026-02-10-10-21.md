# Test Type: AUTOMATED
(Reason: All specified signals (HVACAct1Stat_CurrentPos, HVACAct2Stat_CurrentPos, HVACAct3Stat_CurrentPos) were found in the database with a 'LIN_' prefix (LIN_HVACAct1Stat_CurrentPos, LIN_HVACAct2Stat_CurrentPos, LIN_HVACAct3Stat_CurrentPos), confirming their existence.)

# Scenario: Verification of HVAC Actuator Position Status Feedback to CCM
**Description:** This scenario verifies that the Thermal System accurately receives the final position status of HVAC actuators (Recirculation, Vent/Defrost/Floor, Heat Blend) from the HVAC unit and sends this feedback internally to the CCM.
**Pre-conditions:** The vehicle's HVAC system and CCM are powered on and operational. The HVAC actuators are capable of receiving and executing position commands.
**Trigger:** The HVAC actuators complete a commanded movement to a specific position.
**Steps:**
1. Command LIN_HVACAct1Stat_CurrentPos (Recirculation actuator) to a specific position value, for example, 128.
2. Command LIN_HVACAct2Stat_CurrentPos (Vent/Defrost/Floor actuator) to a specific position value, for example, 64.
3. Command LIN_HVACAct3Stat_CurrentPos (Heat Blend actuator) to a specific position value, for example, 192.
4. Monitor the feedback signals from the HVAC to the CCM.
**Expected Outcome:**
- LIN_HVACAct1Stat_CurrentPos == 128
- LIN_HVACAct2Stat_CurrentPos == 64
- LIN_HVACAct3Stat_CurrentPos == 192