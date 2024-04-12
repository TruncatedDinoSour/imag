#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ocr migration"""

import os
import sqlite3
import sys
from warnings import filterwarnings as filter_warnings

import PIL
import pytesseract  # type: ignore


def main() -> int:
    """entry / main function"""

    if len(sys.argv) < 3:
        print(
            f"Usage: {sys.argv[0]} <images directory> <max ocr size>", file=sys.stderr
        )
        return 1

    s: int = int(sys.argv[2])

    print("-- Migration for version 3.0.0: OCR support")

    print(f"ALTER TABLE image ADD COLUMN ocr VARCHAR({s}) NOT NULL DEFAULT '';")

    conn: sqlite3.Connection = sqlite3.connect(":memory:")

    for image in os.listdir(sys.argv[1]):
        with PIL.Image.open(os.path.join(sys.argv[1], image)) as img:  # type: ignore
            ocr: str = str(pytesseract.image_to_string(img)).strip()[:s].strip()  # type: ignore
            ocre: str = conn.execute("SELECT quote(?);", (ocr,)).fetchone()[0]
            print(f"UPDATE image SET ocr={ocre} WHERE iid={os.path.basename(image)};")

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())
