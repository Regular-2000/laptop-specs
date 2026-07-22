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

---

# VETTED FRU LOOKUP TABLES (research leads)

External battery spec reviewed 2026-07-21. Part numbers below are largely corroborated
and are a strong upgrade over the `search "..."` placeholders — **use as leads, verify per
generation before committing.** Three rules from the source spec were REJECTED and must NOT
be applied: (a) its "never use pipes" rule — our `|>` fold depends on the pipe, keep it;
(b) its `<span class="amber-warn">` markup — that class doesn't exist, keep our inline
`style="color:#e5b567"` warning verbatim; (c) its shortened warning text — keep our fuller
version (includes "check cycle count").

**⚠ Over-consolidations to SPLIT back out (source merged gens that used different packs):**
- X1 Carbon **Gen 1 / 2 / 3** — three different batteries, not one. Verify each.
- X1 Carbon **Gen 5 vs Gen 6** — NOT interchangeable (Gen5 ≈ 01AV429, Gen6 = 01AV494).
- X1 Carbon **Gen 7–10** — four gens, almost certainly multiple packs. Verify each.
- HP ProBook **4310s–4710s** — s-series changed packs across sub-gens; one spare won't cover all.

## ThinkPad
- T20–T23: 02K6843 · T30: 02K7036 — removable
- T40–T43 / R50–R51: 92P1102 (hi-cap 6-cell) — removable
- T60–T61 / R60–R61 / Z60–Z61: 40Y6799 (6-cell) / 40Y6797 (9-cell) — removable *(Z-series may differ)*
- T400–T500 / R400–R500: 42T4566 (6-cell) — removable
- T410–T520 / W510–W520 / L410–L520: 42T4795 (57) / 42T4797 (57+) — removable ✓verified
- T430 / T530 / W530 / L430–L530: 0A36302 (70) / 0A36303 (70+) — removable ✓verified
- Power Bridge T440–T480 / X240–X270: ext 45N1136 / 01AV427 (68+); internal-slim
  (T460s–T480s) 00HW022 / 01AV422 — bridge ✓verified
- T490 / T14 Gen1–2 / P43s / P14s: 01AV490 / L18M4P74 (50Wh) — internal
- T14 Gen3–5 / P14s Gen3–5: 5B10W13955 / L21C3P72 (52.5Wh) — internal
- X200–X201: 42T4653 (6-cell) / 42T4654 (9-cell) — removable
- X220: 0A36282 · X230: 0A36307 — removable ✓verified
- X1 Carbon G1–3: 45N1111 / 04W6939 — internal *(SPLIT — gens differ)*
- X1 Carbon G5 / G6: 01AV429 (G5) / 01AV494 (G6) — internal *(NOT interchangeable)*
- X1 Carbon G7–10 / X1 Yoga: 01AV479 / 5B10W13932 — internal *(SPLIT — verify each)*
- E480 / E580 / L14 / L15: 01AV445 (45Wh) — internal ✓verified

## Dell
- D620–D630 / D820–D830: PC764 / X284G (6-cell) — removable
- E5400–E6500: KM958 (9-cell) / PT434 (6-cell) — removable
- E5410–E6510: NM711 / JK3NN — removable
- E5420–E6530 / E6440 / E6540: T54FJ / M5Y0X / KJ321 (9-cell 87Wh) — removable ✓verified
- E7240 / E7440: 34GKR (3-cell) / 3RNFD (4-cell) — removable ✓verified
- E7250 / E7450 / E7270 / E7470: GWD7V / V4RM3 (54Wh) — internal
- 5280–5590 / 5400–5510: GJKNX (68Wh) / 1VX15 (51Wh) — internal ✓verified
- 7280–7490: F3YGT (60Wh) / DJ1J0 (42Wh) — internal ✓verified
- 7200–7440 modern: 1WYHP / 722KK / R8D7N — internal

## HP
- ProBook 4310s–4710s: 593554-001 / HSTNN-OB9C — removable *(SPLIT — s-series varies; my 4x30s row uses PR06)*
- EliteBook 8460p–8570p: 628670-001 / CC06 (6-cell) — removable ✓verified *(VH08 is the 8x60w/8x70w workstation pack, not the p-line)*
- 2560p / 2570p: 632423-001 / CC09 — removable
- Folio 9470m / 9480m: 687945-001 / BT04XL — **removable** 🔬 owner-verified (5-sec pull, 2026-07-21)
- 840 G1/G2 / 850 G1/G2: CM03XL (50Wh) / 717376-001 — internal
- 840 G3/G4 / 745 G3/G4: CS03XL (46.5Wh) / 800513-001 — internal ✓verified
- 830/840/850 G5/G6 / 745 G6: SS03XL (50Wh) / 932823-421 — internal ✓verified
- 830/840 G7/G8 / Firefly 14 G7/G8: CC03XL (56Wh) / M07399-001 — internal
- 830/840 G9/G10: WP03XL (51.3Wh) / N04955-001 — internal
