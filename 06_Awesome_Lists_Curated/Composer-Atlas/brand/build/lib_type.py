# -*- coding: utf-8 -*-
"""Typesetting and curve helpers for the Composer Atlas brand build.

NOT part of the site. See docs/PRD.md, Brand Identity, for why these scripts sit
in brand/build/ rather than scripts/, and why they may use Pillow and fontTools
where the rest of the project is standard library only. Nothing here runs in CI,
in deploy.yml, or at serve time.

Typeface: Archivo, by Omnibus-Type. SIL Open Font License 1.1.
The TTF is not committed. build_concepts.py downloads it to a scratch directory
and bakes the outlines into the SVGs as paths, so no build output depends on the
font being present afterwards.
"""
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


class Face:
    """One weight of one typeface, with glyph outlines addressable by character."""

    def __init__(self, path):
        self.font = TTFont(path)
        self.upem = self.font['head'].unitsPerEm
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font['hmtx']
        os2 = self.font['OS/2']
        self.cap = getattr(os2, 'sCapHeight', None) or int(self.upem * 0.7)

    def name(self, ch):
        gn = self.cmap.get(ord(ch))
        if gn is None:
            raise KeyError('no glyph for %r' % ch)
        return gn

    def advance(self, ch):
        return self.hmtx[self.name(ch)][0]

    def bounds(self, ch):
        bp = BoundsPen(self.glyphs)
        self.glyphs[self.name(ch)].draw(bp)
        return bp.bounds

    def path(self, ch):
        pen = SVGPathPen(self.glyphs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
        self.glyphs[self.name(ch)].draw(pen)
        return pen.getCommands()


def typeset(face, text, tracking=0, kerns=None):
    """Lay out `text` in font units, left to right.

    tracking: uniform letter spacing in font units, added after every glyph.
    kerns:    {'AB': delta} pair adjustments, applied before the second glyph.
              Hand-kerned rather than read from GPOS: a wordmark is kerned by
              eye, and the pairs that matter in a 13-character string are few.

    Returns (placements, width) where each placement is (char, x, path_d).
    """
    kerns = kerns or {}
    out, x = [], 0
    for i, ch in enumerate(text):
        if i:
            x += kerns.get(text[i - 1] + ch, 0)
        if ch != ' ':
            out.append((ch, x, face.path(ch)))
        x += face.advance(ch) + tracking
    return out, x - tracking


def quad_at(p0, p1, p2, t):
    """Point on a quadratic Bezier at parameter t."""
    u = 1 - t
    return (u * u * p0[0] + 2 * t * u * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * t * u * p1[1] + t * t * p2[1])


def quad_split(p0, p1, p2, t1, t2):
    """The sub-curve of a quadratic Bezier over [t1, t2], as (q0, q1, q2).

    Used to fill one cell of the graticule: the cell's curved sides are pieces of
    the full meridian, and drawing them as fresh curves guessed by eye would
    leave a visible seam against the meridian stroke drawn over it.
    """
    def lerp(a, b, t):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    q0 = quad_at(p0, p1, p2, t1)
    q2 = quad_at(p0, p1, p2, t2)
    q1 = lerp(lerp(p0, p1, t1), lerp(p1, p2, t1), t2)
    return q0, q1, q2


def f(v):
    """Format a coordinate: trim trailing zeros so the SVG stays readable."""
    s = '%.2f' % v
    return s.rstrip('0').rstrip('.') if '.' in s else s
