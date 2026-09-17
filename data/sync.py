# -*- coding: utf-8 -*-
"""스티비 아카이브 → articles.json

스티비 공개 엔드포인트에서 발송 목록을 받아 분류해 articles.json으로 쓴다.
인증이 필요 없다(스티비 '이메일 목록 조회' API는 프로 전용이지만, 아카이브 페이지가
쓰는 이 엔드포인트는 공개되어 있다).

    python3 data/sync.py            # 받아서 갱신
    python3 data/sync.py --offline  # 네트워크 없이 data/archive.json 캐시로만
"""
import json, os, re, sys, urllib.request
from collections import Counter

LIST_ID = 106252
URL = f'https://page.stibee.com/archives/{LIST_ID}/emails'

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(BASE, 'data', 'archive.json')     # 원본 응답 스냅샷
OVERRIDES = os.path.join(BASE, 'data', 'overrides.tsv')
OUT = os.path.join(BASE, 'articles.json')

# ── 분류 규칙 : 위에서부터 먼저 걸리는 쪽이 이긴다 ─────────────────────────
CATS = ['monthly', 'insight', 'open']
RULES = [
    ('monthly', [
        r'\d\s*월\s*소식', r'월소식', r'마지막.{0,4}스파크레터', r'스파크랩\s*소식',
        r'\d+\s*살이 된', r'주년', r'스파크랩\s*&\s*포트폴리오',
    ]),
    ('open', [
        r'데모데이', r'네트워킹', r'세미나', r'포럼', r'컨퍼런스', r'초대',
        r'사전\s*등록', r'클럽하우스', r'오디션', r'상담회', r'비즈매칭',
        r'행사', r'GRAVITY', r'슈퍼 매치', r'오피스\s*아워', r'Office Hour',
        r'한자리에', r'한 자리에', r'STARTUP:CON', r'생중계', r'D-\d',
        r'IR 미팅', r'무대', r'만나보세요', r'개최', r'참가자 모집', r'만나요',
        r'아이디어톤', r'창업경진대회', r'경진대회',
        r'\d+\s*기\b', r'배치', r'모집', r'지원하세요', r'지원 사업', r'지원사업',
        r'Spark Claw', r'스파크클로', r'액셀러레이팅', r'접수', r'도전하세요',
        r'선정된', r'선정 기업', r'선정 소식', r'선정 스타트업', r'선정됐을까',
        r'찾습니다', r'프론티어', r'PoC 참여', r'참여 기업 모집', r'신청 OPEN',
        r'스타트업을 소개합니다', r'지원 안내', r'운영기관',
    ]),
]
FALLBACK = 'insight'

# ── 'open' 안의 세부 분류 ────────────────────────────────────────────────
SUBS = ['batch', 'demoday', 'support', 'session']
SUB_RULES = [
    ('batch', [
        r'배치', r'\d+\s*기\b', r'Spark Claw', r'스파크클로', r'액셀러레이팅',
        r'함께 성장할', r'프론티어를 찾습니다', r'초기 스타트업을 찾습니다',
        r'스타트업을 소개합니다', r'선정된 스타트업', r'선정 기업',
    ]),
    ('demoday', [
        r'데모데이', r'IR', r'피칭', r'투자 상담', r'상담회', r'비즈매칭',
        r'VC', r'투자자', r'투자 네트워킹', r'무대', r'슈퍼 매치', r'GRAVITY',
        r'유니콘', r'배틀필드', r'오디션', r'경진대회', r'아이디어톤',
    ]),
    ('support', [
        r'지원\s*사업', r'지원사업', r'PoC', r'운영기관', r'지원 안내',
        r'팁스', r'정부', r'부울경', r'강남구',
    ]),
]
SUB_FALLBACK = 'session'


def match(title, rules, fallback):
    for name, pats in rules:
        for p in pats:
            if re.search(p, title, re.I):
                return name
    return fallback


def load_overrides():
    out = {}
    if not os.path.exists(OVERRIDES):
        return out
    for line in open(OVERRIDES, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        url, cat = line.split('\t')[:2]
        out[url.strip()] = cat.strip()
    return out


def fetch():
    req = urllib.request.Request(URL, headers={
        'Accept': 'application/json',
        'User-Agent': 'sparkletter-site/1.0 (+https://github.com/SparkLabs-kr/sparkletter-site)',
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def main():
    offline = '--offline' in sys.argv

    if offline:
        raw = json.load(open(CACHE, encoding='utf-8'))
        print(f'캐시 사용: {CACHE}')
    else:
        raw = fetch()
        json.dump(raw, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'스티비에서 {len(raw)}건 수신')

    overrides = load_overrides()
    rows = []
    for e in raw:
        title = (e.get('subject') or '').strip()
        url = (e.get('permanentLink') or '').strip()
        if not title or not url:
            continue

        spec = overrides.get(url) or match(title, RULES, FALLBACK)
        cat, _, sub = spec.partition(':')
        if cat not in CATS:
            sys.exit(f'알 수 없는 카테고리 "{cat}" — {url}')
        if cat == 'open':
            sub = sub or match(title, SUB_RULES, SUB_FALLBACK)
            if sub not in SUBS:
                sys.exit(f'알 수 없는 세부분류 "{sub}" — {url}')
        else:
            sub = None

        rows.append({
            'date': (e.get('sentTime') or '')[:10],
            'title': title,
            'url': url,
            'category': cat,
            'sub': sub,
            'preview': (e.get('previewText') or '').strip(),
            'ad': title.startswith(('(광고)', '(재발송)')),
        })

    rows.sort(key=lambda r: r['date'], reverse=True)

    before = None
    if os.path.exists(OUT):
        before = open(OUT, encoding='utf-8').read()
    after = json.dumps(rows, ensure_ascii=False, indent=1)
    changed = before != after
    open(OUT, 'w', encoding='utf-8').write(after)

    c = Counter(r['category'] for r in rows)
    sc = Counter(r['sub'] for r in rows if r['sub'])
    print(f'총 {len(rows)}건 (수동 지정 {len(overrides)}건) — {"변경됨" if changed else "변경 없음"}')
    for k in CATS:
        print(f'  {k:8} {c[k]:3}')
    print('  └ open 세부')
    for k in SUBS:
        print(f'      {k:9} {sc[k]:3}')


if __name__ == '__main__':
    main()
