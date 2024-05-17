from MuonDataLib.test_helpers.nexus import NexusTestHelper
import unittest


class UtilsTest(unittest.TestCase):

    def test_compare_keys(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        """
        nexus = NexusTestHelper()
        data = {'sample': 1, 'source': 2, 'user': 3}
        ref = ['sample', 'source', 'user']
        # this has an assertion within it
        nexus.compare_keys(data, ref)

    def test_compare_keys_bad_case(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        """
        nexus = NexusTestHelper()
        data = {'sample': 1, 'Source': 2, 'user': 3}
        ref = ['sample', 'source', 'user']
        with self.assertRaises(AssertionError):
            nexus.compare_keys(data, ref)

    def test_compare_keys_repeated_key(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        """
        nexus = NexusTestHelper()
        data = {'sample': 1, 'Source': 2, 'user': 3}
        ref = ['sample', 'source', 'sample']
        with self.assertRaises(AssertionError):
            nexus.compare_keys(data, ref)

    def test_compare_keys_missing_key(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        """
        nexus = NexusTestHelper()
        data = {'sample': 1, 'Source': 2, 'user': 3}
        ref = ['sample', 'user']
        with self.assertRaises(AssertionError):
            nexus.compare_keys(data, ref)

    def test_assertString(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        The dicts have string keys and the
        values are a list of encoded strings.
        """
        nexus = NexusTestHelper()

        data = {'name': ['unit test'.encode()], 'version': ['1.1.2'.encode()]}
        # contains an assert
        nexus.assertString(data, 'name', 'unit test')
        nexus.assertString(data, 'version', '1.1.2')

    def test_assertString_not_encoded(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        The dicts have string keys and the
        values are a list of encoded strings.
        """
        nexus = NexusTestHelper()

        data = {'name': ['unit test'], 'version': ['1.1.2']}

        with self.assertRaises(AttributeError):
            nexus.assertString(data, 'name', 'unit test')
            nexus.assertString(data, 'version', '1.1.2')

    def test_assertString_missing_key(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        The dicts have string keys and the
        values are a list of encoded strings.
        """
        nexus = NexusTestHelper()

        data = {'name': ['unit test'], 'version': ['1.1.2']}

        with self.assertRaises(KeyError):
            nexus.assertString(data, 'python', 'unit test')

    def test_assertString_value_does_not_match(self):
        """
        Since the hdf5 reader returns a dict
        object, we can pass just a dict
        to represent the readers results.
        The dicts have string keys and the
        values are a list of encoded strings.
        """
        nexus = NexusTestHelper()

        data = {'name': ['unit test'.encode()], 'version': ['1.1.2'.encode()]}

        with self.assertRaises(AssertionError):
            nexus.assertString(data, 'name', 'Unit test')
            nexus.assertString(data, 'version', '2.1.2')

    def test_assertArrays_no_recursion(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [1, 2, 3]
        ref = [1, 2, 3]
        nexus = NexusTestHelper()

        nexus.assertArrays(array, ref)

    def test_assertArrays_no_recursion_diff_len(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [1, 2, 3, 4]
        ref = [1, 2, 3]
        nexus = NexusTestHelper()
        with self.assertRaises(AssertionError):
            nexus.assertArrays(array, ref)

    def test_assertArrays_no_recursion_mismatch(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [1, 2, 3.01]
        ref = [1, 2, 3]
        nexus = NexusTestHelper()
        with self.assertRaises(AssertionError):
            nexus.assertArrays(array, ref)

    def test_assertArrays_one_recursion(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [[1, 2, 3], [4, 5, 6]]
        ref = [[1, 2, 3], [4, 5, 6]]
        nexus = NexusTestHelper()

        nexus.assertArrays(array, ref)

    def test_assertArrays_no_recursion_diff_len_1(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [[1, 2, 3, 4], [4, 5, 6]]
        ref = [[1, 2, 3], [4, 5, 6]]
        nexus = NexusTestHelper()
        with self.assertRaises(AssertionError):
            nexus.assertArrays(array, ref)

    def test_assertArrays_no_recursion_diff_len_2(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [[1, 2, 3], [4, 5, 6, 7]]
        ref = [[1, 2, 3], [4, 5, 6]]
        nexus = NexusTestHelper()
        with self.assertRaises(AssertionError):
            nexus.assertArrays(array, ref)

    def test_assertArrays_no_recursion_mismatch_1(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [[1, 2, 3.01], [4, 5, 6]]
        ref = [[1, 2, 3], [4, 5, 6]]
        nexus = NexusTestHelper()
        with self.assertRaises(AssertionError):
            nexus.assertArrays(array, ref)

    def test_assertArrays_no_recursion_mismatch_2(self):
        """
        The assertArrays method is a recursive so to test it
        we will use something akin to proof by induction.
        We will show it does/doesn't works without any recursion (n=1), then
        that it does/doesn't work with a single recursion (n+1). Therefore,
        it will work for an arbitary number of recursions.
        """
        array = [[1, 2, 3], [4, 5, 5.2]]
        ref = [[1, 2, 3], [4, 5, 6]]
        nexus = NexusTestHelper()
        with self.assertRaises(AssertionError):
            nexus.assertArrays(array, ref)


if __name__ == '__main__':
    unittest.main()
