---
version: 1
slug: "readme-md"
primary_target: "README.md"
related_targets: []
---

# Surface: GitHub profile README

Scope: README.md plus generated display SVGs in assets/. Visitor mode: Experience (a profile/portfolio, where the work leads).
Audience: recruiters, developers and transit people equally. Job: know who Daniel is, what he builds, and how to reach him, within seconds.
Constraints: GitHub-sanitized Markdown, no CSS or JS on the page; all motion lives inside the SVGs; must read fully when static or under reduced motion.

## Direction contract

THESIS: The profile is a run of passenger information displays, the hardware Daniel's own software feeds. Every letter is lit dots (bits) and every board is a terminal. It refuses the category default of a typing-SVG header plus shields badge grid plus stats cards.

OWN-WORLD: Amber LED (#FFB000) dot matrix on black glass, with unlit LEDs visible as a dim amber grid. Charcoal display housings carry square-pixel silkscreen labels in the same 5x7 face. Green appears only as a "live / in service" pip. No glow, no gradients, no badges. One hand-authored 5x7 dot-matrix face (proportional, with descenders, a bold variant and integer scaling) is used for everything.

STORY: The visitor reads the bus destination sign (who), then the platform departures board (what he builds: five lines of stack, with self-rated load bars), then the service updates (Ferret soon, Unity in build), and finally the terminus (LinkedIn, passengers served).

FIRST VIEWPORT: A full-width bus destination sign. The left route number is a 3x terminal prompt ">_", knocked out of a lit route badge, with a blinking cursor. The right destination block alternates "Daniel Santos" / "Fullstack Dev" in 2x. A 1x "via" ticker steps across the bottom one dot at a time. Housing silkscreen reads DSSANTOS TERMINAL, with a green LIVE pip. Right under it sit the about prose and the LinkedIn link.

FORM: LED passenger information display, from my ordered list (position 1 of 7, taken as IMPECCABLE'S PICK; the roll assigned 3). Seed key 4ef04187. Signature motion: dot-pitch stepped scrolling (steps() timing) plus hard-cut page alternation, like real PIS firmware.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
