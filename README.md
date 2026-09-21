# README Forge

[![CI](https://github.com/rad03i2/readme-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/rad03i2/readme-forge/actions/workflows/ci.yml)

A small, local-first CLI and Python library that inspects project metadata and generates a clean README draft without sending source code or metadata to external services.

## Why it exists

Starting documentation is repetitive. README Forge turns metadata already present in `pyproject.toml` or `package.json` into a useful Markdown baseline while keeping the developer in control of the final document.

## Key features

- Detects Python projects from `pyproject.toml` and JavaScript/TypeScript projects from `package.json`.
- Falls back safely for projects without recognized metadata.
- Generates installation, usage, testing, security, limitations, contributing, and license sections.
- Optional complete English + Arabic output with `--bilingual`.
- `--inspect` JSON output for automation and `--stdout` for pipelines.
- Refuses to overwrite existing output unless `--force` is supplied.
- Rejects output paths outside the selected project directory.
- Local-only operation: no HTTP calls, telemetry, API keys, or project-script execution.
- Reusable Python API with zero runtime dependencies.

## Preview

```text
$ readme-forge ./my-project --inspect
{
  "name": "my-project",
  "description": "...",
  "language": "Python",
  ...
}

$ readme-forge ./my-project --bilingual --author "Your Name"
Generated .../my-project/README.generated.md
```

For visual screenshots, run the commands in a terminal and capture the generated Markdown preview in your editor; the project intentionally has no GUI.

## Requirements

- Python 3.10+
- `pytest` only for development/testing

## Installation

```bash
git clone https://github.com/rad03i2/readme-forge.git
cd readme-forge
python -m pip install -e .
```

For development:

```bash
python -m pip install -e . pytest
```

## Usage

Generate a safe draft (the default output is `README.generated.md`):

```bash
readme-forge /path/to/project
```

Generate English and Arabic sections and include author text:

```bash
readme-forge . --bilingual --author "Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2"
```

Inspect discovered metadata without writing:

```bash
readme-forge . --inspect
```

Pipe Markdown elsewhere:

```bash
readme-forge . --stdout > preview.md
```

Replace an existing generated file deliberately:

```bash
readme-forge . --force
```

You can also run it as a module:

```bash
python -m readme_forge . --inspect
```

## Configuration

README Forge needs no environment variables or configuration file. CLI flags are the complete configuration surface. The default output is deliberately different from `README.md` to protect existing documentation.

## Python API

```python
from readme_forge import inspect_project, render

info = inspect_project(".")
markdown = render(info, bilingual=True, author="Your Name")
print(markdown)
```

## Project structure

```text
src/readme_forge/
  __init__.py   Public API and version
  __main__.py   `python -m` entry point
  core.py       Metadata inspection, rendering, safe generation
  cli.py        Command-line interface
tests/          Functional unit and CLI tests
.github/workflows/ci.yml
```

## Testing

```bash
python -m pytest -q
python -m compileall -q src tests
readme-forge . --inspect
```

CI runs these checks across Ubuntu, Windows, and macOS on Python 3.10, 3.12, and 3.13.

## Security & privacy

All inspection is local. README Forge parses metadata as data and does not execute package scripts. It makes no network requests. Output is constrained to the chosen project directory, and overwrite requires explicit `--force`. Treat project metadata as untrusted input and review generated Markdown before publishing it.

## Limitations

- Metadata discovery currently targets `pyproject.toml` and `package.json`; unknown stacks use a conservative fallback.
- It does not infer architecture, deployment topology, screenshots, badges, API contracts, or domain-specific instructions.
- It does not rewrite an existing README intelligently; generation is intentionally deterministic and template-based.
- Package metadata can contain misleading text, so human review remains necessary.

## Optional roadmap

Future contributions may add opt-in adapters for Cargo, Go modules, Maven/Gradle, or richer template customization without weakening the local-first safety model.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security guidance is in [SECURITY.md](SECURITY.md).

## License

MIT — see [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

# العربية

## نظرة عامة

**README Forge** أداة سطر أوامر ومكتبة Python صغيرة تعمل محليًا، تقرأ بيانات المشروع المتاحة وتولد مسودة README مرتبة من دون إرسال الكود أو البيانات إلى خدمات خارجية.

## لماذا هذا المشروع؟

بداية كتابة التوثيق تتكرر في كل مشروع. تستفيد الأداة من البيانات الموجودة أصلًا في `pyproject.toml` أو `package.json` لتكوين أساس عملي يمكن للمطور مراجعته وتخصيصه بدل البدء من صفحة فارغة.

## أهم المزايا

- اكتشاف مشاريع Python من `pyproject.toml` ومشاريع JavaScript/TypeScript من `package.json`.
- وضع احتياطي آمن للمشاريع التي لا تحتوي صيغة بيانات معروفة.
- إنشاء أقسام التثبيت والاستخدام والاختبارات والأمان والقيود والمساهمة والترخيص.
- إنشاء نسخة إنجليزية وعربية كاملة عبر `--bilingual`.
- إخراج JSON عبر `--inspect` واستخدام stdout عبر `--stdout` للأتمتة.
- عدم استبدال ملف موجود إلا عند تمرير `--force` صراحةً.
- رفض مسارات الإخراج التي تخرج من مجلد المشروع المحدد.
- لا شبكة ولا Telemetry ولا API keys ولا تنفيذ لسكربتات المشروع.
- Python API قابلة لإعادة الاستخدام ومن دون تبعيات تشغيل خارجية.

## المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/readme-forge.git
cd readme-forge
python -m pip install -e .
```

للتطوير والاختبار:

```bash
python -m pip install -e . pytest
```

## الاستخدام

إنشاء مسودة آمنة باسم `README.generated.md`:

```bash
readme-forge /path/to/project
```

إنشاء نسخة ثنائية اللغة مع المؤلف:

```bash
readme-forge . --bilingual --author "Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2"
```

فحص البيانات المكتشفة بصيغة JSON دون كتابة ملف:

```bash
readme-forge . --inspect
```

إرسال Markdown إلى stdout:

```bash
readme-forge . --stdout
```

استخدم `--force` فقط عندما تريد استبدال ملف الإخراج الموجود عمدًا.

## الإعداد

لا تحتاج الأداة إلى متغيرات بيئة أو ملف إعداد. جميع الخيارات عبر CLI، واسم الإخراج الافتراضي مختلف عن `README.md` لحماية التوثيق الموجود.

## Python API

```python
from readme_forge import inspect_project, render

info = inspect_project(".")
markdown = render(info, bilingual=True, author="Your Name")
```

## بنية المشروع

المحرك موجود في `src/readme_forge/core.py`، وواجهة الأوامر في `cli.py`، والواجهة العامة في `__init__.py`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`.

## الاختبارات

```bash
python -m pytest -q
python -m compileall -q src tests
readme-forge . --inspect
```

يختبر CI المشروع على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

## المعاينة

المشروع لا يملك GUI عمدًا. لمعاينة النتيجة شغّل الأداة وافتح ملف Markdown الناتج في محرر يدعم المعاينة، ويمكن التقاط صورة للشاشة عند الحاجة إلى عرض بصري للمستودع.

## الأمان والخصوصية

الفحص محلي بالكامل ولا توجد طلبات شبكة. تُقرأ بيانات الحزم كبيانات فقط ولا يتم تشغيل سكربتاتها. الإخراج محصور داخل مجلد المشروع، والاستبدال يحتاج `--force`. يجب مراجعة Markdown قبل النشر إذا كانت بيانات المشروع من مصدر غير موثوق.

## القيود

- الاكتشاف المتخصص حاليًا لـ`pyproject.toml` و`package.json` فقط.
- لا تستنتج الأداة المعمارية أو النشر أو الصور أو عقود API أو تفاصيل المجال تلقائيًا.
- لا تعيد تحرير README موجودة بذكاء؛ التوليد مقصود أن يكون حتميًا وقائمًا على قالب واضح.
- تبقى المراجعة البشرية ضرورية لأن بيانات المشروع نفسها قد تكون غير دقيقة.

## خارطة طريق اختيارية

يمكن مستقبلًا إضافة محولات اختيارية لـCargo وGo وMaven/Gradle أو قوالب أكثر تخصيصًا مع الحفاظ على نموذج الأمان المحلي.

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وإرشادات الأمان في [SECURITY.md](SECURITY.md).

## الترخيص

MIT — راجع [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
