#!/usr/bin/env python3
"""Shared layout / collision checker for the manuscript figures.

Purpose: replace eyeballing with a measurement. After a figure is drawn, this
walks the artist tree, takes the *rendered* bounding box of every visible text
(annotations, tick labels, axis labels, titles, legend entries, panel letters)
and reports

  (1) text-text pairs that overlap or sit closer than a stated minimum gap,
  (2) text that overlaps a supplied data artist (markers, whiskers, bars),
  (3) text that leaves its axes, or leaves the figure canvas,
  (4) any text rendered below the stated minimum font size.

Gaps are reported in typographic points at the figure's own scale, so the
numbers mean the same thing as the "min 8 pt" requirement.

Tick labels of the *same* axis are exempt from the pair check only when they do
not actually overlap - matplotlib already spaces them, and flagging every
neighbouring tick pair would bury the real collisions.
"""
from __future__ import annotations

import matplotlib
from matplotlib.text import Text, Annotation


def relative_luminance(rgb):
    """WCAG 2.x relative luminance of an (r, g, b) triple in 0..1."""
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(float(c)) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb_a, rgb_b):
    """WCAG contrast ratio between two colours (1.0 = identical, 21.0 = max)."""
    la, lb = relative_luminance(rgb_a), relative_luminance(rgb_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def best_text_colour(bg_rgb):
    """Pick black or white against `bg_rgb`, whichever has more contrast.

    Returns (colour, ratio). Because the ratio depends only on relative
    luminance, and a luminance-based greyscale conversion preserves luminance,
    a colour that passes here passes identically in greyscale print.
    """
    black, white = (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
    rb, rw = contrast_ratio(bg_rgb, black), contrast_ratio(bg_rgb, white)
    return ("black", rb) if rb >= rw else ("white", rw)


def _walk_texts(artist, out, seen):
    """Collect every visible, non-empty Text in the artist tree."""
    try:
        children = artist.get_children()
    except Exception:
        return
    for ch in children:
        if id(ch) in seen:
            continue
        seen.add(id(ch))
        if isinstance(ch, Text):
            try:
                if ch.get_visible() and ch.get_text().strip():
                    out.append(ch)
            except Exception:
                pass
        _walk_texts(ch, out, seen)


def _owner_axes(fig, text):
    """Which axes does this text belong to (None for figure-level text)?"""
    for ax in fig.axes:
        node, guard = text, 0
        while node is not None and guard < 40:
            if node is ax:
                return ax
            node = getattr(node, "axes", None) or getattr(node, "figure", None)
            if node is fig:
                return None
            guard += 1
    return getattr(text, "axes", None)


def _gap_pt(a, b, dpi):
    """Signed gap between two bboxes in points. Negative == overlap depth."""
    dx = max(a.x0 - b.x1, b.x0 - a.x1)
    dy = max(a.y0 - b.y1, b.y0 - a.y1)
    if dx >= 0 or dy >= 0:          # separated on at least one axis
        gap_px = max(dx, dy)
    else:                            # overlapping in both -> penetration depth
        gap_px = max(dx, dy)         # both negative; max == shallowest overlap
    return gap_px * 72.0 / dpi


def _cartopy_gridline_texts(fig, out, seen):
    """Cartopy graticule labels are generated during draw and are not reachable
    from the normal artist tree, so collect them from each Gridliner."""
    for ax in fig.axes:
        for art in list(getattr(ax, "artists", [])) + list(
                getattr(ax, "_children", [])):
            labels = getattr(art, "label_artists", None)
            if labels is None:
                continue
            for t in labels:
                if id(t) in seen or not isinstance(t, Text):
                    continue
                seen.add(id(t))
                try:
                    if t.get_visible() and t.get_text().strip():
                        out.append(t)
                except Exception:
                    pass


def check(fig, name, min_gap_pt=1.5, min_font_pt=8.0, data_artists=(),
          ignore_pairs=(), contained=(), verbose=True):
    """Draw `fig` and report layout problems. Returns a list of problem strings."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    dpi = fig.dpi

    texts = []
    seen = set()
    _walk_texts(fig, texts, seen)
    _cartopy_gridline_texts(fig, texts, seen)

    entries = []
    for t in texts:
        try:
            bb = t.get_window_extent(renderer)
        except Exception:
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        entries.append({
            "artist": t,
            "text": t.get_text(),
            "bbox": bb,
            "axes": _owner_axes(fig, t),
            "size": t.get_fontsize(),
            "is_tick": _is_tick_label(t),
        })

    problems = []

    # ---- (4) font sizes -------------------------------------------------
    for e in entries:
        if e["size"] < min_font_pt - 1e-6:
            problems.append(
                f"FONT   {e['size']:.2f} pt < {min_font_pt} pt : {e['text']!r}")

    # ---- (1) text vs text ----------------------------------------------
    ignore = {frozenset(p) for p in ignore_pairs}
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a, b = entries[i], entries[j]
            if frozenset((a["text"], b["text"])) in ignore:
                continue
            gap = _gap_pt(a["bbox"], b["bbox"], dpi)
            same_axis_ticks = (a["is_tick"] and b["is_tick"]
                               and a["axes"] is b["axes"])
            limit = 0.0 if same_axis_ticks else min_gap_pt
            if gap < limit:
                kind = "OVERLAP" if gap < 0 else "TIGHT  "
                problems.append(
                    f"{kind} {gap:+.2f} pt : {a['text']!r} <-> {b['text']!r}")

    # ---- (2) text vs data artists ---------------------------------------
    for art, label in data_artists:
        try:
            bb = art.get_window_extent(renderer)
        except Exception:
            continue
        # A perfectly horizontal or vertical artist (a dumbbell, a whisker, a
        # reference line) has a bbox of zero height or zero width. Requiring
        # BOTH to be positive silently skipped exactly the artists most likely
        # to sit under a label, so only a fully empty artist is skipped here.
        if bb.width <= 0 and bb.height <= 0:
            continue
        for e in entries:
            if e["is_tick"]:
                continue
            gap = _gap_pt(e["bbox"], bb, dpi)
            if gap < min_gap_pt:
                kind = "OVERLAP" if gap < 0 else "TIGHT  "
                problems.append(
                    f"{kind} {gap:+.2f} pt : {e['text']!r} <-> data[{label}]")

    # ---- (3) containment -------------------------------------------------
    figbb = fig.bbox
    for e in entries:
        bb = e["bbox"]
        if (bb.x0 < figbb.x0 - 0.5 or bb.x1 > figbb.x1 + 0.5
                or bb.y0 < figbb.y0 - 0.5 or bb.y1 > figbb.y1 + 0.5):
            problems.append(f"CLIPPED off canvas : {e['text']!r}")

    # Text drawn *inside* an axes must also keep clear of that axes' frame,
    # which the canvas check above cannot see.
    for e in entries:
        ax, bb = e["axes"], e["bbox"]
        if ax is None or e["is_tick"]:
            continue
        ab = ax.bbox
        inside = (bb.x0 >= ab.x0 - 1 and bb.x1 <= ab.x1 + 1
                  and bb.y0 >= ab.y0 - 1 and bb.y1 <= ab.y1 + 1)
        if not inside:
            continue  # deliberately outside (axis labels, panel letters)
        margin = min(bb.x0 - ab.x0, ab.x1 - bb.x1,
                     bb.y0 - ab.y0, ab.y1 - bb.y1) * 72.0 / dpi
        if margin < min_gap_pt:
            problems.append(
                f"TIGHT   {margin:+.2f} pt to axes frame : {e['text']!r}")

    # ---- (3b) legends must stay inside their own axes --------------------
    # A legend placed with loc=/bbox_to_anchor can extend past the axes it
    # belongs to and sit over a neighbouring panel. Its texts are "outside the
    # axes", which the containment test above deliberately tolerates (axis
    # labels live there), so legend overflow needs its own check.
    for ax in fig.axes:
        leg = ax.get_legend()
        if leg is None or not leg.get_visible():
            continue
        try:
            lb = leg.get_window_extent(renderer)
        except Exception:
            continue
        ab = ax.bbox
        over = max(ab.x0 - lb.x0, lb.x1 - ab.x1) * 72.0 / dpi
        if over > 0.5:
            problems.append(
                f"OVERFLOW legend leaves its axes by {over:+.2f} pt "
                f"(entries: {[t.get_text() for t in leg.get_texts()][:3]})")

    # ---- (5) text that must stay inside its own container ----------------
    # A schematic has no numbers to assert, but it can still fail silently by
    # letting a label spill out of the box it names. This catches that.
    for text_artist, patch_artist, label in contained:
        try:
            tb = text_artist.get_window_extent(renderer)
            pb = patch_artist.get_window_extent(renderer)
        except Exception:
            continue
        over_x = max(pb.x0 - tb.x0, tb.x1 - pb.x1) * 72.0 / dpi
        over_y = max(pb.y0 - tb.y0, tb.y1 - pb.y1) * 72.0 / dpi
        if over_x > -min_gap_pt or over_y > -min_gap_pt:
            problems.append(
                f"OVERFLOW box {label!r}: text exceeds/─crowds container by "
                f"{max(over_x, over_y):+.2f} pt")

    if verbose:
        print(f"\n[layout check] {name}")
        print(f"  texts checked      : {len(entries)}")
        print(f"  min font size      : "
              f"{min(e['size'] for e in entries):.2f} pt "
              f"(required >= {min_font_pt})")
        print(f"  min text-text gap  : {_min_gap(entries, dpi):.2f} pt "
              f"(required >= {min_gap_pt})")
        if problems:
            print(f"  PROBLEMS ({len(problems)}):")
            for p in problems:
                print("    " + p)
        else:
            print("  PROBLEMS: none - no overlaps, no clipping, "
                  "all text at or above minimum size")
    return problems


def _is_tick_label(t):
    ax = getattr(t, "axes", None)
    if ax is None:
        return False
    try:
        return t in list(ax.get_xticklabels()) + list(ax.get_yticklabels())
    except Exception:
        return False


def _min_gap(entries, dpi):
    best = float("inf")
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a, b = entries[i], entries[j]
            if a["is_tick"] and b["is_tick"] and a["axes"] is b["axes"]:
                continue
            best = min(best, _gap_pt(a["bbox"], b["bbox"], dpi))
    return best if best != float("inf") else 0.0


def assert_inside(ax, name, xs=(), ys=()):
    """Every data value (point or CI bound) must lie strictly inside the axis view.

    Added 2026-09-23 after Fig. 8 clipped a CI at the x limit on the corrected label:
    the text collision checker cannot see a data line that runs off the axes.
    """
    x0, x1 = sorted(ax.get_xlim())
    y0, y1 = sorted(ax.get_ylim())
    bad = [("x", v) for v in xs if not (x0 < v < x1)] + [("y", v) for v in ys if not (y0 < v < y1)]
    assert not bad, f"{name}: data outside axis view {bad[:5]} (x {x0:.3f}-{x1:.3f}, y {y0:.3f}-{y1:.3f})"
    return True
