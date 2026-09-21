# Security Policy / سياسة الأمان

README Forge is local-first and makes no network requests. It reads project metadata and writes Markdown only to a path inside the selected project directory.

## Reporting

Please report security concerns privately through GitHub's security reporting facilities when available. Do not publish credentials or exploit details in a public issue.

## Safety properties

- Existing output is not overwritten unless `--force` is explicit.
- Output paths escaping the selected project directory are rejected.
- Package metadata is parsed as data; project scripts are never executed.
- Generated Markdown should still be reviewed before publication because source metadata may contain untrusted text.

الأداة تعمل محليًا ولا ترسل بيانات عبر الشبكة. لا تُنفَّذ سكربتات المشروع أثناء قراءة البيانات، ويُرفض مسار الإخراج خارج مجلد المشروع، ولا تتم الكتابة فوق ملف موجود دون `--force`. راجع Markdown الناتج قبل نشره إذا كانت بيانات المشروع من مصدر غير موثوق.
