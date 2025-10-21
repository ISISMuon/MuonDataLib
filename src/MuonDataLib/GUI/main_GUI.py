from MuonDataLib.GUI.main_app import MainApp
from MuonDataLib.GUI.launch import launch_dash


def launch_GUI():
    """
    A simple method to launch the filtering GUI.
    """
    launch_dash(MainApp())
