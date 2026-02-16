# Test Type: AUTOMATED
(Reason: All specified signals (LIN_HVACAct1Stat_CurrentPos, LIN_HVACAct2Stat_CurrentPos, LIN_HVACAct3Stat_CurrentPos) were found in the database.)

# Scenario: Verify HVAC Actuator Final Position Status Feedback to CCM
**Description:** This test verifies that the Thermal System correctly receives the final position status of the HVAC actuators from the HVAC module to the CCM using the specified LIN signals.
**Pre-conditions:**
- The vehicle system is powered on.
- The HVAC and CCM modules are operational and communicating via the LIN bus.
- HVAC actuators are capable of moving to commanded positions and providing feedback.
**Trigger:** The HVAC system commands its actuators to specific final positions, and these actuators report their current position status.
**Steps:**
1. Simulate HVAC Actuator 1 (Recirculation) reaching a final position value of 100.
2. Simulate HVAC Actuator 2 (Vent/Defrost/Floor) reaching a final position value of 150.
3. Simulate HVAC Actuator 3 (Heat Blend) reaching a final position value of 200.
4. Monitor the LIN bus for the feedback signals from the HVAC to the CCM.
**Expected Outcome:**
- LIN_HVACAct1Stat_CurrentPos == 100
- LIN_HVACAct2Stat_CurrentPos == 150
- LIN_HVACAct3Stat_CurrentPos == 200