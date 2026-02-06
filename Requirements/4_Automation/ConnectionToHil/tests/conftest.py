# import pytest
# from Hil_lab_project import read_project_config
# from niveristand.legacy import NIVeriStand


# def pytest_addoption(parser):
#     parser.addoption(
#         "--configfile",                      # command-line option name
#         action="store",
#         default="projectConfig.json",      # default if not provided
#         help="Path to config JSON config file"
#     )

# @pytest.fixture(scope="session")
# def configfile(request):
#     return request.config.getoption("--configfile")

# @pytest.fixture(scope="session", autouse=True) # Automatically run this fixture for the entire session 
# def connect_to_veristand(configfile):

#     project_path, calibration_file, Systemadress, variables = read_project_config(configfile)
#     """Connect to VeriStand Workspace and deploy the project."""
#     NIVeriStand.LaunchNIVeriStand()
#     NIVeriStand.WaitForNIVeriStandReady()
#     ws = NIVeriStand.Workspace2(Systemadress)
#     filtered_targets = None
#     ws.ConnectToSystem(project_path, True, 120000, calibration_file, filtered_targets)
#     print("Connected to VeriStand and deployed the project.")

#     yield variables    # This allows the test to run after the connection is established


#     ws = NIVeriStand.Workspace2(Systemadress)
#     ws.DisconnectFromSystem("", True)

