# -*- coding: utf-8 -*-
"""Phase 4: build the full logo system into brand/logo/.

Run from the repository root:  python brand/build/build_logo.py

The direction chosen at the Phase 3 gate is **C and D as one system**, not as
two rivals. The render check settled it: C, the 3x3 index cell, is the strongest
mark and fills into a grey smudge at 16px; D, the same graticule reduced to 2x2
with a heavier stroke, is the only version that holds there. They share the same
vocabulary, so the switch between them is invisible to anyone who is not looking
for it. B, the Archivo wordmark with a green graticule tick for a word space,
locks up with either.

  primary   C, the 3x3 index cell. Used above 32px.
  compact   D, the 2x2 quadrant. Used at 32px and below, and for merchandise.

Rasterisation goes through headless Edge rather than a Python SVG library,
because Edge is the renderer the marks were judged in, and a second rasteriser
would mean the shipped PNGs were never the images anybody looked at.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_concepts import (ARCHIVO_SEMIBOLD, DARK, GREEN, HI, IN_, S, SPAN,
                            Face, lockup, svg, symbol_c, symbol_d, wordmark)
from contact_sheet import edge, profile_dir
from lib_type import f

import urllib.request

OUT = os.path.join('brand', 'logo')
LIGHT_INK = '#e9edf2'

# One graticule cell of the primary mark. Used as the clear-space unit, so the
# rule is stated in the mark's own vocabulary rather than in an arbitrary ratio.
CELL = SPAN / 3.0


# --------------------------------------------------------------- the variants

def variants(ink_dark=DARK, ink_light=LIGHT_INK):
    """(suffix, ink, accent) for every colour treatment the system ships.

    `color` keeps the green. `black` and `white` are single-colour: the accent
    collapses into the ink, which is what a fax, an embroidery head or a
    one-plate print will do to it anyway. The filled cell survives that collapse
    because it is a fill against open cells, not a hue against another hue.
    """
    return (
        ('color', ink_dark, GREEN),
        ('color-reversed', ink_light, GREEN),
        ('black', ink_dark, ink_dark),
        ('white', ink_light, ink_light),
    )


# Symbol width as a fraction of the wordmark's width. "COMPOSER ATLAS" is a
# fourteen-character string and will always be the wider element, so the symbol
# cannot be made to dominate by width; what it has to do is stop reading as an
# accessory. 0.46 left it looking like a hat on the wordmark. 0.62 makes it the
# thing the eye lands on first, which is the only reason to stack at all.
SYMBOL_SHARE = 0.62


def stacked(symbol_body, face, cap_px=20, gap=None, ink='currentColor',
            accent=GREEN):
    """Symbol above, wordmark below, both centred on one axis.

    The symbol is scaled up rather than used at its native 64 units. At native
    size it is a quarter of the wordmark's width and the stack reads as a
    wordmark wearing a small hat; the symbol has to be substantial enough to be
    the thing the eye lands on first, since that is the whole point of a stacked
    lockup over a horizontal one.
    """
    # The gap is set from cap height, not from the symbol, so it stays a
    # typographic interval rather than growing every time the symbol does.
    gap = 0.62 * cap_px if gap is None else gap
    wm, wm_w = wordmark(face, cap_px, ink=ink, accent=accent)
    sym_w = wm_w * SYMBOL_SHARE
    k = sym_w / S
    # Space from the INK, not from the canvas. The symbol carries a 9-unit
    # neatline inset on its 64-unit canvas, so measuring the gap from the canvas
    # edge silently adds 14% of the scaled symbol on top of it. At this scale
    # that was 22 units of accidental space against 12 of intended space, and it
    # read as the two halves of the lockup drifting apart.
    ink_h = SPAN * k
    width = max(sym_w, wm_w)
    body = ('<g transform="translate(%s %s) scale(%s)">%s</g>'
            '<g transform="translate(%s %s)">%s</g>'
            % (f((width - sym_w) / 2), f(-IN_ * k), f(k), symbol_body,
               f((width - wm_w) / 2), f(ink_h + gap), wm))
    return body, width, ink_h + gap + cap_px


# -------------------------------------------------------------- rasterisation

def rasterise(svg_path, png_path, size, background=None, pad=0.0):
    """Render one SVG to a square PNG at exactly `size` pixels, through Edge.

    background: None for transparency, or a hex string for an opaque plate.
    pad:        fraction of the canvas left empty around the mark. Maskable
                icons need the mark inside the central 80%, which is pad=0.1.
    """
    inner = size * (1 - 2 * pad)
    rel = os.path.relpath(svg_path, os.path.dirname(png_path)).replace(os.sep, '/')
    plate = background or 'transparent'
    html = (
        '<!doctype html><meta charset="utf-8"><style>'
        'html,body{margin:0;padding:0;width:%dpx;height:%dpx;overflow:hidden}'
        'body{background:%s;display:flex;align-items:center;'
        'justify-content:center}'
        'img{width:%spx;height:%spx;display:block}'
        '</style><img src="%s">'
        % (size, size, plate, f(inner), f(inner), rel))

    page = png_path + '.html'
    with open(page, 'w', encoding='utf-8') as fh:
        fh.write(html)

    cmd = [edge(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
           '--user-data-dir=' + profile_dir(),
           '--disable-sync', '--disable-component-update', '--no-first-run',
           '--force-device-scale-factor=1',
           '--window-size=%d,%d' % (size, size),
           '--screenshot=' + os.path.abspath(png_path),
           'file:///' + os.path.abspath(page).replace('\\', '/')]
    if background is None:
        # Without this the screenshot is composited onto opaque white and every
        # icon ships with a white box behind it.
        cmd.insert(-1, '--default-background-color=00000000')
    subprocess.run(cmd, check=True, capture_output=True, timeout=180)
    os.remove(page)
    return png_path


def build_ico(png_paths, ico_path):
    """Multi-resolution .ico from already-rendered PNGs.

    Pillow only. The sizes are baked from real renders rather than resampled
    from one large image, because 16px is where this mark is decided and a
    downsample of the 48 is not the same picture as a 16 drawn at 16.
    """
    from PIL import Image
    imgs = [Image.open(p).convert('RGBA') for p in png_paths]
    base = max(imgs, key=lambda im: im.size[0])
    base.save(ico_path, format='ICO',
              sizes=[im.size for im in imgs])
    return ico_path


# --------------------------------------------------------------------- favicon

def favicon_svg(path):
    """One file that answers both colour schemes.

    A favicon is the one asset that cannot ship as a light/dark pair, because
    the browser requests exactly one file and then draws it on a tab strip whose
    colour it never tells you. A media query inside the SVG is the only
    mechanism that works, and it works because here the SVG is a document in its
    own right rather than an <img> whose currentColor resolves against itself.
    """
    body = symbol_d(ink='var(--ink)', accent=GREEN)
    doc = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" '
           'width="%s" height="%s" role="img">'
           '<style>'
           ':root{--ink:%s}'
           '@media (prefers-color-scheme: dark){:root{--ink:%s}}'
           '</style>%s</svg>'
           % (f(S), f(S), f(S), f(S), DARK, LIGHT_INK, body))
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(doc)
    return path


# ------------------------------------------------------------------------ main

def main():
    # Overwritten in place rather than cleared first. OneDrive holds a handle on
    # a freshly created directory often enough that rmtree fails with WinError 5,
    # and a build script that deletes a tree is the wrong shape for this repo.
    os.makedirs(OUT, exist_ok=True)

    cache = os.path.join(os.environ.get('TEMP', '.'), 'Archivo-SemiBold.ttf')
    if not os.path.exists(cache):
        print('downloading Archivo SemiBold (SIL OFL 1.1)')
        urllib.request.urlretrieve(ARCHIVO_SEMIBOLD, cache)
    face = Face(cache)

    written = []

    def put(name, content):
        path = os.path.join(OUT, name)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        written.append(name)
        return path

    # ---- symbols -----------------------------------------------------------
    for suffix, ink, accent in variants():
        put('symbol-primary-%s.svg' % suffix,
            svg(S, S, symbol_c(ink=ink, accent=accent)))
        put('symbol-compact-%s.svg' % suffix,
            svg(S, S, symbol_d(ink=ink, accent=accent)))

    # ---- wordmark ----------------------------------------------------------
    for suffix, ink, accent in variants():
        wm, ww = wordmark(face, 40, ink=ink, accent=accent)
        put('wordmark-%s.svg' % suffix, svg(ww, 40, wm))

    # ---- lockups -----------------------------------------------------------
    for suffix, ink, accent in variants():
        body, lw = lockup(symbol_c(ink=ink, accent=accent), face, ink=ink)
        put('lockup-horizontal-%s.svg' % suffix, svg(lw, S, body))

        # The compact horizontal lockup is the system doing its job rather than
        # an extra file. The standard lockup puts C at the lockup's full height,
        # so C's 32px floor becomes a 288px floor for the whole lockup. Below
        # that the same lockup is set with D, which holds down to 16px, and a
        # reader who sees both never notices the substitution.
        body, lw_c = lockup(symbol_d(ink=ink, accent=accent), face, ink=ink)
        put('lockup-horizontal-compact-%s.svg' % suffix, svg(lw_c, S, body))

        body, sw_, sh_ = stacked(symbol_c(ink=ink, accent=accent), face,
                                 ink=ink, accent=accent)
        put('lockup-stacked-%s.svg' % suffix, svg(sw_, sh_, body))

    # ---- merchandise -------------------------------------------------------
    # D, single colour, at the weight that keeps every line and gap above 1mm
    # when the mark is reproduced 25mm wide. At 25mm one unit of the 46-unit
    # span is 0.543mm, so a 1mm minimum is 1.84 units. D's 3.6 stroke is 1.96mm
    # and its narrowest gap is 11.4mm, both clear. C is not used here: its 2.0
    # stroke is 1.09mm, which survives print and does not survive embroidery.
    put('merch-single-colour.svg', svg(S, S, symbol_d(ink='#000000',
                                                      accent='#000000')))
    # A white counterpart, because half of merchandise is a dark substrate and
    # a black-only file leaves that half with nothing to send to the supplier.
    put('merch-single-colour-white.svg', svg(S, S, symbol_d(ink='#ffffff',
                                                            accent='#ffffff')))

    # ---- favicon -----------------------------------------------------------
    fav = favicon_svg(os.path.join(OUT, 'favicon.svg'))
    written.append('favicon.svg')

    # ---- rasters -----------------------------------------------------------
    # Favicon PNGs come off the compact mark, which is the one that holds at 16.
    src_compact = os.path.join(OUT, 'symbol-compact-color.svg')
    src_compact_rev = os.path.join(OUT, 'symbol-compact-color-reversed.svg')
    src_primary_rev = os.path.join(OUT, 'symbol-primary-color-reversed.svg')

    # On an OPAQUE plate in the brand's dark base, with the reversed mark.
    #
    # The first build shipped these transparent, with the dark ink, and the
    # render check showed them on a dark tab strip as a lone green square: the
    # strokes were there and were the same colour as the ground. A transparent
    # PNG bakes exactly one ink and a browser never says which tab-strip colour
    # it is about to draw on, so transparency cannot answer both. favicon.svg
    # answers both with a media query; the PNG and ICO fallback answers both by
    # bringing its own ground.
    ico_parts = []
    for px in (16, 32, 48):
        p = rasterise(src_compact_rev, os.path.join(OUT, 'favicon-%d.png' % px),
                      px, background=DARK, pad=0.09)
        ico_parts.append(p)
        written.append(os.path.basename(p))

    build_ico(ico_parts, os.path.join(OUT, 'favicon.ico'))
    written.append('favicon.ico')

    # App icons sit on an opaque plate in the brand's own dark base, because a
    # transparent app icon is composited by the OS onto a surface nobody
    # controls, and the reversed mark on white is the one failure case.
    for px in (180, 192, 512, 1024):
        src = src_compact_rev if px <= 192 else src_primary_rev
        # pad 0 is not a missing margin. The mark carries a 9-unit inset on a
        # 64-unit canvas, so its ink already stops at 72% of the plate, which is
        # the proportion a platform icon wants. Adding a pad on top shrank it to
        # 53% and it read as a small logo lost on a big tile.
        p = rasterise(src, os.path.join(OUT, 'icon-%d.png' % px), px,
                      background=DARK, pad=0.0)
        written.append(os.path.basename(p))

    # Maskable icons: the platform may crop to a circle, so the mark has to sit
    # inside the central 80% and the plate has to fill the whole canvas.
    for px in (192, 512):
        src = src_compact_rev if px <= 192 else src_primary_rev
        # Ink lands at about 62% of the canvas: comfortably inside the 80%
        # safe zone a circular crop leaves, without the mark looking shrunken.
        p = rasterise(src, os.path.join(OUT, 'maskable-%d.png' % px), px,
                      background=DARK, pad=0.07)
        written.append(os.path.basename(p))

    for name in written:
        size = os.path.getsize(os.path.join(OUT, name))
        print('  %-34s %7d bytes' % (name, size))
    print('\n%d files in %s' % (len(written), OUT))


if __name__ == '__main__':
    main()
