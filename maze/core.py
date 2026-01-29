"""CLI entry point for the Maze Narrative Engine."""

import argparse
import sys
from pathlib import Path

from .pipeline import Pipeline
from .gates import IdeaGate, QualityGate, SafetyGate


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for CLI commands."""
    parser = argparse.ArgumentParser(
        prog="maze",
        description="The Maze Narrative Engine - Trap-Based Story Generator",
        epilog="Use 'maze generate --help' or 'maze audit --help' for more info.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a new story")
    generate_parser.add_argument(
        "--theme", "-t", required=True, help="Story theme or concept"
    )
    generate_parser.add_argument(
        "--constraints", "-c", default="", help="User constraints (e.g., 'NO AI')"
    )
    generate_parser.add_argument(
        "--output", "-o", default="./output", help="Output directory for story files"
    )
    generate_parser.add_argument(
        "--formula", "-f", default="auto", help="Formula to use (cool/sweet/regret/auto)"
    )

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Audit an existing draft")
    audit_parser.add_argument(
        "--file", "-f", required=True, help="Path to draft file or directory"
    )
    audit_parser.add_argument(
        "--gate", "-g", default="all", choices=["idea", "quality", "safety", "all"],
        help="Which gate to audit (default: all)"
    )
    audit_parser.add_argument(
        "--output", "-o", default="./audit_reports", help="Output directory for audit reports"
    )

    return parser


def run_generate(args: argparse.Namespace) -> int:
    """Execute the story generation pipeline."""
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    pipeline = Pipeline(
        theme=args.theme,
        constraints=args.constraints,
        formula=args.formula,
        output_dir=output_dir,
    )

    try:
        result = pipeline.run()
        if result.success:
            print(f"[OK] Story generated: {result.output_path}")
            return 0
        else:
            print(f"[FAIL] Generation failed: {result.error}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


def run_audit(args: argparse.Namespace) -> int:
    """Execute the audit process."""
    from .library.loader import ResourceLoader

    target = Path(args.file)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    loader = ResourceLoader()
    report_path = output_dir / "Audit_Report.md"

    gates_to_run = []
    if args.gate in ("idea", "all"):
        gates_to_run.append(IdeaGate(loader))
    if args.gate in ("quality", "all"):
        gates_to_run.append(QualityGate(loader))
    if args.gate in ("safety", "all"):
        gates_to_run.append(SafetyGate(loader))

    if not target.is_file():
        print(f"[ERROR] File not found: {target}", file=sys.stderr)
        return 1

    content = target.read_text(encoding="utf-8")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Audit Report: {target.name}\n\n")
        f.write(f"**Date**: {__import__('datetime').datetime.now().isoformat()}\n")
        f.write(f"**Gate**: {args.gate}\n\n---\n\n")

        for gate in gates_to_run:
            result = gate.audit(content, target)
            f.write(f"## {gate.name}\n\n")
            f.write(f"**Status**: {'PASS' if result.passed else 'FAIL'}\n\n")
            if result.issues:
                f.write("**Issues**:\n")
                for issue in result.issues:
                    f.write(f"- {issue}\n")
            f.write("\n")

    print(f"[OK] Audit report: {report_path}")
    return 0


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "generate":
        return run_generate(args)
    elif args.command == "audit":
        return run_audit(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
