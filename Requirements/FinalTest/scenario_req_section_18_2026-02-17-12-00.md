# Test Type: AUTOMATED
*(Reason: The core trigger signal `ACRequest` is available in the database. `MaxDefrostStatus` is also available for observation. Although `ACStatus` is not explicitly found, the test is still automated as per the "Partial Automation Logic" rule, with a note for manual verification for the missing signal.)*

# Scenario: AC Activation/Deactivation during Max Defrost
**Description:** Verify that the Thermal System correctly activates/deactivates AC and keeps Max Defrost active when requested by the Driver Experience system, and reports the correct status.
**Pre-conditions:**
- The vehicle is in an operating mode that allows AC activation and Max Defrost (e.g., Running).
- Max Defrost is currently active.
**Trigger:** The Driver Experience system requests activation or deactivation of the AC.
**Steps:**
1.  Verify that `MaxDefrostStatus` == 1 (On).
2.  Set `ACRequest` to 1 (On) to activate the AC.
3.  Wait for the Thermal System to process the AC activation request.
4.  Set `ACRequest` to 0 (Off) to deactivate the AC.
5.  Wait for the Thermal System to process the AC deactivation request.
**Expected Outcome:**
- After Step 2 (AC Activation Request):
    - `MaxDefrostStatus` == 1 (On)
    - `ACStatus` == 1 (On) (Note: Signal missing from DB; manual verification required)
- After Step 4 (AC Deactivation Request):
    - `MaxDefrostStatus` == 1 (On)
    - `ACStatus` == 0 (Off) (Note: Signal missing from DB; manual verification required)