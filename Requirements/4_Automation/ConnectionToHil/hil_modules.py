import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import asyncio, json, sys, logging, os, pathlib
from niveristand.legacy import NIVeriStand
from niveristand.library import wait
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand import nivs_rt_sequence, NivsParam, realtimesequencetools

from typing import Tuple


def read_project_config(project_config_path='projectConfig.json'):
    logging.debug("Reading project config")
    """Read project configuration from a JSON file."""
    try:
        with open(project_config_path, 'r') as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading configuration file: {e}")
        return None, None, None, None

    root_dir = os.environ.get("CI_PROJECT_DIR", os.getcwd())
    project_path = str(pathlib.Path(root_dir, config.get('projectpath', '')).resolve())
    calibration_file = str(pathlib.Path(root_dir, config.get('calibrationfile', '')).resolve())
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

def connect_to_veristand(project_path: str, calibration_file: str, system_address: str):
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

def connect_hil(configfile='projectConfig.json') -> Tuple[object, str]:
    """Run project with the specified configuration file."""
    check_if_already_connected(disconnect_if_connected = True)
    logging.debug("Initializing HIL")
    project_path, calibration_file, Systemadress, variables = read_project_config(configfile)
    if not project_path or not Systemadress:
        return
    ws = connect_to_veristand(project_path, calibration_file, Systemadress)
    logging.debug("3 second delay...")
    asyncio.run(asyncio.sleep(3))
    logging.debug("Delay done.")

    return ws, Systemadress

def disconnect_hil(ws, Systemadress):
    print("Disconnecting from VeriStand system...")
    ws = NIVeriStand.Workspace2(Systemadress)
    ws.DisconnectFromSystem("", True)
    if ws.GetSystemState()["state"] == 1:
        logging.debug("HIL disconnected successfully!")


def config_logs(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,   # <-- overrides any previous logging config
    )

def check_if_already_connected(disconnect_if_connected = False):
    sys_addr = read_project_config()[2]
    
    logging.debug("Checking if HIL is already conencted...")
    ws = NIVeriStand.Workspace2(sys_addr)
    
    hil_connected = ws.GetSystemState()["state"] == 1
    
    if disconnect_if_connected and hil_connected:
        logging.debug("Disconnecting already connected HIL triggered by flag...")
        disconnect_hil(ws, sys_addr)

    return ws.GetSystemState()["state"] == 1



if __name__ == "__main__":
    config_logs()
    # config_logs(debug=True)
    logging.debug("Starting main")
    configfile = sys.argv[1] if len(sys.argv) > 1 else 'projectConfig.json'
    root_dir = os.environ.get("CI_PROJECT_DIR", os.getcwd())
    project_config_path='projectConfig.json'

    try:
        with open(project_config_path, 'r') as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading configuration file: {e}")
    project_path = config.get('projectpath', '')
    project_path = str(pathlib.Path(root_dir, project_path).resolve())
    print(project_path)
