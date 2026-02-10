# Test Type: AUTOMATED
(Reason: All specified signals (`HVACAct1Stat_CurrentPos`, `HVACAct2Stat_CurrentPos`, `HVACAct3Stat_CurrentPos`) were found in the database as `LIN_HVACAct1Stat_CurrentPos`, `LIN_HVACAct2Stat_CurrentPos`, and `LIN_HVACAct3Stat_CurrentPos` respectively.)

# Scenario: Verify HVAC Actuator Position Feedback to CCM
**Description:** This test scenario verifies that the Thermal System correctly receives and processes the final position status of HVAC actuators, which are fed back internally from the HVAC module to the CCM via dedicated status signals.
**Pre-conditions:**
- The HVAC system is powered on and operational.
- The Communication Controller Module (CCM) is active and monitoring LIN bus traffic.
**Trigger:** An HVAC actuator changes its physical position.
**Steps:**
1. Command the HVAC Recirculation Actuator (corresponding to HVACAct1) to its fully closed position.
2. Allow sufficient time for the actuator to reach its commanded position and for the status signal to be updated.
3. Command the HVAC Vent/Defrost/Floor Actuator (corresponding to HVACAct2) to its fully open (defrost) position.
4. Allow sufficient time for the actuator to reach its commanded position and for the status signal to be updated.
5. Command the HVAC Heat Blend Actuator (corresponding to HVACAct3) to a specific intermediate position, e.g., 50% open.
6. Allow sufficient time for the actuator to reach its commanded position and for the status signal to be updated.
**Expected Outcome:**
- LIN_HVACAct1Stat_CurrentPos == 0 (fully closed for Recirculation)
- LIN_HVACAct2Stat_CurrentPos == 255 (fully open/defrost for Vent/Defrost/Floor)
- LIN_HVACAct3Stat_CurrentPos == 128 (approx. 50% open for Heat Blend)