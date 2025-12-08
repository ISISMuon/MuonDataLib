import numpy as np
import unittest


class TestHelper(unittest.TestCase):
    """
    A simple wrapper to make unit tests easier
    for nxs file
    """
    def compare_keys(self, nxs, expected):
        """
        Compares the options (keys) from a nexus file
        to an expected list
        :param nxs: the open nexus file (at the correct level)
        :param expected: the list of expected keys
        :return: the keys from the nexus file
        """
        keys = list(nxs.keys())
        # check same number of keys
        self.assertEqual(len(expected), len(keys))
        ref = expected
        # check keys match
        for value in keys:
            self.assertTrue(value in ref)
            ref.remove(value)
        # check all of the expected values have been seen
        self.assertEqual(len(ref), 0)
        return keys

    def assertString(self, group, key, expected):
        """
        The strings in nexus files are lists,
        with just one element. They also need
        decoding
        :param group: the open nexus group
        :param key: the key we want to check
        :param expected: the expected string
        """
        string_list = group[key]
        self.assertEqual(len(string_list), 1)
        self.assertEqual(string_list[0].decode(), expected)

    def assertArrays(self, array, ref):
        for j in range(len(array)):
            len_a = len(array)
            len_r = len(ref)
            msg = f'The arrays are not the same length: {len_a}, {len_r}'
            self.assertEqual(len_a, len_r, msg=msg)

            if isinstance(array[j], (list, np.ndarray)):
                self.assertArrays(array[j], ref[j])
            else:
                msg = f'values do not match in array {array[j]}, {ref[j]}'
                self.assertAlmostEqual(array[j], ref[j], 3, msg=msg)

    def assertMockOnce(self, mock, expected_args):
        """
        A method to check that a mock has the correct
        args. We assume that it is called once.
        This is needed as we often have arrays.
        :param mock: the mock object
        :param expected_args: the expected args for the
        call
        """
        mock.assert_called_once()
        args = mock.call_args[0]

        self.assertEqual(len(expected_args),
                         len(args))
        for k in range(len(args)):
            self.assertArrays(args[k],
                              expected_args[k])

    def check_shape(self, shape, k, x0, x1, y0, y1):
        """
        A method to compare the vertical rectangles
        that have been added.
        :param shape: the details of the shape
        :param k: the domain index (starts at 0)
        :param x0: the start x value
        :param x1: the end x value
        :param y0: the start y value
        :param y1: the end y value
        """
        self.assertEqual(shape['fillcolor'], 'PaleGreen')
        self.assertEqual(shape['layer'], 'above')
        self.assertEqual(shape['line']['color'], 'black')
        self.assertEqual(shape['line']['width'], 4)
        self.assertEqual(shape['opacity'], 0.3)
        self.assertEqual(shape['type'], 'rect')
        self.assertEqual(shape['x0'], x0)
        self.assertEqual(shape['x1'], x1)
        self.assertEqual(shape['y0'], y0)
        self.assertEqual(shape['y1'], y1)
        if k == 0:
            self.assertEqual(shape['xref'], 'x')
            self.assertEqual(shape['yref'], 'y domain')
        else:
            self.assertEqual(shape['xref'], f'x{k+1}')
            self.assertEqual(shape['yref'], f'y{k+1} domain')

    def check_shapes(self, expected):
        """
        Method to check the list of shapes currently applied
         to the plots.
         :param expected: the expected shapes
        """
        N_plots = 2
        shapes = self.presenter._plot.fig.layout.shapes
        n = 0

        for k in range(len(expected)):
            for j in range(N_plots):
                self.check_shape(shapes[n], j, *expected[k])
                n += 1
