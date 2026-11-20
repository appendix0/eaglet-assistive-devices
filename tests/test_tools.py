import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import at_eval  # noqa: E402
import check_privacy  # noqa: E402

HEADER = ",".join(at_eval.COLUMNS)


def write_case(root, name, rows, stl=False):
    d = Path(root) / name
    (d / "stl").mkdir(parents=True)
    (d / "evaluation.csv").write_text(HEADER + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    if stl:
        (d / "stl" / "part.stl").write_text("solid x\nendsolid x\n")


BASE_NO = "baseline,2026-10-10,,N,4,,,,"
BASE_HELP3 = "baseline,2026-10-10,,Y,3,,,,"
V1 = "v1,2026-12-01,{days},{done},{help},3,N,4,"
V2 = "v2,2026-12-10,7,{done},{help},4,N,5,"


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def status(self, name_prefix):
        for name, status, _ in at_eval.targets(at_eval.evaluate(self.root)):
            if name.startswith(name_prefix):
                return status
        raise KeyError(name_prefix)

    def test_all_targets_pass(self):
        write_case(self.root, "case-01", [BASE_NO, V1.format(days=14, done="Y", help=1),
                                          V2.format(done="Y", help=0)], stl=True)
        write_case(self.root, "case-02", [BASE_HELP3, V1.format(days=15, done="Y", help=2),
                                          V2.format(done="Y", help=2)], stl=True)
        write_case(self.root, "case-03", [BASE_HELP3, V1.format(days=20, done="Y", help=3),
                                          V2.format(done="Y", help=3)], stl=True)
        statuses = [s for _, s, _ in at_eval.targets(at_eval.evaluate(self.root))]
        self.assertEqual(statuses, ["PASS"] * 5)

    def test_kpi_fails_when_only_one_of_three_improves(self):
        write_case(self.root, "case-01", [BASE_NO, V1.format(days=14, done="Y", help=1)])
        for n in ("02", "03"):
            write_case(self.root, f"case-{n}", [BASE_HELP3, V1.format(days=14, done="Y", help=3)])
        self.assertEqual(self.status("KPI"), "FAIL")

    def test_kpi_uses_final_version_not_v1(self):
        # v1 helped, v2 regressed back to baseline help level -> not improved
        write_case(self.root, "case-01", [BASE_HELP3, V1.format(days=14, done="Y", help=1),
                                          V2.format(done="Y", help=3)])
        case = at_eval.evaluate(self.root)["case-01"]
        self.assertFalse(at_eval.improved(case))

    def test_short_first_use_fails(self):
        write_case(self.root, "case-01", [BASE_NO, V1.format(days=13, done="Y", help=1)])
        self.assertEqual(self.status("v1 used"), "FAIL")

    def test_in_progress_is_pending_not_fail(self):
        write_case(self.root, "case-01", [BASE_NO])
        self.assertEqual(self.status("KPI"), "PENDING")
        self.assertEqual(self.status("v1 used"), "PENDING")
        self.assertEqual(self.status("at least 1 revision"), "PENDING")

    def test_template_folder_is_ignored(self):
        write_case(self.root, "_template", [BASE_NO])
        self.assertEqual(at_eval.evaluate(self.root), {})

    def test_out_of_range_help_level_rejected(self):
        write_case(self.root, "case-01", ["baseline,2026-10-10,,N,5,,,,"])
        with self.assertRaises(at_eval.DataError):
            at_eval.evaluate(self.root)

    def test_version_row_requires_days_used(self):
        write_case(self.root, "case-01", [BASE_NO, "v1,2026-12-01,,Y,1,3,N,4,"])
        with self.assertRaises(at_eval.DataError):
            at_eval.evaluate(self.root)

    def test_wrong_header_rejected(self):
        d = Path(self.root) / "case-01"
        d.mkdir()
        (d / "evaluation.csv").write_text("timepoint,score\nbaseline,3\n")
        with self.assertRaises(at_eval.DataError):
            at_eval.evaluate(self.root)

    def test_shipped_template_is_valid(self):
        repo = Path(__file__).resolve().parent.parent
        at_eval.load_case(repo / "cases" / "_template" / "evaluation.csv")


class PrivacyTests(unittest.TestCase):
    def scan_text(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(text)
        try:
            return [kind for _, _, kind, _ in check_privacy.scan([f.name])]
        finally:
            Path(f.name).unlink()

    # Fake values are assembled at runtime so this file passes the scan itself.
    def test_detects_phone_formats(self):
        self.assertEqual(self.scan_text("연락처 010-" + "1234-5678"), ["phone"])
        self.assertEqual(self.scan_text("010" + "12345678"), ["phone"])

    def test_detects_resident_id_and_email(self):
        self.assertEqual(self.scan_text("900101-" + "1234567"), ["resident-id"])
        self.assertEqual(self.scan_text("someone" + "@school.ac.kr"), ["email"])

    def test_allows_placeholders_and_measurements(self):
        self.assertEqual(self.scan_text("name@example.com, grip 32.0 mm, 2026-10-10"), [])


if __name__ == "__main__":
    unittest.main()
