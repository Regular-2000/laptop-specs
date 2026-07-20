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
