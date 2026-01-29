"""Gate 2: Quality Control and Format Validation."""

import re
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


class QualityGate:
    """Gate 2: Quality control and format validation."""

    name = "Gate 2 - Quality (质量检测)"

    # Minimum lexicon density threshold
    MIN_LEXICON_DENSITY = 0.005  # 0.5%

    # Forbidden patterns
    FORBIDDEN_PATTERNS = [
        (r"^#{1,6}\s+", "Markdown headers"),
        (r"第[一二三四五六七八九十百千]+章", "Chapter markers"),
        (r"第[一二三四五六七八九十百千]+节", "Section markers"),
        (r"\d+%\s*$", "Progress markers"),
        (r"^\s*\[\d+\]\s+", "Reference markers"),
    ]

    # Required at 90% - no explanatory phrases
    EXPLANATORY_PATTERNS = [
        r"因为",
        r"所以",
        r"于是",
        r"原来",
        r"事实上",
        r"真相是",
        r"其实",
        r"也就是说",
    ]

    def __init__(self, loader: ResourceLoader) -> None:
        self.loader = loader

    def generate(self, spec_content: str) -> GateResult:
        """Generate a draft from SPEC (simplified - would call LLM in production)."""
        issues = []

        # In production, this would call an LLM to generate the story
        # For now, return a placeholder
        draft = f"""这是一个根据规格生成的草稿模板。

[此处应根据 spec_content 中的 formula_stages 生成完整故事]

当前公式: {spec_content}
"""

        return GateResult(passed=True, content=draft, issues=[])

    def audit(self, content: str, path: Path) -> GateResult:
        """Audit a draft for quality and format compliance."""
        issues = []

        # Check format violations
        for pattern, description in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, content, re.MULTILINE):
                issues.append(f"Contains forbidden pattern: {description}")

        # Check lexicon density
        lexicon_words = set()
        for category in self.loader.lexicon.values():
            lexicon_words.update(category)

        words = set(re.findall(r"[\u4e00-\u9fff]+", content))
        if words:
            matched = words & lexicon_words
            density = len(matched) / len(words)
            if density < self.MIN_LEXICON_DENSITY:
                issues.append(
                    f"Lexicon density too low: {density:.2%} "
                    f"(minimum: {self.MIN_LEXICON_DENSITY:.1%})"
                )

        # Check for explanatory language in final section
        # (In production, would check last 10% only)
        for pattern in self.EXPLANATORY_PATTERNS:
            if re.search(pattern, content):
                issues.append(f"Explanatory language found: '{pattern}'")

        return GateResult(
            passed=len(issues) == 0,
            issues=issues,
        )
