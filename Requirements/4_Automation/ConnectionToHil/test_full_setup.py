"""Test with full CCM prerequisites"""
import asyncio
from hil_modules import read_project_config
from niveristand.clientapi import ChannelReference

hil_var = read_project_config()[3]

print("Setting up CCM prerequisites...")

# Set all the signals from the working CAN test
can_out = hil_var["CAN"]["OUT"]
ChannelReference(can_out["VehicleMode"]).value = 6  # Try 6 instead of 4
ChannelReference(can_out["ClimatePowerRequest"]).value = 1
ChannelReference(can_out["MaxDefrostRequest"]).value = 0
ChannelReference(can_out["ClimateAirDistRequest_Defrost"]).value = 0
ChannelReference(can_out["ClimateAirDistRequest_Floor"]).value = 1
ChannelReference(can_out["ClimateAirDistRequest_Vent"]).value = 1
ChannelReference(can_out["AirRecirculationRequest"]).value = 1
ChannelReference(can_out["HVACBlowerRequest"]).value = 1

print("Waiting 2 seconds for CCM to initialize...")
asyncio.run(asyncio.sleep(2))

print("Setting LIN28 EAC_InvrtTemp to 81...")
ChannelReference(hil_var["LIN28"]["OUT"]["EAC_InvrtTemp"]).value = 81

print("\nMonitoring for 10 seconds:")
for i in range(20):
    valve = ChannelReference(hil_var["CAN"]["IN"]["ChlrVlvPsnRqst"]).value
    fan = ChannelReference(hil_var["CAN"]["IN"]["ACCoolingFanSpeedRequest_CCM_UB"]).value
    lin = ChannelReference(hil_var["LIN28"]["OUT"]["EAC_InvrtTemp"]).value
    print(f"  {i*0.5:.1f}s - LIN: {lin:6.2f} | Valve: {valve:6.2f} | Fan: {fan:6.2f}")
    asyncio.run(asyncio.sleep(0.5))