---
name: architecture-from-codebase
description: Reverse-engineer any codebase into a polished, self-contained HTML architecture reference — with hand-rendered annotated SVG diagrams (sequence, block, ER, flow, matrix), a navigable table of contents, per-section GitHub source links, and honest "observed vs inferred" provenance. Use this whenever the user wants to understand, document, diagram, or "reverse engineer" how a repository works; produce an architecture document, design doc, system map, or technical walkthrough of a codebase; onboard onto an unfamiliar repo; or turn source code into design documentation — even if they never say the word "skill", "architecture", or "diagram" explicitly. Prefer this over ad-hoc prose whenever the deliverable is "explain/map/document how this code/system is built."
---

# Architecture from a codebase

Turn a source repository into a single, self-contained HTML architecture reference: layered map + tech stack + annotated sequence diagrams + subsystem deep-dives + design rationale, every claim grounded in the actual code and linked back to it.

## What you produce

- **One self-contained `.html` file** (no CDN, no runtime `<script>`) so it renders offline forever. All diagrams are **inline SVG**.
- **A design system** applied consistently (see `references/design-system.md`): cool paper background, ink text, one teal accent, amber reserved for safety/security, monospace only for code identifiers.
- **Hand-rendered annotated diagrams** — never Mermaid or a CDN renderer. Use the bundled `scripts/seqgen.py` for sequence diagrams; use the recipes in `references/diagram-recipes.md` for block/ER/flow/matrix/"terminal-trace" diagrams. Annotations (numbered callout cards with leader lines) are what make these worth more than boxes-and-arrows.
- **A table of contents** and numbered sections (`NN / LABEL`).
- **Per-section "Source ↗" links** to the real files/dirs on the repo host, so the reader can trace every claim.

## The loop

Work **incrementally**, one section at a time. Do not try to write the whole document in one pass.

1. **Orient** — clone shallow, map the top level, identify the build system, language(s), entry points, and the ~dozen most important modules/crates/packages. Read the repo's own `README` / `AGENTS.md` / `docs/`.
2. **Investigate** — for the section you're building, run **targeted grep batches** for the load-bearing types and patterns (enums, structs, traits, key function names, constants). Read a *slice*, not the whole file. Verify every claim against the code.
3. **Draft + diagram** — write the prose for that section and generate its diagram(s). QA each SVG by rasterizing to PNG and viewing it (see recipes) before wiring it in.
4. **Assemble** — insert the section into the HTML with small, surgical string edits (a Python script that reads the file, does targeted replacements, inserts the block, renumbers, updates the TOC). **Validate after every assembly** (below).
5. **Present + iterate** — show the artifact, take feedback, add/deepen sections. Each new user question is usually a new subsection or section.

Start with a skeleton (hero title block + TOC + the layered map), then grow it. Revisit the layered map at the end — early maps under-represent what later investigation reveals.

## Investigation technique

- **Grep for the skeleton, not the flesh.** The architecture lives in enums (`grep -rhoE 'SomeEnum::[A-Za-z]+'`), struct/trait definitions, central constants (limits, timeouts, budgets), and a few function names. A handful of well-aimed greps beats reading files top to bottom.
- **Batch related greps** in one command to save round-trips.
- **Trace the central pattern first.** Most systems have one organizing idea (a message protocol, an event loop, a plugin registry, a pipeline). Find it early; it explains everything else.
- **Confirm before asserting.** If you're about to claim a value (a cap, a default, a model name), grep for it. If a file/dir you want to link doesn't exist, don't link it — verify paths before writing `Source ↗` links.
- **Never invent.** If the code doesn't show it, say so or leave it out.

## Honesty & provenance (non-negotiable)

Reverse-engineering mixes fact and interpretation. Keep them visibly separate:

- **Observed** — names, types, values quoted from the tree. State them plainly.
- **Inferred** — pattern names (e.g. "this reads as hexagonal"), *rationale*, and *trade-offs*. Label them as interpretation ("reads as…", "the likely reason…"). A "Rationale/Decisions" section's trade-off column is almost entirely interpretation — say so.
- **Illustrative** — example traces, token proportions, sample data. Mark them "illustrative, not measured/captured."
- **Scope boundaries** — call out what lives *outside* the repo (e.g. server-side training, hosted services) rather than implying the repo does it.
- Put a one-line provenance note (which crates/files a section came from) near each section, in addition to the `Source ↗` links.

## Section menu

Pull from this menu per codebase — not every repo needs every section, and order/naming should fit the system. A typical order:

1. **Layered map** — a top-to-bottom block diagram of the layers (interfaces → protocol/core → subsystems → external), with cross-cutting concerns.
2. **Tech stack** — grouped by concern (language/build, async, networking, persistence, security, observability…).
3. **Commentary / "one request, ball by ball"** — a prose play-by-play of the main request path.
4. **Sequence diagrams (flows)** — the key paths as annotated sequence diagrams, plus one **holistic** diagram that composes them.
5. **Subsystem deep-dives** — one section per major subsystem the codebase has (e.g. agents, retrieval, caching/compaction, model/provider selection, tools, state, plugins…). Give each: what it is, a diagram, the mechanism, and its source links.
6. **State & persistence** — an **ER diagram** from the real schema/migrations; note the source-of-truth vs projections.
7. **Design principles** — the values (the "why").
8. **Design patterns (deep)** — recurring structures, each explained generically *and* as-applied, with the trade-off.
9. **Rationale / decisions** — tables of architecture / design / tech decisions, each with **Rationale** and **Trade-off** columns.
10. **External/backend interactions** — what crosses the network, endpoints, trust boundary.
11. **Deployment / runtime topology** — artifacts, distribution, process constellation.

For any subsystem, a strong deep-dive answers: **what it is → a diagram → the mechanism (with real type/const names) → guardrails/limits → source links.** Tables are excellent for catalogs (tools, entities, decisions) — use them when the user asks for a table or when the content is a comparison across a fixed set.

## Diagram toolkit

Read `references/diagram-recipes.md` before making non-sequence diagrams. Quick guide:

- **Sequence diagram** → use `scripts/seqgen.py` (`Seq` class). Supports participants, actors (dark boxes), solid calls / dashed returns, self-calls, `alt/else/loop` fragments, notes, and **numbered annotation cards with leader lines**. Import it; don't rewrite it.
- **Block / layered map** → HTML `<div>` bands with chips (CSS, not SVG) so it reflows; or an SVG hub-and-spoke.
- **ER diagram** → SVG entity boxes (header + PK `•` / FK `▸` rows) with crow's-foot-ish connectors and `1..∞` labels. Build from real migrations/schema.
- **Funnel / composition** → sources converging into a target (context assembly, retrieval mix).
- **Lane / responsibilities** → N columns (who does what) with a handoff arrow.
- **Matrix / gate ladder** → categories × gates, for guardrails/permissions.
- **"Terminal trace"** → a dark mock-terminal panel of commands + outputs with side-note callouts; ideal for walking through CLI/agentic behavior.
- **Worked-example** → a numbered trace beside a composition bar.

Every diagram: match the design tokens, keep the SVG responsive (`style="max-width:100%;height:auto"`), and **QA it as a PNG first** (cairosvg — see recipes for the two gotchas that make it render blank).

## Assembly & validation

Build the HTML with Python string surgery (read file → replace/insert → write), not by hand-editing a giant file. After **every** assembly step, check:

- **Figure/SVG balance** — count of `class="figure"` equals count of `<svg` (a mismatch means a broken insert).
- **No stray `<script>`** and no `mermaid` runtime (self-containment).
- **Section order & TOC** — numbers are contiguous and the TOC matches.
- **Cross-references survive renumbering.** Inserting a section renumbers later ones. Prefer **name-based** cross-refs ("see the Patterns section") over numeric ("§14") so they don't rot. If you must renumber, grep for `§NN` first and fix every one; insert new sections *after* the highest already-referenced number when possible.
- **Escaping** — inside HTML, write `&amp;`, `&lt;`, `&gt;` (a raw `<Type>` breaks rendering; a raw `&` breaks XML in SVG). In Python f-strings, double literal braces (`{{ }}`) when the text contains `{` or `}`.

Then `present_files` the HTML so the user gets a real artifact card.

## Gotchas learned (read `references/diagram-recipes.md` for fixes)

- **cairosvg renders blank** unless you strip the root `style="max-width:100%..."` and pass explicit `output_width`/`output_height`. Keep that style attr in the *artifact* (for responsiveness); strip it only for local PNG QA.
- **Sequence-diagram crowding** — the first message inside an `alt`/`else` fragment collides with the fragment label unless you pad; a multi-line note needs height proportional to its line count. (Fixed in the bundled engine.)
- **Annotation alignment** — annotation indices count `msg`+`selfmsg` calls; miscounting points a callout at the wrong step. Verify against the render.
- **Renumbering breaks `§NN` prose refs** — see validation above.

## Deliver

The primary deliverable is the single HTML artifact. Offer, as follow-ups: a companion pattern→source-file map, a slide deck / guided-tour HTML built from the same diagrams, or a narration script. Do **not** offer AI-avatar/talking-face video generation — that capability isn't available and is out of scope.
