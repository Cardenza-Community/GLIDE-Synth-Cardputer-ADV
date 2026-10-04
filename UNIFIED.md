# Runtime Cardputer/ADV/Cardenza build

Build `pio run -e unified` (the default). Application-only image is
`dist/unified/GLIDE.bin` (or `dist/cardenza/GLIDE.bin` with the alias); do not flash its generated bootloader/partition table.
M5Unified fork identifies Cardenza by ES8156 chip ID, initializes codec and
keeps keyboard LEDs off. Other boards use upstream keyboard/audio selection.
Missing ES8156 on ADV is no longer fatal. An identified Cardenza with codec
setup failure still shows the audio error screen.

LED, battery and tilt menus follow runtime capability. DSP, render parking,
three PCM buffers, Launcher-preserving storage guards remain unchanged.
Microphone timeout guards now protect every board. Speaker.begin restores
ES8156 after PDM capture through the library callback, with no app register writes.

Fork baseline0.2.24 / M5GFX0.2.31 is a deliberate user-requested migration from
the earlier verified0.2.17 stack. Compile and codec host checks are separate
from hardware confirmation: phase0 audio/rollover and full GLIDE sound,
keyboard, SD, microphone handoff require fresh physical tests on all3 boards.
