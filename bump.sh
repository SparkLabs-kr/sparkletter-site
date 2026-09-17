#!/bin/sh
# CSS·JS를 고친 뒤 실행한다. 파일 주소에 버전을 붙여 방문자 브라우저가 옛 파일을 계속 쓰는 것을 막는다.
# (GitHub Pages는 CSS·JS에 긴 캐시를 걸어서, 버전을 안 바꾸면 갱신이 안 보인다)
V=$(date +%Y%m%d%H%M)
sed -i '' "s|href=\"style.css?v=[0-9]*\"|href=\"style.css?v=$V\"|g; s|src=\"app.js?v=[0-9]*\"|src=\"app.js?v=$V\"|g" index.html feedback.html
echo "버전 갱신: $V"
