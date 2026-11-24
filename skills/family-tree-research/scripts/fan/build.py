#!/usr/bin/env python3
"""Build a self-contained interactive fan chart (one HTML file) from a JSON tree.

Usage: python3 build.py tree.json out.html [--img DIR]

tree.json:
  config  – title, subtitle, eyebrow, footer, rootLabel, lines
  people  – {path: person}; path "" is the person in the centre, then F/M per
            generation ("F" father, "FM" father's mother, ...)
  events  – chronicle entries
Images (photos and document scans) are embedded as base64, so the HTML works offline.
"""
import base64, json, mimetypes, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    src, out = args[0], args[1]
    img_dir = args[args.index("--img") + 1] if "--img" in args else os.path.join(os.path.dirname(os.path.abspath(src)), "img")
    tree = json.load(open(src, encoding="utf-8"))
    people, cfg, events = tree["people"], tree["config"], tree.get("events", [])

    if "" not in people:
        sys.exit('people must contain "" – the person in the centre')
    for p in people:
        if p and (set(p) - {"F", "M"} or p[:-1] not in people):
            sys.exit(f"bad path {p!r}: use only F/M, and the child {p[:-1]!r} must exist")

    imgs = {}
    for v in people.values():
        v.setdefault("s", ""); v.setdefault("y", ""); v.setdefault("p", ""); v.setdefault("c", "f"); v.setdefault("n", [])
        for k in ("ph", "dc"):
            v[k] = [list(x) for x in v.get(k, [])]
            for f, _ in v[k]:
                if f not in imgs:
                    path = os.path.join(img_dir, f)
                    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
                    with open(path, "rb") as fh:
                        imgs[f] = f"data:{mime};base64," + base64.b64encode(fh.read()).decode()

    ev = []
    for e in events:
        w = e.get("who")
        if w is not None and w not in people:
            sys.exit(f"event refers to unknown path {w!r}: {e}")
        ev.append(dict(y=e["year"], d=e.get("date", ""), t=e.get("type", "record"), w=w,
                       l=e.get("lane"), x=e["text"], a=1 if e.get("approx") else 0))
    ev.sort(key=lambda e: e["y"])

    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    page = (tpl.replace("/*DATA*/null", json.dumps(people, ensure_ascii=False))
               .replace("/*IMGS*/null", json.dumps(imgs))
               .replace("/*EV*/null", json.dumps(ev, ensure_ascii=False))
               .replace("/*CFG*/null", json.dumps(cfg, ensure_ascii=False)))
    open(out, "w", encoding="utf-8").write(page)
    print(f"ok: {len(people)} people, {len(imgs)} images, {len(ev)} events, {len(page)/1e6:.2f} MB -> {out}")


if __name__ == "__main__":
    main()
