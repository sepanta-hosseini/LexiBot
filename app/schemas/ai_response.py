from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    input_type: Literal["word", "phrase", "text"]
    original_text: str = Field(min_length=1)
    english_meaning: str | None = None
    persian_meaning: str | None = None
    part_of_speech: str | None = None
    synonyms: list[str] = Field(default_factory=list, max_length=10)
    antonyms: list[str] = Field(default_factory=list, max_length=10)
    persian_translation: str | None = None
    usage_example: str | None = None

    @field_validator("synonyms", "antonyms")
    @classmethod
    def clean_word_lists(cls, values: list[str]) -> list[str]:
        return [value.strip() for value in values if value and value.strip()]
