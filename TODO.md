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
verifies; (3) **line endings inconsistent**: dell.csv = CRLF, thinkpad.csv + hp.csv = LF
— normalize before/at merge; (4) grouped rows now use LEAD-model links across ThinkPad+HP
(Dell was mostly single-model already); a future "one url per grouped model" upgrade would
need a multi-url schema + renderer change (deferred). STILL OPEN: 44 ThinkPad blanks +
the 8 Dell clamshell blanks + Pro Plus spec page, if clean sources ever surface; optional
multi-url-per-group upgrade.

## ⚠ Build note — specdata.js cache stamp
The three HTML pages import the loader via `import('./specdata.js?b=YYYYMMDD')` (a cache
buster, because GitHub Pages caches JS ~10 min without revalidating). CSV fetches use
`{cache:'no-cache'}` so DATA edits show on a normal refresh with no stamp change. BUT
whenever `specdata.js` ITSELF changes, bump the `?b=` stamp in all three HTML files or
visitors keep running the stale loader. Current stamp: 20260802a.

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
