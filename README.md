# Laptop specs quick reference

Interactive spec sheets for used-laptop hunting on eBay / Facebook Marketplace / Mercari.
Live at **https://regular-2000.github.io/laptop-specs/**

Covers **Dell Latitude**, **Lenovo ThinkPad** (incl. IBM era), **HP business laptops**
(ProBook / EliteBook / Dragonfly / ZBook) and — since Oct 2026 — the rugged brands
**Getac** and **Panasonic Toughbook** (separate pages; may be merged later), and — since Nov 2026 — **Dell Precision** mobile workstations (own page, GPU + screen options). Per model: RAM type & max, upgradeability
(soldered vs SODIMM), storage interfaces, Windows 11 eligibility, typical shipped OS,
typical eBay sold price, a photo and a link to the official spec page.

## Project goal

> **~99% of legit model numbers should be searchable on the page in some shape or form.**
> Enter a real model number in search and something should light up — its own chip, a
> grouped chip ("T480 / T480s / T580"), or a hidden alias (e.g. "X1 Yoga Gen 3" matches
> the X1 Carbon Gen 6 row, its platform twin). A few exotic exceptions (X1 Fold…) are
> acceptable. **Not over-bloating the grid is equally important — compromise beats
> completeness.**

## Design constraint

Current density is near the comfortable limit for a 14″ laptop screen (as of ~330 model
groups total). If the grids grow much further, rethink layout before adding rows —
candidates: collapsible year-decades, a compact mode, or splitting legacy eras onto
sub-pages. Until then: prefer grouped rows and aliases over new chips.

## Architecture

- `index.html` — landing page (brand picker + cross-brand quick search)
- `dell.html` / `thinkpad.html` / `hp.html` — pure renderers, one per brand
- `getac.html` / `panasonic.html` — rugged renderers (cloned from `hp.html`, identical code
  except the brand config block: META/order/TIER/POS/YEAROS/WIN11Y). Fix a bug in one → fix both.
- `dell.csv` / `thinkpad.csv` / `hp.csv` / `getac.csv` / `panasonic.csv` — ALL model data lives here (universal schema)
- The rugged CSVs are NOT in `specdata.js` BRAND_FILES on purpose: `index.html` loads them itself
  (`EXTRA_CSV`), so adding them needed no change to the shared loader and no cache-stamp bump.
- `specdata.js` — shared CSV loader; schema documentation lives at the top of this file

**Adding a laptop = adding one CSV row.** No code changes needed. Edit the CSV directly
on GitHub (pencil icon) and the site updates after the Pages build (~1 min).

**Version line:** the front page (`index.html`, bottom) shows `Version YYYY.MM.DD · what changed`
plus the time GitHub Pages published the page. Bump it with every commit — see TODO "Build note".

## Data conventions

- `aliases` column: extra searchable names that share the row's platform but don't get
  their own chip (variant models, twins).
- Prices: `price` + `price_note` columns. Notes starting with **"Real eBay sold IQR"**
  are measured from actual eBay sold listings (interquartile range, filtered to working
  single units); **"Est. (calibrated…)"** are estimates calibrated against that sold data.
  Snapshot: July 2026. Vintage (pre-2009) rows are flagged: the collector market trends
  *up*, so clean examples can sell well above the listed range.
- Storage is structured (`st_25sata`, `st_msata`, `st_m2sata`, `st_m2nvme`, `st_ide`,
  `st_emmc`, `st_m2len`, `st_note`) with 0/1/2 = no/yes/optional — this drives the
  filter chips and the generated storage description.
- Chargers (`pwr`) and batteries (`bat`, `bat_note`): connector family + nickname +
  typical shipped wattage on the surface; part numbers, buying tips, and warnings go
  behind the ⓘ (any field can carry a `short |> deep` split — the renderer folds the
  deep part into an expandable note). Connector thumbnails come from `img/chg-*.svg`,
  matched on the short part of the pwr text only.

- Serial port (`rs232`, `rs232_note`, added 2026-10-05 → **34-col schema**): `1` = native
  RS-232 on the machine itself (DB9, or Dell's micro/mini-serial on tablets — the note says
  which cable it needs), `2` = only some units (a factory option, an optional I/O module, or
  a grouped row where only one sub-model has it — e.g. 6470b / 6570b), `0` = confirmed
  none, **blank = unverified**. Dock / port-replicator / Ultrabay-adapter serial does NOT
  count — it goes in `rs232_note`. Drives the "⊶ RS-232" toggle on all three pages and
  the "serial / rs232 / db9" search terms. Every filled cell cites its source behind the ⓘ.
- **Since 2026-11-16 (later): `typ` = odds for a random unit** — "RAM 16 GB ~50% · 8 GB ~40%<br>SSD 256 GB
  ~55% · …", from eBay active-listing titles (`ebay_raw/`, rebuilt by `tools/typ_build.py`); the
  UserBenchmark numbers moved behind the ⓘ as a second opinion. The paragraph below describes the
  first (UserBenchmark-only) version and its limits, which still apply to that second opinion.
- Typical config as found (`typ`, `typ_note`, added 2026-11-16 → **38-col schema**): the RAM
  size / stick layout and SSD size that real machines of this model actually carry — NOT the
  spec-sheet range. Surface text like `16 GB (1×16) · 256 GB NVMe`; two values (`8 GB (1×8) /
  16 GB (2×8)`) when no single size reaches 60 % of the visible counts. `typ_note` (behind
  the ⓘ) holds the evidence: UserBenchmark system, PC count, pull date, size split, caveats.
  **blank = not harvested yet** (the panel row is hidden then). Never hand-edit: the cells are
  generated by `tools/typ_from_ubm.py` from the raw pulls in `ubm_raw/` — change the grouping
  rules in that script and re-run to regroup, no re-pull needed. Limits to keep in mind: only
  the top-5 parts per component are visible (usually 20–45 % of the PCs), benchmark-runners
  skew toward upgraded units, Lenovo pages are per-MTM so samples are small (< 50 PCs = left
  blank), and a grouped row is represented by ONE system (named in the note).
- CPU re-paste difficulty (`repaste`, `repaste_note`, added 2026-10-09 → **36-col schema**):
  how far you tear down to reach the CPU die. `1` = very easy — bottom cover off, heatsink
  only, fan is separate and stays (Latitude 3400); `2` = easy — bottom cover off, heatsink +
  fan as one assembly; `3` = complex — partial disassembly first (keyboard / palmrest / more)
  (ProBook 650 G5); `4` = very complex — motherboard out / full teardown; **blank =
  unverified**. Sources: hands-on 🔬 first, else the service manual's heatsink-removal
  prerequisites (Dell Service Manual / Lenovo HMM / HP Maintenance & Service Guide).
  Gotchas (shared dGPU heatsink, VRM pads, clip-on covers that crack) go in the note.
  Drives the "🔧 Re-paste" cycle button (any → ≤2 → ≤3) on all three pages.
- Dell **5xx1 performance twins** (2026-11-16): 5491 / 5591 · 5401 / 5501 · 5411 / 5511 · 5421 / 5521 · 5431 / 5531 are their
  own rows, NOT aliases of the 5xx0 — different board: H-series (5431: P-series) CPU, optional GeForce MX, 90 / 130 W charger,
  a battery pack not always shared with the 5xx0, and from 2022 different RAM (5431 / 5531 = DDR5, 5430 / 5530 = DDR4). `dell.html`
  `slotOf()` gives any model matching `5[45]x1` its own aligned sub-column (slot 1.5) right beside the 5000s, so a new one
  only needs a CSV row. Built from Dell Setup & Specifications + service manuals, then cross-checked against the
  UserBenchmark system pages (`ubm_raw/2026-11-16-xx1.jsonl`): CPU list, RAM type and dGPU share all agreed.
- Dell **Rugged column** (2026-10-05): any Dell row whose model contains "Rugged" or
  "XFR" is pulled out of its screen-size column into one 🛡 Rugged column (all sizes,
  largest first; the chip shows the size). Name new rugged rows "<num> Rugged",
  "<num> Rugged Ext.", "<num> Rugged Tab." or "<model> XFR" and they land there
  automatically. Semi-rugged ATG variants are aliases on their base E/D rows, not chips.

## Rugged pages (Getac / Panasonic, added 2026-10-10)

- **Scope:** ~2005 → 2026, Windows devices only. Everything that existed goes in, even models that
  fail a buyer's requirement — negative answers are information (SM: "I want to see it in the table,
  not googling").
- **One chip per generation / Mark.** Getac G-numbers and Panasonic Marks change CPU, RAM type and
  ports, so they are never grouped. Panasonic's own letter→Mark table (from the TOUGHBOOK Support
  site model list) is in the aliases, e.g. `CF-31S` `CF-31U` `CF-31V` → CF-31 mk3.
- **Part-number paste:** the search also matches a pasted full part number against those Mark
  prefixes (`cf-31sblaxxm` → CF-31 mk3) — tokens shaped `cf-xxx` / `fz-xxx`, query ≥7 chars.
- **Search syntax (rugged pages):** space-separated words are AND-ed; a leading `-` excludes
  (`-ddr3 -ddr4 serial`, `b300 -g7`). Haystack = model, aliases, CPU, size, RAM, charger/battery
  family plus status tokens: `serial`/`rs232` (has port), `native-serial`, `optional-serial`,
  `portnone` (spec ports list shows none), `portunknown` (not verified), `win11` / `no-win11`, `soldered`.
- **⊶ Serial button** cycles: any → has port (1 or 2) → native only (1) → confirmed NONE (0) →
  not verified (blank). Chip face shows `⊶` (native) or `⊶°` (option).
- **gen = `unk`** → grey chip "RAM ?": the generation exists (needed for search / Mark lookup) but
  RAM type isn't verified yet. Same rule as everywhere: blank/unk beats a guess.
- **Serial on keyboards/docks** (CF-33 keyboard = USB-based serial, UX10 keyboard dock, CF-H1 dock)
  does NOT count — it goes in `rs232_note`.
- **Sources used:** Getac/Panasonic spec sheets and press releases, Panasonic Operating Instructions
  PDFs (dl-pc-support.connect.panasonic.com — `pc-dl.panasonic.co.jp` is robots-blocked, not used),
  RuggedPCReview.com spec tables (excellent per-generation tables; reachable from the built-in
  browser, not from the cloud fetcher), Kingston's memory configurator for slot counts.
- No prices yet on either rugged page (needs a live sold-comps pull — never training data).

## Dell Precision page (added 2026-11-19)

- `precision.html` + `precision.csv` — Dell's mobile workstations, ~2001 → 2026, one chip per model (the xx1
  H-series 3000s — 3541/3551/3561/3571/3581/3591 — are their own chips, like the Latitude 5xx1 rows).
  Generated from `getac.html` by `tools/make_precision_html.py` (re-run it after a renderer fix in getac/panasonic).
  `index.html` loads `precision.csv` via `EXTRA_CSV` (brand key `precision`).
- **Tabs by lineage:** ③ 3000 (Latitude-based: M20 → M2300 → M2400 → M2800 → 3510 … → Pro Max 14/16) ·
  ⑤ 5000 (XPS-based: M3800 → 5510 … 5690, 5470/5480/5490, 17″ 5750/5760/5770) · ⑦ 7000 15–16″
  (M40/M50/M60/M70/M65 → M4300 … M4800 → 7510 … 7680) · ⑰ 7000 17–18″ (M90 → M6300 … M6800 → 7710 … 7780).
- **Extra columns (precision.csv only; specdata.js passes them through, harmless elsewhere):**
  `gpu` (every graphics option Dell sold, with VRAM; starts with "UMA only" when no dGPU was offered),
  `gpu_note`, `gpu_mxm` (1 = removable card — MXM type-A/B on M4800 → 7540, Dell's own "GPU card" on
  7550 → 7770, older Dell video modules on M40/M60/M70/M90/M6500/M6600; 0 = soldered; blank = unverified),
  `gpu_mxm_note`, `gpu_typ` / `gpu_typ_note` (likely GPU of a random unit — not filled yet), `scr` / `scr_note`
  (every panel Dell offered: resolution, touch, brightness, gamut, refresh, panel tech).
- **🎮 GPU filter:** any → ▣ removable card → soldered dGPU → integrated only. Search also matches GPU and panel
  text (`rtx a2000`, `t1000`, `oled`, `touch`, `uhd`) and tokens `mxm` / `removable-gpu` / `soldered-gpu` / `uma-only`.
- **Sources:** Dell's own documents only for specs — Setup & Specifications / Owner's Manual HTML pages on
  dell.com/support (harvested in the built-in browser, see TODO §15) and Dell PDFs on
  `dl.dell.com/manuals/...` (lowercase path works with WebFetch; `/Manuals/` and downloads.dell.com are
  robots-blocked). Removable-vs-soldered GPU comes from the service manual's table of contents ("Removing the
  video/graphics/GPU card") or Dell's own "MXM type-A/B add-in card" wording. Where Dell's text contradicts
  itself or other sources, the note says so instead of picking one.
- No prices, no likely-GPU odds, no screen value premium yet — those need slow live pulls (TODO §15).

## Source-of-truth hierarchy (how much to trust a given cell)

Buying 400 machines to touch every one isn't realistic, so most cells lean on documents.
This is the ranking of how close each source sits to physical reality, strongest first:

1. **Physical unit in hand (owner-verified).** Gold, but a single sample — it confirms
   *this* unit, not necessarily every unit of the model. Tagged 🔬 in the data. ~20+ of
   the fleet's models have been personally handled; those double as the **calibration
   set** — every time a hands-on unit agrees with the parts ref, trust in the parts ref
   rises for the models nobody has touched.
2. **Service-tag / serial-keyed parts lookup** (Dell parts-by-tag, HP PartSurfer,
   Lenovo PSREF by serial). Nearly as good as physical: it reads the actual BOM Dell/HP/
   Lenovo shipped for *that specific machine* — the real DC-in harness or battery FRU,
   not a marketing sheet. **The tag is what makes it strong.** A model-level parts search
   with no tag loses the config/revision pin and slides down toward tier 3.
3. **Replacement-adapter / aftermarket listings** (what "fits" the 8470p, etc.). Useful
   aggregate market knowledge, but muddied by universal-compatible sellers who list one
   part against dozens of models. Good for confirming a family, weak for edge cases.
4. **Spec sheets, QuickSpecs, wikis, marketing pages.** Weakest for connector-level
   detail — they copy-paste errors and routinely omit tip type entirely. Fine for CPU/
   screen/year, unreliable for the barrel-vs-blue-tip kind of question.

**Stability caveat (mid-cycle running changes).** Even a tag-keyed parts ref can be
wrong if the model got a running change mid-production. But this bites different specs
differently: **connector tips are among the MOST stable** (retooling a barrel jack mid-
cycle is expensive, so it rarely happens), whereas **RAM vendor, panel, wifi card, and
sometimes battery P/N drift within a single model year.** So a parts ref on a charger
tip is close to bulletproof; the same source on "which exact RAM shipped" deserves more
doubt. Weight confidence by *which spec* you're reading, not just by the source tier.

## ⚠ eBay scraping pace — NEVER do rapid searches (SM's rule, 2026-11-16)
On 2026-11-16 ~110 eBay search loads in one session at 4–9 s gaps got eBay to answer **403 on search** for
SM's own Chrome (eBay home still worked). SM's own buying/selling account and IP depend on eBay — don't burn it.
- **≥ 20 s between searches** (randomized 20–30 s), **≤ 40 searches per sitting**, then **≥ 3 h cool-down**.
- Stop at the FIRST non-200 / empty / challenge page — no retries, no switching browser or method to get around it.
- Keep results in the page AND mirror to localStorage as they arrive; make **ONE** download at the end
  (Chrome blocks a 2nd automatic download); never navigate the working tab away before the file is in Downloads.
- Same spirit for any other site (UserBenchmark: ≤ ~30 page loads per sitting, captcha = hard stop).

## Verification methodology (proof run)

Planned "triple-distilled" audit uses **UserBenchmark system pages** as the empirical
confirmation layer (~73M auto-detected systems; detection data only — their scores are
irrelevant). Validated in a 6-system pilot (Jul 2026):

- **What it proves:** which CPUs and memory configs *actually exist* in a model.
  Frequencies are biased (benchmark-runners skew toward tinkerers), but every observed
  config is an existence proof — and laptop platforms constrain what can change, so
  possibilities are what we verify (CPU family, max RAM seen, soldered-vs-slotted).
- **Soldered vs SODIMM signature:** slotted machines report retail module part numbers
  (Samsung M471*/M425*, Hynix HMA*/HMCG*, Micron MT*); soldered machines report bare
  DRAM die part numbers (e.g. Hynix H58G* LPDDR5X) in odd channel configs (4×4GB).
  Mixed platforms (soldered + 1 slot) show TWO part numbers in one machine.
- **Lookup keys:** Lenovo = MTM codes (`20L5` = T480, `21HD`/`21K3` = T14 Gen 4
  Intel/AMD; CTO SKUs carry the biggest samples). HP and Dell = marketing names.
  The site search fuzzy-redirects some queries — search bare MTM or exact name.
- **ARM caveat:** the benchmark client is x86-only; Snapdragon machines (Latitude
  5455 etc.) appear as empty stub pages with 0 PCs. Absence of data ≠ absence of model.
- **Pacing:** observed limit ~40 page loads per session before the "click the green
  human" captcha wall appears (even at 5–10s intervals). Budget ≤~15 systems (≈30
  loads) per session, then let it cool down for hours/overnight. Captchas are a
  hard stop — never automated past. Compare observed CPU/RAM population against the
  row's `cpu`/`gen`/`slots`/`max` columns and flag disagreements for human review.
- **Faster harvest (2026-11-16, 32 systems in one sitting, no captcha):** (1) get the
  system-page IDs WITHOUT touching UserBenchmark — WebSearch restricted to userbenchmark.com
  for "UserBenchmark <brand model> Compatible Components" returns `/System/<slug>/<id>` URLs,
  ~5–10 neighbouring models per query (the slug alone 404s; the numeric id is what matters).
  (2) Open ONE system page in the built-in browser, then pull the rest with same-origin
  `fetch()` + DOMParser from that tab — one load per system, parsed from `table.ms-table`
  (`thead th` = component, `td.ms-freq` = count). A hidden tab throttles timers, so the
  8–11 s delay really runs at ~30–40 s per system — slow but it stayed under the wall
  (33 loads). Stop on any non-200 / empty page; captchas remain a hard stop.
  (3) Save every row to `ubm_raw/<date>.jsonl` (+ `ubm_raw/system_map.csv` = which grid row a
  system feeds), verify with the per-system checksum, then `python3 tools/typ_from_ubm.py --write`.
- **Blind spot:** chargers and batteries are invisible to the benchmark — those columns
  are verified from PSREF/QuickSpecs/manuals and owner reports instead.
