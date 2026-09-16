# -*- coding: utf-8 -*-
"""archive.tsv -> articles.json  (카테고리 자동 분류)"""
import json, re, sys
from collections import Counter

RULES = [
  # 순서 중요: 위에서부터 먼저 걸린다

  ('event',   ['데모데이','네트워킹','세미나','포럼','컨퍼런스','초대','사전등록','사전 등록',
               '클럽하우스','오디션','상담회','비즈매칭','행사','gravity','슈퍼 매치',
               'office hour','오피스아워','한자리에','startup:con','만나보세요','만나는',
               '생중계','접수 start','d-6','참가자 모집','만나요','무대']),
  ('program', ['배치','기 프로그램','모집','지원하세요','지원 사업','지원사업','spark claw',
               '스파크클로','액셀러레이팅','접수','선정','운영기관','찾습니다','프론티어',
               '아이디어톤','창업경진대회','poc 참여','도전하세요','신청 open','지원 안내',
               '참여 기업','모집 안내','기업을 모집']),
  ('insight', ['꿀팁','노하우','비밀','비하인드','결정 기준','특징 3가지','말하는','밝히는',
               '어떻게 진출','전략 대방출','팁 대방출','북극성','쌉가능','어디서 빌리나',
               '하고 싶은 이야기','성장 전략','인사이트 공유','밖에 모르신다고요',
               '진짜 도움 돼','고민을 들려주세요','궁금하다면']),
]

def cat(t):
    low = t.lower()
    if re.search(r'(월\s*소식|월소식|마지막 .{0,3}스파크레터|스파크레터\s*\d|스파크랩 소식)', t):
        return 'news'
    for name, kws in RULES:
        if any(k in low for k in kws):
            return name
    return 'news'

rows = []
for line in open('data/archive.tsv', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip(): continue
    d, title, url = line.split('\t')
    y, m, dd = re.findall(r'\d+', d)
    rows.append({
        'date': f'{y}-{int(m):02d}-{int(dd):02d}',
        'title': title.strip(),
        'url': url.strip(),
        'category': cat(title),
        'ad': title.strip().startswith(('(광고)', '(재발송)')),
    })
rows.sort(key=lambda r: r['date'], reverse=True)
json.dump(rows, open('articles.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('총', len(rows), dict(Counter(r['category'] for r in rows)))
