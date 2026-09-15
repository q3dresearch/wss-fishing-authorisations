# Data shape

*Generated 2026-09-15T13:14:37Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **572,577 observations** across 1 partition(s), in **1 series**
  - `iccat.vessels.record` — 572,577 rows, **87295 entities**
- Raw: 0 file(s), 0 bytes on disk, 1 capture date(s), 2026-09-11 → 2026-09-11

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `iccat.vessels.record` | monthly | 3 | object | present | ICCAT publishes the Record of Vessels under Rec. 25-12 as a  |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **iccat.vessels.record** `authorisation:AT000AGO00002:ALBs`, `authorisation:AT000AGO00002:P20m`, `authorisation:AT000AGO00002:SWOs`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `authorisation_lapsed` | iccat.vessels.record | 14,492 | 14492 | text | state | 1 | `yes` |
| `columns` | iccat.vessels.record | 3 | 3 | number | count | 2 | `35` … `87` |
| `days_left` | iccat.vessels.record | 26,082 | 26082 | number | day | 184 | `-619` … `1419` |
| `flag` | iccat.vessels.record | 61,082 | 61082 | text | state | 71 | `AGO`, `ALB`, `BHS` |
| `flag_chartered_to` | iccat.vessels.record | 14,679 | 14679 | text | state | 5 | `---`, `EU-ITA`, `NAM` |
| `flag_previous` | iccat.vessels.record | 489 | 489 | text | state | 70 | `AUS`, `BHS`, `BLZ` |
| `flag_reporting` | iccat.vessels.record | 14,678 | 14678 | text | state | 52 | `AGO`, `ALB`, `BHS` |
| `flags_listed` | iccat.vessels.record | 3 | 3 | number | count | 3 | `31` … `66` |
| `imo` | iccat.vessels.record | 7,473 | 7473 | number | text | 4582 | `0000000` … `9998652` |
| `inoperative_code` | iccat.vessels.record | 1,444 | 1444 | text | state | 4 | `DELI`, `DEST`, `SCRP` |
| `length_invalid` | iccat.vessels.record | 3,083 | 3083 | number | count | 10 | `0.0` … `2575` |
| `length_m` | iccat.vessels.record | 58,002 | 58002 | number | metre | 909 | `1.0` … `499.0` |
| `length_missing` | iccat.vessels.record | 3 | 3 | number | count | 3 | `0` … `20` |
| `listed` | iccat.vessels.record | 61,109 | 61109 | text | state | 3 | `active`, `inactive`, `inoperative` |
| `name` | iccat.vessels.record | 60,886 | 60886 | text | text | 48809 | `'' FKHKA''`, `(n/a)`, `--` |
| `name_previous` | iccat.vessels.record | 7,901 | 7901 | text | text | 7328 | `'REEL CENTS'`, `(DESCONHECIDO)`, `--` |
| `notified_at` | iccat.vessels.record | 26,082 | 26082 | date | date | 352 | `2015-01-27` … `2025-12-31` |
| `operator` | iccat.vessels.record | 3,127 | 3127 | text | text | 2122 | `10474 (NFLD) LIMITED`, `18 Reeler Llc`, `2 SEA FISHERIES LLC` |
| `operator_country` | iccat.vessels.record | 20,989 | 20989 | text | state | 73 | `4493`, `Albania`, `Algerie` |
| `operator_fp` | iccat.vessels.record | 20,989 | 20989 | text | text | 15443 | `00034180bde59434`, `000901f471bcad48`, `00101c196a2c3598` |
| `owner` | iccat.vessels.record | 3,474 | 3474 | text | text | 2504 | `10474 (NFLD) LIMITED`, `18 Reeler Llc`, `2 SEA FISHERIES LLC` |
| `owner_country` | iccat.vessels.record | 20,989 | 20989 | text | state | 74 | `4493`, `Albania`, `Algerie` |
| `owner_fp` | iccat.vessels.record | 20,989 | 20989 | text | text | 16250 | `00034180bde59434`, `000901f471bcad48`, `00101c196a2c3598` |
| `quota_bluefin` | iccat.vessels.record | 438 | 438 | number | kg | 146 | `478.082468578431` … `750000.0` |
| `quota_bluefin_total` | iccat.vessels.record | 1 | 1 | number | kg | 1 | `25022393.2` … `25022393.2` |
| `quota_vessels` | iccat.vessels.record | 1 | 1 | number | count | 1 | `438` … `438` |
| `reflagged_listed` | iccat.vessels.record | 3 | 3 | number | count | 3 | `42` … `238` |
| `renamed_listed` | iccat.vessels.record | 3 | 3 | number | count | 3 | `191` … `4185` |
| `rows_listed` | iccat.vessels.record | 3 | 3 | number | count | 3 | `1444` … `44980` |
| `valid_from` | iccat.vessels.record | 26,082 | 26082 | date | date | 442 | `2006-01-01` … `2025-08-18` |
| `valid_to` | iccat.vessels.record | 26,082 | 26082 | date | date | 185 | `2024-12-31` … `2030-07-31` |
| `vessel_type` | iccat.vessels.record | 61,083 | 61083 | text | state | 25 | `---`, `AU`, `DO` |
| `vessels_active` | iccat.vessels.record | 73 | 73 | number | count | 54 | `1` … `4151` |
| `vessels_all_expired` | iccat.vessels.record | 1 | 1 | number | count | 1 | `14492` … `14492` |
| `vessels_authorised` | iccat.vessels.record | 1 | 1 | number | count | 1 | `186` … `186` |
| `vessels_inactive` | iccat.vessels.record | 88 | 88 | number | count | 65 | `1` … `17832` |
| `vessels_inoperative` | iccat.vessels.record | 48 | 48 | number | count | 23 | `1` … `734` |
| `vessels_listed` | iccat.vessels.record | 7 | 7 | number | count | 7 | `11` … `44980` |
| `vessels_no_window` | iccat.vessels.record | 1 | 1 | number | count | 1 | `7` … `7` |
| `vms_system` | iccat.vessels.record | 10,608 | 10608 | text | state | 9 | `3991,96`, `ARGOS`, `INMSAT` |
| `windows_expired` | iccat.vessels.record | 1 | 1 | number | count | 1 | `25033` … `25033` |
| `windows_listed` | iccat.vessels.record | 1 | 1 | number | count | 1 | `26081` … `26081` |
| `windows_live` | iccat.vessels.record | 1 | 1 | number | count | 1 | `1048` … `1048` |
| `with_imo` | iccat.vessels.record | 3 | 3 | number | count | 3 | `302` … `4288` |

## Partitions

- `derived/observations/2026-09.csv.gz`
