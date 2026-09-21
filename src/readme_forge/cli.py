from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from .core import ForgeError, generate, inspect_project, render


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="readme-forge", description="Generate README drafts from local project metadata.")
    p.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory)")
    p.add_argument("--output", default="README.generated.md", help="Output path inside the project")
    p.add_argument("--bilingual", action="store_true", help="Generate English and Arabic sections")
    p.add_argument("--author", default="", help="Author text to include")
    p.add_argument("--force", action="store_true", help="Replace an existing output file")
    p.add_argument("--stdout", action="store_true", help="Print Markdown instead of writing a file")
    p.add_argument("--inspect", action="store_true", help="Print discovered metadata as JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        info = inspect_project(args.project)
        if args.inspect:
            print(json.dumps(asdict(info), ensure_ascii=False, indent=2))
            return 0
        if args.stdout:
            sys.stdout.write(render(info, bilingual=args.bilingual, author=args.author))
            return 0
        path = generate(args.project, args.output, bilingual=args.bilingual, author=args.author, force=args.force)
        print(f"Generated {path}")
        return 0
    except (ForgeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
