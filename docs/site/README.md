# 2.5.2 website

GitHub Pages source remains in `docs/`.

- Consistent orange/black palette, small rainbow accents, sans-serif typography and a restrained shared type scale.
- The local Monoton font is the same face as the firmware's Disco! boot lettering; its OFL licence is included alongside the font.
- Three theme galleries, original copy, screenshots, tour and newcomer guidance retained.
- On wide/tall desktop viewports, chapters briefly pin as the document scrolls. Tall sections scroll completely into view. Mobile, short viewports and reduced-motion preferences use normal flow.
- Existing screenshot swap controls and native dialog remain; without JavaScript the images and page still open normally.

Browser-control QA was unavailable. JavaScript syntax, chapter layout logic and local asset/link checks passed. No browser-rendered screenshot or device performance result is claimed.

Squash Working mode and Shortcuts now share fixed pill rows and larger headers; all five modes fit without scrolling. Preview: `screens/squash-modes.webp`.

Installation links include the macOS guide and external Apple Silicon flash tools. The floating disc progress indicator and its scroll listener have been removed.

## 3.0.0 Zune walkthrough

The original main-branch site remains the design baseline. Zune leads with seven interactive screens, four accents, full-size image viewing and keyboard-accessible screen selection. No external JavaScript or tracking is added. Reduced-motion readers retain normal page flow. The download panel explicitly distinguishes this 3.0.0 branch preview from the latest published installer.

Regenerate the 28 actual LVGL screenshots in a disposable Linux host container:

```sh
make -C ui CROSS= host-render -j4
python3 tools/render-zune-site.py --allow-host-fixtures
```

Requires Pillow. The host harness writes `/usr/data/fiio/db/song.db`; never run it on a player. Artwork is synthetic geometric illustration, not third-party album covers. Immersive is captured with its real transport overlay open. All UI colour changes are set before theme initialization.
