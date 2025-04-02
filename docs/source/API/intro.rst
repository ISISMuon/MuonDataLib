Introduction
============

At present MuonDataLib has interactive built-in help GUI and static API documentation.
The API documentation only covers the code that a user is likely to need.
Therefore, it is not a complete record of the whole code base.
This was done to prevent the API documentation from becoming overwhelming.

To use the built-in help GUI you will need to run the following code

.. code:: python

    from MuonDataLib.GUI.help import launch_help
    launch_help()

This will create a pop-up window to appear containing the interactive API documentation.
Running this command, will prevent the rest of the script from executing.
Hence, do not expect any code after the `launch_help` command to be executed.

As an alternative static API documentation is provided here.
It is split into sections based upon the modules for the documented code.
