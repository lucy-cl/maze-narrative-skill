"""Resource loader for narrative materials."""

import json
from pathlib import Path
from typing import Any


class ResourceLoader:
    """Loads and provides access to narrative resources."""

    def __init__(self, library_path: Path | None = None) -> None:
        self.library_path = library_path or Path(__file__).parent.parent.parent / "library"
        self._baits: dict[str, Any] | None = None
        self._lexicon: dict[str, list[str]] | None = None
        self._materials: dict[str, Any] | None = None

    @property
    def baits(self) -> dict[str, Any]:
        """Load and cache formula templates."""
        if self._baits is None:
            self._baits = self._load_json("baits.json")
        return self._baits

    @property
    def lexicon(self) -> dict[str, list[str]]:
        """Load and cache lexicon entries."""
        if self._lexicon is None:
            self._lexicon = self._load_json("lexicon.json")
        return self._lexicon

    @property
    def materials(self) -> dict[str, Any]:
        """Load and cache narrative materials."""
        if self._materials is None:
            self._materials = self._load_json("materials.json")
        return self._materials

    def _load_json(self, filename: str) -> dict[str, Any]:
        """Load a JSON resource file."""
        path = self.library_path / filename
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def get_lexicon_words(self, category: str) -> list[str]:
        """Get words from a specific lexicon category."""
        return self.lexicon.get(category, [])

    def get_formula(self, name: str) -> dict[str, Any]:
        """Get a formula template by name."""
        return self.baits.get(name, {})

    def get_random_materials(self, count: int = 3) -> list[str]:
        """Get random materials for injection into SPEC."""
        materials = self.materials.get("lock_memes", [])
        import random
        return random.sample(materials, min(count, len(materials)))
