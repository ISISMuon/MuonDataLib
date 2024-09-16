from MuonDataLib.data.periods import (_Periods,
                                      Periods,
                                      EventsPeriods)

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.periods import PeriodsTestTemplate
from MuonDataLib.cython_ext.events_cache import EventsCache

import unittest
import numpy as np


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
        self.raw = np.asarray(args[4], dtype=np.double)
        self.counts = np.asarray(args[6], dtype=np.int32)
        return _Periods(args[0], args[1], args[2],
                        args[5], args[7])

    def save(self, period, file):
        period.save_nxs2(file, self.requested,
                         self.raw, self.counts)

    def setUp(self):
        self.filename = '_periods.nxs'


class PeriodsTest(PeriodsTestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        return Periods(*args)

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        return Periods(*args)

    def setUp(self):
        self.filename = 'periods.nxs'

    def save(self, period, file):
        period.save_nxs2(file)

    def test_periods_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        super().test_periods_object_stores_correct_info_single_period()

        self.assertArrays(self.period._dict['requested'], [500])
        self.assertArrays(self.period._dict['raw'], [1000])
        self.assertArrays(self.period._dict['counts'], [1.23])

    def test_periods_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        super().test_periods_object_stores_correct_info_multiperiod()

        self.assertArrays(self.period._dict['requested'], [500, 400])
        self.assertArrays(self.period._dict['raw'], [1000, 500])
        self.assertArrays(self.period._dict['counts'], [1.23, 4.56])


class EventsPeriodsTest(PeriodsTestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        cache = EventsCache()
        events = EventsPeriods(cache,
                               args[0], args[1],
                               args[2], args[5],
                               args[7])
        cache.save(args[6], args[4], args[3])
        return events

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        cache = EventsCache()
        events = EventsPeriods(cache,
                               args[0], args[1],
                               args[2], args[5],
                               args[7])
        cache.save(args[6], args[4], args[3])
        return events

    def save(self, period, file):
        period.save_nxs2(file)

    def setUp(self):
        self.filename = 'events_periods.nxs'

    def test_periods_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        super().test_periods_object_stores_correct_info_single_period()

        counts, bins = self.period._cache.get_histograms()
        requested = self.period._cache.get_total_frames()

        self.assertArrays(requested, [500])
        self.assertArrays(bins, [1000])
        self.assertArrays(counts, [1.23])

    def test_periods_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        super().test_periods_object_stores_correct_info_multiperiod()

        counts, bins = self.period._cache.get_histograms()
        requested = self.period._cache.get_total_frames()

        self.assertArrays(requested, [500, 400])
        self.assertArrays(bins, [1000, 500])
        self.assertArrays(counts, [1.23, 4.56])


if __name__ == '__main__':
    unittest.main()
