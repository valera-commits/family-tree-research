#!/usr/bin/env python3
"""Export the fan tree (tree.json) to GEDCOM 5.5.1, readable by most genealogy programs.

Usage: python3 gedcom_export.py tree.json out.ged

Each person becomes INDI, each father+mother pair a FAM. Years, places, notes and the
evidence level (c: d = document, f = family / hypothesis) go into NOTE records, so the
level of proof travels with the tree.
"""
import json, re, sys
from datetime import date


def year_of(y, idx):
    """'≈1765 – после 1794' -> ('ABT 1765', 'AFT 1794'); idx 0 birth, 1 death."""
    if not y:
        return None
    parts = re.split(r"\s*[–-]\s*", y)
    if idx >= len(parts):
        return None
    s = parts[idx].strip()
    m = re.search(r"(\d{4})", s)
    if not m:
        return None
    yr = m.group(1)
    if "после" in s:
        return f"AFT {yr}"
    if "до " in s:
        return f"BEF {yr}"
    if "≈" in s or "-е" in s or "ок" in s:
        return f"ABT {yr}"
    return yr


def esc(s):
    return str(s).replace("@", "@@").replace("\n", " ")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    tree = json.load(open(sys.argv[1], encoding="utf-8"))
    people = tree["people"]
    ids = {p: f"@I{i + 1}@" for i, p in enumerate(sorted(people, key=lambda k: (len(k), k)))}
    fams, fam_of_child = {}, {}
    for p in people:
        f, m = p + "F", p + "M"
        if f in people or m in people:
            fid = f"@F{len(fams) + 1}@"
            fams[fid] = (f if f in people else None, m if m in people else None, p)
            fam_of_child[p] = fid
    spouse_fams = {}
    for fid, (f, m, _) in fams.items():
        for x in (f, m):
            if x:
                spouse_fams.setdefault(x, []).append(fid)

    out = ["0 HEAD", "1 SOUR family-tree-research", "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED",
           "1 CHAR UTF-8", f"1 DATE {date.today().strftime('%d %b %Y').upper()}"]
    for p, d in people.items():
        out.append(f"0 {ids[p]} INDI")
        given, sur = esc(d.get("g", "")), esc(d.get("s", ""))
        out.append(f"1 NAME {given} /{sur}/".strip())
        if p:
            out.append(f"1 SEX {'M' if p.endswith('F') else 'F'}")
        b, de = year_of(d.get("y", ""), 0), year_of(d.get("y", ""), 1)
        if b:
            out += ["1 BIRT", f"2 DATE {b}"] + ([f"2 PLAC {esc(d['p'])}"] if d.get("p") else [])
        if de:
            out += ["1 DEAT", f"2 DATE {de}"]
        level = "по документу" if d.get("c") == "d" else "по семейным сведениям или гипотеза"
        out.append(f"1 NOTE Доказанность: {level}")
        for n in d.get("n", []):
            out.append(f"1 NOTE {esc(n)}")
        for f, cap in d.get("dc", []):
            out += ["1 OBJE", f"2 FILE {esc(f)}", f"2 TITL {esc(cap)}"]
        for fid in spouse_fams.get(p, []):
            out.append(f"1 FAMS {fid}")
        for fid, (_, _, child) in fams.items():
            if child == p:
                out.append(f"1 FAMC {fid}")
    for fid, (f, m, child) in fams.items():
        out.append(f"0 {fid} FAM")
        if f:
            out.append(f"1 HUSB {ids[f]}")
        if m:
            out.append(f"1 WIFE {ids[m]}")
        out.append(f"1 CHIL {ids[child]}")
    out.append("0 TRLR")
    open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"ok: {len(people)} people, {len(fams)} families -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
