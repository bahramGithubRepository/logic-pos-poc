# Test Type: AUTOMATED
(Reason: All specified signals (HVACAct1Stat_CurrentPos, HVACAct2Stat_CurrentPos, HVACAct3Stat_CurrentPos) were found in the database as LIN_HVACAct1Stat_CurrentPos, LIN_HVACAct2Stat_CurrentPos, and LIN_HVACAct3Stat_CurrentPos, indicating their presence and feasibility for automation.)

# Scenario: Verification of HVAC Actuator Position Feedback
**Description:** This scenario verifies that the Thermal System correctly receives the final position status of HVAC actuators (Recirculation, Vent/Defrost/Floor, Heat Blend) by sending feedback internally from the HVAC to the CCM.
**Pre-conditions:**
- Vehicle in an operational mode (e.g., Running).
- HVAC system initialized and functional.
- CCM module is active and receiving data.
**Trigger:** HVAC actuator positions are commanded to change.
**Steps:**
1. Command the HVAC system to set the Recirculation flap to an intermediate position.
2. Command the HVAC system to set the Vent/Defrost/Floor flap to a position favoring defrost.
3. Command the HVAC system to set the Heat Blend flap to a maximum heat position.
4. Monitor the feedback signals from HVAC to CCM.
**Expected Outcome:**
- LIN_HVACAct1Stat_CurrentPos == 127
- LIN_HVACAct2Stat_CurrentPos == 191
- LIN_HVACAct3Stat_CurrentPos == 255