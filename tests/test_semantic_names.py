"""
Tests for semantic naming and regression fixtures.

Covers:
  1. SemanticNamer – translates win_* filenames to semantic role names.
  2. asset_map.json – validates structure and completeness.
  3. Regression fixtures – verifies that the canonical PNG files from
     mathieujobin/kwin_e13 have the expected SHA-256 checksums.
  4. ThemeExtractor --semantic-names mode – verifies that extracted images
     are written with semantic filenames.
"""

import hashlib
import json
import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

from semantic_names import SemanticNamer
from create_test_db import create_test_db_v1, create_sample_png

FIXTURES_DIR = Path(__file__).parent / "fixtures"
ASSET_MAP_PATH = REPO_ROOT / "asset_map.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_fixture_hashes() -> dict:
    with open(FIXTURES_DIR / "fixture_hashes.json") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# 1. SemanticNamer unit tests
# ---------------------------------------------------------------------------

class TestSemanticNamer(unittest.TestCase):
    """Tests for the SemanticNamer helper."""

    def setUp(self):
        self.namer = SemanticNamer(ASSET_MAP_PATH)

    # --- translate() ---

    def test_translate_ppm_state1(self):
        self.assertEqual(self.namer.translate("win_a_1.ppm"), "button_iconify_uns.png")

    def test_translate_ppm_state2(self):
        self.assertEqual(self.namer.translate("win_a_2.ppm"), "button_iconify_sel.png")

    def test_translate_ppm_state3(self):
        self.assertEqual(self.namer.translate("win_a_3.ppm"), "button_iconify_clk.png")

    def test_translate_png_variant(self):
        self.assertEqual(self.namer.translate("win_l_1.png"), "button_close_uns.png")

    def test_translate_all_states_close_button(self):
        self.assertEqual(self.namer.translate("win_l_1.ppm"), "button_close_uns.png")
        self.assertEqual(self.namer.translate("win_l_2.ppm"), "button_close_sel.png")
        self.assertEqual(self.namer.translate("win_l_3.ppm"), "button_close_clk.png")

    def test_translate_border_left(self):
        self.assertEqual(self.namer.translate("win_e_1.ppm"), "border_left_uns.png")

    def test_translate_corner_bottomleft(self):
        self.assertEqual(self.namer.translate("win_f_1.ppm"), "corner_bottomleft_uns.png")

    def test_translate_titlebar_bg(self):
        self.assertEqual(self.namer.translate("win_m_2.ppm"), "titlebar_bg_sel.png")

    def test_translate_titlebar_title_full(self):
        self.assertEqual(self.namer.translate("win_o_3.ppm"), "titlebar_title_clk.png")

    def test_translate_titlebar_title_small(self):
        self.assertEqual(self.namer.translate("win_p_1.ppm"), "titlebar_title_small_uns.png")

    def test_translate_unknown_stem_returns_none(self):
        self.assertIsNone(self.namer.translate("win_z_1.ppm"))

    def test_translate_non_win_name_returns_none(self):
        self.assertIsNone(self.namer.translate("background.png"))

    def test_translate_path_preserves_directory(self):
        p = Path("/some/dir/win_a_1.ppm")
        result = self.namer.translate_path(p)
        self.assertIsNotNone(result)
        self.assertEqual(result.parent, Path("/some/dir"))
        self.assertEqual(result.name, "button_iconify_uns.png")

    # --- get_semantic_role() ---

    def test_get_semantic_role_known(self):
        self.assertEqual(self.namer.get_semantic_role("win_l"), "button_close")

    def test_get_semantic_role_unknown_returns_none(self):
        self.assertIsNone(self.namer.get_semantic_role("win_z"))

    # --- list_stems() ---

    def test_list_stems_returns_all_16(self):
        stems = self.namer.list_stems()
        self.assertEqual(len(stems), 16)

    def test_list_stems_sorted(self):
        stems = self.namer.list_stems()
        self.assertEqual(stems, sorted(stems))

    def test_list_stems_contains_expected(self):
        stems = self.namer.list_stems()
        for letter in "abcdefghijklmnop":
            self.assertIn(f"win_{letter}", stems)


# ---------------------------------------------------------------------------
# 2. asset_map.json structural validation
# ---------------------------------------------------------------------------

class TestAssetMapStructure(unittest.TestCase):
    """Validates the structure and content of asset_map.json."""

    @classmethod
    def setUpClass(cls):
        with open(ASSET_MAP_PATH) as fh:
            cls.data = json.load(fh)

    def test_state_map_has_three_entries(self):
        sm = self.data["state_map"]
        self.assertEqual(sm["1"], "uns")
        self.assertEqual(sm["2"], "sel")
        self.assertEqual(sm["3"], "clk")

    def test_assets_has_16_entries(self):
        self.assertEqual(len(self.data["assets"]), 16)

    def test_every_asset_has_semantic_role(self):
        for stem, entry in self.data["assets"].items():
            self.assertIn("semantic_role", entry, f"Missing semantic_role for {stem}")

    def test_every_asset_has_three_png_states(self):
        for stem, entry in self.data["assets"].items():
            states = entry.get("states", {})
            png_states = [k for k in states if k.endswith(".png")]
            self.assertEqual(
                len(png_states), 3,
                f"Expected 3 PNG state entries for {stem}, got {len(png_states)}"
            )

    def test_every_asset_has_type(self):
        valid_types = {"button", "decoration", "title"}
        for stem, entry in self.data["assets"].items():
            self.assertIn(entry.get("type"), valid_types,
                          f"Invalid type for {stem}: {entry.get('type')}")

    def test_svg_buttons_section_present(self):
        self.assertIn("svg_buttons", self.data)

    def test_svg_buttons_are_marked_non_authoritative(self):
        for name, entry in self.data["svg_buttons"].items():
            if not isinstance(entry, dict):
                continue  # skip comment keys
            self.assertFalse(
                entry.get("authoritative_raster", True),
                f"SVG {name} should not be authoritative_raster=True"
            )

    def test_semantic_names_are_unique(self):
        """No two different stems should share the same semantic_role."""
        roles = [e["semantic_role"] for e in self.data["assets"].values()]
        self.assertEqual(len(roles), len(set(roles)), "Duplicate semantic roles found")

    def test_win_o_is_title_type(self):
        self.assertEqual(self.data["assets"]["win_o"]["type"], "title")

    def test_win_p_is_title_type(self):
        self.assertEqual(self.data["assets"]["win_p"]["type"], "title")

    def test_win_l_is_button_close(self):
        self.assertEqual(
            self.data["assets"]["win_l"]["semantic_role"], "button_close"
        )


# ---------------------------------------------------------------------------
# 3. Regression fixtures – SHA-256 hash verification
# ---------------------------------------------------------------------------

class TestRegressionFixtures(unittest.TestCase):
    """
    Verifies that canonical PNG files from kwin_e13 (mathieujobin/kwin_e13 @
    bd9908ec) match their expected SHA-256 checksums stored in
    tests/fixtures/fixture_hashes.json.
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = _load_fixture_hashes()

    def _check_fixture(self, filename: str):
        path = FIXTURES_DIR / filename
        if not path.exists():
            self.skipTest(f"Fixture not present: {filename}")
        self.assertEqual(
            _sha256(path),
            self.expected[filename],
            f"SHA-256 mismatch for fixture {filename}"
        )

    def test_fixture_win_a_1_uns(self):
        self._check_fixture("win_a_1.png")

    def test_fixture_win_a_2_sel(self):
        self._check_fixture("win_a_2.png")

    def test_fixture_win_a_3_clk(self):
        self._check_fixture("win_a_3.png")

    def test_fixture_win_e_1_border_left_uns(self):
        self._check_fixture("win_e_1.png")

    def test_fixture_win_e_2_border_left_sel(self):
        self._check_fixture("win_e_2.png")

    def test_fixture_win_e_3_border_left_clk(self):
        self._check_fixture("win_e_3.png")

    def test_fixture_win_f_1_corner_bottomleft(self):
        self._check_fixture("win_f_1.png")

    def test_fixture_win_g_1_border_bottom(self):
        self._check_fixture("win_g_1.png")

    def test_fixture_win_h_1_corner_bottomright(self):
        self._check_fixture("win_h_1.png")

    def test_fixture_win_i_1_border_right(self):
        self._check_fixture("win_i_1.png")

    def test_fixture_win_l_1_button_close_uns(self):
        self._check_fixture("win_l_1.png")

    def test_fixture_win_l_2_button_close_sel(self):
        self._check_fixture("win_l_2.png")

    def test_fixture_win_l_3_button_close_clk(self):
        self._check_fixture("win_l_3.png")

    def test_fixture_win_m_1_titlebar_bg(self):
        self._check_fixture("win_m_1.png")

    def test_fixture_win_o_1_titlebar_title(self):
        self._check_fixture("win_o_1.png")

    def test_fixture_win_p_1_titlebar_title_small(self):
        self._check_fixture("win_p_1.png")

    def test_all_fixtures_are_valid_png(self):
        """Every fixture PNG must start with the PNG magic bytes."""
        PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
        for filename in self.expected:
            path = FIXTURES_DIR / filename
            if not path.exists():
                continue
            with open(path, "rb") as fh:
                header = fh.read(8)
            self.assertEqual(
                header, PNG_MAGIC,
                f"Fixture {filename} does not start with PNG magic bytes"
            )


# ---------------------------------------------------------------------------
# 4. ThemeExtractor --semantic-names integration test
# ---------------------------------------------------------------------------

class TestExtractorSemanticNames(unittest.TestCase):
    """Integration tests for ThemeExtractor with semantic_names=True."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _make_db_with_win_image(self, filename: str) -> Path:
        """Create a minimal DB v1 with a single win_* PNG entry."""
        # Create a proper PNG that Pillow can fully decode (not just header-parse)
        try:
            from PIL import Image as PILImage
            import io
            img = PILImage.new("RGB", (4, 4), color=(200, 100, 50))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            png_data = buf.getvalue()
        except ImportError:
            png_data = create_sample_png()
        entries = {filename: png_data}
        db_path = self.test_dir / "test.db"
        create_test_db_v1(db_path, entries)
        return db_path

    def _extract(self, db_path: Path, semantic: bool) -> Path:
        # Import here so path-sys setup above takes effect
        from extract_theme import ThemeExtractor
        out_dir = self.test_dir / "output"
        extractor = ThemeExtractor(out_dir, verbose=False, semantic_names=semantic)
        result = extractor.extract_theme(db_path, extract_images=True, extract_config=False)
        self.assertTrue(result["success"])
        return out_dir / "images"

    def test_semantic_names_flag_renames_win_a(self):
        db = self._make_db_with_win_image("win_a_1.png")
        images_dir = self._extract(db, semantic=True)
        self.assertTrue(
            (images_dir / "button_iconify_uns.png").exists(),
            "Expected button_iconify_uns.png to be created"
        )
        self.assertFalse(
            (images_dir / "win_a_1.png").exists(),
            "Legacy win_a_1.png should not be created in semantic mode"
        )

    def test_semantic_names_flag_renames_win_l(self):
        db = self._make_db_with_win_image("win_l_3.png")
        images_dir = self._extract(db, semantic=True)
        self.assertTrue((images_dir / "button_close_clk.png").exists())

    def test_no_semantic_names_keeps_original(self):
        db = self._make_db_with_win_image("win_a_1.png")
        images_dir = self._extract(db, semantic=False)
        self.assertTrue((images_dir / "win_a_1.png").exists())

    def test_semantic_names_titlebar_bg(self):
        db = self._make_db_with_win_image("win_m_2.png")
        images_dir = self._extract(db, semantic=True)
        self.assertTrue((images_dir / "titlebar_bg_sel.png").exists())

    def test_semantic_names_border_bottom(self):
        db = self._make_db_with_win_image("win_g_1.png")
        images_dir = self._extract(db, semantic=True)
        self.assertTrue((images_dir / "border_bottom_uns.png").exists())


if __name__ == "__main__":
    unittest.main()
