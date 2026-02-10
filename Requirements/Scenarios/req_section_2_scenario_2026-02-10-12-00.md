# Test Type: AUTOMATED
(Reason: All specified signals (HVACAct1Stat_CurrentPos, HVACAct2Stat_CurrentPos, HVACAct3Stat_CurrentPos) were found in the database with the prefix 'LIN_'. This indicates that the required feedback signals are available for automated testing.)

# Scenario: HVAC Actuator Final Position Status Feedback
**Description:** Verify that the Thermal System correctly receives the final position status of HVAC actuators (Recirculation, Vent/Defrost/Floor, Heat Blend) by sending feedback internally from HVAC to CCM.
**Pre-conditions:**
*   HVAC system is powered on and initialized.
*   CCM (Climate Control Module) is operational.
*   The vehicle is in a state where HVAC actuator movement is permitted (e.g., Running mode).
**Trigger:** A command is issued to change the position of the HVAC Recirculation, Vent/Defrost/Floor, or Heat Blend actuators.
**Steps:**
1.  Command the HVAC Recirculation actuator to move to a new position.
2.  Command the HVAC Vent/Defrost/Floor actuator to move to a new position.
3.  Command the HVAC Heat Blend actuator to move to a new position.
**Expected Outcome:**
- LIN_HVACAct1Stat_CurrentPos == 100
- LIN_HVACAct2Stat_CurrentPos == 150
- LIN_HVACAct3Stat_CurrentPos == 200