#!/usr/bin/env python3
"""news-image-20261125 entry (Python 3.13, standard library only).

The image is the entry.png beside this file, rendered at build time from
real 25 November 2026 news; the program copies it to /output/entry.png.
The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels; the
judge sees exactly the bytes copied.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(_HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
