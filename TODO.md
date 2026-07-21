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

## 5. Filtering / cosmetics (owner's list pending)
SM has cosmetic filtering changes in mind + probably more filter criteria.
Await specifics. Current chips: RAM gen, storage types, Win11, search.
Obvious candidates when the time comes: dGPU (see #2), USB-C charging,
battery removable, price bracket.

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

## Standing context
- eBay price batches still in progress (ThinkPad partially real-data'd; HP all
  estimates — Task #20).
- Vintage UB lookups need full-MTM detective work (web search "site:userbenchmark.com").
- E480 + ProBook 450 G5 show small 7th-gen CPU tails in UB data — judge someday.
