# Test Type: AUTOMATED
(Reason: The signals `VehicleMode`, `MaxDefrostRequest`, and `MaxDefrostStatus` were found in the database. These signals are sufficient to test the availability of the Max Defrost function in the specified vehicle modes. It is assumed that `MaxDefrostRequest` can be set to `1` to request activation and `MaxDefrostStatus` will transition to `1` when active, indicating availability for activation.)

# Scenario: Max Defrost Function Availability in Valid Vehicle Modes
**Description:** Verify that the Max Defrost function is made available for activation when the vehicle is in `PreRunning`, `Cranking`, or `Running` modes.
**Pre-conditions:**
-   `MaxDefrostRequest` == `0` (Max Defrost is not requested)
-   `MaxDefrostStatus` == `0` (Max Defrost is not active)
**Trigger:** Set the `VehicleMode` to each of the specified valid states.
**Steps:**
1.  Set `VehicleMode` to `PreRunning`.
2.  Set `MaxDefrostRequest` to `1`.
3.  Observe system response for `MaxDefrostStatus`.
4.  Set `MaxDefrostRequest` to `0`.
5.  Set `VehicleMode` to `Cranking`.
6.  Set `MaxDefrostRequest` to `1`.
7.  Observe system response for `MaxDefrostStatus`.
8.  Set `MaxDefrostRequest` to `0`.
9.  Set `VehicleMode` to `Running`.
10. Set `MaxDefrostRequest` to `1`.
11. Observe system response for `MaxDefrostStatus`.

**Expected Outcome:**
-   When `VehicleMode` == `PreRunning` and `MaxDefrostRequest` is set to `1`: `MaxDefrostStatus` == `1`
-   When `VehicleMode` == `Cranking` and `MaxDefrostRequest` is set to `1`: `MaxDefrostStatus` == `1`
-   When `VehicleMode` == `Running` and `MaxDefrostRequest` is set to `1`: `MaxDefrostStatus` == `1`