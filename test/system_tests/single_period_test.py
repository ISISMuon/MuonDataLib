from MuonDataLib.data.loader.load_nxs2 import load_nxs2
import unittest
import time
import os
import numpy as np
import filecmp


DATADIR = os.path.join(os.path.dirname(__file__),
                       '..',
                       'data_files')
INFILE = os.path.join(DATADIR, 'HIFI00180594.nxs')
REFFILE = os.path.join(DATADIR, 'HIFI42.nxs')
OUTFILE = 'single_period_test.nxs'


class SinglePeriodSystemTest(unittest.TestCase):

    def test_run_time(self):
        """
        This is fairly fast code, so will
        do 100 workflows to get some statistics.
        """
        times = []
        for j in range(100):
            start = time.time()
            data = load_nxs2(INFILE)
            data.save_histograms(OUTFILE)
            times.append(time.time() - start)
            os.remove(OUTFILE)
            del data
        # the requirment is that its less than 5 seconds
        self.assertLess(np.mean(times), 0.1)
        self.assertLess(np.max(times), 1.0)
        self.assertLess(np.max(times), 5.00)

    def test_saved_data(self):
        data = load_nxs2(INFILE)
        data.save_histograms(OUTFILE)

        self.assertTrue(filecmp.cmp(REFFILE, OUTFILE, shallow=False),
                        msg=('The single period nexus file does not '
                             'match the reference file'))

        os.remove(OUTFILE)


if __name__ == '__main__':
    unittest.main()
