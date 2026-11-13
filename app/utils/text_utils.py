from app.schemas.ai_response import AIResponse


def normalize_input(text: str) -> str:
    return " ".join(text.split())


def format_ai_response(result: AIResponse) -> str:
    if result.input_type in {"word", "phrase"}:
        sections = [
            f"📘 {result.original_text}",
            "",
        ]
        if result.part_of_speech:
            sections.append(f"Part of speech / نقش دستوری: {result.part_of_speech}")
        if result.english_meaning:
            sections.extend(["", "🇬🇧 English meaning:", result.english_meaning])
        if result.persian_meaning:
            sections.extend(["", "🇮🇷 معنی فارسی:", result.persian_meaning])
        if result.synonyms:
            sections.extend(["", "🔹 Synonyms / مترادف‌ها:", ", ".join(result.synonyms)])
        if result.antonyms:
            sections.extend(["", "🔸 Antonyms / متضادها:", ", ".join(result.antonyms)])
        if result.usage_example:
            sections.extend(["", "✍️ Example:", result.usage_example])
        return "\n".join(sections).strip()

    sections = [
        "🇬🇧 Original text:",
        result.original_text,
        "",
        "🇮🇷 ترجمه فارسی:",
        result.persian_translation or "ترجمه‌ای برای این متن تولید نشد.",
    ]
    return "\n".join(sections).strip()


def split_message(text: str, limit: int = 4000) -> list[str]:
    if limit < 1:
        raise ValueError("limit must be greater than zero.")
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit + 1)
        if split_at <= 0:
            split_at = remaining.rfind(" ", 0, limit + 1)
        if split_at <= 0:
            split_at = limit
        chunks.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    if remaining:
        chunks.append(remaining)
    return chunks
