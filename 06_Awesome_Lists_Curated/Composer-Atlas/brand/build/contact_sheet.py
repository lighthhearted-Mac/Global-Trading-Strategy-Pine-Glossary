# -*- coding: utf-8 -*-
"""Build a contact sheet for brand files and screenshot it in headless Edge.

  python brand/build/contact_sheet.py <sheet-name> <svg-or-png> [more files...]

The render check exists because an SVG that reads correctly as code can still
blur, fill in, or vanish once a rasteriser has had it at 16 pixels. Every logo
in this project is judged from the screenshot, never from the markup.

Each file is shown at three sizes on a light and a dark ground, in full colour
and in grayscale, because a mark that only works in colour will fail the day
somebody faxes, embroiders, or photocopies it.

Edge, never Chrome: a second Chrome launch would take over the owner's live
session. The flags below are not decoration. --user-data-dir gives the run a
throwaway profile, and without --disable-sync and --disable-component-update a
second launch against a fresh profile can hang with no output at all.
"""
import os
import subprocess
import sys

EDGE = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']
CHECKS = os.path.join('brand', 'checks')
DARK = '#16191f'
# SIZES may be overridden for a focused pass, e.g. SHEET_SIZES=16,32 to judge
# the small end near 1:1 instead of hunting for it inside a 9,000px sheet.
SIZES = tuple(int(n) for n in os.environ['SHEET_SIZES'].split(','))     if os.environ.get('SHEET_SIZES') else (16, 32, 512)


def edge():
    for p in EDGE + [os.environ.get('EDGE_PATH', '')]:
        if p and os.path.exists(p):
            return p
    raise SystemExit('Microsoft Edge not found; set EDGE_PATH')


def profile_dir():
    """A profile directory unique to this process.

    Edge refuses to share a --user-data-dir between live instances, and a
    headless run that has not fully exited still counts as live, so a shared
    throwaway profile makes the next launch hang with no output at all. Killing
    stray msedge processes is not an option: the owner's own browser runs under
    the same executable.
    """
    d = os.path.join(os.environ.get('TEMP', '.'),
                     'edge-brand-profile-%d' % os.getpid())
    os.makedirs(d, exist_ok=True)
    return d


def is_wide(path):
    """A lockup or a banner is judged on width; a symbol or icon on height."""
    if not path.endswith('.svg'):
        return False
    head = open(path, encoding='utf-8').read(400)
    if 'viewBox="0 0 ' not in head:
        return False
    nums = head.split('viewBox="0 0 ', 1)[1].split('"', 1)[0].split()
    try:
        return float(nums[0]) / float(nums[1]) > 1.25
    except (ValueError, IndexError, ZeroDivisionError):
        return False


def tile(rel, size, wide, grayscale):
    dim = ('width:%dpx' % min(size * 3, 1320)) if wide else ('width:%dpx;height:%dpx' % (size, size))
    gs = 'filter:grayscale(1);' if grayscale else ''
    return ('<figure><img src="%s" style="%s;%sobject-fit:contain">'
            '<figcaption>%dpx%s</figcaption></figure>'
            % (rel, dim, gs, size, ' gray' if grayscale else ''))


def build(name, files):
    os.makedirs(CHECKS, exist_ok=True)
    rows = []
    for path in files:
        wide = is_wide(path)
        rel = os.path.relpath(path, CHECKS).replace(os.sep, '/')
        # A "-dark" file is dark ink FOR a light ground, and vice versa. Pair
        # them so each ground is tested with the file that is meant for it.
        # The concepts are named <stem>-dark / <stem>-light; the shipped logo
        # system is named <stem>-color / <stem>-color-reversed. Both are the
        # same idea, an ink meant for a light ground and its reverse, and both
        # have to be paired or the dark panel quietly tests the wrong file,
        # which is how the dark-on-dark failure went unnoticed the first time.
        alt = None
        for a, b in (('-dark.', '-light.'), ('-color.', '-color-reversed.'),
                     ('-black.', '-white.')):
            if a in rel and os.path.exists(path.replace(a, b)):
                alt = rel.replace(a, b)
                break
        blocks = []
        for ground, label in ((('#ffffff', '#16191f'), 'light'),
                              ((DARK, '#e9edf2'), 'dark')):
            bg, fg = ground
            for g in (False, True):
                src = alt if (label == 'dark' and alt) else rel
                if wide and len(SIZES) > 2:
                    tiles = ('<div class="row">%s</div><div class="row">%s</div>'
                             % (''.join(tile(src, s, wide, g) for s in SIZES[:-1]),
                                tile(src, SIZES[-1], wide, g)))
                else:
                    tiles = '<div class="row">%s</div>' % ''.join(
                        tile(src, s, wide, g) for s in SIZES)
                blocks.append('<div class="ground" style="background:%s;color:%s">'
                              '<span class="lab">%s%s</span>%s</div>'
                              % (bg, fg, label, ' grayscale' if g else '', tiles))
        rows.append('<section><h2>%s</h2>%s</section>'
                    % (os.path.basename(path), ''.join(blocks)))

    html = (
        '<!doctype html><meta charset="utf-8"><title>%s</title><style>'
        'body{margin:0;background:#8a8f98;font:13px/1.4 system-ui,sans-serif}'
        'section{margin:0 0 2px}'
        'h2{margin:0;padding:8px 14px;background:#2c3038;color:#e9edf2;'
        'font:600 12px/1 ui-monospace,monospace;letter-spacing:.04em}'
        '.ground{padding:14px 18px;position:relative}'
        '.lab{position:absolute;top:6px;right:10px;font:10px/1 ui-monospace,monospace;opacity:.5}'
        '.row{display:flex;align-items:flex-end;gap:32px;flex-wrap:nowrap;margin-bottom:10px}'
        'figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}'
        'figcaption{font:10px/1 ui-monospace,monospace;opacity:.6}'
        '</style>%s' % (name, ''.join(rows)))

    page = os.path.join(CHECKS, name + '.html')
    with open(page, 'w', encoding='utf-8') as fh:
        fh.write(html)

    shot = os.path.abspath(os.path.join(CHECKS, name + '.png'))
    profile = profile_dir()
    subprocess.run([edge(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    '--user-data-dir=' + profile, '--disable-sync',
                    '--disable-component-update', '--no-first-run',
                    '--window-size=1500,%d' % (120 + (600 if max(SIZES) > 64 else 130) * 4 * len(files)),
                    '--screenshot=' + shot,
                    'file:///' + os.path.abspath(page).replace('\\', '/')],
                   check=True, capture_output=True, timeout=180)
    print('%s  (%d bytes)' % (shot, os.path.getsize(shot)))
    return shot


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    build(sys.argv[1], sys.argv[2:])
