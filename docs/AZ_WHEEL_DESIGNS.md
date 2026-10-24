# A-Z wheel design studies

Three host-only LVGL design studies. Focus (design 2) was selected and integrated
for 3.0.1, with the heading above the centre letter removed. The alternatives
remain preview-only; the production implementation lives in ui/azjump.c.

1. Halo: fixed full alphabet, softly feathered annulus, faint upper rim highlight,
   theme-native centre button.
2. Focus dial: current letter at twelve o’clock; neighbouring letters emphasised,
   distant letters fade; minimal centre confirmation area.
3. Orbit: gently shaded full disc, rim ticks, accent centre tile and adjacent
   letters. Null uses compact square corners; Zune uses lowercase Open Sans;
   Braun uses its Inter faces.

All colours come from semantic theme roles. Letter fonts follow theme faces;
large Zune alphabet uses the full-character 52px font cut, not digit-only clocks.
Every alphabet glyph is checked in both ring and centre fonts during preview.
Fades are bounded static LVGL arcs/gradients, with no runtime blur required.
These are design studies, not target-device performance measurements.

Preview: build `make -C ui CROSS= host-render`, then run host-render with
`LETTER_WHEEL_PREVIEW=wheel AZ_DESIGN=1` (or 2/3), a valid `ZNP_PATH` fixture,
and the normal theme/variant/preview-home/output arguments.

Keep the current wheel’s clockwise/reverse selection, wrapping, centre-tap,
auto-confirm, held-touch and Back cancellation contracts when integrating.
