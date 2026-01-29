"""Gate 1: Idea Generation and Validation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..library.loader import ResourceLoader


@dataclass
class GateResult:
    """Result of a gate operation."""
    passed: bool
    content: str = ""
    issues: list[str] = None

    def __post_init__(self) -> None:
        if self.issues is None:
            self.issues = []


class IdeaGate:
    """Gate 1: Creative idea audit and SPEC generation."""

    name = "Gate 1 - Idea (创意核审)"

    def __init__(self, loader: ResourceLoader) -> None:
        self.loader = loader

    def generate(
        self,
        theme: str,
        constraints: str,
        formula: str = "auto",
    ) -> GateResult:
        """Generate a story SPEC based on theme and constraints."""
        issues = []

        # Validate constraints
        prohibited = ["AI", "人工智能", "大模型", "ChatGPT", "Claude"]
        for word in prohibited:
            if word.lower() in constraints.lower():
                issues.append(f"Prohibited keyword in constraints: {word}")

        # Select formula
        if formula == "auto":
            formula = self._select_formula(theme)
        elif formula not in self.loader.baits:
            issues.append(f"Unknown formula: {formula}")
            formula = "formula_cool"

        formula_data = self.loader.get_formula(formula)

        # Get random materials for injection
        materials = self.loader.get_random_materials(3)

        # Generate SPEC (simplified - in production, would call LLM)
        spec = {
            "theme": theme,
            "constraints": constraints,
            "formula": formula,
            "formula_stages": formula_data.get("stages", []),
            "injected_materials": materials,
            "triggers": self.loader.materials.get("trigger_templates", {}).get(
                formula.replace("formula_", ""), []
            ),
        }

        import json
        content = json.dumps(spec, ensure_ascii=False, indent=2)

        return GateResult(
            passed=len(issues) == 0,
            content=content,
            issues=issues,
        )

    def audit(self, content: str, path: Path) -> GateResult:
        """Audit an existing SPEC or idea document."""
        issues = []

        # Check for prohibited content
        prohibited = ["AI", "人工智能", "大模型"]
        for word in prohibited:
            if word in content:
                issues.append(f"Contains prohibited keyword: {word}")

        # Check for required sections in SPEC
        import json
        try:
            spec = json.loads(content)
            required = ["theme", "formula", "formula_stages"]
            for field in required:
                if field not in spec:
                    issues.append(f"Missing required field: {field}")
        except json.JSONDecodeError:
            issues.append("Invalid JSON format")

        return GateResult(
            passed=len(issues) == 0,
            issues=issues,
        )

    def _select_formula(self, theme: str) -> str:
        """Auto-select formula based on theme keywords."""
        theme_lower = theme.lower()

        if any(w in theme_lower for w in ["甜", "爱", "恋", "甜宠"]):
            return "formula_sweet"
        if any(w in theme_lower for w in ["悔", "遗憾", "错", "救"]):
            return "formula_regret"
        if any(w in theme_lower for w in ["电竞", "比赛", "逆", "胜"]):
            return "formula_esports"

        return "formula_cool"
