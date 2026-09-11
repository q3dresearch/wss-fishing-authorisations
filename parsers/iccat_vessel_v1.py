"""iccat-vessel.v1 — who may fish tuna in the Atlantic, and what is erased when
they stop.

THE DESTRUCTION IS COLUMNAR, NOT ROW-WISE, and that is why nobody has noticed.
ICCAT does not delete the vessel. It publishes the same fleet in three exports
with ZERO serial-number overlap -- active 14,685 rows and 88 columns, inactive
44,980 rows and 36, inoperative 1,444 and 36. A vessel is in exactly one list
and MOVES. The 52 columns that do not survive the move are the whole
authorisation history: twelve windows, the bluefin quota, the reporting flag,
the charter flag and the VMS system.

AND THE TRANSITION HAS NO DATE ANYWHERE. 44,980 vessels marked `inactive` and
not one says when. So `listed` is the observation: which of the three lists a
vessel was in, on a given month. A vessel whose `listed` changes between two
captures is the event, and there is no other way to see it.

FISHERIES ARE A SUB-ENTITY, NOT A METRIC SUFFIX. Twelve authorisation windows
x three dates would be 36 metric names, and a vocabulary that wide stops being
a vocabulary. `authorisation:<serial>:<fishery>` with valid_from / valid_to /
notified_at keeps three metrics and a closed twelve-value entity space.

PERSONAL DATA IS A PUBLICATION DECISION, NOT A COLLECTION ONE. OwName and
OpName are filled on 48.4% of active rows and mix companies (Rozafa shpk,
INTERA COMPANY SA) with individuals (HARROLL WEAVER, J GREER, SHAWN
TRUESDALE). Raw goes to object storage complete, because a vessel owner
disputing an enforcement action has no way to evidence what the register said
once ICCAT overwrites it. What is PUBLISHED here is an unsalted fingerprint
for everyone, plus the name in clear ONLY where a corporate token matches --
so a misclassified individual stays hidden and a misclassified company merely
goes unnamed. The error is made in the safe direction on purpose.

THE UNSALTED HASH IS DELIBERATE, same reasoning as wss-healthcare-exclusions.
ICCAT's own public export already names every owner currently on the record, so
a secret would guard nothing while risking an archive that cannot join to its
own history if the secret is lost.

LOAm REACHES 2,445 METRES. That is a data-entry error in the source, not a
vessel. Lengths outside 1-500 m are recorded as `length_invalid` rather than
dropped, because a quality defect that is silently discarded looks like clean
data to everyone downstream.

THE EXPORT IS CP1252, NOT UTF-8. Decoding it as UTF-8 raises on byte 0xdc, and
decoding with errors="replace" quietly turns Türkiye into T\ufffdrkiye and
ACUNA, AIME and ABDULHAMID into mojibake across thousands of vessel and owner
names. UTF-8 is tried strictly first so a future switch is picked up rather
than mangled, and cp1252 is the fallback.

TWO COLUMNS ARE RENAMED AT THE EXIT, NOT DROPPED. VMSSysCode becomes
VmsComSysCode, and OwCtryCode/OpCtryCode become OwCountry/OpCountry. Reading
only the active spelling would report a loss that did not happen, which is the
same error in the opposite direction from missing a real one.

AND ICCAT MISSPELLS ITS OWN HEADER. The inoperative export spells the operator
column `Op--Name` where the inactive export spells it `OpName` -- 436 of the
1,444 inoperative rows carry an operator and a parser reading only `OpName`
finds zero. Both spellings are accepted.
"""

import csv
import hashlib
import io
import re
from datetime import date

from wss import derive

PARSER_VERSION = "1"

# vStatus in the URL -> the state the row is in. These are the only three the
# export offers and the whole point is which one a vessel is in this month.
STATUS_BY_VSTATUS = {"1": "active", "2": "inactive", "3": "inoperative"}

# The twelve authorisation windows, exactly as the active export spells them.
# Closed by the source's own schema, so this is a vocabulary and not a slug.
FISHERIES = ("P20m", "SWOn", "SWOs", "ALBn", "ALBs", "TROP",
             "SWOm", "ALBm", "BFEc", "BFEo", "Carr", "Char")

# What ICCAT means by inoperative. No date accompanies any of them.
INOPERATIVE_REASON = {
    "DEST": "destroyed", "DELI": "delisted", "SCRP": "scrapped", "SUNK": "sunk",
}

# A name carrying one of these is a business. Matching is deliberately
# generous: a false positive names a company that might be a person's trading
# name, a false negative merely leaves a company unnamed. Only the first is a
# harm, so the list stays conservative -- no bare surnames, no initials.
CORPORATE = re.compile(
    r"\b(LTD|LTDA|LIMITED|S\.?A\.?|S\.?L\.?|S\.?R\.?L\.?|SARL|SNC|SPA|SCARL|"
    r"INC|LLC|L\.?L\.?C|CORP|CORPORATION|COMPANY|CO\.|GMBH|B\.?V\.?|N\.?V\.?|"
    r"A/S|APS|OY|AB|AS|PTE|SDN|BHD|SHPK|PESCA|PESCAS|PESQUERA|PECHE|PECHERIE|"
    r"FISHING|FISHERIES|SEAFOOD|TUNA|ARMEMENT|ARMADORA|GROUP|GROUPE|HOLDING|"
    r"HOLDINGS|ENTERPRISE|ENTERPRISES|INDUSTRIA|INDUSTRIES|MARINE|MARITIME|"
    r"SHIPPING|TRADING|COOPERATIVA|COOP|SOCIEDAD|SOCIETE|LDA|A\.?Ş\.?)\b",
    re.IGNORECASE)

BLANK = {"", "(blank)", "unk", "unknown", "n/a", "na", "nap", "-"}

# Columns that change name between the active export and the two exit exports.
# First spelling present wins.
ALIASES = {
    "vms_system": ("VMSSysCode", "VmsComSysCode"),
    "owner_country": ("OwCtryCode", "OwCountry"),
    "operator_country": ("OpCtryCode", "OpCountry"),
    # ICCAT's own header typo, inoperative export only.
    "operator_name": ("OpName", "Op--Name"),
    "owner_name": ("OwName",),
}

MIN_ROWS = {"active": 5_000, "inactive": 20_000, "inoperative": 300}


def _first(row: dict, names: tuple) -> str:
    """The first spelling of a renamed column that is actually present."""
    for name in names:
        if name in row:
            v = _clean(row.get(name))
            if v:
                return v
    return ""


def _clean(value) -> str:
    v = str(value or "").strip()
    return "" if v.lower() in BLANK else v


def _fingerprint(name: str) -> str:
    """Unsalted, so the archive can join to its own history for ever."""
    return hashlib.sha256(re.sub(r"\s+", " ", name).strip().upper().encode()).hexdigest()[:16]


def _iso(value) -> str:
    """ICCAT writes dd/mm/yyyy. Anything else is not a date."""
    v = _clean(value)
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", v)
    if not m:
        return ""
    d, mo, y = (int(x) for x in m.groups())
    try:
        return date(y, mo, d).isoformat()
    except ValueError:
        return ""


def _number(value):
    v = _clean(value).replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def _vstatus(url: str) -> str:
    m = re.search(r"vStatus=(\d)", url or "")
    return m.group(1) if m else ""


def parse(body: bytes, ctx: derive.ParseContext):
    vstatus = _vstatus(ctx.url)
    status = STATUS_BY_VSTATUS.get(vstatus)
    if not status:
        raise ValueError(
            f"iccat-vessel.v1: cannot tell which list this is. The url must carry "
            f"vStatus=1, 2 or 3 -- got {ctx.url!r}. Which list a vessel is in IS "
            f"the observation, so guessing would invent the finding")

    # Strict UTF-8 first so a future switch is noticed, cp1252 otherwise.
    # errors="replace" here would silently mangle every accented vessel name.
    try:
        text = body.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = body.decode("cp1252")
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    cols = reader.fieldnames or []
    if "ICCATSerialNo" not in cols:
        raise ValueError(
            f"iccat-vessel.v1: no ICCATSerialNo column in the {status} export. "
            f"Found {cols[:8]}")

    rows = 0
    seen: set[str] = set()
    flags: dict[str, int] = {}
    types: dict[str, int] = {}
    reasons: dict[str, int] = {}
    reflagged = renamed = with_imo = 0
    windows = expired = live = 0
    vessels_no_window = vessels_live = 0
    quota_total = 0.0
    quota_vessels = 0
    bad_length = no_length = 0
    all_expired_vessels = 0
    today = date.today().isoformat()

    for row in reader:
        rows += 1
        serial = _clean(row.get("ICCATSerialNo"))
        if not serial or serial in seen:
            continue
        seen.add(serial)
        eid = f"vessel:{serial}"

        # WHICH LIST. Without this a transition is invisible, because the
        # vessel row survives the move and nothing on it changes to say so.
        yield derive.Observation(eid, "listed", status, "state")

        name = _clean(row.get("VesselName"))
        if name:
            yield derive.Observation(eid, "name", name, "text")
        flag = _clean(row.get("FlagVesCode"))
        if flag:
            flags[flag] = flags.get(flag, 0) + 1
            yield derive.Observation(eid, "flag", flag, "state")

        # One hop is all ICCAT keeps. Every capture extends the chain by one
        # link that would otherwise be overwritten.
        prev_flag = _clean(row.get("FlagVesCodePrev"))
        if prev_flag:
            reflagged += 1
            yield derive.Observation(eid, "flag_previous", prev_flag, "state")
        prev_name = _clean(row.get("VesselNamePrev"))
        if prev_name:
            renamed += 1
            yield derive.Observation(eid, "name_previous", prev_name, "text")

        imo = _clean(row.get("IntRegNo"))
        if imo:
            with_imo += 1
            yield derive.Observation(eid, "imo", imo, "text")

        # Renamed at the exit rather than dropped -- read whichever spelling
        # this export uses, or the archive reports a loss that never happened.
        vms = _first(row, ALIASES["vms_system"])
        if vms:
            yield derive.Observation(eid, "vms_system", vms, "state")
        for metric in ("owner_country", "operator_country"):
            value = _first(row, ALIASES[metric])
            if value:
                yield derive.Observation(eid, metric, value, "state")

        vtype = _clean(row.get("IsscfvCode"))
        if vtype:
            types[vtype] = types.get(vtype, 0) + 1
            yield derive.Observation(eid, "vessel_type", vtype, "state")

        loa = _number(row.get("LOAm"))
        if loa is None:
            no_length += 1
        elif 1.0 <= loa <= 500.0:
            yield derive.Observation(eid, "length_m", round(loa, 2), "metre")
        else:
            # 2,445 m is in the active export. Recorded, not dropped: a defect
            # that is silently discarded looks like clean data downstream.
            bad_length += 1
            yield derive.Observation(eid, "length_invalid", round(loa, 2), "metre")

        # --- the 52 columns that exist only while the vessel is active ------
        if status == "active":
            for extra, metric in (("FlagRepCode", "flag_reporting"),
                                  ("FlagChartTo", "flag_chartered_to")):
                value = _clean(row.get(extra))
                if value:
                    yield derive.Observation(eid, metric, value, "state")

            quota = _number(row.get("BFEc_CatchQuota"))
            if quota:
                quota_vessels += 1
                quota_total += quota
                # ICCAT writes this in kilograms -- the median is 40,000 and
                # the fleet total 25,022,393, which is the bluefin TAC in kg,
                # not tonnes. Labelling it tonnes would inflate it a thousandfold.
                yield derive.Observation(eid, "quota_bluefin", quota, "kg")

            vessel_windows = vessel_live = 0
            for fishery in FISHERIES:
                frm = _iso(row.get(f"{fishery}_DtFrom"))
                to = _iso(row.get(f"{fishery}_DtTo"))
                notified = _iso(row.get(f"{fishery}_DtNotif"))
                if not (frm or to or notified):
                    continue
                aid = f"authorisation:{serial}:{fishery}"
                if frm:
                    yield derive.Observation(aid, "valid_from", frm, "date")
                if to:
                    yield derive.Observation(aid, "valid_to", to, "date")
                if notified:
                    yield derive.Observation(aid, "notified_at", notified, "date")
                if frm and to:
                    windows += 1
                    vessel_windows += 1
                    if to < today:
                        expired += 1
                    else:
                        live += 1
                        vessel_live += 1
            if not vessel_windows:
                # Six of them. Neither lapsed nor valid, and lumping them in
                # with either makes the headline wrong by six.
                vessels_no_window += 1
            elif not vessel_live:
                all_expired_vessels += 1
                # The state that needs a second capture before anyone repeats
                # it: on the active list with nothing left that is valid.
                yield derive.Observation(eid, "authorisation_lapsed", "yes", "state")
            else:
                vessels_live += 1

        if status == "inoperative":
            code = _clean(row.get("OperStatusCode"))
            if code:
                reasons[code] = reasons.get(code, 0) + 1
                yield derive.Observation(eid, "inoperative_reason",
                                         INOPERATIVE_REASON.get(code, code), "state")

        # --- owners and operators -------------------------------------------
        for key, role in (("owner_name", "owner"), ("operator_name", "operator")):
            who = _first(row, ALIASES[key])
            if not who:
                continue
            yield derive.Observation(eid, f"{role}_fp", _fingerprint(who), "text")
            if CORPORATE.search(who):
                yield derive.Observation(eid, role, who, "text")

    floor = MIN_ROWS[status]
    if rows < floor:
        raise ValueError(
            f"iccat-vessel.v1: only {rows} rows in the {status} export, expected "
            f"at least {floor}. September 2026 held 14,685 / 44,980 / 1,444. A "
            f"file this small is a truncated response, not a month in which the "
            f"Atlantic tuna fleet vanished")

    feed = f"feed:iccat:{status}"
    yield derive.Observation(feed, "vessels_listed", len(seen), "count")
    yield derive.Observation(feed, "rows_listed", rows, "count")
    yield derive.Observation(feed, "flags_listed", len(flags), "count")
    yield derive.Observation(feed, "reflagged_listed", reflagged, "count")
    yield derive.Observation(feed, "renamed_listed", renamed, "count")
    yield derive.Observation(feed, "with_imo", with_imo, "count")
    yield derive.Observation(feed, "length_invalid", bad_length, "count")
    yield derive.Observation(feed, "length_missing", no_length, "count")
    # The TSV ends every line with a tab, so csv gives a trailing empty column
    # name. Counting it would report 88 and 36 where the real shapes are 87
    # and 35, and the whole finding is a column count.
    yield derive.Observation(feed, "columns", len([c for c in cols if c]), "count")
    if status == "active":
        yield derive.Observation(feed, "windows_listed", windows, "count")
        yield derive.Observation(feed, "windows_expired", expired, "count")
        yield derive.Observation(feed, "windows_live", live, "count")
        yield derive.Observation(feed, "vessels_all_expired", all_expired_vessels, "count")
        yield derive.Observation(feed, "vessels_authorised", vessels_live, "count")
        yield derive.Observation(feed, "vessels_no_window", vessels_no_window, "count")
        yield derive.Observation(feed, "quota_vessels", quota_vessels, "count")
        yield derive.Observation(feed, "quota_bluefin_total", round(quota_total, 1), "kg")
    for flag, n in sorted(flags.items()):
        yield derive.Observation(f"flag:{flag}", f"vessels_{status}", n, "count")
    for vtype, n in sorted(types.items()):
        yield derive.Observation(f"vesseltype:{vtype}", f"vessels_{status}", n, "count")
    for code, n in sorted(reasons.items()):
        yield derive.Observation(f"reason:{INOPERATIVE_REASON.get(code, code)}",
                                 "vessels_listed", n, "count")


derive.register("iccat-vessel.v1", parse, PARSER_VERSION)
