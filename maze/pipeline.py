"""Story generation pipeline orchestrator."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .gates import IdeaGate, QualityGate, SafetyGate, GateResult
from .library.loader import ResourceLoader


@dataclass
class PipelineResult:
    """Result of a pipeline execution."""
    success: bool
    output_path: Optional[Path] = None
    error: Optional[str] = None
    spec_path: Optional[Path] = None
    draft_path: Optional[Path] = None
    final_path: Optional[Path] = None


class Pipeline:
    """Orchestrates the 3-Gate story generation pipeline."""

    def __init__(
        self,
        theme: str,
        constraints: str,
        formula: str,
        output_dir: Path,
    ) -> None:
        self.theme = theme
        self.constraints = constraints
        self.formula = formula
        self.output_dir = output_dir
        self.loader = ResourceLoader()

    def run(self) -> PipelineResult:
        """Execute the full generation pipeline."""
        story_id = self._generate_story_id()

        # Gate 1: Idea Generation
        idea_gate = IdeaGate(self.loader)
        spec_result = idea_gate.generate(self.theme, self.constraints, self.formula)

        if not spec_result.passed:
            return PipelineResult(
                success=False,
                error=f"Gate 1 failed: {', '.join(spec_result.issues)}"
            )

        spec_path = self.output_dir / f"SPEC_{story_id}.json"
        spec_path.write_text(spec_result.content, encoding="utf-8")

        # Gate 2: Draft Generation & Quality Check
        quality_gate = QualityGate(self.loader)
        draft_result = quality_gate.generate(spec_result.content)

        if not draft_result.passed:
            return PipelineResult(
                success=False,
                error=f"Gate 2 failed: {', '.join(draft_result.issues)}",
                spec_path=spec_path,
            )

        draft_path = self.output_dir / f"draft_v1_{story_id}.txt"
        draft_path.write_text(draft_result.content, encoding="utf-8")

        # Gate 3: Safety Review
        safety_gate = SafetyGate(self.loader)
        final_result = safety_gate.review(draft_result.content)

        if not final_result.passed:
            return PipelineResult(
                success=False,
                error=f"Gate 3 failed: {', '.join(final_result.issues)}",
                spec_path=spec_path,
                draft_path=draft_path,
            )

        final_path = self.output_dir / f"final_trap_{story_id}.txt"
        final_path.write_text(final_result.content, encoding="utf-8")

        return PipelineResult(
            success=True,
            output_path=final_path,
            spec_path=spec_path,
            draft_path=draft_path,
            final_path=final_path,
        )

    def _generate_story_id(self) -> str:
        """Generate a unique story ID based on timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
