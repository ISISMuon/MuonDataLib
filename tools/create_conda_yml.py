import argparse
import sys
from conda_dict_to_yml import write_conda_yml_from_dict


versions = ['3.8', '3.9', '3.10', '3.11']


def get_input():
    """
    get the python version from the command line arg
    :returns the Python version
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('version',
                        help='the Python version'
                        ' (3.8, 3.9, 3.10, 3.11)', type=str)
    args = parser.parse_args()

    if args.version not in versions:
        raise ValueError(str(args.version) + ' is not a supported'
                                             ' Python version.')
    print(args.version)
    return args.version


def get_info(version):
    """
    Gets the yml_dict and file name from the OS
    :param version: the Python version
    :Return a dict of contents for the yml file and file name
    """
    yml_dict = create_default(version)
    file_name = str(yml_dict["name"])+'.yml'
    return yml_dict, file_name


"""
Here we list the conda recipes.
We start with a default.
Can add changes for specific OS's
"""


def create_default(version):
    """
    The default yml file for all OS's.
    Should only change these values if there is a
    good reason.
    :param version: Python version to build (exclude patch)
    """
    default_yml = {}

    pip_dict = {}

    default_yml['name'] = 'MuonDataLib-dev'
    default_yml['channels'] = 'conda-forge'
    default_yml['dependencies'] = {'python': '=' + version + '.*',
                                   'numpy': '',
                                   'pytest': '',
                                   'pre-commit': '>=2.15',
                                   'Cython': '',
                                   'pip': pip_dict}
    return default_yml


if __name__ == "__main__":
    try:
        version = get_input()
        yml_dict, file_name = get_info(version)
        with open(file_name, 'w') as outfile:
            write_conda_yml_from_dict(yml_dict, outfile)

    except ValueError:
        error = sys.exc_info()[1]
        print(error)
