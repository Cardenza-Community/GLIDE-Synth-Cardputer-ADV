# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (C) 2026 Charles Tobin (CHARL3X)
"""Run the real erase guard with fake IDF types and an observable erase backend."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp)
    (p / "esp_err.h").write_text(
        "#pragma once\nusing esp_err_t = int;\n#define ESP_ERR_NOT_SUPPORTED 0x106\n"
    )
    (p / "esp_partition.h").write_text(
        "#pragma once\n#include <cstddef>\n"
        "struct esp_partition_t {int type, subtype; size_t size;};\n"
        "#define ESP_PARTITION_TYPE_DATA 1\n"
        "#define ESP_PARTITION_SUBTYPE_DATA_NVS 2\n"
    )
    (p / "test.cpp").write_text(r'''
#include <cassert>
#include <esp_err.h>
#include <esp_partition.h>
extern "C" int __wrap_nvs_flash_erase();
extern "C" int __wrap_esp_partition_erase_range(const esp_partition_t*, size_t, size_t);
static int calls;
extern "C" int __real_esp_partition_erase_range(const esp_partition_t*, size_t, size_t) {
    ++calls;
    return 37; // Backend errors must be propagated unchanged.
}
int main() {
    esp_partition_t nvs{1, 2, 0x5000}, app{0, 16, 0x100000}, data{1, 3, 0x5000};
    assert(__wrap_nvs_flash_erase() == ESP_ERR_NOT_SUPPORTED);
    assert(__wrap_esp_partition_erase_range(&nvs, 0, nvs.size) == ESP_ERR_NOT_SUPPORTED);
    assert(calls == 0);
    assert(__wrap_esp_partition_erase_range(&nvs, 0, 0x1000) == 37);
    assert(__wrap_esp_partition_erase_range(&nvs, 0x1000, 0x1000) == 37);
    assert(__wrap_esp_partition_erase_range(&app, 0, app.size) == 37);
    assert(__wrap_esp_partition_erase_range(&data, 0, data.size) == 37);
    assert(__wrap_esp_partition_erase_range(nullptr, 0, 0) == 37);
    assert(calls == 5);
}
''')
    exe = p / "test.exe"
    subprocess.run(["g++", "-std=c++14", "-I", str(p),
                    str(root / "src/launcher_nvs_guard.cpp"), str(p / "test.cpp"),
                    "-o", str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
print("PASS: whole-NVS erase blocked; page GC and unrelated operations preserved")
