// SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
// Copyright (C) 2026 Charles Tobin (CHARL3X)
#include <esp_err.h>
#include <esp_partition.h>

// Cover Arduino startup recovery as well as GLIDE's storage reset paths.
// Shared NVS belongs to Launcher and all installed apps, not only GLIDE.
extern "C" esp_err_t __wrap_nvs_flash_erase() {
    return ESP_ERR_NOT_SUPPORTED;
}

extern "C" esp_err_t __real_esp_partition_erase_range(
    const esp_partition_t*, size_t, size_t);

extern "C" esp_err_t __wrap_esp_partition_erase_range(
    const esp_partition_t* partition, size_t offset, size_t size) {
    // Arduino's initArduino bypasses nvs_flash_erase on an NVS format error.
    // Keep ordinary single-page NVS garbage collection working.
    if (partition && partition->type == ESP_PARTITION_TYPE_DATA &&
        partition->subtype == ESP_PARTITION_SUBTYPE_DATA_NVS &&
        offset == 0 && size == partition->size) {
        return ESP_ERR_NOT_SUPPORTED;
    }
    return __real_esp_partition_erase_range(partition, offset, size);
}
