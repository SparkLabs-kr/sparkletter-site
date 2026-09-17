# -*- coding: utf-8 -*-
"""archive.tsv -> articles.json

분류 규칙은 위에서부터 순서대로 검사한다(먼저 걸리는 쪽이 이김).
규칙으로 안 잡히는 건 data/overrides.tsv 에 "링크<TAB>카테고리" 로 직접 지정한다.
"""
import json, re, sys, os
from collections import Counter

CATS = ['monthly', 'insight', 'open']

RULES = [
    # ── 1) 스파크랩 월간호 : 정기 발행호 + 스파크랩 자체 소식 ──────────────
    ('monthly', [
        r'\d\s*월\s*소식', r'월소식', r'마지막.{0,4}스파크레터', r'스파크랩\s*소식',
        r'운영기관', r'\d+\s*살이 된', r'주년',
        r'스파크랩\s*&\s*포트폴리오',
    ]),
    # ── 2) 모집·행사 : 지원하거나 참가하는 모든 기회 ──────────────────────
    ('open', [
        r'데모데이', r'네트워킹', r'세미나', r'포럼', r'컨퍼런스', r'초대',
        r'사전\s*등록', r'클럽하우스', r'오디션', r'상담회', r'비즈매칭',
        r'행사', r'GRAVITY', r'슈퍼 매치', r'오피스\s*아워', r'Office Hour',
        r'한자리에', r'한 자리에', r'STARTUP:CON', r'생중계', r'D-\d',
        r'IR 미팅', r'무대', r'만나보세요', r'개최', r'참가자 모집', r'만나요',
        r'아이디어톤', r'창업경진대회', r'경진대회',
    ]),
    ('open', [
        r'\d+\s*기\b', r'배치', r'모집', r'지원하세요', r'지원 사업', r'지원사업',
        r'Spark Claw', r'스파크클로', r'액셀러레이팅', r'접수', r'도전하세요',
        r'선정된', r'선정 기업', r'선정 소식', r'선정 스타트업', r'선정됐을까',
        r'찾습니다', r'프론티어', r'PoC 참여', r'참여 기업 모집', r'신청 OPEN',
        r'스타트업을 소개합니다', r'지원 안내',
    ]),
    # ── 3) 스파크랩만의 인사이트 : 읽을거리 (규칙 없이도 기본값) ──────────
]

FALLBACK = 'insight'

# ── 'open' 안의 세부 분류 (위에서부터 먼저 걸리는 쪽이 이김) ────────────────
SUBS = ['batch', 'demoday', 'support', 'session']

SUB_RULES = [
    # 스파크랩 배치·액셀러레이팅 : 뽑혀서 들어가는 프로그램
    ('batch', [
        r'배치', r'\d+\s*기\b', r'Spark Claw', r'스파크클로', r'액셀러레이팅',
        r'함께 성장할', r'프론티어를 찾습니다', r'초기 스타트업을 찾습니다',
        r'스타트업을 소개합니다', r'선정된 스타트업', r'선정 기업',
    ]),
    # 데모데이·투자유치 : 투자자 앞에서 피칭하거나 만나는 자리
    ('demoday', [
        r'데모데이', r'IR', r'피칭', r'투자 상담', r'상담회', r'비즈매칭',
        r'VC', r'투자자', r'투자 네트워킹', r'무대', r'슈퍼 매치', r'GRAVITY',
        r'유니콘', r'배틀필드', r'오디션', r'경진대회', r'아이디어톤',
    ]),
    # 외부 지원사업·공모 : 정부·지자체·파트너사가 여는 것
    ('support', [
        r'지원\s*사업', r'지원사업', r'PoC', r'운영기관', r'지원 안내',
        r'팁스', r'정부', r'부울경', r'강남구',
    ]),
    # 세미나·네트워킹 : 듣고 교류하는 자리 (기본값)
]
SUB_FALLBACK = 'session'


def classify_sub(title):
    for sub, pats in SUB_RULES:
        for p in pats:
            if re.search(p, title, re.I):
                return sub
    return SUB_FALLBACK



def classify(title):
    for cat, pats in RULES:
        for p in pats:
            if re.search(p, title, re.I):
                return cat
    return FALLBACK


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tsv = os.path.join(base, 'data', 'archive.tsv')
    ovr = os.path.join(base, 'data', 'overrides.tsv')
    out = os.path.join(base, 'articles.json')

    overrides = {}
    if os.path.exists(ovr):
        for line in open(ovr, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            url, cat = line.split('\t')[:2]
            overrides[url.strip()] = cat.strip()

    rows = []
    for line in open(tsv, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        d, title, url = line.split('\t')
        y, m, dd = re.findall(r'\d+', d)
        url = url.strip()
        raw = overrides.get(url) or classify(title)
        cat, _, sub = raw.partition(':')
        if cat not in CATS:
            sys.exit(f'알 수 없는 카테고리 "{cat}" — {url}')
        if cat == 'open':
            sub = sub or classify_sub(title)
            if sub not in SUBS:
                sys.exit(f'알 수 없는 세부분류 "{sub}" — {url}')
        else:
            sub = None
        rows.append({
            'date': f'{y}-{int(m):02d}-{int(dd):02d}',
            'title': title.strip(),
            'url': url,
            'category': cat,
            'sub': sub,
            'ad': title.strip().startswith(('(광고)', '(재발송)')),
        })

    rows.sort(key=lambda r: r['date'], reverse=True)
    json.dump(rows, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    c = Counter(r['category'] for r in rows)
    print(f'총 {len(rows)}건 (수동 지정 {len(overrides)}건)')
    for k in CATS:
        print(f'  {k:8} {c[k]:3}')
    sc = Counter(r['sub'] for r in rows if r['sub'])
    print('  └ open 세부')
    for k in SUBS:
        print(f'      {k:9} {sc[k]:3}')


if __name__ == '__main__':
    main()
