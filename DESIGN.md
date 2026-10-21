---
name: DSSantos Terminal
description: A GitHub profile drawn as a run of amber LED passenger information displays, every letter a lit dot.
colors:
  led-amber: "#FFB000"
  led-off: "#2A1E06"
  black-glass: "#0B0A08"
  housing-charcoal: "#1B1B19"
  housing-edge: "#34332E"
  silkscreen-grey: "#9A968A"
  live-green: "#3DDC84"
  screw-head: "#2B2A26"
  counter-amber: "#9A5B00"
typography:
  route-prompt:
    fontFamily: "PIS 5x7 (hand-set bitmap in scripts/build_displays.py), bold, 3x"
    fontSize: "84px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "1 dot"
  display:
    fontFamily: "PIS 5x7 (hand-set bitmap in scripts/build_displays.py), 2x"
    fontSize: "56px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "1 dot"
  sign-line:
    fontFamily: "PIS 5x7 (hand-set bitmap in scripts/build_displays.py), 1x"
    fontSize: "28px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "1 dot"
  board-title:
    fontFamily: "PIS 5x7 (hand-set bitmap in scripts/build_displays.py), bold, 1x"
    fontSize: "21px"
    fontWeight: 700
    lineHeight: "11 dots"
    letterSpacing: "1 dot"
  board-body:
    fontFamily: "PIS 5x7 (hand-set bitmap in scripts/build_displays.py), 1x"
    fontSize: "21px"
    fontWeight: 400
    lineHeight: "11 dots"
    letterSpacing: "1 dot"
  silkscreen:
    fontFamily: "PIS 5x7 (hand-set bitmap in scripts/build_displays.py), square pixels, 1x"
    fontSize: "18.2px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "1 dot"
rounded:
  housing: "16px"
  glass: "6px"
spacing:
  dot-pitch-sign: "4px"
  dot-pitch-board: "3px"
  dot-pitch-silkscreen: "2.6px"
  housing-inset-x: "8px"
  housing-inset-top: "6px"
  housing-margin-bottom: "16px"
  matrix-top: "22px"
  glass-bezel: "8px"
  silkscreen-strip: "50px"
  board-row-stride: "24 dots"
components:
  housing:
    backgroundColor: "{colors.housing-charcoal}"
    rounded: "{rounded.housing}"
    width: "864px"
  glass:
    backgroundColor: "{colors.black-glass}"
    rounded: "{rounded.glass}"
    padding: "{spacing.glass-bezel}"
  silkscreen-strip:
    backgroundColor: "{colors.housing-charcoal}"
    textColor: "{colors.silkscreen-grey}"
    typography: "{typography.silkscreen}"
    height: "{spacing.silkscreen-strip}"
  destination-sign:
    backgroundColor: "{colors.black-glass}"
    textColor: "{colors.led-amber}"
    typography: "{typography.display}"
    size: "205 x 36 dots at 4px pitch"
    height: "238px"
    width: "880px"
  route-badge:
    backgroundColor: "{colors.led-amber}"
    textColor: "{colors.led-off}"
    typography: "{typography.route-prompt}"
    height: "28 dots"
  departures-board:
    backgroundColor: "{colors.black-glass}"
    textColor: "{colors.led-amber}"
    typography: "{typography.board-body}"
    size: "273 x 134 dots at 3px pitch"
    height: "496px"
    width: "880px"
  line-number-block:
    backgroundColor: "{colors.led-amber}"
    textColor: "{colors.led-off}"
    typography: "{typography.board-title}"
    size: "13 x 11 dots"
  usage-bar:
    backgroundColor: "{colors.led-off}"
    textColor: "{colors.led-amber}"
    size: "12 cells, 3 x 7 dots each, 1-dot gutter"
  service-updates-board:
    backgroundColor: "{colors.black-glass}"
    textColor: "{colors.led-amber}"
    typography: "{typography.board-body}"
    size: "273 x 80 dots at 3px pitch"
    height: "334px"
  terminus-sign:
    backgroundColor: "{colors.black-glass}"
    textColor: "{colors.led-amber}"
    typography: "{typography.display}"
    size: "205 x 36 dots at 4px pitch"
    height: "238px"
  live-pip:
    backgroundColor: "{colors.live-green}"
    size: "6.8px"
---

# Design System: DSSantos Terminal

## Overview

**Creative North Star: "The Passenger Information Display"**

The profile is a run of real-looking PIS hardware: amber LEDs on black glass, inside charcoal housings that carry a silkscreened model strip. Every visible letter is a lit dot drawn from one hand-set 5x7 face, so each board reads at once as a transit sign and as a terminal printing bits. The page is a sequence of four displays in story order (destination sign, departures board, service updates, terminus), each a full-width 880-unit SVG, with GitHub's own Markdown carrying only the short prose and the link between them.

The world is dense, mechanical and flat-lit. Nothing glows, nothing is graded, and nothing moves smoothly: text steps one dot at a time and pages hard-cut, the way firmware drives a matrix. The unlit grid is always visible, because a real panel's dead LEDs are part of how it looks. The only hue outside amber is the green live pip, and it means exactly one thing.

All design tokens live in `scripts/build_displays.py`; the SVGs in `assets/` are generated output and are never hand-edited.

**Key Characteristics:**
- One colour of light (#FFB000) on one glass, with the off-state grid always drawn.
- One bitmap face, proportional, with descenders, a bold variant and integer scaling only.
- Two LED pitches (4 for signs, 3 for boards) and one square-pixel silkscreen pitch (2.6).
- Stepped motion only: steps() scrolling at 30 dots/s, hard-cut pages, on/off blinks.
- Every display is complete when static; motion is decoration over a still frame.

## Colors

A single-emitter palette: amber light, its own dark off-state, and the dull materials of the hardware around it.

### Primary
- **Sodium Amber LED** (led-amber): every lit dot, every knocked-out block. It is the only text colour inside the glass.

### Tertiary
- **Live Green** (live-green): the in-service pip in the silkscreen strip, nowhere else. Appears only on displays that carry a right-hand status label (PIS-01 · GTFS-RT LIVE, EXIT CODE 0).

### Neutral
- **Dead LED Amber** (led-off): the unlit grid, a dot at every matrix position (radius 0.33 x pitch) under the lit layer. Also the visible colour inside knockouts.
- **Black Glass** (black-glass): the display window behind the matrix, with a 1.5px #000 stroke.
- **Housing Charcoal** (housing-charcoal): the enclosure body and its silkscreen strip.
- **Housing Edge** (housing-edge): the 1px enclosure outline.
- **Silkscreen Grey** (silkscreen-grey): printed labels on the housing, square pixels only.
- **Screw Head** (screw-head): the four corner screws (r 3.2, inset 11, stroke #111110 at 0.8).
- **Counter Amber** (counter-amber): the colour parameter of the third-party komarev visitor counter. It exists so the one foreign object sits near the amber family; it is not a palette colour for new work.

### Named Rules
**The One Emitter Rule.** Inside the glass there is amber and dead amber, nothing else. A second LED colour would make it a different display.

**The Green Means Live Rule.** Live green marks real in-service status and is used for nothing decorative: no green text, no green accents, no green bars.

## Typography

**Display Font:** PIS 5x7, the hand-set bitmap in `FONT_SRC` (no fallback; it is drawn, not loaded)
**Body Font:** the same face at 1x
**Label Font:** the same face, rendered as square pixels in silkscreen grey

**Character:** A proportional dot-matrix face: glyphs are trimmed to their lit columns, letters sit on a 7-row cap height with 2 descender rows, words are separated by 3 dots and letters by 1. Bold is the glyph ORed with itself shifted one column right, which widens it by one dot. Sizes are pitch times integer scale, never fractional.

### Hierarchy
- **Route prompt** (bold, 3x at pitch 4): the ">_" knocked out of the route badge. One per destination sign.
- **Display** (regular, 2x at pitch 4): the destination ("Daniel Santos" / "Fullstack Dev") and "Terminus".
- **Sign line** (regular 1x at pitch 4; bold for callouts): the via ticker and the terminus right-hand lines ("All change", "LinkedIn ▸").
- **Board title** (bold, 1x at pitch 3): line names, service names, statuses ("Soon", "In build").
- **Board body** (regular, 1x at pitch 3): calling-at lists, notes, column headers, ordinals, tickers. Body sits 11 dots under its title.
- **Silkscreen** (regular, 1x at pitch 2.6, square caps, stroke 0.86): housing labels, uppercase, separated by "  ·  ".

### Named Rules
**The One Face Rule.** Every character on every display comes from the 5x7 face. A missing glyph is added to `FONT_SRC` as a bitmap; it is never substituted with a system font, an emoji or an icon.

**The Integer Scale Rule.** Scale is 1, 2 or 3 whole dots per dot. A size that needs a fractional scale is the wrong size; pick another pitch or another scale.

## Layout

Each display is an independent 880-unit-wide SVG embedded at `width="100%"`, so it scales as one rigid object; there are no breakpoints. The matrix is centred in the housing: columns x pitch is held near 820 units (205 x 4 = 820 for signs, 273 x 3 = 819 for boards), giving a constant 30-unit side margin across every display.

Vertical anatomy, top to bottom: 6 above the housing, 22 to the matrix, rows x pitch of matrix, a 50-unit silkscreen strip, 16 below. Glass extends 8 units around the matrix.

Inside a board, placement is in dots: a header row at row 2, a dotted separator (every second column) at row 12, entries from row 16 with a 24-dot stride (bold title, then body 11 dots lower). Right-aligned content ends at column cols - 1. Columns: line-number block in columns 1-13, text from column 18 (departures) or 22 (service updates, after the ordinal at column 1). Every text placement goes through `check_fits`, and the build fails rather than clipping or overflowing.

Between displays the README uses only GitHub defaults: a `<br>` gap, the prose block under the destination sign, and a centred footer.

## Elevation & Depth

Depth is physical and singular: the housing is an object resting on the page, lifted by one soft drop shadow, and everything inside it is flat. The glass is recessed by tone (black inside charcoal) and a black stroke, not by shadow. LEDs carry no glow, bloom or gradient.

### Shadow Vocabulary
- **Housing rest** (`feDropShadow dx=0 dy=6 stdDeviation=6 flood-color=#000 flood-opacity=.3`): on the housing rect only, so the display sits on either GitHub theme.

### Named Rules
**The Cold LED Rule.** A lit dot is a flat round-capped stroke (width 0.74 of pitch). No blur, glow, halo or gradient on any dot.

## Shapes

Dots are round (zero-length path segments with round caps); silkscreen pixels are square (square caps). The housing is a 16-unit rounded rectangle, the glass a 6-unit rounded rectangle; everything inside the glass is on the dot grid and has no corners of its own. Lit blocks (route badge, line-number blocks, usage cells) are solid rectangles of dots, and their content is knocked out: the glyph is subtracted from the block, so the dead grid shows through as the letterform.

## Components

### Housing (every display)
Charcoal enclosure, 864 wide, 16-unit radius, 1px housing-edge stroke, the housing-rest shadow, four screws inset 11 at the corners. Contains one glass window and one silkscreen strip. Built by `Display(cols, rows, pitch, title)`.

### Silkscreen Strip
The 50-unit band under the glass. Left label always begins "DSSANTOS TERMINAL  ·  " followed by the display's role (ROUTE >_, PLATFORM 1  ·  DEPARTURES, SERVICE UPDATES, TERMINUS). An optional right label is a model or status line; when present it is preceded by the blinking live pip, 4 silkscreen dots to its left. Left label aligns with the matrix's left edge, right label with its right edge.

### Destination Sign
205 x 36 at pitch 4. Left: the route badge. Right: a 2x destination that hard-cuts between two pages (A for 6s, B for 3s of a 9s cycle) above a 1x via ticker on row 24. Right label "PIS-01  ·  GTFS-RT LIVE" with the live pip.

### Route Badge
A lit block 28 dots tall from row 3, with the bold 3x ">" and "_" knocked out and 5 dots of lit padding around them. The cursor blinks by filling its own hole back in (1.1s, off for the first 55%).

### Departures Board
273 x 134 at pitch 3. Header "Destination  ·  calling at" at column 18 and "Usage" right-aligned, dotted separator, then five lines. Each line: a line-number block, a bold line name, a calling-at list joined with "  ·  ", and an optional usage bar. Lines without a rating show no bar rather than an invented one.

### Line Number Block
A lit block 13 x 11 dots (columns 1-13, from 2 rows above the title) with the bold numeral knocked out and centred.

### Usage Bar
Twelve cells, each 3 x 7 dots with a 1-dot gutter, right-aligned on the title row. Filled cells are lit full height; empty cells keep only their baseline row lit, so the scale stays readable. The value is a self-rating out of 12.

### Platform Console
205 x 70 at pitch 4, directly under the departures board. The prompt "DSSantos.Terminal>" types `dotnet run` one key every 0.09s behind a 4 x 7 block cursor, holds a beat for Enter, then prints a .NET-style startup log one line at a time (11-dot line pitch; the GTFS feed load is the slow line). The cursor then blinks after "info: Ready. Mind the gap" until the 11.6s cycle restarts. Each moment is its own keyframe window on one shared clock. The still frame is the finished log. Right label "DOTNET RUN" with the live pip.

### Service Updates Board
273 x 80 at pitch 3. Header "Next departures" / "Expected", separator, two entries (ordinal, bold name, body note, bold right-aligned status), a second separator at row 64, and a full-width service-information ticker on row 69. An imminent status flashes (1.6s blink).

### Terminus Sign
205 x 36 at pitch 4, wrapped in the LinkedIn link. "Terminus" at 2x top-left, bold 1x "All change" and "LinkedIn ▸" right-aligned, a ticker on row 24 whose still frame is the LinkedIn handle. Right label "EXIT CODE 0" with the live pip.

### Ticker
Text scrolls right to left through a clipped window, one dot per step: `steps(window + text width)` over `(window + text width) / 30` seconds, started with a negative delay so the window is already full. Each ticker carries a still line that must fit the window; it is shown when animation does not run and hidden by a 0.01s animation when it does.

### Adding a New Display
- Add a builder function in `scripts/build_displays.py`, register it in `main()`, and regenerate; never hand-edit an SVG.
- Choose the form: a sign (pitch 4, 205 columns) for one big message, a board (pitch 3, 273 columns) for rows of information. Height is the only free dimension.
- Label the silkscreen "DSSANTOS TERMINAL  ·  <ROLE>". Add a right label and live pip only if the display reports something genuinely live or in service.
- Lay out on the board grid: header at row 2, separator at row 12, entries from row 16 on a 24-dot stride; route every string through `check_fits`.
- Give every ticker a still line that carries the essential information, and write the full message into the alt text.
- Reuse the existing motion classes (pa/pb, ci, fl, pip) rather than inventing new timings.

## Do's and Don'ts

### Do:
- **Do** draw every character with the 5x7 face, adding glyphs to `FONT_SRC` as bitmaps when needed.
- **Do** keep the dead LED grid visible behind every lit layer.
- **Do** move text only in whole-dot steps (steps() timing, 30 dots/s) and change pages by hard cut.
- **Do** make every display complete with animation off: the still line, page A and the knocked-out cursor are the reduced-motion frame.
- **Do** put the information of every display in its alt text and `<title>`.
- **Do** knock content out of lit blocks (route badge, line numbers) instead of using a second colour.

### Don't:
- **Don't** add a second LED colour, a gradient, or any glow or blur on the dots.
- **Don't** use live green for anything except a real live or in-service pip.
- **Don't** use fractional scales or set any text inside the glass below pitch 3 at 1x.
- **Don't** add eased, smooth or sub-dot motion; no fades between pages.
- **Don't** add shields-style badges, stats cards or typing-SVG headers; the komarev visitor counter is a retained product requirement, not a pattern to extend.
- **Don't** pad a board with invented facts or ratings; an unknown is shown as "Soon" or omitted.
