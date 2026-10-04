# Cardenza support

This fork keeps upstream head `b9e7a23ba2351101c806ebe5d6fe88800811646d` and
restores the last public buildable source from
`30ae81be13caf8fe28f7db734933ea4a1c53b9e8` (v3.4). Upstream removed source in
`b12e9f0acedb4209001af819288a98d61311ad01`. The Cardenza port is **v3.4-L5**;
it does not implement the later binary-only v3.5/v3.6 changes.
The original v3.6 Cardputer distribution remains in `dist/GLIDE.bin` and
`dist/NOTICES.txt`. That original binary is separate from the runtime-detecting source build below.

## Runtime hardware detection

The default `unified` build and `cardenza` alias pin [203Null/M5Unified](https://github.com/203Null/M5Unified) commit `74fe31c6d9a2bd7c04f81eb4f8f0af99262e3bc2`, M5Cardputer 1.1.1 and M5GFX 0.2.31. The same application selects original Cardputer, ADV or Cardenza at runtime. ES8156 identity at GPIO2/1 enables Cardenza handling; ADV keeps ES8311 and its keyboard. Cardenza codec initialization and PDM-to-playback recovery belong to the library, with LED, battery and IMU suppression only on Cardenza. The independent Launcher shared-NVS guard remains enabled on all builds. No new physical validation has been performed for this revision.

## Build and check

```sh
pio run -e cardenza
python support/test_cardenza_flash_mode.py
python support/test_launcher_nvs_guard.py  # requires a host g++ on PATH
pio run -e native
.pio/build/native/program                 # program.exe on Windows
```

Install `dist/cardenza/GLIDE.bin` with Software Launcher; redistribute its
matching `dist/cardenza/NOTICES.txt`. Install the app only: preserve Launcher's
bootloader, partition table, NVS, OTA data and other app slots.

## Hardware and storage

- ES8156 is identified and initialized inside M5Unified startup; Philips stereo
  I2S, 16-bit slots, BCLK 41, LRCK 43, DATA 42. Existing M5Unified audio buffers
  and DSP remain unchanged. The port requires no PSRAM.
- The original matrix keyboard is retained. Keyboard lighting is disabled,
  GPIO21 is held high, and unsupported battery/IMU/RGB paths are disabled.
- PDM microphone pins are 46/43. LISTEN checks its worker and queue errors,
  bounds waits, and restores playback after failure.
- Whole-partition NVS erase is blocked, including Arduino startup recovery.
  Ordinary page garbage collection and GLIDE's own namespace operations remain
  possible. Full storage disables persistence while preserving other apps.
- Platform and M5 dependencies are pinned to the fork versions listed above;
  the app uses the QIO SDK that matches Cardenza's shared Launcher bootloader.

## Validation scope

The prior device-tested v3.4-L5 image has SHA-256
`708ac1b482adea2c6095d20b685a52a571c34214409e000d35c1b962c8a2a051`.
On 2026-10-01 the user confirmed display, keyboard, playback and keyboard LED
off for that image. Microphone recording and repeated reboot were not confirmed.
Rebuilding this repository produces a separate artifact; passing a build or host
test does not extend that physical confirmation to a new image.

The 2026-10-02 repository rebuild passed the Cardenza device build, DSP host
tests, QIO link check, attribution check and shared-NVS guard tests. Its app
image is 915600 bytes, SHA-256
`dded15788a64a5f4bcdf4578a703267f2d13488bea50b26bd7e808d91068bbff`;
static RAM is 199856 bytes, matching the prior port. It has not been reflashed
or physically rechecked as part of this repository-history task.

The original source remains PolyForm Noncommercial 1.0.0. Preserve upstream
copyright, LICENSE and notices; the Cardenza HAL retains its own MIT license.
