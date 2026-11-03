# -*- coding: utf-8 -*-
"""Phase 6: build brand/presentation.html and print it to a PDF.

Run from the repository root:  python brand/build/build_presentation.py

One file. Every logo is **inlined** rather than linked, which is why the page
has no <img> tags at all: the brief allows photographs from brand/mockups/ as
the only images, that directory is empty because this brand has never been
photographed, so every mockup here is drawn in CSS and SVG. Inlining also makes
the file genuinely single, which a folder of linked SVGs would not be.

The only external request the page makes is Archivo from Google Fonts, which is
the brand typeface. The wordmark itself does not depend on it: those outlines
are baked into the SVG as paths, so the page is correct even offline.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact_sheet import edge, profile_dir  # noqa: E402

LOGO = os.path.join('brand', 'logo')
OUT_HTML = os.path.join('brand', 'presentation.html')
OUT_PDF = os.path.join('brand', 'brand-guidelines.pdf')

GREEN = '#00e676'
DARK = '#16191f'


def inline(name, width=None, cls=''):
    """Read a logo SVG and return it ready to drop into the page.

    The width/height attributes are stripped so CSS controls the size; the
    viewBox is what makes it scale, and leaving the attributes in means every
    mark on the page is locked to 64px no matter what the stylesheet says.
    """
    svg = open(os.path.join(LOGO, name), encoding='utf-8').read()
    svg = re.sub(r'\swidth="[^"]*"', '', svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', '', svg, count=1)
    style = (' style="width:%s"' % width) if width else ''
    svg = svg.replace('<svg ', '<svg class="mark %s"%s ' % (cls, style), 1)
    return svg


# --------------------------------------------------------------------- styles

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#16191f; --surface:#2c3038; --raised:#373c46;
  --border:#4c515c; --ink:#e9edf2; --ink2:#d2d8df; --ink3:#b8bec6;
  --green:#00e676; --pink:#ff82ac; --blue:#68afff;
  --yellow:#f5c518; --purple:#b39dff;
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);
  font-family:'Archivo',system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased;line-height:1.55}
.mark{display:block;height:auto}

section{max-width:1080px;margin:0 auto;padding:110px 56px;
  border-bottom:1px solid rgba(255,255,255,.07)}
section:last-child{border-bottom:0}

.eyebrow{font-size:12px;font-weight:600;letter-spacing:.2em;
  text-transform:uppercase;color:var(--green);margin-bottom:20px}
h1{font-size:clamp(40px,7vw,86px);font-weight:700;letter-spacing:-.028em;
  line-height:1.03}
h2{font-size:clamp(28px,4vw,44px);font-weight:700;letter-spacing:-.02em;
  line-height:1.12;margin-bottom:22px}
h3{font-size:19px;font-weight:600;letter-spacing:-.005em;margin-bottom:10px}
p{color:var(--ink2);font-size:17px;max-width:68ch;margin-bottom:16px}
p.lead{font-size:21px;color:var(--ink);max-width:60ch}
strong{color:var(--ink);font-weight:600}
em{color:var(--ink);font-style:normal;
  border-bottom:2px solid var(--green);padding-bottom:1px}
code{font-family:ui-monospace,'JetBrains Mono',monospace;font-size:.88em;
  background:var(--surface);padding:2px 6px;border-radius:4px;color:var(--ink)}

.grid{display:grid;gap:22px;margin-top:34px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}

.card{background:var(--surface);border:1px solid var(--border);
  border-radius:12px;padding:26px}
.card p{font-size:15px;margin-bottom:0;color:var(--ink3)}
.card .mark{margin-bottom:18px}

table{width:100%;border-collapse:collapse;margin-top:26px;font-size:15px}
th,td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--border);
  vertical-align:top}
th{font-size:12px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink3);font-weight:600}
td{color:var(--ink2)}

.swatches{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;
  margin-top:30px}
.sw{border-radius:10px;overflow:hidden;border:1px solid var(--border)}
.sw .chip{height:86px}
.sw .meta{padding:11px 13px;background:var(--surface);font-size:12px}
.sw .meta b{display:block;color:var(--ink);font-weight:600;margin-bottom:3px}
.sw .meta span{font-family:ui-monospace,monospace;color:var(--ink3)}

/* ---- the size ladder ------------------------------------------------- */
.ladder{display:flex;align-items:flex-end;gap:38px;margin-top:34px;
  flex-wrap:wrap}
.rung{display:flex;flex-direction:column;align-items:center;gap:10px}
.rung .cap{font-family:ui-monospace,monospace;font-size:11px;color:var(--ink3)}

/* ---- clear space diagram --------------------------------------------- */
.clear{position:relative;display:inline-block;margin-top:30px;
  padding:48px;background:
    repeating-linear-gradient(45deg,rgba(0,230,118,.10) 0 8px,
      transparent 8px 16px);
  border:1px dashed rgba(0,230,118,.5);border-radius:6px}
.clear .inner{background:var(--bg);padding:0}

/* ---- mockups: no photographs exist, so these are built -------------- */
.stage{background:
    radial-gradient(120% 90% at 50% 0%,#232833 0%,#14171d 70%);
  border:1px solid var(--border);border-radius:16px;
  padding:60px 40px;display:flex;align-items:center;justify-content:center;
  gap:56px;flex-wrap:wrap;perspective:1400px}

/* A phone home screen. Drawn, not photographed. */
.phone{width:206px;border-radius:30px;padding:13px;
  background:linear-gradient(150deg,#3b414d,#1b1e25);
  box-shadow:
    0 1px 0 rgba(255,255,255,.14) inset,
    0 26px 44px -18px rgba(0,0,0,.85),
    0 70px 90px -50px rgba(0,0,0,.9);
  transform:rotateY(-17deg) rotateX(5deg) rotateZ(.6deg)}
.phone .screen{border-radius:20px;height:352px;padding:26px 15px;
  background:
    linear-gradient(200deg,rgba(0,230,118,.16),transparent 46%),
    linear-gradient(160deg,#20242c,#0e1014);
  position:relative;overflow:hidden}
.phone .screen::after{content:'';position:absolute;inset:0;
  background:linear-gradient(115deg,rgba(255,255,255,.13) 0%,
    rgba(255,255,255,0) 34%);pointer-events:none}
.apps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px 11px}
.app{aspect-ratio:1;border-radius:13px;background:rgba(255,255,255,.07)}
.app.real{background:var(--bg);border:1px solid rgba(255,255,255,.1);
  display:flex;align-items:center;justify-content:center;padding:15%;
  box-shadow:0 5px 12px -4px rgba(0,0,0,.8)}
.applab{margin-top:7px;text-align:center;font-size:8px;color:#cfd5dd;
  letter-spacing:.02em}
.appwrap{display:flex;flex-direction:column}

/* A browser tab. The favicon at the size that decided the whole system. */
.browser{width:430px;border-radius:12px;overflow:hidden;
  background:#22262e;border:1px solid var(--border);
  box-shadow:0 24px 40px -20px rgba(0,0,0,.85);
  transform:rotateY(13deg) rotateX(4deg)}
.chrome{display:flex;align-items:flex-end;gap:7px;padding:11px 12px 0;
  background:#1a1d24}
.dot{width:10px;height:10px;border-radius:50%;margin-bottom:11px}
.tab{display:flex;align-items:center;gap:8px;background:#2c3038;
  padding:9px 15px;border-radius:9px 9px 0 0;font-size:11.5px;
  color:var(--ink2);white-space:nowrap}
.tab .mark{width:15px;flex:none}
.bar{height:34px;background:#2c3038;display:flex;align-items:center;
  padding:0 14px}
.url{background:#1a1d24;border-radius:7px;height:21px;flex:1;
  display:flex;align-items:center;padding:0 10px;
  font-family:ui-monospace,monospace;font-size:10.5px;color:var(--ink3)}
.viewport{height:132px;background:
  linear-gradient(180deg,#191c23,#14171d);padding:20px}
.skel{height:9px;border-radius:5px;background:rgba(255,255,255,.09);
  margin-bottom:9px}

/* A business card, two sides, lit from upper left. */
.card3d{width:290px;height:172px;border-radius:9px;position:relative;
  overflow:hidden;
  box-shadow:0 20px 34px -16px rgba(0,0,0,.9),
             0 1px 0 rgba(255,255,255,.1) inset;
  transform:rotateY(-13deg) rotateX(7deg)}
.card3d.front{background:linear-gradient(145deg,#232830,#14171c);
  display:flex;align-items:center;justify-content:center;padding:40px}
.card3d.back{background:linear-gradient(145deg,#f4f6f8,#dfe4ea);
  color:#16191f;padding:26px;display:flex;flex-direction:column;
  justify-content:space-between}
.card3d::after{content:'';position:absolute;inset:0;
  background:linear-gradient(118deg,rgba(255,255,255,.16),
    rgba(255,255,255,0) 42%);pointer-events:none}
.card3d.back .nm{font-weight:700;font-size:15px}
.card3d.back .dm{font-family:ui-monospace,monospace;font-size:11px;
  color:#5b626d}

/* An embroidered patch: a thread texture and a raised edge, not a flat fill. */
.patch{width:180px;height:180px;border-radius:50%;position:relative;
  display:flex;align-items:center;justify-content:center;padding:34px;
  background:
    repeating-linear-gradient(48deg,rgba(0,0,0,.16) 0 1.5px,
      transparent 1.5px 3.5px),
    radial-gradient(75% 75% at 32% 26%,#31414f,#1b242c);
  box-shadow:0 0 0 7px #223040 inset,
             0 0 0 9px rgba(255,255,255,.08) inset,
             0 18px 30px -14px rgba(0,0,0,.9);
  transform:rotateX(11deg) rotateZ(-5deg)}
.patch .mark{filter:drop-shadow(0 1.5px 0 rgba(0,0,0,.45))}

/* ---- do and do not ---------------------------------------------------- */
.rules{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:32px}
.rule{border-radius:12px;padding:22px;border:1px solid var(--border);
  background:var(--surface)}
.rule.no{border-color:rgba(255,130,172,.42)}
.rule.yes{border-color:rgba(0,230,118,.42)}
.rule .tag{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  font-weight:700;margin-bottom:12px}
.rule.no .tag{color:var(--pink)}
.rule.yes .tag{color:var(--green)}
.rule ul{list-style:none;font-size:15px;color:var(--ink2)}
.rule li{padding:7px 0 7px 20px;position:relative}
.rule li::before{position:absolute;left:0;top:7px;font-weight:700}
.rule.no li::before{content:'\\00d7';color:var(--pink)}
.rule.yes li::before{content:'\\2713';color:var(--green)}

.foot{padding:70px 56px 96px;text-align:center;color:var(--ink3);font-size:14px}

/* ---- print ------------------------------------------------------------ */
@page{size:A4 landscape;margin:12mm}
@media print{
  html,body{background:#16191f !important;
    -webkit-print-color-adjust:exact;print-color-adjust:exact}
  section{break-after:page;page-break-after:always;
    break-inside:avoid;page-break-inside:avoid;
    padding:34px 0;border-bottom:0;max-width:none}
  section:last-of-type{break-after:auto;page-break-after:auto}
  .grid,.stage,.rules,.swatches,.ladder{break-inside:avoid;
    page-break-inside:avoid}
  h1{font-size:52px}
  h2{font-size:30px}
  p{font-size:13.5px}
  .foot{break-before:page;page-break-before:always}
  /* The tilts are a screen device. On paper they only cost legibility. */
  .phone,.browser,.card3d,.patch{transform:none}
  .stage{padding:26px}
}
"""


# ---------------------------------------------------------------- the content

def build_html():
    sym_primary = inline('symbol-primary-color-reversed.svg', '100%')
    sym_compact = inline('symbol-compact-color-reversed.svg', '100%')

    def rung(name, px):
        return ('<div class="rung">%s<span class="cap">%dpx</span></div>'
                % (inline(name, '%dpx' % px), px))

    # The .sw tiles need their grid container. Without it they are block-level
    # and the palette renders as five full-width bars.
    swatches = '<div class="swatches">' + ''.join(
        '<div class="sw"><div class="chip" style="background:%s"></div>'
        '<div class="meta"><b>%s</b><span>%s</span></div></div>'
        % (hexv, label, hexv)
        for label, hexv in (('Base', '#16191f'), ('Surface', '#2c3038'),
                            ('Raised', '#373c46'), ('Primary text', '#e9edf2'),
                            ('Green', '#00e676'))) + '</div>'

    # Seven neighbours, so the home screen reads as a home screen. Three left
    # the grid one short of a second row and the phone looked unfinished.
    apps = ''.join('<div class="app"></div>' for _ in range(7))

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Composer Atlas Brand Guidelines</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&display=swap">
<style>%(css)s</style>
</head>
<body>

<section>
  <div style="width:150px;margin-bottom:46px">%(sym_primary)s</div>
  <p class="eyebrow">Brand guidelines</p>
  <h1>Composer&nbsp;Atlas</h1>
  <p class="lead" style="margin-top:26px">A reference instrument, not a growth
  story. An identity built from the measured vocabulary of real cartography.</p>
  <p style="margin-top:40px;color:var(--ink3);font-size:14px">
  Version 1.0 &middot; 28 September 2026 &middot; Concept work, not yet adopted</p>
</section>

<section>
  <p class="eyebrow">01 &mdash; The brief</p>
  <h2>Mapped territory</h2>
  <p class="lead">Thousands of automated strategies charted and navigable, so a
  reader can understand one before committing money to it.</p>
  <p>The product's promise is specific and it is not a promise about returns:
  <em>the drawdown printed next to the return rather than beneath it</em>. That
  sentence rules out most of what this category's logos do, because a site whose
  first principle is transparency over hype cannot open with a picture of going
  up.</p>
  <div class="grid g3">
    <div class="card"><h3>Primary audience</h3><p>Self-directed retail investors
    already using Composer, who want to understand a strategy before cloning
    it.</p></div>
    <div class="card"><h3>Secondary</h3><p>Systematic-investing learners who know
    what a moving average is but have never built a strategy.</p></div>
    <div class="card"><h3>Position</h3><p>An independent reference. Worth more,
    not less, now that the platform it documents has been acquired.</p></div>
  </div>
</section>

<section>
  <p class="eyebrow">02 &mdash; The competitive edge</p>
  <h2>What everyone else does</h2>
  <p>Eight brands were analysed across retail systematic investing, screeners,
  backtesters and research publishers. They converge hard.</p>
  <table>
    <tr><th>They share</th><th>What it signals</th><th>Why it is out</th></tr>
    <tr><td>The upward-right arrow, rising line, candlestick or bar ramp</td>
        <td>Performance</td>
        <td>It is a claim about returns. This site does not make one</td></tr>
    <tr><td>Blue as the primary</td><td>Finance trust</td>
        <td>The category default, and now specifically the acquirer's territory</td></tr>
    <tr><td>Globes, pins, compass roses, folded paper</td><td>"Atlas"</td>
        <td>The four most obvious drawings. One of them is the emoji this
        replaces</td></tr>
    <tr><td>Rounded geometric sans, gradients, glow</td><td>Consumer startup</td>
        <td>This competes with research houses for credibility, not with a
        neobank for warmth</td></tr>
  </table>
  <p style="margin-top:28px"><strong>The opening.</strong> Two of the eight are
  trusted precisely because they look like instruments rather than products, and
  one earns institutional authority through pure restraint. The decorated end of
  the category belongs to businesses selling a feeling about money. This site
  sells an accurate picture, so restraint is the honest expression of the
  product rather than a style preference laid over it.</p>
</section>

<section>
  <p class="eyebrow">03 &mdash; The vocabulary</p>
  <h2>Four words, all of them real</h2>
  <p>The obvious vocabulary for "atlas" was ruled out, so the mark is built from
  terms a cartographer would recognise. Every shape in the system is one of
  these four.</p>
  <div class="grid g4">
    <div class="card"><h3>Neatline</h3><p>The border that frames a map plate.
    Every real map has one. Almost no logo does.</p></div>
    <div class="card"><h3>Parallel</h3><p>A line of latitude. Straight and
    horizontal, which is the calm axis.</p></div>
    <div class="card"><h3>Meridian</h3><p>A line of longitude. It bows away from
    centre, and that bow is the whole argument.</p></div>
    <div class="card"><h3>Index cell</h3><p>One cell of the graticule, filled.
    An atlas finds a place by its cell reference.</p></div>
  </div>
  <p style="margin-top:30px"><strong>The bow is the load-bearing decision.</strong>
  A grid of straight lines is a spreadsheet, and a spreadsheet is the wrong
  metaphor for a product that argues numbers need context. Curve the interior
  meridians the way a pseudocylindrical projection does and the same grid becomes
  a map. Nothing else in the mark carries that meaning, and removing it would
  leave a table.</p>
</section>

<section>
  <p class="eyebrow">04 &mdash; What was explored</p>
  <h2>Four directions, judged from renders</h2>
  <p>Every concept was rasterised at 16, 32 and 512 pixels, in colour and in
  grayscale, on light and dark grounds, and judged from the screenshot. Never
  from the drawing.</p>
  <div class="grid g4">
    <div class="card">%(c_a)s<h3>A &middot; Neatline</h3>
      <p>Frame plus one green parallel. Clean and confident large.
      <strong>Fails at 16px:</strong> the parallel vanishes and it becomes an
      empty rectangle.</p></div>
    <div class="card">%(c_c)s<h3>C &middot; Index cell</h3>
      <p>The full 3x3 graticule with one located cell. The strongest mark at
      size. Fills into a smudge at 16px.</p></div>
    <div class="card">%(c_d)s<h3>D &middot; Evolved</h3>
      <p>The same graticule at 2x2 with a heavier stroke and a deeper bow. The
      only version that holds at 16px.</p></div>
    <div class="card" style="display:flex;flex-direction:column;
      justify-content:center"><h3>B &middot; Wordmark</h3>
      <p>Archivo SemiBold caps, hand-kerned, the word space replaced by a green
      graticule tick. Locks up with either symbol.</p></div>
  </div>
  <p style="margin-top:30px"><strong>One concept was corrected rather than
  defended.</strong> The wordmark originally ran a rule through each O's counter.
  It rendered as a slashed Scandinavian O and the word read
  <code>C&Oslash;MPOSER</code>. It was removed outright, not thinned, because a
  detail that changes which letters a reader sees is not a detail, and a lighter
  version of it would fail the same way more quietly.</p>
</section>

<section>
  <p class="eyebrow">05 &mdash; The decision</p>
  <h2>Not four rivals. One system.</h2>
  <p class="lead">C and D are the same idea at two levels of detail, and the
  render check is what proved it.</p>
  <div class="stage" style="padding:52px">
    <div class="ladder">
      %(ladder)s
    </div>
  </div>
  <p style="margin-top:32px">The primary mark carries the projection and the
  located cell. Below 33 pixels its eight interior gaps merge, so the compact
  mark takes over: the same neatline, the same bow, the same green cell, with
  two divisions instead of eight. <strong>A reader who meets both never registers
  the substitution</strong>, which is the only test a responsive logo has to
  pass.</p>
</section>

<section>
  <p class="eyebrow">06 &mdash; The system</p>
  <h2>Lockups</h2>
  <div class="grid g2">
    <div class="card"><div style="padding:14px 0">%(lock_h)s</div>
      <h3>Horizontal</h3><p>The default. Minimum 288px wide, set by the symbol
      rather than by the type.</p></div>
    <div class="card"><div style="padding:14px 0;max-width:260px">%(lock_s)s</div>
      <h3>Stacked</h3><p>For square and narrow spaces. Minimum 120px wide.</p></div>
  </div>
  <table>
    <tr><th>Asset</th><th>Minimum</th><th>What sets the floor</th></tr>
    <tr><td>Compact symbol</td><td>16px</td>
        <td>The lowest size anything here survives, verified from a 16px render</td></tr>
    <tr><td>Primary symbol</td><td>32px</td>
        <td>Below it the interior gaps merge</td></tr>
    <tr><td>Wordmark alone</td><td>120px wide</td>
        <td>Cap height drops under 8px and Archivo's counters close</td></tr>
    <tr><td>Horizontal lockup</td><td>288px wide</td>
        <td>The symbol occupies the full height, so its 32px floor becomes the
        lockup's 288px floor. Use the compact lockup below this</td></tr>
    <tr><td>Stacked lockup</td><td>120px wide</td><td>Cap height</td></tr>
  </table>
  <h3 style="margin-top:44px">Clear space</h3>
  <p>One graticule cell on every side, which is the mark's own unit rather than
  an arbitrary ratio. Nothing else enters that box.</p>
  <div class="clear"><div class="inner" style="width:120px">%(sym_primary2)s</div></div>
</section>

<section>
  <p class="eyebrow">07 &mdash; Colour</p>
  <h2>One accent, and it means something</h2>
  <p>The palette was rebuilt with every step solved for a measured contrast
  ratio. The logo does not introduce a colour; it borrows the one the product
  already uses, in a third role the original rule did not anticipate:
  <em>green as identity</em> rather than green as a value.</p>
  %(swatches)s
  <p style="margin-top:30px"><strong>The constraint that follows from it.</strong>
  On the site, green means a positive number or a primary action. So the mark
  never pairs green with an arrow, a rising line, or anything else that reads as
  a value, or the logo would start making a performance claim on every page it
  appears on.</p>
  <table>
    <tr><th>Treatment</th><th>Ink</th><th>Accent</th><th>Use</th></tr>
    <tr><td>Colour</td><td>#16191f</td><td>#00e676</td><td>Light grounds</td></tr>
    <tr><td>Colour reversed</td><td>#e9edf2</td><td>#00e676</td>
        <td>Dark grounds, including the site</td></tr>
    <tr><td>Mono black</td><td>#16191f</td><td>collapses to ink</td>
        <td>One-plate print, fax, engraving</td></tr>
    <tr><td>Mono white</td><td>#e9edf2</td><td>collapses to ink</td>
        <td>Reversed one-colour</td></tr>
  </table>
  <p style="margin-top:22px">The single-colour versions keep the filled cell
  because it is a <strong>fill against open cells</strong>, not one hue beside
  another. It survives being flattened, photocopied or stitched.</p>
</section>

<section>
  <p class="eyebrow">08 &mdash; In place</p>
  <h2>Where it has to work</h2>
  <p>This brand has never been photographed, so nothing below is a photograph.
  Each surface is drawn, and each one is a size or a medium that has already
  changed a decision in this system.</p>

  <div class="stage">
    <div class="phone">
      <div class="screen">
        <div class="apps">
          <div class="appwrap"><div class="app real">%(app_icon)s</div>
            <div class="applab">Atlas</div></div>
          %(apps)s
        </div>
      </div>
    </div>

    <div class="browser">
      <div class="chrome">
        <span class="dot" style="background:#ff5f57"></span>
        <span class="dot" style="background:#febc2e"></span>
        <span class="dot" style="background:#28c840"></span>
        <div class="tab">%(fav)s Composer Atlas</div>
      </div>
      <div class="bar"><div class="url">composeratlas.com</div></div>
      <div class="viewport">
        <div class="skel" style="width:52%%"></div>
        <div class="skel" style="width:86%%"></div>
        <div class="skel" style="width:74%%"></div>
        <div class="skel" style="width:40%%;background:rgba(0,230,118,.35)"></div>
      </div>
    </div>
  </div>

  <div class="stage" style="margin-top:22px">
    <div class="card3d front"><div style="width:100%%">%(lock_h2)s</div></div>
    <div class="card3d back">
      <div style="width:44px">%(sym_dark)s</div>
      <div><div class="nm">Composer Atlas</div>
        <div class="dm">composeratlas.com</div></div>
    </div>
    <div class="patch"><div style="width:100%%">%(sym_white)s</div></div>
  </div>

  <p style="margin-top:30px"><strong>The patch is the reason the merchandise file
  exists.</strong> Reproduced 25mm wide, the primary mark's stroke is 1.09mm.
  That survives print and does not survive an embroidery head, so merchandise
  uses the compact mark, whose stroke is 1.96mm and whose narrowest gap is
  11.4mm. Both clear the 1mm floor.</p>
</section>

<section>
  <p class="eyebrow">09 &mdash; Usage</p>
  <h2>How to keep it intact</h2>
  <div class="rules">
    <div class="rule yes"><div class="tag">Do</div><ul>
      <li>Use the compact mark at 32px and below, and for anything stitched or
      engraved</li>
      <li>Leave one graticule cell of clear space on every side</li>
      <li>Reverse to the light ink on any ground darker than the surface
      colour</li>
      <li>Use the supplied single-colour files when a process cannot hold the
      green</li>
      <li>Keep the green for the index cell and the word tick, and nothing
      else</li>
    </ul></div>
    <div class="rule no"><div class="tag">Do not</div><ul>
      <li>Set the primary mark below 32px, where the gaps merge into a smudge</li>
      <li>Recolour the cell, or add a second accent</li>
      <li>Straighten the meridians. Without the bow it is a table</li>
      <li>Add a gradient, glow, shadow or outline. The system has none by
      design</li>
      <li>Rebuild the lockup by hand, or respace the wordmark</li>
      <li>Place the mark beside an arrow or a rising line</li>
    </ul></div>
  </div>
</section>

<div class="foot">
  Composer Atlas brand guidelines &middot; concept work, not yet adopted &middot;
  28 September 2026<br>
  Wordmark set in Archivo by Omnibus-Type, SIL Open Font License 1.1.
</div>

</body>
</html>
""" % {
        'css': CSS,
        'sym_primary': sym_primary,
        'sym_primary2': inline('symbol-primary-color-reversed.svg', '100%'),
        'c_a': inline('../concepts/concept-a-neatline-symbol-light.svg', '62px')
               if os.path.exists(os.path.join(LOGO, '..', 'concepts',
                                              'concept-a-neatline-symbol-light.svg'))
               else '',
        'c_c': inline('symbol-primary-color-reversed.svg', '62px'),
        'c_d': inline('symbol-compact-color-reversed.svg', '62px'),
        'ladder': ''.join(
            rung('symbol-compact-color-reversed.svg', px) for px in (16, 24, 32)
        ) + ''.join(
            rung('symbol-primary-color-reversed.svg', px) for px in (48, 96, 168)
        ),
        'lock_h': inline('lockup-horizontal-color-reversed.svg', '100%'),
        'lock_h2': inline('lockup-horizontal-color-reversed.svg', '100%'),
        'lock_s': inline('lockup-stacked-color-reversed.svg', '100%'),
        'swatches': swatches,
        'app_icon': inline('symbol-compact-color-reversed.svg', '100%'),
        'apps': apps,
        'fav': inline('symbol-compact-color-reversed.svg', '15px'),
        'sym_dark': inline('symbol-primary-color.svg', '100%'),
        'sym_white': inline('symbol-compact-white.svg', '100%'),
    }


def main():
    html = build_html()
    with open(OUT_HTML, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('%s  (%d bytes)' % (OUT_HTML, os.path.getsize(OUT_HTML)))

    url = 'file:///' + os.path.abspath(OUT_HTML).replace('\\', '/')
    base = [edge(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
            '--user-data-dir=' + profile_dir(), '--disable-sync',
            '--disable-component-update', '--no-first-run']

    shot = os.path.abspath(os.path.join('brand', 'checks', 'presentation.png'))
    os.makedirs(os.path.dirname(shot), exist_ok=True)
    subprocess.run(base + ['--window-size=1280,13000', '--screenshot=' + shot,
                           url], check=True, capture_output=True, timeout=300)
    print('%s  (%d bytes)' % (shot, os.path.getsize(shot)))

    pdf = os.path.abspath(OUT_PDF)
    subprocess.run(base + ['--no-pdf-header-footer', '--print-to-pdf=' + pdf,
                           url], check=True, capture_output=True, timeout=300)
    print('%s  (%d bytes)' % (OUT_PDF, os.path.getsize(pdf)))


if __name__ == '__main__':
    main()
