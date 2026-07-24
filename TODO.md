# TODO / Roadmap (chaotic by design)

*Parked 2026-07-21. Order is negotiable, chaos is intentional.*

## 1. Batteries
Fill the `bat` / `bat_note` columns (schema + renderer already live, all three brands):
type = removable / internal / bridge (both), plus ONE common part number per
interchangeability family for precise searching (e.g. ThinkPad 68+/X240–X270 packs,
Dell E-family bricks, HP CC06/CA06). PSREF/QuickSpecs-deterministic for type;
part families added conservatively.

## 2. Video cards (dGPU)
New column: dGPU Yes / No / Optional per model group. Candidate filter chip.
UserBenchmark GPU sections already reveal the real split (e.g. E6540 = HD 4000 vs
HD 8790M configs) — harvest during UB runs.

## 3. UserBenchmark harvesting — go wide
- Continue the proof run (~30 of ~330 rows done; budget ≤15 systems/session,
  captcha wall at ~40 page loads — see README methodology).
- **Collect EVERYTHING visible per system page**: CPU, RAM, GPU, and raw
  SSD/HDD drive models (drives requested explicitly), USB, MBD if shown.
  Dump into `ubm_stats.csv`; figure out uses later. Storage costs nothing.
- Build CPU-make distribution profiles per model: aggregated to
  i3 / i5 / i7 (+ Ryzen tiers), and dual vs quad core for older gens —
  not per-SKU granularity. Output could be a small per-model bar in the panel
  or a separate stats page.

## 4. eBay "days on market" per model
Where feasible: sold listings expose sold date; listing-start date is the hard
part (sometimes visible on listing page). Research feasibility first — even a
rough "sells in days vs weeks" tier per model would be valuable for both
buying and reselling decisions.

## 5. Filtering / cosmetics
DONE 2026-07-22: component-first reverse lookup. `bat_fam` column (31-col schema) +
"⇄ same battery / ⇄ same charger" buttons in the panel + amber filter banner; search
box now also matches battery family keys and charger connector text. Jumps to the
▦ All view so cross-series compatibility shows.
STILL OPEN (approved design, not yet built): segmented filter selector
(💾 Storage | 🔌 Charger | 🔋 Battery) swapping chip sets in one row, all chips
colored by the era palette (storage buttons stop being "random colors":
IDE brown → 2.5″ SATA mauve → mSATA blue → M.2 SATA green → NVMe orange).
Other candidates: dGPU (see #2), price bracket.

## 6. Visitors counter
Static GitHub Pages → needs external counter. Privacy-friendly candidates:
GoatCounter (free, no cookies), Cloudflare Web Analytics, or a simple
hit badge. Decide tolerance for third-party script first.

## 7. Chargers PHOTOSESSION 📸
Replace/augment the schematic SVGs (`img/chg-*.svg`) with real macro photos —
plug tip toward camera, slight angle, plain background. Shopping list:
Dell 7.4mm, Dell legacy (C-series if one survives), Lenovo 16V barrel,
Lenovo round tip (R50/Z60m chargers!), Lenovo slim tip, HP 7.4mm smart-pin
(8570w), HP 4.5mm blue tip (840 G3), one USB-C. Photoshop for clarity is
allowed and encouraged — this is a reference diagram, not an eBay condition
disclosure. Blocked on: photosession room availability.

## 8. Field-tested owner benchmarks 🔬
SM has Speedometer 3.1 + WebXPRT 5 results for EVERY machine that passed through
his hands (PassMark for some) — same tester, same methodology, real bought-and-
upgraded configs. Plan: `owner_bench.csv` (model, config_as_tested, speedometer31,
webxprt5, passmark, date, notes) → "🔬 field-tested" badge in the detail panel
with the score on the surface and config-as-tested behind the ⓘ. Doubles as the
personal-verification marker. Waiting on: SM dumping the numbers (any format —
messy list is fine, will be normalized).

## 10. Official-link `url` column (added 2026-07-24)
A manual `url` column now exists (last col, schema = 32). Empty = the page auto-links a
brand-scoped model search ("🔍 Look up on Dell.com/Lenovo PSREF/HP support"); an exact
URL in the cell overrides it with a direct "product page" link. Backlog: fill exact
spec-page URLs per row, incrementally, where the auto-search isn't precise enough.
Only Pro Plus 16 is filled so far.

## ⚠ Build note — specdata.js cache stamp
The three HTML pages import the loader via `import('./specdata.js?b=YYYYMMDD')` (a cache
buster, because GitHub Pages caches JS ~10 min without revalidating). CSV fetches use
`{cache:'no-cache'}` so DATA edits show on a normal refresh with no stamp change. BUT
whenever `specdata.js` ITSELF changes, bump the `?b=` stamp in all three HTML files or
visitors keep running the stale loader. Current stamp: 20260724.

## 9. Battery market research
Fake-OEM problem: $20–35 "genuine" packs on eBay are counterfeit almost without
exception. Current row tips state the honest tiers (aftermarket $50–70+, genuine
new $100+, used real OEM pulls = value play) but the used-real-OEM market needs
proper research: how to spot authentic pulls, which sellers, price ranges per
family. SM has field experience here — capture it.

## Standing context
- eBay price batches still in progress (ThinkPad partially real-data'd; HP all
  estimates — Task #20).
- Vintage UB lookups need full-MTM detective work (web search "site:userbenchmark.com").
- E480 + ProBook 450 G5 show small 7th-gen CPU tails in UB data — judge someday.
