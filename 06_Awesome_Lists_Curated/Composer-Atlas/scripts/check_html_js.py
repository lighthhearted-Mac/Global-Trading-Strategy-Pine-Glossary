#!/usr/bin/env python3
"""Syntax sanity check for the inline <script> blocks in the site's HTML.

Why this exists: v1.22.2 took the Signal Miner down in production. An
apostrophe inside a single-quoted string, 'Ignore BIL's Sortino...', closed
the string early. The stray quotes happened to re-pair, so brackets still
balanced, and the file looked fine. The whole 1,300-line inline script died
with a syntax error. The page still served HTTP 200 and still rendered its
static HTML, so nothing downstream noticed: every control was simply dead.

There is no JS runtime in this project's toolchain, so `node --check` is not
available. This is a small tokenizer that catches the two failure modes that
have actually bitten:

  1. A ' or " string that runs past end of line. Only ` may span lines.
  2. Unbalanced brackets.

It understands line comments, block comments, template literals with nested
${...}, and regex literals, which matters because several pages contain
regexes carrying unbalanced brackets and quotes inside them (converter.html
and etf-cloner.html both hold a JSON-highlighting regex that trips a naive
scanner).

Usage:
    python scripts/check_html_js.py                 # every *.html in the repo root
    python scripts/check_html_js.py a.html b.html   # named files
    python scripts/check_html_js.py --self-test     # prove the checker still works

Exit code is non-zero if any file fails, so it can gate a deploy.
"""
import re
import sys
from pathlib import Path

BS = chr(92)   # backslash, kept out of literals so a mangled heredoc cannot eat it
SQ = chr(39)   # '
DQ = chr(34)   # "
BT = chr(96)   # `

# After one of these words a '/' opens a regex, not a division. Without this,
# `return /re/.test(x)` reads as division because the preceding token is a word.
KEYWORDS = {
    'return', 'typeof', 'instanceof', 'in', 'of', 'new', 'delete', 'void',
    'throw', 'case', 'do', 'else', 'yield', 'await',
}
WORD = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$')

# A <script> we should parse as JavaScript: no src=, and either no type at all
# or a JavaScript type. Skips things like application/ld+json.
SCRIPT_RE = re.compile(r'<script([^>]*)>(.*?)</script>', re.S | re.I)
TYPE_RE = re.compile(r'type\s*=\s*["\']([^"\']*)["\']', re.I)
JS_TYPES = {'', 'module', 'text/javascript', 'application/javascript'}


def scan(js):
    """Return a list of (line, message). Line numbers are relative to js."""
    errors = []
    stack = []
    pairs = {'}': '{', ']': '[', ')': '('}
    # 'value' means the previous token can be divided (identifier, number,
    # closing bracket, string, regex). 'op' means a '/' here opens a regex.
    last = 'op'
    i, n, line = 0, len(js), 1

    while i < n:
        c = js[i]

        if c == '\n':
            line += 1
            i += 1
            continue
        if c in ' \t\r':
            i += 1
            continue

        # line comment
        if c == '/' and i + 1 < n and js[i + 1] == '/':
            while i < n and js[i] != '\n':
                i += 1
            continue

        # block comment
        if c == '/' and i + 1 < n and js[i + 1] == '*':
            i += 2
            while i + 1 < n and not (js[i] == '*' and js[i + 1] == '/'):
                if js[i] == '\n':
                    line += 1
                i += 1
            i += 2
            continue

        # regex literal
        if c == '/' and last == 'op':
            start_line = line
            i += 1
            in_class = False
            closed = False
            while i < n:
                ch = js[i]
                if ch == BS:
                    i += 2
                    continue
                if ch == '\n':
                    break            # a regex literal cannot span lines
                if in_class:
                    if ch == ']':
                        in_class = False
                elif ch == '[':
                    in_class = True
                elif ch == '/':
                    closed = True
                    break
                i += 1
            if not closed:
                errors.append((start_line, 'unterminated regex literal'))
                return errors
            i += 1
            while i < n and js[i] in 'dgimsuvy':   # flags
                i += 1
            last = 'value'
            continue

        # string or template literal
        if c in (DQ, SQ, BT):
            quote, start_line = c, line
            i += 1
            closed = False
            while i < n:
                ch = js[i]
                if ch == BS:
                    i += 2
                    continue
                if ch == '\n':
                    line += 1
                    if quote != BT:
                        break        # unterminated: ' and " cannot span lines
                    i += 1
                    continue
                if ch == quote:
                    closed = True
                    break
                if quote == BT and ch == '$' and i + 1 < n and js[i + 1] == '{':
                    depth = 1
                    i += 2
                    while i < n and depth:
                        if js[i] == '{':
                            depth += 1
                        elif js[i] == '}':
                            depth -= 1
                        elif js[i] == '\n':
                            line += 1
                        i += 1
                    continue
                i += 1
            if not closed:
                kind = 'apostrophe' if quote == SQ else 'quote'
                errors.append((start_line, 'unterminated ' + quote + ' string '
                               '(likely a stray ' + kind + ' inside it)'))
                if len(errors) > 4:
                    return errors
            i += 1
            last = 'value'
            continue

        # identifier or number
        if c in WORD:
            j = i
            while j < n and js[j] in WORD:
                j += 1
            last = 'op' if js[i:j] in KEYWORDS else 'value'
            i = j
            continue

        if c in '{[(':
            stack.append((c, line))
            last = 'op'
            i += 1
            continue

        if c in '}])':
            if not stack or stack[-1][0] != pairs[c]:
                errors.append((line, "unexpected '" + c + "'"))
                return errors
            stack.pop()
            last = 'value'
            i += 1
            continue

        last = 'op'
        i += 1

    if stack and not errors:
        errors.append((stack[-1][1], 'bracket opened here is never closed'))
    return errors


def check_file(path, verbose=True):
    src = open(path, encoding='utf-8').read()
    ok = True
    blocks = 0

    for m in SCRIPT_RE.finditer(src):
        attrs, js = m.group(1), m.group(2)
        if re.search(r'\bsrc\s*=', attrs, re.I):
            continue
        t = TYPE_RE.search(attrs)
        if t and t.group(1).strip().lower() not in JS_TYPES:
            continue
        blocks += 1
        # Report file-relative lines, so the output is clickable.
        base = src.count('\n', 0, m.start(2))
        for line, msg in scan(js):
            ok = False
            print('  ' + path + ':' + str(base + line) + '  ' + msg)

    for tag in ('div', 'table', 'tbody', 'thead'):
        o = len(re.findall(r'<' + tag + r'[\s>]', src, re.I))
        c = len(re.findall(r'</' + tag + r'>', src, re.I))
        if o != c:
            ok = False
            print('  ' + path + '  <' + tag + '> ' + str(o) + ' open / '
                  + str(c) + ' close, mismatch')

    if verbose:
        print(('  ok   ' if ok else '  FAIL ') + path
              + '  (' + str(blocks) + ' inline script block(s))')
    return ok


# Cases the checker must get right. The first is the real v1.22.2 outage.
#
# Known limitation, deliberately encoded below as a passing case: an intruding
# quote whose stray quotes all re-pair before end of line is invisible here.
# 's = "he said "hi" to me";' is a genuine JS syntax error that this tool
# reports as clean, because every string it sees opens and closes on one line.
# What makes the outage detectable is that its re-pairing left a string running
# off the end of the line. A stricter check would need a real JS parser.
SELF_TEST = [
    (False, "s = 'Ignore BIL's Sortino and Calmar: cash has no drawdown.';"),
    (True,  's = "he said "hi" to me";'),   # see the limitation note above
    (False, 'function f() { return 1;'),
    (False, 'const a = [1, 2, 3));'),
    (True,  "s = 'plain string'; t = " + DQ + 'another' + DQ + ';'),
    (True,  's = ' + BT + 'multi\nline ${a + b} template' + BT + ';'),
    (True,  "s = 'it" + BS + "'s escaped';"),
    (True,  'x = json.replace(/("(' + BS + BS + 'u[a-f0-9]{4}|[^"])*")/g, f);'),
    (True,  "x = s.replace(/" + DQ + "/g, '&quot;').replace(/'/g, '&#39;');"),
    (True,  'if (a) { return /ab[/]c/.test(s); } // regex after return'),
    (True,  'const r = total / count; const q = (a + b) / 2;'),
    (True,  '// a comment with an unmatched ' + SQ + " and a { brace\nx = 1;"),
    (True,  '/* block ' + SQ + ' comment { */ x = 1;'),
]


def self_test():
    bad = 0
    for expect_ok, snippet in SELF_TEST:
        got_ok = not scan(snippet)
        if got_ok != expect_ok:
            bad += 1
            print('  FAIL  expected ' + ('ok' if expect_ok else 'an error')
                  + ' for: ' + snippet.replace('\n', BS + 'n')[:70])
    print('self-test: ' + str(len(SELF_TEST) - bad) + '/' + str(len(SELF_TEST))
          + ' cases correct')
    return bad == 0


def main(argv):
    if '--self-test' in argv:
        return 0 if self_test() else 1

    paths = [a for a in argv if not a.startswith('-')]
    if not paths:
        root = Path(__file__).resolve().parent.parent
        paths = sorted(str(q) for q in root.glob('*.html'))

    print('checking ' + str(len(paths)) + ' file(s)')
    ok = True
    for p in paths:
        ok &= check_file(p)
    if not self_test():
        ok = False
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
