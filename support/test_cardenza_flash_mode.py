# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (C) 2026 Charles Tobin (CHARL3X)
"""Run after pio run: validate both the app header and linked Flash driver."""
from configparser import ConfigParser
from pathlib import Path

root = Path(__file__).resolve().parents[1]
config = ConfigParser(interpolation=None)
config.read(root / "platformio.ini", encoding="utf-8")
assert config["base"]["board_build.flash_mode"] == "qio", "Match the Cardenza QIO bootloader"
image = (root / "dist/cardenza/GLIDE.bin").read_bytes()
assert image[0] == 0xE9 and image[2] == 2, "Pinned Arduino SDK emits a DIO app header"
link = (root / ".pio/build/cardenza/firmware.map").read_text(encoding="utf-8")
assert "esp32s3/qio_qspi" in link and "esp32s3/dio_qspi" not in link, \
    "Correct .bin header alone does not select the matching SDK driver"
assert "nvsProbe" not in link, "Normal instrument must exclude diagnostics"
assert "__wrap_nvs_flash_erase" in link and "__wrap_esp_partition_erase_range" in link, \
    "Shared-NVS recovery guards must be linked"
notices = (root / "dist/cardenza/NOTICES.txt").read_text(encoding="utf-8")
assert "Cardenza HAL" in notices and "LICENCE TEXT MISSING" not in notices
assert "UNLISTED LIBRARIES" not in notices, "Review attribution before publishing"
print("PASS: QIO SDK driver selected; normal app retains the SDK's DIO header")
