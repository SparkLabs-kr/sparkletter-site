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
- `index.html` — 지난 호 아카이브 (카테고리 탭 필터)
- `subscribe.html` — 구독 안내 (레터 3종 카드 → 스티비)
- `feedback.html` — 피드백
- `app.js` / `style.css` / `articles.json` / `logo-white.png`

배포용 파일은 **저장소 루트**에 둔다. Vercel·GitHub Pages가 설정 없이 바로 서빙한다.
`mockups/`, `data/`는 정적 호스팅이 무시하므로 같이 두어도 안전하다.

## articles.json 갱신
`data/archive.tsv`에 한 줄(날짜<TAB>제목<TAB>링크) 추가 후:
    python3 data/classify.py
카테고리는 제목 키워드로 자동 분류된다(event → program → insight → news 순).
틀리면 `articles.json`의 해당 `category`를 직접 고쳐도 되지만,
classify.py를 다시 돌리면 덮어쓰므로 규칙 쪽을 고치는 편이 안전하다.

## 남은 TODO
- subscribe.html: 스티비 구독 페이지 주소 (`000000`) 교체
- feedback.html: 구글 폼 주소 연결

## 설계 메모
구독은 **한 군데로만** 받는다(그룹 분리 안 함). 웹사이트에서만 주제별로 분류해 보여준다.
카드를 누르면 스티비 원문(stib.ee/...)으로 이동한다 — 본문은 복제하지 않는다.

## 배포 — GitHub Pages
Settings → Pages → Source: *Deploy from a branch* → Branch `main` / `(root)` → Save.
`.nojekyll`이 있어야 Jekyll이 파일을 건드리지 않는다(밑줄로 시작하는 파일 무시 등).
저장소가 Public이어야 무료다. push하면 1~2분 뒤 자동 반영된다.
