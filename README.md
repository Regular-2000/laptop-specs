# Laptop specs quick reference

Interactive spec sheets for used-laptop hunting on eBay / Facebook Marketplace / Mercari.
Live at **https://regular-2000.github.io/laptop-specs/**

Covers **Dell Latitude**, **Lenovo ThinkPad** (incl. IBM era) and **HP business laptops**
(ProBook / EliteBook / Dragonfly / ZBook). Per model: RAM type & max, upgradeability
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

- `index.html` — landing page (brand picker)
- `dell.html` / `thinkpad.html` / `hp.html` — pure renderers, one per brand
- `dell.csv` / `thinkpad.csv` / `hp.csv` — ALL model data lives here (universal schema)
- `specdata.js` — shared CSV loader; schema documentation lives at the top of this file

**Adding a laptop = adding one CSV row.** No code changes needed. Edit the CSV directly
on GitHub (pencil icon) and the site updates after the Pages build (~1 min).

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
- **Blind spot:** chargers and batteries are invisible to the benchmark — those columns
  are verified from PSREF/QuickSpecs/manuals and owner reports instead.
