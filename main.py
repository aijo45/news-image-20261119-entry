#!/usr/bin/env python3
"""Entry program: write the front-page image to /output/entry.png.

The image (entry.png, JPEG data) ships in this repository; this program only
copies it to the grader's output path. Deterministic: the same bytes on every
run. No network, no randomness, no dependencies beyond the standard library.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path("/output/entry.png")


def main():
    src = HERE / "entry.png"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT)


if __name__ == "__main__":
    main()
