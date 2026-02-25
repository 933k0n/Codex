from src.requisites import parse_from_json_dict, parse_from_text


def test_parse_from_text_extracts_core_fields() -> None:
    text = """
    ООО "Ромашка"
    ИНН 7701234567
    КПП 770101001
    ОГРН 1027700123456
    Юридический адрес: г. Москва, ул. Пример, д. 1
    Генеральный директор: Иванов Иван Иванович
    действует на основании: Устава
    """

    req = parse_from_text(text)
    assert req.company_name.startswith("ООО")
    assert req.inn == "7701234567"
    assert req.kpp == "770101001"
    assert req.ogrn == "1027700123456"
    assert "Москва" in req.legal_address
    assert "Иванов" in req.director_name


def test_parse_from_json_dict_maps_synonyms() -> None:
    req = parse_from_json_dict(
        {
            "название": "ООО Тест",
            "инн": "1234567890",
            "кпп": "123456789",
            "юридический адрес": "г. Тест, ул. Полевая, 2",
            "генеральный директор": "Петров Петр Петрович",
        }
    )

    assert req.company_name == "ООО Тест"
    assert req.inn == "1234567890"
    assert req.kpp == "123456789"
    assert req.legal_address.startswith("г. Тест")
    assert req.director_name.startswith("Петров")


def test_to_context_contains_generated_blocks() -> None:
    req = parse_from_json_dict(
        {
            "company_name": "ООО Тест",
            "inn": "1234567890",
            "kpp": "123456789",
            "director_name": "Петров Петр Петрович",
            "acting_on": "Устава",
        }
    )

    context = req.to_context()
    assert "contract_date" in context
    assert "п" not in context["contract_date"].lower()
    assert "ООО Тест" in context["preamble_client"]
    assert "Подпись" in context["signature_block_client"]
