# Zune theme integration preview

Optional Zune-inspired styling on the 2.7.0 codebase, including the tested Disc Shelf playback overlay and copy navigation guard. This is development source, not a published firmware release.

![Current real LVGL screens](zune/screens/gallery.png)

## Scope

Home, music, immersive playback, library, album/artist views, selection, letter pickers, search, queue, settings, Quick Settings, Wi-Fi, Bluetooth, modes, battery, screensaver, equalizer and apps use Zune styling. Disc Shelf retains its landing screen, download handling and music controls. The five existing working modes remain unchanged.

The theme uses lowercase Open Sans, magenta accents, curved lists and a dark canvas. Appearance is fixed dark with an explanation in settings. Menu hold uses the existing configurable actions, including Shuffle!. Row swipes retain multiselect; library category swipes are restricted to the header.

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

## Credit

Adapted from namastecoconut-imagined/diskos-disco-zune, commit `13821d6d024d6dfc90d6ac505ca7e4af94f4e256`. Open Sans retains its bundled SIL Open Font License. This is an unofficial fan theme and is not affiliated with Microsoft, FiiO or Snowsky.
