"""Tests for the Maze Narrative Engine."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from maze.gates.idea import IdeaGate, GateResult
from maze.gates.quality import QualityGate
from maze.gates.safety import SafetyGate
from maze.library.loader import ResourceLoader


@pytest.fixture
def loader(tmp_path) -> ResourceLoader:
    """Create a resource loader with test data."""
    # Create temporary library structure
    library_dir = tmp_path / "library"
    library_dir.mkdir()

    # Create test baits.json
    baits = {
        "formula_cool": {
            "name": "Power Fantasy",
            "stages": [{"name": "setup"}]
        },
        "formula_sweet": {
            "name": "Romance",
            "stages": []
        }
    }
    (library_dir / "baits.json").write_text(__import__("json").dumps(baits))

    # Create test lexicon.json
    lexicon = {
        "industrial_cool": ["降维", "碾压"],
        "emotional_sweet": ["心跳", "悸动"]
    }
    (library_dir / "lexicon.json").write_text(__import__("json").dumps(lexicon))

    # Create test materials.json
    materials = {
        "lock_memes": [
            {"id": "lm_001", "content": "那把伞"},
        ],
        "trigger_templates": {
            "cool": ["所有人才意识到"]
        }
    }
    (library_dir / "materials.json").write_text(__import__("json").dumps(materials))

    return ResourceLoader(library_path=library_dir)


class TestIdeaGate:
    """Tests for IdeaGate."""

    def test_generate_spec(self, loader):
        """Test SPEC generation from theme."""
        gate = IdeaGate(loader)
        result = gate.generate("Cyberpunk Revenge", "NO AI", "formula_cool")

        assert result.passed is True
        assert "theme" in result.content
        assert "Cyberpunk Revenge" in result.content

    def test_constraint_validation(self, loader):
        """Test that prohibited constraints are caught."""
        gate = IdeaGate(loader)
        result = gate.generate("Test", "NO AI", "formula_cool")

        # Should pass - NO AI is allowed
        assert result.passed is True

    def test_auto_formula_selection(self, loader):
        """Test automatic formula selection."""
        gate = IdeaGate(loader)

        # Sweet theme
        result = gate.generate("甜宠故事", "", "auto")
        assert "formula_sweet" in result.content

        # Default to cool
        result = gate.generate("Action story", "", "auto")
        assert "formula_cool" in result.content

    def test_audit_valid_spec(self, loader):
        """Test auditing a valid SPEC."""
        import json
        spec = {"theme": "Test", "formula": "formula_cool", "formula_stages": []}

        gate = IdeaGate(loader)
        result = gate.audit(json.dumps(spec), Path("test.json"))

        assert result.passed is True

    def test_audit_missing_fields(self, loader):
        """Test auditing a SPEC with missing fields."""
        gate = IdeaGate(loader)
        result = gate.audit("{}", Path("test.json"))

        assert result.passed is False
        assert len(result.issues) > 0


class TestQualityGate:
    """Tests for QualityGate."""

    def test_format_validation(self, loader):
        """Test that forbidden formats are caught."""
        gate = QualityGate(loader)

        # Test Markdown headers
        content = "# Chapter 1\n正文"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is False

        # Test chapter markers
        content = "第一章 开始"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is False

    def test_lexicon_density(self, loader):
        """Test lexicon density checking."""
        gate = QualityGate(loader)

        # Low density - should fail
        content = "这是一个简单的测试内容没有任何高级词汇"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is False

        # High density - should pass
        content = "降维打击让对手感到碾压式的窒息"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is True

    def test_explanatory_language(self, loader):
        """Test that explanatory phrases are caught."""
        gate = QualityGate(loader)

        content = "因为他很强，所以赢了"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is False


class TestSafetyGate:
    """Tests for SafetyGate."""

    def test_prohibited_content(self, loader):
        """Test that prohibited content is caught."""
        gate = SafetyGate(loader)

        content = "这是一些极端暴力内容"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is False

    def test_ai_content_blocked(self, loader):
        """Test that AI-related content is blocked."""
        gate = SafetyGate(loader)

        content = "这是一个AI生成的故事"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is False

    def test_clean_content_passes(self, loader):
        """Test that clean content passes."""
        gate = SafetyGate(loader)

        content = "这是一个正常的故事内容"
        result = gate.audit(content, Path("test.txt"))
        assert result.passed is True


class TestResourceLoader:
    """Tests for ResourceLoader."""

    def test_load_baits(self, loader):
        """Test loading bait formulas."""
        baits = loader.baits
        assert "formula_cool" in baits

    def test_load_lexicon(self, loader):
        """Test loading lexicon."""
        lexicon = loader.lexicon
        assert "industrial_cool" in lexicon

    def test_get_formula(self, loader):
        """Test getting a specific formula."""
        formula = loader.get_formula("formula_cool")
        assert formula["name"] == "Power Fantasy"

    def test_get_random_materials(self, loader):
        """Test getting random materials."""
        materials = loader.get_random_materials(1)
        assert len(materials) == 1
