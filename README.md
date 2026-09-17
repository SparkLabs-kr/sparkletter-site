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

## articles.json 갱신 — 자동

스티비 공개 엔드포인트에서 받아온다. **인증이 필요 없다.**

    https://page.stibee.com/archives/106252/emails   ← 제목·링크·발송일·미리보기문구

- `.github/workflows/sync-archive.yml` 이 **매일 10:00 KST**에 돌고, 변경이 있을 때만 커밋한다.
- 새 호를 발송하면 다음 날 자동 반영된다. 손댈 것이 없다.
- 즉시 반영하려면 GitHub → Actions → "스티비 아카이브 동기화" → Run workflow.
- 로컬에서 돌리려면 `python3 data/sync.py` (`--offline`은 네트워크 없이 캐시로만).

> 스티비 '이메일 목록 조회' **API는 프로 요금제 전용**이라 못 쓴다.
> 하지만 아카이브 페이지가 쓰는 위 엔드포인트는 공개되어 있어 스탠다드에서도 그냥 된다.
> 예전에는 `data/archive.tsv`를 손으로 고쳤는데, 이제 필요 없어서 지웠다.

### 카테고리 (3종 + open 세부 4종)
| 키 | 화면 이름 | 기준 |
|---|---|---|
| monthly | 📅 스파크랩 월간호 | 정기 발행호(N월 소식) |
| insight | 💡 스파크랩만의 인사이트 | 읽을거리 — 노하우·인터뷰·전략 (**기본값**) |
| open | 🚀 모집·행사 | 지원하거나 참가하는 모든 기회 |

| sub | 화면 이름 |
|---|---|
| batch | 🎓 배치·액셀러레이팅 |
| demoday | 📊 데모데이·투자유치 |
| session | 🎤 세미나·네트워킹 (**기본값**) |
| support | 🏛 지원사업·공모 |

규칙은 `data/sync.py`의 `RULES`/`SUB_RULES`에 있고 위에서부터 먼저 걸리는 쪽이 이긴다.
개별 예외는 `data/overrides.tsv`에 `링크<TAB>카테고리` 한 줄(세부까지 지정하려면 `open:demoday`).

## 스티비 연결 (고정값)
- 구독 페이지: https://page.stibee.com/subscriptions/106252
- 아카이브 전체: https://page.stibee.com/archives/106252

## 디자인 — D. Clay + Electric (2026-09-17)
색 변수는 `style.css` 최상단 `:root` 한 곳에 있다.

- 바탕은 순수 검정이 아니라 **따뜻한 클레이 다크(#1B1A16)**, 카드는 한 단계 밝은 #24231D
- **코랄(#FF5C39)은 화면에서 유일하게 튀는 색** — 구독·아카이브 버튼에만 쓴다
- 카테고리 칩은 어스톤(클레이/올리브/오커)으로 낮춰 액센트와 경쟁하지 않게 한다
- 타이포는 clamp로 확대(히어로 최대 60px, 섹션 제목 최대 32px)
- `word-break:keep-all` — 한국어가 어절 중간에서 끊기지 않게

> 라이트(웜 본 → 쿨 near-white)도 만들어봤으나 밋밋해서 D로 정했다.
> 후보 4종 비교본은 `mockups/palettes.html`에 남아 있다.
> 어두운 바탕이므로 로고는 **logo-white.png**(원본에서 검은 글자만 흰색으로 바꾼 것)를 쓴다.
> 원본은 `data/logo.png`. 배경을 다시 밝게 바꾸면 원본으로 되돌리면 된다.

## 저장소 · 배포 주소
- **정식**: `SparkLabs-kr/sparkletter-site` (Public) → https://sparklabs-kr.github.io/sparkletter-site/
- 개인 계정 `sl2266/sparkletter-site`는 회사 저장소가 Private이던 동안 임시로 쓰던 미러다.
  회사 Pages가 뜨면 더 쓰지 않는다. (remote 이름 `personal`)

평소에는 `git push origin main` 하나면 된다.
