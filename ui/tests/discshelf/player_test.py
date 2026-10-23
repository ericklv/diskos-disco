#!/usr/bin/env python3
"""Real LVGL pointers: copy navigation guard and local music overlay, all palettes."""
import os
from pathlib import Path
import subprocess

ui = Path(__file__).resolve().parents[2]
subprocess.run(["make", "-C", str(ui), "CROSS=", "-j1", "host-render"], check=True)
for preset, variants in ((10, (0, 1)), (11, (0, 1, 2)), (12, (0, 1)), (13, (0,))):
    for variant in variants:
        (ui / "tests/host_build/diskos.conf").unlink(missing_ok=True)
        subprocess.run([str(ui / "tests/host_build/host-render"), str(preset), str(variant),
                        "shelf-player", "0", "/dev/null"], check=True,
                       env={**os.environ, "REVIEW_SHELF_PLAYER": "1"})
print("PASS: Shelf music overlay and download navigation guard in all eight theme palettes")
