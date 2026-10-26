# Display settings: ownership split (organising draft)

Status: ownership classification implemented under the approved hierarchy in
[SETTINGS_TEMPLATE.md](SETTINGS_TEMPLATE.md). Timing controls have moved to Battery
& power, online services to Connectivity, and 24-hour time to System / Date & time.

## Agreed Display root

1. Brightness
2. Theme
3. <selected theme> settings (for example Disco settings or Zune settings)
4. Submenus containing controls common to the modern themes

Modern themes here means Disco, Null, Squash and Zune. Ring and Braun do not
constrain the modern shared structure: retain their own controls in Ring settings
and Braun settings. No feature removal is implied. Stone/custom themes need their
own applicability check rather than silently inheriting a modern theme's controls.

The shared submenu names and order are defined in SETTINGS_TEMPLATE.md. The
lists below explain the ownership split.

## Common pool: modern shared features

| Setting / feature | Ownership and preservation requirement |
| --- | --- |
| Brightness | Shared backlight setting, pinned at Display root. |
| Theme | Shared picker, pinned second; keep saved theme IDs. |
| List/body text size | Shared library/body sizing; does not promise to resize every theme's title. |
| Screen rotation | Shared display/touch control; keep firmware capability guard. |
| Screen transitions | Shared animation preference; preserve existing animations. |
| 24-hour time | Shared clock-format preference; themes draw their own clocks. |
| Screen-off delay | Shared backlight policy. |
| Screensaver/standby delay | Shared activation timing, separate from each theme's saver design. |
| Album view | Shared List / Wall / Coverflow selection. |
| Album-list track numbers | Shared list preference; distinct from a Music-screen title number. |
| Back-swipe distance | Shared threshold in the main input loop. |
| Immersive style | Shared Vinyl / CD / Cover implementation. |
| Immersive lyrics | Shared artwork/lyrics overlay switch. |
| Immersive circular control | Shared enable switch. |
| Immersive control action | Shared seek/volume choice; preserve enable dependency. |
| Quick Settings items | Common capability, different theme editors, capacities and saved keys. Keep each theme's choices independent. |
| Shortcuts | Shared shortcut-picker feature; keep existing entry points and stored choices. |
| Online album art / lyrics | Shared services, not theme appearance controls. Final category/submenu placement still undecided. |
| Artwork cache | Shared artwork service; final placement undecided. |
| Weather service switch | Shared fetch/service preference, separate from a theme-specific weather/clock display. Final placement undecided. |

Shared in concept does not require a shared stored key. Conversely a setting
being present in the settings table does not prove it works for every theme.

## Theme-owned pool

These go into the selected theme's named menu, never into an unrelated theme's
menu as disabled leftovers. Some themes have a similar concept with different
behaviour; keep their own controls and keys rather than pretending all four have
one interchangeable implementation.

| Theme | Its own settings |
| --- | --- |
| Disco | Light/dark and automatic appearance; supported accent/colour controls; rim sheen; Music text/font/alignment, clock, times and title track number; progress colour/shape; configurable button/autofade/gesture controls; navigation side, menu items and menu actions; Classic/Straight/Disco list motion; Quick Settings List/Arc layout. |
| Null | Colour scheme/palette; menu-arrow colours; Music background and font set, alignment, clock/album/title-number display; button/autofade/gesture controls; drawer timeout and menu actions; list motion; Quick Settings Text/Icons layout. Fixed-dark appearance and fixed-right navigation are properties, not working switches to expose. |
| Squash | Music background; Music font/alignment and supported information indicators, including playback state/mode; progress shape/colour; supported EQ/volume colouring; editable navigation destinations/actions; list motion. Keep its independent simple_* settings. Gesture controls, right-side navigation and its Quick Settings layout are fixed; do not offer Disco's switches for them. |
| Zune | Accent; main-icon tap/double-tap/hold actions; main-menu hold action; lock-screen Album Art/Clock Only selection and clock-accent treatment. Typography, dark appearance, progress and transport design are fixed where no actual selector exists. |

### Appearance is not wholly common

Light/dark is configurable in Disco/Squash but Null and Zune are fixed-dark.
The Display > Light / dark selector offers Dark, Light and Auto for supported themes. Auto is dark from 19:00 to 07:00 and light otherwise; switching happens while the display is off. Custom accent selection is blocked for Null and Squash. These controls
must be classified by actual capability, rather than grouped as universal ones.

### Similar names do not imply the same setting

- Quick Settings **items** are a common feature. Text/Icons, List/Arc and fixed
  theme layouts are theme-owned presentation choices.
- Standby **timing** is common. Zune lock-screen content/tint and legacy saver
  styles belong to their own themes.
- Album-list track numbers are common. Prefixing the Music-screen title is not
  implemented by the same control in every theme.
- Weather fetching is shared. Clock/weather/battery decoration controls currently
  used by Disco/Squash/Null are not automatically Zune decoration controls.
- Library/body text size is common. Selecting a Music-title font family is owned
  by the theme that actually consumes that setting.

## Ring and Braun

Retain their current theme-specific settings and applicable legacy Now Playing /
screensaver controls under their own named menus. Preserve the Now Playing style
named Ring and all its supported options; it is distinct from the Ring theme.
Do not copy Disco's navigation, Squash's Music controls or Null's palettes here.
Determine exact applicable rows before implementing these named menus.

## Items requiring clarification, not an invented working switch

- Startup disc colour (`disc_colour`) was removed with user approval: no rendering
  consumer was found. Old stored values remain harmless.
- Clock battery-percentage/weather decorations and interaction hints have
  implementation-specific consumers. Treat them as theme-owned/limited-support
  until applicability is mapped, rather than promising them in every modern theme.
- DSD Output remains a read-only Audio information row; it is outside this Display
  split and does not send a mode command.

## Code grounding

- `ui/settings.c`: setting keys, handlers, current descriptions and blocked actions.
- `ui/settings_display.h`: current presentation aliases, visibility and capability guards.
- `ui/simple_theme.c`: inherited disco_* settings map to independent simple_* keys;
  several Squash choices are deliberately fixed rather than configurable.
- `ui/theme.c`: automatic appearance capability and Music font selection.
- `ui/disco_home.c`, `ui/null_theme.c`: actual Music text, clock and progress consumers.
- `ui/zune_home.c`, `ui/home_shortcuts.c`, `ui/zune_saver.c`: Zune menu/icon/lock controls.
- `ui/main.c`, `ui/ui.c`, `ui/library.c`, `ui/quicksettings.c`: shared input, standby,
  Immersive, library presentation and per-theme Quick Settings item limits.
