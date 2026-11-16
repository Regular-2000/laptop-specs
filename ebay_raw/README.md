# ebay_raw — raw eBay listing pulls

Main source for the site's "📦 Likely config (random unit)" row (odds of RAM / SSD size in a random unit
of a model, as it shows up for sale). Nothing here is interpreted — regroup it later without re-pulling.

| file | what |
|---|---|
| `<date>_active.json` | `{date, source, pulls:[{brand, model, query, url, status, total, items:[{id, cond, price, t}]}]}` — page 1 (240 cards) of an eBay ACTIVE-listing search per model, US-only, category 177, Best Match. `t` = listing title, `cond` = eBay condition label, `price` = as shown. Sponsored / other-model cards are included as eBay served them. |
| `<date>_latitude-7490_active.txt` | first test pull (7490 only, `item_id|condition|title`) |
| `row_map.csv` | which grid row (exact `model` cell of the brand CSV) each pull feeds, plus the title regexes that decide a card is that model (`must`) and not a neighbour (`exclude`) |

**PACE: ≥ 20 s between searches, ≤ 40 per sitting, ≥ 3 h between sittings, stop at the first 403 — see
TODO.md "eBay scraping pace". (Rapid 4–9 s gaps got search blocked on 2026-11-16.)**

How it is pulled: Claude in Chrome, one search page loaded, the others fetched same-origin from that tab
(~10 s apart), all kept in the page and saved as ONE download (Downloads → copied here). Plain HTTP from
the PC is refused by eBay; the cloud shell can't reach eBay at all.

Rebuild the site columns: `python3 tools/typ_build.py` (dry run) / `--write`. All counting rules live in
that script: identical titles counted once; lots, for-parts, spec ranges ("8-32GB", "up to") dropped;
odds rounded to 5 %, < 5 % hidden; < 50 usable listings = "(thin sample)".
