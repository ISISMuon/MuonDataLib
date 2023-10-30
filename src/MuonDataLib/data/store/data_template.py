import h5py
import numpy as np
from numpy import ndarray


INT32 = np.int32
FLOAT32 = np.float32


class dataTemplate(object):
    """
    A basic class for storing
    muon data.
    """
    def __init__(self):
        return

    def _save_int(self, file, name: str, data: ndarray):
        return file.require_dataset(name, shape=data.shape, data=data, dtype=np.int32)

    def _save_float(self, file, name:str, data: ndarray):
        return file.require_dataset(name, shape=data.shape, data=data, dtype=np.float32)

    def _save_single_str(self, file, name:str, data: str):
        txt = data.encode()
        dtype = f'S{len(txt)}'
        return file.require_dataset(name, shape=(1), data=np.array(txt, dtype=dtype), dtype=dtype)


