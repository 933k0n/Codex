from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.docgen import render_contract
from src.requisites import (
    parse_requisites_from_url,
    parse_uploaded_requisites,
)


st.set_page_config(page_title="Генератор договоров", page_icon="📄", layout="centered")

st.title("📄 Генератор договора из шаблона .docx")
st.write(
    "Загрузите шаблон договора и реквизиты клиента (файлом или ссылкой). "
    "Приложение подставит реквизиты, преамбулу, подписи и текущую дату."
)

with st.form("contract_form"):
    template_file = st.file_uploader("Шаблон договора (.docx)", type=["docx"])

    source_type = st.radio(
        "Источник реквизитов",
        ["Файл", "Ссылка"],
        horizontal=True,
    )

    req_file = None
    req_url = ""

    if source_type == "Файл":
        req_file = st.file_uploader("Файл с реквизитами (.txt/.json/.docx)", type=["txt", "json", "docx"])
    else:
        req_url = st.text_input("URL страницы с реквизитами", placeholder="https://example.com/requisites")

    submitted = st.form_submit_button("Сформировать договор")

if submitted:
    if template_file is None:
        st.error("Пожалуйста, загрузите шаблон договора .docx")
        st.stop()

    try:
        if source_type == "Файл":
            if req_file is None:
                st.error("Пожалуйста, загрузите файл с реквизитами")
                st.stop()
            requisites = parse_uploaded_requisites(req_file.name, req_file.read())
        else:
            if not req_url.strip():
                st.error("Пожалуйста, укажите URL")
                st.stop()
            requisites = parse_requisites_from_url(req_url.strip())

        context = requisites.to_context()

        st.subheader("Предпросмотр извлеченных полей")
        st.json(context)

        rendered = render_contract(template_file.read(), context)

        date_part = datetime.now().strftime("%Y%m%d")
        filename = f"contract_{date_part}.docx"

        st.download_button(
            "⬇️ Скачать готовый договор",
            data=rendered,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        st.success("Договор сформирован. Проверьте документ перед отправкой клиенту.")

    except Exception as exc:  # noqa: BLE001
        st.exception(exc)
