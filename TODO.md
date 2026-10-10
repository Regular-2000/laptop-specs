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
DONE 2026-08-02: ▤ report button (all 3 pages, next to ✕ clear). Opens a full-screen
compact overlay listing ONLY the models matching the current filters — THIS page's
brand only (cross-brand judged overly ambitious for now), grouped by year, mini chips
in the era palette, dashed + ° = st value 2 (optional/config-dependent). Honors every
filter (storage chips, RAM legend, Win11, search, ⇄ fam). Overlay actions:
"⬇ save report (.html)" = standalone light/print-friendly file, self-contained, named
report-<brand>-<filters>-<date>.html, one context line per chip (storage by default,
battery/charger when a ⇄ fam filter is active); "🖼 save as photo (.jpg)" = eBay-ready 1600px canvas-drawn JPEG (no 3rd-party libs);
"⧉ copy as text" for eBay descriptions;
Esc closes. Shared code in specdata.js (showCompactList + buildReportHTML; loadAllBrands
kept exported for the future merged table); stamp bumped 20260802.
Origin: mSATA queries used to need 6 screenshots — now one screen or one saved file.
DONE 2026-08-02: landing-page quick search (index.html). Compact text field above the
brand cards; lazy-loads all 3 CSVs via the already-exported loadAllBrands() and live-counts
matches per brand (same haystack as page search: model + aliases + bat_fam + charger text).
Brand-colored count buttons appear as you type; Enter jumps straight to <brand>.html?q=…
when exactly ONE brand matches (the common case — full model numbers are near-unique);
cross-brand collisions (440/450/840/830…) take one click on a brand button. Brand pages
now honor ?q= — pre-fill search + auto-scroll to first hit; ThinkPad/HP additionally start
in ▦ All view when arriving with ?q= so hits outside the default tab are visible.
specdata.js unchanged → no stamp bump needed.
DONE 2026-08-02: ▥ compact layout toggle (all 3 pages, next to ▤ report). Merges the
aligned columns into ONE flowing row per year — report-style density but full-size,
fully interactive chips (filters/search/panel all work). Dell: sizes merged 15–16″ → 12″,
tier order kept inside each size, no alignment spacers. ThinkPad/HP: applies to the
▦ All view, series merged budget → premium (single-series tabs already flow — no-op
there). Toggle persists via localStorage key `specs_compact`, shared across the three
pages. specdata.js unchanged → no stamp bump.
Compact v2 (same day): in compact flow, filtered-out chips are REMOVED (not dimmed) so
survivors pack tight; year rows with zero visible chips hide entirely; subtle dashed
vertical separators between series (TP/HP ▦ All) / size groups (Dell), auto-hidden when
a whole group is filtered away (never two in a row, never leading/trailing). Aligned
mode keeps the dim-in-place behavior — there, position IS information. TP/HP compact
now also packs single-series tabs (flow cells, no seps).
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
Dell 7.4mm, Dell 4.5mm small tip (3400-era 3000-series), Dell legacy (C-series if
one survives), Lenovo 16V barrel,
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

**Dell: DONE 2026-07-25.** 143/151 rows filled with verified Dell *support* overview
pages (`…/product-support/product/<slug>/overview`) — tech/spec hub, not sales pages.
Slugs are NOT derivable and a wrong one silently 302s to the generic "Support Home"
hub (looks valid, is useless), so EVERY url was load-checked against the page title
before pasting. 8 rows left blank on purpose — the 7410/7420/7430/7440/7450/7310/7330/
7340 clamshells: their base slug redirects to the hub and only the `-2-in-1-laptop`
slug resolves (different form factor / specs), so they fall through to the auto-search.
Pro Plus 16 kept its existing shop URL (its support slug also hit the hub — unverified).
Slug traps logged for next time: E7-thin models use `-ultrabook` (e7250-ultrabook,
e7440-ultrabook); 2012 E6x30 use a BARE slug w/ no suffix (`latitude-e6530`); Rugged
hides under screen-prefixed base slugs (`latitude-14-5430-laptop` = 5430 *Rugged*, while
plain 5430 = `latitude-5430-laptop`); education 11″ = `latitude-11-` prefix. Method:
per-model web search → extract real slug from a live dell.com/support result → fetch
/overview → confirm title names the exact model.

**ThinkPad + HP: DONE 2026-07-25 (lead-model policy — revised from singles-only).**
Initial pass was singles-only (grouped rows left blank so the renderer's per-model
search shows). SM preferred a direct link over a search even on grouped rows, so the
policy is now: **every row gets a direct link to its FIRST-listed (lead) model** where a
page exists; only rows whose lead model has NO official page stay blank. Tradeoff (known
+ accepted): on a grouped row the shown link is labeled with the whole group but points
to the lead model only, and the per-model search links are replaced.
- ThinkPad → **Lenovo PSREF spec PDF** `…/syspool/Sys/PDF/ThinkPad/<slug>/<slug>_Spec.PDF`
  (SM's call — the pure spec sheet, fetch-verifiable, and works for withdrawn models
  whose HTML `/Product/` pages are broken/redirect to `/WDProduct/`). 101/145 filled;
  every URL confirmed by fetching the PDF. Notes: server is case-insensitive on the
  extension → normalized to `.PDF`. Intel/AMD-split models have NO combined PDF → use the
  `_Intel` variant (E14 Gen3 = `_AMD`, the only one lacking Intel). Slug quirks: X1 Carbon
  Gen2–7 = `_2nd_Gen`…`_7th_Gen` then Gen8+ = `_Gen_8`; X1 Extreme Gen1 = bare
  `ThinkPad_X1_Extreme`; P1 Gen1 = bare `ThinkPad_P1`; E14 Gen1 = bare `ThinkPad_E14`;
  L13 Gen1 = bare `ThinkPad_L13`. One oddball: **E430** has no standard `_Spec.PDF` — used
  its `/withdrawnbook/ThinkPad_E430.PDF` (an E430-only withdrawn catalog, still a real
  E430 sheet). 44 blanks = models with no per-model PSREF PDF (T20–T430, X31–X230,
  R-series, SL410, W500–W530, W700/W701, X300, Z60m/Z61m, Edge 14/E420, L412–L430,
  X1C Gen1) — these predate PSREF's per-model PDFs (they live only in giant consolidated
  withdrawn books) → left to the per-model search.
- HP → **support.hp.com** spec page `/us-en/product/product-specs/<slug>/<oid>`. 86/86
  filled (all rows). OIDs non-derivable; verified via indexed result titles (support.hp.com
  is a JS app). No PDF equivalent (HP QuickSpecs are messy family PDFs), so HTML spec page
  is the right target here.

**Unification notes (for the eventual merged all-brands table):** the hard part is
already done — all 3 CSVs share the identical 32-col header, so a merge is a concat keyed
on `brand`. `url` semantics = "official manufacturer SPEC page/sheet", never sales. Watch
items: (1) `url` KIND differs by brand by necessity — Dell = support-overview HTML,
ThinkPad = PSREF **PDF**, HP = support-specs HTML — all spec sources, fine; (2) the lone
sales outlier is Dell **Pro Plus 16** (dell.com/shop url) — swap when a spec page
verifies; (3) line endings: all CSVs are LF now (dell.csv was normalized; re-checked 2026-10-10); (4) grouped rows now use LEAD-model links across ThinkPad+HP
(Dell was mostly single-model already); a future "one url per grouped model" upgrade would
need a multi-url schema + renderer change (deferred). STILL OPEN: 44 ThinkPad blanks +
the 8 Dell clamshell blanks + Pro Plus spec page, if clean sources ever surface; optional
multi-url-per-group upgrade.

## 11. RS-232 serial port + Dell Rugged column (started 2026-10-05)
DONE: schema → 34 cols (`rs232`, `rs232_note`); "⊶ RS-232" toggle + panel row + search
terms on all 3 pages (+ landing search); report export shows the serial note as context.
Dell: Rugged/XFR rows moved to their own 🛡 Rugged column; added 5404, 7404, 7204, 7214,
7202/7212/7220/7030 tablets, Pro Rugged 13/14, XFR D630/E6400/E6420; 5420 Rugged = alias on
the 5424 row; ATG = aliases on D620/D630/E6400/E6410/E6420/E6430; 7230 renamed
"7230 Rugged Tab.". New rugged rows have NO price yet (needs an eBay sold pull).
Serial filled & sourced so far: all pre-2012 Dell C/D/E5x00–E5x20 + E6x00, every Rugged/XFR
row, HP 6930p / 6x40b–6x70b / 8x40p–8x70p, ThinkPad T20–R61 era (ThinkWiki list).
Findings worth knowing: on Dell E5500/E5510 and HP 6540b/6560b/6570b/8560p/8570p only the
15″ model has the port — the 14″ twin doesn't. Device Manager "PCI Serial Port" on
EliteBooks is Intel AMT Serial-over-LAN, NOT a physical port.
STILL OPEN: (a) modern rows (~2012+, all brands) are blank = "Unverified" — sweep
spec sheets to confirm 0s (Dell Setup&Specs ports table / PSREF / QuickSpecs);
(b) HP 8530w, 8760w, 8770w, ProBook 4x10s–4x40s, Dell E4200/E4300/E4310/E6410/Latitude 13
unchecked; (c) DONE since: HP ProBook 640/650 G1–G7 rows exist with rs232 filled (650 G1 = 1,
650 G2–G5 = 2, 640s = 0, 650 G7 = 0); (d) new rugged rows need eBay prices; (e) 7204/7214/7202/7212
chargers not audited.

## 12. CPU re-paste difficulty (started 2026-10-09)
DONE: schema → 36 cols (`repaste` 1–4, `repaste_note`); panel row "🔧 CPU re-paste" + cycle
filter button (any → ≤2 → ≤3 — ≤1 step dropped 2026-10-10 per SM, unverified hidden while active) + report context line,
all 3 pages; stamp 20261009. Seeded from SM hands-on only: Dell 3400 = 1, HP ProBook 650 G5 = 3.
DELL SWEEP DONE 2026-10-09: 146/164 Dell rows filled from Dell service/owner's manuals
(heat-sink removal prerequisites) — 50× L1, 54× L2, 30× L3, 13× L4; every note cites the manual.
Method: dl.dell.com directory listings (/topicspdf/ + esuprt_latitude_laptop/) read in the built-in
browser, PDFs parsed with pdf.js in-page; 2022+ models via dell.com/support/manuals HTML topic pages
(clamshell 7x10–7x50 manuals live under the "-2-in-1-laptop" product slug). Findings: E5250/E5440/
E5450/E5540/E5550/E7440/E7450/E6320/E6330/E4200/E4300/E4310/Latitude 13 = heatsink under the system
board (L4); 5480/5490/5590 manuals only document UMA (L1) — dGPU units differ; E5420/E5520/E5430/
E5530 = L1 via CPU door. Dell blanks left: Pro Plus 13/16, D400/D410/D420/D430, C400 (no heatsink
section in manual), 7370, 9510/9520 (Dell: heatsink ships attached to the board — note added),
3480/3580 (manual has screw table only), 3150-3190 edu, 7202/7030 tablets, Pro Rugged 13/14.
THINKPAD + HP SWEEP DONE 2026-10-10:
ThinkPad 131/145 (L1 5, L2 87, L3 30, L4 9) from Lenovo HMMs — "For access, remove these FRUs in
order" list for the thermal fan / heat sink FRU. Manual URLs via pcsupport.lenovo.com API
(/api/v4/mse/getproducts?productId=<token> → ParentID → /us/en/api/v4/contents/recommendmanualv2?pids=)
and, for pre-2012 models, the thinkpad-manuals.retropc.se mirror. Most 2013+ ThinkPads = L2 (one-piece
thermal fan assembly under the base cover); L14 Gen 1 (Intel)/Gen 3–5 and X13s = L1; E4x0/E5x0
2015–2017 = L4 (system board + thermal fan are one FRU); P50/P51/P52/P53/P72/P73 and W540/T540p = L4
(LCD + chassis/frame). Blanks: X200/X201, X220, X230, E420/E520, R30–R32, X300/X301 (old HMM text not
machine-readable), Z13/Z16 Gen 1–2, X1 Nano Gen 1, X1 Titanium (no HMM reached).
HP 83/98 (L1 31, L2 12, L3 17, L4 23) from HP Maintenance & Service Guides ("Before removing the heat
sink, follow these steps"). MSG links via support.hp.com /wcc-services/pdp/manuals/getManuals?productID=
<OID> (Akamai blocks it after ~1000 rapid calls — go slow). Grouped rows use the LEAD model's MSG,
except 820/840/850 G1–G2 where the 840/850 MSGs were also checked (all L3). Notable L4s: ProBook 440/450
G1–G4, 640/650 G2, 6470b/8470p/9470m, 2740p/2760p, EliteBook 840 G9, 845 G9/G10, 1040 G9–G11, x360 1030/
1040 G4–G8, ZBook Fury 16 G9/G10. 650 G5 = L3 matches SM hands-on. Blanks: 4420s, 640/650 G3, 650 G4,
640/650 G7, 440 G5, 2570p, x360 1030 G2/G3, ZBook 15 G2, Studio G3, Firefly G7, Fury G7/G8.
STILL OPEN: (a) 840/850 G3–G8 not checked separately (row level is from the 830/820 lead) — worth a look
since the 840 is the volume model; (b) the blanks above; (c) hands-on spot checks to calibrate — SM's hands-on machines first (calibration set),
then service manuals (the "before removing the heat sink" prerequisite list maps straight to
a level); (b) twins are likely but NOT assumed (640 G5 ≈ 650 G5, 3500 ≈ 3400) — confirm
before copying; (c) grouped rows can split (e.g. T480 vs T480s) → use the dominant level +
note, or 2-style "varies"; (d) optional chip-face marker for level 4 if it proves useful.

## 13. Rugged pages — Getac + Panasonic Toughbook (started 2026-10-10)
DONE: `getac.html` + `getac.csv` (62 rows, 2005–2026, tabs Semi / Convertibles / Tablets / Fully rugged)
and `panasonic.html` + `panasonic.csv` (66 rows, one chip per Mark, tabs Semi / Convertibles & 2-in-1 /
Tablets / Fully rugged). Landing page cards + quick search (loaded via `EXTRA_CSV` in index.html).
New on these two pages only: AND / `-exclude` search, 5-state ⊶ serial button, `unk` grey chips,
Toughbook part-number paste → Mark. SM decisions: separate pages for now ("maybe combine later"),
~20 years back, show models that fail requirements, Win 11 = nice-to-have not a requirement.
OPEN (grey chips / blank serial = the to-do list, search `portunknown` or click RAM ? legend):
- Getac: V110 G3/G4/G6, F110 G5, UX10 G2/G3/G4, A140 G1, K120 G1 — RAM type and serial unverified;
  S410 G3 CPU SKUs; B300 G4 label ↔ CPU mapping; "B300 G6 (DDR3)" Kingston oddity; S510 serial "0"
  is from the RPCR ports list — confirm against Getac's configurator.
- Panasonic: CF-19 mk4/mk5, CF-31 mk2, CF-52 mk1/mk4, CF-53 mk3, CF-33 mk2–mk4, FZ-40 mk3,
  FZ-G1 mk3/mk5, FZ-G2 mk2, FZ-M1 mk2, CF-D1 mk1/2 — CPU/RAM unverified (Mark + letters ARE verified).
  Panasonic OI PDFs for most of these exist on dl-pc-support.connect.panasonic.com/itn/manual/<series>/.
- Panasonic "Let's note"-based business Toughbooks (CF-F9, S10, SX2, AX2/3, LX3, MX4, XZ6) and
  Android devices not included yet.
- Getac ZX80W (Windows 8″, 2026) and G140 not included yet.
- Prices (both pages), chargers (`pwr` mostly blank — Panasonic CF-AA5713A 15.6V filled where an OI
  names it), re-paste levels (no public service manuals; hands-on units first).
- Candidate extra fields if SM wants to filter on them: hot-swap battery, IP rating, touch/digitizer.
  For now they live in `note` (searchable).

## ⚠ Build note — specdata.js cache stamp
The three HTML pages import the loader via `import('./specdata.js?b=YYYYMMDD')` (a cache
buster, because GitHub Pages caches JS ~10 min without revalidating). CSV fetches use
`{cache:'no-cache'}` so DATA edits show on a normal refresh with no stamp change. BUT
whenever `specdata.js` ITSELF changes, bump the `?b=` stamp in all three HTML files or
visitors keep running the stale loader. Current stamp: 20261009.

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
