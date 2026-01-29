# 迷宫叙事引擎

> "不要写故事。要设陷阱。"

基于陷阱叙事理论的自动化小说生成引擎，专为 Claude Code 设计。

[English](README_EN.md) | [日本語](README_JA.md)

## 简介

迷宫叙事引擎是一个专业的 Claude Skill，实现了**三门协议**用于自动化短篇小说生成。它遵循陷阱叙事故事的核心原则：90% 之前的每个故事元素都必须秘密地为不可避免的结局服务。

## 安装

```bash
# 克隆仓库
git clone git@github.com:lucy-cl/maze-narrative-skill.git
cd maze-narrative-skill

# 安装依赖
pip install -e .
```

## 使用方法

### 1. 生成新故事

```bash
# 基础生成
maze generate --theme "电竞逆袭" --constraints "NO AI"

# 指定公式
maze generate --theme "甜宠爱情" --formula sweet --output ./stories

# 带约束条件
maze generate --theme "复仇爽文" --constraints "NO AI, NO 虐恋" --output ./output
```

### 2. 审计现有草稿

```bash
# 完整审计（所有门）
maze audit --file ./draft.txt

# 指定门
maze audit --file ./draft.txt --gate quality

# 输出到指定目录
maze audit --file ./draft.txt --output ./reports
```

### 3. 作为 Python 模块使用

```python
from maze.pipeline import Pipeline
from pathlib import Path

pipeline = Pipeline(
    theme="你的主题",
    constraints="约束条件",
    formula="cool",  # cool/sweet/regret/esports/auto
    output_dir=Path("./output"),
)

result = pipeline.run()
if result.success:
    print(f"故事已创建: {result.final_path}")
```

## 三门协议

| 门 | 名称 | 用途 |
|----|------|------|
| 1 | 创意门 | 主题验证、公式选择、约束检查 |
| 2 | 质量门 | 词汇密度、格式合规、前瞻性放置 |
| 3 | 安全门 | 平台合规、心理安全、禁止内容 |

## 故事结构

```
0-15%   诱饵(Bait)      - 建立高价值预期
15-90%  陷阱(Trap)      - 积累预期差距
90-100% 触发器(Trigger) - 必然释放，无需解释
```

## 公式模板

| 公式 | 中文名称 | 结构 |
|------|----------|------|
| `formula_cool` | 爽文公式 | 铺垫 → 压制 → 反击 → 主导 |
| `formula_sweet` | 甜文公式 | 锁定 Meme → 甜蜜场景 → 情感确认 |
| `formula_regret` | 虐文公式 | 遗憾 → 救赎 → 余韵 |
| `formula_esports` | 电竞公式 | 质疑 → 压力 → 转折 → 胜利 |

## 项目结构

```
maze-narrative-skill/
├── skills/                # Claude Code Skills（官方标准）
│   └── maze-engine/
│       └── SKILL.md       # 主要技能定义
├── CLAUDE.md              # 遗留参考（后向兼容）
├── README.md              # 中文文档
├── README_EN.md           # 英文文档
├── README_JA.md           # 日文文档
├── pyproject.toml         # 包配置
├── maze/                  # 核心 Python 包
│   ├── __init__.py
│   ├── core.py            # CLI 入口点
│   ├── pipeline.py        # 管道编排器
│   ├── gates/             # 三门协议实现
│   │   ├── idea.py
│   │   ├── quality.py
│   │   └── safety.py
│   └── library/           # 资源加载器
│       └── loader.py
├── library/               # 静态资源
│   ├── baits.json         # 公式模板
│   ├── lexicon.json       # 词汇数据库
│   └── materials.json     # 叙事素材
└── tests/                 # 单元测试
```

## 与 Claude Code 集成

1. 将整个 `skills/maze-engine/` 文件夹复制到你的 Claude Code 项目
2. 或将 `CLAUDE.md` 复制到项目根目录（遗留方式）
3. 在项目目录中运行 `claude`
4. 技能将通过 `skills/` 目录自动加载

## 测试矩阵

| 场景类型 | 示例命令 | 预期行为 |
|----------|----------|----------|
| **正常操作** | "使用 Maze Engine 生成一个赛博朋克复仇故事" | 激活技能，调用 `maze-generate`，生成故事 |
| **边缘情况** | "写一个故事但不遵循任何结构" | 激活技能但警告用户 Maze Engine 强制三门协议，询问是否继续 |
| **范围外** | "帮我写一个网页爬虫的 Python 脚本" | 不激活技能（被系统提示中的 `NOT FOR` 阻止） |

## 配置

### 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `MAZE_OUTPUT_DIR` | 默认输出目录 | `./output` |
| `MAZE_SILENT_MODE` | 抑制控制台输出 | `true` |

### 约束条件

常用用户约束：
- `NO AI` - 排除 AI 相关内容
- `NO 虐恋` - 无虐心恋情
- `NO 政治` - 无政治内容
- `甜宠` - 甜宠恋爱向

## 开发

```bash
# 运行测试
pytest

# 格式化代码
black maze/ tests/

# 代码检查
ruff check maze/ tests/
```

## 开源协议

MIT License - 详见 [LICENSE](LICENSE)。

## 致谢

基于 [The Maze Project](https://github.com/lucy-cl/the-maze-project) 的陷阱叙事理论原则构建。
