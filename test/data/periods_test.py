from MuonDataLib.data.periods import (_Periods,
                                      Periods,
                                      EventsPeriods)

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.periods import PeriodsTestTemplate
from MuonDataLib.cython_ext.events_cache import EventsCache

import unittest
import numpy as np
import datetime


class _PeriodsTest(PeriodsTestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        self.requested = args[3]
        self.raw = args[4]
        self.counts = args[6]
        return _Periods(args[0], args[1], args[2],
                        args[5], args[7])

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        self.requested = args[3]
        self.raw = args[4]
        self.counts = np.asarray(args[6], dtype=np.double)
        return _Periods(args[0], args[1], args[2],
                        args[5], args[7])

    def save(self, period, file):
        period.save_nxs2(file, self.requested,
                         self.raw, self.counts)

    def setUp(self):
        self.filename = '_test_periods.nxs'


class PeriodsTest(PeriodsTestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        return Periods(*args)

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        return Periods(*args)

    def setUp(self):
        self.filename = 'test_periods.nxs'

    def save(self, period, file):
        period.save_nxs2(file)

    def test_periods_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        super().test_periods_object_stores_correct_info_single_period()

        self.assertArrays(self.period._dict['requested'], [500])
        self.assertArrays(self.period._dict['raw'], [1000])
        self.assertArrays(self.period._dict['total_counts'], [1.2e-5])

    def test_periods_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        super().test_periods_object_stores_correct_info_multiperiod()

        self.assertArrays(self.period._dict['requested'], [500, 400])
        self.assertArrays(self.period._dict['raw'], [1000, 500])
        self.assertArrays(self.period._dict['total_counts'], [1.2e-5, 4.5e-5])


class EventsPeriodsTest(PeriodsTestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray(args[4], dtype=np.int32))
        events = EventsPeriods(cache,
                               args[0], args[1],
                               args[2], args[5],
                               args[7])
        cache.save(np.asarray([[[2, 3], [5, 2]]], dtype=np.int32),
                   np.asarray([3.2, 5.6], dtype=np.double),
                   np.asarray([0], dtype=np.int32),
                   np.asarray([500], dtype=np.int32),
                   0.0, 100.0, 0.016
                   )

        return events

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray(args[4], dtype=np.int32))
        events = EventsPeriods(cache,
                               args[0], args[1],
                               args[2], args[5],
                               args[7])
        cache.save(np.asarray([[[2, 3], [5, 2]],
                               [[20, 21], [1, 3]]], dtype=np.int32),
                   np.asarray([3.2, 5.6], dtype=np.double),
                   np.asarray([0, 0], dtype=np.int32),
                   np.asarray([500, 100], dtype=np.int32),
                   0.0, 100.0, 0.016)
        return events

    def save(self, period, file):
        period.save_nxs2(file)

    def setUp(self):
        self.filename = 'test_events_periods.nxs'


if __name__ == '__main__':
    unittest.main()
