# -*- coding: utf-8 -*-
"""Phase 3: emit the four concept directions to brand/concepts/.

Run from the repository root:  python brand/build/build_concepts.py

Design vocabulary, so the numbers below are readable rather than magic.

  neatline   The border that frames a map plate. Every real map has one; almost
             no logo does. Here it is a true square, because a map's frame stays
             rectangular however the projection inside it curves.
  parallel   A line of latitude. Straight, horizontal.
  meridian   A line of longitude. In any pseudocylindrical projection these bow
             away from the central meridian, which is the single detail that
             makes a grid read as a MAP rather than as a spreadsheet.
  index cell One cell of the graticule, filled. An atlas index finds a place by
             its cell reference; the product's whole job is to put a reader in
             the right cell and explain the ground under it.

Colour: --color-green #00e676 and --color-bg #16191f, both fixed by owner ruling.
See docs/PRD.md, Brand Identity, Brand Brief.
"""
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_type import Face, typeset, quad_at, quad_split, f  # noqa: E402

GREEN = '#00e676'
DARK = '#16191f'
OUT = os.path.join('brand', 'concepts')

ARCHIVO_SEMIBOLD = ('https://fonts.gstatic.com/s/archivo/v25/'
                    'k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTT6jRp8A.ttf')

# ---------------------------------------------------------------- the graticule

S = 64.0          # symbol viewBox is S x S
IN_ = 9.0         # neatline inset: the mark never touches its own edge
HI = S - IN_      # 55
SPAN = HI - IN_   # 46
BOW = 4.8         # how far a meridian departs from vertical at mid-height


def meridian(nominal_x, mirrored=False, bow=None):
    """Control points for one bowed meridian, top to bottom.

    The bow goes AWAY from the centre of the plate, which is what a projection
    does. `nominal_x` is where the meridian meets the top and bottom neatline.
    """
    b = BOW if bow is None else bow
    cx = nominal_x - b if not mirrored else nominal_x + b
    return (nominal_x, IN_), (cx, S / 2), (nominal_x, HI)


def t_at_y(y):
    """Parameter t on a meridian at height y.

    The meridians are quadratics whose y component is exactly linear, because
    the control point sits at mid-height: IN_ + HI - 2*(S/2) == 0 while IN_ and
    HI are symmetric about S/2. Worth stating, because it is the reason a cell
    boundary can be solved in closed form instead of sampled.
    """
    return (y - IN_) / SPAN


def cell_path(x_left, x_right, y_top, y_bot):
    """One graticule cell, with its two curved sides taken from the meridians."""
    lp = meridian(x_left)
    rp = meridian(x_right, mirrored=True)
    t1, t2 = t_at_y(y_top), t_at_y(y_bot)
    la, lb, lc = quad_split(*lp, t1=t1, t2=t2)
    ra, rb, rc = quad_split(*rp, t1=t1, t2=t2)
    return ('M%s %sL%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ' % (
        f(la[0]), f(la[1]),
        f(ra[0]), f(ra[1]),
        f(rb[0]), f(rb[1]), f(rc[0]), f(rc[1]),
        f(lc[0]), f(lc[1]),
        f(lb[0]), f(lb[1]), f(la[0]), f(la[1])))


def meridian_d(nominal_x, mirrored=False, bow=None):
    p0, p1, p2 = meridian(nominal_x, mirrored, bow)
    return 'M%s %sQ%s %s %s %s' % (f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]),
                                   f(p2[0]), f(p2[1]))


def inset(path_d, cx, cy, k=0.72):
    """Shrink a filled cell about its own centre.

    Only used when ink and accent are the SAME colour. In full colour the
    located cell reads because it is green against an open cell; in single
    colour it has nothing to contrast with except the strokes it touches, so
    the fill and the graticule merge into one blob and the idea of one cell
    being located disappears. Pulling the fill back off the strokes restores a
    hairline of ground around it, which is what carries the meaning once the
    hue is gone. Found on a render of the embroidered patch, not in the code.
    """
    return ('<g transform="translate(%s %s) scale(%s) translate(%s %s)">'
            '<path d="%s"/></g>'
            % (f(cx), f(cy), f(k), f(-cx), f(-cy), path_d))


# ------------------------------------------------------------------- the marks

def symbol_a(ink='currentColor', accent=GREEN, sw=2.6):
    """A: Neatline. A frame and one parallel: the minimum viable map.

    One focal point, the green parallel. Nothing else in the mark.
    """
    y = IN_ + SPAN * 0.63          # below centre, so the mark is not static
    return (
        '<g fill="none" stroke="%s" stroke-width="%s" stroke-linecap="butt">'
        '<rect x="%s" y="%s" width="%s" height="%s"/></g>'
        '<path d="M%s %sH%s" stroke="%s" stroke-width="%s" stroke-linecap="butt"/>'
    ) % (ink, f(sw), f(IN_), f(IN_), f(SPAN), f(SPAN),
         f(IN_), f(y), f(HI), accent, f(sw))


def symbol_c(ink='currentColor', accent=GREEN, sw=2.0):
    """C: Index Cell. The full graticule, one cell located.

    Three columns by three rows. The interior meridians bow; the parallels do
    not. The centre cell is filled, and it is filled with the curve-exact
    sub-paths of the meridians rather than an eyeballed shape, so no seam shows
    where the stroke crosses the fill.
    """
    c1, c2 = IN_ + SPAN / 3.0, IN_ + SPAN * 2.0 / 3.0
    r1, r2 = IN_ + SPAN / 3.0, IN_ + SPAN * 2.0 / 3.0
    cell = cell_path(c1, c2, r1, r2)
    if accent == ink:
        cell_g = '<g fill="%s">%s</g>' % (accent, inset(cell, S / 2, S / 2))
    else:
        cell_g = '<path d="%s" fill="%s"/>' % (cell, accent)
    return (
        '%s'
        '<g fill="none" stroke="%s" stroke-width="%s">'
        '<rect x="%s" y="%s" width="%s" height="%s"/>'
        '<path d="M%s %sH%s"/><path d="M%s %sH%s"/>'
        '<path d="%s"/><path d="%s"/>'
        '</g>'
    ) % (cell_g,
         ink, f(sw),
         f(IN_), f(IN_), f(SPAN), f(SPAN),
         f(IN_), f(r1), f(HI), f(IN_), f(r2), f(HI),
         meridian_d(c1), meridian_d(c2, mirrored=True))


def symbol_d(ink='currentColor', accent=GREEN, sw=3.6):
    """D: Evolved. The graticule reduced to what survives at nav size.

    Two by two rather than three by three, and a heavier stroke, because the
    existing mark is set at 1.25rem in the nav and that is the size this has to
    win at. Same vocabulary as C, fewer statements.
    """
    mid = S / 2
    D_BOW = 7.4
    p0, p1, p2 = meridian(mid, bow=D_BOW)
    t1, t2 = t_at_y(IN_), t_at_y(mid)
    qa, qb, qc = quad_split(p0, p1, p2, t1, t2)
    cell = ('M%s %sL%s %sL%s %sL%s %sQ%s %s %s %sZ' % (
        f(qa[0]), f(qa[1]), f(HI), f(IN_), f(HI), f(mid), f(qc[0]), f(qc[1]),
        f(qb[0]), f(qb[1]), f(qa[0]), f(qa[1])))
    if accent == ink:
        cell_g = '<g fill="%s">%s</g>' % (
            accent, inset(cell, (mid + HI) / 2, (IN_ + mid) / 2))
    else:
        cell_g = '<path d="%s" fill="%s"/>' % (cell, accent)
    return (
        '%s'
        '<g fill="none" stroke="%s" stroke-width="%s">'
        '<rect x="%s" y="%s" width="%s" height="%s"/>'
        '<path d="M%s %sH%s"/><path d="%s"/>'
        '</g>'
    ) % (cell_g, ink, f(sw),
         f(IN_), f(IN_), f(SPAN), f(SPAN),
         f(IN_), f(mid), f(HI), meridian_d(mid, bow=D_BOW))


# ---------------------------------------------------------------- the wordmark

TRACK = 26          # all-caps wants positive tracking; a reference brand wants calm
KERNS = {'LA': -28, 'AT': -18, 'TL': -22, 'SE': -6, 'ER': -6, 'OM': -8}


def wordmark(face, cap_px, ink='currentColor', accent=GREEN,
             parallel=False, tick=True, word_gap=300):
    """COMPOSER ATLAS, with the two custom details.

    `tick`, the one surviving custom detail: the word space is a graticule
    tick. It does the job a space does and carries the brand's measuring device
    while doing it, at exactly cap height and at the symbol's own stroke module,
    so the wordmark and the mark are built from one measurement rather than
    merely placed beside each other.

    `parallel` is OFF and defaults off. It drew a rule through every O's counter,
    which was meant to read as a projected field and read instead as a slashed
    Scandinavian O: the render check showed "CØMPØSER". A detail that changes
    which letters a reader sees is not a detail, and it was removed rather than
    softened, because a thinner rule fails the same way more quietly.

    All caps, deliberately. Mixed case brings a descender on the p and puts the
    t and l above cap height, and neither earns its irregularity here; caps read
    as institutional, which is the position Phase 2 argues for.
    """
    k = cap_px / face.cap
    text = 'COMPOSER' + ' ' + 'ATLAS'
    places, width = typeset(face, text, TRACK, KERNS)
    # widen the word space by word_gap font units, applied to everything after it
    split_at = len('COMPOSER')
    shifted = []
    for i, (ch, x, d) in enumerate(places):
        shifted.append((ch, x + (word_gap if i >= split_at else 0), d))
    width += word_gap

    glyphs = ''.join('<path transform="translate(%s 0)" d="%s"/>' % (f(x), d)
                     for _, x, d in shifted)
    body = '<g fill="%s">%s</g>' % (ink, glyphs)

    extras = ''
    if parallel:
        # The rule spans the O's counter. Taken from the glyph's own bounds
        # rather than typed in, so it stays correct if the weight changes.
        ox0, oy0, ox1, oy1 = face.bounds('O')
        side = 92          # stem thickness of the O at this weight, measured
        y0 = (oy0 + oy1) / 2 - 42
        for ch, x, _ in shifted:
            if ch != 'O':
                continue
            extras += ('<rect x="%s" y="%s" width="%s" height="84" fill="%s"/>'
                       % (f(x + ox0 + side * 0.72),
                          f(y0),
                          f((ox1 - ox0) - side * 1.44), ink))
    if tick:
        # Centred on the ink, not on the advance widths. R ends on a diagonal
        # leg and A opens on one, so the optical gap and the metric gap are not
        # the same interval, and a tick placed by advance sits against the A.
        TICK_W = 70
        prev_ch, prev_x, _ = shifted[split_at - 1]
        next_ch, next_x, _ = shifted[split_at]
        gap0 = prev_x + face.bounds(prev_ch)[2]
        gap1 = next_x + face.bounds(next_ch)[0]
        tx = (gap0 + gap1) / 2 - TICK_W / 2
        extras += ('<rect x="%s" y="0" width="%d" height="%s" fill="%s"/>'
                   % (f(tx), TICK_W, f(face.cap), accent))

    inner = body + ('<g fill="%s">%s</g>' % (ink, '') if False else extras)
    return ('<g transform="translate(0 %s) scale(%s -%s)">%s</g>'
            % (f(cap_px), f(k), f(k), inner)), width * k


# ------------------------------------------------------------------ assembling

def svg(w, h, body, ink=None):
    style = ' color="%s"' % ink if ink else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" '
            'width="%s" height="%s" role="img"%s>%s</svg>'
            % (f(w), f(h), f(w), f(h), style, body))


def lockup(symbol_body, face, cap_px=34, gap=22, ink='currentColor'):
    wm, wm_w = wordmark(face, cap_px, ink=ink)
    # Optical centring: caps have no descender, so centring on cap height alone
    # sits the word visibly high against a full-height square. Nudge down.
    y = (S - cap_px) / 2 + 1.5
    body = (symbol_body
            + '<g transform="translate(%s %s)">%s</g>' % (f(S + gap), f(y), wm))
    return body, S + gap + wm_w


def main():
    os.makedirs(OUT, exist_ok=True)
    cache = os.path.join(os.environ.get('TEMP', '.'), 'Archivo-SemiBold.ttf')
    if not os.path.exists(cache):
        print('downloading Archivo SemiBold (SIL OFL 1.1)')
        urllib.request.urlretrieve(ARCHIVO_SEMIBOLD, cache)
    face = Face(cache)

    written = []

    INKS = (('dark', '#16191f'), ('light', '#e9edf2'))

    def write(stem, w, h, make_body):
        """Write one mark twice, once per ink.

        Two files rather than one with currentColor: an SVG referenced by an
        <img> resolves currentColor against its own root element, never against
        the page around it, so a single file cannot be proved on both grounds.
        The pair is a deliverable in its own right (Phase 4 wants monochrome
        black and reversed white), so nothing is duplicated that was not needed.
        """
        for suffix, ink in INKS:
            name = '%s-%s.svg' % (stem, suffix)
            path = os.path.join(OUT, name)
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(svg(w, h, make_body(ink), None))
            written.append((name, os.path.getsize(path)))

    for key, fn in (('a-neatline', symbol_a),
                    ('c-index-cell', symbol_c),
                    ('d-evolved', symbol_d)):
        _, lw = lockup(fn('#000'), face)
        write('concept-%s' % key, lw, S,
              lambda ink, fn=fn: lockup(fn(ink), face, ink=ink)[0])
        write('concept-%s-symbol' % key, S, S, lambda ink, fn=fn: fn(ink))

    _, ww = wordmark(face, 40)
    write('concept-b-wordmark', ww, 40,
          lambda ink: wordmark(face, 40, ink=ink)[0])

    for name, size in written:
        print('  %-34s %5d bytes' % (name, size))


if __name__ == '__main__':
    main()
