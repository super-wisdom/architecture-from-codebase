# Design system & HTML building blocks

Apply these consistently so the document reads as one intentional artifact, not a template. Read this before writing the HTML shell or any SVG.

## Palette (CSS variables)

```css
:root{
  --paper:#EDF1F5;   /* cool light background (add a faint grid) */
  --ink:#111C29;     /* primary text */
  --ink-soft:#42556A;/* secondary text */
  --panel:#0D1826;   /* dark hero / terminal */
  --panel-2:#16273B; /* dark actor boxes / banners */
  --line:#C4CFDA; --line-soft:#DBE2EA;
  --teal:#0F7788; --teal-br:#25A7BA; --teal-d:#0b5460;  /* the one accent */
  --amber:#BC5824;   /* RESERVED for safety/security/danger only */
  --chip:#FFFFFF;
}
```

SVG-side constants (mirror the above): ink `#111C29`, soft `#42556A`, teal `#0F7788`, teal-dark `#0b5460`, line `#C4CFDA`, panel `#16273B`, amber `#BC5824`, grey `#8494a3`, purple `#6b5ca6`, slate `#5b6b7d`, muted `#6f8ea0`.

Colour discipline: **teal = the accent; amber = safety/danger only.** Use purple/slate/grey/muted for categorical distinctions (e.g. retrieval types, item kinds). Never let colour alone carry meaning — always label.

## Fonts

`Space Grotesk` (headings), `Inter` (body), `IBM Plex Mono` (code identifiers only). Load via Google Fonts `<link>` in the HTML head; in SVG use `font-family="'Inter','Segoe UI',system-ui,sans-serif"` and `'IBM Plex Mono',monospace` so raster/PNG QA still looks right.

## The HTML shell

- **Hero "title block"** — an engineering drawing-title feel: dark panel, mono kicker, big title, a grid of key facts (repo, language, build, central pattern, ships-as).
- **TOC nav** — `.toc` with `<a>` links whose `.n` is the mono teal section number.
- **Section header** — `<h2 id="slug"><span class="sec-num">NN / LABEL</span>Title</h2><hr class="rule">`. `.sec-num` is small teal mono.
- **Figure wrapper** — put every inline SVG in `<div class="figure">…</div>` (bordered, rounded, white, `overflow-x:auto`; `svg{max-width:100%;height:auto}`). Optional `<p class="figcap">` for provenance.
- **Source links** — end each section with:
  ```html
  <div class="srcs"><div class="lt">Source ↗ github.com/OWNER/REPO</div>
    <a href="URL" target="_blank" rel="noopener">path/to/file_or_dir</a> … </div>
  ```

## Reusable component CSS (copy into the shell `<style>`)

```css
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:'Inter',system-ui,sans-serif;
  line-height:1.6;font-size:16px;
  background-image:linear-gradient(rgba(120,140,160,.06) 1px,transparent 1px),
    linear-gradient(90deg,rgba(120,140,160,.06) 1px,transparent 1px);background-size:26px 26px;}
.wrap{max-width:960px;margin:0 auto;padding:22px 18px 90px;}
h2{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:1.5rem;margin:54px 0 4px;scroll-margin-top:14px;}
h3{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:1.08rem;margin:26px 0 6px;}
.sec-num{color:var(--teal);font-family:'IBM Plex Mono',monospace;font-size:.9rem;font-weight:600;display:block;margin-top:8px;}
.rule{height:1px;background:var(--line);border:0;margin:6px 0 0;}
code,.mono{font-family:'IBM Plex Mono',monospace;font-size:.86em;}
.figure{margin:16px 0 6px;border:1px solid var(--line);border-radius:11px;background:#fff;padding:14px;overflow-x:auto;}
.figure svg{display:block;margin:0 auto;max-width:100%;height:auto;}
.figcap{color:var(--ink-soft);font-size:.8rem;margin:10px 2px 0;}
.toc{margin:20px 0 0;border:1px solid var(--line);border-radius:9px;background:var(--chip);padding:13px 15px;}
.toc .lt{font-family:'IBM Plex Mono',monospace;font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft);margin-bottom:9px;}
.toc a{display:inline-block;margin:3px 14px 3px 0;font-size:.9rem;color:var(--ink);text-decoration:none;border-bottom:1px solid transparent;}
.toc a:hover{border-color:var(--teal);color:var(--teal);}
.toc a .n{font-family:'IBM Plex Mono',monospace;color:var(--teal);font-size:.78rem;margin-right:5px;}
.srcs{margin:20px 0 2px;border:1px solid var(--line);border-radius:9px;background:#fbfcfd;padding:11px 14px;}
.srcs .lt{font-family:'IBM Plex Mono',monospace;font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);margin-bottom:8px;}
.srcs a{display:inline-block;margin:3px 14px 3px 0;font-size:.8rem;color:var(--teal);text-decoration:none;font-family:'IBM Plex Mono',monospace;border-bottom:1px solid transparent;}
.srcs a:hover{border-color:var(--teal);}
.srcs a::before{content:"\2197 ";opacity:.55;}
/* tables (catalogs, entity roles, decision rationale) */
.etbl{width:100%;border-collapse:collapse;margin-top:14px;font-size:.85rem;}
.etbl th,.etbl td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;}
.etbl th{background:#eef6f7;font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:.78rem;}
.etbl tr:nth-child(even) td{background:#fafcfd;}
.etbl tr.grp td{background:#eef6f7;font-family:'Space Grotesk',sans-serif;font-weight:700;color:var(--teal);}
.etbl td .mono{color:var(--teal-d);}
/* principle / callout cards */
.pr{background:#fff;border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:0 8px 8px 0;padding:12px 14px;margin:10px 0;}
```

## Source-link URL construction

```python
def gh_url(repo_path):            # repo_path relative to repo root
    seg = repo_path.rstrip('/').split('/')[-1]
    kind = 'blob' if ('.' in seg) else 'tree'   # file → blob, dir → tree
    return f'https://github.com/OWNER/REPO/{kind}/main/{repo_path}'
```

Link **files and directories on the default branch — never line numbers** (they rot). Verify each path exists in the clone before emitting the link.
