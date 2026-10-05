"""resume-polish-lite 命令行入口。

用法示例：
    python3 cli.py --line "负责用户后台系统，做了权限模块，性能提升了30%"
    python3 cli.py --file experience.txt --llm
"""

from __future__ import annotations

import argparse
import sys

from resume_polish import polish


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="resume-polish-lite",
        description="把大白话经历改写为动作动词+量化结果的简历 bullet（可选 LLM）",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--line", help="单条经历")
    src.add_argument("--file", help="从文件读取经历（每行一条）")
    p.add_argument("--llm", action="store_true", help="启用 LLM 润色（需 OPENAI_API_KEY）")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            lines = [ln for ln in f.read().splitlines() if ln.strip()]
    else:
        lines = [args.line]

    bullets = polish(lines, use_llm=args.llm)
    for b in bullets:
        print(f"• {b}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
