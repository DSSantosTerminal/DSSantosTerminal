#!/usr/bin/env python3
"""Draws the LED passenger information displays used in README.md.

Every glyph is a hand-set 5x7 dot-matrix bitmap (with descenders), and every
lit LED is a zero-length path segment with a round cap. Scrolling text moves
in whole-dot steps, the way real PIS firmware does it.

    python scripts/build_displays.py      # writes assets/*.svg
"""
import re
from html import escape
from pathlib import Path
from urllib.request import urlopen

OUT = Path(__file__).resolve().parent.parent / "assets"
# The README counts visits with komarev's invisible pixel; this reads the total.
COUNTER = "https://komarev.com/ghpvc/?username=DSSantosTerminal&style=flat"

LED_ON = "#FFB000"
LED_OFF = "#2A1E06"
GLASS = "#0B0A08"
HOUSING = "#1B1B19"
HOUSING_EDGE = "#34332E"
SILKSCREEN = "#9A968A"
LIVE = "#3DDC84"

WIDTH = 880
SCROLL_SPEED = 30  # dots per second

# ---------------------------------------------------------------------------
# Font: '#' is a lit LED. Rows 0-6 sit above the baseline, rows 7-8 descend.
# Glyphs are trimmed to their lit columns, so the face is proportional.
# ---------------------------------------------------------------------------
FONT_SRC = {
    "A": ".###. #...# #...# #...# ##### #...# #...#",
    "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.",
    "D": "###.. #..#. #...# #...# #...# #..#. ###..",
    "E": "##### #.... #.... ####. #.... #.... #####",
    "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .####",
    "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": "### .#. .#. .#. .#. .#. ###",
    "J": "..### ...#. ...#. ...#. ...#. #..#. .##..",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    "N": "#...# #...# ##..# #.#.# #..## #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.",
    "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#",
    "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.",
    "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.",
    "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.",
    "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    "a": "..... ..... .###. ....# .#### #...# .####",
    "b": "#.... #.... #.##. ##..# #...# #...# ####.",
    "c": "..... ..... .###. #.... #.... #...# .###.",
    "d": "....# ....# .##.# #..## #...# #...# .####",
    "e": "..... ..... .###. #...# ##### #.... .###.",
    "f": "..##. .#..# .#... ###.. .#... .#... .#...",
    "g": "..... ..... .#### #...# #...# #...# .#### ....# .###.",
    "h": "#.... #.... #.##. ##..# #...# #...# #...#",
    "i": ".#. ... ##. .#. .#. .#. ###",
    "j": "...# .... ..## ...# ...# ...# ...# #..# .##.",
    "k": "#.... #.... #..#. #.#.. ##... #.#.. #..#.",
    "l": "##. .#. .#. .#. .#. .#. ###",
    "m": "..... ..... ##.#. #.#.# #.#.# #...# #...#",
    "n": "..... ..... #.##. ##..# #...# #...# #...#",
    "o": "..... ..... .###. #...# #...# #...# .###.",
    "p": "..... ..... ####. #...# #...# #...# ####. #.... #....",
    "q": "..... ..... .#### #...# #...# #...# .#### ....# ....#",
    "r": "..... ..... #.##. ##..# #.... #.... #....",
    "s": "..... ..... .###. #.... .###. ....# ####.",
    "t": ".#... .#... ###.. .#... .#... .#..# ..##.",
    "u": "..... ..... #...# #...# #...# #..## .##.#",
    "v": "..... ..... #...# #...# #...# .#.#. ..#..",
    "w": "..... ..... #...# #...# #.#.# #.#.# .#.#.",
    "x": "..... ..... #...# .#.#. ..#.. .#.#. #...#",
    "y": "..... ..... #...# #...# #...# #...# .#### ....# .###.",
    "z": "..... ..... ##### ...#. ..#.. .#... #####",
    "ç": "..... ..... .###. #.... #.... #...# .###. ..#.. .##..",
    "ã": ".##.# #..#. .###. ....# .#### #...# .####",
    "0": ".###. #...# #..## #.#.# ##..# #...# .###.",
    "1": ".#. ##. .#. .#. .#. .#. ###",
    "2": ".###. #...# ....# ...#. ..#.. .#... #####",
    "3": "##### ...#. ..#.. ...#. ....# #...# .###.",
    "4": "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    "5": "##### #.... ####. ....# ....# #...# .###.",
    "6": "..##. .#... #.... ####. #...# #...# .###.",
    "7": "##### ....# ...#. ..#.. .#... .#... .#...",
    "8": ".###. #...# #...# .###. #...# #...# .###.",
    "9": ".###. #...# #...# .#### ....# ...#. .##..",
    ".": ". . . . . . #",
    ",": ".. .. .. .. .. .# #.",
    ":": ". . # . . # .",
    "-": ".... .... .... #### .... .... ....",
    "_": "..... ..... ..... ..... ..... ..... #####",
    "/": "..... ....# ...#. ..#.. .#... #.... .....",
    "#": ".#.#. .#.#. ##### .#.#. ##### .#.#. .#.#.",
    "+": "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    "=": "..... ..... ##### ..... ##### ..... .....",
    ">": "#... .#.. ..#. ...# ..#. .#.. #...",
    "$": "..#.. .#### #.#.. .###. ..#.# ####. ..#..",
    "(": "..# .#. #.. #.. #.. .#. ..#",
    ")": "#.. .#. ..# ..# ..# .#. #..",
    "'": "# # . . . . .",
    "!": "# # # # # . #",
    "&": ".##.. #..#. #.#.. .#... #.#.# #..#. .##.#",
    "·": ".. .. .. ## ## .. ..",
    "—": "...... ...... ...... ###### ...... ...... ......",
    "▸": ".... #... ##.. ###. ##.. #... ....",
}
SPACE_WIDTH = 3


def _parse(src):
    rows = src.split()
    lit = {(x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == "#"}
    left = min(x for x, _ in lit)
    right = max(x for x, _ in lit)
    return right - left + 1, {(x - left, y) for x, y in lit}


FONT = {ch: _parse(src) for ch, src in FONT_SRC.items()}


def glyph(ch, bold):
    if ch == " ":
        return SPACE_WIDTH + bold, set()
    width, dots = FONT[ch]
    if bold:
        dots = dots | {(x + 1, y) for x, y in dots}
        width += 1
    return width, dots


def render(text, bold=False, scale=1):
    """Lays out a string. Returns (width in dots, set of lit dots)."""
    x, lit = 0, set()
    for ch in text:
        width, dots = glyph(ch, bold)
        lit |= {(x + gx, gy) for gx, gy in dots}
        x += width + 1
    width = max(x - 1, 0)
    if scale > 1:
        lit = {(x * scale + i, y * scale + j) for x, y in lit for i in range(scale) for j in range(scale)}
    return width * scale, lit


def shift(dots, dx, dy):
    return {(x + dx, y + dy) for x, y in dots}


# ---------------------------------------------------------------------------
# SVG assembly
# ---------------------------------------------------------------------------
def dots_path(dots, cls="", extra=""):
    # Dots further along the same row are relative hops from the previous one.
    parts, prev = [], None
    for x, y in sorted(dots, key=lambda p: (p[1], p[0])):
        parts.append(f"m{x - prev[0]} 0h0" if prev and prev[1] == y else f"M{x} {y}h0")
        prev = (x, y)
    d = "".join(parts)
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<path{cls_attr}{extra} d="{d}"/>'


class Display:
    """A housing with one LED matrix and a silkscreen strip along the bottom."""

    def __init__(self, cols, rows, pitch, title):
        self.cols, self.rows, self.pitch, self.title = cols, rows, pitch, title
        self.pad_x, self.pad_top, self.strip = 22, 22, 50
        self.hx, self.hy = 8, 6
        self.sx = (WIDTH - cols * pitch) / 2
        self.sy = self.hy + self.pad_top
        self.hw = WIDTH - 2 * self.hx
        self.hh = self.pad_top + rows * pitch + self.strip
        self.height = self.hy + self.hh + 16
        self.layers, self.css, self.clips = [], [], []
        self.label_left, self.label_right = "", ""

    def lit(self, dots, cls=""):
        self.layers.append(dots_path(dots, cls))

    def ticker(self, text, still, col, row, width_cols, cls="tk"):
        """Scrolls text right-to-left through a window, one dot per step.

        `still` is what the window shows when nothing animates (reduced motion,
        renderers without CSS animation), so it has to fit the window.
        """
        still_w, still_dots = render(still)
        check_fits(still, still_w, width_cols)
        # The ticker lives inside the matrix group, so everything here is in dots.
        text_w, dots = render(text)
        clip_id = f"clip{len(self.clips)}"
        self.clips.append(
            f'<clipPath id="{clip_id}"><rect x="{col - 0.5:g}" y="{row - 1.5:g}" width="{width_cols:g}" height="11"/></clipPath>'
        )
        steps = width_cols + text_w
        seconds = steps / SCROLL_SPEED
        self.css.append(
            f"@keyframes {cls}{{from{{opacity:1;transform:translateX({width_cols}px)}}"
            f"to{{opacity:1;transform:translateX({-text_w}px)}}}}"
            # A negative delay starts the scroll with text already filling the window.
            f".{cls}{{opacity:0;animation:{cls} {seconds:.1f}s steps({steps}) {-width_cols / SCROLL_SPEED:.2f}s infinite}}"
        )
        self.layers.append(
            f'<g clip-path="url(#{clip_id})"><g class="{cls}">{dots_path(shift(dots, col, row))}</g></g>'
            f'<g class="still">{dots_path(shift(still_dots, col, row))}</g>'
        )

    def svg(self, alt):
        alt = escape(alt)
        p, w = self.pitch, WIDTH
        sx, sy = self.sx, self.sy
        sw, sh = self.cols * p, self.rows * p
        hx, hy, hw, hh = self.hx, self.hy, self.hw, self.hh

        screws = "".join(
            f'<circle cx="{cx:g}" cy="{cy:g}" r="3.2"/>'
            for cx in (hx + 11, hx + hw - 11)
            for cy in (hy + 11, hy + hh - 11)
        )

        label_pitch = 2.6
        label_y = hy + hh - self.strip / 2 - 3.5 * label_pitch
        left_w, left = render(self.label_left)
        right_w, right = render(self.label_right)
        lx = (sx) / label_pitch
        rx = (sx + sw) / label_pitch - right_w
        label_dots = shift(left, round(lx), 0) | shift(right, round(rx), 0)
        pip_x = (round(rx) - 4) * label_pitch
        labels = (
            f'<g transform="translate(0 {label_y:g}) scale({label_pitch})" stroke="{SILKSCREEN}" '
            f'stroke-width=".86" stroke-linecap="square">{dots_path(label_dots)}</g>'
            f'<circle class="pip" cx="{pip_x:g}" cy="{label_y + 3 * label_pitch:g}" r="3.4" fill="{LIVE}"/>'
            if self.label_right
            else f'<g transform="translate(0 {label_y:g}) scale({label_pitch})" stroke="{SILKSCREEN}" '
            f'stroke-width=".86" stroke-linecap="square">{dots_path(label_dots)}</g>'
        )

        css = "".join(self.css) + (
            ".pa{animation:pa 9s infinite}.pb{opacity:0;animation:pb 9s infinite}"
            ".still{animation:hide .01s forwards}@keyframes hide{to{opacity:0}}"
            "@keyframes pa{0%,66.6%{opacity:1}66.7%,100%{opacity:0}}"
            "@keyframes pb{0%,66.6%{opacity:0}66.7%,100%{opacity:1}}"
            ".ci{opacity:0;animation:ci 1.1s infinite}@keyframes ci{0%,54.9%{opacity:0}55%,100%{opacity:1}}"
            ".pip{animation:bl 2.4s infinite}.fl{animation:bl 1.6s infinite}"
            "@keyframes bl{0%,54.9%{opacity:1}55%,100%{opacity:.08}}"
            "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        )

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {self.height:g}" '
            f'width="{w}" height="{self.height:g}" role="img" aria-label="{alt}">'
            f"<title>{alt}</title>"
            f"<style>{css}</style>"
            "<defs>"
            f'<pattern id="off" patternUnits="userSpaceOnUse" x="{sx:g}" y="{sy:g}" width="{p}" height="{p}">'
            f'<circle cx="{p / 2:g}" cy="{p / 2:g}" r="{p * 0.33:g}" fill="{LED_OFF}"/></pattern>'
            '<filter id="sh" x="-5%" y="-10%" width="110%" height="130%">'
            '<feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity=".3"/></filter>'
            + "".join(self.clips)
            + "</defs>"
            f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh:g}" rx="16" fill="{HOUSING}" '
            f'stroke="{HOUSING_EDGE}" filter="url(#sh)"/>'
            f'<g fill="#2B2A26" stroke="#111110" stroke-width=".8">{screws}</g>'
            f'<rect x="{sx - 8:g}" y="{sy - 8:g}" width="{sw + 16:g}" height="{sh + 16:g}" rx="6" fill="{GLASS}" '
            'stroke="#000" stroke-width="1.5"/>'
            f'<rect x="{sx:g}" y="{sy:g}" width="{sw:g}" height="{sh:g}" fill="url(#off)"/>'
            f'<g transform="translate({sx + p / 2:g} {sy + p / 2:g}) scale({p})" stroke="{LED_ON}" '
            f'stroke-width=".74" stroke-linecap="round">' + "".join(self.layers) + "</g>"
            + labels
            + "</svg>\n"
        )


def check_fits(name, used, available):
    if used > available:
        raise SystemExit(f"{name}: needs {used} dots, only {available} available")


# ---------------------------------------------------------------------------
# The displays
# ---------------------------------------------------------------------------
def destination_sign():
    d = Display(cols=205, rows=36, pitch=4, title="destination sign")
    d.label_left = "DSSANTOS TERMINAL  ·  ROUTE >_"
    d.label_right = "PIS-01  ·  GTFS-RT LIVE"

    # Route number: a terminal prompt at 3x, knocked out of a lit route badge.
    # The cursor blinks by filling its hole back in.
    gt_w, gt = render(">", bold=True, scale=3)
    cur_w, cur = render("_", bold=True, scale=3)
    badge_w = gt_w + 3 + cur_w + 10
    badge = {(x, y) for x in range(2, 2 + badge_w) for y in range(3, 31)}
    gt, cur = shift(gt, 7, 7), shift(cur, 7 + gt_w + 3, 7)
    d.lit(badge - gt - cur)
    d.lit(cur, "ci")
    dest_col = 2 + badge_w + 6

    available = d.cols - dest_col - 2
    for text, cls in (("Daniel Santos", "pa"), ("Fullstack Dev", "pb")):
        w, dots = render(text, scale=2)
        check_fits(text, w, available)
        d.lit(shift(dots, dest_col, 3), cls)

    d.ticker(
        "via C# · .NET 10 · React · TypeScript · PostgreSQL · PostGIS · Python · GTFS"
        "   ·   Fullstack developer at OPT — Optimização e Planeamento de Transportes"
        "   ·   Public transit enthusiast   ·",
        "via C# · .NET · React · GTFS",
        dest_col, 24, available,
    )
    alt = (
        "LED bus destination sign. Route: a terminal prompt with a blinking cursor. "
        "Destination: Daniel Santos, Fullstack Dev. Scrolling via: C#, .NET 10, React, TypeScript, "
        "PostgreSQL, PostGIS, Python, GTFS. Fullstack developer at OPT, Optimização e Planeamento "
        "de Transportes. Public transit enthusiast."
    )
    return d.svg(alt)


STACK = [
    ("1", "Backend", "C# · .NET 10 · ASP.NET Core · EF Core", 10),
    ("2", "Database", "PostgreSQL · PostGIS · SQL", None),
    ("3", "Frontend", "React · JavaScript · TypeScript · HTML · CSS", 6),
    ("4", "Data & scripting", "Python · FastAPI", 3),
    ("5", "Tools", "Git · Docker · GitHub Actions · Hangfire · GTFS", None),
]


def separator(cols, row):
    return {(x, row) for x in range(0, cols, 2)}


def departures():
    stride, first = 24, 16
    d = Display(cols=273, rows=first + stride * len(STACK) - 2, pitch=3, title="departures")
    d.label_left = "DSSANTOS TERMINAL  ·  PLATFORM 1  ·  DEPARTURES"
    d.label_right = ""
    cols = d.cols
    text_col = 18

    _, head = render("Destination  ·  calling at")
    d.lit(shift(head, text_col, 2))
    usage_w, head = render("Usage")
    d.lit(shift(head, cols - 1 - usage_w, 2))
    d.lit(separator(cols, 12))

    for i, (num, name, via, load) in enumerate(STACK):
        r = first + i * stride
        # Line number knocked out of a lit block.
        nw, ndots = render(num, bold=True)
        box = {(x, y) for x in range(1, 14) for y in range(r - 2, r + 9)}
        d.lit(box - shift(ndots, 1 + (13 - nw) // 2, r))

        w, dots = render(name, bold=True)
        d.lit(shift(dots, text_col, r))
        w, dots = render(via)
        check_fits(via, text_col + w, cols)
        d.lit(shift(dots, text_col, r + 11))

        if load is not None:
            cells = set()
            start = cols - 1 - (12 * 4 - 1)
            for c in range(12):
                x0 = start + c * 4
                rows = range(r, r + 7) if c < load else range(r + 6, r + 7)
                cells |= {(x, y) for x in range(x0, x0 + 3) for y in rows}
            d.lit(cells)

    alt = "LED departures board, platform 1: the stack as five lines. " + " ".join(
        f"Line {num}, {name}: calling at {via.replace(' · ', ', ')}."
        + (f" Self-rated usage {load} of 12." if load is not None else "")
        for num, name, via, load in STACK
    )
    return d.svg(alt)


def window(start, end, total):
    """Keyframes that light an element only between `start` and `end` seconds."""
    a, b = start / total * 100, end / total * 100
    on = f"{a:.2f}%,{b - 0.01:.2f}%{{opacity:1}}"
    if a == 0:
        return f"{on}{b:.2f}%,100%{{opacity:0}}"
    return f"0%,{a - 0.01:.2f}%{{opacity:0}}{on}{b:.2f}%,100%{{opacity:0}}"


def console():
    """A console that boots the terminal: types `dotnet run`, then prints the log."""
    d = Display(cols=205, rows=70, pitch=4, title="console")
    d.label_left = "DSSANTOS TERMINAL  ·  PLATFORM 1  ·  CONSOLE"
    d.label_right = "DOTNET RUN"
    col, line_pitch = 3, 11

    prompt, command = "DSSantos.Terminal> ", "dotnet run"
    # Each log line is (seconds after the previous one, text). The feed load is
    # the slow one, the way it is in real life.
    log = [
        (0.9, "info: GTFS feed loaded · 5 lines"),
        (0.4, "info: Platform 1 open for boarding"),
        (0.5, "info: Now listening on:"),
        (0.1, "      github.com/DSSantosTerminal"),
        (0.6, "info: Ready. Mind the gap"),
    ]
    rest, key, enter, hold = 0.8, 0.09, 0.4, 7.0
    cursor = {(x, y) for x in range(4) for y in range(7)}

    prompt_w, dots = render(prompt)
    d.lit(shift(dots, col, 3))
    command_col = col + prompt_w + 1
    check_fits(prompt + command, prompt_w + 1 + render(command)[0] + 5, d.cols - 2 * col)

    # Typing: key k lights at its keystroke; the cursor sits after the last key.
    x, moments, still = command_col, [], set()
    for k, ch in enumerate(command):
        moments.append((shift(cursor, x, 3), rest + k * key if k else 0, rest + (k + 1) * key))
        w, dots = glyph(ch, False)
        moments.append((shift(dots, x, 3), rest + (k + 1) * key, None))
        still |= shift(dots, x, 3)
        x += w + 1
    typed = rest + len(command) * key
    moments.append((shift(cursor, x, 3), typed, typed + enter))

    t = typed + enter
    for i, (gap, text) in enumerate(log, start=1):
        t += gap
        w, dots = render(text)
        check_fits(text, w + 5, d.cols - 2 * col)
        dots = shift(dots, col, 3 + i * line_pitch)
        moments.append((dots, t, None))
        still |= dots
    end_w = w
    ready = t
    total = ready + hold

    for i, (dots, start, stop) in enumerate(moments):
        d.css.append(f".m{i}{{opacity:0;animation:m{i} {total:.2f}s infinite}}"
                     f"@keyframes m{i}{{{window(start, stop or total, total)}}}")
        d.lit(dots, f"m{i}")

    # Once the log is done, the cursor blinks at the end of the last line.
    last = len(moments)
    final = shift(cursor, col + end_w + 2, 3 + len(log) * line_pitch)
    d.css.append(f".m{last}{{opacity:0;animation:m{last} {total:.2f}s infinite}}"
                 f"@keyframes m{last}{{{window(ready, total, total)}}}")
    d.layers.append(f'<g class="m{last}">{dots_path(final, "ci")}</g>')
    d.layers.append(f'<g class="still">{dots_path(still | final)}</g>')

    alt = (
        "LED console on platform 1. The prompt DSSantos.Terminal types dotnet run, and the log reads: "
        "GTFS feed loaded, 5 lines. Platform 1 open for boarding. Now listening on github.com/DSSantosTerminal. "
        "Ready. Mind the gap."
    )
    return d.svg(alt)


def service_updates():
    d = Display(cols=273, rows=80, pitch=3, title="service updates")
    d.label_left = "DSSANTOS TERMINAL  ·  SERVICE UPDATES"
    d.label_right = ""
    cols, text_col = d.cols, 22

    _, head = render("Next departures")
    d.lit(shift(head, 1, 2))
    w, head = render("Expected")
    d.lit(shift(head, cols - 1 - w, 2))
    d.lit(separator(cols, 12))

    rows = [
        ("1st", "Ferret", "Details announced on departure", "Soon", "fl"),
        ("2nd", "Unity · game development", "Line U · engineering works in progress", "In build", ""),
    ]
    for i, (ordinal, name, note, status, cls) in enumerate(rows):
        r = 16 + i * 24
        _, dots = render(ordinal)
        d.lit(shift(dots, 1, r))
        _, dots = render(name, bold=True)
        d.lit(shift(dots, text_col, r))
        _, dots = render(note)
        d.lit(shift(dots, text_col, r + 11))
        w, dots = render(status, bold=True)
        d.lit(shift(dots, cols - 1 - w, r), cls)

    d.lit(separator(cols, 64))
    d.ticker(
        "Service information: Line U (Unity, game development) is under construction"
        "   ·   Ferret will be announced on this board   ·   Thank you for travelling with DSSantos Terminal   ·",
        "Service information: Line U under construction",
        1, 69, cols - 2,
    )
    alt = (
        "LED service updates board. Next departures: 1st, Ferret, expected soon, details announced on departure. "
        "2nd, Unity game development, in build, engineering works in progress."
    )
    return d.svg(alt)


def passenger_count():
    """Reads the visit counter, or None when it can't be reached.

    Reading the badge counts as one visit, so this runs once per build.
    """
    try:
        with urlopen(COUNTER, timeout=10) as response:
            badge = response.read().decode()
    except OSError as error:
        print(f"passenger count unavailable ({error}), keeping assets/passengers.svg")
        return None
    return int(re.sub(r"\D", "", re.findall(r"<text[^>]*>([^<]*)</text>", badge)[-1]))


def passengers(count):
    """A ridership odometer. On load each wheel rolls up to its digit."""
    d = Display(cols=205, rows=36, pitch=4, title="passengers")
    d.label_left = "DSSANTOS TERMINAL  ·  RIDERSHIP"
    d.label_right = "UPDATED DAILY"

    digits = f"{count:06d}"
    cell_w, cell_h, gap, top = 19, 27, 2, 4
    x0 = d.cols - 3 - len(digits) * (cell_w + gap) + gap
    for text, row in (("Passengers", 8), ("served", 19)):
        w, dots = render(text, bold=True)
        check_fits(text, 3 + w + 4, x0)
        d.lit(shift(dots, 3, row))

    def wheel_face(n, x, y):
        w, dots = render(str(n), scale=3)
        box = {(i, j) for i in range(x, x + cell_w) for j in range(y, y + cell_h)}
        return box - shift(dots, x + (cell_w - w) // 2, y + 3)

    still = set()
    for i, ch in enumerate(digits):
        x, target = x0 + i * (cell_w + gap), int(ch)
        if target == 0:
            d.lit(wheel_face(0, x, top))
            continue
        # The wheel is the last few faces up to the digit, stacked; it slides up
        # through the cell's window a dot at a time. Higher places stop sooner.
        first = max(0, target - 4)
        faces = range(first, target + 1)
        wheel = set().union(*(wheel_face(n, x, top + k * cell_h) for k, n in enumerate(faces)))
        target -= first
        clip_id = f"clip{len(d.clips)}"
        d.clips.append(
            f'<clipPath id="{clip_id}"><rect x="{x - 0.5:g}" y="{top - 0.5:g}" '
            f'width="{cell_w:g}" height="{cell_h:g}"/></clipPath>'
        )
        steps, seconds = target * cell_h, 0.9 + 0.25 * i
        d.css.append(
            f"@keyframes r{i}{{from{{opacity:1;transform:translateY(0)}}"
            f"to{{opacity:1;transform:translateY({-steps}px)}}}}"
            f".r{i}{{opacity:0;animation:r{i} {seconds:.2f}s steps({steps}) .4s both}}"
        )
        d.layers.append(f'<g clip-path="url(#{clip_id})"><g class="r{i}">{dots_path(wheel)}</g></g>')
        still |= wheel_face(int(ch), x, top)
    d.layers.append(f'<g class="still">{dots_path(still)}</g>')

    alt = f"LED ridership counter: {count:,} passengers served. Updated daily."
    return d.svg(alt)


def terminus():
    d = Display(cols=205, rows=36, pitch=4, title="terminus")
    d.label_left = "DSSANTOS TERMINAL  ·  TERMINUS"
    d.label_right = "EXIT CODE 0"

    w, dots = render("Terminus", scale=2)
    d.lit(shift(dots, 3, 3))
    for text, row in (("All change", 3), ("LinkedIn ▸", 13)):
        tw, dots = render(text, bold=True)
        d.lit(shift(dots, d.cols - 3 - tw, row))
    d.ticker(
        "This service terminates here   ·   Find Daniel on LinkedIn: in/daniel-santos-8bb581169"
        "   ·   process exited with code 0   ·",
        "in/daniel-santos-8bb581169",
        3, 24, d.cols - 6,
    )
    alt = "LED sign: Terminus. All change. Find Daniel on LinkedIn: in/daniel-santos-8bb581169."
    return d.svg(alt)


def main():
    OUT.mkdir(exist_ok=True)
    displays = [
        ("destination-sign", destination_sign),
        ("departures", departures),
        ("console", console),
        ("service-updates", service_updates),
        ("terminus", terminus),
    ]
    count = passenger_count()
    if count is not None:
        displays.append(("passengers", lambda: passengers(count)))
    for name, build in displays:
        svg = build()
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"assets/{name}.svg  {len(svg.encode()) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
