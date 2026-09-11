# What an archive of the ICCAT Record of Vessels is for

Written before the registry, because the rule is: probe the shape, write the
questions down, name who acts on them, try to answer them from what you already
have — and only then decide what to build. Most questions die at the fourth
step, and that is the point.

The screening that chose this source is in `webprobes/catalogue.csv` under
`iccat.vessels.record`, and the rule that found it is in
`webprobes/doctrine/who-else-is-listening.md` under *"count the columns on both
sides of the exit"*.

## The spine

**ICCAT does not delete the vessel. It deletes fifty-four columns about it,
and never records when.**

**And its sister commission does not.** IATTC's register was pulled on
2026-09-11 as the control: 29 columns on the live register and **29 on the
inactive/sunk export**, `first inclusion` filled on 100% of 4,725 vessels back
to 2002, and the transition narrated in prose — *"Sunk on 22 Dec 2024."*,
*"Vanuatu - Change to Belize notified on 14 Jul 2026 (recorded on 16 Jul 2026)
- Vessel name at time of change: Nine Lucky No. 6"*. So this is not how
fisheries registers work. It is how **this** one works.

That is a subtler destruction than the usual wss case and it is worth stating
precisely, because "the row is still there" is exactly why nobody has noticed.

ICCAT publishes the same vessels in three exports. Fetched 2026-09-11:

| | rows | columns |
| --- | --- | --- |
| **Active** (`vStatus=1`) | 14,685 | **87** |
| **Inactive** (`vStatus=2`) | 44,980 | **35** |
| **Inoperative** (`vStatus=3`) | 1,444 | 35 |

**Zero serial numbers overlap between the three.** A vessel is in exactly one
list and *moves* between them. Diffing the three headers rather than eyeballing
them: 57 columns are on the active export and not on the exit exports, **three
of those are renames**, and **54 are genuinely deleted**:

| | columns | what they are |
| --- | --- | --- |
| twelve authorisation windows × `_DtFrom` `_DtTo` `_DtNotif` | 36 | `P20m` `SWOn` `SWOs` `ALBn` `ALBs` `TROP` `SWOm` `ALBm` `BFEc` `BFEo` `Carr` `Char` |
| the same twelve × `_ddIF` | 12 | **days left on that authorisation** — ICCAT's own countdown, negative when overdue |
| `BFEc_CatchQuota`, `BFEc_YearQuota` | 2 | the bluefin quota the vessel held, and its year. 438 active vessels carry one, **25,022,393 kg between them** |
| `P20m_RM`, `TROP_RM` | 2 | the recommendation it was listed under |
| `FlagRepCode`, `FlagChartTo` | 2 | which party reported it, who it is chartered to |

Renamed rather than lost, and worth stating because calling a rename a deletion
is the same error in the other direction: `VMSSysCode` to `VmsComSysCode`,
`OwCtryCode` to `OwCountry`, `OpCtryCode` to `OpCountry`. The exit exports gain
two of their own — `OperStatusCode` and `InactiveStatus`.

And the inactive export carries **no date of any kind**. 44,980 vessels marked
`inactive` and not one says when. The inoperative export keeps a *reason* —
`DEST` 812, `DELI` 423, `SCRP` 198, `SUNK` 11 — and still no date.

So: the date a vessel stopped being authorised to fish tuna in the Atlantic
exists nowhere, and is recoverable only by holding two captures.

## The number that needs a second capture before anyone repeats it

Of the 14,685 vessels on the **active** record, as the parser counts them:

| | vessels |
| --- | --- |
| every authorisation window already expired | **14,492** |
| holds at least one window valid past today | **186** |
| carries no authorisation window at all | 7 |

25,033 of the 26,081 windows (96%) have already expired. `SWOm`, `ALBm`, `BFEc` and
`BFEo` are **100% expired**. And **no authorisation in the file is dated 2026
at all** — `DtNotif` runs 2015–2025 with 19,676 in 2025 and **zero in 2026**;
`DtFrom` likewise.

**This is not yet a finding, and it must not be published as one.** From a
single capture there is no way to tell the difference between:

1. the record genuinely holding 14,492 vessels whose authorisation lapsed and
   which nobody has moved to the inactive list, and
2. an annual notification cycle that has not been entered yet, or an export
   regenerated from a database that stopped being updated.

**ICCAT's own `_ddIF` columns narrow it, and they narrow it towards (2).** Its
`Readme.xlsx` names them *"SWO-N (days left active)"* and eleven more like it,
and states the convention outright — authorisation status is *"[+] in force OR
[-] expired"*. So the publisher itself publishes a countdown, and the
distribution of overdue windows is one cohort, not a spread:

| how overdue | windows | share |
| --- | --- | --- |
| within 90 days | 160 | 0.6% |
| 91–180 days | 589 | 2.4% |
| **181–365 days** | **23,571** | **94.2%** |
| 366–547 days | 699 | 2.8% |
| 548+ days | 15 | 0.1% |

Median **254 days** overdue, which puts the mass on **31 December 2025** — the
end of an annual authorisation year — unrenewed in the eight and a half months
since. That is what an un-entered 2026 cycle looks like, and it is the leading
hypothesis rather than a stalled register.

**714 windows (2.9%) are more than a year past expiry**, and no annual cycle
explains those. Worst is **619 days**. Whatever the answer to F2 turns out to
be, that smaller population is a separate question.

What was ruled out: there is no hidden date filter. `vStatus=1`,
`vessAll=True&vStatus=1` and `vessAll=False&vStatus=1` return **byte-identical
4,380,450-byte files with the same 14,685 rows** — `vessAll` is ignored, and
the page's only other controls are flag, keyword, type and sort order. The
`Last-Modified` header is useless: it equals the request time, because the
export is generated per request.

**Two captures one month apart settle it**, which is the strongest possible
argument for this repository existing and the reason it ships with the claim
written down rather than dressed up.

## Flag-hopping, and the chain that gets overwritten

Reflagging is the classic way a vessel escapes a sanction, and ICCAT keeps
exactly **one** previous value:

| field | filled on the 14,685 active |
| --- | --- |
| `VesselNamePrev` | 4,185 (28.5%) |
| `FlagVesCodePrev` | 238 (1.6%) |

One hop. A vessel that changes flag twice between captures overwrites its own
history, and a vessel that changes flag once a year for five years leaves a
record showing one change. A monthly capture turns that single field into a
chain.

The flag composition also does something unexpected, and it is a **stock**
comparison rather than a rate — the inactive pile is cumulative over the
register's whole history:

| flag | active | inactive |
| --- | --- | --- |
| Morocco | 4,151 (28.3%) | 812 (1.8%) |
| **France** | 343 (2.3%) | **14,962 (33.3%)** |
| **Türkiye** | 333 (2.3%) | **7,712 (17.1%)** |
| Italy | 2,250 (15.3%) | 8,674 (19.3%) |
| Japan | 164 (1.1%) | 68 (0.2%) |

France and Türkiye hold half of everything ICCAT has ever marked inactive
between them, on 4.6% of the current record. Whether that is one historic
deregistration or a continuing flow is exactly what the archive answers and a
snapshot cannot.

## The questions

One status — `source not yet added` — is the only one that justifies another
registry entry.

| # | question | needs | status |
| --- | --- | --- | --- |
| F1 | **When does a vessel stop being authorised, and what was it authorised for?** | 2 captures | **the founding question.** The transition date is recorded nowhere, and the twelve authorisation windows are deleted at the moment of transition. Unanswerable from any single frame and from any other source |
| F2 | Is the active record live, or has it stopped being maintained? | **2 captures** | **the one question with a one-month deadline.** 14,492 of 14,685 vessels hold only expired windows and nothing in the file is dated 2026. If October's capture is identical, the record is stale and that is a compliance story; if 2026 notifications appear, this measures notification lag. Either answer is worth having and neither is available today |
| F3 | How long does an ICCAT authorisation actually run, end to end? | ~12 months | needs the archive. `DtFrom`/`DtTo` give the *scheduled* window; whether a vessel is renewed, lapses quietly, or leaves before its `DtTo` needs consecutive captures |
| F4 | Do vessels reflag more than once, and where to? | ~12 months | needs the archive. `FlagVesCodePrev` holds one hop and is filled on 238 of 14,685. Every capture extends the chain by one link that would otherwise be overwritten |
| F5 | Was a departure an enforcement action or an ordinary exit? | a source | **`source not yet added`** — ICCAT's IUU list at `/Data/IUU/IUU.xlsx` is the other half, and it is a larder: 163 vessels back to 2004 with `Date Included On List` intact, exactly as the incentive rule predicts. Fetch it ONCE as a join control. A vessel that leaves the active record AND appears there left for a completely different reason than one that quietly went inactive |
| F6 | Is this a property of tuna RFMOs or one secretariat's habit? | **answered against IATTC, 2026-09-11** | **It is ICCAT's habit, and that makes the claim sharper rather than weaker.** IATTC's Regional Vessel Register was pulled and diffed: **29 columns on the register and 29 on the inactive/sunk export — nothing is dropped at the exit.** `Register Status` is a real status changed in place (Active 4,713 / Inactive 9 / Sunk 3) rather than a move between lists; `first inclusion` is filled on **100% of 4,725 vessels** back to 2002; `Notes` carries the transition date in prose; and `Previous flag` narrates the change with both dates and the vessel's name at the time. **IATTC records precisely what ICCAT deletes.** IOTC and WCPFC remain untested |
| F12 | Does anyone keep a flag-hop chain longer than one? | **answered, and nobody does** | IATTC describes its one previous flag far better than ICCAT — with the notification date, the recording date and the name at the time — but **0 of its 234 previous-flag entries narrate more than one change.** Both commissions keep exactly one hop. The chain is only reconstructable from consecutive captures, at either |
| F7 | Which flags account for departures against their share of the standing record? | ~12 months | needs the archive. The stock comparison above is not a rate: 44,980 inactive vessels accumulated over decades cannot be divided by a 14,685-vessel snapshot and called a departure rate. Only observed transitions can |
| F8 | What happens to the bluefin quota when a vessel leaves? | ~6 months | needs the archive. 438 active vessels carry `BFEc_CatchQuota`, 25,022,393 kg between them, and the column does not exist on the inactive export. Whether a departing vessel's quota reappears on another vessel is a question about how quota is actually traded, and it is invisible from one frame |
| F9 | Is the fleet getting smaller or just smaller-vessel? | ~12 months | needs the archive. Median length overall is **9.0 m on the active record, 6.8 m inactive and 25.1 m inoperative** — the vessels that are destroyed, delisted, scrapped or sunk are four times the length of the ones that merely go inactive. Those are two different events wearing one label |
| F10 | How identifiable are these vessels? | **answered, and it limits every join.** | An IMO/Lloyd's number is present on **4,288 of 14,685 active vessels (29.2%)** and **2,883 of 44,980 inactive (6.4%)**. Without it a join to any other registry rests on name and flag, both of which this source shows changing. That is a cap on F5 and F6, not a reason to skip them |
| F11 | Is the data clean enough to measure? | **answered, and partly not.** | `LOAm` reaches **2,445 m** on the active record — a vessel two and a half kilometres long. 499 active rows fall outside 1–500 m and 7 carry no length at all; the inactive export has 2,575 more. Anything computed on length needs a sanity bound, and the archive should record the bad values rather than silently drop them |

## Who acts on these, and what changes

Each row names a decision, not a sector. A question with no name against it is
trivia, and trivia does not justify a job that runs for years.

| who | questions | the decision it changes |
| --- | --- | --- |
| **IUU-fishing investigators** (Trygg Mat Tracking, Global Fishing Watch, EJF) | F1, F4, F5 | which vessel to investigate. A vessel that leaves an authorisation record and reappears under a new flag is the canonical evasion pattern, and today the before-state is deleted at the moment it becomes interesting |
| **Port state control officers** | F1, F10 | whether a vessel presenting itself was authorised *at the time it fished*, not just today. The Port State Measures Agreement turns on exactly that question and the answer is currently unreconstructable |
| **Seafood supply-chain due diligence** | F1, F5, F8 | whether a catch came from an authorised vessel on the date of the catch. An importer can check today's record; nobody can check last March's |
| **The ICCAT Compliance Committee** | F2, F7 | whether parties are notifying on time. ICCAT holds this internally and publishes no series, and F2 suggests the public record may itself be the evidence |
| **Quota researchers and fisheries economists** | F8 | how bluefin quota moves between vessels. 25,022,393 kg is allocated per vessel and the allocation vanishes with the vessel |
| **Anyone building the RFMO comparison** | F6 | whether "registers delete their authorisation history" is a fact about fisheries governance or about one secretariat |

**Who this is NOT for.** Anyone wanting today's list of authorised vessels.
That is ICCAT's own export, free, unauthenticated and better than anything
here. This archive answers the opposite question — who used to be on it, for
what, and until when.

## What would make this worth stopping

1. ICCAT adds a date to the inactive export. One column — the date the vessel
   left the active record — makes F1 a query and most of this table citations.
2. The authorisation windows migrate to the inactive schema. Then the history
   is kept by the publisher and this becomes a larder.
3. F2 resolves as "stale": if the record has genuinely stopped being maintained
   and stays frozen for six months, there is nothing left to listen to and the
   right output is a written note, not a job.

## Three things the source calls something other than what I assumed

**`_ddIF` is "days left active", not an identifier.** The first parser called
the twelve `_ddIF` columns *an internal identifier per fishery* on the strength
of their values (−254, −255, 323). They are a countdown, documented in ICCAT's
own `Readme.xlsx`, and they are the publisher's own answer to the question this
repository asks. **Their sign agrees with `valid_to < today` on all 26,081
windows — zero disagreements** — which is the strongest independent check
available on the central claim here, and it comes from the source itself.

**`DEST`, `DELI`, `SCRP` and `SUNK` are not defined by ICCAT anywhere.** The
`Readme.xlsx` documents every other column in the export and says nothing about
`OperStatusCode`. The first parser stored `delisted`, `destroyed`, `scrapped`
and `sunk` as the observed values, which would have put a guess in the archive
indistinguishable from a fact. The codes now travel verbatim, and the reading
appears only on the chart, marked as a guess. **`DELI` is the one that matters:
it reads as "delisted" and could as easily be "delivered"**, which would mean
close to the opposite — 423 of 1,444 inoperative vessels turn on it.

## Two defects in the source, found by parsing it

Both were found by reading the bytes rather than the documentation, and both
would have silently produced wrong output.

**The export is cp1252, not UTF-8.** It raises on byte `0xdc`, and decoding
with `errors="replace"` quietly turns Türkiye into `T\ufffdrkiye` and mangles
`ACUÑA`, `AIMÉ`, `SALAIÑO` and `ABDÜLHAMID` across thousands of vessel and
owner names. The parser tries UTF-8 strictly first, so a future switch is
noticed instead of mangled, and falls back to cp1252.

**ICCAT misspells its own header.** The inoperative export spells the operator
column `Op--Name` where the inactive export spells it `OpName`. **436 of the
1,444 inoperative rows carry an operator**, and a parser reading only `OpName`
finds zero of them — a clean, plausible, entirely false answer.

## Personal data

`OwName`, `OpName` and their addresses are filled on 7,110 of 14,685 active
vessels (48.4%) and 13,443 of 44,980 inactive (29.9%). Most are companies —
`Rozafa shpk`, `INTERA COMPANY SA` — but plenty are plainly individuals:
`HARROLL WEAVER`, `J GREER`, `SHAWN TRUESDALE`, `DIEGO SUAREZ`.

Raw goes to object storage **complete**, because the record cuts both ways: a
vessel owner disputing an enforcement action has no way to evidence what the
register said in 2025 once ICCAT overwrites it. What is *published* is
fingerprinted for individuals and named in clear for companies — the same split
as `wss-healthcare-exclusions`, for the same reason.
