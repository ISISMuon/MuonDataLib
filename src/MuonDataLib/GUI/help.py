from MuonDataLib.GUI.launch import launch_dash
from MuonDataLib.help.help import help_app


def launch_help():
    """
    A simple method to launch the help pages.
    """
    launch_dash(help_app())
