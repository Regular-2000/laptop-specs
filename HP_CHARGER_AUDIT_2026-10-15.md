# HP charger audit — 2026-10-15

**Source:** HP PartSurfer spare-parts BOMs, pulled for every product number under each hp.csv model (98 rows).
**Method:**

* Every AC adapter listed in the BOM was classified by its description: "4.5MM" or "RC 4" means blue tip, "7.4MM" means smart pin, "USB-C" or "TYPE-C" means USB-C.
* Legacy part numbers were also counted as 7.4mm: 6939xx, 742437, 744893, 609939/40/47, 613xxx, 4639xx, 5355xx, 5771xx and 6451xx.
* Bricks of 120W or more on non-workstation models were dropped, because they are dock power supplies.
* If a model had an explicit 4.5mm part, a stray legacy 7.4mm part listed next to it was ignored.

Backup of the old file: `hp.csv.bak-20261015`. Delete it before committing.

## The answer you asked about

**EliteBook 840 G1 is 7.4mm, not 4.5mm.** The CSV was already right. Across both G1 product groups, the only adapters PartSurfer lists are 7.4mm 65W smart-pin bricks.

The CSV was wrong one generation later. **820/840/850 G2 was listed as 4.5mm but is 7.4mm.** Its BOM lists 744893-001, whose description explicitly says "with 7.4mm barrel connector". On the 800 series the blue tip starts at **G3**.

## Changes made to hp.csv (25 labels changed, 42 notes rewritten)

| Model | Was | Now | Evidence |
|---|---|---|---|
| 440/450 G2 | 4.5mm | **7.4mm** | 12 products, only 7.4mm bricks |
| 745/755 G2 | 4.5mm | **7.4mm** | 14 products, only 7.4mm bricks |
| 820/840/850 G2 | 4.5mm | **7.4mm** | 744893-001 "7.4mm barrel connector" |
| 640 G4, 640 G5 | 4.5mm | 4.5mm **+ USB-C** | Both brick types listed (13 and 7 products) |
| 640 G7, 650 G7 | 4.5mm | 4.5mm **+ USB-C** | BOMs list blue tip only. USB-C comes from QuickSpecs (the old note). |
| 440/450 G6, G7 | 4.5mm | 4.5mm **+ USB-C** | Both listed |
| 440/450 G8 | 4.5mm | 4.5mm **+ USB-C** | ⚠ Thin evidence: 1 product, USB-C brick |
| 440/450 G9, G10 | USB-C | 4.5mm **+ USB-C** | ⚠ Thin evidence: 1 product each, 4.5mm brick (65W / 45W) |
| 745/755 G5, 745 G6 | USB-C | 4.5mm **+ USB-C** | Both listed (18 and 17 products) |
| 835/845/855 G7 | USB-C | 4.5mm **+ USB-C** | Both listed |
| 835/845/855 G8 | USB-C | 4.5mm **+ USB-C** | ⚠ Thin evidence: 1 product, 4.5mm brick |
| 830/840/850 G5, G7, G8 | USB-C | 4.5mm **+ USB-C** | Both listed |
| 830/840/850 G6 | USB-C | 4.5mm **+ USB-C** | ⚠ 14 products, blue tip only. USB-C PD is assumed from the G5/G7 design. |
| x360 1030 G2 | USB-C | 4.5mm **+ USB-C** | 65W blue tip + 90W USB-C listed (22 products) |
| Firefly 14/15 G7, G8 | USB-C | 4.5mm **+ USB-C** | Both listed |
| Fury 15/17 G7 | 150–230W | 120–200W | Bricks listed: 120/150/200W |
| ZBook Fury G1i | "250W-class" | 4.5mm · 200–280W | Bricks listed: 200/280W |

Other rewrites:

* All 4.5mm-only rows from G2 through G5 lost the old "Many of these also charge via USB-C" line. That line was unsupported. They now say USB-C charging is **not confirmed**.
* The 7.4mm rows now cite example part numbers (693711-001, 744893-001).

## Confirmed unchanged

* **USB-C only:**
  * ProBook 440/460 G11 (22 products)
  * EliteBook 845/865 G9–G11 and 840/860 G9–G11
  * x360 1030 G3/G4/G7/G8
  * 1040 G9–G11
  * Dragonfly G2/G3
  * Firefly G10/G11
  * Elite Folio
  * ZBook 8 G1i (140W)
  * ZBook Ultra G1a (140W USB-C; its 230W 4.5mm brick is the dock's)
* Firefly 14/16 G9 is USB-C only, but on thin evidence (1 product).
* All pre-2013 7.4mm rows and the workstation wattage ranges (ZBook G2–G6, Studio, Fury G9/G10, 8560w/8570w) are unchanged.

## No evidence found (rows left as they were)

These had no adapter in any spare BOM, or no PartSurfer hierarchy match:

* 4440s/4540s, 2740p, 2760p
* Dragonfly G1, Dragonfly G4
* ZBook 15/17 G1
* Fury 15/17 G8

## Caveats, where this could be wrong

1. **A spare BOM lists the adapters HP *sells* for the model, not the port's capability.** "No USB-C brick listed" does not prove the USB-C port can't charge. That is why those rows say "not confirmed" rather than "no". Test with a PD brick before advertising it.
2. **Thin rows** (440 G8/G9/G10, 845 G8, Firefly G9) rest on one product number each. I labelled them dual-input because neighbouring generations show both connectors. If you get one in hand, look for a round DC jack and update the row.
3. **The 840 G6 is a judgement call.** The data says blue tip only, but G5 and G7 are both confirmed dual.
4. **840 G3: confirmed by owner test (SM, 2026-10-15). It does NOT charge from USB-C PD.** The hp.csv note now says so. The G4 is still "not confirmed" (no USB-C bricks listed), but the G3 result makes "no" the likely answer.

## Site change

`hp.html` now supports multiple charger families, the same as `dell.html`:

* Dual-input models show two "⇄ same charger" buttons (blue tip and USB-C).
* They appear under both filters.
