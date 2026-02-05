import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import logging
import sys
import asyncio
import time
from niveristand.legacy import NIVeriStand
import json
from niveristand.library import wait
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand import nivs_rt_sequence, NivsParam, realtimesequencetools


def read_project_config(project_config_path='projectConfig.json'):
    logging.debug("Reading project config")
    """Read project configuration from a JSON file."""
    try:
        with open(project_config_path, 'r') as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading configuration file: {e}")
        return None, None, None, None

    project_path = config.get('projectpath', '')
    calibration_file = config.get('calibrationfile', '')
    system_address = config.get('Systemadress', '')
    variables = config.get('variables', {})
    if not project_path:
        print("Project path is not specified in the configuration.")
        return None, None, None, None
    if not system_address:
        print("No Systemadress found in the configuration.")
        return None, None, None, None
    logging.debug("Project config imported")
    return project_path, calibration_file, system_address, variables


def connect_to_veristand(project_path: str, calibration_file: str, system_address: str) -> None:
    """Connect to VeriStand Workspace and deploy the project."""
    logging.debug("Launching VeriStand Worksapce")
    NIVeriStand.LaunchNIVeriStand()
    logging.debug("Waiting for Verstand to be ready")
    NIVeriStand.WaitForNIVeriStandReady()
    ws = NIVeriStand.Workspace2(system_address)
    filtered_targets = None
    ws.ConnectToSystem(project_path, True, 120000,calibration_file, filtered_targets)
    logging.debug("Connected to VeriStand and deployed the project.")
    
    return ws


def run_demo(iterations=10):
    """Blink light on cRIO module."""
    with open ("projectConfig.json") as f:
        data = json.load(f)
    # do_channels = data["variables"]["do_channels"]
    # ai_channels = data["variables"]["ai_channels"]
    DO_channels = [ChannelReference(ch) for ch in data["variables"]["DO_channels"]]
    for _ in range(iterations):
        for i in range(len(DO_channels)):
            DO_channels[i].value = True
        wait(0.5)
        for i in range(len(DO_channels)):
            DO_channels[i].value = False
        wait(0.5)


def init_hil(configfile='projectConfig.json'):
    """Run project with the specified configuration file."""
    project_path, calibration_file, Systemadress, variables = read_project_config(configfile)
    if not project_path or not Systemadress:
        return
    ws = connect_to_veristand(project_path, calibration_file, Systemadress)
    logging.debug("3 second delay...")
    asyncio.run(asyncio.sleep(3))
    logging.debug("Delay done.")
    return ws, Systemadress

def disconnect_hil(ws, Systemadress):
    run_demo(iterations=100)
    print("Disconnecting from VeriStand system...")
    ws = NIVeriStand.Workspace2(Systemadress)
    ws.DisconnectFromSystem("", True)


def config_logs(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,   # <-- overrides any previous logging config
    )


if __name__ == "__main__":
    config_logs()
    # config_logs(debug=True)
    logging.debug("Starting main")
    configfile = sys.argv[1] if len(sys.argv) > 1 else 'projectConfig.json'
    ws, Systemaddress = init_hil(configfile)
    disconnect_hil(ws, Systemaddress)

