# Changelog

All notable changes to this plugin are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-09-15

### Added
- Initial release of the **architecture-from-codebase** plugin and skill.
- **Methodology** (`SKILL.md`): the reverse-engineering loop — orient → investigate (targeted grep batches) → draft + diagram → assemble incrementally → validate — plus a section menu, observed-vs-inferred provenance rules, and a validation checklist.
- **Annotated sequence-diagram engine** (`scripts/seqgen.py`): participants/actors, solid-call and dashed-return arrows, self-calls, `alt`/`else`/`loop` fragments, notes, and numbered annotation cards with leader lines. Importable as `Seq`; runnable standalone for a demo.
- **Reference guides**:
  - `references/design-system.md` — palette, fonts, copy-paste CSS building blocks, and GitHub source-link URL construction.
  - `references/diagram-recipes.md` — recipes for block/ER/funnel/lane/matrix/terminal-trace/worked-example diagrams, the cairosvg PNG-QA workflow (with the two blank-render gotchas), and HTML/f-string escaping rules.
- **Sample diagrams** under `examples/images/` (annotated sequence diagram, layered map).
- `README.md` (positioning + install + usage), `LICENSE` (MIT), and `.gitignore`.

[0.1.0]: https://github.com/YOUR_HANDLE/architecture-from-codebase/releases/tag/v0.1.0
