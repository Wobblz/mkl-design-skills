#!/usr/bin/env python3
"""What a font file really ships, before you write CSS that asks for it.

    pip install fonttools brotli
    python3 font-check.py path/or/url/to/font.woff2 [more fonts…]

Check the file the browser actually gets: the next/font output in
.next/static/media, the Fontsource file, or a fonts.gstatic.com URL. Google
Fonts and Fontsource strip stylistic sets, small caps, old-style figures and
more, so the specimen page tells you nothing about the served file.
"""
import io
import sys
import urllib.request

from fontTools.ttLib import TTFont

# Features worth knowing about, and what asking for them without the font does.
FEATURES = {
    "tnum": "tabular-nums",
    "pnum": "proportional-nums",
    "lnum": "lining-nums",
    "onum": "oldstyle-nums (no-op without it)",
    "smcp": "small-caps (faked without it)",
    "c2sc": "all-small-caps (faked without it)",
    "frac": "diagonal-fractions",
    "zero": "slashed-zero",
    "case": "case-sensitive punctuation",
    "sups": "font-variant-position: super (faked without it)",
    "ordn": "ordinal",
    "dlig": "discretionary-ligatures",
    "locl": "localised forms (needs lang)",
}

# Characters the skill reaches for. A missing one falls back to another font.
CHARS = {
    0x2007: "figure space (pads numbers)",
    0x2009: "thin space",
    0x202F: "narrow no-break space",
    0x2011: "no-break hyphen",
    0x2212: "minus",
    0x00D7: "multiplication",
    0x2026: "ellipsis",
    0x201E: "„ low-9 quote (Bulgarian)",
    0x201C: "“ quote",
    0x2013: "en dash",
    0x2014: "em dash",
    0x0434: "д (Cyrillic)",
}


def load(src):
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        return TTFont(io.BytesIO(urllib.request.urlopen(req).read()))
    return TTFont(src)


def features(font):
    """Feature tags, plus which script/language pairs carry locl."""
    tags, locl = set(), set()
    for table in ("GSUB", "GPOS"):
        if table not in font or not font[table].table.FeatureList:
            continue
        t = font[table].table
        records = t.FeatureList.FeatureRecord
        tags.update(r.FeatureTag for r in records)
        if table != "GSUB" or not t.ScriptList:
            continue
        for s in t.ScriptList.ScriptRecord:
            for l in s.Script.LangSysRecord:
                idx = l.LangSys.FeatureIndex
                if any(records[i].FeatureTag == "locl" for i in idx):
                    locl.add(f"{s.ScriptTag.strip()}/{l.LangSysTag.strip()}")
    return tags, locl


def digit_widths(font):
    """Width of "0" (what `ch` measures) against the tabular digit width."""
    cmap, hmtx = font.getBestCmap(), font["hmtx"]
    zero = cmap.get(0x30)
    if not zero:
        return None
    w0 = hmtx[zero][0]
    tab = None
    gsub = font["GSUB"].table if "GSUB" in font else None
    if gsub and gsub.FeatureList:
        for rec in gsub.FeatureList.FeatureRecord:
            if rec.FeatureTag != "tnum":
                continue
            for li in rec.Feature.LookupListIndex:
                for st in gsub.LookupList.Lookup[li].SubTable:
                    st = getattr(st, "ExtSubTable", st)
                    mapping = getattr(st, "mapping", None)
                    if mapping and zero in mapping:
                        tab = hmtx[mapping[zero]][0]
    return w0, tab


def report(src):
    font = load(src)
    name = font["name"].getDebugName(4) or src
    tags, locl = features(font)
    cmap = font.getBestCmap()
    print(f"\n{name}  ({src})")
    if "fvar" in font:
        axes = ", ".join(f"{a.axisTag} {a.minValue:g}–{a.maxValue:g}" for a in font["fvar"].axes)
        print(f"  axes: {axes}")
    print("  features:")
    for tag, what in FEATURES.items():
        print(f"    {'✓' if tag in tags else '✗'} {tag:5} {what}")
    sets = sorted(t for t in tags if t[:2] in ("ss", "cv"))
    print(f"    stylistic sets / variants: {', '.join(sets) or 'none (stripped, or never there)'}")
    bg = any(x.endswith("/BGR") for x in locl)
    print(f"  locl for: {', '.join(sorted(locl)) or 'none'}")
    if 0x0434 in cmap:
        print(f"  Bulgarian forms via lang=bg: {'yes' if bg else 'NO, Bulgarian renders in Russian forms'}")
    missing = [f"U+{c:04X} {w}" for c, w in CHARS.items() if c not in cmap]
    print(f"  missing characters: {'; '.join(missing) or 'none'}")
    widths = digit_widths(font)
    if widths:
        w0, tab = widths
        if tab is None:
            print(f"  digits: default '0' is {w0} units; no tnum mapping for '0' (digits may already be tabular)")
        elif tab != w0:
            print(f"  digits: '0' is {w0} units but tabular '0' is {tab}: 1ch ≠ one tabular digit, size with a measured span")
        else:
            print(f"  digits: 1ch equals one tabular digit ({w0} units)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        report(arg)
