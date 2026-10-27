"""Tests for the Clean Up-style toy. Run: python3 -m unittest -v"""

import unittest

from cleanup_demo import run_cleanup_episode


class TestCleanup(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(
            run_cleanup_episode("mixed", 42), run_cleanup_episode("mixed", 42)
        )

    def test_bounds_and_unknown(self):
        result = run_cleanup_episode("all_cleaners", 42)
        self.assertTrue(0 <= result["final_cleanliness"] <= 100)
        self.assertTrue(result["final_stock"] >= 0)
        self.assertTrue(all(a["A"] >= 0 for a in result["agents"]))
        with self.assertRaises(ValueError):
            run_cleanup_episode("nope", 42)


if __name__ == "__main__":
    unittest.main()
