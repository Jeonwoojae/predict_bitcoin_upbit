# predict_bitcoin_upbit
한이음 멘토링에서 수행하는 비트코인 가격예측 프로젝트

### 업비트 api의 요청 수 제한
주문 요청 : 초당 8회, 분당 200회
그 외 API : 초당 30회, 분당 900회

Quotation API의 경우
Websocket 연결 요청 수 : 초당 5회, 분당 100회
Rest API 요청 수 : 초당 10회, 분당 600회 (종목, 캔들, 체결, 티커, 호가별 각각 적용)


git push -u origin main

실수로 토큰 노출의 경우
해당 커밋으로 복구 : git reset --hard 해당 커밋 해시
올린 스테이징으로 커밋 덮어쓰기 : git commit --amend
강제로 push : git push -u origin main --force
