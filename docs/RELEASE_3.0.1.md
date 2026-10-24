# Disco 3.0.1 validation

This release includes the changes from dev since 3.0.0: theme rendering/cache work,
idle-shutdown fixes, the unified settings hierarchy and the chosen Focus A–Z wheel.

- Focus uses theme font/colour roles, a fixed top selection, bounded static highlights
  and distance-based letter fades. It omits the old heading. Positions are cached;
  selection changes do not allocate objects. The existing timeout timer is reused.
- Wheel checks cover clockwise/reverse movement, Z/#/A wrapping, fixed selection,
  glyph coverage, tap/timeout confirmation, held touch, Back and repeated teardown.
- Settings checks cover all seven themes / twelve appearances, every visible submenu
  and Back path, nonempty destinations, Equalizer/Details routing and saved preferences.
- Retained setting keys, option arrays, bounds, defaults and handlers are unchanged.
- Theme regression fixtures retain previous animation, Home, Music and Quick Settings
  output. Only the intentional seven-category settings-root snapshots are new.
- Idle shutdown, shutdown flow, audio-running and plugged-in detection host checks pass.
- The known REVIEW_HINTS song/album overlay assertion also fails on the pre-change host
  baseline. The remaining focused Display cases are checked independently.

The payload metadata records the exact source digest, compiler/ABI and binary hashes.
`tools/check-release.py --tag v3.0.1` must pass before packaging. The release workflow
can now run when a version bump reaches main as well as on an existing version tag;
it creates the matching tag only after preparation and packaging succeed.

Host checks and ABI checks are not physical device tests. Extended playback,
charging limits, physical shutdown, USB-C DAC/cable compatibility and real NAS/SD
acceptance remain on-device checks. The boot, signature and fail-closed safety
contracts are unchanged.
