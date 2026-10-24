# dev — experimental / in testing

Development continues from Disco! 3.0.0, commit `721e07ee2266466888d84b92e756fd3a4fc778b1` (`v3.0.0`). Work belongs on **dev**. Do not update main or release tags without the maintainer’s explicit instruction.

This branch is experimental and in testing. The published 3.0.0 release is a separate baseline.

## Zune animation efficiency review

The review preserves the existing animation timing, easing, momentum, font steps, opacity, artwork detail and rendering quality. No animations are removed or simplified. Immersive already uses elapsed-time rotation, cached lyric snapshots, adaptive frame pacing and hidden/off-screen suspension; those paths remain unchanged.

Implemented:

- Cache the original integer bezel geometry once, sharing it between Home, action/settings dials and curved library rows. Each scrolling row now reads a lookup instead of repeatedly evaluating square root/rounding. Both original rounding conventions are retained. The lookup uses 360 bytes plus its initialization flag, with no heap allocation or new timer.
- Cache each action-dial row’s fitted font for its three distance bands. Returning to a band reuses the result instead of measuring the same string again. The cache adds 288 bytes and resets when a label, subline or dial changes.
- Skip redundant font assignments when adjacent bands resolve to the same fitted face. Replacing text refits immediately, including all loop copies.

A proposed Home caption-alignment shortcut was rejected because the frame comparison detected differences. Its original alignment behavior remains intact.

## Validation

- `python3 ui/tests/zune_scroll_test.py`: 122 Home/action-dial frames match the 3.0.0 baseline byte for byte; both bezel rounding rules checked across off-screen and visible positions; settled callbacks produce zero style-change events; replacement text and newly added sublines invalidate fitted-font choices correctly.
- Focused host checks cover Zune Home/focus, main-icon gestures, modal volume, all Immersive entry/exit styles, live Immersive rendering and standby work suppression.
- Theme source gate passes. Static Home/Music/Quick Settings/Settings frames are compared with the baseline in Disco, Null, Squash and Zune.

Build the host renderer before the scroll check:

```sh
make -C ui CROSS= host-render -j1
python3 ui/tests/zune_scroll_test.py
```

The golden scroll hashes in `ui/tests/fixtures/zune-scroll-3.0.0.txt` were captured with the same diagnostic against unmodified 3.0.0 production sources. They cover 61 intermediate offsets in each of two scrolling scenes.

These are host checks, not measured device frame-rate or battery improvements. On the Disc, check long scrolling sessions, cold and warm settings menus, library font sizes, touch response while music plays and Immersive entry/exit.

The tracked `payload/mq_ui` and its metadata remain the original 3.0.0 release artifact. They do **not** contain these source changes. A new target build and device validation are required before distributing a development firmware; the release preflight correctly rejects changed UI sources against the older artifact.
