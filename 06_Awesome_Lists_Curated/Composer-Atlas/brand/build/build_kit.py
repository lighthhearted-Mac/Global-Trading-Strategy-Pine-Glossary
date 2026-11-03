# -*- coding: utf-8 -*-
"""Phase 5: build the brand kit into brand/kit/.

Run from the repository root:  python brand/build/build_kit.py

Social images, design tokens in two formats, an email signature and a web
manifest. Nothing here is linked from the site: `site.webmanifest` is written so
that adopting it later is a one-line change, not so that it ships today.

The copy on the social images is the site's own. "Judge a Composer strategy
before you run it" is the existing og:title in index.html, and the supporting
line is the existing meta description, trimmed. A brand kit is not the place to
invent a tagline the product has never used.

Layout rule shared by every image here: the composition is a graticule. The
lockup sits on a cell boundary rather than on a guessed margin, which is the
same device the mark is built from and is the reason the images look like they
belong to it rather than merely carrying it.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_concepts import DARK, GREEN  # noqa: E402
from contact_sheet import edge, profile_dir  # noqa: E402

OUT = os.path.join('brand', 'kit')
LOGO = os.path.join('brand', 'logo')

TITLE = 'Judge a Composer strategy before you run it'
SUPPORT = ('Free breakdowns of hand-picked symphonies, a searchable database, '
           'daily signals and testing tools.')
DOMAIN = 'composeratlas.com'

# Straight from the :root block of css/main.css. Not retyped from memory: the
# palette was rebuilt at v1.82.0 with every step solved for a measured contrast
# ratio, and a brand kit that ships a remembered palette is how the two copies
# drift apart again.
TOKENS = {
    'color': {
        'bg':             ('#16191f', 'Page base'),
        'surface':        ('#2c3038', 'Cards and panels'),
        'surface-raised': ('#373c46', 'The brightest surface, and the hardest '
                                      'ground for text'),
        'border':         ('#4c515c', 'Default border'),
        'border-hover':   ('#616672', 'Border on hover'),
        'primary':        ('#e9edf2', 'Primary text'),
        'secondary':      ('#d2d8df', 'Secondary text'),
        'disabled':       ('#b8bec6', 'Disabled text. The name is a misnomer '
                                      'kept knowingly; see DESIGN.md Section 2'),
        'green':          ('#00e676', 'Positive values, primary actions, and '
                                      'the brand accent'),
        'pink':           ('#ff82ac', 'Negative values'),
        'blue':           ('#68afff', 'Interactive'),
        'yellow':         ('#f5c518', 'Caution'),
        'purple':         ('#b39dff', 'Momentum'),
        # An ALIAS in the CSS (var(--color-green)), flattened to its literal
        # value here on purpose: this file is consumed by decks and prototypes
        # that will not have --color-green defined. The distinction it carries
        # is meaning, not hue. --color-positive says a number went up;
        # --color-brand says this is us.
        'brand':          ('#00e676', 'Identity, not a value. The mark only, '
                                      'and never paired with an arrow or a '
                                      'rising line; see DESIGN.md Section 11'),
    },
    'radius': {'sm': ('4px', ''), 'md': ('8px', ''), 'lg': ('12px', '')},
    'font': {
        'sans': ("'Inter', system-ui, -apple-system, sans-serif", 'UI and prose'),
        'mono': ("'JetBrains Mono', 'Fira Code', monospace", 'Every number on '
                 'the site'),
        'brand': ("'Archivo', 'Inter', sans-serif", 'The wordmark only. Not '
                  'loaded by the site'),
    },
}


# ------------------------------------------------------------------- contrast

def luminance(hex_colour):
    """WCAG relative luminance. sRGB is not linear, so the channels are
    linearised before weighting; averaging the raw bytes gives a number that
    looks plausible and is wrong."""
    c = hex_colour.lstrip('#')
    out = []
    for i in (0, 2, 4):
        v = int(c[i:i + 2], 16) / 255.0
        out.append(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# -------------------------------------------------------------- rasterisation

def shoot(html, path, w, h):
    """Render an HTML string to a PNG of exactly w x h."""
    page = path + '.html'
    with open(page, 'w', encoding='utf-8') as fh:
        fh.write(html)
    subprocess.run(
        [edge(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
         '--user-data-dir=' + profile_dir(), '--disable-sync',
         '--disable-component-update', '--no-first-run',
         '--force-device-scale-factor=1',
         '--window-size=%d,%d' % (w, h),
         '--screenshot=' + os.path.abspath(path),
         'file:///' + os.path.abspath(page).replace('\\', '/')],
        check=True, capture_output=True, timeout=180)
    os.remove(page)
    return path


def frame(w, h, body, extra_css=''):
    """Shared page chrome: exact pixel box, brand base, no scrollbars.

    Inter is pulled from Google Fonts because it is the face the site actually
    runs. If the network is unavailable the fallback stack is system-ui, which
    changes the metrics, so these images are rebuilt rather than trusted when
    the build has been offline.
    """
    return (
        '<!doctype html><meta charset="utf-8">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Inter:wght@400;500;600;700&display=swap">'
        '<style>'
        '*{margin:0;padding:0;box-sizing:border-box}'
        'html,body{width:%dpx;height:%dpx;overflow:hidden}'
        'body{background:%s;color:#e9edf2;'
        "font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased}"
        '%s</style>%s' % (w, h, DARK, extra_css, body))


def rel(name):
    """Path to a logo file, relative to brand/kit/."""
    return os.path.relpath(os.path.join(LOGO, name), OUT).replace(os.sep, '/')


# ---------------------------------------------------------------- the images

def og_image(path):
    """1200x630. The card Slack, iMessage, Discord and every preview will show.

    The green rule is the graticule's parallel, not a decorative underline: it
    sits at the same 63% of the composition that the parallel sits at in the
    mark, so the card is laid out by the same instrument it advertises.
    """
    css = (
        '.wrap{padding:72px 80px;height:100%%;display:flex;flex-direction:column;'
        'justify-content:center;gap:0}'
        '.top{display:flex;align-items:center;gap:22px;margin-bottom:46px}'
        '.top img{width:88px;height:88px;display:block}'
        '.name{font:600 27px/1 Inter,sans-serif;letter-spacing:.14em;'
        'text-transform:uppercase}'
        'h1{font:700 62px/1.1 Inter,sans-serif;letter-spacing:-.022em;'
        'max-width:21ch}'
        '.rule{width:104px;height:7px;background:%s;margin:36px 0 26px}'
        'p{font:400 25px/1.45 Inter,sans-serif;color:#b8bec6;max-width:44ch}'
        '.dom{position:absolute;right:80px;bottom:64px;'
        "font:500 21px/1 'JetBrains Mono',ui-monospace,monospace;color:#8b93a0;"
        'letter-spacing:.02em}' % GREEN)
    body = ('<div class="wrap">'
            '<div class="top"><img src="%s"><span class="name">Composer Atlas</span></div>'
            '<h1>%s</h1><div class="rule"></div><p>%s</p></div>'
            '<div class="dom">%s</div>'
            % (rel('symbol-primary-color-reversed.svg'), TITLE, SUPPORT, DOMAIN))
    return shoot(frame(1200, 630, body, css), path, 1200, 630)


def profile(path):
    """400x400, and every platform will crop it to a circle.

    So the mark sits inside the inscribed circle with room to spare, and there
    is nothing in the corners to lose. The compact mark is used rather than the
    primary one because a profile image is rendered at 32px in a comment thread
    far more often than it is rendered at 400.
    """
    css = ('body{display:flex;align-items:center;justify-content:center}'
           'img{width:236px;height:236px;display:block}')
    body = '<img src="%s">' % rel('symbol-compact-color-reversed.svg')
    return shoot(frame(400, 400, body, css), path, 400, 400)


def x_header(path):
    """1500x500. The avatar overlaps the lower left, and the visible band
    narrows a great deal on a phone, so everything that must survive is held in
    the middle third and nothing sits in the bottom left at all."""
    css = ('body{display:flex;align-items:center;justify-content:center}'
           '.mid{display:flex;flex-direction:column;align-items:center;gap:26px;'
           'margin-bottom:28px}'
           '.mid img{width:560px;display:block}'
           'p{font:400 22px/1 Inter,sans-serif;color:#b8bec6;'
           'letter-spacing:.01em}')
    body = ('<div class="mid"><img src="%s"><p>%s</p></div>'
            % (rel('lockup-horizontal-color-reversed.svg'), TITLE))
    return shoot(frame(1500, 500, body, css), path, 1500, 500)


def linkedin(path):
    """1584x396. Left aligned: LinkedIn puts the company logo over the lower
    left of the banner on desktop but not on mobile, so the lockup is held
    clear of that corner while still reading as left-anchored."""
    css = ('body{display:flex;align-items:center}'
           '.wrap{padding-left:96px;display:flex;flex-direction:column;gap:22px}'
           '.wrap img{width:640px;display:block}'
           'p{font:400 23px/1 Inter,sans-serif;color:#b8bec6}'
           '.bar{position:absolute;left:0;top:0;bottom:0;width:10px;'
           'background:%s}' % GREEN)
    body = ('<div class="bar"></div><div class="wrap"><img src="%s"><p>%s</p></div>'
            % (rel('lockup-horizontal-color-reversed.svg'), TITLE))
    return shoot(frame(1584, 396, body, css), path, 1584, 396)


def signature(path):
    """720x180, which is 360x90 at 2x for a retina mail client.

    On WHITE, unlike everything else in the kit: an email signature is composited
    into a reply chain whose background is whatever the recipient's client uses,
    and light is the safe assumption. This is the one asset in the kit that uses
    the dark-ink treatment.
    """
    css = ('body{background:#ffffff;color:#16191f;display:flex;'
           'align-items:center;padding:0 24px}'
           '.row{display:flex;align-items:center;gap:26px}'
           '.row img{width:120px;height:120px;display:block}'
           '.rule{width:3px;height:96px;background:#00e676}'
           '.name{font:700 34px/1.2 Inter,sans-serif;letter-spacing:-.01em}'
           '.dom{font:500 24px/1.4 "JetBrains Mono",ui-monospace,monospace;'
           'color:#5b626d;margin-top:8px}')
    body = ('<div class="row"><img src="%s"><div class="rule"></div>'
            '<div><div class="name">Composer Atlas</div>'
            '<div class="dom">%s</div></div></div>'
            % (rel('symbol-primary-color.svg'), DOMAIN))
    return shoot(frame(720, 180, body, css), path, 720, 180)


# ----------------------------------------------------------------- the tokens

def write_tokens(css_path, json_path):
    lines = ['/* Composer Atlas design tokens.',
             ' *',
             ' * Generated from the :root block of css/main.css by',
             ' * brand/build/build_kit.py. This file is a PORTABLE COPY for use',
             ' * outside the site, in a deck, a prototype or a partner document.',
             ' * css/main.css remains the source of truth, and if the two ever',
             ' * disagree the CSS wins. Regenerate rather than hand-edit.',
             ' */',
             ':root {']
    data = {}
    for group, items in TOKENS.items():
        lines.append('  /* %s */' % group)
        data[group] = {}
        for key, (value, note) in items.items():
            name = '--%s-%s' % (group, key) if group != 'color' else '--color-%s' % key
            comment = ('  /* %s */' % note) if note else ''
            lines.append('  %s: %s;%s' % (name, value, comment))
            data[group][key] = {'value': value, 'note': note} if note else {'value': value}
        lines.append('')
    lines.append('}')
    with open(css_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')

    payload = {
        'name': 'Composer Atlas',
        'generated': '2026-09-28',
        'source': 'css/main.css',
        'note': ('Portable copy for use outside the site. css/main.css is the '
                 'source of truth; regenerate with brand/build/build_kit.py '
                 'rather than editing this file.'),
        'tokens': data,
    }
    with open(json_path, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2)
        fh.write('\n')


def write_manifest(path):
    """Written, NOT linked. Adopting it is a one-line change in each page head,
    and that change is a site change, which this commission does not make."""
    manifest = {
        'name': 'Composer Atlas',
        'short_name': 'Atlas',
        'description': SUPPORT,
        'start_url': '/',
        'display': 'standalone',
        'background_color': DARK,
        'theme_color': DARK,
        'icons': [
            {'src': '/brand/logo/icon-192.png', 'sizes': '192x192',
             'type': 'image/png', 'purpose': 'any'},
            {'src': '/brand/logo/icon-512.png', 'sizes': '512x512',
             'type': 'image/png', 'purpose': 'any'},
            {'src': '/brand/logo/maskable-192.png', 'sizes': '192x192',
             'type': 'image/png', 'purpose': 'maskable'},
            {'src': '/brand/logo/maskable-512.png', 'sizes': '512x512',
             'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, indent=2)
        fh.write('\n')


def contrast_report():
    """Every text colour against every ground it can legally sit on."""
    grounds = [('bg', '#16191f'), ('surface', '#2c3038'),
               ('surface-raised', '#373c46')]
    inks = ['primary', 'secondary', 'disabled', 'green', 'pink', 'blue',
            'yellow', 'purple']
    rows = []
    for ink in inks:
        hexv = TOKENS['color'][ink][0]
        for gname, ghex in grounds:
            r = ratio(hexv, ghex)
            rows.append((ink, hexv, gname, r,
                         'AAA' if r >= 7 else 'AA' if r >= 4.5
                         else 'AA large' if r >= 3 else 'FAIL'))
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    built = []

    for name, fn, dims in (
            ('og-image.png', og_image, (1200, 630)),
            ('profile-400.png', profile, (400, 400)),
            ('x-header-1500x500.png', x_header, (1500, 500)),
            ('linkedin-banner-1584x396.png', linkedin, (1584, 396)),
            ('email-signature@2x.png', signature, (720, 180))):
        fn(os.path.join(OUT, name))
        built.append((name, dims))

    write_tokens(os.path.join(OUT, 'tokens.css'),
                 os.path.join(OUT, 'tokens.json'))
    write_manifest(os.path.join(OUT, 'site.webmanifest'))
    built += [('tokens.css', None), ('tokens.json', None),
              ('site.webmanifest', None)]

    for name, dims in built:
        p = os.path.join(OUT, name)
        extra = ''
        if dims:
            from PIL import Image
            got = Image.open(p).size
            extra = '  %dx%d %s' % (got[0], got[1],
                                    'OK' if got == dims else 'SIZE MISMATCH')
        print('  %-30s %8d bytes%s' % (name, os.path.getsize(p), extra))

    print('\nContrast, computed not assumed:')
    worst = None
    for ink, hexv, ground, r, grade in contrast_report():
        if grade == 'FAIL' or (ink in ('primary', 'secondary') and r < 4.5):
            print('  !! %-10s %s on %-14s %5.2f:1  %s'
                  % (ink, hexv, ground, r, grade))
        if worst is None or r < worst[3]:
            worst = (ink, hexv, ground, r, grade)
    print('  lowest ratio in the palette: %s on %s = %.2f:1 (%s)'
          % (worst[0], worst[2], worst[3], worst[4]))


if __name__ == '__main__':
    main()
