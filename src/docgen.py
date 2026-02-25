from __future__ import annotations

from io import BytesIO

from docxtpl import DocxTemplate


def render_contract(template_bytes: bytes, context: dict[str, str]) -> bytes:
    template_io = BytesIO(template_bytes)
    doc = DocxTemplate(template_io)
    doc.render(context)

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output.read()
