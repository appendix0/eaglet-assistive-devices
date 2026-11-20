import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import design_params as dp  # noqa: E402


class DesignParamTests(unittest.TestCase):
    def test_grip_is_19_7_percent_of_hand_length(self):
        opt, rng, ra = dp.grip_diameter(180)
        self.assertAlmostEqual(opt, 35.46, places=2)
        self.assertEqual(rng, (30.0, 40.0))
        self.assertAlmostEqual(ra, 38.1)

    def test_grip_rejects_implausible_hand_length(self):
        with self.assertRaises(ValueError):
            dp.grip_diameter(50)

    def test_default_torque_is_28_lbf_in(self):
        self.assertAlmostEqual(dp.DEFAULT_TORQUE_NM, 3.1636, places=3)

    def test_lever_length_keeps_force_at_ada_limit(self):
        # 3.16 N*m / 22.2 N = 142.5 mm
        self.assertAlmostEqual(dp.min_lever_length_mm(), 142.5, delta=0.1)
        self.assertAlmostEqual(dp.min_lever_length_mm(1.11, 22.2), 50.0, places=6)

    def test_bending_stress_formula(self):
        # width is the section depth: 6 * 100 N * 100 mm / (10 mm * 20 mm^2) = 15 MPa
        self.assertAlmostEqual(dp.lever_bending_stress_mpa(100, 20, 10, 100), 15.0)

    def test_thin_lever_flagged(self):
        self.assertFalse(dp.lever_report(dp.DEFAULT_TORQUE_NM, 18, 12, 200)["ok"])
        self.assertTrue(dp.lever_report(dp.DEFAULT_TORQUE_NM, 24, 14, 200)["ok"])


if __name__ == "__main__":
    unittest.main()
