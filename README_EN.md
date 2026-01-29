# The Maze Narrative Engine

> "Don't write stories. Construct Traps."

An autonomous fiction generation engine based on Trap-Based Narrative Theory, built for Claude Code.

[中文版](README.md) | [日本語版](README_JA.md)

## Overview

The Maze Narrative Engine is a specialized Claude Skill that implements the **3-Gate Protocol** for automated short story generation. It follows the core principle of trap-based storytelling: every story element before the 90% mark must secretly serve the inevitable ending.

## Installation

```bash
# Clone the repository
git clone git@github.com:lucy-cl/maze-narrative-skill.git
cd maze-narrative-skill

# Install dependencies
pip install -e .
```

## Usage

### 1. Generate a New Story

```bash
# Basic generation
maze generate --theme "电竞逆袭" --constraints "NO AI"

# Specify formula
maze generate --theme "甜宠爱情" --formula sweet --output ./stories

# With constraints
maze generate --theme "复仇爽文" --constraints "NO AI, NO 虐恋" --output ./output
```

### 2. Audit an Existing Draft

```bash
# Full audit (all gates)
maze audit --file ./draft.txt

# Specific gate
maze audit --file ./draft.txt --gate quality

# Output to specific directory
maze audit --file ./draft.txt --output ./reports
```

### 3. Use as a Python Module

```python
from maze.pipeline import Pipeline
from pathlib import Path

pipeline = Pipeline(
    theme="Your theme",
    constraints="Your constraints",
    formula="cool",  # cool/sweet/regret/esports/auto
    output_dir=Path("./output"),
)

result = pipeline.run()
if result.success:
    print(f"Story created: {result.final_path}")
```

## The 3-Gate Protocol

| Gate | Name | Purpose |
|------|------|---------|
| 1 | Idea | Theme validation, formula selection, constraint checking |
| 2 | Quality | Lexicon density, format compliance, foreshadowing placement |
| 3 | Safety | Platform compliance, psychological safety, prohibited content |

## Story Structure

```
0-15%   Bait (诱饵)      - Establish high-value expectation
15-90%  Trap (陷阱)      - Accumulate expectation gap
90-100% Trigger (触发)   - Inevitable release, no explanation
```

## Formula Templates

| Formula | Description | Structure |
|---------|-------------|-----------|
| `formula_cool` | Satisfying Story | Setup → Suppression → Counterattack → Dominance |
| `formula_sweet` | Sweet Romance | Lock Meme → Sweet Scenes → Emotional Confirmation |
| `formula_regret` | Bittersweet | Regret → Redemption → Lingering Aftertaste |
| `formula_esports` | Esports Victory | Doubt → Pressure → Turning Point → Triumph |

## Project Structure

```
maze-narrative-skill/
├── skills/                # Claude Code Skills (official standard)
│   └── maze-engine/
│       └── SKILL.md       # Primary skill definition
├── CLAUDE.md              # Legacy reference (backward compatibility)
├── README.md              # Chinese documentation
├── README_EN.md           # English documentation
├── README_JA.md           # Japanese documentation
├── pyproject.toml         # Package config
├── maze/                  # Core Python package
│   ├── __init__.py
│   ├── core.py            # CLI entry point
│   ├── pipeline.py        # Pipeline orchestrator
│   ├── gates/             # 3-Gate implementations
│   │   ├── idea.py
│   │   ├── quality.py
│   │   └── safety.py
│   └── library/           # Resource loader
│       └── loader.py
├── library/               # Static resources
│   ├── baits.json         # Formula templates
│   ├── lexicon.json       # Vocabulary database
│   └── materials.json     # Narrative materials
└── tests/                 # Unit tests
```

## Integrating with Claude Code

1. Copy the entire `skills/maze-engine/` folder to your Claude Code project
2. Or copy `CLAUDE.md` to your project root (legacy method)
3. Run `claude` in the project directory
4. The skill will be automatically loaded via the `skills/` directory

## Test Matrix

| Scenario Type | Example User Command | Expected Behavior |
| --- | --- | --- |
| **Normal Operation** | "Generate a Cyberpunk Revenge story using Maze Engine." | Activates Skill, calls `maze-generate`, generates story |
| **Edge Case** | "Write a story but don't follow any structure." | Activates Skill but warns user that Maze Engine enforces 3-Gate Protocol, asks to proceed |
| **Out of Scope** | "Help me write a Python script for web scraping." | Does NOT activate Skill (blocked by `NOT FOR` in System Prompt) |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAZE_OUTPUT_DIR` | Default output directory | `./output` |
| `MAZE_SILENT_MODE` | Suppress console output | `true` |

### Constraints

Common user constraints:
- `NO AI` - Exclude AI-related content
- `NO 虐恋` - No bittersweet romance
- `NO 政治` - No political content
- `甜宠` - Sweet romance focus

## Development

```bash
# Run tests
pytest

# Format code
black maze/ tests/

# Lint
ruff check maze/ tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Built on the principles of Trap-Based Narrative Theory from [The Maze Project](https://github.com/lucy-cl/the-maze-project).
