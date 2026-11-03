# -*- coding: utf-8 -*-
"""Run a driver against overfit.html.

_edge.py is written for signal-miner.html: it splices a hook naming that page's
internals and rewrites that page's CPU throttle line. Neither exists here, so
this is a separate, much smaller launcher rather than a flag on that one.

The overfit page is also an IIFE (trap 1), so a driver that needs the page's own
functions gets them through a hook spliced before the closing `})();`. Trap 4
still applies: the DOM comes back as bytes and is decoded explicitly. Trap 13's
flags are passed for the same reason they are there.
"""
import io
import os
import re
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE)) if False else os.path.abspath(
    os.path.join(HERE, '..', '..'))
PAGE = os.path.join(REPO, 'overfit.html')
TAIL = "    })();\n  </script>"

# Only what a structural test needs. Bound through getters where the page
# reassigns, by value where it does not (trap 2).
HOOK = """      window.__of = {
        walkTree: walkTree, freeParams: freeParams, renderStructure: renderStructure,
        parseSymphony: parseSymphony, nearDuplicates: nearDuplicates,
        offConvention: offConvention, lookup: lookup, extractId: extractId
      };
"""


def edge_path():
    env = os.environ.get('EDGE_PATH')
    if env and os.path.exists(env):
        return env
    for c in (r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
              r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'):
        if os.path.exists(c):
            return c
    raise SystemExit('Edge not found; set EDGE_PATH')


def run(driver_js, timeout=600, config=None):
    src = io.open(PAGE, encoding='utf-8').read()
    if src.count(TAIL) != 1:
        raise SystemExit('IIFE tail not found or not unique in overfit.html')
    src = src.replace(TAIL, HOOK + TAIL)

    prefix = '_harness_of_' + os.path.splitext(os.path.basename(driver_js))[0]
    html_path = os.path.join(REPO, prefix + '.html')
    js_path = os.path.join(REPO, prefix + '_driver.js')
    src = src.replace('</body>', '<script src="%s"></script></body>'
                      % os.path.basename(js_path))
    io.open(html_path, 'w', encoding='utf-8', newline='').write(src)

    body = io.open(os.path.join(HERE, driver_js), encoding='utf-8').read()
    if config:
        import json
        body = 'window.__cfg = %s;\n' % json.dumps(config) + body
    io.open(js_path, 'w', encoding='utf-8', newline='').write(body)

    prof = tempfile.mkdtemp(prefix='composer-of-')
    url = 'file:///' + html_path.replace('\\', '/').replace(' ', '%20')
    argv = [edge_path(), '--headless=new', '--disable-gpu', '--no-sandbox',
            '--virtual-time-budget=120000', '--user-data-dir=' + prof,
            '--disable-sync', '--disable-component-update', '--dump-dom', url]
    try:
        dom = subprocess.run(argv, capture_output=True, timeout=timeout).stdout
    finally:
        for f in (html_path, js_path):
            try:
                os.remove(f)
            except OSError:
                pass
        import shutil
        shutil.rmtree(prof, ignore_errors=True)

    html = dom.decode('utf-8', 'replace')                        # trap 4
    m = re.search(r'<pre id="HARNESS">(.*?)</pre>', html, re.S)
    if not m:
        return 'NO HARNESS OUTPUT (the driver threw before it could report)'
    return (m.group(1).replace('&quot;', '"').replace('&gt;', '>')
            .replace('&lt;', '<').replace('&amp;', '&'))


if __name__ == '__main__':
    import sys
    print(run(sys.argv[1]))
