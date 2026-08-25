import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "pi-zh-apply.py"
SPEC = importlib.util.spec_from_file_location("pi_zh_apply", MODULE_PATH)
assert SPEC and SPEC.loader
pi_zh_apply = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pi_zh_apply)


class PiZhApplyTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.package_root = Path(self.temp_dir.name) / "pi-coding-agent"
        self.dist = self.package_root / "dist"
        (self.dist / "core").mkdir(parents=True)
        (self.dist / "modes").mkdir()
        (self.dist / "cli").mkdir()
        (self.dist / "bundle").mkdir()
        (self.dist / "cli.js").write_text("// entry\n", encoding="utf-8")
        (self.dist / "cli" / "args.js").write_text("你好 World\n", encoding="utf-8")
        (self.dist / "bundle" / "cli.js").write_text("// bundled entry\n", encoding="utf-8")
        (self.package_root / "package.json").write_text(
            json.dumps({"version": "0.84.3", "bin": {"pi": "dist/bundle/cli.js"}}),
            encoding="utf-8",
        )
        self.patches = {"cli\\args.js": [["Hello", "你好"], ["World", "世界"]]}

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_explicit_dist_and_windows_patch_path_work_on_posix(self):
        self.assertEqual(pi_zh_apply.find_dist(str(self.dist)), self.dist.resolve())
        self.assertEqual(
            pi_zh_apply.target_path(self.dist, "cli\\args.js"),
            self.dist / "cli" / "args.js",
        )

    def test_partial_localization_can_continue_and_is_idempotent(self):
        before = pi_zh_apply.check_status(self.dist, self.patches)
        self.assertEqual((before.localized, before.applied, before.unmatched), (1, 1, 0))

        first = pi_zh_apply.apply(self.dist, self.patches)
        self.assertEqual((first.applied, first.localized, first.unmatched), (1, 1, 0))
        self.assertEqual((self.dist / "cli" / "args.js").read_text(encoding="utf-8"), "你好 世界\n")

        second = pi_zh_apply.apply(self.dist, self.patches)
        self.assertEqual((second.applied, second.localized, second.unmatched), (0, 2, 0))

    def test_bundle_entry_redirects_to_localized_unbundled_cli(self):
        self.assertEqual(pi_zh_apply.bundle_entry_status(self.dist), "待切换")
        self.assertTrue(pi_zh_apply.redirect_bundle_entry(self.dist))
        self.assertEqual(pi_zh_apply.bundle_entry_status(self.dist), "已切换")
        self.assertEqual(
            (self.dist / "bundle" / "cli.js").read_text(encoding="utf-8"),
            pi_zh_apply.BUNDLE_PROXY,
        )
        self.assertFalse(pi_zh_apply.redirect_bundle_entry(self.dist))

    def test_patch_path_cannot_escape_dist(self):
        with self.assertRaises(ValueError):
            pi_zh_apply.target_path(self.dist, "../outside.js")


if __name__ == "__main__":
    unittest.main()
