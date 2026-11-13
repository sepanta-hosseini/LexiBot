import pytest

from app.schemas.ai_response import AIResponse
from app.utils.text_utils import format_ai_response, normalize_input, split_message


def test_normalize_input_collapses_whitespace():
    assert normalize_input("  hello  world\nagain ") == "hello world again"


def test_format_word_response_contains_dictionary_fields():
    result = AIResponse(
        input_type="word",
        original_text="abundant",
        english_meaning="Existing in large quantities.",
        persian_meaning="فراوان",
        part_of_speech="adjective",
        synonyms=["plentiful"],
        antonyms=["scarce"],
    )
    output = format_ai_response(result)
    assert "abundant" in output
    assert "فراوان" in output
    assert "plentiful" in output
    assert "scarce" in output


def test_format_text_response_contains_translation():
    result = AIResponse(
        input_type="text",
        original_text="This is a test.",
        persian_translation="این یک آزمایش است.",
    )
    output = format_ai_response(result)
    assert "This is a test." in output
    assert "این یک آزمایش است." in output


def test_split_message_respects_limit_and_preserves_content():
    source = "alpha beta\ngamma delta epsilon"
    chunks = split_message(source, limit=10)
    assert all(len(chunk) <= 10 for chunk in chunks)
    assert " ".join(chunks).replace("  ", " ") == source.replace("\n", " ")


def test_split_message_rejects_invalid_limit():
    with pytest.raises(ValueError):
        split_message("text", limit=0)
