#!/usr/bin/env python3
"""Render charts from derived/observations/*.csv.gz as SVG.

    python examples/visualize.py

  the-columns-that-vanish.svg   the spine: 88 columns on the way in, 36 on the
                                way out, and what the missing 52 are
  expired-and-still-listed.svg  the one question with a one-month deadline
  how-a-vessel-leaves.svg       inactive and inoperative are two different
                                events wearing one label
  one-hop-of-history.svg        ICCAT keeps exactly one previous flag and one
                                previous name; reflagging is how vessels hide
  where-the-fleet-went.svg      flag composition of the three lists — a stock
                                comparison, deliberately not called a rate

Reads the derived table, never the raw archive. Stdlib only, deterministic
output: the same observations always produce the same bytes.
"""

from __future__ import annotations

import collections
import csv
import gzip
import io
import statistics
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "examples" / "charts"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
HUE = "#2a78d6"
HUE_SOFT = "#9ec5f4"
ACCENT = "#eb6834"
DEAD = "#b8b6ad"
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'

# Counted by diffing the three headers rather than eyeballed: 57 columns are
# on the active export and not on the exit exports, and THREE of those are
# renames (VMSSysCode -> VmsComSysCode, OwCtryCode -> OwCountry, OpCtryCode ->
# OpCountry) rather than losses. 54 are genuinely deleted. The exit exports
# gain two of their own: OperStatusCode and InactiveStatus.
VANISHED = [
    ("twelve authorisation windows × _DtFrom _DtTo _DtNotif", 36,
     "P20m SWOn SWOs ALBn ALBs TROP SWOm ALBm BFEc BFEo Carr Char"),
    ("the same twelve × _ddIF", 12, "an internal identifier per fishery"),
    ("BFEc_CatchQuota, BFEc_YearQuota", 2,
     "the bluefin quota the vessel held, and its year"),
    ("P20m_RM, TROP_RM", 2, "the recommendation it was listed under"),
    ("FlagRepCode, FlagChartTo", 2,
     "which party reported it, and who it is chartered to"),
]
# Columns that survive under a new name. Naming a rename as a loss is the same
# mistake as missing a real one, in the other direction.
RENAMED = [("VMSSysCode", "VmsComSysCode"), ("OwCtryCode", "OwCountry"),
           ("OpCtryCode", "OpCountry")]
CARRIED_OVER = 33  # 87 active columns minus the 54 deleted

FLAG_NAME = {
    "MAR": "Morocco", "EU-ITA": "Italy", "EU-CYP": "Cyprus", "EU-ESP": "Spain",
    "EU-MLT": "Malta", "TUN": "Tunisia", "DZA": "Algeria", "USA": "United States",
    "EU-GRC": "Greece", "EU-FRA": "France", "TUR": "Türkiye", "JPN": "Japan",
    "EU-PRT": "Portugal", "KOR": "Korea", "CHN": "China", "TWN": "Chinese Taipei",
    "LBY": "Libya", "EGY": "Egypt", "BRA": "Brazil", "MEX": "Mexico",
    "EU-HRV": "Croatia", "VEN": "Venezuela", "PAN": "Panama", "CIV": "Côte d'Ivoire",
}

LIST_LABEL = {"active": "Active", "inactive": "Inactive", "inoperative": "Inoperative"}


def _open(path: Path):
    if str(path).endswith(".gz"):
        return io.TextIOWrapper(gzip.open(path, "rb"), encoding="utf-8", newline="")
    return open(path, encoding="utf-8", newline="")


def load():
    """(vessels, feeds, flags, reasons, notified) from the derived table."""
    vessels = collections.defaultdict(dict)
    feeds = collections.defaultdict(dict)
    flags = collections.defaultdict(dict)
    reasons = {}
    notified = collections.Counter()
    for part in sorted((REPO / "derived" / "observations").glob("*.csv*")):
        with _open(part) as fh:
            for r in csv.DictReader(fh):
                eid, metric, value = r["entity_id"], r["metric"], r["value"]
                if eid.startswith("vessel:"):
                    vessels[eid][metric] = value
                elif eid.startswith("feed:"):
                    feeds[eid][metric] = value
                elif eid.startswith("flag:"):
                    flags[eid[5:]][metric] = value
                elif eid.startswith("reason:"):
                    reasons[eid[7:]] = value
                elif eid.startswith("authorisation:") and metric == "notified_at":
                    notified[value[:4]] += 1
    return vessels, feeds, flags, reasons, notified


def T(x, y, text, size=12, fill=INK, anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family=\'{FONT}\' font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(text))}</text>')


def R(x, y, w, h, fill, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" '
            f'height="{max(h, 0):.1f}" fill="{fill}" rx="{rx}"/>')


def L(x1, y1, x2, y2, stroke=GRID, width=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{width}"{d}/>')


def head(w, h, title, sub, note=""):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
         f'viewBox="0 0 {w} {h}">', R(0, 0, w, h, SURFACE),
         T(56, 48, title, 20, INK, weight="600"),
         T(56, 74, sub, 13, INK2)]
    lines = [note] if isinstance(note, str) else list(note)
    for i, line in enumerate(l for l in lines if l):
        p.append(T(56, 96 + i * 16, line, 12, MUTED))
    return p


def save(parts, name, w, h):
    OUT.mkdir(parents=True, exist_ok=True)
    svg = "\n".join(parts) + "\n</svg>\n"
    import xml.etree.ElementTree as ET
    ET.fromstring(svg)
    (OUT / name).write_text(svg, encoding="utf-8")
    print(f"  wrote examples/charts/{name}")


def flag_name(code: str) -> str:
    return FLAG_NAME.get(code, code)


# --- charts ---------------------------------------------------------------

def chart_columns_that_vanish(feeds):
    """88 cells, 36 of them kept. The spine, drawn as the columns themselves."""
    w, h = 940, 740
    act = int(feeds["feed:iccat:active"]["columns"])
    ina = int(feeds["feed:iccat:inactive"]["columns"])
    dropped = sum(n for _, n, _ in VANISHED)
    p = head(w, h, f"A vessel keeps its row and loses {dropped} columns",
             f"ICCAT's active export carries {act} columns. The inactive and "
             f"inoperative exports carry {ina}.",
             ["Zero serial numbers overlap between the three lists, so a vessel "
              "is in exactly one and MOVES between them.",
              "Each square below is one column of the active export. The orange "
              "ones do not survive the move, and no export records its date."])
    # A grid of the columns themselves: 36 kept, then the 52 that are not.
    cell, gap, per_row = 26, 6, 22
    gx, gy = 120, 180
    for i in range(act):
        r, c = divmod(i, per_row)
        x = gx + c * (cell + gap)
        y = gy + r * (cell + gap)
        p.append(R(x, y, cell, cell, HUE if i < CARRIED_OVER else ACCENT, rx=4))
    rows_used = (act + per_row - 1) // per_row
    legend_y = gy + rows_used * (cell + gap) + 18
    p.append(R(gx, legend_y, 14, 14, HUE, rx=3))
    p.append(T(gx + 22, legend_y + 12,
               f"{CARRIED_OVER} carried to the exit list ({len(RENAMED)} under a new name)",
               12, INK2))
    p.append(R(gx + 300, legend_y, 14, 14, ACCENT, rx=3))
    p.append(T(gx + 322, legend_y + 12, f"{dropped} deleted at the moment of exit",
               12, INK, weight="600"))

    y = legend_y + 54
    p.append(T(56, y, "What the deleted columns are", 14, INK, weight="600"))
    y += 26
    for label, n, detail in VANISHED:
        if not n:
            continue
        p.append(T(300, y, f"{n:>2}", 12, ACCENT, anchor="end", weight="600"))
        p.append(T(312, y, label, 12, INK, weight="600"))
        if detail:
            p.append(T(312, y + 15, detail, 10.5, MUTED))
            y += 15
        y += 24
    p.append(T(312, y + 4,
               "Renamed, not lost: "
               + ", ".join(f"{a} to {b}" for a, b in RENAMED), 11, MUTED))
    p.append(T(56, h - 52,
               "Nothing in the inactive export carries a date of any kind. "
               "44,980 vessels are marked inactive and not one says when.",
               13, INK, weight="600"))
    p.append(T(56, h - 30,
               "The inoperative export keeps a reason and still no date. That "
               "date is what two captures produce and one cannot.", 12, INK2))
    save(p, "the-columns-that-vanish.svg", w, h)


def chart_expired(vessels, feeds, notified):
    w, h = 940, 620
    f = feeds["feed:iccat:active"]
    total = int(f["vessels_listed"])
    lapsed = int(f["vessels_all_expired"])
    live = int(f["vessels_authorised"])
    none = int(f["vessels_no_window"])
    p = head(w, h, f"{lapsed:,} of {total:,} vessels on the ACTIVE record hold nothing valid",
             "Every authorisation window expired, and the vessel is still listed "
             "as active.",
             ["This is not yet a finding. From one capture there is no way to "
              "separate a stalled register from an annual cycle not yet entered,",
              "and it must not be published as one. What was ruled out: vStatus=1, "
              "vessAll=True and vessAll=False return byte-identical files.",
              "Two captures a month apart settle it, which is the whole argument "
              "for this repository."])
    x0, y0 = 300, 186
    bar = 520
    wl = bar * lapsed / total
    wv = bar * live / total
    p.append(R(x0, y0, wl, 28, ACCENT, rx=4))
    p.append(R(x0 + wl + 2, y0, wv, 28, HUE, rx=4))
    p.append(R(x0 + wl + wv + 4, y0, max(bar * none / total, 2), 28, DEAD, rx=4))
    p.append(T(x0 - 14, y0 + 19, f"{total:,} active vessels", 13, INK,
               anchor="end", weight="600"))
    p.append(T(x0, y0 + 52, f"{lapsed:,} — every window expired ({lapsed/total:.1%})",
               12, ACCENT, weight="600"))
    # Two captions on one line collided at every width tried. Second line.
    p.append(T(x0, y0 + 72,
               f"{live:,} hold an authorisation valid past today   ·   "
               f"{none} carry no window at all",
               12, INK2))

    y = y0 + 128
    p.append(T(56, y, "When the record was last told anything", 14, INK, weight="600"))
    y += 12
    # Read from the archive, never hardcoded: this chart's whole point is that
    # the last populated year keeps NOT advancing, so the year list has to be
    # able to advance on its own the month it does.
    span = range(min(int(y) for y in notified), max(int(y) for y in notified) + 2)
    years = {str(y): notified.get(str(y), 0) for y in span}
    mx = max(years.values())
    bw = max(int(700 / len(years)) - 12, 18)
    base = y + 190
    for i, (year, n) in enumerate(years.items()):
        x = 120 + i * (bw + 12)
        hgt = 150 * n / mx
        p.append(R(x, base - hgt, bw, max(hgt, 1.5), ACCENT if n == 0 else HUE, rx=3))
        p.append(T(x + bw / 2, base + 18, year, 11, INK if n else ACCENT,
                   anchor="middle", weight="600" if n == 0 else "normal"))
        p.append(T(x + bw / 2, base - hgt - 8, f"{n:,}", 10,
                   ACCENT if n == 0 else INK2, anchor="middle",
                   weight="600" if n == 0 else "normal"))
    p.append(L(104, base, 880, base, BASELINE, 2))
    empty = [y for y, n in years.items() if n == 0]
    p.append(T(56, base + 52,
               "Authorisation notifications by year (DtNotif). "
               + (f"Not one is dated {', '.join(empty)}." if empty
                  else "Every year in range is populated."),
               13, INK, weight="600"))
    save(p, "expired-and-still-listed.svg", w, h)


def chart_how_a_vessel_leaves(vessels, feeds, reasons):
    w, h = 940, 560
    lengths = collections.defaultdict(list)
    for eid, m in vessels.items():
        st = m.get("listed")
        ln = m.get("length_m")
        if st and ln:
            lengths[st].append(float(ln))
    p = head(w, h, "Inactive and inoperative are two different events",
             "ICCAT's two exit lists hold different fleets. The vessels that are "
             "destroyed, delisted, scrapped or sunk are much larger.",
             ["Median length overall, and what the inoperative export gives as a "
              "reason. Neither list carries a date.",
              "A vessel that quietly goes inactive and one that sinks are the "
              "same row in this archive until the reason is read."])
    x0, y0, row = 250, 180, 46
    mx = max(statistics.median(v) for v in lengths.values())
    for i, key in enumerate(("active", "inactive", "inoperative")):
        v = lengths.get(key, [])
        if not v:
            continue
        y = y0 + i * row
        med = statistics.median(v)
        p.append(T(x0 - 14, y + 13, LIST_LABEL[key], 13, INK, anchor="end", weight="600"))
        p.append(T(x0 - 14, y + 28, f"{len(v):,} with a length", 10, MUTED, anchor="end"))
        p.append(R(x0, y, 420 * med / mx, 18, ACCENT if key == "inoperative" else HUE, rx=4))
        p.append(T(x0 + 420 * med / mx + 10, y + 14, f"median {med:.1f} m", 12, INK2))

    y = y0 + 3 * row + 40
    p.append(T(56, y, "Why a vessel is inoperative", 14, INK, weight="600"))
    y += 24
    if reasons:
        tot = sum(int(v) for v in reasons.values())
        mxr = max(int(v) for v in reasons.values())
        for label, value in sorted(reasons.items(), key=lambda kv: -int(kv[1])):
            n = int(value)
            p.append(T(x0 - 14, y + 12, label, 12, INK, anchor="end"))
            p.append(R(x0, y, 420 * n / mxr, 16, HUE, rx=4))
            p.append(T(x0 + 420 * n / mxr + 10, y + 12, f"{n:,}  ({n/tot:.0%})", 11, INK2))
            y += 28
    p.append(T(56, y + 18,
               "The inactive export gives no reason at all — 44,980 vessels, one "
               "word, no date.", 13, INK, weight="600"))
    save(p, "how-a-vessel-leaves.svg", w, h)


def chart_one_hop(feeds):
    w, h = 940, 580
    p = head(w, h, "ICCAT keeps exactly one previous flag, and one previous name",
             "Reflagging is the standard way a vessel escapes a sanction. The "
             "record holds a single hop.",
             ["A vessel that changes flag twice between captures overwrites its "
              "own history, and one that changes annually for five years leaves",
              "a record showing one change. Every capture adds a link that would "
              "otherwise be lost. IMO numbers, which cannot be changed, are on a",
              "minority of rows — so a join to any other register rests on name "
              "and flag, both of which this source shows changing."])
    x0, y0 = 320, 200
    rows = []
    for key in ("active", "inactive", "inoperative"):
        f = feeds.get(f"feed:iccat:{key}")
        if not f:
            continue
        n = int(f["vessels_listed"])
        rows.append((LIST_LABEL[key], n,
                     int(f["renamed_listed"]), int(f["reflagged_listed"]),
                     int(f["with_imo"])))
    labels = [("previous name kept", 2, HUE), ("previous flag kept", 3, ACCENT),
              ("IMO / Lloyd's number", 4, HUE_SOFT)]
    y = y0
    for li, (label, idx, colour) in enumerate(labels):
        p.append(T(56, y, label, 13, INK, weight="600"))
        y += 22
        for name, n, *vals in rows:
            v = vals[idx - 2]
            share = v / n
            p.append(T(x0 - 14, y + 11, f"{name}  ({n:,})", 11, INK2, anchor="end"))
            p.append(R(x0, y, 400, 14, GRID, rx=4))
            p.append(R(x0, y, 400 * share, 14, colour, rx=4))
            p.append(T(x0 + 410, y + 11, f"{share:5.1%}   {v:,}", 11, INK2))
            y += 20
        y += 18
    p.append(T(56, y + 8,
               "29.2% of active vessels carry an IMO number and 6.4% of inactive "
               "ones do.", 13, INK, weight="600"))
    p.append(T(56, y + 30,
               "That is a cap on every join this archive can make, and a reason "
               "to record the chain while it is still visible.", 12, INK2))
    save(p, "one-hop-of-history.svg", w, h)


def chart_where_the_fleet_went(flags, feeds):
    w, h = 940, 620
    tot = {k: int(feeds[f"feed:iccat:{k}"]["vessels_listed"])
           for k in ("active", "inactive")}
    rows = []
    for code, m in flags.items():
        a = int(m.get("vessels_active", 0))
        i = int(m.get("vessels_inactive", 0))
        if a + i >= 500:
            rows.append((code, a, i))
    rows.sort(key=lambda r: -(r[1] + r[2]))
    rows = rows[:14]
    p = head(w, h, "France and Türkiye hold half of everything ICCAT has ever set aside",
             "Each flag's share of the 14,685 active vessels against its share of "
             "the 44,980 inactive.",
             ["This is a STOCK comparison and deliberately not called a rate. The "
              "inactive list accumulated over the register's whole history and",
              "cannot be divided by a single snapshot of the active one. Only "
              "observed transitions give a rate, and that needs two captures."])
    x0, y0, row = 230, 196, 28
    mx = max(max(a / tot["active"], i / tot["inactive"]) for _, a, i in rows)
    p.append(T(x0, y0 - 16, "share of ACTIVE", 11, HUE, weight="600"))
    p.append(T(x0 + 330, y0 - 16, "share of INACTIVE", 11, ACCENT, weight="600"))
    for n, (code, a, i) in enumerate(rows):
        y = y0 + n * row
        sa, si = a / tot["active"], i / tot["inactive"]
        p.append(T(x0 - 14, y + 12, flag_name(code), 12, INK, anchor="end"))
        p.append(R(x0, y, 250 * sa / mx, 16, HUE, rx=4))
        p.append(T(x0 + 250 * sa / mx + 6, y + 12, f"{sa:.1%}", 10, INK2))
        p.append(R(x0 + 330, y, 250 * si / mx, 16, ACCENT, rx=4))
        p.append(T(x0 + 330 + 250 * si / mx + 6, y + 12, f"{si:.1%}", 10, INK2))
    fra = next((r for r in rows if r[0] == "EU-FRA"), None)
    tur = next((r for r in rows if r[0] == "TUR"), None)
    if fra and tur:
        share = (fra[2] + tur[2]) / tot["inactive"]
        act = (fra[1] + tur[1]) / tot["active"]
        p.append(T(56, y0 + len(rows) * row + 34,
                   f"France and Türkiye are {act:.1%} of the active record and "
                   f"{share:.1%} of the inactive one.", 13, INK, weight="600"))
        p.append(T(56, y0 + len(rows) * row + 56,
                   "Whether that is one historic deregistration or a continuing "
                   "flow is exactly what a snapshot cannot say.", 12, INK2))
    save(p, "where-the-fleet-went.svg", w, h)


def main():
    vessels, feeds, flags, reasons, notified = load()
    if not vessels:
        raise SystemExit("no observations — run `wss derive --parsers parsers.iccat_vessel_v1` first")
    print(f"loaded {len(vessels):,} vessels, {len(flags)} flags")
    chart_columns_that_vanish(feeds)
    chart_expired(vessels, feeds, notified)
    chart_how_a_vessel_leaves(vessels, feeds, reasons)
    chart_one_hop(feeds)
    chart_where_the_fleet_went(flags, feeds)


if __name__ == "__main__":
    main()
