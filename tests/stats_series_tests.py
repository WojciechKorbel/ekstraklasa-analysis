import unittest
from stats_series import *


class StatsSeriesTests(unittest.TestCase):
    # get_longest_series
    def test_get_longest_series_with_empty_list(self):
        param = []
        expected = {'win': 0,  'draw': 0,  'lost': 0}
        self.assertEqual(get_longest_series(param), expected)

    def test_get_longest_series_with_single_element(self):
        params = [
            ['W'],
            ['D'],
            ['L']
        ]
        expected = [
            {'win': 1, 'draw': 0, 'lost': 0},
            {'win': 0, 'draw': 1, 'lost': 0},
            {'win': 0, 'draw': 0, 'lost': 1}
        ]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_series(params[index]), expected[index])

    def test_get_longest_series_on_the_edge(self):
        params = [
            ['W', 'W', 'W', 'L', 'D'],
            ['L', 'D', 'L', 'L']
        ]
        expected = [
            {'win': 3, 'draw': 1, 'lost': 1},
            {'win': 0, 'draw': 1, 'lost': 2}
        ]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_series(params[index]), expected[index])

    def test_get_longest_series_in_the_middle(self):
        params = [
            ['L', 'L', 'W', 'W', 'W', 'L', 'W', 'L', 'W', 'W', 'W', 'W', 'D'],
            ['L', 'L', 'D', 'D', 'L'],
        ]
        expected = [
            {'win': 4, 'draw': 1, 'lost': 2},
            {'win': 0, 'draw': 2, 'lost': 2}
        ]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_series(params[index]), expected[index])


if __name__ == '__main__':
    unittest.main()
