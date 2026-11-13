import asyncio
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class OCRServiceError(RuntimeError):
    """Raised when OCR is unavailable or text extraction fails."""


class OCRService:
    def __init__(self, languages: tuple[str, ...] = ("en",)) -> None:
        self.languages = list(languages)
        self._reader: Any | None = None

    def _get_reader(self) -> Any:
        if self._reader is None:
            try:
                import easyocr
            except ImportError as exc:
                raise OCRServiceError(
                    "Image support is not installed. Install requirements-ocr.txt."
                ) from exc

            try:
                self._reader = easyocr.Reader(self.languages, gpu=False)
            except Exception as exc:
                logger.exception("Could not initialize EasyOCR.")
                raise OCRServiceError("Could not initialize the OCR engine.") from exc
        return self._reader

    def _extract_sync(self, image_path: str) -> str:
        path = Path(image_path)
        if not path.is_file():
            raise OCRServiceError("The downloaded image file was not found.")

        reader = self._get_reader()
        try:
            results = reader.readtext(str(path), detail=0, paragraph=True)
        except Exception as exc:
            logger.exception("OCR extraction failed.")
            raise OCRServiceError("Could not read text from this image.") from exc

        extracted = "\n".join(
            item.strip() for item in results if isinstance(item, str) and item.strip()
        )
        if not extracted:
            raise OCRServiceError(
                "No readable text was found. Try a clearer, well-lit image."
            )
        return extracted

    async def extract_text(self, image_path: str) -> str:
        return await asyncio.to_thread(self._extract_sync, image_path)
