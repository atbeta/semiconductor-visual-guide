#!/usr/bin/env python3
"""把原书（zh-CN）里的名词框、Know-how 框、常见异常表、延伸阅读、晶圆位置
抽取成 HTML，补进可视化页面。

用法：
    python3 scripts/enrich_from_source.py --dry chapters/04-lithography.html
    python3 scripts/enrich_from_source.py            # 全部 25 章
    python3 scripts/enrich_from_source.py --strip     # 移除已注入的内容
"""
import argparse
import glob
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'zh-CN')
SITE_JS = os.path.join(ROOT, 'assets', 'site.js')

WSTART = '<!-- wp:start -->'
WEND = '<!-- wp:end -->'
START = '<!-- enriched:start -->'
END = '<!-- enriched:end -->'


def chapter_map():
    """从 site.js 拿到 章号 -> 页面文件名"""
    s = open(SITE_JS, encoding='utf-8').read()
    m = {}
    for n, f in re.findall(r"\{ n: '(\d+)', t: '[^']*', f: '([^']+)' \}", s):
        m[n.lstrip('0') or '0'] = f
    return m


def find_source(num):
    """章节目录一律是「两位数字-名字」，分部目录是「一位数字-名字」，要排掉。"""
    for p in glob.glob(os.path.join(SRC, '**', 'README.md'), recursive=True):
        d = os.path.basename(os.path.dirname(p))
        m = re.match(r'^(\d{2})-', d)
        if m and str(int(m.group(1))) == str(int(num)):
            return p
    return None


def ch_num_from_link(url):
    mm = re.search(r'/(\d{2})-', url)
    return str(int(mm.group(1))) if mm else None


def inline(text, cmap, current=''):
    text = html.escape(text, quote=False)

    def link(m):
        label, url = m.group(1), m.group(2)
        n = ch_num_from_link(url)
        if n and n in cmap and cmap[n] != current:
            return f'<a href="{cmap[n]}">{label}</a>'
        return label
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def parse_boxes(md, cmap, current):
    """返回 [(kind, title, [(label, text), ...]), ...]"""
    boxes = []
    blocks = re.split(r'\n\s*\n', md)
    for b in blocks:
        lines = [l[2:] if l.startswith('> ') else l[1:] if l == '>' else l
                 for l in b.split('\n') if l.startswith('>')]
        if not lines:
            continue
        head = lines[0].strip()
        if head not in ('[!NOTE]', '[!TIP]'):
            continue
        kind = 'note' if head == '[!NOTE]' else 'tip'
        title = ''
        fields = []
        for l in lines[1:]:
            l = l.strip()
            if not l:
                continue
            m = re.match(r'\*\*(.+?)\*\*$', l)
            if m and not title:
                title = m.group(1)
                continue
            m = re.match(r'-\s+\*\*(.+?)\*\*[：:]\s*(.*)$', l)
            if m:
                fields.append((m.group(1), inline(m.group(2), cmap, current)))
            elif fields:
                fields[-1] = (fields[-1][0], fields[-1][1] + inline(l, cmap, current))
        if title:
            title = re.sub(r'^[📖🔧]\s*', '', title)
            title = re.sub(r'^(名词|Know-how)\s*[｜|]\s*', '', title)
            boxes.append((kind, title, fields))
    return boxes


def parse_waferpos(md, cmap, current):
    m = re.search(r'>\s*📍\s*\*\*晶圆位置\*\*\n((?:>.*\n)+)', md)
    if not m:
        return None
    lines = [l[2:].strip() for l in m.group(1).split('\n') if l.strip().startswith('>')]
    out = []
    for l in lines:
        l = re.sub(r'^-\s*', '', l)
        if not l:
            continue
        l = re.sub(r'^[^：:]*[：:]\s*', '', l)
        l = l.replace('**', '')
        out.append(inline(l, cmap, current))
    return out if len(out) >= 2 else None


def parse_table(md, keyword):
    m = re.search(r'##\s*' + keyword + r'\s*\n+((?:\|.*\n)+)', md)
    if not m:
        return None
    rows = [r.strip() for r in m.group(1).strip().split('\n')]
    rows = [r for r in rows if not re.match(r'^\|[\s\-:|]+\|$', r)]
    cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
    if len(cells) < 2:
        return None
    return cells


def parse_reading(md):
    m = re.search(r'##\s*延伸阅读\s*\n+((?:[-*].*\n?)+)', md)
    if not m:
        return []
    items = [re.sub(r'^[-*]\s*', '', l).strip() for l in m.group(1).split('\n') if l.strip()]
    return items


def build_html(src_path, page_name, cmap):
    md = open(src_path, encoding='utf-8').read()
    cn = os.path.basename(src_path)
    num = os.path.basename(os.path.dirname(src_path)).split('-')[0]
    current = str(int(num))

    wp = parse_waferpos(md, cmap, current)
    boxes = parse_boxes(md, cmap, current)
    exc = parse_table(md, '常见异常')
    reading = parse_reading(md)

    wp_html = ''
    if wp:
        labels = ['前一站', '本章', '下一站']
        items = []
        for i, t in enumerate(wp[:3]):
            lab = labels[i] if i < 3 else ''
            items.append(f'<span><b>{lab}</b> {t}</span>')
        wp_html = WSTART + '<div class="waferpos">📍 ' + '<span class="arw">→</span>'.join(items) + '</div>' + WEND

    parts = [START]

    if boxes:
        cards = []
        for kind, title, fields in boxes:
            rows = ''.join(
                f'<dt>{html.escape(k)}</dt><dd{"" if k not in ("常见混淆", "没做会怎样") else " class=\"q\""}>{v}</dd>'
                for k, v in fields)
            cls = 'note-c' if kind == 'note' else 'tip-c'
            tag = '名词' if kind == 'note' else 'Know-how'
            cards.append(
                f'<div class="cc {cls}"><h4><span class="badge-s">{tag}</span>'
                f'<span>{html.escape(title)}</span></h4><dl>{rows}</dl></div>')
        parts.append('<section><h2 class="sec-head"><span class="num">＋</span>原文里的名词与现场经验</h2>'
                     '<p class="sub">以下内容逐条取自原书，保留「定义 / 现场用法 / 常见混淆」与「情境 / 做法 / 为什么」的原始结构。</p>'
                     '<div class="cards">' + ''.join(cards) + '</div></section>')

    if exc:
        head, body = exc[0], exc[1:]
        th = ''.join(f'<th>{html.escape(c)}</th>' for c in head)
        trs = ''.join('<tr>' + ''.join(f'<td>{inline(c, cmap, current)}</td>' for c in r) + '</tr>' for r in body)
        parts.append('<section><h2 class="sec-head"><span class="num">＋</span>常见异常</h2>'
                     f'<div style="overflow-x:auto"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div></section>')

    if reading:
        lis = ''.join(f'<li>{inline(x, cmap, current)}</li>' for x in reading)
        parts.append('<section><h2 class="sec-head"><span class="num">＋</span>延伸阅读</h2>'
                     f'<ul style="color:var(--dim);font-size:14.5px;line-height:2;padding-left:22px">{lis}</ul></section>')

    parts.append(END)
    return wp_html, '\n'.join(parts)


def inject(page_path, wp, block):
    s = open(page_path, encoding='utf-8').read()
    s = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', s, flags=re.S)
    s = re.sub(re.escape(WSTART) + r'.*?' + re.escape(WEND), '', s, flags=re.S)
    if wp:
        i = s.find('<main')
        j = s.find('<section', i)
        if j > 0:
            s = s[:j] + wp + '\n\n  ' + s[j:]
    # 插在「本章重点」那一节之前；没有就插在 pager 之前
    m = re.search(r'\n\s*<section>\s*\n\s*<h2 class="sec-head">本章重点</h2>', s)
    if m:
        s = s[:m.start()] + '\n' + block + s[m.start():]
    else:
        s = s.replace('<nav class="pager">', block + '\n  <nav class="pager">', 1)
    open(page_path, 'w', encoding='utf-8').write(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pages', nargs='*')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--strip', action='store_true')
    args = ap.parse_args()

    cmap = chapter_map()
    pages = args.pages or sorted(glob.glob(os.path.join(ROOT, 'chapters', '*.html')))
    for p in pages:
        num = os.path.basename(p).split('-')[0]
        num = str(int(num))
        src = find_source(num)
        if not src:
            print('no source for', p)
            continue
        if args.strip:
            s = open(p, encoding='utf-8').read()
            s = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', s, flags=re.S)
            open(p, 'w', encoding='utf-8').write(s)
            print('stripped', os.path.basename(p))
            continue
        wp, block = build_html(src, os.path.basename(p), cmap)
        if args.dry:
            print(f'--- {os.path.basename(p)} ({len(wp)+len(block)} chars) ---')
            print(wp)
            print(block[:800])
            continue
        inject(p, wp, block)
        print(f'{os.path.basename(p)} +{len(block)} chars')


if __name__ == '__main__':
    main()
