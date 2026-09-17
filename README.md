# 스파크레터 웹사이트

## 폴더 구조
- `mockups/` — UI 목업
- `site/` — 실제 사이트 코드
- `data/` — 아카이브 목록, 로고 원본

## data/archive.tsv
스티비 아카이브(page.stibee.com/archives/106252)에서 추출한 지난 호 106건.
형식: 날짜 <TAB> 제목 <TAB> 링크

## 방향
- 구독 폼 · 발송 · 구독자 관리 → 스티비 (그대로)
- 안내 페이지 · 지난 호 분류 목록 → 이 사이트
- 스티비 이메일 목록 API는 프로 요금제 전용 → 현재 스탠다드라 사용 불가.
  당분간 archive.tsv를 사람이 갱신한다.

## 사이트 구조
- `index.html` — 지난 호 아카이브 (섹션별 카드 그리드)
- 구독은 별도 페이지 없이 사이드바에서 스티비로 바로 연결한다
- `feedback.html` — 피드백
- `app.js` / `style.css` / `articles.json` / `logo-white.png`

배포용 파일은 **저장소 루트**에 둔다. Vercel·GitHub Pages가 설정 없이 바로 서빙한다.
`mockups/`, `data/`는 정적 호스팅이 무시하므로 같이 두어도 안전하다.

## articles.json 갱신

`data/archive.tsv`에 한 줄(날짜<TAB>제목<TAB>링크) 추가 후 `python3 data/classify.py`.

### 카테고리 (3종)
| 키 | 화면 이름 | 기준 |
|---|---|---|
| monthly | 📅 스파크랩 월간호 | 정기 발행호(N월 소식) |
| insight | 💡 스파크랩만의 인사이트 | 읽을거리 — 노하우·인터뷰·전략 (**기본값**) |
| open | 🚀 모집·행사 | 지원하거나 참가하는 모든 기회 |

`open`은 다시 4개로 나뉜다(`SUB_RULES`). 화면에서는 섹션 위 **필터 칩**으로 고르고,
카드 칩에는 대분류 대신 세부 분류 이름이 뜬다.

| sub | 화면 이름 | 기준 |
|---|---|---|
| batch | 🎓 배치·액셀러레이팅 | 뽑혀서 들어가는 스파크랩 프로그램 (N기, Spark Claw) |
| demoday | 📊 데모데이·투자유치 | 투자자 앞에서 피칭하거나 만나는 자리 |
| session | 🎤 세미나·네트워킹 | 듣고 교류하는 자리 (**기본값**) |
| support | 🏛 지원사업·공모 | 정부·지자체·파트너사가 여는 것 |

overrides.tsv에서 세부까지 지정하려면 `링크<TAB>open:demoday` 처럼 쓴다.

> 세부 축은 '독자 행동(지원/참가/관람)'도 후보였으나, 지난 호 아카이브라
> "마감 임박" 건들이 전부 이미 지난 마감이어서 의미가 없어 기회의 종류로 나눴다.

규칙은 `data/classify.py`의 `RULES`에 있고 **위에서부터 먼저 걸리는 쪽이 이긴다**
(monthly → open → 나머지는 insight).

개별 예외는 **`data/overrides.tsv`** 에 `링크<TAB>카테고리` 한 줄. 규칙보다 우선한다.

> 원래 event(행사)와 program(모집)을 나눴는데 실제 호들이 두 성격을 같이 갖는 경우가 많아
> (데모데이 = 행사이자 참가 모집) 2026-09-17에 open 하나로 합쳤다.
> 그 전에는 'news'가 폴백 통이어서 월간호·인터뷰·행사가 뒤섞이는 문제도 있었다.


## 새 호가 나가면 — 수동 갱신 필요
스티비 '이메일 목록 조회' API는 **프로 요금제 전용**이라 현재(스탠다드) 자동 연동이 불가능하다.

    # data/archive.tsv 맨 위에 추가:  2026.9.30<TAB>9월 소식<TAB>https://stib.ee/xxxx
    python3 data/classify.py
    git add -A && git commit -m "add: 9월호" && git push origin main && git push personal main

링크는 스티비 아카이브에서 해당 호 제목 우클릭 → 링크 주소 복사.
`articles.json`은 `cache: 'no-cache'`로 읽으므로 방문자에게 옛 목록이 남지 않는다.

## 스티비 연결 (고정값)
- 구독 페이지: https://page.stibee.com/subscriptions/106252
- 아카이브 전체: https://page.stibee.com/archives/106252
