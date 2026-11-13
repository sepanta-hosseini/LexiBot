from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.services.ai_service import AIService, AIServiceError


@pytest.mark.asyncio
async def test_ai_service_parses_valid_json_response():
    content = (
        '{"input_type":"word","original_text":"abundant",'
        '"english_meaning":"Existing in large quantities.",'
        '"persian_meaning":"فراوان","part_of_speech":"adjective",'
        '"synonyms":["plentiful"],"antonyms":["scarce"],'
        '"persian_translation":null,"usage_example":"Food is abundant."}'
    )
    create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=content)
                )
            ]
        )
    )
    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=create)
        )
    )
    service = AIService(
        api_key="test-key",
        client=client,
        max_text_length=100,
    )

    result = await service.analyze(" abundant ")

    assert result.original_text == "abundant"
    assert result.persian_meaning == "فراوان"
    create.assert_awaited_once()


@pytest.mark.asyncio
async def test_ai_service_rejects_empty_input():
    service = AIService(api_key="test-key", client=object())
    with pytest.raises(AIServiceError, match="empty"):
        await service.analyze("   ")


@pytest.mark.asyncio
async def test_ai_service_rejects_too_long_input():
    service = AIService(
        api_key="test-key",
        client=object(),
        max_text_length=3,
    )
    with pytest.raises(AIServiceError, match="too long"):
        await service.analyze("four")


@pytest.mark.asyncio
async def test_ai_service_rejects_invalid_provider_json():
    create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="not-json"))]
        )
    )
    client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )
    service = AIService(api_key="test-key", client=client)
    with pytest.raises(AIServiceError, match="couldn't analyze"):
        await service.analyze("abundant")
