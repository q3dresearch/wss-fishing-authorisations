# Pilot study: does one capture justify publishing this?

Run 2026-09-11 against the first capture, following step 10 of the wss research
sequence — *interrogate the finished charts before believing them*.

The capture: all three ICCAT exports, 4,380,450 + 6,673,620 + 252,050 bytes to
R2. Derived to 572,577 observations over 61,109 vessels.

## 1. Is any chart lying?

**43 of 43 published headline claims were recomputed from the derived rows by
code that does not import `visualize.py`, and all 43 reproduce exactly.** That
includes the three list sizes and column counts, the zero-overlap claim
recomputed from the vessel rows themselves, the 14,492 / 186 / 7 split, the
quota total, every reflagging and IMO share, all three median lengths, the four
operational codes and the France + Türkiye shares.

**And the central claim has an independent check from the publisher itself.**
ICCAT's twelve `_ddIF` columns are documented in its own `Readme.xlsx` as
*"SWO-N (days left active)"* and eleven more like it, with the convention stated
outright: *"[+] in force OR [-] expired"*. Their sign agrees with
`valid_to < today` on **all 26,081 windows — zero disagreements**. Two different
routes, one from the source and one from this parser, reach the same answer.

## 2. Did you merge categories that are not one thing?

**Two merges found, one fixed and one flagged as unverifiable.**

**Fixed.** The parser was storing `destroyed`, `delisted`, `scrapped` and `sunk`
as the observed values of `OperStatusCode`. ICCAT's `Readme.xlsx` documents
every other column in the export and says **nothing** about these four, so those
readings are a guess — and a guess in the archive is indistinguishable from a
fact once it is there. The codes now travel verbatim as `DEST`, `DELI`, `SCRP`,
`SUNK`. **`DELI` is the one that matters**: it reads as *delisted* and could as
easily be *delivered*, which would mean close to the opposite, and 423 of the
1,444 inoperative vessels turn on it.

**Flagged, not fixed.** The owner/operator split into "company" and "individual"
is done by a token regex, and there is **no second column to check it against** —
the export carries no organisation-type field. The regex is therefore
deliberately biased: a name is published in clear only when a corporate token
matches, so a misclassified individual stays hidden and a misclassified company
merely goes unnamed. That is a bias, not a validation, and it is stated in the
parser docstring and the README rather than presented as a classification.

A third, caught at the same time and not a merge but a mislabel: `_ddIF` was
called *an internal identifier per fishery*. It is the days-left countdown
above — the most useful column in the export, nearly discarded as noise.

## 3. Does any chart raise more than it answers?

**`expired-and-still-listed.svg` raised the biggest one and now answers most of
it.** Showing that 14,492 of 14,685 active vessels hold only expired
authorisations invites *"is the register dead, or has the 2026 cycle simply not
been entered?"* The chart could not answer that. It now carries the overdue
distribution from ICCAT's own countdown: **94.2% of overdue windows sit 181–365
days past expiry, median 254 days**, putting the mass on 31 December 2025 — an
annual authorisation year, unrenewed for eight and a half months. That is what
an un-entered cycle looks like, and it is now the leading reading rather than an
unstated one.

What it still cannot answer: the **714 windows (2.9%) more than a year overdue,
worst 619 days**. No annual cycle explains those, and the chart says so.

**`where-the-fleet-went.svg` raises "compared to what" by construction** and
answers it in its own subtitle: it is a stock comparison and is explicitly not
called a rate, because 44,980 inactive vessels accumulated over decades cannot
be divided by one snapshot of 14,685.

## 4. What must be read together?

- **`the-columns-that-vanish.svg` is the premise for everything else.** Without
  it, `expired-and-still-listed.svg` looks like a story about lapsed paperwork
  rather than about 54 columns being deleted at the exit.
- **`expired-and-still-listed.svg` is invalid without its own caveat block.**
  The headline number is not a finding and the chart says so in three lines.
  Cropped to the bar alone it would assert something the data does not support.
- **`one-hop-of-history.svg` bounds `where-the-fleet-went.svg`.** An IMO number
  is on 29.2% of active and 6.4% of inactive vessels, so any flag analysis that
  needs to follow individual hulls is capped by that, not by the flag counts.

## 5. What policy or prediction follows, and what does not?

**Follows.** A port state control officer or an importer cannot today establish
that a vessel was authorised on the date it fished, because the authorisation
window is deleted when the vessel leaves the active record and the transition
carries no date at all. That is a concrete gap in the Port State Measures
Agreement's evidence chain, and it is true from this single capture.

**Does not follow.** Nothing here says ICCAT's register is abandoned, that any
vessel is fishing illegally, or that any owner has done anything wrong. The
expired-window figure has an innocent reading that the evidence currently
favours. No departure, duration or rate can be reported from one frame — F1
through F9 all read *needs the archive* or *2 captures*.

## What the first two captures taught, four hours apart

The listener's first interval produced a finding about the listener.

The **inactive** export came back `changed` while the other two came back
`unchanged`. It was an identical **6,673,620 bytes**, 44,980 rows, **zero rows
gone, zero new, zero column differences** — and **19.3% of its lines in a
different position**. Sorting both bodies makes them byte-identical.

**ICCAT's export has non-deterministic row order, so `changed` in the manifest
carries no signal for this source.** The content hash will differ on most
captures while nothing has moved, and `dedupe_ignore` cannot fix it — it strips
regex-matched substrings, not row order. Anyone reading the manifest's outcome
column as "the fleet changed" will be wrong most months.

The derived table is unaffected: observations are keyed by entity, metric,
value and date, so re-parsing reordered identical content collapses to the same
rows. **Read the observations, not the outcome column.**

## Against the rest of the fleet

| | this repo | published fleet |
| --- | --- | --- |
| sources | 1 (three endpoints) | 1–48 |
| charts | 5 | 3–14 |
| questions with honest statuses | 11 | 0–15 |
| questions still `source not yet added` | 2 (IOTC/WCPFC/IATTC, and the IUU list) | 0–2 |

## Verdict

**Publishable, with the F2 caveat kept prominent.** The pilot found one
mislabel that would have put a guess in the archive, one that discarded the
single most useful column, and it surfaced an independent confirmation of the
central claim from the publisher's own data. Every headline reproduces.

The repository's own strongest claim is deliberately withheld: whether 14,492
lapsed authorisations mean a stalled register is **not** asserted, and the
October capture decides it. Publishing now is what makes that test possible.
