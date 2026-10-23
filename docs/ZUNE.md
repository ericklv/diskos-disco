# Zune theme integration preview

Optional Zune-inspired styling on the 2.7.0 codebase, including the tested Disc Shelf playback overlay and copy navigation guard. This is development source, not a published firmware release.

![Current real LVGL screens](zune/screens/gallery.png)

## Scope

Home, music, immersive playback, library, album/artist views, selection, letter pickers, search, queue, settings, Quick Settings, Wi-Fi, Bluetooth, modes, battery, screensaver, equalizer and apps use Zune styling. Disc Shelf retains its landing screen, download handling and music controls. The five existing working modes remain unchanged.

The theme uses lowercase Open Sans, magenta accents, curved lists and a dark canvas. Appearance is fixed dark with an explanation in settings. Menu hold uses the existing configurable actions, including Shuffle!. Row swipes retain multiselect; library category swipes are restricted to the header.

## Shared library and controls update

All work remains on `integration/zune-theme`; main and release tags are untouched.

- Immersive: left-edge Back stays available with scrubbing off or on. Feedback follows the finger; reverse the drag before release to cancel. A normal tap still reveals Zune playback controls.
- Quick Settings: up to six user-selected actions, using the shared Items editor. Zune keeps its original Wi-Fi, Bluetooth, Gain, Shuffle, Sleep and Modes defaults; EQ and the other shared actions can replace them. Radio/EQ taps toggle, their holds open the full screen. Gain hold opens Audio; other destinations open normally. Copy navigation restrictions remain active.
- Album View: List / Wall / Coverflow for every theme. List is text only; Wall reuses the three-column Zune tiles and bounded thumbnail worker; Coverflow uses Zune’s curved cover geometry in each theme. The old reflected Coverflow presentation is replaced. The former numeric Cover Flow choice (1) now selects Wall; choose Coverflow (2) to use the new carousel.
- Library: swipe the header or tap either adjacent category to cycle Songs / Albums / Artists / Genres. Header Back returns to the library overview. Row swipes remain selection gestures in text lists. The main-menu Albums shortcut respects Album View too.

No new periodic timer is added. Header watching runs only during a held header touch; thumbnails stop doing work when the relevant page is hidden or the display is off.

## Preserve the working firmware

The fork’s USB-C audio routing, power-button changes, framebuffer recovery, boot workarounds, automatic shutdown policy and global compiler optimization changes are excluded. Bluetooth and Wi-Fi backend behavior remains on the current base. No release version, tag, device binary or website release claim changes here.

Thumbnail loading is limited to relevant visible pages, with a 24-entry cache and a sleeping worker off-page or with the display off. Visible clock/rim updates use the existing UI loop rather than extra periodic timers. This reduces unnecessary work; battery life and peak RAM still require device measurement.

## Validation

- Host build and 51 screen fixture renders completed; these are real LVGL renders with preview music and artwork.
- Pointer checks exercised menu navigation, configured Shuffle!, transport, Quick Settings and modal Back handling.
- Disc Shelf overlay, cancellation cleanup and exit guards passed across eight theme/palette combinations.
- Home, music, settings and Quick Settings in Disco, Null and Squash remained pixel-identical to the previous build (12 comparisons).
- Library fixture exercised populated songs/albums/artists/genres, letter grid and row swipe selection.

Host tests do not establish hardware stability. Before release: test long library sessions, all font choices, lock/wake, radio reconnects, immersive seeking, real downloads and playback together, and measure memory/battery on the Disc. Additional font tables increase the compiled binary; no device-size measurement has been made yet.

## Follow-up validation

34 host checks/render cases passed in this shared-controls pass, including header gestures in all seven presets and all three album modes, row-selection gestures in Disco/Null/Squash/Zune, saved QS ordering and EQ/radio actions, and cancelled/completed immersive Back with scrubbing off/on. Disc Shelf playback/exit-guard regression checks passed in all eight palettes.

![Shared album views](zune/screens/shared-album-views.png)
![Zune controls](zune/screens/shared-controls.png)

## Credit

Adapted from namastecoconut-imagined/diskos-disco-zune, commit `13821d6d024d6dfc90d6ac505ca7e4af94f4e256`. Open Sans retains its bundled SIL Open Font License. This is an unofficial fan theme and is not affiliated with Microsoft, FiiO or Snowsky.
