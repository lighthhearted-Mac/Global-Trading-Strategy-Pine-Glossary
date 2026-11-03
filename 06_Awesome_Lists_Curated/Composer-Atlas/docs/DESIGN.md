# Composer Atlas: Design System

**Version:** 1.31
**Status:** Active
**Last Updated:** 2026-10-07

All values in this document are derived from `css/main.css` and `js/app.js`: the source files are the
ground truth. Where this document and the CSS disagree, the CSS wins and the disagreement is marked
inline as a **Discrepancy** rather than quietly overwritten, so the author can decide which side was
the mistake. See PRD.md Section 24, "Documentation Versus Reality", for the full register.

**Scope, stated plainly.** This document covers the shared design system in `css/main.css`, which is
what every page loads. It does **not** yet cover the three tool pages that carry their own inline
`<style>` blocks on top of it. See Section 10, "Undocumented Surfaces", for what those are and why
they are called out rather than left silently missing.

---

## 1. Design Philosophy

Composer Atlas uses a dark, editorial visual language inspired by Composer.trade's interface. It pairs the energy and color vocabulary of Composer with the structured, wiki-style readability of a reference document. The result is a site that feels authoritative and trustworthy without being sterile.

Every visual decision serves the user's ability to understand information. Color is used semantically. Typography is used for hierarchy. Whitespace is not wasted. Nothing is decorative for its own sake.

---

## 2. Color Palette

All colors are defined as CSS custom properties in the `:root` block of `css/main.css`.

### CSS Custom Properties

**Rebuilt 2026-09-09 (v1.82.0).** The owner asked for backgrounds in the range Visual Studio's dark
theme uses. Measured relative luminance of the reference: VS Code Dark+ editor `#1e1e1e` is 0.0130,
Dark Modern `#1f1f1f` is 0.0137, the sidebar `#252526` is 0.0186. The palette this replaced sat at
**0.0040**, roughly three and a half times darker than the editor it was meant to resemble.

| Token | Hex | Usage |
|---|---|---|
| `--color-bg` | `#16191f` | Page background (`body` background). L 0.0096, just under VS Dark+ |
| `--color-surface` | `#2c3038` | Card and panel background. Separation 1.33 above bg |
| `--color-surface-raised` | `#373c46` | Elevated surface; **`.db-table tbody tr:hover`**; nav active state. 1.20 above surface |
| `--color-border` | `#4c515c` | Default borders and dividers. 1.66 above surface |
| `--color-border-hover` | `#616672` | Border color on hover. 2.30 above surface |
| `--color-primary` | `#e9edf2` | Body text, headings, primary content |
| `--color-secondary` | `#d2d8df` | Labels, captions, metadata, muted text, `<p>` elements |
| `--color-disabled` | `#b8bec6` | **Tertiary text.** Breadcrumb separators, captions, table labels, `.risk-cat.is-absent`, `.j-null` |
| `--color-green` | `#00e676` | Positive returns, CTAs, active nav, highlights, "View Strategy" links |
| `--color-pink` | `#ff82ac` | Negative returns, max drawdown, warning states |
| `--color-blue` | `#68afff` | Links, interactive element hover borders, focus rings |
| `--color-yellow` | `#f5c518` | Neutral caution indicators, mean/median return values |
| `--color-purple` | `#b39dff` | Momentum tag, strategy-concept badge |
| `--color-positive` | alias of green | Semantic role, added v1.82.0 |
| `--color-negative` | alias of pink | Semantic role, added v1.82.0 |
| `--color-caution` | alias of yellow | Semantic role, added v1.82.0 |
| `--color-info` | alias of blue | Semantic role, added v1.82.0 |
| `--color-brand` | alias of green | **Identity**, not a value. Added when the brand system was adopted; see the Semantic Color Rules below and Section 11 |

**Every step is solved for a contrast ratio, not picked by eye.** sRGB is not linear, so adding a
fixed amount to each channel is a different perceptual step at every brightness level, and a ladder
built that way drifts. The surface step matters most: **a separation below about 1.3 is not an edge a
person can see**, and panels are most of the page.

> **The failed first attempt is worth recording, because the mistake is easy to repeat.** v1.82.0's
> first pass raised the *borders* past the visibility threshold (1.18 to 1.55) but left the
> *surfaces* at 1.10. Every number improved, and the owner, looking at the result, could not see any
> difference at all. That was the correct reading: borders are thin, surfaces are most of the pixels.

> **`--color-disabled` is a misnomer and is knowingly kept.** It renders breadcrumb separators,
> captions, table labels, `.risk-cat.is-absent` body copy and `.j-null`, all of which a reader is
> meant to read. It is therefore set to clear AA rather than to something dim enough to deserve the
> name. Renaming it touches 30 rules in `css/main.css` and 61 places in markup, which belongs in its
> own mechanical commit rather than inside a visual change. This supersedes the 2026-08-24
> discrepancy note, which recorded the table claiming `#444444` while the code said `#c0c0c0`; the
> code was right then too.

> **The prior palette had the grey hierarchy backwards.** `--color-disabled` (`#c0c0c0`) was
> *brighter* than `--color-secondary` (`#b0b0b0`), so the text meant to recede was the most prominent
> grey on the site. Fixed here.

### Inline rgba() Values (Not Named Properties)

The following color variants appear as inline `rgba()` values in `css/main.css` and are not defined as named CSS custom properties:

| Usage | Value |
|---|---|
| Tag background: RSI, 200d-MA | `rgba(104, 175, 255, 0.08)` |
| Tag border: RSI, 200d-MA | `rgba(104, 175, 255, 0.25)` |
| Tag background: momentum | `rgba(179, 157, 255, 0.08)` |
| Tag border: momentum | `rgba(179, 157, 255, 0.25)` |
| Tag background: vix-tiers | `rgba(245, 197, 24, 0.08)` |
| Tag border: vix-tiers | `rgba(245, 197, 24, 0.25)` |
| Tag background: leveraged-etfs | `rgba(255, 130, 172, 0.08)` |
| Tag border: leveraged-etfs | `rgba(255, 130, 172, 0.25)` |
| Tag background: sharpe/calmar/max-drawdown | `rgba(0, 230, 118, 0.08)` |
| Tag border: sharpe/calmar/max-drawdown | `rgba(0, 230, 118, 0.25)` |
| Badge background: indicator | `rgba(104, 175, 255, 0.1)` |
| Badge border: indicator | `rgba(104, 175, 255, 0.2)` |
| Badge background: risk-metric | `rgba(255, 130, 172, 0.1)` |
| Badge border: risk-metric | `rgba(255, 130, 172, 0.2)` |
| Badge background: asset-class | `rgba(245, 197, 24, 0.1)` |
| Badge border: asset-class | `rgba(245, 197, 24, 0.2)` |
| Badge background: strategy-concept | `rgba(179, 157, 255, 0.1)` |
| Badge border: strategy-concept | `rgba(179, 157, 255, 0.2)` |
| Inline code background | `rgba(0, 230, 118, 0.08)` |
| Nav background | `rgba(22, 25, 31, 0.95)` |

### Semantic Color Rules

- **Green**: used for positive values, primary CTAs, and **identity**. Never decorative.
  Identity is a third role, added when the brand system was adopted, and it is an *addition*
  to this rule rather than an exception to it: a logo is neither a positive value nor a call to
  action, so the original wording had no place to put it. `--color-positive` means a number went
  up; `--color-brand` means this is us. Both resolve to `#00e676` today and are not obliged to
  forever. **The constraint that comes with the third role:** brand green is never paired with an
  arrow, a rising line, or anything else that reads as a value, because that is exactly what
  collapses identity back into data. See Section 11.
- **Pink**: used exclusively for negative values (drawdown, losses). Never decorative.
- **Purple**: reserved for momentum tags and strategy-concept glossary badges.
- **Blue**: reserved for interactive states (links, focus rings, hover borders). Not used for data values.
- **Yellow**: used for neutral/caution indicators (mean period return, median period return).

### The referral surfaces (v1.31)

Four components, all built from tokens with no raw colour literals, so they follow both themes.

- **`.ref-banner`**, the first-visit strip. **It lives inside `.page`, not before it.** `.nav` is
  `position: fixed; top: 0`, so anything first in normal flow renders at y=0 *behind* the nav;
  `.page` already carries `padding-top: var(--nav-height)` for exactly this reason. A DOM probe will
  report such an element visible, `display: block`, with a real height, and be correct: painted,
  then covered. **Only a screenshot catches it.**
- **`.ref-cta`**, the offer block under the disclosure, and **`.ref-cta-strip`**, the lighter repeat
  further down the page. Both wash green at low alpha over whatever surface they sit on.
- **`.ref-code-block`** and **`.ref-code-inline`**, the code itself. Mono, and the block form uses
  `word-break: break-all` so a long code never pushes the copy button off a phone screen.
- **`.ref-disclosure`**, caution-toned with a left bar. Caution rather than warning on purpose: it
  is a notice the reader should not miss, not an error.

**The code is never written into markup.** `REFERRAL_CODE` in `app.js` is the single definition and
`renderReferral()` fills every `[data-referral-code]` element. The copy buttons fall back to a
hidden textarea and `execCommand`, because `navigator.clipboard` is undefined on `file://` and on
any insecure origin.

### Themes (v1.30)

**The site has two themes and dark is the default.** `:root` carries the dark values; a
`:root[data-theme="light"]` block overrides them. **There is deliberately no
`prefers-color-scheme` query**: the owner's instruction is that the site opens dark and the visitor
chooses otherwise, so the system setting is not consulted at all.

**The switch is a single button in the nav** showing a sun or a moon. The glyph names the
**destination**, not the current state: a sun offers light, a moon offers dark. The emoji is
`aria-hidden` and the button carries a real `aria-label` that says what the button does, because an
emoji is a picture and rule 3 of the colour standard forbids a control that relies on one alone.

**The theme is applied by a small inline script in every page's `<head>`, not by `js/app.js`.**
`app.js` is deferred, so applying it there would paint a dark page first and flash to light on every
single navigation. The boot script is small enough to inline and runs before the first paint. The
choice is remembered in `localStorage` under `ca-theme`, wrapped in try/catch so private mode falls
through to the dark default rather than throwing.

**Light surfaces are the Template Interface Color Standard's**: canvas white, surface `gray-5`,
raised `gray-10`, border `gray-20`, strong border `gray-50`. **The hardest pair inverts between the
modes.** In dark mode it is the brightest surface, because light text loses contrast as the panel
lightens; in light mode it is the darkest surface. Every light value is measured on
`--color-surface-raised` `#d8dee5`.

**Brand green is not `#00e676` in light mode, and that is not a change to the brand.** `#00e676`
measures 1.67:1 on white: as link or button text it is illegible. The light accent is the same hue
at `green-60`. The dark theme, which is what the site opens in and what every brand asset is drawn
against, is untouched.

### Colour channels, and why tints are not literals (v1.30)

Every translucent wash in the stylesheet composes from an `--rgb-*` triple rather than a hardcoded
`rgba(245, 197, 24, 0.1)`. **A literal is a copy of a token and does not follow when the token
moves**, which was found sixteen times during the palette rebuild, and it is also what would have
made a light theme impossible: every tint would have stayed a dark-mode colour on a white card.
There are now **zero raw colour literals in any rule** in `css/main.css`.

### Semantic roles after the colour audit (v1.30)

| Role | Means | Dark | Light |
|---|---|---|---|
| `--color-accent` | Links, primary actions, identity | green | `green-60` |
| `--color-positive` | A number went up | green | `green-60` |
| `--color-negative` | A loss, a danger | **red** (was pink) | `red-60` |
| `--color-caution` | A warning | yellow | `yellow-60` |
| `--color-info` | A neutral notice | **teal** (was blue) | `teal-60` |
| `--color-focus` | The focus ring | blue | `blue-60` |

**Blue, pink and purple now carry no status meaning.** They are data and chart colours. Blue is the
focus ring specifically because a focus ring must not be mistaken for a selected or positive state.

**THE ONE DELIBERATE DEVIATION FROM THE STANDARD, owner ruling 2026-10-07.** The standard says a
brand colour goes in the accent role, and separately that green means success and nothing else.
**Both cannot hold when the brand is green.** Green therefore serves accent and positive at once.
The three names are kept apart (`--color-accent`, `--color-positive`, `--color-brand`) because they
are three jobs even where they are one colour, and they are not required to resolve the same way
forever.

**A value must never name a hue.** `colorClass()` returns `text-positive` and `text-negative`, not
`text-green` and `text-pink`. Naming the colour is exactly why pink survived as the loss colour long
after the palette gained a red: repointing the token could not chase every call site.

### Contrast Ratios (WCAG AA)

**Quoted against `--color-surface-raised` (`#373c46`), the brightest surface and therefore the
hardest case.** Quoting the easy pair against `--color-bg` is how a palette passes on paper and fails
on a card. Every value below also clears 4.5:1 on `--color-bg` and `--color-surface`.

| Foreground | On raised `#373c46` | On surface `#2c3038` | On bg `#16191f` |
|---|---|---|---|
| `#e9edf2` (primary) | 9.41 | 11.25 | 14.97 |
| `#d2d8df` (secondary) | 7.71 | 9.22 | 12.26 |
| `#b8bec6` (tertiary) | 5.91 | 7.07 | 9.40 |
| `#00e676` (green) | 6.63 | 7.93 | 10.55 |
| `#ff82ac` (pink) | 4.77 | 5.70 | 7.58 |
| `#68afff` (blue) | 4.83 | 5.77 | 7.68 |
| `#f5c518` (yellow) | 6.79 | 8.12 | 10.80 |
| `#b39dff` (purple) | 4.84 | 5.79 | 7.70 |
| `#fe8786` (red, v1.30) | 4.77 | 5.70 | 7.58 |
| `#00beba` (teal, v1.30) | 4.77 | 5.70 | 7.58 |

`#16191f` used as dark text on a bright chip measures 10.55 on green and 10.80 on yellow.

**The two lower greys were raised again at v1.83.1, and nothing was failing when they were.** An
audit of every visible paragraph across all ten pages, reading computed colours from the live
document rather than from the CSS, found body prose at **10.24:1 on the page background and 7.69:1 on
a card**, comfortably past AA, and the owner still reported it as hard to read. **AA is a floor for
whether text is perceivable, not a target for whether a long paragraph is comfortable**, and a page of
body copy is exactly where that gap shows. Secondary went 6.44 to 7.71 on the raised surface, tertiary
4.67 to 5.91, and the ordering against `--color-primary` (9.41) still holds, which is the constraint
that stops "brighter" from collapsing into "all one colour".

**Pink, blue and purple were re-derived, not carried over.** At their previous values they *failed*
AA on the raised surface once the base came up. That is the constraint that makes a dark theme
impossible to lighten one token at a time: surfaces, greys and accents are one system, and moving one
silently drops another under the line.

**Red and teal were added at v1.30 and the standard's own dark grades could not be used.** The
Template Interface Color Standard's `red-40` `#fe4745` and `teal-40` `#009c99` measure **3.27 and
3.28** against this stylesheet's raised surface, because they are solved against a darker canvas than
`#373c46`. They were re-solved in HLS holding hue and saturation, landing on the same 4.77 the
existing pink carries. **Published values are not safe to copy across a different surface**, which is
the same lesson as the paragraph above, arriving from the opposite direction.

### Light theme contrast (v1.30)

Measured on `--color-surface-raised` `#d8dee5`, the darkest light surface and therefore the hardest
pair in that mode. The inversion is the point: dark mode's worst case is the brightest panel.

| Token | Value | On raised |
|---|---|---|
| `--color-primary` | `#20252a` | 11.40 |
| `--color-secondary` | `#454b53` | 6.50 |
| `--color-disabled` | `#5c6168` | 4.61 |
| `--color-green` | `#00712a` | 4.56 |
| `--color-red` | `#c5001a` | 4.57 |
| `--color-yellow` | `#795d00` | 4.59 |
| `--color-teal` | `#006d6a` | 4.56 |
| `--color-blue` | `#005bc7` | 4.57 worst case |
| `--color-pink` | `#b4226d` | 4.57 |
| `--color-purple` | `#7e3bcb` | 4.59 |
| `--color-border-strong` | `#71767d` | 3.38 |

**Blue and the zoop orange were solved against their composited chip tint, not the plain panel.** A
chip background is a translucent wash, so the plain surface is the easy case and measuring it would
have passed two pairs that fail in place. `blue-60` `#005cc9` came in at 4.49 on the blue chip, 0.01
short, so it moved a grade step to `#005bc7`; zoop's `#a65500` read 4.13 on its own tag tint and was
re-solved at `#954c00` against all five light backgrounds a tag can land on.

---

## 3. Typography

### Font Families

Defined in `:root` in `css/main.css` and loaded via Google Fonts:

```css
--font-sans: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
--font-brand: 'Archivo', 'Inter', sans-serif;
```

Google Fonts import (in `css/main.css`):
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
```

- **Inter**: body text, UI labels, headings, nav links
- **JetBrains Mono**: metric values, strategy IDs, code blocks, `font-mono` utility class
- **Archivo**: the brand face, and **the one font in this list the site does not load.** The
  wordmark is Archivo SemiBold caps, but it ships from `brand/logo/` as drawn outlines rather than
  as live text, so no page needs the font file to render the mark correctly. The token is declared
  without being added to the `@import` above so that it falls back to Inter, which is already
  loaded, and costs nothing. Adding Archivo to the font request is a real per-page cost for one
  line of type, and it waits until something on the site sets live brand copy. See Section 11.

### Type Scale (from css/main.css)

| Element | CSS Rule | Size | Weight | Line Height |
|---|---|---|---|---|
| `h1` | `h1` | `2rem` (32px) | `700` | `1.2` |
| `h2` | `h2` | `1.375rem` (22px) | `700` | `1.3` |
| `h3` | `h3` | `1.125rem` (18px) | `600` | `1.4` |
| `h4` | `h4` | `0.9375rem` (15px) | `600` | n/a |
| Body | `body` | `0.9375rem` (15px) | `400` | `1.6` |
| Hero title | `.hero-title` | `clamp(1.75rem, 4vw, 3rem)` | `700` | `1.15` |
| Hero description | `.hero-desc` | `1.0625rem` (17px) | `400` | `1.7` |

**Hero copy budget, set 2026-09-09 (v1.82.1): the h1 stays under ~60 characters and the
paragraph under ~150.** This is a real constraint, not a style note. At 363 characters the
paragraph pushed the call-to-action buttons below the fold at 1440x900, which is the one thing
a landing hero must not do. It also spent its first two sentences on setup before saying what
the site is. The rule is that the paragraph names the offer and the search terms; the argument
for the site belongs in the sections below it.

**The hero paragraph is not the meta description and must not be written as one.** Section 27
governs `og:description` and `meta name="description"`, which are read in a search result or a
shared link. The hero is read by someone already on the page with a button in front of them.
Conflating the two is what produced the 363-character version.
| Card title | `.card-title` | `0.9375rem` (15px) | `600` | `1.4` |
| Card description | `.card-desc` | `0.875rem` (14px) | `400` | `1.6` |
| Metric value (card) | `.card-metric-value` | `0.875rem` (14px) | `500` | n/a |
| Metrics row label | `.metrics-row dt` | `0.875rem` (14px) | (inherited) | n/a |
| Metrics row value | `.metrics-row dd` | `0.875rem` (14px) | `500` (mono) | n/a |
| Label / eyebrow | `.label`, `.card-metric-label` | `0.6875rem` (11px) | `500` | n/a |
| Tag / badge | `.tag`, `.badge` | `0.75rem` (12px) | `500` | n/a |
| Nav link | `.nav-link` | `0.875rem` (14px) | (inherited) | n/a |
| Mobile nav link | `.mobile-nav-link` | `0.9375rem` (15px) | (inherited) | n/a |
| Footer link | `.footer-links a` | `0.8rem` (12.8px) | (inherited) | n/a |
| Footer legal | `.footer-legal` | `0.75rem` (12px) | (inherited) | `1.6` |
| Footer copy | `.footer-copy` | `0.75rem` (12px) | (inherited) | n/a |
| Prose body | `.prose p` | `0.9375rem` (15px) | (inherited) | `1.7` |
| Prose heading | `.prose h2` | `1.125rem` (18px) | `700` | n/a |
| Stat value | `.stat-value` | `1.5rem` (24px) | `700` (mono) | `1` |
| Stat label | `.stat-label` | `0.75rem` (12px) | (inherited) | n/a |

### Color of Text by Context

- Default `<p>` elements: `color: var(--color-secondary)` (set globally in CSS)
- Headings (`h1`–`h4`): inherit `--color-primary` from body, or set explicitly
- `.text-primary` class: `--color-primary`
- `.text-secondary` class: `--color-secondary`
- `.text-disabled` class: `--color-disabled` (tertiary text, not a disabled state)

---

## 4. Spacing System

**Base unit: 4px.** All spacing values in the codebase are multiples of 4.

### Named CSS Custom Properties

| Token | Value | Usage |
|---|---|---|
| `--nav-height` | `56px` | Fixed nav bar height; `padding-top` on `.page` |
| `--page-px` | `24px` | Horizontal page padding in `.container` and `.nav-inner` |
| `--max-width` | `1280px` | Maximum content width |

### Utility Classes (from css/main.css)

| Class | Value |
|---|---|
| `.py-12` | `padding-top: 48px; padding-bottom: 48px` |
| `.mt-8` | `margin-top: 32px` |
| `.mb-4` | `margin-bottom: 16px` |
| `.mb-6` | `margin-bottom: 24px` |
| `.mb-8` | `margin-bottom: 32px` |
| `.mb-10` | `margin-bottom: 40px` |

### Common Spacing Values in Use

| Value | Context |
|---|---|
| `2px` | Tag padding vertical |
| `4px` | Icon-text gap, breadcrumb gap |
| `5px` | Nav hamburger bar gap, `.btn-sm` vertical padding |
| `6px` | Tag padding horizontal, card-tags gap, breadcrumb gap |
| `8px` | Card tags gap, nav logo gap, metrics section label margin |
| `10px` | Metrics row padding vertical |
| `12px` | Card footer gap, signal header gap, `.btn-sm` horizontal padding |
| `16px` | Card padding, metrics row padding horizontal, section header margin, footer link gap |
| `20px` | Card padding (`.card { padding: 20px }`), metrics section margin |
| `24px` | Page horizontal padding (`--page-px`), section header margin, breadcrumb margin |
| `28px` | Prose h2 margin-top |
| `32px` | Sidebar gap, `.mt-8` |
| `40px` | Grid-2 gap, about-content h2 margin-top |
| `48px` | Hero bottom padding, `.py-12` |
| `56px` | Nav height (`--nav-height`) |
| `64px` | Hero top padding |

---

## 5. Border Radius

Defined as CSS custom properties in `css/main.css`:

| Token | Value | Used On |
|---|---|---|
| `--radius-sm` | `4px` | Tags, badges, tooltip-style elements, hamburger bar border-radius |
| `--radius-md` | `8px` | Buttons, nav links, mobile nav links, metrics table, signal cards, risk box, formula box, compact list |
| `--radius-lg` | `12px` | Cards (`.card`) |

---

## 6. Breakpoints

Mobile-first. Base styles target the smallest viewport; media queries add complexity at larger sizes.

| Min Width | Applied To | What Changes |
|---|---|---|
| `0px` (base) | All elements | Single-column layout; mobile nav visible; hamburger shown |
| `480px` | `.nav-logo-text` | Site name text appears next to 🗺️ emoji in nav |
| `640px` | `.grid-3` | Strategy/glossary card grid changes from 1-column to 2-column |
| `768px` | `.nav-links`, `.nav-cta`, `.nav-hamburger` | Desktop nav links appear; hamburger hides; nav CTA appears |
| `1024px` | `.grid-3`, `.grid-2`, `.detail-sidebar-sticky` | Grid-3 goes to 3-column; Grid-2 (detail layout) goes to `2fr 1fr`; sidebar becomes sticky |

**One max-width query also exists**, and it is the only rule in the stylesheet that runs the other
direction:

| Max Width | Applied To | What Changes |
|---|---|---|
| `640px` | `.tagfilter-label` | The tag-filter bar's label takes `flex-basis: 100%`, dropping the filter chips onto their own row below it (`css/main.css:657`) |

**Narrow-screen hardening (v1.16.7).** `body` carries `overflow-x: clip` and `overflow-wrap:
break-word`. This is not a breakpoint but it governs behaviour below roughly 390px: it stops a stray
overflowing child from letting the whole page scroll sideways and clipping the fixed nav. `clip` is
used rather than `hidden` deliberately, because `hidden` would make `<body>` a scroll container and
break `position: sticky` and `position: fixed` inside it.

**Max content width:** `1280px` (`--max-width`), centered via `.container { max-width: var(--max-width); margin: 0 auto; padding: 0 var(--page-px); }`.

---

## 7. Component Patterns

### Navigation

**Desktop nav (768px+):**

- Fixed to top of viewport; `z-index: 100`; height: `56px` (`--nav-height`)
- Background: `rgba(22, 25, 31, 0.95)` with `backdrop-filter: blur(8px)` and `border-bottom: 1px solid var(--color-border)`
- Logo: 🗺️ emoji (`font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji'`, `font-size: 1.25rem`) + "Composer Atlas" text (hidden below 480px)
- Logo hover: transitions to `--color-green` in 150ms
- Nav links: `--color-secondary` default; `--color-primary` + `bg-surface` on active/hover; 150ms transition
- "Open Composer ↗" button: `.btn-outline-green`: green border, green text; switches to green bg on hover
- Active route detection: `isActive()` function in `renderNav()` in `js/app.js`

**Mobile nav (< 768px):**

- Hamburger button: `36x36px`, `border-radius: --radius-md`; three `1.5px` bars
- Hamburger animates to X when open: bar 1 → `translateY(6.5px) rotate(45deg)`, bar 2 → `opacity: 0`, bar 3 → `translateY(-6.5px) rotate(-45deg)`
- `aria-expanded` attribute drives animation via CSS
- Mobile menu: `.nav-mobile` with class `.open` toggled by JS event listener on `#nav-toggle`
- Mobile menu panel: `background: --color-bg`, `border-top: 1px solid --color-border`, `padding: 12px 16px 16px`, `flex-direction: column`, `gap: 2px`
- Mobile nav links: `0.9375rem`, `padding: 10px 12px`, full-width tap targets

**Nav rendered by:** `renderNav()` in `js/app.js` into `<nav id="nav-root">`.

---

### Buttons

All buttons use `.btn` base class.

| Variant | Class | Background | Text | Border | Hover |
|---|---|---|---|---|---|
| Green filled | `.btn-green` | `--color-green` | `--color-bg` | Transparent | `opacity: 0.9` |
| Outline (default) | `.btn-outline` | Transparent | `--color-primary` | `--color-border` | Border → `--color-border-hover`, bg → surface |
| Outline green | `.btn-outline-green` | Transparent | `--color-green` | `--color-green` | bg → green, text → bg |

| Size | Class | Padding | Font Size |
|---|---|---|---|
| Default | `.btn` | `8px 16px` | `0.875rem` (14px) |
| Small | `.btn-sm` | `5px 12px` | `0.8125rem` (13px) |
| Large | `.btn-lg` | `11px 22px` | `0.9375rem` (15px) |
| Nav CTA | `.btn-outline-green` (override) | `5px 12px` | `0.8125rem` (13px) |

Transition: `opacity 0.15s, background 0.15s, color 0.15s, border-color 0.15s`

All external links use `target="_blank" rel="noopener noreferrer"`.

---

### Strategy Card

Used on the home page strategy grid (`renderStrategyCard()` in `js/app.js`).

```html
<article class="card">
  <h2 class="card-title"><a href="...">Strategy Name</a></h2>
  <p class="card-desc">Short description (3-line clamp)</p>
  <div class="card-metrics">  <!-- 3-column grid -->
    ARR / Max DD / Sharpe
  </div>
  <div class="card-tags"><!-- tag pills --></div>
  <div class="card-footer">
    <a href="..." class="btn btn-sm" style="color:var(--color-green)">View Strategy →</a>
  </div>
</article>
```

**States:**
- Default: `background: --color-surface`, `border: 1px solid --color-border`, `border-radius: --radius-lg (12px)`, `padding: 20px`
- Hover: `border-color: --color-border-hover`; card title color → `--color-green`
- Transition: `border-color 0.15s`

**Card metrics grid:** `grid-template-columns: repeat(3, 1fr)`, `gap: 12px`
- Metric label: `0.6875rem`, `500`, uppercase, `letter-spacing: 0.08em`, `--color-disabled`
- Metric value: `--font-mono`, `0.875rem`, `500`, color-coded (see Section 12 display guidelines)

**Card description:** `-webkit-line-clamp: 3`

---

### StrategyCardCompact

Slim variant used in glossary page sidebars (`renderStrategyListItem()` in `js/app.js`). Single row: strategy name + ARR.

```html
<a href="..." class="strategy-list-item">
  <span>Strategy Name</span>
  <span class="arr text-green">+31.20%</span>
</a>
```

Container: `.strategy-list-compact`: `border: 1px solid --color-border`, `border-radius: --radius-md`, `overflow: hidden`

Row: `.strategy-list-item`: `display: flex`, `justify-content: space-between`, `padding: 10px 12px`, `font-size: 0.875rem`, `--color-secondary`

Hover: `background: --color-surface-raised`, color → `--color-primary`; transition: `background 0.15s`

---

### Concept Card (Glossary)

Used on the glossary index (`renderConceptCard()` in `js/app.js`).

Same `.card` base structure. Contains: category badge + strategy count row, card title (concept name), description (2-line clamp), "Learn more →" link.

Category badge colors: blue (indicator), pink (risk-metric), yellow (asset-class), purple (strategy-concept). See Section 2 for rgba values.

---

### Metrics Table

Used on strategy detail pages (`renderMetricsTable()` in `js/app.js`).

Structure: grouped `<div class="metrics-section">` blocks, each with a section label and a `<dl class="metrics-table">` containing `<div class="metrics-row">` items.

```css
.metrics-table {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.metrics-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid var(--color-border);
}
```

- `<dt>` (label): `0.875rem`, `--color-secondary`
- `<dd>` (value): `--font-mono`, `0.875rem`, `500`, color-coded

Groups: Returns, Risk, Risk-Adjusted, Daily Distribution, Trailing Returns, Metadata.

---

### Tags (GlossaryTag Pills)

Rendered by `renderTag(slug)` in `js/app.js` as `<a href="/glossary.html?slug=...">` links.

```css
.tag {
  display: inline-flex;
  padding: 2px 8px;
  border-radius: 4px;  /* --radius-sm */
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid;
  transition: opacity 0.15s;
}
.tag:hover { opacity: 0.8; }
```

Tag color assignments (from `TAG_CLASSES` in `js/app.js`):

| Slug | CSS Class | Color |
|---|---|---|
| `rsi`, `200d-ma` | `.tag-rsi`, `.tag-200d-ma` | Blue |
| `momentum` | `.tag-momentum` | Purple |
| `vix-tiers` | `.tag-vix-tiers` | Yellow |
| `leveraged-etfs` | `.tag-leveraged-etfs` | Pink |
| `sharpe-ratio`, `calmar-ratio`, `max-drawdown` | `.tag-sharpe-ratio`, etc. | Green |
| `zoop` | `.tag-zoop` | Orange |
| `original` | `.tag-original` | Neutral gray |
| Unknown | `.tag-default` | Surface-raised + secondary |

---

### Category Badges (ConceptCard)

Used on glossary index and detail pages.

```css
.badge {
  display: inline-flex;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid;
}
```

| Category | Class | Color |
|---|---|---|
| `indicator` | `.badge-indicator` | Blue |
| `risk-metric` | `.badge-risk-metric` | Pink |
| `asset-class` | `.badge-asset-class` | Yellow |
| `strategy-concept` | `.badge-strategy-concept` | Purple |

---

### Signal Cards

Used on strategy detail pages to list signals used by the strategy.

```css
.signal-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 8px;
}
.signal-name { font-family: var(--font-mono); font-size: 0.875rem; font-weight: 600; }
.signal-desc { font-size: 0.875rem; color: var(--color-secondary); line-height: 1.6; }
```

Header row: `.signal-header`: `display: flex`, `align-items: center`, `gap: 10px`, `margin-bottom: 8px`. Contains: signal name + a tag pill linking to the related glossary concept.

---

### AI Summary Box

Used at the top of strategy detail pages, directly above the "How It Works" section, to present the Claude-authored `ai_summary` analysis. A purple accent distinguishes it as machine-generated commentary rather than first-party editorial copy.

```css
.ai-summary {
  background: linear-gradient(180deg, rgba(179, 157, 255, 0.06), rgba(179, 157, 255, 0.02));
  border: 1px solid rgba(179, 157, 255, 0.25);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
}
.ai-summary-mark { width: 26px; height: 26px; border-radius: var(--radius-sm); background: rgba(179, 157, 255, 0.12); color: var(--color-purple); }
.ai-summary-title { font-size: 1.125rem; font-weight: 700; color: var(--color-primary); }
.ai-summary-p { font-size: 0.9375rem; color: var(--color-secondary); line-height: 1.75; }
```

Header row: `.ai-summary-header` with `display: flex`, `align-items: center`, `gap: 10px`. Contains a `✦` mark in `.ai-summary-mark` plus the `AI Summary` title. Each `ai_summary` paragraph renders as a `.ai-summary-p`.

---

### Risk Profile Box

```css
.risk-box {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  font-size: 0.875rem;
  color: var(--color-secondary);
  line-height: 1.7;
}
```

---

### Formula Box

Used on glossary detail pages when a concept has a formula.

```css
.formula-box {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-top: 16px;
}
.formula-label { font-size: 0.6875rem; font-weight: 500; text-transform: uppercase; color: var(--color-disabled); margin-bottom: 6px; }
.formula-value { font-family: var(--font-mono); font-size: 0.875rem; color: var(--color-green); }
```

---

### Wiki Index (glossary listing, v1.83.0)

```css
.wiki-jump        /* horizontal in-page anchor strip */
.wiki-group       /* one category, with scroll-margin-top for the fixed nav */
.wiki-group-head  /* heading + count, underlined */
.wiki-entry       /* one row: name | description | meta */
```

**The problem this fixed.** The glossary listing sorted 27 concepts by category and then rendered
them as a flat grid of 27 identical cards. **The grouping existed only in the sort order and was
invisible on screen.** Each card spent a category badge, a two-line clamped description and a "Learn
more" button to deliver a single name, and repeated the same four category labels 27 times. At three
columns, finding one term meant scanning the whole grid.

**Borrowed from the `wiki-portal` template**, which states the thesis directly: the home page of a
large reference site "is a directory, and its success is measured by how quickly a reader reaches one
of the hundreds of pages behind it", built from "many small, dense, scannable blocks rather than a
few large ones".

**Not borrowed: the 168px navigation rail.** The owner reversed that decision on 2026-09-09 in favour
of the existing top nav, before any rail code was written. `.wiki-jump` does the rail's actual job,
showing the whole structure and jumping into it, while scrolling with the page and needing no second
column. Whether a per-page contents sidebar is ever warranted is to be judged against real pages, not
decided in advance.

**Category order is fixed, not alphabetical:** Indicator, Risk Metric, Strategy Concept, Asset Class.
Sorting the categories by name would lead with Asset Class, the least likely reason anyone opens a
glossary. Concepts *within* a group stay alphabetical, because that is what a reader scans.

**An unrecognised category is appended in its own group, never dropped.** A concept added with a new
category would otherwise vanish from the page with no error anywhere.

**`.wiki-group[id]` carries `scroll-margin-top: calc(var(--nav-height) + 16px)`.** The nav is
`position: fixed`, so a jump-strip anchor would otherwise land the group heading underneath it. The
offset is derived from the nav token rather than typed, so it follows the nav.

**Rows are a single-column grid that becomes three columns at 720px**, so the same markup serves
mobile and desktop without a media query on the row itself.

---

### Guides (v1.28, disclaimer and markup rule v1.29)

`guides.html` renders `data/guides.json` through **the same `.wiki-*` markup and CSS as the glossary
listing**, with the same two views: a category-grouped index at the root and a detail view at
`?slug=`. Reusing the component was the point. Two collections that look different for no reason are
two things to maintain.

**Why it is a separate collection rather than more glossary entries.** The two have different
*maintenance contracts*, which matters more than their shared shape. A glossary entry is a reference
claim: the definition of Calmar does not expire, and it is edited only when it was wrong. A guide is
a claim about a platform that keeps changing, so it carries a visible `last_updated` that actually
means something. Mixing them would make the stable collection inherit the unstable one's review
burden. Their *fields* differ for the same reason: a glossary entry wants a `formula`, a guide wants
`takeaways` and links to the tool that measures the thing it describes.

**Schema.** `slug`, `title`, `category`, `summary`, `takeaways[]`, `related_terms[]` (glossary
slugs), `related_tools[]` (`{label, href, note?}`), `sections[{title, paragraphs[]}]`,
`last_updated`, and an optional `disclaimer`. `sections` is deliberately identical to the glossary's so one renderer serves both.

**Categories and their badge colours**, which are not arbitrary:

| Category | Badge | Hue | Why |
|---|---|---|---|
| `testing` | `.badge-testing` | blue | Informational, matching `--color-info` |
| `execution` | `.badge-execution` | yellow | Caution, matching `--color-caution` |
| `instrument-risk` | `.badge-instrument-risk` | pink | Risk, matching `--color-negative` |

**Green is deliberately not used for a guide badge.** Section 2 reserves it for positive values,
primary actions and identity, and a category label is none of those.

**`.guide-disclaimer` is optional and deliberately rare.** A guide carrying a `disclaimer`
string renders it as a yellow callout **above** the takeaways, so the reader meets it before the
content rather than in the footer after it. Only `clearing-wash-sales-before-year-end` uses it,
because it is the only page where acting on a misunderstanding produces a letter from the IRS. The
hue is yellow because Section 2 assigns yellow to caution, which is exactly what it is: pink would
read as a negative value and green is reserved. **Do not add it to guides that merely feel
important**, or it stops meaning anything.

**All guide prose goes through `mdInline()`, which supports only `**bold**` and `` `code` ``.** A
single-asterisk `*emphasis*` pair renders as literal asterisks. This is invisible in the json and
**no render assertion catches it either**, because the text is all present and merely wrong, so
`scripts/build_guides_twin.py` fails the build on it instead.

**`.guide-takeaways` asks for `list-style: disc` explicitly**, because the global reset near the top
of `css/main.css` sets `list-style: none` on every `ul`. Without it the takeaways render as indented
paragraphs and stop reading as a list. **This was only visible in a screenshot**, which is the
standing argument for judging a component from a render rather than from its markup.

**`data/guides.js` is GENERATED**, by `scripts/build_guides_twin.py`, and says so in its header. The
glossary's twin is maintained by hand and its header says *that*. Generating this one closes a
standing drift risk: a stale twin renders correct content over HTTP and silently stale content from
the file system. The same script validates that every `related_terms` slug exists in the glossary and
every `related_tools` href is a real page in the repo, so a dead cross-link fails the build instead
of rendering a link that goes nowhere.

---

### Breadcrumb

```css
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  color: var(--color-secondary);
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.breadcrumb-sep { color: var(--color-disabled); }
.breadcrumb a { color: var(--color-secondary); transition: color 0.15s; }
.breadcrumb a:hover { color: var(--color-primary); }
.breadcrumb .current { color: var(--color-primary); }
```

Rendered by `renderBreadcrumb(containerId, crumbs)` in `js/app.js`. Wrapped in `<nav aria-label="Breadcrumb">`.

---

### Footer

Rendered by `renderFooter()` in `js/app.js` into `<footer id="footer-root">`.

```css
footer {
  border-top: 1px solid var(--color-border);
  background: var(--color-bg);
  padding: 2rem;
  text-align: center;
}
.footer-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; margin-bottom: 1rem; }
.footer-links a { font-size: 0.8rem; color: var(--color-secondary); transition: color 0.15s; }
.footer-links a:hover { color: var(--color-primary); }
.footer-legal { font-size: 0.75rem; color: var(--color-secondary); line-height: 1.6; max-width: 560px; margin: 0 auto 0.5rem; }
.footer-copy { font-size: 0.75rem; color: var(--color-secondary); }
.footer-copy a { color: var(--color-blue); }
.footer-copy a:hover { color: var(--color-primary); }
```

Three stacked elements: links row, legal disclaimer, copyright + "Built by Azqato".

---

### Tabs (Database Page)

Used on `database.html` to switch between All Strategies, Leaderboard, and Screener views (`renderNav()`-adjacent inline script in `database.html`).

```css
.db-tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--color-border); margin-bottom: 24px; }
.db-tab {
  background: none; border: none; border-bottom: 2px solid transparent;
  color: var(--color-secondary); font-size: 0.9375rem; font-weight: 500;
  padding: 10px 16px; cursor: pointer; transition: color 0.15s, border-color 0.15s;
}
.db-tab:hover { color: var(--color-primary); }
.db-tab.active { color: var(--color-primary); border-bottom-color: var(--color-green); }
.db-tab-panel[hidden] { display: none; }
```

Markup: a `role="tablist"` container of `button[role="tab"]` elements, each with a `data-tab` attribute matching a sibling `.db-tab-panel[role="tabpanel"]` id. JS toggles `.active` and `aria-selected` on the clicked tab and `hidden` on the corresponding panels; no page navigation occurs on tab switch.

**Coming-soon panel:** an unbuilt tab (e.g. Leaderboard, Screener) renders the existing `.empty-state` pattern with `.empty-eyebrow` reading "Coming Soon" instead of building a placeholder from scratch.

---

### Data Table (Database Page)

Used on `database.html`'s All Strategies tab to render the full raw symphony database (thousands of rows) without the card-grid layout used elsewhere on the site.

```css
.db-table-wrap { overflow-x: auto; border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.db-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; white-space: nowrap; }
.db-table th {
  text-align: left; padding: 10px 16px; background: var(--color-surface-raised);
  color: var(--color-disabled); font-size: 0.6875rem; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.08em; border-bottom: 1px solid var(--color-border);
}
.db-table td { padding: 10px 16px; color: var(--color-primary); font-family: var(--font-mono); border-bottom: 1px solid var(--color-border); }
.db-table td:first-child { font-family: var(--font-sans); white-space: normal; max-width: 360px; }
.db-pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px; }
```

**Why a table instead of cards:** at full-database scale (~6,500 rows), the card grid used for the curated strategy library (31 entries as of 2026-08-24) does not scale; a dense table with client-side pagination (50 rows/page) keeps the DOM light while still fitting the site's existing color-coded metric conventions (Section 12/PRD.md Metric Display Guidelines apply identically here: green positive, pink negative).

**Resolved (V1.16, Performance Fix):** the table loads `data/database_summary.json` (a columnar, float-rounded derivative of the full `database.json`, ~2.3MB vs. ~11.5MB, ~540KB gzipped), not the full file. Note the site's `<500KB` target (Section 13) is scoped to the homepage specifically; it never literally bound this page, an earlier version of this note over-generalized it. See PRD.md Section 14, V1.16 for the full before/after and what actually drove the size down (columnar layout beat dropping fields alone by a wide margin).

---

### Filter Panel (database.html, V1.11)

Shared component reused by both the All Strategies tab and the Screener tab (V1.12), each gets its own independent filter state (`createFilterController()` instance), but both use the same field list and match logic.

```css
.filter-panel { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px; margin-bottom: 16px; }
.filter-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.filter-row select, .filter-row input { background: var(--color-surface-raised); border: 1px solid var(--color-border); color: var(--color-primary); border-radius: var(--radius-sm); padding: 6px 8px; font-size: 0.8125rem; }
.filter-remove { background: none; border: none; color: var(--color-pink); cursor: pointer; }
```

A "Filter" button sits directly above each tab's result-count line. Clicking it toggles a panel below the toolbar: an empty state ("No filters applied") until at least one row exists, each row a field-picker + operator dropdown + value input + delete icon, an "Add filter" button to stack more rows (AND logic between them), and Cancel/Apply. Apply closes the panel and re-filters the table in place; Cancel discards unsaved edits back to the last-applied state. Field list is restricted to real fields in `database_summary.json` (see PRD.md Section 12), never fabricated columns.

### Tier Badge (Leaderboard, database.html, V1.13)

```css
.tier-badge { display: inline-flex; align-items: center; justify-content: center; min-width: 28px; padding: 2px 8px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; border: 1px solid; }
.tier-sp { color: var(--color-green); background: rgba(0, 230, 118, 0.14); border-color: rgba(0, 230, 118, 0.35); }
.tier-s  { color: var(--color-green); background: rgba(0, 230, 118, 0.08); border-color: rgba(0, 230, 118, 0.25); }
.tier-a  { color: var(--color-blue); background: rgba(104, 175, 255, 0.08); border-color: rgba(104, 175, 255, 0.25); }
.tier-b  { color: var(--color-yellow); background: rgba(245, 197, 24, 0.08); border-color: rgba(245, 197, 24, 0.25); }
.tier-c  { color: var(--color-secondary); background: var(--color-surface-raised); border-color: var(--color-border); }
.tier-f  { color: var(--color-pink); background: rgba(255, 130, 172, 0.08); border-color: rgba(255, 130, 172, 0.25); }
```

Six tiers (S+, S, A, B, C, F), color intensity roughly tracking favorability: S+/S green, A blue, B yellow, C neutral/secondary, F pink. S+ is visually distinguished from S by a stronger background/border opacity rather than a different hue, since both represent "top tier," S+ is just the perfect-score special case.

---

### RSI Signal Colors (rsi.html, shipped V2.1)

```css
.db-table td.rsi-extreme-oversold   { color: var(--color-green); font-weight: 700; }  /* 6.63:1 */
.db-table td.rsi-oversold           { color: #52c98a; }                               /* 5.31:1 */
.db-table td.rsi-neutral            { color: var(--color-secondary); }                /* 6.44:1 */
.db-table td.rsi-overbought         { color: #f78a83; }                               /* 4.70:1 */
.db-table td.rsi-extreme-overbought { color: #ffaaa4; font-weight: 700; }             /* 6.08:1 */
```

Five tiers, thresholds >=79 / 70-78 / 42-69 / 29-41 / <=28 (see PRD.md Section 14, V2.1). Direction
is **buy = green**: oversold, where Frontrunner dip-buy branches may fire, reads green; overbought
reads red. Both extremes are bold, so the ladder does not depend on colour vision alone.

> **This entry described the ladder BACKWARDS until 2026-09-09.** It listed `rsi-extreme-oversold` as
> `#ff0000` and `rsi-extreme-overbought` as `#00ff00`, the exact inverse of the shipped code and of
> the stated buy-is-green semantic. Nothing broke, because a doc that contradicts the code produces
> no error.

**Ratios are quoted against `--color-surface-raised`, not the table's resting background.** This is
the correction that mattered: `.db-table tbody tr:hover` swaps the row to the raised surface, so a
**hovered row is the hardest case** and the only one worth measuring. Two tiers passed review against
the resting background and still failed in practice.

**Order matters as much as the threshold.** Each colour carries a rank, so a mild tier must stay
dimmer than the extreme above it. Brightening a mid tier past its own extreme to clear 4.5:1 would
satisfy the checker and destroy the ladder.

**These reds were never right.** The original `#e04545` / `#ff0000` measured 4.48 and 4.41 on the old
`#141414` surface, both under AA, so the note claiming all five tiers passed was wrong from the day
it was written rather than broken by any later change. They were re-derived twice in v1.82.0: once
for the new surface, then again once the base moved to Visual Studio range.

**Selector specificity note:** these rules must be scoped as `.db-table td.rsi-x`, not a bare `.rsi-x` class. `.db-table td` (class+type, specificity 0,1,1) otherwise wins over a bare single-class selector (0,1,0) regardless of source order, which silently prevented any of these colors from rendering until this was caught and fixed.

---

### Overfit Score (overfit.html, V2.4 Tier 1, v1.76.0)

```css
.of-score { display: flex; align-items: center; gap: 22px; flex-wrap: wrap; }
.of-score .num { font-family: var(--font-mono); font-size: 3.5rem; line-height: 1; font-weight: 600; }
.of-score .of-band { font-size: 1.125rem; font-weight: 600; margin-bottom: 4px; }
.of-score .of-par { font-size: 0.8125rem; color: var(--color-secondary); }
.of-s0, .of-s1 { color: var(--color-green); }
.of-s2 { color: var(--color-yellow); }
.of-s3, .of-s4 { color: var(--color-pink); }
.of-bar { position: relative; height: 8px; border-radius: 4px; background: var(--color-surface-raised);
          border: 1px solid var(--color-border); margin: 14px 0 6px; overflow: visible; }
.of-bar .fill { position: absolute; top: 0; bottom: 0; left: 0; border-radius: 4px; background: currentColor; }
.of-bar .par { position: absolute; top: -4px; bottom: -4px; width: 2px; background: var(--color-primary); }
.of-bar-key { display: flex; justify-content: space-between; font-size: 0.6875rem; color: var(--color-disabled); }
```

Five bands over a 0 to 100 scale, **low is good**, which is the reverse of every other graded
component on the site: 0 to 25 "Held its backtest", 25 to 50 "Mild decay", 50 to 75 "Substantial
decay", 75 to 95 "Severe decay", 95 and up "Did not survive". Because the direction is inverted, the
band label is always rendered beside the number rather than leaving the color to carry the meaning
on its own. Only three hues are used across five bands, unlike Tier Badge's six: the two green bands
and the two pink bands are separated by their labels, not by opacity, since a reader distinguishing
"severe" from "terminal" by shade is a distinction the underlying measurement cannot support.

**`.fill` uses `background: currentColor`**, so the bar inherits whichever band color is set on its
parent and the two can never disagree. Adding a band means adding one `.of-sN` rule and nothing else.

**`overflow: visible` on `.of-bar` is load-bearing, not an oversight.** The `.par` marker is
deliberately taller than the bar (`top: -4px; bottom: -4px`) so it reads as a reference line laid
across the track rather than a segment of the fill. Clipping it would make par look like part of the
score, which is the exact misreading the whole design avoids: par is context printed beside a golf
score, never a term inside it. See PRD.md V2.4, "The fitted-era split and the Overfit Score".

**Rounding is a claim at the ends of this scale.** 0 asserts a strategy kept its whole fitted rate
and 100 asserts it kept none, so `scoreText()` renders a decimal within half a point of either end.
A 99.7 printed as "100" would state the stronger claim.

---

### Stats Bar (Homepage) - REMOVED 2026-09-09 (v1.81.0)

**The component is gone and so are its four CSS rules**, which nothing else on the site used. Removed
by owner instruction. Recorded here rather than deleted because the failure it ended is worth not
repeating: the values were hardcoded and updated by hand after each database refresh, and by removal
day two of the five had drifted, with Last Refreshed reading Sep 1 against an actual refresh date of
Sep 6, and Median ARR reading +50.7% against a measured +50.6%.

**This entry was also wrong for roughly two months before that**, which is the smaller lesson. It
described five stats, "Strategies, Best Sharpe, Top ARR, Concepts, Longest Backtest", that were
replaced on 2026-07-15 by a different five. A component doc that names specific content goes stale
without anything breaking, so nothing catches it.

---

### Homepage Sections

```css
.home-section { padding: 56px 0 16px; }
.home-section-last { padding-bottom: 64px; }
.home-section[id] { scroll-margin-top: calc(var(--nav-height) + 16px); }
.home-section-title { color: var(--color-primary); font-size: 1.5rem; margin-bottom: 8px; }
.home-section-sub { color: var(--color-secondary); font-size: 1rem; max-width: 620px; margin-bottom: 32px; }
```

**Order, top to bottom: hero, How It Works, Explore.** Set 2026-09-09 by owner instruction.

**Padding is keyed to position rather than to content**, which is the point of these classes. The two
sections previously carried inline `style` attributes with a different bottom padding on each,
hardcoded because one of them happened to be last. Reordering them moved the spacing to the wrong
one. `.home-section-last` moves with the position instead.

**`scroll-margin-top` is not optional here.** The nav is `position: fixed`, so the hero's Explore
button, a plain `#explore` anchor, would otherwise scroll the section heading underneath it. The
offset is derived from `--nav-height` rather than typed as a number, so it follows the nav.

**Smooth scrolling is set on `html` and turned back off under `prefers-reduced-motion`.** A large
involuntary scroll is precisely the motion that preference exists to prevent.

---

### Hero Section (Homepage)

```css
.hero { padding: 64px 0 48px; }
.hero-eyebrow { font-family: var(--font-mono); font-size: 0.8125rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-green); margin-bottom: 12px; }
.hero-title { font-size: clamp(1.75rem, 4vw, 3rem); font-weight: 700; line-height: 1.15; color: var(--color-primary); margin-bottom: 16px; max-width: 600px; }
.hero-desc { font-size: 1.0625rem; color: var(--color-secondary); line-height: 1.7; max-width: 540px; margin-bottom: 32px; }
```

---

### Grid Layouts

`.grid-3`: strategy/glossary index cards:
- Base: `grid-template-columns: 1fr`
- 640px+: `repeat(2, 1fr)`
- 1024px+: `repeat(3, 1fr)`
- `gap: 16px`

`.grid-2`: strategy/glossary detail two-column layout:
- Base: `grid-template-columns: 1fr`, `gap: 40px`
- 1024px+: `grid-template-columns: 2fr 1fr`

`.detail-sidebar`: `display: flex; flex-direction: column; gap: 32px`

`.detail-sidebar-sticky` (1024px+); `position: sticky; top: calc(var(--nav-height) + 20px)`

---

### Prose (Glossary Content)

Long-form text sections use `.prose` wrapper.

```css
.prose h2 { font-size: 1.125rem; font-weight: 700; color: var(--color-primary); margin: 28px 0 12px; }
.prose p { font-size: 0.9375rem; color: var(--color-secondary); line-height: 1.7; margin-bottom: 14px; }
.prose strong { color: var(--color-primary); font-weight: 600; }
.prose code { font-family: var(--font-mono); font-size: 0.875em; color: var(--color-green); background: rgba(0,230,118,0.08); padding: 1px 5px; border-radius: 3px; }
.prose pre { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px; font-family: var(--font-mono); font-size: 0.8125rem; color: var(--color-primary); line-height: 1.6; }
.prose table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.prose th { padding: 8px 12px; background: var(--color-surface-raised); color: var(--color-primary); font-weight: 600; border-bottom: 1px solid var(--color-border); }
.prose td { padding: 8px 12px; color: var(--color-secondary); border-bottom: 1px solid var(--color-border); }
.prose ul { list-style: disc; padding-left: 20px; margin-bottom: 14px; }
.prose li { color: var(--color-secondary); font-size: 0.9375rem; line-height: 1.7; margin-bottom: 6px; }
```

---

### Loading State

Shown while data loads from JSON (before `loadStrategies()` / `loadGlossary()` resolve):

```css
.loading { display: flex; align-items: center; justify-content: center; min-height: 400px; }
.spinner { width: 32px; height: 32px; border: 2px solid var(--color-border); border-top-color: var(--color-green); border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
```

---

### Error State

Shown when JSON parse fails:

```css
.error-state { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; text-align: center; gap: 12px; }
.error-state h2 { color: var(--color-primary); }
.error-state p { color: var(--color-secondary); }
```

---

### Empty / 404 State

```css
.empty-state { display: flex; flex-direction: column; align-items: center; min-height: 50vh; text-align: center; gap: 16px; padding: 48px 24px; }
.empty-eyebrow { font-family: var(--font-mono); font-size: 0.875rem; font-weight: 700; color: var(--color-green); text-transform: uppercase; letter-spacing: 0.1em; }
.empty-title { font-size: 2rem; font-weight: 700; color: var(--color-primary); }
.empty-desc { max-width: 380px; }
```

The custom `404.html` uses this pattern. Both hosts serve it automatically for unmatched routes:
Cloudflare Pages (the canonical host, `composeratlas.com`) and GitHub Pages
(`azqato.github.io/composer/`). See PRD.md Section 10 for the two-host arrangement.

---

### Explore / Step Cards (Homepage)

Two small modifiers layered on the standard `.card` base, used by the homepage's "Everything on this
site" grid and its numbered how-it-works row. There is no `.explore-card` or `.step-card` class: the
card itself is a plain `.card`, and only the ornament is styled.

```css
.explore-icon { font-size: 1.5rem; margin-bottom: 12px; }   /* the emoji at the top of a card */
.step-num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--color-green); color: var(--color-bg);
  font-family: var(--font-mono); font-weight: 700; font-size: 0.8125rem;
  margin-bottom: 12px; flex-shrink: 0;
}
```

`.step-num` is the one place in the system where green is used as a **fill behind text** rather than
as the text colour, which is why it inverts to `--color-bg` for legibility.

---

### Provenance Chips (strategy detail pages, V1.20 item 8)

Pill chips above the tag row, so the age of the numbers is read before the numbers are.

```css
.prov-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
.prov-chip { display: inline-flex; align-items: center; gap: 7px; padding: 5px 11px; border: 1px solid var(--color-border); border-radius: 999px; background: var(--color-surface); font-size: 0.75rem; color: var(--color-secondary); }
.prov-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--color-green); flex-shrink: 0; }
.prov-chip.stale .prov-dot { background: var(--color-yellow); }
```

**Two chips, not one, because there are two ages.** The headline strip and the sidebar table carry
`strategies.json`'s `last_updated`; everything fed by the build-time join carries `database.json`'s
`refresh_date`. Collapsing them into a single date would be tidier and would be a claim the data
does not support: the two differ on all 31 strategies today. The page falls back to one chip only
when they genuinely agree, or when the join did not load and only one is knowable.

**The dot is the only colour, and it has exactly two states.** Green under 14 days, yellow past it.
A pill that changed size, weight or border by age would compete with the tag row directly beneath
it, which is real navigation.

---

### Hero Metric Strip (strategy detail pages, V1.20 item 2)

```css
.hero-metrics { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: var(--color-border); border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
@media (min-width: 720px) { .hero-metrics { grid-template-columns: repeat(4, 1fr); } }
.hero-metric { background: var(--color-surface); padding: 14px 16px; min-width: 0; }
```

**The 1px gap over a border-coloured background is the divider.** Four separately bordered cards
would double every internal rule and read as four things; one bordered block with hairline seams
reads as one strip, which is what it is.

**Two columns before four, and never one.** A single column would push the fourth metric a full
screen down on a phone, which is the exact failure this item exists to fix: the metrics table was
already reachable on mobile, just below three paragraphs of prose.

The value inherits `colorClass()`, so the same green and pink used everywhere else for gains and
losses apply here without a second convention. Backtest Period is neutral because it is not a
result.

---

### Deeper Metrics Grid (strategy detail pages, V1.20 item 3)

```css
.metric-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
@media (min-width: 640px) { .metric-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 1180px) { .metric-grid { grid-template-columns: repeat(4, 1fr); } }
.metric-tile { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 13px 15px; min-width: 0; }
.metric-tile-sub { font-size: 0.6875rem; color: var(--color-secondary); margin-top: 6px; line-height: 1.5; }
```

**Separate bordered tiles here, unlike the hero strip's seamed block.** Seven items do not divide
into a strip, they wrap, and a wrapped seam grid produces ragged half-rules at the end of each row.

**`.metric-tile-sub` is not optional decoration, it is the reason the grid is publishable.** These
are the seven values a visitor is least likely to know. The gloss line means the tile is legible
without leaving the page, and the glossary link means the full definition is one click away. A grid
of bare numbers labelled Kurtosis and Herfindahl Index would be jargon with a link attached.

**1180px for the fourth column, not 1024px.** The detail view is a two-column layout and the main
column is already narrowed by the sticky sidebar at 1024px, so four tiles there are too cramped to
hold a gloss line.

---

### Metric Term Links (V1.20 item 12)

```css
.metric-term { color: inherit; text-decoration: none; border-bottom: 1px dotted currentColor; }
.metric-term:hover, .metric-term:focus-visible { color: var(--color-green); border-bottom-color: var(--color-green); }
```

**Inherited colour with a dotted rule, not the site's link colour.** These labels sit inside metric
tables and tiles where a row of green underlined text would read as navigation and pull the eye off
the values, which are the content. The dotted rule is enough affordance to say "there is more here"
and little enough to stay subordinate. Hover and keyboard focus both promote to green, so the
interactive state is the same one used everywhere else.

---

### TL;DR Card (strategy detail pages, V1.20 item 13)

The first thing under the Open in Composer button. A Core Thesis callout above two opposed columns.

```css
.tldr { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 20px 22px; }
.tldr-thesis { border-left: 3px solid var(--color-green); padding-left: 14px; margin-bottom: 18px; }
.tldr-cols { display: grid; grid-template-columns: 1fr; gap: 18px; }
@media (min-width: 720px) { .tldr-cols { grid-template-columns: 1fr 1fr; gap: 28px; } }
.tldr-col.good .tldr-col-label { color: var(--color-green); }
.tldr-col.bad .tldr-col-label { color: var(--color-pink); }
.tldr-col.good .tldr-list li::before { content: '+'; color: var(--color-green); }
.tldr-col.bad .tldr-list li::before { content: '-'; color: var(--color-pink); }
```

**The two columns are the component, not a layout choice.** A single-column version would let an
author describe a strategy without naming what breaks it, which is the one thing this format exists
to prevent. They stack below 720px and stay labelled, so the opposition survives on a phone.

**Green and pink are the site's existing return colours** (`colorClass()` in `js/app.js` paints
gains green and losses pink), so the columns read as good and bad without a legend. The `+` and `-`
markers carry the same meaning for anyone who cannot separate the two hues.

---

### Underlying Assumptions (strategy detail pages, V1.20 item 14)

```css
.assump-cols { display: grid; grid-template-columns: 1fr; gap: 18px; }
@media (min-width: 860px) { .assump-cols { grid-template-columns: 1fr 1fr; gap: 24px; } }
.assump-col { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px 18px; }
```

**860px rather than the 720px used by `.tldr-cols`**, because these items are long paragraphs and
two of them side by side need more room before the columns stop helping. The two breakpoints are
deliberately different; matching them would make one of the two sections worse.

Both columns are neutral grey. Unlike the TL;DR, neither side is the good one.

---

### Market Regime Table (strategy detail pages, V1.20 item 15)

```css
.regime-wrap { overflow-x: auto; }
.regime-table { width: 100%; min-width: 560px; border-collapse: collapse; font-size: 0.8125rem; }
.regime-table td.regime-exp { white-space: nowrap; font-weight: 600; }
.regime-exp.good { color: var(--color-green); }
.regime-exp.mixed { color: var(--color-yellow); }
.regime-exp.bad { color: var(--color-pink); }
```

**Placed immediately before Risk Profile** (owner decision, v1.29.3). It shipped after Risk
Profile in v1.29.0 and reads better ahead of it: the table names the conditions a strategy meets and
how it behaves in each, which is the evidence, and Risk Profile is the conclusion drawn from that
evidence. A reader arriving at the risk summary has already seen what it is a summary of.

**`min-width: 560px` inside an `overflow-x: auto` wrapper is the point.** The example-period column
is what makes this table falsifiable rather than a set of adjectives, so it is never dropped at
narrow widths: the table scrolls inside its own container instead, per the rule the v1.12.0 mobile
audit set after `.db-tabs` widened whole pages. Verified at 390px: the wrapper scrolls internally
and the document's own width is unchanged.

**Three colours, read off the first word of authored prose.** The author writes "Strong", "Mixed to
strong" or "Poor. The worst case." and `regimeClass()` buckets it. Deliberately not a numeric score:
the roadmap's instruction for this whole tier is that these stay judgements. A colour that only ever
means one of three things is the most the design does with it.

---

### Holdings Tax Notice (strategy detail pages, V1.20 item 7)

Two states on one component, sitting **directly under Risk Profile** and above Underlying
Assumptions.

**It shipped above the AI Summary in v1.28.0 and was moved down in v1.29.1, by owner decision.** The
original argument was that a mechanical fact about holding the thing should come before any
description of why someone might want it. The placement that won reads better: the notice is a
specific risk, and it belongs in the run of risk sections rather than interrupting the summary of
what the strategy is. A reader who has just been told the strategy's risk profile is in the right
frame to be told which of its holdings sends a K-1, and one who has not reached that point yet is
being handed a tax detail before they know what they are looking at.

```css
.hold-notice { border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 14px 16px; font-size: 0.875rem; line-height: 1.7; color: var(--color-secondary); margin-bottom: 10px; }
.hold-notice.k1 { border-color: rgba(245, 197, 24, 0.4); background: rgba(245, 197, 24, 0.05); }
.hold-notice.etn { border-color: rgba(104, 175, 255, 0.4); background: rgba(104, 175, 255, 0.05); }
.hold-notice-title { display: block; font-size: 0.8125rem; font-weight: 600; margin-bottom: 6px; color: var(--color-primary); }
.hold-notice.k1 .hold-notice-title { color: var(--color-yellow); }
.hold-notice.etn .hold-notice-title { color: var(--color-blue); }
.hold-tickers { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
.hold-ticker { font-family: var(--font-mono); font-size: 0.8125rem; padding: 2px 8px; border-radius: var(--radius-sm); border: 1px solid var(--color-border-hover); color: var(--color-primary); text-decoration: none; }
```

**The two colours are quotations, not decisions.** Yellow is the `Yes` verdict on `/k1` and blue is
`.k1-etn` there. A visitor who has seen that page reads these without being taught, and a visitor who
has not is being taught the palette they will meet when they follow the ticker link.

**It is deliberately not `.risk-box`.** `risk_profile` is authored prose about how a strategy
behaves. This is a mechanical fact about a position, resolved at build time from `data/k1.json`. The
two should not look alike, or the mechanical fact reads as one more paragraph of opinion.

`.hold-ticker` is a link to `k1.html?t=TICKER`, so every ticker in the notice is a route into the
full entry rather than a name the reader has to go and look up.

---

### Statistics Live in One Place (site-wide rule, v1.37.0)

**A performance figure belongs in the metrics table and nowhere else.** Prose may compare
("meaningfully lower than Holy Grail at comparable annualised return") but may not quote
("a 3.68 Calmar").

The reason is mechanical, not stylistic. `scripts/update_metrics.py` refreshes every strategy's
metrics nightly and cannot rewrite prose, so a duplicated figure is correct only on the day it was
typed and then degrades in silence: the page still renders, still returns 200, still reads fluently,
and is wrong. When this rule was first enforced it found **89 stale figures across 29 of 31
strategies**, one of them advertising a Calmar more than double the real value on the same page that
displayed the real value in a table.

**Durations follow the same rule; start dates do not.** `backtest_days` grows nightly, so any stated
duration drifts. A start date is fixed, and it is the half a reader actually needs, because it says
which crises the record contains.

`scripts/check_stat_drift.py` enforces this.

### Unlisted Strategies (site-wide, v1.41.0)

A strategy with `hidden: true` is removed from every listing but keeps its own page.

The rule is enforced at one function, `loadStrategies()` in `js/app.js`, rather than at each grid.
Every path that lists strategies already called it, so filtering there makes the safe behaviour the
default for code that does not yet exist; the detail renderer opts out explicitly via
`loadAllStrategies()`. The alternative, filtering at each call site, is the shape that leaks the
first time someone adds a listing and forgets.

**The page survives, the advertisement does not.** Hidden entries are dropped from `sitemap.xml`,
since that file is where the site states what it wants crawled, but the detail page still resolves
for anyone holding a link. Hiding is a reversible editorial act, not a deletion, and it is used for
strategies awaiting replacement rather than for strategies being retired.

### Categorised Risk Profile (strategy detail pages, V1.20 item 10)

Replaces the single `.risk-box` blob with a verdict badge and a stack of named categories. As of
v1.36.0 **all 31 strategies carry the object shape**, so `.risk-box` no longer renders anywhere.
The renderer branch and the CSS rule are kept anyway: `risk_profile` is hand-edited and the string
form is still valid, so a future entry written as a string must render rather than vanish.

**A plain stack, not cards or a grid.** Roughly half the categories are absent on any given strategy.
A grid would put "No hedge leg" in visual parity with a paragraph describing a real one, which is the
wrong weighting; `.is-absent` dims the row instead, so a reader scanning for a real risk skips past
it.

**Absent categories are dimmed, never hidden.** Omitting the row would leave a reader unable to tell
"this strategy has no hedge" from "nobody wrote about hedging". Those are different claims and only
one of them is information.

**Categories are ordered by measured frequency across the 31 strategies, not by severity.** Ordering
by danger would be a judgement the site has no grounds to make, and it is the same rule that stops the
outlier panel becoming a score.

**The verdict is a bordered badge rather than a coloured one.** All 31 strategies open with
"Aggressive", "Extremely Aggressive" or "Conservative", and colouring that scale would turn a
self-description into a rating.

### Assets Section (strategy detail pages, V1.20 item 6, rebuilt v1.43.0)

Between the risk profile and the K-1 notices. **The reachable universe, and nothing about today's
position.** The keys of `last_market_days_holdings` are the universe and its values are the last
market day's allocation; this section renders the keys and discards the values.

A count line, a wrapped row of ticker chips, one paragraph. That is the whole component.

**It did not always be this.** Through v1.41.x it led with "1 of 6 tickers held as of the last
market day", an allocation bar per holding, a percentage beside each one, and a separate "can also
hold, but is not holding today" list. Every number in it was accurate.

**It was removed because accuracy was not the problem.** What a strategy CAN hold is a durable fact
about its logic. What it holds today is one rebalance old, and putting it at the top of the section
invites a reader to read a position as a recommendation, which is the one thing this site does not
do. The chips say what the logic is allowed to own; the reader is never handed a portfolio.

**Chips reuse `.hold-ticker`, the same component as the K-1 and ETN notices.** A reader meets one
kind of ticker list on this page rather than two.

**Nothing renders per-chip.** Two things were tried on the row and both removed in review:

| Tried | Why it went |
| --- | --- |
| Per-ticker K-1 and ETN badges | The notices directly below already name every affected ticker **and** explain what the treatment costs. A three-letter badge restated the fact without its explanation, and its variable width was what stopped the rest of the row from aligning. |
| Per-ticker first-traded dates | They existed to bound the backtest, and the Backtest window card above does that properly by naming the binding holding and its date. They survive as the chip's `title`. |

**The count line keeps its tax summary** ("3 tickers this strategy can hold, of which 2 are ETNs").
It is the one place a reader learns the shape of the list before reading it, so it is a summary
rather than a repeat.

**`.asset-row`, `.asset-bar`, `.asset-pct`, `.asset-since`, `.asset-flags`, `.asset-badge`,
`.asset-ticker` and `.asset-idle` were deleted in v1.43.0** after a grep confirmed no remaining
consumer. `.asset-head` and its two children are all that survive.

### Strategy Page Section Order (site-wide, v1.43.0)

**Approved by the owner on 2026-09-02 after review of the `gold-miner-original` pilot, and rolled
out to all 36 strategy pages in the same version.** This is the canonical shape. A new strategy
page is correct when it matches this order, and a change to the order is a change to every page.

| # | Section | Note |
| --- | --- | --- |
| 1 | Hero metric strip | V1.20 item 2 |
| 2 | Open in Composer button | |
| 3 | **AI Summary** | **Moved above the TL;DR in v1.42.0.** It was already below the button; the TL;DR card sat between them |
| 4 | TL;DR card | V1.20 item 13 |
| 5 | Underlying Assumptions | V1.20 item 14 |
| 6 | Market Regime table | V1.20 item 15, moved above Risk Profile in v1.29.3 |
| 7 | Risk Profile | V1.20 item 10 |
| 8 | **Assets** | The reachable universe as chips. No allocation, no snapshot |
| 9 | K-1 and ETN notices | Moved below Risk Profile in v1.29.1 |
| 10 | Beyond the Backtest | Reliance on its best days, Out of sample, Backtest window |
| 11 | Deeper Metrics | V1.20 item 3 |
| 12 | Provenance chips | V1.20 item 8 |

**Two rules the v1.42.x review produced, both of which generalise beyond the sections that taught
them:**

1. **Today's position is not content.** Anything one rebalance old that could be read as a
   recommendation does not lead a section. What the logic CAN do is durable; what it did this
   morning is not. This is why the Assets section lost its allocation bars.
2. **A figure gets a card or it gets nothing.** A bare line under a grid of cards reads as a card
   that failed to load. The below-SPY case of the best-days figure was demoted to a line for one
   review round and reversed on sight: if a measurement is worth stating, it is worth the same
   container as every other measurement on the page. This is the same reasoning as the item 10 rule
   that an absent risk category states itself explicitly rather than vanishing.

### Metric Tokens in Prose (site-wide, v1.45.0)

**A performance figure quoted in a sentence is written as a token and resolved at render time.**
`{sharpe_ratio}`, not a typed `2.89`. `resolveStrategyTokens` in `js/app.js` walks a deep copy of
the strategy object once, in `strategies.html`, before anything renders, so no template below has to
know tokens exist and a renderer added later cannot forget to call it.

**Why.** `update_metrics.py` refreshes metrics nightly and cannot rewrite prose, so a hand-typed
figure was correct only on the day it was written. At the time of the conversion 37 figures across
12 pages were already wrong on the live site. `check_stat_drift.py` catches a stale quote after the
fact; a token cannot go stale in the first place.

**The rule.** If a number in prose is a value the database holds for that strategy, it is a token.
If it is a historical measurement over a fixed window, or a figure belonging to a different
strategy in a comparative sentence, it stays a literal, because there is nothing on this strategy to
resolve it from. As of v1.45.0 that split is 162 tokens against 141 literals.

**Precision is optional and the prose picks it.** `{max_drawdown_abs}` is `78.3%`,
`{max_drawdown_abs:0}` is `78%`. The library's voice rounds, so most citations use `:0`. The default
is the fuller figure, so omitting the suffix never quietly loses information, and each token sets
its own default because two decimals is right for a Sharpe and absurd for a cumulative return.

**`max_drawdown` has two spellings on purpose.** It is stored negated on all 36 strategies.
`{max_drawdown}` keeps the sign for "its -45.2% drawdown"; `{max_drawdown_abs}` gives the magnitude
for "a 45.2% max drawdown". One number, two sentences.

**Formatting deliberately differs from the metrics table.** `formatPct` prefixes `+`, which is right
in a column of figures and wrong mid-sentence. The values are identical; only presentation differs.

**An unresolvable token renders as itself** rather than vanishing, because a blank where a number
should be is invisible in review and `{sharp_ratio}` on the page is not. The real defence is
`scripts/check_prose_tokens.py`, which fails before a reader sees one, and which parses the token
list out of `js/app.js` rather than restating it.

### Unlisted Page Banner (v1.45.0)

Directly under the `<h1>` and above the description on the 12 hidden strategy pages, because a
reader who is going to act on the page needs it before they read anything else on it.

It states three things: the page is unlisted, the writing is not maintained, and **the metrics are
still refreshed on the normal schedule**. The third is the one that matters. Without it a reader has
no way to know which half of the page to trust, and the honest answer is that the numbers are
current and the words around them are not.

Bordered and tinted rather than a plain paragraph, since it is a statement about the page rather
than part of the page's content. Muted greys rather than a warning colour, because nothing here is
wrong: the strategy is real, the metrics are live, and the page is simply not being written to any
more.

### Reality Check Cards (strategy detail pages, V1.20 items 4, 5 and 9)

The Beyond the Backtest section, after the risk profile. Two columns above 720px, stacked below it.
**Three cards as of v1.33.0**, so on a wide screen the third wraps to a second row on its own. That
is deliberate: a third column would drop each card under 300px and `.rc-value` at 1.75rem is sized
for the number to be the argument, not to be squeezed. The grid is left at two columns rather than
made to fit.

```css
.rc-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 720px) { .rc-grid { grid-template-columns: 1fr 1fr; } }
.rc-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px; }
.rc-label { display: block; font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-disabled); margin-bottom: 8px; }
.rc-value { font-family: var(--font-mono); font-size: 1.75rem; line-height: 1.1; font-weight: 600; color: var(--color-primary); display: block; }
.rc-value.warn { color: var(--color-yellow); }
.rc-sub { display: block; font-size: 0.75rem; font-family: var(--font-mono); color: var(--color-disabled); margin-top: 6px; }
.rc-body { font-size: 0.8125rem; color: var(--color-secondary); line-height: 1.7; margin-top: 12px; }
```

**`.rc-value` is 1.75rem because the number is the argument.** The paragraph below it is the
footnote, not the other way round. This is the same reasoning as the oversized verdict on `/k1`,
one size down because there are two of these on a page rather than one.

**A number in `.rc-value` must be interpretable without leaving the card. Added v1.43.0, and it
cost a rewrite to learn.** The first card in this section printed
`top_five_percent_day_contribution` raw and coloured it yellow above 100%, warning that "the other
95% of days lost money on net: remove those days and this strategy is a net loser". Arithmetically
true. Materially false as an impression, because the denominator is NET return, a small residual
under a much larger gross: plain buy-and-hold SPY scores **202%** on the same measure and TLT
**729%**. The threshold flagged 28 of 36 strategies, nearly all of which are less reliant on their
best days than the index is.

The card now prints the strategy against SPY over the same window, so **46%** reads as "a little
under half as reliant as the index" rather than as a bare figure the reader cannot place. Both raw
figures and the window length stay on the card in `.rc-fine`, so the ratio never has to be taken on
trust.

**`.rc-value.warn` was deleted in v1.43.0.** Nothing uses it, and that is on purpose. The
strategies clustered near parity sit inside the gap between Composer's formula and ours, so a hard
colour change at exactly 100% would assert a precision the data does not have. The prose
distinguishes above from below; a colour would have made it a verdict.

**A card with no comparison available states that, rather than falling back.** Three strategies
backtest further back than `data/prices.json` reaches, so there is no honest same-window baseline.
They print the raw figure with its own limitation attached ("on its own that number says less than
it looks like it does") instead of reverting to the pre-v1.43.0 card. A page with no benchmark is
exactly where a reader is least equipped to discount a threshold.

```css
.rc-fine { font-size: 0.75rem; font-family: var(--font-mono); color: var(--color-disabled); line-height: 1.6; margin-top: 12px; }
```

**The backtest-window card (v1.33.0) carries no `.warn` and no colour at all.** It states a length,
the earliest date the window could have started, and the holding that sets that date. Both of its
copy branches describe something normal: a window the data forced, or a start date somebody chose.
Neither is a failure, and colouring the second one would have turned a disclosure into an accusation.

**Its copy switches on measured headroom, not on a rule of thumb.** Under a year of headroom it says
the window is about as long as it could be and names the limiting holding; over a year it says the
data allowed a longer test than was run. The split is 18 to 13 across the 31 featured strategies.
The card is **suppressed entirely** when any holding lacks an inception date, because one undated
holding could be the true floor and a floor computed from a subset is silently too early.

**`.rc-value.warn` is the only conditional colour**, applied when outlier dependence exceeds 100%,
which is true for 25 of the 31 featured strategies. Yellow rather than pink: it is a fact the reader
should weigh, not a failure. The roadmap item is explicit that this must not become a score or a
badge, and a colour that only ever means "over 100%" is the most the design does with it.

---

### Tag Filter Bar (strategies.html, V1.17)

The filter panel above the strategy index. Reuses the `.tag` pills from the cards below it rather
than inventing a second chip style, so a filter chip and the tag it filters on are visibly the same
object.

```css
.tagfilter { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 16px 18px; margin-bottom: 32px; }
.tagfilter-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.tagfilter-title { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--color-disabled); }
.tagfilter-group { display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px; padding: 6px 0; }
.tagfilter-group + .tagfilter-group { border-top: 1px solid var(--color-border); }
.tagfilter-label { flex: 0 0 88px; font-size: 0.75rem; color: var(--color-disabled); }
.tagfilter-tags { display: flex; flex-wrap: wrap; gap: 6px; min-width: 0; }
.tagfilter-tag { opacity: 0.62; font: inherit; font-size: 0.75rem; font-weight: 500; }
.tagfilter-tag:hover { opacity: 0.85; }
.tagfilter-tag.active { opacity: 1; box-shadow: 0 0 0 1px currentColor inset; }
.tagfilter-count { margin-left: 5px; opacity: 0.7; font-size: 0.6875rem; }
```

**Selection is expressed by opacity plus an inset ring, not by a different colour.** An inactive chip
sits at `opacity: 0.62` and an active one at `1` with a `currentColor` inset ring, so each chip keeps
its own semantic tag colour in both states. This is deliberate: recolouring a chip on selection would
break the Section 2 rule that a tag's colour identifies its concept.

**Accessibility caveat, recorded rather than fixed:** opacity plus a one-pixel ring is a weak
distinction on its own, and the ring is the part carrying the state for anyone who cannot separate
the two opacity levels. Worth revisiting if the bar grows.

Below `640px` the label takes a full row (see Breakpoints above) so the chips are not squeezed into
the remaining 88px-offset column.

---

### Database Toolbar (database.html)

The header row above each database table: heading, live result-count pill, name search, and the
Filter button.

```css
.db-export {                 /* Screener CSV buttons, v1.32.2 */
  display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
}
.db-toolbar { display: flex; gap: 8px 16px; }
.db-toolbar h2 { display: inline; color: var(--color-primary); font-size: 1.125rem; }
.db-count-pill {
  display: inline-flex; padding: 2px 10px; border-radius: 999px;
  background: var(--color-surface-raised); border: 1px solid var(--color-border);
  color: var(--color-secondary); font-size: 0.75rem;
}
.db-search-input {
  background: var(--color-surface-raised); border: 1px solid var(--color-border);
  color: var(--color-primary); border-radius: var(--radius-sm);
  padding: 6px 10px; font-size: 0.8125rem; width: 200px; max-width: 100%;
}
```

`border-radius: 999px` is the pill idiom used here and by `.updated-badge` below. It is the only
radius in the system not drawn from the `--radius-*` tokens, because a pill is "fully round" rather
than a size choice.

---

### Last-Updated Badge (database.html, rsi.html)

A green-dot pill stating when the underlying data last refreshed. Replaced the old "this section is a
work in progress" line in v1.13.5.

```css
.updated-badge {
  display: inline-flex; gap: 8px; padding: 6px 14px; border-radius: 999px;
  background: var(--color-surface-raised); border: 1px solid var(--color-border);
  color: var(--color-green); font-size: 0.8125rem;
}
.updated-badge-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-green); }
```

The dot is decorative and duplicated by the adjacent text, so it needs no accessible name.

---

### Screener Bucketed Filter Grid (database.html, V1.12 redesign)

The Screener's always-visible filter grid, one labelled dropdown per numeric field, which replaced
the hidden click-to-open Filter Panel on that tab only.

```css
.screener-filter-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 10px 12px; background: var(--color-surface);
  border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px;
}
.screener-filter-cell { display: flex; flex-direction: column; gap: 4px; }
.screener-filter-cell label { color: var(--color-secondary); font-size: 0.6875rem; }
.screener-filter-cell select,
.screener-filter-cell input {
  background: var(--color-surface-raised); border: 1px solid var(--color-border);
  color: var(--color-primary); border-radius: var(--radius-sm);
  padding: 6px 8px; font-size: 0.8125rem; width: 100%;
}
```

`auto-fill` with a `160px` minimum is what makes this responsive without a breakpoint: the grid sheds
columns on its own as the viewport narrows.

---

### Modal (database.html, V1.13)

One shared overlay serves both the per-row score breakdown and the Methodology explainer. There is a
single `#modal-overlay` in the page, driven by `openModal()` / `closeModal()`.

```css
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0, 0, 0, 0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 24px;
}
.modal-overlay[hidden] { display: none; }
.modal-panel {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); max-width: 880px; width: 100%;
  display: flex; flex-direction: column;
}
.modal-header { display: flex; padding: 16px 20px; border-bottom: 1px solid var(--color-border); }
.modal-header h2 { font-size: 1.0625rem; color: var(--color-primary); }
.modal-close { background: none; border: none; color: var(--color-secondary); font-size: 1.5rem; padding: 4px 8px; }
.modal-close:hover { color: var(--color-primary); }
```

`z-index: 1000` sits deliberately above the fixed nav's `z-index: 100`, so an open modal covers the
nav rather than letting it float over the panel. Closable by the X, by clicking the overlay, and by
Escape.

**Accessibility, closed v1.32.3.** The panel traps focus, and the background is made `inert`
while it is open.

**Half of the gap this paragraph used to describe never existed.** It said the panel "does not set
`role="dialog"` / `aria-modal="true"`". It always did. What was missing was everything that makes
those attributes true, which is the worse failure of the two: `aria-modal="true"` is a promise to
assistive technology that the rest of the page is unreachable, and the page behind was fully
reachable, so the markup was asserting something false rather than merely omitting something.

The contract now:

- `aria-labelledby="modal-title"` on the panel, so the dialog is announced with its own heading.
- On open, the previously focused element is remembered and focus moves to the **close button**,
  not the panel. It is the one control every modal here has, and landing on it tells a screen
  reader user how to get out before anything else is read to them.
- Tab and Shift+Tab wrap within the panel. Focus that is somehow outside the panel is pulled back
  to the first control rather than left loose.
- `#nav-root`, `.page` and `#footer-root` are set `inert` while the modal is open. **A focus trap
  alone is not enough**: it stops Tab, but a screen reader user can still browse past the modal
  into the table behind it. `inert` removes the background from the accessibility tree as well as
  the tab order.
- On close, focus returns to whatever opened the modal. Without that, the next Tab restarts at the
  top of the document, which on this page means walking the whole nav again to get back to the row
  you were reading.

**One implementation trap, since it cost a round of testing.** The focusable-element selector must
be scoped **per selector**, not once for the whole list. `'#modal-overlay ' + 'button, [href], ...'`
scopes only `button` and leaves every other clause global. The first version did exactly that and
collected **47 elements, 44 of them symphony links in the table behind the modal**; the forward
wrap then tried to focus a nav link that `inert` had just made unfocusable, and silently did
nothing. Scoped correctly it collects 3.

---

## 8. Undocumented Surfaces

Five tool pages carry their own inline `<style>` block on top of `css/main.css`. They are listed
here rather than left silently absent, because a design system that quietly omits a third of the
site's interface is worse than one that admits the boundary.

| Page | Inline CSS | Prefix | What it styles |
|---|---|---|---|
| `signal-miner.html` | ~135 lines | `.sl-*` | The whole Signal Miner interface: ticker chip rows and groups, the family checkbox grid, the parameter fields, the run status and progress line, the results table and its wrapper, the buy-and-hold baseline strip, and the combine bar. Two column classes carry a meaning worth naming: `th.nosort` and `td.plat` are the parameter-plateau columns (v1.73.0), and they take `cursor: help` rather than the pointer and hover colour every other header has, because they are the only columns that cannot be sorted and a cursor that promises a sort is a lie the reader finds out by clicking |
| `converter.html` | ~48 lines | `.conv-*`, `.t-*` | Panels and actions, plus the `.t-*` syntax highlighter for the rendered logic tree (`.t-fn`, `.t-cond`, `.t-asset`, `.t-wt`, `.t-kw`, `.t-muted`). The `.j-*` raw-JSON highlighter it used to carry moved to `css/main.css` at v1.31.2 |
| `etf-cloner.html` | ~65 lines | `.ec-*` | Panels, the file drop zone, the live/full mode toggle, and the holdings table wrapper. The `.j-*` JSON highlighter it shared with `converter.html` moved to `css/main.css` at v1.31.2 |
| `nodes.html` | ~36 lines | `.nd-*` | Panels and actions, the oversized node total, the breakdown table (including the muted `tr.excluded` rows for what is deliberately not counted), and the quoted node definition. No syntax highlighter: this page prints one number and a table, not JSON (v1.26.0) |
| `k1.html` | ~62 lines | `.k1-*` | The lookup form and its hint line, the result panel, the oversized Yes/No verdict and its subtitle, the fact rows beneath it (`.k1-label` + value pairs), the caveat note, and the collapsible fund table: `.k1-filters` and `.k1-filter` for the All/K-1/No K-1 pills and the Expand toggle (`.on` marks the active pill, `.k1-toggle` pushes the toggle to the right edge), and `td.yes`/`td.no` for the verdict column. `.k1-wrap` caps at `60vh` and scrolls, since the table is 184 rows expanded, and `th` is `position: sticky` so the sortable headers stay reachable while scrolling. `button.k1-sort` makes each header a real button for keyboard use, styled to look like the header text it replaced; its `.arrow` is shown only when the button carries `aria-sort`, so the visible indicator and the announced state cannot drift apart. `.k1-warn` is the one loud element on the page: a pink-bordered tinted block, used only when etfdb's `Distributes K1` flag contradicts its own `Structure` field. It is deliberately not styled like `.k1-note`, because a reader who mistakes a contested answer for a settled one files their taxes wrong, and grey caveat text is read as boilerplate. `.k1-export` carries the `margin-left: auto` that pushes the right-hand button group over, with `.k1-toggle` sitting beside it. `.k1-etn` is the second callout and is deliberately the quieter of the two: a blue-bordered tinted block on the same geometry as `.k1-warn`, shown when a fund's `structure` is `ETN`. The colour split carries the meaning. Pink says the answer above may be wrong; blue says the answer is right and a different risk sits beside it, namely that an ETN is unsecured bank debt rather than a basket of assets. Giving both the same weight would train a reader to skim both. `.k1-tag` is the matching inline badge on the ticker cell, blue outline and mono, so the same fact is visible while scanning the table rather than only after a lookup. No syntax highlighter: this page prints a verdict and a table, not JSON (v1.27.0, table reworked v1.27.2, warning and export v1.27.7, ETN callout v1.27.9) |

`rsi.html`, `database.html`, `index.html`, `about.html`, `strategies.html`, `glossary.html` and
`404.html` carry **no** inline style at all; everything they render is in `css/main.css` and
documented above. `strategies.html` stayed in that list through V1.20: `.hold-notice`, `.rc-*`,
`.tldr-*`, `.assump-*`, `.regime-*`, `.prov-*`, `.hero-metric*`, `.metric-grid`, `.metric-tile*` and
`.metric-term` all went into `css/main.css` beside the components they sit among, rather than into a
`<style>` block on the page, because the strategy detail view is a core page and not a
self-contained tool.

**RESOLVED v1.31.2. The `.j-*` JSON highlighter was duplicated** between `converter.html` and
`etf-cloner.html`, and now lives in `css/main.css`. The paragraph below records the position that
held until then. Both
copies define the same five classes. Nothing has gone wrong with that yet, but it is exactly the kind
of pair that drifts, and it is the strongest candidate for promotion into `css/main.css` if a third
page ever needs to print JSON.

**Why these were never folded into the shared stylesheet.** Each tool is a single self-contained page
whose styles are used nowhere else, so keeping them inline means one file to open when working on
that tool, and no dead rules loaded by every other page on the site. That trade is defensible and is
not being reversed here. What was not defensible was leaving it undocumented.

**Documenting them properly is open work**, listed in PRD.md Section 25. Anyone changing a tool's
appearance should keep to the tokens in Section 2 and the type scale in Section 3, which all three
pages already do.

---

## 9. Accessibility Standards

**Target: WCAG 2.1 Level AA**

### Focus Management

**A real focus ring is now defined, v1.30.** It used to be a target in this document and a browser
default in practice:

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
```

The audit measured the inherited default at an apparent 1.08:1 and that reading was **wrong**:
`outline-style: auto` means the browser paints its own adaptive ring, so the computed colour says
nothing about what lands on screen. A screenshot of a focused link showed Edge painting a clearly
visible white ring. It was never a failure. **It was unspecified, which is a different problem**:
an appearance nobody chose is not the same as one that is correct, and it varies by browser. The
ring above is measured at 4.83 on the hardest dark surface and 4.66 on the hardest light one.

### Control boundaries (v1.30)

**The one unambiguous WCAG failure the colour audit found.** `--color-border` is 1.66:1 on surface
and is decorative by design. A text entry field has no fill distinct from the panel behind it, so
that border was the only thing marking where the field was, which is WCAG 1.4.11 at 3:1.

`--color-border-strong` exists so controls can clear 3:1 without brightening every divider on the
site. **It had to be applied in each tool page's own inline `<style>`**, not in `css/main.css`: the
page-level block comes after the external stylesheet in the document and wins, so appending a rule
to `main.css` could never have fixed it. That is why the first attempt measured as no change at all.

**Checkboxes, radios and file inputs are deliberately excluded.** They are native controls the
browser draws itself, and forcing a border on them changes something already legible.

Tab order follows visual reading order. Mobile nav hamburger: `aria-expanded` attribute updates on open/close; `aria-controls="mobile-menu"`.

### Semantic HTML

- One `<h1>` per page
- Proper heading hierarchy (no skipping levels)
- Strategy cards use `<article>` elements
- Nav uses `<nav id="nav-root">` (with `aria-label="Mobile navigation"` on the mobile menu)
- Breadcrumb uses `<nav aria-label="Breadcrumb">` with `.current` class on current item
- Metrics table uses `<dl>` with `<dt>` / `<dd>` pairs (not `<table>`)
- Footer links use `<nav class="footer-links">`

### Screen Reader Support

- External links rendered with descriptive context (link text includes destination)
- Metric color coding is never the sole means of conveying meaning: values include sign (`+` / `-`)
- Strategy card metric labels are visible text above each value

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
```

---

## 10. Animation and Motion

Keep motion minimal and purposeful. No page transitions at MVP.

### Transition Table (from css/main.css)

| Element | Property | Duration | Easing |
|---|---|---|---|
| Cards (hover) | `border-color` | `0.15s` | `ease` (default) |
| Nav links | `color`, `background` | `0.15s` | `ease` |
| Nav logo | `color` | `0.15s` | `ease` |
| Nav hamburger background | `background` | `0.15s` | `ease` |
| Hamburger bars (open/close) | `transform`, `opacity` | `0.2s` | `ease` |
| Mobile nav links | `color`, `background` | `0.15s` | `ease` |
| Buttons | `opacity`, `background`, `color`, `border-color` | `0.15s` | `ease` |
| Tags (hover) | `opacity` | `0.15s` | `ease` |
| Compact strategy list items | `background` | `0.15s` | `ease` |
| Breadcrumb links | `color` | `0.15s` | `ease` |
| Footer links | `color` | `0.15s` | `ease` |
| About content links | `opacity` | `0.15s` | `ease` |
| Loading spinner | `transform` (rotate) | `0.6s` | `linear` (infinite) |

### Rules

- All transitions use `ease` timing unless continuity demands `linear` (spinner)
- Duration ceiling: `0.2s` for most interactions; spinner at `0.6s` is a persistent animation, not a transition
- `prefers-reduced-motion` sets all transition and animation durations to `0.01ms` (effectively instant)
- No decorative animations; no entrance animations; no scroll-triggered effects at MVP


---

## 11. Brand Identity

**Opened 2026-09-28.** The "how" of the logo system. The "why" lives in `docs/PRD.md` under its own
`## Brand Identity` heading: the brand brief, the audience, the competitive analysis and the cliche
list are there and are not repeated here.

**This section documents work that mostly does not ship, and says which part now does.** Nothing in
`brand/` is served by either host. **The token layer has been adopted:** `css/main.css` carries
`--color-brand` and `--font-brand`, and Section 2's green rule has been amended to name identity as a
third role. **The mark has not:** `favicon.svg` is still the map emoji and the nav mark is still the
emoji. Adopting the mark is a separate decision and a separate change.

### The Design Vocabulary

Four words carry every shape in every concept. They are real cartographic terms, chosen because the
obvious vocabulary for "atlas" is the pin, the globe, the compass rose and the folded map, and all
four are ruled out in the PRD's cliche table.

| Term | What it is | Why it is here |
|---|---|---|
| **Neatline** | The border that frames a map plate | Every real map has one and almost no logo does. Drawn as a true square, because a plate's frame stays rectangular however the projection inside it curves |
| **Parallel** | A line of latitude. Straight, horizontal | The horizontal is the calm axis. It is also the one line that can carry the green without reading as a rising trend |
| **Meridian** | A line of longitude | In any pseudocylindrical projection these bow away from the central meridian. **This is the single detail that makes a grid read as a map rather than as a spreadsheet**, and it is the load-bearing decision in concepts C and D |
| **Index cell** | One cell of the graticule, filled | An atlas index finds a place by its cell reference. The product's whole job is to put a reader in the right cell and describe the ground under it |

**Construction constants**, shared by every symbol. The symbol viewBox is 64 x 64. The neatline is
inset 9 units on every side, giving a 46-unit span, so the mark never touches its own edge and has
built-in clear space at small sizes. The bow is 4.8 units for a three-column graticule and 7.4 for a
single meridian.

**Why the cell fills are solved rather than drawn.** Each meridian is a quadratic Bezier whose control
point sits at mid-height, which makes its y component exactly linear, so the parameter at any height
is `t = (y - 9) / 46` in closed form. A filled cell takes its curved sides from the **exact sub-curve**
of the meridian it sits against, via `quad_split` in `brand/build/lib_type.py`. A shape guessed by eye
would leave a visible seam where the meridian stroke crosses the fill, and that seam would only appear
at large sizes, which is the worst place to find it.

### Typography

| | |
|---|---|
| **Face** | **Archivo**, by Omnibus-Type |
| **Licence** | **SIL Open Font License 1.1.** Free to use, modify, embed and redistribute, including commercially. The one real restriction is that the font itself may not be sold on its own, which does not apply to a logo |
| **Weight** | SemiBold, all caps |
| **Tracking** | +26 font units, uniform. All-caps settings need positive tracking to breathe, and a reference brand wants the result calm rather than tight |
| **Kerning** | **Hand-kerned, not read from GPOS.** `LA -28, AT -18, TL -22, SE -6, ER -6, OM -8`. A wordmark is kerned by eye, and the pairs that matter in a thirteen-character string are few |
| **Outlines** | The TTF is **not committed**. The build downloads it to a scratch directory and bakes the outlines into the SVG as paths, so no output depends on the font being installed afterwards |

**Why Archivo and not Inter.** The site already runs Inter, and setting the wordmark in Inter would
make the logo indistinguishable from a heading. Archivo is a grotesque in the same family of shapes,
so it sits beside Inter without conflict, but it has a squarer, more industrial cast that reads as
plate lettering rather than as UI text. **All caps is deliberate:** mixed case brings a descender on
the `p` and pushes the `t` and `l` above cap height, and neither irregularity earns its place.

### Concepts

Four directions, all built as **dark-ink and light-ink pairs** rather than one file using
`currentColor`. This is not a preference. **An SVG referenced by an `<img>` resolves `currentColor`
against its own root element, never against the page around it**, so a single file cannot be proved on
both a light and a dark ground. The pairs are also exactly the monochrome-black and reversed-white
deliverables Phase 4 asks for, so nothing is wasted.

Files are in `brand/concepts/`. Every one was judged from a rendered screenshot in `brand/checks/`,
never from its markup.

#### A. Neatline

*Luxury minimalism. The minimum viable map.*

A square neatline and one green parallel at 63% of the span, below centre so the mark is not static.
Stroke 2.6. Nothing else.

- **Intent:** the least a map can be and still be a map. Frame plus one measured line.
- **Palette:** ink plus `#00e676` on the parallel. One accent, one focal point.
- **Type:** pairs with the wordmark; has no lettering of its own.
- **Render verdict:** clean and confident at 512 and 32, on both grounds and in grayscale. **It fails
  at 16px.** The green parallel drops to a sub-pixel line and disappears, leaving an empty rectangle
  that could belong to anything. Concept A is a large-format mark that cannot be a favicon.

#### B. Wordmark

*Typography first. No symbol at all.*

COMPOSER ATLAS in Archivo SemiBold caps, with the word space replaced by a **green graticule tick** at
full cap height, 70 units wide.

- **Intent:** compete with Morningstar and Portfolio Visualizer on credibility rather than on imagery.
  Two of the eight brands analysed are trusted precisely because they look almost unbranded.
- **Palette:** ink plus one green tick. The tick does a space's job and carries the measuring device.
- **Type:** the whole concept. See the table above.
- **Render verdict:** reads correctly at every size, though at 16px it is legible only as a texture.
  The tick is now centred on the **ink bounds** of the R and the A rather than on their advance
  widths: R ends on a diagonal leg and A opens on one, so the optical gap and the metric gap are
  different intervals, and a tick placed by advance sits visibly against the A.

#### C. Index Cell

*Symbol plus meaning. The full graticule.*

A square neatline, three columns by three rows. The two interior **meridians bow**; the two parallels
stay straight. The centre cell is filled green. Stroke 2.0.

- **Intent:** the located cell. The bow is what makes it a projection instead of a table.
- **Palette:** ink on the structure, `#00e676` on one cell only. The green is the index, and the index
  is the point.
- **Type:** pairs with the wordmark.
- **Render verdict:** **the strongest mark at large sizes.** The bow genuinely reads as a projection,
  the filled cell is an unmistakable focal point, and both survive grayscale and reversal. **It fills
  in at 16px**, where the 2.0 stroke and the eight interior gaps merge into a grey smudge and the green
  cell stops being distinguishable.

#### D. Evolved

*The same idea reduced to what survives at nav size.*

The graticule at two by two, one meridian and one parallel, stroke 3.6, bow 7.4. The top-right cell is
filled green.

- **Intent:** not a rival to C. It is C at the size the existing emoji occupies, which is 1.25rem in
  the nav and 16px in a browser tab.
- **Palette:** identical to C.
- **Type:** pairs with the wordmark.
- **Render verdict:** **the only mark that holds at 16px.** The quadrant structure stays open, the
  green cell stays legible, and the bow is still visible at 512 rather than flattening into a window
  pane. The bow was raised from 4.8 to 7.4 for exactly this reason: a single meridian can carry more
  curve than one of three can, because nothing beside it has to stay parallel to it, and at 4.8 the
  mark read as a four-pane window rather than as a map quadrant.

### What the Render Check Changed

The rule is that every logo is judged from a rendered image and never from its markup. Five things
were wrong in the code and invisible there. They are listed because the list is the argument for the
rule.

| Found in the render | What was actually happening | Fix |
|---|---|---|
| **The mark was invisible on dark grounds, and the test was passing** | `color="#16191f"` was baked on the SVG root with `currentColor` ink. An `<img>`-referenced SVG resolves `currentColor` against its own root, so the dark panel was showing a dark mark on a dark ground and reporting success | Emit dark-ink and light-ink **pairs**, and pair each to its ground in the contact sheet |
| **The wordmark read "CoMPOSER" with a slashed O** | A second custom detail put a rule through each O's counter. At every size it rendered as a Scandinavian O-slash | **Removed entirely, not softened.** A detail that changes which letters a reader sees is not a detail, and a thinner rule fails the same way more quietly |
| **Strokes rendered as a chunky picture frame** | A 4.0-unit stroke on a 46-unit span is heavy at 512 in a way it is not in code | A 4.0 to 2.6, C 3.5 to 2.0, D 4.5 to 3.6 |
| **D read as a window pane** | The bow at 4.8 is legible on three meridians and invisible on one | D's bow raised to 7.4 |
| **The green tick sat against the A** | Placed by advance width rather than by ink bounds | Centred on `bounds()` of the two adjacent glyphs |

### Phase 3 Quality Gate

Each concept was checked against the three tests before being presented. **Pass means the check was
applied and the concept survived it**, not that the concept is beyond criticism.

| Test | A | B | C | D |
|---|---|---|---|---|
| **One focal point** | Pass. The green parallel | Pass. The green tick | Pass. The filled centre cell | Pass. The filled quadrant |
| **Every effect has a job** | Pass. No gradient, glow, texture or shadow exists in any concept | Pass | Pass | Pass |
| **Could not be pasted onto an unrelated brand** | **Weakest.** A framed rectangle with a line is close to generic; it depends on the wordmark to mean anything | Pass. The name is the mark | Pass. A bowed graticule with one located cell is specific to this brief | Pass, less strongly than C: at two by two there is less projection to read |

**What was removed, and why removal rather than restyling.** Two things. The barred O in concept B,
covered above. And a **decorative corner registration tick** that appeared in the first draft of the
neatline: it looked like a technical drawing and it had no job, since it carried no meaning, created
no hierarchy and added nothing to recognition. The gate's instruction is to remove rather than
restyle, and the reason is visible in the B case: a softened version of a detail that fails still
fails, just less legibly.

### Chosen Direction

**Picked at the Phase 3 gate: C and D as one system, locked up with B.**

The render check is what made the decision rather than taste. C, the 3x3 index cell, is the most
meaningful mark and provably dies at 16px. D, the same graticule reduced to 2x2 with a heavier stroke,
is the only version that survives there. They are built from identical vocabulary, so a reader who
meets both never registers the substitution. A, the neatline, was the same reduction taken one step
too far and is not part of the system.

| Role | Mark | Used |
|---|---|---|
| **Primary** | C, the 3x3 index cell | 33px and above |
| **Compact** | D, the 2x2 quadrant | 32px and below, and for all merchandise |
| **Wordmark** | B, Archivo SemiBold caps with a green graticule tick | Beside either, or alone |

---

### Logo System

Every file is in `brand/logo/`. **36 files, all render-checked.** Nothing here is linked from the
site: `favicon.svg` in the repository root is still the emoji, and adoption is a separate decision.

#### Colour treatments

Four, applied to every vector deliverable.

| Suffix | Ink | Accent | For |
|---|---|---|---|
| `-color` | `#16191f` | `#00e676` | Light grounds |
| `-color-reversed` | `#e9edf2` | `#00e676` | Dark grounds, including the site itself |
| `-black` | `#16191f` | `#16191f` | Single colour, light ground |
| `-white` | `#e9edf2` | `#e9edf2` | Single colour, dark ground |

**Why the single-colour versions collapse the accent into the ink rather than dropping the filled
cell.** A fax, an embroidery head or a one-plate print will flatten the green whatever the file says.
The mark survives that flattening because the index cell is a **fill against open cells**, not one hue
against another, so the located cell still reads when there is only one colour left.

#### The files

| Group | Files | Notes |
|---|---|---|
| **Symbols** | `symbol-primary-*.svg`, `symbol-compact-*.svg` | 64 x 64. Four treatments each |
| **Wordmark** | `wordmark-*.svg` | 576.03 x 40 |
| **Horizontal lockup** | `lockup-horizontal-*.svg` | 575.63 x 64. Primary symbol |
| **Compact horizontal lockup** | `lockup-horizontal-compact-*.svg` | Same layout, compact symbol, for use below 288px |
| **Stacked lockup** | `lockup-stacked-*.svg` | 288.02 x 160.75 |
| **Merchandise** | `merch-single-colour.svg` | D in pure black, for embroidery, engraving and one-plate print |
| **Favicon, vector** | `favicon.svg` | Answers both colour schemes from one file |
| **Favicon, raster** | `favicon-16.png`, `favicon-32.png`, `favicon-48.png`, `favicon.ico` | Opaque, reversed mark on the dark base |
| **App icons** | `icon-180.png`, `icon-192.png`, `icon-512.png`, `icon-1024.png` | Opaque. 1024 is the App Store submission size |
| **Maskable** | `maskable-192.png`, `maskable-512.png` | Ink inside the central 80% |

#### Clear space and minimum size

**Clear space is one graticule cell**, which is the 46-unit span divided by three, so 15.33 units of
the symbol's own 64-unit canvas. Stated in the mark's vocabulary rather than as an arbitrary ratio, so
it scales correctly and can be checked by eye: leave the width of one cell of the primary symbol clear
on every side. Nothing else sits inside that box.

**The symbol files already carry a 9-unit inset** on all four sides of their 64-unit canvas, which is
built-in breathing room but is **not** the clear-space rule and does not substitute for it.

| Asset | Minimum | What sets the floor |
|---|---|---|
| **Compact symbol** | **16px** | The lowest size anything in this system survives. Verified from a 16px render, not extrapolated |
| **Primary symbol** | **32px** | Below this the eight interior gaps merge and the located cell stops being distinguishable |
| **Wordmark alone** | **120px wide** | Cap height falls below 8px, at which Archivo's counters close |
| **Horizontal lockup** | **288px wide** | **Set by the symbol, not the type.** The primary symbol occupies the lockup's full height, so C's 32px floor becomes the lockup's 288px floor. Below 288px use the compact horizontal lockup, which holds to 144px |
| **Stacked lockup** | **120px wide** | Cap height again |

**The 288px figure is the single most useful number in this section**, because it is the one that is
surprising. A lockup that looks fine on a screen at 200px is being rendered with a symbol at 22px,
which is below the primary mark's floor, and the failure is a slightly muddy square rather than an
obviously broken one. That is why the compact lockup exists.

#### Merchandise

`merch-single-colour.svg` is the **compact** mark, and the choice is arithmetic rather than
preference. Reproduced 25mm wide, one unit of the 46-unit span is 0.543mm.

| | Stroke | Narrowest gap | Verdict at 25mm |
|---|---|---|---|
| **Primary (C)** | 2.0 units = **1.09mm** | 13.3 units = 7.2mm | Survives print. Does not survive embroidery |
| **Compact (D)** | 3.6 units = **1.96mm** | 21.0 units = 11.4mm | Clears the 1mm floor on every line and every gap |

#### Favicon and icon decisions

**`favicon.svg` is the only file in the system that answers both colour schemes from one file**, using
`@media (prefers-color-scheme: dark)` on a CSS variable inside the SVG. That mechanism works here and
nowhere else in this system: a favicon is requested as a document in its own right, whereas an SVG
pulled in through an `<img>` resolves its own `currentColor` against itself and cannot see the page.

**The PNG and ICO favicons are opaque, and that is a correction rather than a default.** The first
build shipped them transparent with the dark ink, and the render check showed them on a dark tab strip
as a lone green square: the strokes were present and were the same colour as the ground. A transparent
PNG bakes exactly one ink, and no browser tells you what colour the tab strip is about to be, so
transparency cannot answer both. The raster favicons therefore bring their own ground.

**App icons are opaque for the same reason plus one more:** the operating system composites a
transparent icon onto a surface nobody controls, and the reversed mark on a white springboard is the
failure case.

**Ink coverage, measured from the rendered pixels rather than from the padding constants.**

| Asset | Ink spans | Requirement |
|---|---|---|
| `icon-180` / `icon-192` | 78% | None. 75 to 80% is the platform convention |
| `icon-512` / `icon-1024` | 75% | None |
| `maskable-192` | 68% | **Inside 80%.** Pass |
| `maskable-512` | 65% | **Inside 80%.** Pass |

The padding was tuned twice. The first pass put maskable ink at 47%, which satisfied the safe zone and
looked like a small logo lost on a large tile. The second removed the pad from the standard icons
entirely, because the mark's own 9-unit inset already stops its ink at 72% of the plate, and a pad on
top of that was double-counting breathing room that was already there.

#### What the render check changed in Phase 4

| Found in the render | Fix |
|---|---|
| **Raster favicons were invisible on a dark tab strip.** Dark ink on transparency | Opaque plate, reversed mark |
| **Maskable icons looked shrunken.** Ink at 47% of the canvas | Pad 0.20 to 0.07, ink to 65% |
| **Standard app icons were double-padded.** The mark's own inset plus an added pad | Pad to 0 |
| **The stacked lockup read as a wordmark wearing a hat.** Symbol at its native 64 units against a 576-unit wordmark | Symbol scaled to 62% of the wordmark's width |
| **The stacked lockup's two halves drifted apart.** The gap was measured from the symbol's canvas edge, which silently added 14% of the scaled symbol on top of the intended gap | Space from the ink, not the canvas |
| **The contact sheet was testing the wrong file on dark grounds again.** It paired `-dark`/`-light`, and the shipped system is named `-color`/`-color-reversed` | Taught the sheet all three naming pairs |

---

### Color Contrast

**Computed, not asserted.** Every figure below comes from `brand/build/build_kit.py`, which
linearises each sRGB channel before weighting it, because sRGB is not linear and averaging the raw
bytes produces a number that looks plausible and is wrong. Regenerate rather than hand-edit.

Ratios are stated against all three grounds a token can legally sit on. AA needs 4.5:1 for body text
and 3:1 for large text; AAA needs 7:1.

| Token | Value | on bg `#16191f` | on surface `#2c3038` | on raised `#373c46` |
|---|---|---|---|---|
| `--color-primary` | `#e9edf2` | 14.97:1 AAA | 11.25:1 AAA | 9.41:1 AAA |
| `--color-secondary` | `#d2d8df` | 12.26:1 AAA | 9.22:1 AAA | 7.71:1 AAA |
| `--color-disabled` | `#b8bec6` | 9.40:1 AAA | 7.07:1 AAA | 5.91:1 AA |
| `--color-green` | `#00e676` | 10.55:1 AAA | 7.93:1 AAA | 6.63:1 AA |
| `--color-pink` | `#ff82ac` | 7.58:1 AAA | 5.70:1 AA | 4.77:1 AA |
| `--color-blue` | `#68afff` | 7.68:1 AAA | 5.77:1 AA | 4.83:1 AA |
| `--color-yellow` | `#f5c518` | 10.80:1 AAA | 8.12:1 AAA | 6.79:1 AA |
| `--color-purple` | `#b39dff` | 7.70:1 AAA | 5.79:1 AA | 4.84:1 AA |

**Nothing in the palette fails.** The lowest ratio anywhere is **pink on `#373c46` at 4.77:1**, which clears
AA for body text with a small margin and is the constraint the v1.82.0 rebuild was solved against.

**What this table does not cover.** It measures the palette, not the brand assets. The one asset that
inverts the scheme is the email signature, which sets `#16191f` ink on white at 17.68:1, and the one
that carries green on white is the same file's rule, which is a graphic element rather than text and
so has no text-contrast requirement. The green is never used for body text on a light ground in any
deliverable, and it must not be: `#00e676` on white is 1.71:1.

---

### Brand Kit

Everything is in `brand/kit/`. **Nothing here is linked from the site**, including
`site.webmanifest`, which is written so that adopting it later is a one-line change in each page
head rather than a file that has to be authored under time pressure.

| File | Size | Purpose and the constraint that shaped it |
|---|---|---|
| `og-image.png` | 1200x630 | The link preview in Slack, iMessage, Discord and every social card. Copy is the site's **existing** `og:title` and meta description, not a new tagline |
| `profile-400.png` | 400x400 | Avatar. **Every platform crops this to a circle**, so the mark sits inside the inscribed circle with room to spare and nothing lives in the corners. Uses the compact mark, because an avatar is rendered at 32px in a comment thread far more often than at 400 |
| `x-header-1500x500.png` | 1500x500 | The avatar overlaps the lower left and the visible band narrows sharply on a phone, so everything that must survive is held in the middle third |
| `linkedin-banner-1584x396.png` | 1584x396 | LinkedIn puts the company logo over the lower left on desktop and not on mobile, so the lockup is left-anchored but held clear of that corner |
| `email-signature@2x.png` | 720x180 | 360x90 at 2x for a retina mail client. **The one asset in the kit set on white**, because a signature is composited into a reply chain whose background belongs to the recipient |
| `tokens.css` | | Portable copy of the `:root` block, for a deck, a prototype or a partner document |
| `tokens.json` | | The same tokens as data, with the notes carried through |
| `site.webmanifest` | | Name, colours and the four icon entries including both maskables. **Created, deliberately not linked** |

**The tokens files are generated from `css/main.css`, and they say so in their own header.** This is
the open question 20 rule again: the failure mode this project keeps hitting is two copies of the same
fact drifting apart, and a brand kit that ships a remembered palette is exactly how that happens. Both
files carry a line saying the CSS is the source of truth and that they are to be regenerated rather
than edited.

**Copy discipline.** The social images say what the site already says. `og:title` in `index.html` is
"Judge a Composer strategy before you run it" and that is the headline on the card; the supporting
line is the existing meta description. No new claim about the product was introduced anywhere in this
commission.

---

### Rationale

The argument in one page, as it is made in `brand/presentation.html`.

**The problem was not that the logo was weak. There was no logo.** The identity was a `🗺️` emoji in a
`<text>` element, which means the mark was whichever drawing the visitor's operating system shipped,
and on a phone, where the wordmark is hidden below 480px, the entire brand was a system emoji.

**The category converges hard, and the thing it converges on is a performance claim.** Across eight
analysed brands the shared devices are the upward-right diagonal in some form, blue as the primary,
and increasingly a rounded geometric sans. A site whose first tenet is transparency over hype cannot
open with a picture of going up. That single observation removed most of the obvious solutions before
any drawing started.

**The obvious drawings for "atlas" were removed next.** The globe, the pin, the compass rose and the
folded paper map are the first four things anyone sketches, and the fourth is the emoji this work
replaces. Replacing an emoji with a careful drawing of the same emoji is not an identity.

**What was left was real cartography rather than the idea of maps.** The neatline, the parallel, the
meridian and the index cell are terms a cartographer uses and a logo almost never does. They gave the
brief something it badly needed: a vocabulary that is specific, ownable and true to the product, in a
space where every adjacent option was either a competitor's habit or a stock icon.

**The bow is the whole argument.** A grid of straight lines is a spreadsheet, and a spreadsheet is
precisely the wrong metaphor for a product whose case is that numbers need context. Curving the
interior meridians the way a pseudocylindrical projection does turns the same grid into a map. It is
the only element in the mark carrying that meaning, which is why it is the one thing that may never be
straightened.

**The green was inherited, not chosen, and that constrains it.** On the site green means a positive
value or a primary action and is never decorative. A logo is neither, so the mark uses green as a
third role, identity, recorded as an addition to the rule rather than an exception to it. **Section 2
now carries that amended wording and `css/main.css` carries the token that enforces it**, `--color-brand`,
which exists so that no rule can confuse the two meanings: `--color-positive` says a number went up,
`--color-brand` says this is us. They resolve to the same hue today and are not obliged to forever. The price of
that is a standing prohibition: the mark never pairs green with an arrow, a rising line or anything
else that reads as a value, because a logo that borrowed the product's "up" colour while sitting in
the corner of every page would be making a performance claim on every page.

**Restraint here is an argument about honesty, not a style preference.** Two of the eight brands
analysed are trusted precisely because they look like instruments rather than products, and one earns
institutional authority through pure restraint. The decorated end of the category, the gradients and
the glow, belongs to businesses selling a feeling about money. This site sells an accurate picture,
and the identity says so by having no gradient, no glow, no shadow and no texture anywhere in it.

**The system is two marks because the render check said so.** The primary mark is the most meaningful
and dies at 16px. The compact mark is the same idea reduced until it survives there. Neither fact was
visible in the drawing; both came out of a screenshot.

---

### Usage Guidelines

#### Do

- **Use the compact mark at 32px and below**, and for anything stitched, engraved or printed in one
  plate. It is not a fallback, it is the mark at that size.
- **Leave one graticule cell of clear space** on every side of the lockup. Nothing enters that box.
- **Reverse to the light ink** on any ground darker than `--color-surface`.
- **Use the supplied single-colour files** when a process cannot hold the green. Do not make your own
  by recolouring the full-colour file: the single-colour versions pull the filled cell back off the
  strokes, and a naive recolour merges the two.
- **Keep green for the index cell and the word tick** and for nothing else in the mark.

#### Do not

- **Do not set the primary mark below 32px.** Below that its eight interior gaps merge and the located
  cell stops being distinguishable. The failure looks like a slightly muddy square rather than an
  obviously broken logo, which is what makes it easy to ship.
- **Do not straighten the meridians.** Without the bow the mark is a table.
- **Do not recolour the cell** or introduce a second accent.
- **Do not add a gradient, glow, drop shadow, outline or texture.** The system contains none by design,
  and each one fails the test that every effect must have a job.
- **Do not rebuild a lockup by hand** or respace the wordmark. The wordmark is hand-kerned and the
  lockups are spaced from the mark's ink rather than its canvas; both are easy to get subtly wrong.
- **Do not place the mark beside an arrow, a rising line or a chart that trends up.** See the green
  constraint in the rationale above.
- **Do not use the emoji.** It is still what the live site ships, and it is what this system replaces.

#### Ownership of the source

Every deliverable is generated by a script in `brand/build/`, and **the scripts are the source, not
the SVGs**. Editing a file in `brand/logo/` produces something that the next build overwrites. Change
the generator and rebuild.

| Script | Produces |
|---|---|
| `build_concepts.py` | The four Phase 3 concepts, and the symbol geometry every later phase imports |
| `build_logo.py` | The 37 files in `brand/logo/` |
| `build_kit.py` | The 8 files in `brand/kit/`, and the computed contrast table |
| `build_presentation.py` | `brand/presentation.html` and `brand/brand-guidelines.pdf` |
| `contact_sheet.py` | The render checks in `brand/checks/` |

---

### Presentation

`brand/presentation.html` is the full argument, and `brand/brand-guidelines.pdf` is the same document
printed to **15 pages of A4 landscape**. Both are built by `build_presentation.py`.

**It is genuinely one file.** Every logo is inlined as SVG markup rather than linked, so the page has
no `<img>` tags at all. The only external request it makes is Archivo from Google Fonts, and even that
is not load-bearing: the wordmark's outlines are baked into its paths, so the page is correct offline.

**Nothing in it is a photograph.** The brief allows photographs from `brand/mockups/`, that directory
is empty because this brand has never been photographed, so the phone home screen, the browser tab,
the two business cards and the embroidered patch are all drawn in CSS and SVG, with layered shadows,
lighting gradients, a thread texture on the patch and perspective tilts on everything.

**The print stylesheet removes the tilts.** A perspective transform is a screen device that signals
depth; on paper it only costs legibility, so `@media print` resets every transform to `none` and lets
the page breaks fall between sections.

**One fault in this phase was found only in a mockup.** The embroidered patch is where the
single-colour mark was first seen at size on a real surface, and it showed the filled cell merging
into the strokes it touches, because in one colour there is no hue left to separate them. That is the
reason the mono treatments now inset the fill. It would not have appeared on a contact sheet, because
a contact sheet shows the mark on an empty ground where the merge still looks deliberate.

---

### Status

**Phases 1 to 6 are complete.** The gate that stood here was the Phase 3 stop, where four concepts
were presented and the owner chose C and D as one system locked up with the B wordmark. That choice is
recorded above under Chosen Direction, and everything after it follows from it.

**The tokens are adopted; the mark is not.** `css/main.css` carries `--color-brand` and
`--font-brand`, and **no colour value changed to add them**, because `brand/kit/tokens.css` was
generated from the site's own `:root` block and the palettes were therefore already identical. What
the tokens added was a meaning the stylesheet could not previously express.

`favicon.svg` in the repository root is still the emoji and the nav mark is still the emoji, so the
mark itself remains unadopted. That is a separate decision and a separate change, and the files that
would make it a small one already exist: `brand/logo/favicon.svg`, the icon PNGs and
`brand/kit/site.webmanifest`. **It is not merely a file copy**: all three live under `brand/`, which
is excluded from both hosts by `.assetsignore` and by an rsync `--exclude` in `deploy.yml`, so
adopting the mark means moving files out of that exclusion and re-checking both.

**What is still open.**

| Item | State |
|---|---|
| Adoption in the site | **The owner's decision.** Not started, deliberately |
| `brand/mockups/` | Empty. Every mockup in the presentation is drawn, and a photograph would replace one |
| Phase 7 showcase page | See the PRD's Brand Identity section for where it lives and why it is not published |
