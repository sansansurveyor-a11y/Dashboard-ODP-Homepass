#!/usr/bin/env python3
"""Buat data.json untuk dashboard dari file Excel ODP.

Pemakaian:
    python build_data.py Summary_ODP.xlsx            # menulis data.json
    python build_data.py Summary_ODP.xlsx hasil.json # nama keluaran lain
    python build_data.py Summary_ODP.xlsx data.json --modified 2026-11-26T07:51:22.000Z
        # --modified: waktu file sumber diubah (UTC); bawaannya waktu ubah file lokal

Kebutuhan: Python 3 dengan pandas dan openpyxl (pip install pandas openpyxl).
Aturan hitung sama dengan dashboard: satu baris ODP = satu ODP, ODP ID kembar
dilewati, baris dengan port kosong atau nol dilewati, homepass = jumlah port.
"""
import datetime
import json
import os
import re
import sys

import pandas as pd

UNK = "Tidak diketahui"


def norm(v):
    return re.sub(r"[\s_]+", " ", str(v if v is not None else "").lower()).strip()


def find_table(path):
    sheets = pd.read_excel(path, sheet_name=None, header=None)
    for name, raw in sheets.items():
        for i in range(min(len(raw), 15)):
            heads = [norm(x) if pd.notna(x) else "" for x in raw.iloc[i].tolist()]
            if "segment" in heads and "port" in heads:
                df = raw.iloc[i + 1 :].copy()
                df.columns = heads
                return name, df
    sys.exit('Kolom "Segment" dan "port" tidak ditemukan di sheet mana pun.')


def text(series):
    s = series.astype("string").str.strip()
    return s.fillna(UNK).replace("", UNK)


def main():
    args = sys.argv[1:]
    modified_arg = None
    if "--modified" in args:
        k = args.index("--modified")
        modified_arg = args[k + 1] if k + 1 < len(args) else None
        del args[k : k + 2]
    if not args:
        sys.exit(__doc__)
    src = args[0]
    out = args[1] if len(args) > 1 else "data.json"
    sheet, df = find_table(src)

    df["port"] = pd.to_numeric(df["port"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    bad = ~(df["port"] > 0)
    invalid = int(bad.sum())
    df = df[~bad]

    dup = 0
    id_col = next((c for c in ("odp id", "odp") if c in df.columns), None)
    if id_col:
        ids = df[id_col].astype("string").str.strip()
        is_dup = ids.notna() & (ids != "") & ids.duplicated()
        dup = int(is_dup.sum())
        df = df[~is_dup]

    for col in ("region", "stasiun"):
        df[col] = text(df[col]) if col in df.columns else UNK
    vend = next((c for c in df.columns if c.startswith("vendor")), None)
    df["vendor"] = text(df[vend]) if vend else UNK
    df["segment"] = text(df["segment"])

    g = df.groupby(["segment", "region", "stasiun", "vendor", "port"]).size().reset_index(name="n")
    rows = []
    for seg, reg, sta, ven, port, n in g.itertuples(index=False):
        p = float(port)
        rows.append([seg, reg, sta, ven, int(p) if p.is_integer() else p, int(n)])

    if modified_arg:
        modified_str = modified_arg
    else:
        m = datetime.datetime.fromtimestamp(os.path.getmtime(src), datetime.timezone.utc)
        modified_str = m.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    meta = {
        "file": os.path.basename(src),
        "sheet": sheet,
        "odpRows": int(len(df)),
        "dup": dup,
        "invalid": invalid,
        "at": None,
        "driveModified": modified_str,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "rows": rows}, f, ensure_ascii=False, separators=(",", ":"))
    hp = sum(r[4] * r[5] for r in rows)
    print(f"{out}: {meta['odpRows']:,} ODP, {hp:,.0f} homepass, {len(rows):,} baris agregat")


if __name__ == "__main__":
    main()
