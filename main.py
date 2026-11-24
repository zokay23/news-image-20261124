#!/usr/bin/env python3
"""news-image-20261124 entry: write the 24 November 2026 world-news poster
to /output/entry.png, byte-for-byte the committed entry.png.

No network, no randomness: the poster is pre-rendered by build_poster.py
(run it to regenerate entry.png deterministically) and copied here.
"""

import hashlib
import os
import shutil
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes",
          "sha256", sha256(dst))
    assert sha256(dst) == sha256(src), "copy is not byte-for-byte"


if __name__ == "__main__":
    main()
