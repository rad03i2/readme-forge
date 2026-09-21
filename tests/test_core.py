import json
from pathlib import Path

import pytest

from readme_forge.core import ForgeError, generate, inspect_project, render


def test_inspect_pyproject(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text('[project]\nname="hello-tool"\ndescription="Useful tool"\n[project.scripts]\nhello="hello:main"\n', encoding="utf-8")
    info = inspect_project(tmp_path)
    assert info.name == "hello-tool"
    assert info.language == "Python"
    assert info.run == "hello"


def test_inspect_package_json(tmp_path: Path):
    (tmp_path / "package.json").write_text(json.dumps({"name":"web-kit","description":"Web helper","scripts":{"dev":"vite","test":"vitest"},"license":"MIT"}), encoding="utf-8")
    info = inspect_project(tmp_path)
    assert info.language == "JavaScript/TypeScript"
    assert info.run == "npm run dev"


def test_bilingual_render_contains_author(tmp_path: Path):
    info = inspect_project(tmp_path)
    text = render(info, bilingual=True, author="Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2")
    assert "# العربية" in text
    assert "## Author" in text
    assert "## المؤلف" in text


def test_generate_refuses_overwrite(tmp_path: Path):
    target = tmp_path / "README.generated.md"
    target.write_text("keep", encoding="utf-8")
    with pytest.raises(ForgeError):
        generate(tmp_path, target)
    assert target.read_text(encoding="utf-8") == "keep"


def test_generate_force_writes_inside_project(tmp_path: Path):
    target = generate(tmp_path, "docs/README.md", force=True)
    assert target.is_file()
    assert target.parent.name == "docs"


def test_generate_rejects_escape(tmp_path: Path):
    with pytest.raises(ForgeError):
        generate(tmp_path, "../outside.md")
