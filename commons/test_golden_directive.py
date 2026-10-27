"""Unit tests for the Y metric. Run: python3 -m unittest -v"""

import unittest

from golden_directive import harmonic_mean, run_episode


class TestHarmonicMean(unittest.TestCase):
    def test_collapse(self):
        self.assertEqual(harmonic_mean(0, 10), 0.0)
        self.assertEqual(harmonic_mean(10, 0), 0.0)
        self.assertEqual(harmonic_mean(0, 0), 0.0)

    def test_equal(self):
        self.assertEqual(harmonic_mean(7, 7), 7.0)

    def test_between_inputs_pulled_toward_smaller(self):
        self.assertAlmostEqual(harmonic_mean(30, 70), 42.0)
        self.assertGreater(harmonic_mean(30, 70), 30)
        self.assertLess(harmonic_mean(30, 70), 70)
        self.assertLess(harmonic_mean(30, 70), 50)  # below arithmetic mean

    def test_negative_raises_not_silent_clip(self):
        with self.assertRaises(ValueError):
            harmonic_mean(-1, 10)
        with self.assertRaises(ValueError):
            harmonic_mean(10, -1)


class TestEpisode(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(run_episode("restrained", 42), run_episode("restrained", 42))

    def test_unknown_policy_raises(self):
        with self.assertRaises(ValueError):
            run_episode("nope", 42)


if __name__ == "__main__":
    unittest.main()
