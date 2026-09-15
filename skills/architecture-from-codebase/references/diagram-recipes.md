# Diagram recipes & QA

All diagrams are **hand-authored inline SVG** (self-contained, fully controllable annotations). Use the palette/fonts from `design-system.md`. This file gives the recipe per diagram type and the QA workflow that catches the common failures.

## Contents
- Sequence diagrams (bundled engine)
- Block / layered map
- ER diagram
- Funnel / composition
- Lane / responsibilities
- Matrix / gate ladder
- Terminal trace
- Worked-example (trace + composition)
- Numbered annotation cards (the reusable pattern)
- QA: rasterize & view (the two cairosvg gotchas)
- Escaping gotchas

## Sequence diagrams — use the bundled engine

`scripts/seqgen.py` provides a `Seq` class. Import it; don't reinvent it.

```python
from seqgen import Seq
s = Seq([("U","User"),("Core","core"),("API","model")], actors={"U"},
        annotations=[(1,"why this step matters"), (3,"...")])   # (msg_index, note)
s.msg("U","Core","prompt")               # solid call
s.msg("Core","API","request", )          # call
s.frag("alt fast path"); s.msg("API","Core","cached", ret=True)  # dashed return
s.alt("else slow path"); s.msg("API","Core","stream", ret=True); s.endfrag()
s.selfmsg("Core","compact")              # self-loop
s.note(["Core","API"],"a spanning note")
open("out.svg","w").write(s.render())
```

It supports: actor vs service boxes, dashed lifelines, solid-call/dashed-return arrows with arrowheads, `alt/else/loop` fragment boxes with labelled tabs, notes, and **right-margin numbered annotation cards with dashed leader lines**. `annotations` indices count `msg`+`selfmsg` in call order starting at 0 — verify against the render (a miscount points a card at the wrong step). Also render one **holistic** sequence that composes the individual flows, with annotations that cross-reference the detailed sections.

## Block / layered map (HTML, not SVG)

Prefer HTML `<div>` bands + chips so it reflows on mobile. Pattern: stacked `.band` boxes (interfaces → protocol/core → subsystems → external), each with a mono uppercase tag, a name, and a row of `.chip` spans naming the real modules. Use a dashed border for a remote/external band and an amber-tinted band for the safety layer. Add a `.xcut` band for cross-cutting concerns (config, auth, state, observability). Revisit this map at the very end — it always needs updating once deep-dives are done.

## ER diagram (SVG, from real schema)

Build from actual migrations/DDL. Each entity = a box with a coloured header + attribute rows; mark primary keys with `•` and foreign keys with `▸`. Draw relationship connectors between edges with a small dot at the source and a `1..1` / `1..∞` cardinality label placed *outside* the target box. Put the central table in the middle with satellites around it. Include a "source of truth vs projection" note if the store is derived (e.g. an append-only log projected into a DB). Keep ~4–6 attributes per box; footer legend: `• = PK  ▸ = FK`.

## Funnel / composition (SVG)

Sources on the left as coloured chips → cubic-bezier connectors converging into a central bar (e.g. "context window") → arrow to a target ("model"). Colour connectors by category and add a legend. Good for "what flows into X."

## Lane / responsibilities (SVG)

N side-by-side panels (e.g. Harness / Agent / Model, or Deterministic / Semantic) with a coloured header and bulleted duties, plus a handoff arrow between panels. Answers "who does what."

## Matrix / gate ladder (SVG)

For guardrails/permissions: a left "entry" node branching into category lanes, each showing the gate chain it must pass (as small pill chips). Or a true category × gate grid. Answers "what's allowed / what's checked."

## Terminal trace (SVG)

A dark rounded panel styled like a terminal (three traffic-light dots, a muted right-label). Rows are `(tag, text)`: a coloured tool tag (e.g. `shell`, `search`, `patch`) + a mono command in light text, or a muted output line. Attach numbered side-note cards (leader lines) that name the mechanic each command demonstrates. Excellent for walking through CLI / agentic / tool-driven behavior step by step.

## Worked-example (SVG)

A user query banner on top; a numbered retrieval/action **trace** on the left (each step: coloured badge + action + mechanism tag); a stacked **composition bar** on the right (segments = what got assembled, with a reserved/"freed" region shown hatched or dashed). Pair a detailed one as the explainer and compact variants for comparisons.

## Numbered annotation cards (the reusable pattern)

The thing that lifts a diagram from decorative to explanatory: reserve a right margin (~240px), and for each key element draw a small card `fill:#f6fbfc; stroke:teal`, a teal number circle, wrapped text, and a dashed teal leader line from the element to the card. Stack cards so they don't overlap: `cy = max(target_y - h/2, last_bottom + gap)`. The bundled `Seq` does this for sequences; replicate it for other diagram types.

## QA: rasterize & view — do this for EVERY diagram before wiring it in

```python
import cairosvg, re
svg = open("out.svg").read().replace(' style="max-width:100%;height:auto;display:block"','')  # GOTCHA 1
m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg); w,h = int(m.group(1)), int(m.group(2))
cairosvg.svg2png(bytestring=svg.encode(), write_to="out.png",
                 output_width=w, output_height=h, background_color="white")            # GOTCHA 2
```
Then open `out.png` with the image viewer and actually look at it. Fix overlaps/clipping, re-render, re-check.

- **Gotcha 1:** cairosvg renders a **blank** PNG if the root `<svg>` keeps `style="...height:auto..."`. Strip that style attribute *for the PNG only* — keep it in the artifact so the SVG is responsive there.
- **Gotcha 2:** always pass explicit `output_width`/`output_height` (from the viewBox); relying on the intrinsic size can also yield blank/mis-sized output.
- Install once with `pip install cairosvg --break-system-packages -q`.

Common visual fixes: pad the first row inside a fragment; size note boxes by wrapped line count; give dynamic height to step boxes; widen text wrap so labels don't split awkwardly.

## Escaping gotchas

- **In HTML** (including inside SVG text, which is XML): write `&amp;`, `&lt;`, `&gt;`. A raw `<Generic>` breaks HTML; a raw `&` breaks SVG XML (blank render). Don't double-escape (`&amp;amp;`): if a string already contains an entity, don't run it through an HTML-escaper again.
- **In Python f-strings** used to build SVG/HTML: double any literal braces the text contains — `Prompt {{ input, tools }}`, `path/{{enroll,pair}}` — or the f-string will try to evaluate them.
- **Assembly:** build the big HTML with small string replacements/inserts + validation after each step (see SKILL.md). Keep `count('class="figure"') == count('<svg')`.
