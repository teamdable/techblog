---
layout: post
title: "Oauth provider 제작 가이드"
date: 2021-06-21 00:00:00 +0900
author: Sunghyun Lee
tags: [이성현, oauth, oauth2, oauth provider, oauth server, oauth 서버]
---

안녕하세요 데이블 Publisher Platform 팀의 이성현입니다.

최근 외부 업체와의 Oauth 연동을 위해 Oauth provider 서버를 제작했고, 제작 과정에서 겪은 시행착오와 경험을 정리해 보았습니다.

---
## 전체 Oauth 인증 flow 예시 (authorization code grant)

직접 구현하시면 사정에 맞게 달라질 부분이 많으므로 참고용으로만 읽어 주세요.

**P** = Oauth provider = Oauth host = 데이블.

**C** = Oauth client = 특정 유저의 데이블내 정보가 필요한 외부 app.

**U** = user = C의 사용자. C를 통해 P로 로그인하여 C가 P의 인증 정보를 활용할 수 있도록 함.

**(Oauth provider 측이 미리 준비할 것)**

1. **P**: 표준 절차대로 토큰을 발급하는 서버 제작
2. **P**: resource 요청 시 access_token 검증하고 데이터를 내어주는 로직 구현
3. **P**: client 등록 방법부터 access_token을 사용해서 resource 요청하는 방법까지 상세히 기술된 문서 publish
4. **P**: client에서 유저가 Oauth 연동을 위해 랜딩할 로그인 페이지 제작

**(유저에게 Oauth 인증기능을 제공하기 전 client 개발자가 할 일)**

1. **C→P** Oauth provider에 개발자의 app을 Oauth 연동 가능한 client로 등록 (UI 또는 이메일)
2. **P→C** client id, secret 발급하고 client는 이 정보 보관

**(client에서 유저가 Oauth 인증기능 사용 시작)**

1. **U**: client 앱에서 "client 앱이 유저를 대행해 P에서 정보를 자동으로 조회할 수 있도록 만듭니다" 의미가 있는 연동 버튼 클릭
2. **C**: 유저에게 P 로그인 페이지 팝업 오픈 (query string 파라미터에 callback_url, client_id 포함. client_secret 제외)
3. **U**: P로그인 팝업에 id/password 입력, submit
4. **P**: 유저 세션 데이터 생성, 유저에게 세션용 쿠키 set 및 /authorization endpoint로 redirect 응답
5. **U**: P/login → P/authorize 이동 (등록된 client, 등록된 callback_url 인지 검증해서 ok일때만)
6. **P**: 로그인 세션 확인 + 로그인 확인 문자열(authorization_code) 생성 후 callback_url 뒤에 붙여 redirect 응답
7. **U**: P→C callback_url 이동
8. **C**: callback_url 의 컨트롤러가 요청 url을 파싱하여 유저가 가지고 온 authorization_code 획득 및 저장
9. **C→P**: authorization_code 사용해서 token 요청 (client_secret 포함)
10. **P→C**: token 생성 후 시스템에 저장하고 token 응답
11. **C**: 유저 단위로 token 저장, 사용 준비 완료

**(Client의 token 사용)**

1. **C→P**: token 사용해서 리소스 요청
2. **P**: 인증확인 후 데이터 응답

**(Provider의 token 재발급)**

1. **C→P**: token 사용해서 리소스 요청
2. **P→C**: expired 응답
3. **C→P**: refresh_token 사용해서 토큰 재발급 요청
4. **P→C**: expired 응답(refresh_token 만료) 또는 재발급된 토큰 전달
5. **C**: 유저 재 로그인 필요하다고 표시 또는 재발급된 토큰 저장 후 리소스 다시 요청

---
## 시작 전 정리할 부분 (미리 알았더라면 좋았을걸..)

### 1. client 별 권한 구분이 필요하면 권한부터 설계하자

예를 들어 통계조회 기능을 Oauth 인증으로 외부에서 접근할 수 있도록 개발 중이라면, 전체 통계를 조회할 수 있는 client와 일부 통계만 접근할 수 있는 client를 구분해야 할 수 있습니다. client는 필요한 권한을 텍스트로 scope 필드에 넣어 요청해야 하므로 사전에 권한 분석이 필요합니다.

공개된 api가 몇 없고, 연동해서 쓸 client도 제한적인 상황이라면 권한을 분리해 관리할 필요가 없을 수 있습니다. 그러면 일단 한가지 권한으로만 운용하다가 분리가 필요해지는 상황에 scope를 추가하고 기존 범용 scope로 발급했던 token들을 invalidate 하면 됩니다.

### 2. 데이터 저장 구조

Oauth provider 제작 시 기본적으로 저장이 필요한 데이터의 종류입니다.

- internal: 권한 목록
- client 단위: id, secret, 요청 가능한 권한의 종류(scope), callback urls
- user 단위: authorization_code, authorization_code_expires, access_token, access_token_expires, refresh_token, refresh_token_expires, 권한(scope)

이 중 internal과 client 항목은 잘 변하지 않습니다. 구글처럼 client를 직접 등록할 수 있는 구조라면 client도 변할 수 있어 별도 저장소를 준비해야 하겠지만, 규모가 작을 때는 보통 권한 종류는 한두 개고 client는 연동 시 수동으로 추가해주는 경우가 대부분일 것입니다. 연동 초기에는 권한과 client 정보를 하드코딩으로 구현하는 것을 권장해 드립니다.

반면 user 단위 데이터는 client 요청에 따라 생성되므로 코드에 넣을 수 없고 별도 저장소를 운영해야 합니다. 토큰-데이터의 key-value 관계와 expire에 착안해서 TTL 처리가 간편한 redis를 쓸 수도 있습니다.

Redis를 토큰 저장소로 쓰면서 expire를 지정한 경우 일정 시간이 지났을 때 토큰 key가 아예 삭제될 텐데, client에게 해당 access_token이 존재하지 않는 상황과 expire 된 상황을 구분해서 전달해야 하는지를 고민해봐야 합니다. 구분해야 하면 redis TTL이 token들의 lifetime 대비 2~4배 정도로 길게 설정해두고 redis에 저장한 토큰 데이터 내부에 토큰이 언제 만료되는지를 별도로 보관해서 일정 시간까지는 expire를 알려주고 더 시간이 지났을 때 key를 삭제하는 방법이 있습니다.

연동하는 client 수가 적고, 사용자 수가 많지 않으면 어디에 저장하든 조회속도도 빠를 것이고 만료된 토큰도 굳이 삭제할 필요가 없을 수 있습니다. 이럴 때는 RDB 등에 토큰을 영구 저장하고 가져와 쓰는 식으로 구현할 수 있습니다.

### 3. access_token의 검증을 어디에서 할까

Oauth provider 서버는 토큰 발급에 특별한 프로토콜을 요구하기 때문에 보통 resource server와 별개 서버로 개발합니다. 발급은 Oauth 서버에서 하는데, 목적 데이터는 다른 서버에 있는 상황입니다. 리소스 서버는 Oauth 관련 코드도 없는데 어떻게 검증을 할까요? 각 리소스 서버마다 access_token 및 scope 검증 로직을 구현해야 할까요? [RFC6749](https://datatracker.ietf.org/doc/html/rfc6749) 문서는 리소스를 조회하는 과정을 정의하지 않으므로 access_token 검증을 시스템 어디에다 구현할지는 개발자가 결정해야 합니다.

고민했던 위치는 크게 세 가지입니다.

- Oauth provider 서버가 토큰 발급, 리소스 조회를 모두 하는 방법입니다.

  리소스 서버는 Oauth 서버에서만 접근할 수 있도록 구성하고, client는 토큰 발급과 리소스 요청 모두를 Oauth 서버로 합니다. 이 경우 Oauth 서버가 Oauth 관련 경로와 리소스 요청 관련 경로를 모두 갖게 됩니다. Oauth 서버는 토큰을 검증한 후 리소스 서버로 proxy 요청을 해서 데이터를 응답합니다.

  Oauth 쪽 로직 재사용을 할 수 있어 개발 기간이 짧은 것이 장점입니다. 단점은 Oauth 서버에 proxy용 처리가 더해지면서 부하가 늘어날 수 있고, 토큰 발급기능과 리소스 접근 기능 둘 중 하나만 망가져도 다른 한쪽도 같이 문제가 생길 수 있습니다.

- 리소스 조회용 proxy 서버를 만드는 방법입니다.

  Oauth 서버는 token 발급용으로 그대로 두고, access_token 검증 및 데이터 proxy 요청 기능만 가진 별도 서버를 운영하는 형태입니다. 일종의 보안 gateway 역할이며 Oauth를 사용하지 않던 기존 시스템을 손대지 않아도 되는 장점이 있습니다.

- 토큰 검증을 각 리소스 서버에서 하는 방법입니다.

  토큰 검증 로직을 매 서버에 일일이 작성하는 것은 유지보수 측면에서 권장하지 않습니다. 대신 사내 Oauth 토큰인증을 담당하는 라이브러리를 하나 만들고 각 서버에서 공유해 사용하시길 추천해 드립니다.

  서버 대수가 많을경우 토큰 저장소에 요청횟수가 늘어 부하가 생길 수 있습니다. 이러면 일단 connection pool을 사용해 보시고, 그래도 감당이 안 되면 토큰형식을 JWT로 변경해서 토큰 저장소 접근량을 줄이는 방법을 권장합니다.

  직접 인증을 하려면 리소스 서버들을 외부에 공개해야 하므로 보안에 민감한 서버에는 사용하기 어렵습니다. 이때는 리소스 조회용 proxy 서버를 사용해 데이터를 중계하는 방법을 검토해 보세요.

### 4. 유저 로그인 페이지

흔히 사용하는 구글 Oauth 인증을 예로 들어보면 client는 유저를 구글 로그인 창으로 먼저 보내고, 구글은 유저가 로그인을 완료하면 로그인 성공을 인증하는 string(=authorization code)을 url에 쿼리스트링으로 붙여 client의 callback url 로 이동시킵니다.

이 로그인 flow 설계 및 로그인 페이지 작업이 추가로 필요합니다. [RFC6749](https://datatracker.ietf.org/doc/html/rfc6749)는 로그인을 어떻게 해야 하는지, 로그인 완료 후 어떤 과정을 거쳐 authorization code를 붙여 callback url로 유저를 이동시킬지 등을 개발자에게 맡기고 있습니다. 설계 방향에 따라 구현이 까다로울 수 있습니다.

제 경험에서는 로그인 기능을 어떤 서버에 둘지와 어떤 방법으로 Oauth 서버에서 유저의 로그인 여부를 확인할지를 결정하는 것이 중요했습니다.

로그인 기능의 구현 위치는 세 가지 정도의 옵션이 있었습니다.

- Oauth서버
- 로그인만 담당하는 별도 서버
- 기존 로그인 기능이 붙어있는 다른 서버에 붙인 후 세션을 공유

로그인 여부 확인 방법은 로그인 기능방식에 따라 달라지지만, 이미 사용 중인 유저 세션이 구조가 있다면 그대로 활용하시길 권장해 드립니다.

데이블에서는 로그인 페이지를 Oauth 서버에 뒀고 다음 과정을 사용합니다.

1. 유저 랜딩: /login (로그인 페이지)
2. 로그인 완료시 쿠키세션 생성 및 /authorize 이동. 이동 시 쿼리스트링 데이터 유지
3. /authorize에서 유저 세션 확인 후 세션이 존재하면 데이블 로그인 완료로 판단, 유저를 다시 client callback url 로 이동

### 5. 토큰 문자열 형식

토큰 길이, 종류, 생성 방법을 고민하셔야 합니다.

자료를 찾아보시면 JWT를 많이 언급하지만 표준에서는 토큰에 어떤 형식을 써야만 한다고 강제한 적이 없어 권장 사항일 뿐입니다. 반드시 JWT를 사용해야 하는 것은 아니며 Oauth 사용자 규모가 작다면 오히려 별 이득 없이 개발 기간만 길어질 수 있으니 저장소 부하를 줄여야 하는 상황이 있을때만 JWT를 사용하시길 추천해 드립니다.

데이블은 32글자의 랜덤 md5 hash를 사용하면서 토큰 종류에 따라 토큰의 앞에 a* , r* 등을 붙이고 있습니다. (a_abcdabcdabcdabcdabcdabcd: access_token)

### 6. 토큰의 만료 기간

리서치를 해보니 token 저장 위치가 유저인지, client 서버인지에 따라 기간 차이를 두는 분위기입니다.

- browser 등 유저쪽에 저장시: access token) 수일, refresh token) 1달 미만.
- 서버에 저장시: access token) 1~2개월, refresh token) 6개월~1년.

데이블은 서버 to 서버 방식만 사용하기 때문에 access_token 은 30일, refresh token은 180일로 설정했습니다.

### 7. token 재발급 방식

token의 사용기한 연장 방법은 크게 두가지입니다.

- key 새로발급
- key는 그대로인데 사용가능 기간만 업데이트

보안 측면에서 일정 주기로 key를 바꿔주는것이 좋기 때문에 사용가능 기간만 업데이트하는 것보다는 key 재발급과 동시에 새로운 유효기한을 설정해 주세요. 이 정책은 client 개발자가 헷갈리지 않도록 문서에 포함하면 좋습니다.

### 8. refresh_token의 재발급 정책

access_token은 expire 되면 refresh_token으로 재발급받아 다시 쓸 수 있지만 refresh_token은 expire 되면 유저 로그인을 다시 거쳐야 합니다.

refresh token이 expire 되면, 유저가 client에 방문해 연동 절차를 다시 밟기 전까지 provider-client 간의 api 콜은 막히기 때문에 자동으로 반영되어야 할 데이터가 누락되는 등 유저가 불편을 느끼는 상황이 생길 수 있습니다. 따라서 provider 입장에서 재 로그인을 요청하는 빈도를 모든 유저에게 공통으로 적용할지, 활동이 있으면 조금씩 길게 연장해줄지, 그래도 최대 1년까지만 연장해줄지 등의 정책 결정이 필요합니다. 이 기간 조절은 refresh_token의 expire를 조절하는 방식으로 이루어집니다.

- 무한정 연장하는 방법: access_token 재발급 시점에 매번 refresh_token도 재발급하고 유효기한을 처음부터 다시 설정하기
- 최대 1년까지 연장하는 방법: access_token 재발급 시 refresh_token의 유효기한을 늘려주되 refresh_token의 최초 발급일로부터 1년을 넘지 않도록

만약 access_token expire 시점마다 refresh_token을 재발급하기로 하셨다면 아직 유효기한이 남은 기존 refresh_token을 사용할 수 없도록 폐기할지 그대로 둘지를 선택해야 합니다. 표준에서는 정의하지 않았기 때문에 어떤 방식이든 가능하지만, 1 유저에 2개 이상의 key가 있으면 관리가 어려우므로 폐기를 권장합니다.

폐기하는 경우 client에도 이전에 사용하던 유저별 key를 쓸 수 없으니 새로 받은 token을 써달라고 문서화해야 합니다.

### 9. token의 저장구조

실제로 Oauth 서버를 만들다 보면 client의 고객 관리용 api를 거의 필수로 갖추게 됩니다.

- access_token으로 유저를 찾는 api
- access_token으로 access_token 및 refresh_token을 동시에 비활성화시키는 logout api
- refresh_token으로 access_token을 찾거나 그 반대를 찾는 유틸리티 기능

이런 요구사항이 생길 수 있는 것을 모르고 user 하위에만 토큰을 저장하는 구조를 사용하면 조회가 곤란한 상황이 생깁니다. 운영에 필요할 만한 api가 뭐가 있을지 초기에 client측 개발자와 이야기해보고 저장 구조를 고민하시기 바랍니다.

데이블에서는 redis에 access_token 및 refresh_token을 따로 저장하지만, 내용물은 두 key 모두 동일하게 access_token, refresh_token, client, user 모두를 JSON string으로 저장합니다. 재발급 때 access, refresh token을 전부 폐기하고 새로 생성했기 때문에 string을 통으로 넣고 있지만, 일부 값을 업데이트할 필요가 있다면 hset 등을 이용해도 좋겠습니다.

---

## 시작하고 나서 Tip

### 1. Oauth 요청-응답 핸들링 라이브러리 리서치

표준이 정해준 영역은 잘 구현된 라이브러리를 사용하시는 것을 추천해 드립니다. Oauth 표준은 부분적으로 계속 패치되는 중이라 2021년 시점에 직접 구현을 하려면 읽어야 할 문서가 20종 정도로 매우 많아졌습니다. 또한 Oauth 표준을 직접 만들지 않더라도, 표준이 다루지 않는 스펙을 회사 맞춤으로 설계하느라 소모하는 시간이 생각보다 큽니다. 표준은 라이브러리에 맡기고 부가적인 기능만 구현하시더라도 처음 예상한 만큼의 시간이 걸릴 수 있습니다.

경험 삼아 처음부터 구현해보고 싶을 때도 라이브러리 사용을 추천해 드립니다. 라이브러리를 쓴다고 하더라도 요청 validation, 응답 formatting 정도만 해줄 뿐 실제 동작에 필요한 코드는 개발자가 모두 작성해야 하므로 경험을 충분히 할 수 있습니다. 예를 들어 토큰 발급 요청에서 필수 파라미터가 없거나 유효하지 않은 요청이면 적절한 HTTP 응답 코드로 대응하는 것까진 라이브러리가 해주지만 요청에 담긴 client_id가 존재하는지, 토큰 발급/삭제/검증 로직, 권한 확인 로직 등은 저장하는 것까지 개발자가 모두 구현해야 합니다. 흔한 로직으로 미리 구현까지 완료되어서 저장소만 연결하면 되는 라이브러리가 있을지 찾아봤었는데 적어도 Node.js 쪽에서는 없었습니다. Oauth provider를 만드는 경우가 드물어서 그런 것 같습니다.

라이브러리가 처리하는 영역은 대부분 믿고 맡길 만하나, 표준의 모호한 표현이나 모순된 설명으로 인해 제작자가 임의로 설정하는 로직이 종종 있습니다. 예를 들어 라이브러리가 구현한 /authorize controller에서 client_id뿐만 아니라 client_secret 값을 필수로 설정하는 경우가 있었습니다. 하지만 client_secret은 유저에게 노출되는 경로에서는 사용되면 안 되는 값입니다. 한참을 삽질하다 알고 보니 버그는 아니었고 특수한 시나리오에서 authorize 단계부터 client_secret을 활용할 수가 있어 일단 구현은 그렇게 해두었다, 필요 없으면 덮어써서 secret을 필수가 아니도록 처리하라는 가이드를 Github 이슈 한구석의 코멘트에서 찾을 수 있었습니다. 라이브러리가 오류를 뱉는다고 다 구현해주지 마시고 이상한 동작이 보이면 의문을 가지시길 바랍니다.

### 2. 테스트 환경 준비

개발 중에 client 입장, 유저 입장, provider 입장에서 요청을 보내고 기능을 따라다녀야 하는데, 도구가 없다면 굉장히 번거롭습니다.

client 입장의 테스트는 서버를 만드시길 추천해 드립니다. client는 Oauth provider와 데이터를 주고받으면서 유저까지 redirect를 사용해서 왔다 갔다 시켜야 하며 하고 받은 토큰 등 state도 유지해야 합니다. Oauth 서버와 client의 통신은 간단한 request가 아니기 때문에 client는 샘플 서버로 만들어 어느 정도 기능 구현을 해두고 로그를 듬뿍 찍으시길 바랍니다.

처음에는 postman으로 몇몇 request 샘플만 만들어 작업했는데, 하다 보니 매번 새로 생기는 토큰을 계속 복사해 붙이는 등 state 유지 때문에 감당이 안 되었습니다. Node.js 진영에는 passport와 같은 Oauth client가 잘 구현된 것들이 있어 쉽게 만들 수 있었습니다. user 입장에서의 테스트는 client 서버에 테스트 기능을 구현해서 하시면 됩니다.

### 3. 구현

Oauth provider 작업은 크게 5단계로 나눌 수 있습니다. (걸린 시간이 적당한 비슷하도록 나눴습니다)

1. Oauth 표준 이해하기
2. 로그인 flow 설계 + 토큰 정책 설계 + 저장소 준비
3. 라이브러리에서 개발자 구현으로 남겨둔 로직 구현
4. 문서화, 내부 테스트, Code Review
5. client 개발자와의 QA 및 기능수정

작업하다 보면 분명 있을법한 시나리오인데 표준에는 어떻게 해야 하는지 설명이 없는 경우를 보실 겁니다. 일단 어떻게 해야 하는지 찾아보셔야 하겠지만 표준이 rough하고 구현사례가 적기 때문에 쉽게 정보를 얻기 어렵습니다. 적당히 찾아보시고 현재 상황에 알맞은 방법으로 직접 결정하고 문서로 설명하시면 됩니다.

### 4. client 용 가이드 문서

표준대로 구현한 부분도 다시 문서를 작성하시길 추천해 드립니다. 표준대로 개발한 건 또 설명할 필요가 없다 느끼실 수 있지만, 독자(client 개발자) 입장에서 문서 두 개를 동시에 보는 것은 혼란스럽고 어떤 부분이 커스텀 되어있는지 불안해하면서 읽습니다. 처음부터 끝까지 완전한 문서를 제공하는 것이 좋습니다. 구글, 페이스북, github 등도 end to end 가이드를 제공하고 있습니다.

표준에 없지만, 특별히 문서에 포함되어야 하는 내용을 추려봤습니다

- 유저가 로그인 화면을 볼 수 있는 endpoint가 어디인지 (랜딩할 곳)
- 토큰의 길이, expire, 재발급 정책
- resource endpoint 및 access_token을 사용해서 resource를 얻는 방법 예시
- 어떤 resource를 제공하는지 catalog

---

제가 작업할 때는 자료가 없어 고생을 좀 했습니다. Oauth 서버 구현하시는 분들께 이 글이 도움이 되었으면 좋겠습니다. 읽어주셔서 감사합니다!
