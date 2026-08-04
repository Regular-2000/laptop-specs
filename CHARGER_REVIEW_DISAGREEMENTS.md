# Charger reference review — disagreements & unverified claims

Review of `laptop_charger_master_reference.md`, done 2026-07-22. This captures the
parts I **rejected or could not verify**, so SM can adjudicate later. The parts I
agreed with are already applied to the data (see bottom).

Method: every claim that touched our live `pwr` data was checked against replacement-
adapter listings (which list the actual tip size + OEM part number). Web sources are
in the chat where this review ran.

---

## 1. REJECTED — the doc's Dell "4.5mm" claim is backwards

**Doc says:** Latitude E7240/E7440 and the 5280–5590 / 7280–7490 thin era use the
**4.5mm small barrel** (audit row #2 + Section 2A "2013–2019 Ultrabook era").

**Reality (verified):** these are **7.4mm barrel**. Every replacement brick bundles
5490/5480/7480/7290/E7440/E7450 on the 7.4mm LA65NM130 (19.5V 3.34A 65W).

**What happened:** the doc conflated Dell's *XPS / consumer ultrabooks* (which really
did move to 4.5mm) with the *business Latitudes* (which kept the 7.4mm barrel well
past 2013 — it wasn't retired until the USB-C switch). Two different lineages, one
label.

**Our data was already correct** (7.4mm on all these rows). No change made. If SM ever
wants to trust the doc's part-number ledger, note that its "proof" here (DP/N `04W9NY`
= 4.5mm on the E7440) is exactly the claim the evidence contradicts.

---

## 2. NOT PROPAGATED — unverified part numbers & specifics

Could not confirm these from independent listings; the doc is the only source, and
since it got #1 wrong, I did not paste any of them into the CSVs:

- Dell DC-jack DP/Ns: `T0587` (3140), `04W9NY` (E7440 — and see #1).
- HP DC-jack P/Ns: `826805-001` (840 G3), `721936-001` (ProBook G1).
- ThinkPad harness FRU `04W3997` (X1C Gen1 slim tip).
- ThinkPad slim-tip resistor-pin ohm values (135W = 1kΩ, 90W = 550Ω, 65W = 280Ω,
  45W = 120Ω) — plausible, uncited. Fine as trivia, not as data.

These aren't necessarily *wrong* — just unverified. SM to confirm against PSREF /
PartSurfer / Dell parts lookup if we ever want them in the grid.

---

## 3. OPEN QUESTION — exact HP blue-tip switch year

Verified: EliteBook 840 **G1 = 7.4mm**, blue tip is in by **G3** (SM owns a blue-tip
G3). The **G2** boundary is unconfirmed — did the 840 G2 (2014–15) still use 7.4mm, or
had it switched? Same open question for ProBook 4xx **G2**. We currently have no
separate G2 charger row asserting either way; worth a physical check if a G2 passes
through the fleet.

---

## 4. OPEN QUESTION — Latitude 3300 tip (audit 2026-08-04)

The 3000-series audit (see below) left one unresolved row: **Latitude 3300** (13.3″,
listed year 2017 in our CSV). Aftermarket listings claim **7.4mm**, but the 3300 is
the 3400/3500's 13″ sibling (launched 2019 — our CSV year may be off) and that whole
platform is 4.5mm + USB-C per Dell's spec sheets. Sources conflict, so the row was
LEFT at 7.4mm. Needs a tag-keyed parts lookup or a physical unit. (Related education
oddity that keeps this plausible: SM's own 3120/3140 units shipped 7.4mm bricks 🔬.)

---

## Applied 2026-08-04 — Latitude 3000-series tip audit (triggered by SM's 3400 catch)

SM flagged the 3400 as wrongly listed 7.4mm; his service-tag parts export (GQD5NW2)
shows the shipped adapter = `MGJN9` **65W Liteon 4.5MM** — tier-2 evidence. Full
vicinity audit against Dell's own manuals/spec pages followed. The switch point:

- **7.4mm confirmed correct** (Dell manual explicit): 3380, 3480, 3580 — no change.
- **x90 refresh switched to 4.5mm** (Dell manual: "shipped with 4.5 mm barrel plug"):
  3490, 3590 → fixed from 7.4mm.
- **3400 / 3500** (Dell spec table: 45/65W 4.5mm barrel + 65/90W USB-C options) →
  fixed from 7.4mm (3400) / USB-C-only (3500). Surface = 4.5mm (what ships), USB-C
  in the dual note.
- **2019–2024 USB-C rows** (3310, 3330, 3410, 3420, 3430, 3440, 3450, 3520, 3530,
  3540, 3550): kept USB-C as primary but added the **65W 4.5mm barrel** config
  option (Dell spec tables for 3420/3520/3440; Dell's 65W-4.5mm accessory page lists
  3430/3530/3550; DA65NM191 covers the rest) and corrected the old deep-note claim
  that the barrel on these was "7.4mm" — it's 4.5mm on the 3000 series.
- The doc's Section-1 verdict stands: business 5000/7000 of that era = 7.4mm. The
  4.5mm tip entered the *Latitude 3000* line via the education/budget side — a third
  lineage next to the two in #1.

Reviewing the doc caught **3 real errors in our own `pwr` column** — all were wrongly
set to "4.5mm blue tip" and are actually **7.4mm smart-pin barrel**. Fixed
2026-07-22:

- **Folio 9470m** → 7.4mm  *(🔬 owner-verified — SM's unit, "100% 7.4, same as 4430s")*
- **ProBook 440/450 G1** → 7.4mm
- **EliteBook 820/840/850 G1** → 7.4mm

Kept from the doc as accurate reference (no data change needed, already matched):
Dell 3140/3120 = 7.4mm + USB-C; HP 840 G3/G4 = blue tip only (USB-C has no charging
PD); ThinkPad X1C Gen1 = first slim tip; the overall ThinkPad tip timeline.
