Getting Started
===============

To develop for MuonDataLib you will need to clone the github repository :code:`git clone https://github.com/ISISMuon/MuonDataLib.git`.
This will place you onto the main branch.
If you want to make changes then you will need to create a branch by using the command :code:`git checkout --no-track -b origin/main`.
You can then add your changes to this branch and once it is ready to be merged into main, you create a pull request (PR) for review.
Once the changes have been approved they will enter the merge queue, to make sure that the changes are compatible with the current version of main.

To reduce the chances of problems; Conda (alternatively you can use mamba) is used to manage the setup of the development environment (it is also used for the continuous integration).
To setup the developer’s environment use the command :code:`conda env create -f MuonDataLib.yml`.
Once it is completed you will need to use the command :code:`conda activate MuonDataLib-dev` to get access to the environment.
This guarantees that your setup is correct and it is isolated from the rest of your machine (i.e. changes here wont break any of your other software).
To reduce wasted time this environment uses pre-commit to make sure that the code being committed meets a minimum standard (flake8).
However, some setup is required.
In your conda environment enter :code:`conda update pre-commit` and once its complete type :code:`pre-commit install`.
This will create a bash file that will produce an error when you try to use it (known issue for Windows).
To exit your conda environment type :code:`conda deactivate` into the terminal.
Then you can reset your environment (but it keeps the bash file) with :code:`conda env update --file MuonDataLib.yml --prune`.
Once this is complete you will be able to use pre-commit.


To build your local version use :code:`python -m pip install -v -e .`, the full stop is important.
To run all of the tests locally use :code:`python -m pytest`


