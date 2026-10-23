import unittest
from demo import seconds


class FeatureContractTest(unittest.TestCase):
    def test_equivalent_representations(self):
        for value in (0, 1, 30, 3600):
            self.assertEqual(seconds(value, 's'), seconds(value * 1000, 'ms'))

    def test_missing_conversion_is_detectable(self):
        self.assertNotEqual(30000, seconds(30000, 'ms'))

    def test_invalid_inputs(self):
        for value, unit in ((True, 's'), ('30', 's'), (-1, 's'), (float('nan'), 's'),
                            (float('inf'), 's'), (30, 'minutes'), (30, None)):
            with self.subTest(value=value, unit=unit), self.assertRaises(ValueError):
                seconds(value, unit)
