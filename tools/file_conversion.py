import h5py
import os
import sys
import shutil


"""
This is a script to update the 'old'
format data files (pre  Dec 2025) that
use 'detector_1' to the new format, which
uses 'detector_1_events'. It should otherwise
result in identical files.

This script is here to be helpful and is
not fully supported.

To use the script:

    python file_conversion.py <path_to_file>

This will update the file passed to it
(i.e. the origianl file will be deleted).

Author Anthony Lim
"""

# get user inputs
args = sys.argv
file_name = args[1]
# move the original file to a temp location
shutil.move(file_name, 'old.nxs')

# open files
with h5py.File('old.nxs', 'r') as file:
    with h5py.File(file_name, 'w') as new_file:
        # do top level manually
        for key in file.keys():
            new_file.require_group(key)
            # add attributes
            for attr in file[key].attrs:
                new_file[key].attrs.create(attr, file[key].attrs[attr])

            for tmp in file[key].keys():
                # if we need to update the group name
                if tmp == 'detector_1':
                    new_name = tmp + '_events'
                    # copies the data within the group
                    file[key].copy(source=tmp,
                                   dest=new_file[key],
                                   name=new_name)

                else:
                    # copies the group and contents
                    file[key].copy(tmp, new_file[key])
# clean up
os.remove('old.nxs')
print('done conversion')
