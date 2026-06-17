#!/usr/bin/env python3
"""
Semantic name translator for E13 legacy pixmap filenames.

Loads asset_map.json from the repository root and translates legacy win_*
filenames (e.g. win_a_1.ppm, win_l_3.png) to their semantic counterparts
(e.g. button_iconify_uns.png, button_close_clk.png).
"""

import json
import re
from pathlib import Path
from typing import Optional


# Locate asset_map.json relative to this file (tools/ → repo root)
_DEFAULT_MAP_PATH = Path(__file__).parent.parent / "asset_map.json"

# Pattern that matches legacy win_* filenames: win_<letter(s)>_<state>.<ext>
_LEGACY_RE = re.compile(
    r"^(?P<stem>win_[a-z]+)_(?P<state>[123])(?P<ext>\.[a-zA-Z]+)$"
)


class SemanticNamer:
    """Translates legacy E13 win_* pixmap names to semantic role names."""

    def __init__(self, map_path: Optional[Path] = None):
        """
        Initialise the namer.

        Args:
            map_path: Path to asset_map.json.  Defaults to the repo-root copy.
        """
        if map_path is None:
            map_path = _DEFAULT_MAP_PATH
        self._map_path = Path(map_path)
        self._asset_map: dict = {}
        self._state_map: dict = {}
        self._load()

    def _load(self) -> None:
        """Load and parse asset_map.json."""
        with open(self._map_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._state_map = data.get("state_map", {"1": "uns", "2": "sel", "3": "clk"})
        self._asset_map = data.get("assets", {})

    def translate(self, legacy_name: str) -> Optional[str]:
        """
        Translate a legacy win_* filename to its semantic equivalent.

        The input may be a bare filename such as ``win_a_1.ppm`` or a path
        component; only the final filename portion is inspected.

        Args:
            legacy_name: Legacy pixmap filename (e.g. ``win_l_3.ppm``).

        Returns:
            Semantic filename (e.g. ``button_close_clk.png``), or ``None``
            if the name does not match the legacy pattern or has no mapping.
        """
        name = Path(legacy_name).name
        m = _LEGACY_RE.match(name)
        if not m:
            return None

        stem = m.group("stem")   # e.g. "win_a"
        state = m.group("state")  # "1", "2", or "3"
        ext = m.group("ext")     # e.g. ".ppm" or ".png"

        role_entry = self._asset_map.get(stem)
        if role_entry is None:
            return None

        semantic_role = role_entry.get("semantic_role")
        if not semantic_role:
            return None

        state_tag = self._state_map.get(state, "uns")
        return f"{semantic_role}_{state_tag}{ext}"

    def translate_path(self, legacy_path: Path) -> Optional[Path]:
        """
        Translate a full path whose filename is a legacy win_* name.

        The directory portion is preserved; only the filename is changed.

        Args:
            legacy_path: Path ending in a legacy win_* filename.

        Returns:
            New path with semantic filename, or ``None`` if untranslatable.
        """
        semantic_name = self.translate(legacy_path.name)
        if semantic_name is None:
            return None
        return legacy_path.parent / semantic_name

    def get_semantic_role(self, stem: str) -> Optional[str]:
        """
        Return the semantic role for a win_* stem (e.g. ``"win_a"``).

        Args:
            stem: The win_* stem without state/extension.

        Returns:
            Semantic role string, or ``None`` if not found.
        """
        entry = self._asset_map.get(stem)
        if entry is None:
            return None
        return entry.get("semantic_role")

    def list_stems(self) -> list:
        """Return all known win_* stems in sorted order."""
        return sorted(self._asset_map.keys())
