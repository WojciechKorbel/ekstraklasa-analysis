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

    # get_longest_not_lose_series
    def test_get_longest_not_lose_series_with_empty_list(self):
        param = []
        expected = 0
        self.assertEqual(get_longest_not_lose_series(param), expected)

    def test_get_longest_not_lose_series_with_single_element(self):
        params = [
            ['W'],
            ['D'],
            ['L']
        ]
        expected = [1, 1, 0]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_not_lose_series(params[index]), expected[index])

    def test_get_longest_not_lose_series_on_the_edge(self):
        params = [
            ['L', 'W', 'D'],
            ['W', 'D', 'D', 'L', 'L', 'L']
        ]
        expected = [2, 3]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_not_lose_series(params[index]), expected[index])

    def test_get_longest_not_lose_series_in_the_middle(self):
        params = [
            ['L', 'W', 'D', 'L', 'L', 'L', 'W', 'D', 'W', 'D', 'L', 'L', 'W', 'D', 'W', 'D', 'L'],
            ['W', 'L', 'D', 'L', 'D', 'W', 'L']
        ]
        expected = [4, 2]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_not_lose_series(params[index]), expected[index])

    # get_longest_not_draw_series
    def test_get_longest_not_draw_series_with_empty_list(self):
        param = []
        expected = 0
        self.assertEqual(get_longest_not_draw_series(param), expected)

    def test_get_longest_not_draw_series_with_single_element(self):
        params = [
            ['W'],
            ['D'],
            ['L']
        ]
        expected = [1, 0, 1]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_not_draw_series(params[index]), expected[index])

    def test_get_longest_not_draw_series_on_the_edge(self):
        params = [
            ['L', 'W', 'D'],
            ['W', 'D', 'D', 'D', 'D', 'D', 'D', 'W', 'L', 'L', 'L']
        ]
        expected = [2, 4]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_not_draw_series(params[index]), expected[index])

    def test_get_longest_not_draw_series_in_the_middle(self):
        params = [
            ['D', 'W', 'L', 'D', 'D', 'D', 'W', 'L', 'W', 'L', 'D', 'D', 'W', 'L', 'W', 'L', 'D'],
            ['W', 'D', 'L', 'D', 'L', 'W', 'D']
        ]
        expected = [4, 2]
        for index in range(0, len(params)):
            self.assertEqual(get_longest_not_draw_series(params[index]), expected[index])


if __name__ == '__main__':
    unittest.main()
