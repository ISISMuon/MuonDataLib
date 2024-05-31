from MuonDataLib.data.loader.load_event import LoadEventData
import unittest
import time
import os
import numpy as np


DATADIR = os.path.join(os.path.dirname(__file__),
                       '..',
                       'data_files')
INFILE = os.path.join(DATADIR, 'complete_run.nxs')
REFFILE = None
OUTFILE = 'single_period_event_test.nxs'


class SinglePeriodEventTest(unittest.TestCase):

    def test_run_time(self):
        """
        This is fairly fast code, so will
        do 100 workflows to get some statistics.
        """
        times = []
        for j in range(100):
            start = time.time()

            data = LoadEventData()
            data.load_data(INFILE)
            hist, bins = data.get_histograms()
            times.append(time.time() - start)
            del data
        # the requirment is that its less than 5 seconds
        self.assertLess(np.mean(times), 0.1)
        self.assertLess(np.max(times), 1.0)
        self.assertLess(np.max(times), 5.00)


if __name__ == '__main__':
    unittest.main()
