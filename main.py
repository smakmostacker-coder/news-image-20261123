#!/usr/bin/env python3
"""make.fun entry: news-image-20261123.

Writes the committed front page (entry.png, drawn by make_image.py) to
$MAKEFUN_OUTPUT_DIR/entry.png, defaulting to /output/entry.png.
Standard library only, no network, byte-for-byte deterministic.
"""

import os
import shutil
from pathlib import Path

CHUNK = 64 * 1024


def main() -> None:
    src = Path(__file__).with_name("entry.png")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    with src.open("rb") as fin, dst.open("wb") as fout:
        shutil.copyfileobj(fin, fout, CHUNK)


if __name__ == "__main__":
    main()
