"""Durable storage for completed customer enquiries."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Lock

from config import ENQUIRIES_FILE


class EnquiryStorage:
    """Append completed enquiries to a JSON list safely."""

    _write_lock = Lock()

    def __init__(self, file_path=None):
        self.file_path = Path(file_path or ENQUIRIES_FILE)

    def save_enquiry(self, enquiry):
        """Persist an enquiry and return the stored record."""
        record = enquiry.to_dict()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # The API can handle concurrent requests, so keep the read/append/write
        # sequence together as well as writing the final file atomically.
        with self._write_lock:
            enquiries = self._load_enquiries()
            enquiries.append(record)
            self._write_enquiries(enquiries)
        return record

    def _load_enquiries(self):
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                enquiries = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise RuntimeError(
                f"Unable to read enquiry storage: {self.file_path}"
            ) from error

        if not isinstance(enquiries, list):
            raise RuntimeError(
                f"Enquiry storage must contain a JSON list: {self.file_path}"
            )
        return enquiries

    def _write_enquiries(self, enquiries):
        with NamedTemporaryFile(
            "w", encoding="utf-8", dir=self.file_path.parent,
            prefix=f".{self.file_path.stem}-", suffix=".tmp", delete=False
        ) as temporary_file:
            json.dump(enquiries, temporary_file, indent=2, ensure_ascii=False)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)

        try:
            os.replace(temporary_path, self.file_path)
        except OSError:
            temporary_path.unlink(missing_ok=True)
            raise
