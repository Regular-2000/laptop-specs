# Battery data — handoff brief

**Status (2026-07-21):** all 382 grid rows have `bat` + `bat_note` filled. TYPES are
reliable (era-rule derived). PART NUMBERS are verified for ~30 rows; the rest carry a
generic `search "[model] battery"` placeholder. **Your job: replace placeholders with
verified FRU/part numbers, family by family.**

## Where the data lives
- `dell.csv`, `thinkpad.csv`, `hp.csv` — columns `bat` and `bat_note` (28-col schema;
  headers at top of `specdata.js`).
- `bat` = short type shown on the surface: **removable / bridge (int + hot-swap ext) /
  internal / rugged**. Keep this vocabulary small and consistent — a future filter chip
  reads this column, so don't invent new phrasings.
- `bat_note` supports the `short |> deep` split: text before `|>` shows next to the 🔋
  row; text after folds behind the ⓘ. Same mechanism as chargers.

## Conventions to preserve
- **Fake-OEM warning** must stay on every row (the amber ⚠ span + the "$20–35 genuine =
  fake / real aftermarket $50–70+ / used real OEM pull = value" text). Copy it verbatim
  from any filled row.
- One **representative part number** per interchangeability family — the one with the
  most aftermarket listings, so search actually returns cheap packs. Not exhaustive.
- **Verified vs guessed:** only write a specific FRU you've confirmed (PSREF for Lenovo,
  Dell/HP QuickSpecs or the battery vendors — Crucial, Mr Memory, laptopbatteryexpress).
  If unsure, leave the `search "..."` placeholder rather than inventing a number.
- The amber ⚠ uses `<span style="color:#e5b567">⚠</span>` — inline HTML is fine in notes.

## Already-verified families (don't redo, use as templates)
ThinkPad: X220 0A36282, X230 0A36307, T420 42T4795, T430 0A36302, Power Bridge
45N1136/01AV427 (T440–T480/X240–X270), E480 01AV445, X1C6 01AV494.
Dell: T54FJ (E5430/E6430 family), F3YGT (7280–7490), GJKNX (5280–5590), E7440 34GKR.
HP: CC06 (8460p–8570p), VH08 (8x60w/8x70w), CS03XL (840 G3/G4), SS03XL (840 G5/G6),
BT04XL (Folio 9470m), PR06 (4x30s), RR03XL (ProBook 440/450 G4/G5), SE03XL (ZBook 15 G3).

## Priority order
1. Rows that appear in `ebay_prices.csv` / `owner_bench.csv` (most-trafficked models).
2. Fleet models the owner physically has (ask SM — he can read the FRU off the pack).
3. Everything else, newest-to-oldest (vintage packs matter least — they all need
   rebuilding anyway).

## Workflow
Edit the CSV directly on GitHub (pencil icon) → commit → Pages rebuilds in ~1 min.
No code changes needed. Validate column count stays 28 after each edit.

## Open related task (see TODO.md #9)
Used-real-OEM battery market needs research: authentication tips, seller list, per-family
price ranges. SM has field experience to capture.
