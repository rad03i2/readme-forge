from pathlib import Path

from readme_forge.cli import main


def test_cli_inspect(tmp_path: Path, capsys):
    assert main([str(tmp_path), "--inspect"]) == 0
    assert '"name"' in capsys.readouterr().out


def test_cli_stdout(tmp_path: Path, capsys):
    assert main([str(tmp_path), "--stdout", "--bilingual"]) == 0
    output = capsys.readouterr().out
    assert "# العربية" in output


def test_cli_existing_output_returns_error(tmp_path: Path, capsys):
    (tmp_path / "README.generated.md").write_text("existing", encoding="utf-8")
    assert main([str(tmp_path)]) == 2
    assert "Refusing to overwrite" in capsys.readouterr().err
