"""Gate 3: Safety Review and Compliance."""

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


class SafetyGate:
    """Gate 3: Safety compliance and content review."""

    name = "Gate 3 - Safety (安全风控)"

    # Prohibited content categories
    PROHIBITED_CATEGORIES = {
        "extreme_violence": [
            "分尸", "肢解", "凌迟", "虐杀", "烹煮", "生吃",
        ],
        "minors_involved": [
            "幼女", "幼男", "未成年人", "初中生", "小学生",
        ],
        "non_consent": [
            "迷奸", "轮奸", "强迫", "下药",
        ],
        "platform_restricted": [
            "中国", "领导人", "政治", "敏感",
        ],
    }

    # Psychological safety warnings
    PSYCHOLOGICAL_WARNINGS = [
        "自杀", "自残", "安乐死", "抑郁症", "精神病",
    ]

    def __init__(self, loader: ResourceLoader) -> None:
        self.loader = loader

    def review(self, content: str) -> GateResult:
        """Review content for safety compliance."""
        issues = self._scan_content(content)

        if not issues:
            return GateResult(passed=True, content=content)

        # Return content with safety revisions applied (simplified)
        return GateResult(passed=False, content=content, issues=issues)

    def audit(self, content: str, path: Path) -> GateResult:
        """Audit content for safety issues."""
        issues = self._scan_content(content)

        return GateResult(
            passed=len(issues) == 0,
            issues=issues,
        )

    def _scan_content(self, content: str) -> list[str]:
        """Scan content for prohibited categories."""
        issues = []

        # Check prohibited categories
        for category, keywords in self.PROHIBITED_CATEGORIES.items():
            for keyword in keywords:
                if keyword in content:
                    issues.append(f"Prohibited content ({category}): {keyword}")

        # Check psychological safety
        warnings = []
        for keyword in self.PSYCHOLOGICAL_WARNINGS:
            if keyword in content:
                warnings.append(keyword)

        if warnings:
            issues.append(f"Psychological safety warnings: {', '.join(warnings)}")

        # Check for AI-related content (as specified in constraints)
        ai_keywords = ["AI", "人工智能", "大模型", "ChatGPT", "Claude"]
        for keyword in ai_keywords:
            if keyword in content:
                issues.append(f"AI-related content: {keyword}")

        return issues
