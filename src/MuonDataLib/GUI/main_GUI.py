from MuonDataLib.GUI.main_app import main_app
from MuonDataLib.GUI.launch import launch_dash


def launch_GUI():
    """
    A simple method to launch the filtering GUI.
    """
    launch_dash(main_app())
