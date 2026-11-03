# -*- coding: utf-8 -*-
"""Phase 7: build brand/brand-design.html, the interactive Brand Design page.

Run from the repository root:  python brand/build/build_showcase.py

**Offline, not gated.** Composer Atlas is a public static site on Cloudflare
Pages with no accounts, no sessions and no server that could check one; the
project's own tenets rule out user accounts permanently. A "gated" page here
could only ever be an obscure URL, which is not a gate, it is a page you have
lost track of. So this is an offline page: it is written into the repository,
it is added to .gitignore, it is never linked from the site, and it is opened
from the file system.

It is not the same document as brand/presentation.html. The presentation argues
the case and prints to a PDF. This page is the thing you poke at: drag the size
slider until the primary mark breaks, flip the ground, copy a token.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact_sheet import edge, profile_dir  # noqa: E402

LOGO = os.path.join('brand', 'logo')
OUT = os.path.join('brand', 'brand-design.html')
GITIGNORE = '.gitignore'


def inline(name, cls='', style=''):
    svg = open(os.path.join(LOGO, name), encoding='utf-8').read()
    svg = re.sub(r'\swidth="[^"]*"', '', svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', '', svg, count=1)
    return svg.replace(
        '<svg ', '<svg class="%s" style="%s" ' % (cls, style), 1)


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#16191f;--surface:#2c3038;--raised:#373c46;--border:#4c515c;
  --border-hover:#616672;--ink:#e9edf2;--ink2:#d2d8df;--ink3:#b8bec6;
  --green:#00e676;--pink:#ff82ac;--blue:#68afff;--yellow:#f5c518;
  --purple:#b39dff;--r-sm:4px;--r-md:8px;--r-lg:12px;
}
body{background:var(--bg);color:var(--ink);line-height:1.6;
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased}
svg{display:block;height:auto}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}

header{border-bottom:1px solid var(--border);padding:64px 0 40px;
  margin-bottom:56px}
header .row{display:flex;align-items:center;gap:18px;margin-bottom:26px}
header .row svg{width:52px;flex:none}
h1{font-size:40px;font-weight:700;letter-spacing:-.025em;line-height:1.1}
.sub{color:var(--ink3);font-size:16px;max-width:64ch;margin-top:12px}
.flag{display:inline-flex;align-items:center;gap:9px;margin-top:22px;
  background:rgba(245,197,24,.12);border:1px solid rgba(245,197,24,.4);
  color:var(--yellow);border-radius:var(--r-md);padding:9px 14px;
  font-size:13.5px;font-weight:500}

section{margin-bottom:64px}
h2{font-size:24px;font-weight:600;letter-spacing:-.012em;margin-bottom:8px}
.hint{color:var(--ink3);font-size:15px;margin-bottom:22px;max-width:70ch}

.panel{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:26px}
.panel.light{background:#ffffff;border-color:#d8dde3}

.controls{display:flex;align-items:center;gap:18px;flex-wrap:wrap;
  margin-bottom:20px}
.seg{display:inline-flex;background:var(--bg);border:1px solid var(--border);
  border-radius:var(--r-md);overflow:hidden}
.seg button{background:none;border:0;color:var(--ink3);cursor:pointer;
  font:500 13px/1 inherit;padding:9px 15px}
.seg button[aria-pressed=true]{background:var(--raised);color:var(--ink)}
.seg button:hover{color:var(--ink)}
input[type=range]{width:260px;accent-color:var(--green)}
.val{font-family:ui-monospace,'JetBrains Mono',monospace;font-size:13px;
  color:var(--ink2);min-width:74px}

.stagebox{min-height:230px;display:flex;align-items:center;
  justify-content:center;border-radius:var(--r-md);padding:28px;
  background:var(--bg);transition:background .2s ease}
.stagebox.on-light{background:#ffffff}

.verdict{margin-top:16px;font-size:14px;display:flex;align-items:center;
  gap:9px}
.verdict .dot{width:9px;height:9px;border-radius:50%;flex:none}
.ok .dot{background:var(--green)} .ok{color:var(--green)}
.bad .dot{background:var(--pink)} .bad{color:var(--pink)}

.grid{display:grid;gap:16px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}

.tile{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-md);padding:20px;text-align:center}
.tile .box{height:104px;display:flex;align-items:center;
  justify-content:center;margin-bottom:14px;border-radius:var(--r-sm)}
.tile.rev .box{background:var(--bg)}
.tile.lit .box{background:#ffffff}
.tile b{font-size:13.5px;font-weight:600;display:block}
.tile span{font-size:12px;color:var(--ink3);
  font-family:ui-monospace,monospace}

.tok{display:flex;align-items:center;gap:13px;padding:11px 13px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-md);cursor:pointer;text-align:left;width:100%;
  font:inherit;color:inherit}
.tok:hover{border-color:var(--border-hover)}
.tok .chip{width:34px;height:34px;border-radius:var(--r-sm);flex:none;
  border:1px solid rgba(255,255,255,.14)}
.tok .nm{font-size:13.5px;font-weight:500}
.tok .hx{font-family:ui-monospace,monospace;font-size:12px;color:var(--ink3)}
.tok .cp{margin-left:auto;font-size:11px;color:var(--ink3)}

.ladder{display:flex;align-items:flex-end;gap:30px;flex-wrap:wrap;
  justify-content:center}
.rung{display:flex;flex-direction:column;align-items:center;gap:9px}
.rung .cap{font-family:ui-monospace,monospace;font-size:11px;
  color:var(--ink3)}

footer{border-top:1px solid var(--border);padding:38px 0 80px;
  color:var(--ink3);font-size:13.5px}
a{color:var(--blue)}
@media (max-width:760px){
  .g4,.g3{grid-template-columns:repeat(2,1fr)}
  .g2{grid-template-columns:1fr}
  input[type=range]{width:100%}
}
"""

JS = """
(function(){
  var sizeEl = document.getElementById('size');
  var out    = document.getElementById('sizeval');
  var stage  = document.getElementById('stage');
  var verd   = document.getElementById('verdict');

  // Both grounds carry BOTH marks. The first version sized only the dark pair,
  // so switching to the light ground left the slider doing nothing, which is
  // the one interaction this page exists for.
  function marks(role){
    return stage.querySelectorAll('[data-role="' + role + '"]');
  }

  // The switch point is not decoration. The primary mark's interior gaps merge
  // below 33px, so this page shows you the substitution actually happening
  // rather than describing it.
  var SWITCH = 33;

  function render(){
    var px = +sizeEl.value;
    out.textContent = px + 'px';
    var usePrimary = px >= SWITCH;
    ['primary', 'compact'].forEach(function(role){
      var show = (role === 'primary') === usePrimary;
      marks(role).forEach(function(el){
        el.style.display = show ? 'block' : 'none';
        var svg = el.querySelector('svg');
        if(svg) svg.style.width = px + 'px';
      });
    });
    verd.className = 'verdict ok';
    verd.innerHTML = '<span class="dot"></span>' + (usePrimary
      ? 'Primary mark. Above its 32px floor.'
      : 'Compact mark. The primary would fill in at this size.');
  }
  sizeEl.addEventListener('input', render);

  document.querySelectorAll('.seg').forEach(function(seg){
    seg.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return;
      seg.querySelectorAll('button').forEach(function(x){
        x.setAttribute('aria-pressed', String(x === b));
      });
      if(seg.dataset.target){
        var t = document.getElementById(seg.dataset.target);
        t.classList.toggle('on-light', b.dataset.v === 'light');
        t.querySelectorAll('[data-ink]').forEach(function(m){
          m.style.display = (m.dataset.ink === b.dataset.v) ? 'block' : 'none';
        });
        render();
      }
    });
  });

  document.querySelectorAll('.tok').forEach(function(btn){
    btn.addEventListener('click', function(){
      var v = btn.dataset.copy, lab = btn.querySelector('.cp');
      // Clipboard access can be refused, and a button that silently does
      // nothing is worse than one that says it could not.
      var done = function(ok){
        lab.textContent = ok ? 'copied' : 'press ctrl+c';
        setTimeout(function(){ lab.textContent = 'copy'; }, 1400);
      };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(v).then(function(){done(true);},
                                             function(){done(false);});
      } else { done(false); }
    });
  });

  render();
})();
"""


def build():
    def tile(name, cls, label, note):
        return ('<div class="tile %s"><div class="box">%s</div>'
                '<b>%s</b><span>%s</span></div>'
                % (cls, inline(name, style='width:74px'), label, note))

    tokens = [('Base', '--color-bg', '#16191f'),
              ('Surface', '--color-surface', '#2c3038'),
              ('Raised', '--color-surface-raised', '#373c46'),
              ('Border', '--color-border', '#4c515c'),
              ('Primary text', '--color-primary', '#e9edf2'),
              ('Secondary text', '--color-secondary', '#d2d8df'),
              ('Green', '--color-green', '#00e676'),
              ('Pink', '--color-pink', '#ff82ac'),
              ('Blue', '--color-blue', '#68afff'),
              ('Yellow', '--color-yellow', '#f5c518'),
              ('Purple', '--color-purple', '#b39dff')]
    tok_html = ''.join(
        '<button class="tok" data-copy="%s"><span class="chip" '
        'style="background:%s"></span><span><span class="nm">%s</span><br>'
        '<span class="hx">%s</span></span><span class="cp">copy</span></button>'
        % (hexv, hexv, nm, var) for nm, var, hexv in tokens)

    ladder = ''.join(
        '<div class="rung">%s<span class="cap">%dpx</span></div>'
        % (inline('symbol-compact-color-reversed.svg',
                  style='width:%dpx' % px), px) for px in (16, 24, 32))
    ladder += ''.join(
        '<div class="rung">%s<span class="cap">%dpx</span></div>'
        % (inline('symbol-primary-color-reversed.svg',
                  style='width:%dpx' % px), px) for px in (48, 96, 160))

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Brand Design &middot; Composer Atlas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>%(css)s</style>
</head>
<body>

<header><div class="wrap">
  <div class="row">%(mark)s<div>
    <h1>Brand Design</h1>
    <p class="sub">The Composer Atlas identity, as something you can poke at
    rather than read about. Drag the slider until the primary mark gives out.</p>
  </div></div>
  <div class="flag">&#9888; Not published. This page is in <code>.gitignore</code>,
  is not linked from the site, and is opened from the file system.</div>
</div></header>

<div class="wrap">

<section>
  <h2>The responsive mark</h2>
  <p class="hint">Two marks, one idea. The primary carries the full graticule;
  below 33px its interior gaps merge, so the compact mark takes over. The switch
  is the system working, not a compromise.</p>
  <div class="panel">
    <div class="controls">
      <div class="seg" data-target="stage">
        <button data-v="dark" aria-pressed="true">Dark ground</button>
        <button data-v="light" aria-pressed="false">Light ground</button>
      </div>
      <input id="size" type="range" min="12" max="220" value="160"
             aria-label="Mark size in pixels">
      <span class="val" id="sizeval">160px</span>
    </div>
    <div class="stagebox" id="stage">
      <div data-ink="dark" style="display:block">
        <div data-role="primary">%(p_rev)s</div>
        <div data-role="compact" style="display:none">%(c_rev)s</div>
      </div>
      <div data-ink="light" style="display:none">
        <div data-role="primary">%(p_dark)s</div>
        <div data-role="compact" style="display:none">%(c_dark)s</div>
      </div>
    </div>
    <div class="verdict ok" id="verdict"><span class="dot"></span></div>
  </div>
</section>

<section>
  <h2>The size ladder</h2>
  <p class="hint">Rendered at true size. The first three are the compact mark,
  the last three the primary.</p>
  <div class="panel"><div class="ladder">%(ladder)s</div></div>
</section>

<section>
  <h2>Treatments</h2>
  <p class="hint">Four per asset. The single-colour versions pull the filled
  cell back off the strokes, because with one colour there is no hue left to
  separate them.</p>
  <div class="grid g4">
    %(treat)s
  </div>
</section>

<section>
  <h2>Lockups</h2>
  <div class="grid g2">
    <div class="panel"><div style="padding:10px 0">%(lock_h)s</div>
      <p class="hint" style="margin:14px 0 0">Horizontal. Minimum 288px wide,
      set by the symbol rather than the type.</p></div>
    <div class="panel"><div style="padding:10px 0;max-width:186px;margin:0 auto">
      %(lock_s)s</div>
      <p class="hint" style="margin:14px 0 0">Stacked. Minimum 120px wide.</p></div>
  </div>
</section>

<section>
  <h2>Tokens</h2>
  <p class="hint">Click to copy. These are the live values from
  <code>css/main.css</code>; the portable copies are in
  <code>brand/kit/tokens.css</code> and <code>tokens.json</code>.</p>
  <div class="grid g3">%(tokens)s</div>
</section>

<section>
  <h2>The rules that are easy to break</h2>
  <div class="grid g2">
    <div class="panel"><h2 style="font-size:16px;color:var(--green)">Do</h2>
      <p class="hint" style="margin:10px 0 0">Use the compact mark at 32px and
      below and for anything stitched. Leave one graticule cell of clear space.
      Use the supplied single-colour files rather than recolouring the full
      colour one.</p></div>
    <div class="panel"><h2 style="font-size:16px;color:var(--pink)">Do not</h2>
      <p class="hint" style="margin:10px 0 0">Do not straighten the meridians:
      without the bow it is a table. Do not set the primary mark below 32px. Do
      not add a gradient, glow or shadow. Do not put the mark beside an arrow or
      a rising line.</p></div>
  </div>
</section>

</div>

<footer><div class="wrap">
  Composer Atlas brand design &middot; concept work, not adopted. The live site
  still ships the emoji.<br>
  Full reasoning in <code>docs/DESIGN.md</code> Section 11 and
  <code>brand/presentation.html</code>.
</div></footer>

<script>%(js)s</script>
</body>
</html>
""" % {
        'css': CSS, 'js': JS,
        'mark': inline('symbol-primary-color-reversed.svg'),
        'p_rev': inline('symbol-primary-color-reversed.svg',
                        style='width:160px'),
        'c_rev': inline('symbol-compact-color-reversed.svg',
                        style='width:160px'),
        'p_dark': inline('symbol-primary-color.svg', style='width:160px'),
        'c_dark': inline('symbol-compact-color.svg', style='width:160px'),
        'ladder': ladder,
        'treat': (tile('symbol-primary-color.svg', 'lit', 'Colour', '#16191f ink')
                  + tile('symbol-primary-color-reversed.svg', 'rev',
                         'Colour reversed', '#e9edf2 ink')
                  + tile('symbol-primary-black.svg', 'lit', 'Mono black',
                         'one plate')
                  + tile('symbol-primary-white.svg', 'rev', 'Mono white',
                         'one plate')),
        'lock_h': inline('lockup-horizontal-color-reversed.svg',
                         style='width:100%'),
        'lock_s': inline('lockup-stacked-color-reversed.svg',
                         style='width:100%'),
        'tokens': tok_html,
    }


def ensure_ignored():
    """Add the page to .gitignore if it is not already covered."""
    line = 'brand/brand-design.html'
    text = open(GITIGNORE, encoding='utf-8').read() if os.path.exists(GITIGNORE) else ''
    if line in text:
        return False
    block = ('\n# Phase 7 brand showcase. Built by brand/build/build_showcase.py,\n'
             '# opened from the file system, deliberately never published.\n'
             '%s\n' % line)
    with open(GITIGNORE, 'a', encoding='utf-8') as fh:
        fh.write(block)
    return True


def main():
    html = build()
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('%s  (%d bytes)' % (OUT, os.path.getsize(OUT)))

    added = ensure_ignored()
    print('.gitignore: %s' % ('entry added' if added else 'already covered'))

    shot = os.path.abspath(os.path.join('brand', 'checks', 'brand-design.png'))
    subprocess.run(
        [edge(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
         '--user-data-dir=' + profile_dir(), '--disable-sync',
         '--disable-component-update', '--no-first-run',
         '--window-size=1200,4200', '--screenshot=' + shot,
         'file:///' + os.path.abspath(OUT).replace('\\', '/')],
        check=True, capture_output=True, timeout=300)
    print('%s  (%d bytes)' % (shot, os.path.getsize(shot)))


if __name__ == '__main__':
    main()
