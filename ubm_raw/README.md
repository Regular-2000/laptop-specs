# ubm_raw — raw UserBenchmark system-page pulls

Everything the site's "📦 Typical config (as found)" row is built from. Nothing here is
interpreted — regroup it any way you like later without re-pulling.

| file | what |
|---|---|
| `<date>.jsonl` | one line per system page: `{date, u (page URL), sys, n (PCs on that page), rows}` |
| `<date>.wire.txt` | the same data in the plain text form it was copied out of the browser (kept as a second copy) |
| `system_map.csv` | `ubm_id,brand,model,label` — which grid row (exact `model` cell) a system page feeds; several systems may point at one row |

`rows` entries are `COMP|name|brand|count|ubm_component_id`:
- `COMP` = CPU / GPU / SSD / HDD / RAM (whatever tables the page showed; top-5 parts each).
- `name`, `brand` = exactly as UserBenchmark prints them (their brand column is unreliable for
  SSD/RAM — e.g. "PC", "Nvme", "Unknown" — and for soldered RAM the die part number lands there).
- `count` = how many PCs of THIS model were seen with that part.
- `ubm_component_id` = their component id (same part = same id across models).
- Not kept: the site-wide "Bench x %, n samples" line (it describes the part globally, not this model).

Integrity: each pull was checked against a checksum computed in the page (row count, sum of
counts, text lengths) before the .jsonl was written.

Rebuild the site columns: `python3 tools/typ_from_ubm.py` (dry run) / `--write`.
Flat, spreadsheet-friendly copy of the same rows: `../ubm_stats.csv` (started July 2026, CPU + RAM
only back then; SSD / GPU rows from 2026-11-16 on).
