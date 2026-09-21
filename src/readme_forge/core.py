from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ForgeError(ValueError):
    """Raised for invalid project input or unsafe output requests."""


@dataclass(frozen=True)
class ProjectInfo:
    name: str
    description: str
    language: str
    install: str
    run: str
    test: str
    license_name: str = "MIT"


def _clean(value: Any, default: str = "") -> str:
    text = str(value or default).strip()
    return re.sub(r"[\r\n]+", " ", text)


def _from_pyproject(path: Path) -> ProjectInfo:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    name = _clean(project.get("name"), path.parent.name)
    desc = _clean(project.get("description"), f"{name} project")
    scripts = project.get("scripts", {})
    command = next(iter(scripts), f"python -m {name.replace('-', '_')}")
    return ProjectInfo(name, desc, "Python", "python -m pip install -e .", command, "python -m pytest")


def _from_package_json(path: Path) -> ProjectInfo:
    data = json.loads(path.read_text(encoding="utf-8"))
    name = _clean(data.get("name"), path.parent.name)
    desc = _clean(data.get("description"), f"{name} project")
    scripts = data.get("scripts", {})
    run = "npm start" if "start" in scripts else ("npm run dev" if "dev" in scripts else "npm run")
    test = "npm test" if "test" in scripts else "npm run test"
    return ProjectInfo(name, desc, "JavaScript/TypeScript", "npm install", run, test, _clean(data.get("license"), "MIT"))


def inspect_project(root: str | Path) -> ProjectInfo:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ForgeError(f"Project directory does not exist: {root}")
    if (root / "pyproject.toml").is_file():
        return _from_pyproject(root / "pyproject.toml")
    if (root / "package.json").is_file():
        return _from_package_json(root / "package.json")
    name = root.name or "project"
    return ProjectInfo(name, f"{name} project", "Unknown", "Add installation instructions here.", "Add usage instructions here.", "Add test instructions here.")


def render(info: ProjectInfo, *, bilingual: bool = False, author: str = "") -> str:
    title = info.name.replace("-", " ").replace("_", " ").title()
    author_line = f"\n## Author\n\n{author}\n" if author else ""
    english = f"""# {title}

{info.description}

## Features

- Clear, local-first project documentation.
- Reproducible installation and usage guidance.
- Structure ready for extension as the project evolves.

## Requirements

- Runtime/toolchain: {info.language}

## Installation

```bash
{info.install}
```

## Usage

```bash
{info.run}
```

## Testing

```bash
{info.test}
```

## Security & Privacy

Review configuration and generated artifacts before publishing. Never commit credentials, tokens, private keys, or personal data.

## Limitations

This README is generated from discoverable local metadata. Project-specific architecture, screenshots, deployment details, and domain constraints should be added when applicable.

## Contributing

Keep changes focused, add tests for behavior changes, and document user-visible changes.

## License

{info.license_name} unless the repository states otherwise.
{author_line}"""
    if not bilingual:
        return english.rstrip() + "\n"
    arabic = f"""
---

# العربية

## {title}

{info.description}

## المزايا

- توثيق واضح يعتمد على بيانات المشروع المحلية.
- تعليمات قابلة لإعادة الاستخدام للتثبيت والتشغيل والاختبار.
- بنية سهلة التوسعة مع تطور المشروع.

## المتطلبات

- بيئة التشغيل/الأدوات: {info.language}

## التثبيت

```bash
{info.install}
```

## الاستخدام

```bash
{info.run}
```

## الاختبارات

```bash
{info.test}
```

## الأمان والخصوصية

راجع الإعدادات والملفات المولدة قبل النشر، ولا ترفع كلمات المرور أو الرموز السرية أو المفاتيح الخاصة أو البيانات الشخصية.

## القيود

يعتمد التوليد على البيانات المحلية التي يمكن اكتشافها تلقائيًا؛ لذلك يجب إضافة تفاصيل المعمارية والصور والنشر والقيود الخاصة بالمشروع عند الحاجة.

## المساهمة

اجعل التغييرات محددة، وأضف اختبارات عند تغيير السلوك، ووثّق التغييرات الظاهرة للمستخدم.

## الترخيص

{info.license_name} ما لم يذكر المستودع خلاف ذلك.
"""
    if author:
        arabic += f"\n## المؤلف\n\n{author}\n"
    return english.rstrip() + "\n" + arabic.rstrip() + "\n"


def generate(root: str | Path, output: str | Path, *, bilingual: bool = False, author: str = "", force: bool = False) -> Path:
    root = Path(root).expanduser().resolve()
    output = Path(output)
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    if output.exists() and not force:
        raise ForgeError(f"Refusing to overwrite existing file: {output}. Use --force to replace it.")
    if root not in output.parents and output != root:
        raise ForgeError("Output must stay inside the project directory.")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(inspect_project(root), bilingual=bilingual, author=author), encoding="utf-8")
    return output
